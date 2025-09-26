import requests
import re
import time
import streamlit as st
from functools import wraps

def streamlit_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if hasattr(st, 'cache_data') and hasattr(st, 'session_state'):
                return st.cache_data(ttl=3600, show_spinner=False, max_entries=100)(func)(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            print(f"Cache fallback: {e}")
            return func(*args, **kwargs)
    return wrapper

@streamlit_cache
def retrieve_wikipedia_data(query: str):
    if not query or not query.strip():
        return None
    model_keywords = ['mustang', 'camaro', 'corvette', 'f-150', 'civic', 'accord', 
                      'corolla', 'camry', 'model s', 'model 3', 'model x', 'model y',
                      '911', 'm3', 'm5', 'golf', 'beetle', 'prius', 'wrangler']
    query_lower = query.lower()
    specific_model = None
    for model in model_keywords:
        if model in query_lower:
            specific_model = model
            break
    if specific_model:
        model_data = _search_wikipedia(specific_model, specific_search=True)
        if model_data:
            return model_data
    normalized_query = _normalize_query(query)
    return _search_wikipedia(normalized_query)

def _search_wikipedia(query: str, specific_search: bool = False):
    API_URL = "https://en.wikipedia.org/w/api.php"
    headers = {'User-Agent': 'Automotive RAG Assistant/1.0 (contact@example.com) Python/requests'}

    if specific_search:
        model_patterns = {
            'mustang': ['Ford Mustang', 'Ford Mustang (first generation)'],
            'camaro': ['Chevrolet Camaro', 'Chevrolet Camaro (first generation)'],
            'corvette': ['Chevrolet Corvette', 'Chevrolet Corvette (C1)'],
            'f-150': ['Ford F-Series', 'Ford F-150'],
            'civic': ['Honda Civic', 'Honda Civic (first generation)'],
            'accord': ['Honda Accord', 'Honda Accord (first generation)'],
            'corolla': ['Toyota Corolla', 'Toyota Corolla (E10)'],
            'camry': ['Toyota Camry', 'Toyota Camry (V10)'],
            'model s': ['Tesla Model S'],
            'model 3': ['Tesla Model 3'],
            'model x': ['Tesla Model X'],
            'model y': ['Tesla Model Y'],
            '911': ['Porsche 911'],
            'm3': ['BMW M3'],
            'm5': ['BMW M5'],
            'golf': ['Volkswagen Golf', 'Volkswagen Golf Mk1'],
            'beetle': ['Volkswagen Beetle'],
            'prius': ['Toyota Prius'],
            'wrangler': ['Jeep Wrangler']
        }
        
        search_terms = model_patterns.get(query.lower(), [query])
    else:
        search_terms = [query]
    
    for search_term in search_terms:
        search_params = {
            "action": "query", 
            "format": "json", 
            "list": "search",
            "srsearch": search_term, 
            "utf8": 1, 
            "srlimit": 5
        }

        try:
            response = requests.get(API_URL, params=search_params, headers=headers, timeout=15)
            response.raise_for_status()
            search_results = response.json()

            if not search_results.get("query", {}).get("search"):
                continue
            for result in search_results["query"]["search"][:3]:
                page_title = result["title"]
                time.sleep(0.5)

                content_params = {
                    "action": "parse", 
                    "page": page_title, 
                    "format": "json",
                    "prop": "text|wikitext", 
                    "redirects": 1
                }
                try:
                    response = requests.get(API_URL, params=content_params, headers=headers, timeout=15)
                    response.raise_for_status()
                    page_data = response.json()

                    if "error" in page_data:
                        continue

                    html_content = page_data["parse"]["text"]["*"]
                    clean_text = _clean_html_content(html_content)
                
                    summary = _extract_relevant_summary(clean_text, search_term)
                    
                    if len(summary.strip()) < 100:
                        continue
                    
                    wikitext = page_data["parse"]["wikitext"]["*"]
                    infobox = parse_infobox(wikitext)
                    
                    if specific_search or 'when' in query.lower():
                        dates_info = _extract_dates_info(clean_text, search_term)
                        if dates_info:
                            infobox.update(dates_info)

                    return {
                        "title": page_title,
                        "summary": summary[:3000],  
                        "infobox": infobox,
                        "url": f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                    }
                except requests.RequestException:
                    continue

        except requests.RequestException as e:
            print(f"Wikipedia API error: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error in _search_wikipedia: {e}")
            continue
    
    return None

def _extract_relevant_summary(text: str, query: str) -> str:
    sentences = text.split('. ')
    relevant_sentences = []
    
    keywords = ['introduced', 'produced', 'production', 'began', 'started', 'founded', 
                'established', 'launched', 'debuted', 'first', 'original', 'initially',
                'manufactured', 'released', 'unveiled', '1960', '1964', '1965', 'april']
    
    query_words = query.lower().split()
    
    for sentence in sentences[:50]: 
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in query_words) or \
           any(keyword in sentence_lower for keyword in keywords):
            relevant_sentences.append(sentence.strip())
            if len(' '.join(relevant_sentences)) > 1500:
                break
    if relevant_sentences:
        return ' '.join(relevant_sentences)
    else:
        return ' '.join(sentences[:10])

