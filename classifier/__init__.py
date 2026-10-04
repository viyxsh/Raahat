"""Task 4: classification and duplicate detection.

Backend usage:
    from classifier import analyze
    result = analyze(text, lat, lng, phone, existing_tickets)
"""
from .pipeline import analyze, get_classifier, set_classifier

__all__ = ["analyze", "get_classifier", "set_classifier"]
