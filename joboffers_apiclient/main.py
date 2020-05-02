import requests

SUPPORTED_APIS = {
    "githubjobs": {"url": "https://jobs.github.com/positions.json", "method": "GET"},
    "apec": {
        "url": "https://api-beta.dashblock.com/apec_jobs/search",
        "method": "POST",
    },
}


# Design notes:
# - Impose using location + pagination.


def get_offers(api_name, auth_key="", params=None):
    """ Get offers by submitting a POST request to an API we use """

    if api_name not in SUPPORTED_APIS:
        print("'{}' is not a supported API".format(api_name))
        return []

    # The params (used as query string for GET or as 'body' parameter for POST)
    params = params or {}
    paginate_max = params.get("paginate_max", 1)

    if "location" not in params:
        print("Calls without specifying a 'location' are not allowed")
        return []

    api_url = SUPPORTED_APIS[api_name]["url"]
    api_method = SUPPORTED_APIS[api_name]["method"].lower()
    # prepare the function we need for the HTTP calls
    func = getattr(requests, api_method)

    # The headers
    headers = {"Connection": "close"}
    if auth_key:
        headers["Authorization"] = "Basic {}".format(auth_key)

    # Init. the offers list
    offers = []

    if api_name == "githubjobs":
        # todo: IMPORTANT / add 'location' to the request parameters.
        # todo: check if pagination here starts at 0 or 1.
        for i in range(1, paginate_max + 1):
            print("Getting job positions from the page #{}...".format(i))
            resp = func(api_url + "?page=" + str(i), headers=headers)

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
        body = {"department_code": params["location"]}

        for i in range(1, paginate_max + 1):
            print("Getting job offers from the results page #{}...".format(i))
            body["page"] = i
            resp = func(api_url, data=body, headers=headers)

            if resp.status_code == 200:
                res = list(resp.json())
                print("==> Found {} job offers from page #{}".format(len(res), i))
                offers = offers + res
            else:
                print(
                    "==> Response code {} for the POST request with data {}".format(
                        resp.status_code, body
                    )
                )

    return offers
