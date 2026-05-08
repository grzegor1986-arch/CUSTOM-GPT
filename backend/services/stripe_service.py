"""Stripe integration layer."""

import stripe
from fastapi import HTTPException

from config import settings


def _ensure_stripe_ready() -> None:
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=500, detail="Missing STRIPE_SECRET_KEY")
    if not settings.stripe_price_id:
        raise HTTPException(status_code=500, detail="Missing STRIPE_PRICE_ID")
    stripe.api_key = settings.stripe_secret_key


def create_checkout() -> str:
    """Create Stripe Checkout session and return redirect URL."""
    _ensure_stripe_ready()
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
        mode="subscription",
        success_url=settings.frontend_success_url,
        cancel_url=settings.frontend_cancel_url,
    )
    return str(session.url)


def parse_webhook(payload: bytes, signature: str | None) -> stripe.Event:
    """Validate and parse Stripe webhook event."""
    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=500, detail="Missing STRIPE_WEBHOOK_SECRET")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        return stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=settings.stripe_webhook_secret,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook payload") from exc
    except stripe.error.SignatureVerificationError as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook signature") from exc
