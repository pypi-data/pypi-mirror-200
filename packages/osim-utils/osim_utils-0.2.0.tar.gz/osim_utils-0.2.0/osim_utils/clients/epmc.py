import functools
import json
import requests
from osim_utils.logger import get_logger

from http import HTTPStatus
import osim_utils.exceptions as exc


# region decorators
def check_response(*args):
    """
    Checks that a call to a EuropePMC API client method returned an expected status code.
    Raises an AssertionError if the returned status code is unexpected.

    Args:
        *args (tuple): status codes that should NOT lead to an
            exception

    Returns:
        The response of the decorated method
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*inner_args, **kwargs):
            response = func(*inner_args, **kwargs)
            assert response.status_code in args, (
                f"API call initiated by {func.__module__}.{func.__name__} "
                f"returned error: {response.content}"
            )
            return response

        return wrapper

    return decorator


def process_response(func):
    """
    Processes the response of a call to a EuropePMC API client method
    so that only the body of the response is decoded form json and returned

    Returns:
        The json-decoded body of the response of the decorated method
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            return response.json()
        except json.JSONDecodeError:
            raise exc.ApiClientError(
                f"API call initiated by {func.__module__}.{func.__name__} "
                f"failed with error: {response.text}"
            )

    return wrapper


# endregion


class EpmcClient:
    """
    API client for EuropePMC Articles REST API
    (https://europepmc.org/RestfulWebService)
    """

    def __init__(self):
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/"
        self.common_params = {"format": "json"}
        self.session = requests.Session()
        self.logger = get_logger()

    @staticmethod
    def _check_query(**kwargs) -> str:
        """
        Check that required "query" argument was passed to calling method
        Args:
            **kwargs: calling method kwargs

        Returns: The query string
        """
        try:
            return kwargs["query"]
        except KeyError:
            raise ValueError(
                "You must include a 'query' parameter when calling this method"
            )

    @process_response
    @check_response(HTTPStatus.OK)
    def search(self, **kwargs) -> requests.models.Response:
        """
        Queries the publication database using the GET search endpoint

        Args:
            **kwargs:
                query (required; str): query string

        Returns: server's response to the search request
        """
        self._check_query(**kwargs)
        endpoint = f"{self.base_url}search"
        params = self.common_params | kwargs
        return self.session.get(endpoint, params=params)

    @process_response
    @check_response(HTTPStatus.OK)
    def search_post(self, **kwargs) -> requests.models.Response:
        """
        Queries the publication database using the POST searchPOST endpoint

        Args:
            **kwargs:
                query (str): query string
                resultType (str): It can have the following values:
                    lite (default): returns key metadata for the given search terms
                    idlist: returns a list of IDs and sources for the given search terms
                    core: returns full metadata for a given publication ID; including
                        abstract, full text links, and MeSH terms
                pageSize (int): defaults to 25 publications per page; maximum allowed is 1000

        Returns:
        """
        self._check_query(**kwargs)
        body = self.common_params | kwargs
        endpoint = f"{self.base_url}searchPOST/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        return self.session.post(endpoint, data=body, headers=headers)

    @staticmethod
    def escape_brackets(search_term: str) -> str:
        """
        Brackets have special meaning in EuropePMC queries. Thus, they must be escaped
        if they are part of search terms [for example, in the doi 10.1016/S2666-5247(22)00181-1]
        Args:
            search_term: the search term that might contain brackets to be escaped

        Returns: search_term with brackets escaped

        """
        return search_term.replace("(", "\(").replace(")", "\)")

    def query_doi(self, doi: str, **kwargs) -> dict:
        """
        Searches EuropePMC for publications whose DOI matches the doi argument.
        If zero or more than one result is found, raises an error

        Args:
            doi: A DOI string such as 10.1093/bioinformatics/btac311

        Returns: Dictionary representation of the publication matching the queried DOI
        """
        r = self.search(query=f"doi:{self.escape_brackets(doi)}", **kwargs)
        if (hit_count := r["hitCount"]) == 0:
            self.logger.info(f"Query for DOI {doi} did not return any results")
            return dict()
        else:
            assert 1 == hit_count, f"Query for DOI {doi} returned multiple results"
            return r["resultList"]["result"][0]

    def query_doi_list(self, **kwargs) -> dict:
        """
        Args:
            **kwargs:
                 doi_list (required, list): DOIs to query
                 any other kwargs to be passed to search_post (see documentation for that method)
        Returns:

        """
        doi_list = kwargs.pop("doi_list")
        page_size = kwargs.pop("pageSize", None)
        if page_size is None:
            page_size = 1000
        list_length = len(doi_list)
        escaped_list = [self.escape_brackets(doi) for doi in doi_list]
        assert page_size > list_length, (
            f"This method does not support pagination yet and "
            f"the number of DOIs queried ({list_length}) exceeds"
            f"pageSize ({page_size}). Either increase pageSize if possible"
            f"(server-side limit is 1000) or make more than one call to this method"
        )
        query = f"doi:({' OR '.join(escaped_list)})"
        response = self.search_post(query=query, pageSize=page_size, **kwargs)

        if (hit_count := response["hitCount"]) < list_length:
            self.logger.warning(
                "List of publications returned by EuropePMC shorter than queried DOI list",
                extra={"epmc_results": hit_count, "queried_dois": list_length},
            )

        doi_dict = dict()
        for r in response["resultList"]["result"]:
            try:
                doi_dict[r["doi"]] = r
            except KeyError:
                self.logger.error("No doi field!", extra=r)

        return doi_dict
