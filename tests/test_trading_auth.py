import httpx
from defusedxml.ElementTree import fromstring

from ebay_apiroute.trading import TradingApi
from ebay_apiroute.trading_version import TRADING_VERSION

ENV = "http://schemas.xmlsoap.org/soap/envelope/"
EBAY = "urn:ebay:apis:eBLBaseComponents"

RESPONSE = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="{ENV}"><soapenv:Body>
<GetItemResponse xmlns="{EBAY}"><Timestamp>2026-10-23T12:00:00.000Z</Timestamp><Ack>Success</Ack>
<Version>{TRADING_VERSION}</Version><Item><ItemID>123</ItemID><Title>A thing</Title></Item>
</GetItemResponse></soapenv:Body></soapenv:Envelope>"""


def test_soap_credentials_and_query(transport, recorder):
    recorder.respond(httpx.Response(200, content=RESPONSE.encode()))
    trading = TradingApi("AgAA-token", app_id="MyApp-1", site_id=3, transport=transport)
    result = trading.get_item(body={"ItemID": "123"})
    request = recorder.last
    assert request.url.host == "api.ebay.com" and request.url.path == "/wsapi"
    assert dict(request.url.params) == {
        "callname": "GetItem",
        "siteid": "3",
        "appid": "MyApp-1",
        "version": TRADING_VERSION,
        "routing": "new",
    }
    envelope = fromstring(request.content)
    token = envelope.find(f"{{{ENV}}}Header/{{{EBAY}}}RequesterCredentials/{{{EBAY}}}eBayAuthToken")
    assert token.text == "AgAA-token"
    assert envelope.find(f"{{{ENV}}}Body/{{{EBAY}}}GetItemRequest/{{{EBAY}}}ItemID").text == "123"
    assert result["Ack"] == "Success" and result["Item"]["Title"] == "A thing"


def test_typed_trading_call(transport, recorder):
    recorder.respond(httpx.Response(200, content=RESPONSE.encode()))
    trading = TradingApi("t", app_id="a", transport=transport)
    response = trading.models.get_item(body={"ItemID": "123"})
    assert response.ack == "Success" and response.item.title == "A thing"


def test_sandbox(transport, recorder):
    recorder.respond(httpx.Response(200, content=RESPONSE.encode()))
    TradingApi("t", app_id="a", sandbox=True, transport=transport).get_item(body={"ItemID": "1"})
    assert recorder.last.url.host == "api.sandbox.ebay.com"
