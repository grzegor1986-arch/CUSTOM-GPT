"""Payment routes for Stripe checkout and webhook events."""

from fastapi import APIRouter, Request

from services.revenue_tracker import track_revenue_event
from services.stripe_service import create_checkout, parse_webhook

router = APIRouter(tags=["payments"])


@router.get("/checkout")
def checkout() -> dict[str, str]:
    """Create checkout session and return the URL."""
    url = create_checkout()
    return {"url": url}


@router.post("/webhook")
async def webhook(req: Request) -> dict[str, bool]:
    """Handle Stripe webhook events."""
    payload = await req.body()
    signature = req.headers.get("stripe-signature")
    event = parse_webhook(payload=payload, signature=signature)

    if event["type"] == "checkout.session.completed":
        track_revenue_event("checkout.session.completed", dict(event))
        print("💸 PAYMENT RECEIVED")

    return {"ok": True}
