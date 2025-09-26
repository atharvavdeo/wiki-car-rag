"""
Automotive RAG Logic Module

This module contains the core business logic for the RAG system:
- Wikipedia data retrieval and parsing
- Google Gemini AI integration
- Response generation utilities
"""

__version__ = "1.0.0"
__author__ = "Automotive RAG Team"

from .wiki_utils import retrieve_wikipedia_data, parse_infobox
from .gemini_utils import setup_gemini, generate_gemini_response

__all__ = [
    'retrieve_wikipedia_data',
    'parse_infobox', 
    'setup_gemini',
    'generate_gemini_response'
]