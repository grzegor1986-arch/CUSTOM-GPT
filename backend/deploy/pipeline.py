"""Simple orchestrator for deployment pipeline."""

from deploy.railway import deploy_backend
from deploy.vercel import deploy_frontend


def run_pipeline() -> None:
    """Run backend + frontend deployment flow."""
    print("1. Build product")
    print("2. Deploy backend → Railway")
    print(deploy_backend())
    print("3. Deploy frontend → Vercel")
    print(deploy_frontend())
    print("4. Ready to sell 💸")


if __name__ == "__main__":
    run_pipeline()
