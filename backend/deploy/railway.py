"""Minimal Railway deployment helper."""

import requests
from fastapi import HTTPException

from config import settings


def deploy_backend() -> dict:
    """Trigger a Railway project create mutation."""
    if not settings.railway_token:
        raise HTTPException(status_code=500, detail="Missing RAILWAY_TOKEN")

    url = "https://backboard.railway.app/graphql/v2"
    headers = {"Authorization": f"Bearer {settings.railway_token}"}
    query = {
        "query": """
        mutation {
          projectCreate(input: { name: \"ai-backend\" }) { id }
        }
        """
    }
    response = requests.post(url, json=query, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
