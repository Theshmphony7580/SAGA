from typing import Any
import re


def sanitize_text(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ").strip()


def mask_pii(value: str) -> str:
    # Mask emails
    if re.search(r"[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}", value):
        return "***@***.***"
    # Mask phone numbers (10+ digits)
    digits = [c for c in value if c.isdigit()]
    if len(digits) >= 10:
        return "**********"
    return value