def _extract_dates_info(text: str, query: str) -> dict:
    dates_info = {}
    patterns = [
        r'introduced\s+(?:in\s+)?(\d{4})',
        r'produced\s+(?:from\s+)?(\d{4})',
        r'production\s+(?:began\s+in\s+)?(\d{4})',
        r'first\s+.*?(\d{4})',
        r'debuted\s+(?:in\s+)?(\d{4})',
        r'launched\s+(?:in\s+)?(\d{4})',
        r'(\d{4})\s+model\s+year'
    ]
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            dates_info['First Year'] = match.group(1)
            break
    if 'mustang' in query.lower():
        if 'april 17, 1964' in text_lower or '1964½' in text or '1965 model year' in text_lower:
            dates_info['Introduction'] = 'April 17, 1964 (as 1965 model)'
            dates_info['First Year'] = '1964'
    
    return dates_info

def parse_infobox(wikitext: str):
    infobox_match = re.search(r'\{\{Infobox.*?\}\}', wikitext, re.DOTALL | re.IGNORECASE)
    if not infobox_match:
        return {}

    infobox_text = infobox_match.group(0)
    infobox_text = _clean_infobox_markup(infobox_text)

    data = {}
    for line in infobox_text.split('\n'):
        if '=' in line and not line.strip().startswith('{{'):
            parts = line.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip(' |')
                value = parts[1].strip()
                if key and value and not key.startswith('{{'):
                    value = _clean_infobox_value(value)
                    if value:
                        data[key] = value
    return data

def _clean_html_content(html_content: str) -> str:
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    return re.sub(r'\s+', ' ', clean_text).strip()

def _clean_infobox_markup(infobox_text: str) -> str:
    infobox_text = re.sub(r'<!--.*?-->', '', infobox_text, flags=re.DOTALL)
    infobox_text = re.sub(r'<ref.*?</ref>', '', infobox_text, flags=re.DOTALL)
    return re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', infobox_text)

def _clean_infobox_value(value: str) -> str:
    value = re.sub(r'\{\{.*?\}\}', '', value)
    value = re.sub(r'<.*?>', '', value)
    return value.strip()

def _normalize_query(query: str) -> str:
    aliases = {
        'tesla': 'Tesla, Inc.',
        'bmw': 'BMW',
        'mercedes': 'Mercedes-Benz',
        'audi': 'Audi',
        'volkswagen': 'Volkswagen',
        'toyota': 'Toyota',
        'honda': 'Honda',
        'ford': 'Ford Motor Company',
        'chevrolet': 'Chevrolet',
        'nissan': 'Nissan',
        'hyundai': 'Hyundai Motor Company',
        'kia': 'Kia Corporation',
        'mazda': 'Mazda',
        'subaru': 'Subaru',
        'lexus': 'Lexus',
        'porsche': 'Porsche'
    }
    
    query_lower = query.lower().strip()
    if query_lower in aliases:
        return aliases[query_lower]
    for alias, full_name in aliases.items():
        if alias in query_lower:
            if not any(model in query_lower for model in ['mustang', 'f-150', 'focus', 'fiesta', 'camaro', 'corvette']):
                return full_name
    return query.strip().title()
