import httpx
import pytest

from ebay_apiroute.auth import sandbox_url
from ebay_apiroute.sell.inventory import SellInventoryApi


def test_bearer_token_marketplace_and_lazy_sections(transport, recorder):
    api = SellInventoryApi("t0k", marketplace_id="EBAY_US", transport=transport)
    api.inventory_item.get_inventory_item("SKU 1")
    request = recorder.last
    assert str(request.url) == "https://api.ebay.com/sell/inventory/v1/inventory_item/SKU%201"
    assert request.headers["Authorization"] == "Bearer t0k"
    assert request.headers["X-EBAY-C-MARKETPLACE-ID"] == "EBAY_US"


def test_a_token_function_is_called_per_request(transport, recorder):
    tokens = iter(["first", "second"])
    api = SellInventoryApi(lambda: next(tokens), transport=transport)
    api.inventory_item.get_inventory_item("a")
    api.inventory_item.get_inventory_item("b")
    assert [r.headers["Authorization"] for r in recorder.requests] == [
        "Bearer first",
        "Bearer second",
    ]


def test_no_token_sends_no_authorization(transport, recorder):
    SellInventoryApi(transport=transport).inventory_item.get_inventory_item("a")
    assert "Authorization" not in recorder.last.headers
    assert "X-EBAY-C-MARKETPLACE-ID" not in recorder.last.headers


def test_sandbox(transport, recorder):
    SellInventoryApi("t", sandbox=True, transport=transport).inventory_item.get_inventory_item("a")
    assert recorder.last.url.host == "api.sandbox.ebay.com"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://api.ebay.com/sell/v1", "https://api.sandbox.ebay.com/sell/v1"),
        ("https://apiz.ebay.com/x", "https://apiz.sandbox.ebay.com/x"),
        ("https://api.sandbox.ebay.com/x", "https://api.sandbox.ebay.com/x"),
        ("https://example.com/x", "https://example.com/x"),
    ],
)
def test_sandbox_url(url, expected):
    assert sandbox_url(url) == expected


def test_typed_layer(transport, recorder):
    recorder.respond(
        httpx.Response(
            200,
            json={
                "sku": "SKU1",
                "condition": "NEW",
                "availability": {"shipToLocationAvailability": {"quantity": 3}},
            },
        )
    )
    item = SellInventoryApi("t", transport=transport).inventory_item.models.get_inventory_item(
        "SKU1"
    )
    assert item.sku == "SKU1" and item.condition == "NEW"
    assert item.availability.ship_to_location_availability.quantity == 3


@pytest.mark.parametrize(
    "call, attempts",
    [
        (lambda api: api.offer.update_offer("o1", body={}, content_language="en-US"), 2),  # PUT
        (lambda api: api.offer.delete_offer("o1"), 2),  # DELETE
        (lambda api: api.offer.create_offer(body={}, content_language="en-US"), 1),  # POST
    ],
)
def test_put_and_delete_are_retried_after_a_read_timeout_and_post_is_not(call, attempts):
    from apiroute import Retries
    from apiroute.testing import MockTransport

    mock = MockTransport()
    mock.respond(httpx.ReadTimeout("slow"), httpx.Response(200, json={}))
    api = SellInventoryApi(token="t", transport=mock).with_options(
        retries=Retries(attempts=3, sleep=0)
    )
    try:
        call(api)
    except httpx.ReadTimeout:
        pass
    assert len(mock.calls) == attempts
