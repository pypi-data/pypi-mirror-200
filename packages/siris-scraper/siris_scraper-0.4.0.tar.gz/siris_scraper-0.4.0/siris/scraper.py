# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from statscraper import (BaseScraper, Collection, DimensionValue,
                         Dataset, Dimension, Result)
from siris.utils import get_data_from_xml, parse_period, parse_value, iter_options
from copy import deepcopy

BASE_URL = u"http://siris.skolverket.se"


class ScraperUtils():
    ###
    # HELPER METHODS
    ###
    def _get_html(self, url):
        """ Get html from url
        """
        self.log.info(u"/GET {}".format(url))
        r = requests.get(url)
        if hasattr(r, 'from_cache'):
            if r.from_cache:
                self.log.info("(from cache)")

        r.raise_for_status()
        
        return r.text

    def _post_html(self, url, payload):
        self.log.info(u"/POST {} with {}".format(url, payload))
        r = requests.post(url, payload)
        r.raise_for_status()

        return r.content

    def _get_json(self, url):
        """ Get json from url
        """
        self.log.info(u"/GET " + url)
        r = requests.get(url)
        if hasattr(r, 'from_cache'):
            if r.from_cache:
                self.log.info("(from cache)")
        r.raise_for_status()

        return r.json()


    @property
    def log(self):
        if not hasattr(self, "_logger"):
            self._logger = PrintLogger()
        return self._logger

class SirisScraper(BaseScraper, ScraperUtils):

    def _fetch_itemslist(self, current_item):
        # Get start page
        if current_item.is_root:
            # Nivå 1: Välj skolform 
            url = BASE_URL + "/siris/reports/export_api/verksamhetsformer/"
            resp = self._get_json(url)
            for d in resp["verksamhetsformer"]:
                yield Skolform(d["kod"], d["namn"])

        elif isinstance(current_item, Skolform):
            # Nivå 2: Välj nivå 
            verk_form_id = current_item.id

            url = f"{BASE_URL}/siris/reports/export_api/niva/?pVerkform={verk_form_id}"
            resp = self._get_json(url)
            for d in resp:
                yield Niva(d["kod"], d["namn"])

        elif isinstance(current_item, Niva):
            # Nivå 3: Välj statistikområde 
            verk_form_id = current_item.parent.id
            niva_id = current_item.id
            url = f"{BASE_URL}/siris/reports/export_api/omrade/?pVerkform={verk_form_id}&pNiva={niva_id}"

            resp = self._get_json(url)
            for d in resp:
                yield Statistikomrade(d["kod"], d["namn"])
            
        elif isinstance(current_item, Statistikomrade):
            # Nivå 4: Välj export 
            verk_form_id = current_item.parent.parent.id
            niva_id = current_item.parent.id
            omr_id = current_item.id
            url = f"{BASE_URL}/siris/reports/export_api/export/?pVerkform={verk_form_id}&pNiva={niva_id}&pOmrade={omr_id}"
            resp = self._get_json(url)

            for d in resp:
                yield SirisDataset(d["kod"], d["namn"])


        elif isinstance(current_item, SirisDataset):
            url = f"{BASE_URL}/siris/reports/export_api/niva/?pVerkform={current_item.id}"

            # Get links to datasets


    def _fetch_allowed_values(self, dimension):
        """Allowed values are only implemented for regions.
        Ie units would need to be fetched trough an json api.
        """
        pass

    def _fetch_dimensions(self, dataset):
        yield Dimension("niva") # skola|kommun|län
        yield Dimension("kommunkod")
        yield Dimension("kommun_namn")
        yield Dimension("lan_kod")
        yield Dimension("lan_namn")
        yield Dimension("huvudman")
        yield Dimension("huvudman_name")
        yield Dimension("skolnamn")
        yield Dimension("skol_kod")
        yield Dimension("amne")
        yield Dimension("period")
        yield Dimension("periodicity")
        yield Dimension("uttag")
        yield Dimension("variable")
        yield Dimension("status")


    def _fetch_data(self, dataset, query):
        """Make the actual query.

        The only queryable dimensions are period.

        >>> dataset.fetch({"period": "2016"})
        >>> dataset.fetch({"period": ["2015", "2016"]})
        >>> dataset.fetch({"period": "*"}) # Get all periods
        """
        default_query = {
            "period": dataset.latest_period[1],
        }
        if query is None:
            query = default_query
        else:
            default_query.update(query)
            query = default_query

        allowed_query_dims = ["period"]

        for dim in query.keys():
            if dim not in allowed_query_dims:
                msg = "Querying on {} is not implemented yet".format(dim)
                raise NotImplementedError(msg)

        if query["period"] == "*":
            periods = [x[1] for x in dataset.periods]
        else:
            if not isinstance(query["period"], list):
                periods = [query["period"]]
            else:
                periods = query["period"]
        periods = [dataset._get_period_id(x) for x in periods]

        for period in periods:
            url = dataset.get_export_file_url(period, format="xml")
            xml_data = self._get_html(url)
            for datapoint in get_data_from_xml(xml_data):
                value = datapoint["value"]
                del datapoint["value"]
                yield Result(value, datapoint)

