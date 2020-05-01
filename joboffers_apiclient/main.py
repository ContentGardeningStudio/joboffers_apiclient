import requests


def get_offers(api_url, auth_key="", params=None):
    """ Get offers by submitting a POST request to an API we use """

    headers = {"Connection": "close"}
    if auth_key:
        headers["Authorization"] = "Basic {}".format(auth_key)

    params = params or {}

    # prepare 'body' for the POST request
    body = {}
    if "department_code" in params:
        body["department_code"] = params["department_code"]

    offers = []

    # If there is pagination
    if "paginate_max" in params:
        for i in range(1, params["paginate_max"] + 1):
            print("Getting job offers from the results page #{}...".format(i))
            body["page"] = i
            resp = requests.post(api_url, data=body, headers=headers)
            if resp.status_code == 200:
                res = list(resp.json())
                print("==> Found {} job offers from page #{}".format(len(res), i))
                offers = offers + res
            else:
                print("==> Got response code {} for request params: {}".format(resp.status_code, body))
    else:
        # case we need to test, with another api example / endpoint
        resp = requests.post(api_url, data=body, headers=headers)
        offers = list(resp.json())

    return offers
