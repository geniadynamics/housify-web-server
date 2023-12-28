from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.data.schemas.credit_card import CreditCardSchema

router = APIRouter()

#
# async def create_credit_card(credit_card: CreditCardSchema):
#     pass
#
#
# async def get_credit_card(credit_card_id: int):
#     pass
#
#
# async def update_credit_card(credit_card_id: int, credit_card: CreditCardSchema):
#     pass
#
#
# async def delete_credit_card(credit_card_id: int):
#     pass
#
#
# @router.post("/credit-cards/", response_model=CreditCardSchema)
# async def create_credit_card_endpoint(credit_card: CreditCardSchema):
#     """
#     Create a new credit card instance.
#     """
#     await create_credit_card(credit_card)
#     return credit_card
#
#
# @router.get("/credit-cards/{credit_card_id}", response_model=CreditCardSchema,
#             responses={404: {"model": HTTPNotFoundError}})
# async def read_credit_card_endpoint(credit_card_id: int):
#     """
#     Retrieve the details of a specific credit card.
#     """
#     credit_card = await get_credit_card(credit_card_id)
#     if credit_card is not None:
#         return credit_card
#     raise HTTPException(status_code=404, detail="Credit card not found")
#
#
# @router.put("/credit-cards/{credit_card_id}", response_model=CreditCardSchema,
#             responses={404: {"model": HTTPNotFoundError}})
# async def update_credit_card_endpoint(credit_card_id: int, credit_card: CreditCardSchema):
#     """
#     Update the details of a specific credit card.
#     """
#     updated_credit_card = await update_credit_card(credit_card_id, credit_card)
#     if updated_credit_card is not None:
#         return updated_credit_card
#     raise HTTPException(status_code=404, detail="Credit card not found")
#
#
# @router.delete("/credit-cards/{credit_card_id}", response_model=dict, responses={404: {"model": HTTPNotFoundError}})
# async def delete_credit_card_endpoint(credit_card_id: int):
#     """
#     Delete a specific credit card.
#     """
#     await delete_credit_card(credit_card_id)
#     return {"status": "success"}
