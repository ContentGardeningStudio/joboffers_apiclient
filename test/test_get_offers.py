from joboffers_apiclient import get_offers


def test_get_offers_not_supported():
    results = get_offers("some.random.api")
    assert results == []


def test_get_offers_no_location():
    results = get_offers("apec", auth_key="dummy", params={})
    assert results == []


def test_get_offers_not_authorized():
    results = get_offers("apec", auth_key="dummy", params={"location": "any"})
    assert results == []
