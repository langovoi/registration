from .german_visa_page import GermanVisaPage
from .google_page import GooglePage

page_map = {
    "google.com": GooglePage,
    "german visa": GermanVisaPage,
    "italy consulate": ItalyConsulatePage,
    "italy embassy": ItalyEmbassyPage,
}


def factory(page_name: str):
    """Encapsulate screen creation"""
    return page_map[page_name]
