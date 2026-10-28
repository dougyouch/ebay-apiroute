"""The REST clients' _all methods page as eBay does (over a mock transport)."""

import httpx
import pytest
from apiroute.testing import MockTransport

from ebay_apiroute.commerce.notification import CommerceNotificationApi
from ebay_apiroute.sell.finances import SellFinancesApi
from ebay_apiroute.sell.inventory import SellInventoryApi


@pytest.fixture
def mock():
    return MockTransport()


def items_page(skus, total):
    return httpx.Response(200, json={"inventoryItems": [{"sku": s} for s in skus], "total": total})


def test_offset_lists_page_until_the_total(mock):
    api = SellInventoryApi("t0k", transport=mock)
    mock.respond(items_page(["a", "b"], 3), items_page(["c"], 3))
    skus = [i["sku"] for i in api.inventory_item.get_inventory_items_all(limit="2")]
    assert skus == ["a", "b", "c"]
    assert [(c.params.get("offset"), c.params["limit"]) for c in mock.calls] == [
        (None, "2"),
        ("2", "2"),
    ]
    assert all(call.headers["Authorization"] == "Bearer t0k" for call in mock.calls)


def test_typed_items(mock):
    api = SellInventoryApi("t0k", transport=mock)
    mock.respond(items_page(["a"], 1))
    assert [i.sku for i in api.inventory_item.models.get_inventory_items_all()] == ["a"]


def test_sandbox_and_other_hosts_keep_their_host(mock):
    api = SellFinancesApi("t0k", sandbox=True, transport=mock)
    mock.respond(httpx.Response(200, json={"payouts": [{"payoutId": "1"}], "total": 1}))
    assert len(list(api.payout.get_payouts_all(x_ebay_c_marketplace_id="EBAY_US"))) == 1
    assert mock.last.url.host == "apiz.sandbox.ebay.com"


def test_continuation_tokens_follow_the_next_url(mock):
    api = CommerceNotificationApi("t0k", transport=mock)
    base = "https://api.ebay.com/commerce/notification/v1/topic"
    mock.respond(
        httpx.Response(
            200, json={"topics": [{"topicId": "A"}], "next": f"{base}?continuation_token=c2"}
        ),
        httpx.Response(200, json={"topics": [{"topicId": "B"}]}),
    )
    assert [t["topicId"] for t in api.topic.get_topics_all()] == ["A", "B"]
    assert mock.last.params["continuation_token"] == "c2"
