from zeep import Client
from fastapi import APIRouter


router = APIRouter()
soap_client = Client("http://localhost:5262/CryptoRateService.svc?wsdl")


@router.get("/soap/crypto-rate/{symbol}")
async def get_crypto_rate(symbol: str):
    """
    Uses SOAP to get the cryptocurrency rate for a specified symbol
    """
    response = soap_client.service.GetCryptoRate(symbol)
    return {"symbol": response.Symbol, "price": response.Price}


@router.get("/soap/all-crypto-rates")
async def get_all_crypto_rates():
    """
    Uses SOAP to get all cryptocurrency rates stored in the database.
    """
    responses = soap_client.service.GetAllCryptoRates()
    return [{"symbol": rate.Symbol, "price": rate.Price} for rate in responses]
