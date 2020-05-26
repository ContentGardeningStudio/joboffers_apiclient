import os
from urllib.parse import urlencode

import requests


def get_supported_api_conf(name):

    conf = {}
    if name == "githubjobs":
        conf = {"url": "https://jobs.github.com/positions.json", "method": "GET"}
    elif name == "apec":
        auth_key = os.environ.get("APEC_API_KEY", "")
        if not auth_key:
            print(
                "WARNING: You need to provide the API authentication key as an environment variable!"
            )

        conf = {
            "url": "https://api-beta.dashblock.com/apec_jobs/search",
            "method": "POST",
            "auth_key": auth_key,
        }
    return conf


def get_offers(api_name, params=None):
    """ Get offers by submitting a POST request to an API we use """

    conf = get_supported_api_conf(name=api_name)

    if not conf:
        print("'{}' is not a supported API".format(api_name))
        return []

    params = params or {}
    paginate_max = params.get("paginate_max", 1)

    if "location" not in params:
        print("Calls without specifying a 'location' are not allowed")
        return []

    # prepare the request parameters
    req_params = {"location": params["location"]}

    api_url = conf["url"]
    api_method = conf["method"].lower()
    # auth key, in case it is an API with auth
    api_auth_key = conf.get("auth_key", "")

    # prepare the function we need for the HTTP calls
    func = getattr(requests, api_method)

    # The headers
    headers = {"Connection": "close"}
    if api_auth_key:
        headers["Authorization"] = "Basic {}".format(api_auth_key)

    # Init. the offers list
    offers = []

    if api_name == "githubjobs":
        # todo: check if pagination here starts at 0 or 1.
        for i in range(1, paginate_max + 1):
            print("Getting job positions from the page #{}...".format(i))
            req_params["page"] = str(i)
            qs = urlencode(req_params)
            resp = func("{}?{}".format(api_url, qs), headers=headers)

            if resp.status_code == 200:
                res = list(resp.json())
                print("==> Found {} jobs from page #{}".format(len(res), i))
                offers = offers + res
            else:
                print(
                    "==> Response code {} for the GET request on page '{}'".format(
                        resp.status_code, i
                    )
                )
    elif api_name == "apec":
        for i in range(1, paginate_max + 1):
            print("Getting job offers from the results page #{}...".format(i))
            req_params["page"] = i
            resp = func(api_url, data=req_params, headers=headers)

            if resp.status_code == 200:
                res = list(resp.json())
                print("==> Found {} job offers from page #{}".format(len(res), i))
                offers = offers + res
            else:
                print(
                    "==> Response code {} for the POST request with data {}".format(
                        resp.status_code, req_params
                    )
                )

    return offers
