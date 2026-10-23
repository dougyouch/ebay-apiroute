# Changelog

## [0.1.0] - Unreleased

### Added

- Generated clients for 29 eBay REST APIs (Buy, Sell, Commerce, Developer) from eBay's OpenAPI 3 contracts, and for the Trading API from its WSDL, with dict and pydantic model layers, sync and async.
- `EbayAuth`: OAuth access tokens (strings, or functions returning the current one), `X-EBAY-C-MARKETPLACE-ID`, and the sandbox.
- `TradingAuth`: `RequesterCredentials` in the SOAP header, plus the call name, site, application ID and version in the query.
- Weekly Build workflow that refetches the specs, regenerates and commits changes; CI that checks the generated code matches the committed specs; release-please and PyPI trusted publishing.
