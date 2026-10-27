# Changelog

## [0.1.1](https://github.com/dougyouch/ebay-apiroute/compare/v0.1.0...v0.1.1) (2026-10-26)


### Documentation

* date the 0.1.0 changelog entry ([9292bae](https://github.com/dougyouch/ebay-apiroute/commit/9292baea89b4ff8fcc0b38754e1c5a65e9060651))

## [0.1.0] - 2026-10-23

### Added

- Generated clients for 29 eBay REST APIs (Buy, Sell, Commerce, Developer) from eBay's OpenAPI 3 contracts, and for the Trading API from its WSDL, with dict and pydantic model layers, sync and async.
- `EbayAuth`: OAuth access tokens (strings, or functions returning the current one), `X-EBAY-C-MARKETPLACE-ID`, and the sandbox.
- `TradingAuth`: `RequesterCredentials` in the SOAP header, plus the call name, site, application ID and version in the query.
- Weekly Build workflow that refetches the specs, regenerates and commits changes; CI that checks the generated code matches the committed specs; release-please and PyPI trusted publishing.

[0.1.0]: https://github.com/dougyouch/ebay-apiroute/releases/tag/v0.1.0
