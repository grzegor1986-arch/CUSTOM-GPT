"""Minimal Vercel deployment helper."""

import requests
from fastapi import HTTPException

from config import settings


def deploy_frontend() -> dict:
    """Trigger a Vercel deployment using API token."""
    if not settings.vercel_token:
        raise HTTPException(status_code=500, detail="Missing VERCEL_TOKEN")

    url = "https://api.vercel.com/v13/deployments"
    headers = {"Authorization": f"Bearer {settings.vercel_token}"}
    payload = {"name": settings.app_name, "target": "production"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
