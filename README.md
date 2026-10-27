# ebay-apiroute

[![CI](https://github.com/dougyouch/ebay-apiroute/actions/workflows/ci.yml/badge.svg)](https://github.com/dougyouch/ebay-apiroute/actions/workflows/ci.yml)
[![Build](https://github.com/dougyouch/ebay-apiroute/actions/workflows/build.yml/badge.svg)](https://github.com/dougyouch/ebay-apiroute/actions/workflows/build.yml)

Python clients for eBay's REST APIs and its Trading API, generated with [apiroute](https://github.com/dougyouch/apiroute) from the API specs eBay publishes, and kept current by a weekly build.

- **Two layers:** every call works with plain dicts (`api.inventory_item.get_inventory_item("SKU1")`), and `.models` takes and returns typed pydantic models (`api.inventory_item.models.get_inventory_item("SKU1")`).
- **Sync and async:** add `.aio` to any call for the async version.
- **Lazy loading:** only the APIs, sections and models you use are imported, so a script that calls one endpoint stays fast, though the package covers 30 APIs and about 1,400 models.

## Installation

```bash
pip install ebay-apiroute    # or: uv add ebay-apiroute
```

It needs Python 3.10 or newer.

## REST APIs

Every REST client takes an OAuth access token. The token can be a string, or a function that returns the current one, which suits code that refreshes tokens.

```python
from ebay_apiroute.sell.inventory import SellInventoryApi

api = SellInventoryApi(token="v^1.1#i^1#...", marketplace_id="EBAY_US")

item = api.inventory_item.get_inventory_item("SKU1")  # a dict
item = api.inventory_item.models.get_inventory_item("SKU1")  # InventoryItemWithSkuLocaleGroupid
items = await api.inventory_item.models.aio.get_inventory_items(limit="25")

sandbox = SellInventoryApi(token=refreshing_token, sandbox=True)  # api.sandbox.ebay.com
```

- `marketplace_id` is sent as the `X-EBAY-C-MARKETPLACE-ID` header.
- `sandbox=True` switches to eBay's sandbox hosts.
- Getting tokens is up to your application. eBay's [OAuth guide](https://developer.ebay.com/api-docs/static/oauth-tokens.html) covers application tokens (the [client credentials grant](https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html)) and user tokens (the [authorization code grant](https://developer.ebay.com/api-docs/static/oauth-authorization-code-grant.html)).

## Trading API

The Trading API is SOAP. Its client sends your token in the `RequesterCredentials` SOAP header, and adds the call name, site, application ID and API version to each request, as eBay's SOAP endpoint requires.

```python
from ebay_apiroute.trading import TradingApi

trading = TradingApi(token="AgAAAA...", app_id="MyApp-PRD-...", site_id=0)
response = trading.get_item(body={"ItemID": "123456789", "DetailLevel": "ReturnAll"})
response = trading.models.get_item(body={"ItemID": "123456789"})  # GetItemResponseType
```

Bodies and responses use the xmltodict shape:
- child elements are keys
- `"@name"` is an attribute
- `"#text"` is an element's text

A SOAP fault raises `apiroute.soap.SoapFault`. The API version comes from the WSDL (`ebay_apiroute.trading_version.TRADING_VERSION`); pass `version=` to override it.

## APIs

<!-- apis:start -->
| API | Import | Docs |
| --- | --- | --- |
| Browse API | `from ebay_apiroute.buy.browse import BuyBrowseApi` | [docs](https://developer.ebay.com/api-docs/buy/static/api-browse.html) |
| Deal API | `from ebay_apiroute.buy.deal import BuyDealApi` | [docs](https://developer.ebay.com/api-docs/buy/static/api-deal.html) |
| Feed API (Buy) | `from ebay_apiroute.buy.feed import BuyFeedApi` | [docs](https://developer.ebay.com/api-docs/buy/feed/static/overview.html) |
| Buy Marketing API | `from ebay_apiroute.buy.marketing import BuyMarketingApi` | [docs](https://developer.ebay.com/api-docs/buy/marketing/static/overview.html) |
| Buy Offer API | `from ebay_apiroute.buy.offer import BuyOfferApi` | [docs](https://developer.ebay.com/api-docs/buy/offer/static/overview.html) |
| Order API | `from ebay_apiroute.buy.order import BuyOrderApi` | [docs](https://developer.ebay.com/api-docs/buy/order/static/overview.html) |
| Catalog API | `from ebay_apiroute.commerce.catalog import CommerceCatalogApi` | [docs](https://developer.ebay.com/api-docs/commerce/catalog/static/overview.html) |
| Charity API | `from ebay_apiroute.commerce.charity import CommerceCharityApi` | [docs](https://developer.ebay.com/api-docs/commerce/charity/static/overview.html) |
| Feedback API | `from ebay_apiroute.commerce.feedback import CommerceFeedbackApi` | [docs](https://developer.ebay.com/api-docs/commerce/feedback/static/overview.html) |
| Identity API | `from ebay_apiroute.commerce.identity import CommerceIdentityApi` | [docs](https://developer.ebay.com/api-docs/commerce/identity/resources/methods) |
| Media API | `from ebay_apiroute.commerce.media import CommerceMediaApi` | [docs](https://developer.ebay.com/api-docs/commerce/media/static/overview.html) |
| Message API | `from ebay_apiroute.commerce.message import CommerceMessageApi` | [docs](https://developer.ebay.com/api-docs/commerce/message/resources/methods) |
| Notification API | `from ebay_apiroute.commerce.notification import CommerceNotificationApi` | [docs](https://developer.ebay.com/api-docs/commerce/notification/static/overview.html) |
| Taxonomy API | `from ebay_apiroute.commerce.taxonomy import CommerceTaxonomyApi` | [docs](https://developer.ebay.com/api-docs/commerce/taxonomy/static/overview.html) |
| Translation API | `from ebay_apiroute.commerce.translation import CommerceTranslationApi` | [docs](https://developer.ebay.com/api-docs/commerce/translation/static/overview.html) |
| VeRO API | `from ebay_apiroute.commerce.vero import CommerceVeroApi` | [docs](https://developer.ebay.com/api-docs/commerce/vero/static/overview.html) |
| Developer Analytics API | `from ebay_apiroute.developer.analytics import DeveloperAnalyticsApi` | [docs](https://developer.ebay.com/api-docs/developer/analytics/resources/rate_limit/methods/getRateLimits) |
| Account API | `from ebay_apiroute.sell.account import SellAccountApi` | [docs](https://developer.ebay.com/api-docs/sell/account/static/overview.html) |
| Analytics API (Sell) | `from ebay_apiroute.sell.analytics import SellAnalyticsApi` | [docs](https://developer.ebay.com/api-docs/sell/analytics/static/overview.html) |
| Feed API (Sell) | `from ebay_apiroute.sell.feed import SellFeedApi` | [docs](https://developer.ebay.com/api-docs/sell/feed/static/overview.html) |
| Finances API | `from ebay_apiroute.sell.finances import SellFinancesApi` | [docs](https://developer.ebay.com/api-docs/sell/finances/overview.html) |
| Fulfillment API | `from ebay_apiroute.sell.fulfillment import SellFulfillmentApi` | [docs](https://developer.ebay.com/api-docs/sell/fulfillment/overview.html) |
| Inventory API | `from ebay_apiroute.sell.inventory import SellInventoryApi` | [docs](https://developer.ebay.com/api-docs/sell/inventory/static/overview.html) |
| Logistics API | `from ebay_apiroute.sell.logistics import SellLogisticsApi` | [docs](https://developer.ebay.com/api-docs/sell/logistics/static/overview.html) |
| Marketing API | `from ebay_apiroute.sell.marketing import SellMarketingApi` | [docs](https://developer.ebay.com/api-docs/sell/marketing/static/overview.html) |
| Metadata API | `from ebay_apiroute.sell.metadata import SellMetadataApi` | [docs](https://developer.ebay.com/api-docs/sell/metadata/overview.html) |
| Negotiation API | `from ebay_apiroute.sell.negotiation import SellNegotiationApi` | [docs](https://developer.ebay.com/api-docs/sell/negotiation/static/overview.html) |
| Recommendation API | `from ebay_apiroute.sell.recommendation import SellRecommendationApi` | [docs](https://developer.ebay.com/api-docs/sell/recommendation/static/overview.html) |
| Stores API | `from ebay_apiroute.sell.stores import SellStoresApi` | [docs](https://developer.ebay.com/api-docs/sell/stores/static/overview.html) |
| Trading API | `from ebay_apiroute.trading import TradingApi` | [docs](https://developer.ebay.com/devzone/xml/docs/reference/ebay/index.html) |
<!-- apis:end -->

Errors raise `apiroute.UnexpectedResponse`, which carries the `.response`. For retries, transports and other client options, see [apiroute's README](https://github.com/dougyouch/apiroute#readme).

Retries are off unless you turn them on, for example with `api.with_options(retries=3)`, or `retries = Retries(...)` in a subclass. Once on, failed connections are always retried. After a read timeout, though, only calls that are safe to repeat are retried: REST `GET`, `PUT` (eBay's create-or-replace) and `DELETE`, and the Trading API's read-only calls (`Get*`, and the `Verify*` calls, which validate without listing). Writes such as REST `POST`s and Trading's `AddItem` aren't, so an offer or a listing can't be created twice.

## How this repository stays up to date

Nothing under `src/ebay_apiroute/` is written by hand except `auth.py` and `__init__.py`. Everything else is generated from the API descriptions listed in [`apis.yaml`](apis.yaml):

1. Every Monday, the **[Build](.github/workflows/build.yml)** workflow does the following:
   - Upgrades apiroute to its newest release.
   - Downloads each spec again into [`specs/`](specs), the committed copy of what eBay publishes.
   - Regenerates the clients with `apiroute generate`.
   - Runs the lint and tests.
2. If anything changed, it commits the result to `main`:
   - `feat(specs): ...` when eBay changed a spec, which produces a minor release.
   - `fix(codegen): ...` when only a newer apiroute changed the generated code, which produces a patch release.
3. **[Release](.github/workflows/release.yml)** (release-please) then updates its release PR, tests it, merges it and publishes the new version to [PyPI](https://pypi.org/project/ebay-apiroute/). No one has to do anything: a new eBay spec or apiroute release reaches PyPI on its own once the tests pass.

[CI](.github/workflows/ci.yml) checks every push. It lints, runs the tests on Python 3.10 to 3.14, and regenerates from the committed specs to confirm the committed code matches them exactly.

Because `specs/` is committed, `git log -p specs/` shows exactly what eBay changed and when.

## Development

```bash
uv sync
uv run python scripts/generate.py --fetch      # download the latest specs, regenerate everything
uv run python scripts/generate.py --only trading   # regenerate one API from its committed spec
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

To add an API, add an entry to `apis.yaml`, run `scripts/generate.py --fetch`, then commit the spec and the generated code. The table above updates itself. Auth lives in [`src/ebay_apiroute/auth.py`](src/ebay_apiroute/auth.py), which the generated clients extend.

## License

MIT
