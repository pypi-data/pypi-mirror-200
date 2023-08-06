"""Payment models."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .merchant import _MerchantData


class PaymentOperation(Enum):
    """Payment operation."""

    PAYMENT = "payment"
    ONE_CLICK_PAYMENT = "oneclickPayment"
    CUSTOM_PAYMENT = "customPayment"


class PaymentMethod(Enum):
    """Payment method."""

    CARD = "card"
    CARD_LVP = "card#LVP"


@dataclass(frozen=True)
class PaymentInfo:
    """Payment information."""

    pay_id: str
    payment_status: Optional[int] = None
    customer_code: Optional[str] = None
    status_detail: Optional[str] = None
    auth_code: Optional[str] = None
    merchant_data: Optional[bytes] = None

    @classmethod
    def from_response(cls, response: dict) -> "PaymentInfo":
        """Create a PaymentInfo object from a response dictionary."""
        merchant_data = response.get("merchantData")
        if merchant_data is not None:
            merchant_data = _MerchantData.from_base64(merchant_data).data

        return cls(
            response["payId"],
            payment_status=response.get("paymentStatus"),
            customer_code=response.get("customerCode"),
            status_detail=response.get("statusDetail"),
            auth_code=response.get("authCode"),
            merchant_data=merchant_data,
        )
