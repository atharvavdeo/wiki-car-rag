import os
import google.generativeai as genai
import streamlit as st
from functools import wraps
from dotenv import load_dotenv
load_dotenv()

def streamlit_cache_resource(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if hasattr(st, 'cache_resource') and hasattr(st, 'session_state'):
                return st.cache_resource(max_entries=1)(func)(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            print(f"Resource cache fallback: {e}")
            return func(*args, **kwargs)
    return wrapper

@streamlit_cache_resource
def setup_gemini():
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            error_msg = "⚠️ GEMINI_API_KEY environment variable not set"
            if hasattr(st, 'error'):
                st.error(error_msg)
            else:
                print(error_msg)
            return None
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        try:
            test_response = model.generate_content("Hello")
            if not test_response.text:
                raise Exception("Model returned empty response")
        except Exception as test_error:
            error_msg = f"Gemini model test failed: {test_error}"
            if hasattr(st, 'error'):
                st.error(error_msg)
            else:
                print(error_msg)
            return None
        return model
        
    except Exception as e:
        error_msg = f"Error configuring Gemini API: {e}"
        if hasattr(st, 'error'):
            st.error(error_msg)
        else:
            print(error_msg)
        return None

def generate_gemini_response(model, query: str, context: dict):
    if not model:
        return "Gemini model is not available. Please check your API key configuration.", None

    if not context or not context.get('summary'):
        return "No relevant context found. Please try a different query.", None

    try:
        context_str = _build_context_string(context)
        if not context_str or len(context_str.strip()) < 50:
            return "Insufficient context data. Please try a more specific query.", None
            
        prompt = _build_prompt(query, context_str)
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return "No response generated. Please try again.", None
            
        return response.text, context
        
    except Exception as e:
        error_msg = f"Error generating response: {e}"
        print(error_msg)  # Log for debugging
        return f"I encountered an error while generating a response. Please try again. ({error_msg})", None

def _build_context_string(context: dict) -> str:
    if not context:
        return ""
        
    context_str = f"Page Title: {context.get('title', 'Unknown')}\n\nSummary:\n{context.get('summary', 'No summary available')}\n\n"
    
    infobox = context.get('infobox', {})
    if infobox and len(infobox) > 0:
        context_str += "Key Information:\n"
        # Prioritize important fields like founding date, established, etc.
        priority_fields = ['Founded', 'Established', 'Founded by', 'Founded in', 'Founded date', 
                          'Founded by', 'Founded', 'Established', 'Founded in', 'Founded date',
                          'Founded by', 'Founded', 'Established', 'Founded in', 'Founded date']
        
        # Add priority fields first
        for field in priority_fields:
            if field in infobox:
                value = infobox[field]
                if value and str(value).strip():
                    context_str += f"- {field}: {value}\n"
        
        # Add remaining fields
        for key, value in infobox.items():
            if key not in priority_fields and value and str(value).strip():
                context_str += f"- {key}: {value}\n"
    
    # If no founding info in infobox, try to extract from summary
    if not any(field in infobox for field in ['Founded', 'Established', 'Founded by', 'Founded in']):
        founding_info = _extract_founding_info(context.get('summary', ''))
        if founding_info:
            context_str += f"\nAdditional Information:\n- Founded: {founding_info}\n"
    
    return context_str

def _extract_founding_info(summary: str) -> str:
    import re
    patterns = [
        r'founded\s+(?:in\s+)?(\d{4})',
        r'established\s+(?:in\s+)?(\d{4})',
        r'started\s+(?:in\s+)?(\d{4})',
        r'began\s+(?:in\s+)?(\d{4})',
        r'(\d{4})\s+by\s+',
        r'(\d{4})\s+as\s+',
        r'(\d{4})\s+when\s+'
    ]
    
    text_lower = summary.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            year = match.group(1)
            # Look for the full sentence containing this year
            sentences = summary.split('. ')
            for sentence in sentences:
                if year in sentence and ('founded' in sentence.lower() or 'established' in sentence.lower() or 'started' in sentence.lower()):
                    return sentence.strip()
    
    return ""

def _build_prompt(query: str, context_str: str) -> str:
    return f"""You are an expert automotive assistant. Use the provided context to answer the user's question. Look carefully through the context for relevant information.

CONTEXT:
{context_str}

USER'S QUESTION: {query}

Please provide a helpful answer based on the context above. If you find relevant information, share it. If the specific information isn't available, explain what you can find in the context.

ANSWER:"""
