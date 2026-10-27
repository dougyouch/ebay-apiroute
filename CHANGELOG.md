# Changelog

## [0.3.0](https://github.com/dougyouch/ebay-apiroute/compare/v0.2.0...v0.3.0) (2026-10-27)


### Features

* **specs:** update clients from eBay's latest API specs ([aca3fb1](https://github.com/dougyouch/ebay-apiroute/commit/aca3fb11e27e1e7dfbc827127f5c4de4e4feb4ca))

## [0.2.0](https://github.com/dougyouch/ebay-apiroute/compare/v0.1.1...v0.2.0) (2026-10-27)


### Features

* retry calls that are safe to repeat after a read timeout ([9a77c24](https://github.com/dougyouch/ebay-apiroute/commit/9a77c24bf8b9f1fc8f79a64ab293703b2a3250bf))


### Bug Fixes

* regenerate with apiroute 2.2 and require pydantic 2.6 ([1ff0723](https://github.com/dougyouch/ebay-apiroute/commit/1ff072329e3de7d4d495cd06990e78b92d417b1c))

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
