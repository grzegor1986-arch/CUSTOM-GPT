"""Simple starter script for the CUSTOM-GPT repository."""

from datetime import datetime, timezone


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    print("Hello from CUSTOM-GPT 👋")
    print(f"Current UTC time: {now}")
    print("Next step: replace this script with your first project utility.")


if __name__ == "__main__":
    main()