class SirisDataset(Dataset, ScraperUtils):

    def get_url(self, period=None, uttag=1):
        """Get the url for a spefic period and uttag.

        TODO: Make this work with uttag labels as well (dates)

        :param period: a period id (ie "2015")
        :param uttag: an uttag id (typically 1|2)
        """
        url = deepcopy(self.url)

        if period is not None:
            url += "&psAr={}".format(period)
        if uttag is not None:
            url += "&psOmgang={}".format(uttag)

        return url

    def get_export_file_url(self, period, format="xml", uttag=1):
        """Get download link."""
        return f"{BASE_URL}/siris/reports/export_api/runexport/?pFormat={format}&pExportID={self.id}&pAr={period}&pLan=&pKommun=&pHmantyp=&pUttag={uttag}&pFlikar=1"

    @property
    def periods(self):
        """Get all available periods (years, semesters)."""
        if not hasattr(self, "_periods"):
            url = f"{BASE_URL}/siris/reports/export_api/lasar/?pExportID={self.id}"
            resp = self._get_json(url)
            self._periods = [(x["kod"], x["namn"]) for x in resp["data"]]

        return self._periods

    def extra_filters(self, year):
        """Get options for 'Begränsa träfflista' """
        url = f"{BASE_URL}/siris/reports/export_api/extra/?pExportID={self.id}&pAr={year}"


    @property
    def latest_period(self):
        """Get the latest timepoint available in dataset."""
        return self.periods[0]

    @property
    def has_uttag(self):
        """Some dataset (like lärarebehörighet) my be published multiple
        times per year (="uttag"). This property checks if this is such a
        dataset.
        """
        raise NotImplementedError("Not implemented in with latest API")

    def get_uttag(self, period):
        """Get all available 'uttag' in a given period (year).
        Uttag are relevant to "lärarbehörighet" that some years (ie 2014/15)
        have been published multiple times

        :param period: a period id
        :returns: id and label of all uttag (if any) as tuples
        """
        url = self.get_url(period)
        html = self.scraper._get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        select_elem = soup.select_one("select[name='psOmgang']")
        return [(x[0], x[1]) for x in iter_options(select_elem)]

    def get_latest_uttag(self, period):
        """Get the uttag that appaear first in list. Uttag differ from year to year.

        :returns: id and label of latest uttag (if any) as tuple
        """
        uttag = [x for x in self.get_uttag(period)]
        if len(uttag) > 0:
            return uttag[0]
        else:
            return None


    def _get_period_id(self, period_label):
        if not hasattr(self, "_period_translation"):
            self._period_translation = dict([(x[1], x[0]) for x in self.periods])
        return self._period_translation[period_label]



    @property
    def html(self):
        if not hasattr(self, "_html"):
            self._html = self.scraper._get_html(self.url)
        return self._html


    @property
    def soup(self):
        if not hasattr(self, "_soup"):
            self._soup = BeautifulSoup(self.html, 'html.parser')
        return self._soup


class Skolform(Collection):
    pass

class Niva(Collection):
    pass

class Statistikomrade(Collection):
    pass


class SirisDimension(Dimension):
    """docstring for VantetiderDimension"""
    pass




class PrintLogger():
    """ Empyt "fake" logger
    """

    def log(self, msg, *args, **kwargs):
        print(msg)

    def debug(self, msg, *args, **kwargs):
        print(msg)

    def info(self, msg, *args, **kwargs):
        print(msg)

    def warning(self, msg, *args, **kwargs):
        print(msg)

    def error(self, msg, *args, **kwargs):
        print(msg)

    def critical(self, msg, *args, **kwargs):
        print(msg)
