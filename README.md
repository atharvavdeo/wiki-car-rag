# Automotive RAG Assistant

A Retrieval-Augmented Generation (RAG) system that provides intelligent answers about automotive topics using Wikipedia data and Google Gemini AI.

## Features

-  **AI-Powered Responses**: Uses Google Gemini AI for intelligent automotive Q&A
-  **Wikipedia Integration**: Retrieves real-time information from Wikipedia
-  **Automotive Focus**: Specialized for car brands, models, and automotive technology
-  **Interactive Chat**: Streamlit-based conversational interface
-  **Smart Caching**: Optimized performance with intelligent caching
-  **Query Normalization**: Handles various automotive company aliases

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

### Basic Queries
- "When was Tesla founded?"
- "Tell me about Toyota Prius"
- "What is the Ford Mustang history?"
- "BMW M3 specifications"

### Supported Automotive Brands
The system recognizes common aliases for major automotive brands:
- Tesla, BMW, Mercedes-Benz, Audi, Volkswagen
- Toyota, Honda, Ford, Chevrolet, Nissan
- Hyundai, Kia, Mazda, Subaru, Lexus
- And many more...

## Architecture

### Components

1. **`app.py`**: Main Streamlit application with UI
2. **`logic/wiki_utils.py`**: Wikipedia data retrieval and parsing
3. **`logic/gemini_utils.py`**: Google Gemini AI integration
4. **`logic/__init__.py`**: Module exports

### Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key


### Project Structure
```
RAG_miniproj/
├── app.py                 # Main Streamlit application
├── logic/
│   ├── __init__.py       # Module exports
│   ├── wiki_utils.py     # Wikipedia integration
│   └── gemini_utils.py   # Gemini AI integration
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md           # This file
```
