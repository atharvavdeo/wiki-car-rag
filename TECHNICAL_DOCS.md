# Automotive RAG Assistant - Technical Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Streamlit UI  │  │   Chat History  │  │  Debug Panel    │ │
│  │   (Frontend)    │  │   Management    │  │   & Monitoring  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Query           │  │ Model Detection  │  │ Query           │ │
│  │ Normalization   │  │ & Classification │  │ Routing         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Wikipedia API   │  │ Content         │  │ Infobox         │ │
│  │ Integration     │  │ Extraction      │  │ Parsing         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Context         │  │ Google Gemini   │  │ Response        │ │
│  │ Building        │  │ AI Integration  │  │ Generation      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CACHING LAYER                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Wikipedia       │  │ AI Model        │  │ Session         │ │
│  │ Data Cache      │  │ Cache           │  │ State Cache     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend Layer (`streamlit_app.py`)

**Responsibilities**:
- User interface rendering and interaction
- Session state management
- Real-time chat display
- Error handling and user feedback

**Key Classes/Functions**:
```python
def main():
    """Main application entry point"""
    # Session state initialization
    # UI component rendering
    # Event handling and user interaction

# Session State Structure
session_state = {
    'messages': [],           # Chat conversation history
    'gemini_model': None,    # Cached AI model instance
    'example_query': None    # Pre-filled query from examples
}
```

**UI Components**:
- **Header**: Application title and description
- **Sidebar**: Tips, debug info, session stats
- **Main Area**: Query input and chat display
- **Debug Panel**: Technical information and troubleshooting

### 2. Query Processing Layer (`logic/wiki_utils.py`)

**Responsibilities**:
- Query analysis and normalization
- Model detection and classification
- Wikipedia API integration
- Content extraction and processing

**Key Functions**:

#### A. Main Data Retrieval Function
```python
@streamlit_cache
def retrieve_wikipedia_data(query: str) -> dict:
    """
    Main function for Wikipedia data retrieval
    
    Process:
    1. Query normalization
    2. Model detection
    3. Search strategy selection
    4. Content extraction
    5. Data formatting
    """
```

#### B. Model Detection System
```python
model_keywords = [
    'mustang', 'camaro', 'corvette', 'f-150', 'civic', 'accord',
    'corolla', 'camry', 'model s', 'model 3', 'model x', 'model y',
    '911', 'm3', 'm5', 'golf', 'beetle', 'prius', 'wrangler'
]

def _detect_model(query: str) -> str:
    """Detects if query is about a specific car model"""
```

#### C. Smart Search Strategy
```python
def _search_wikipedia(query: str, specific_search: bool = False):
    """
    Internal search function with multiple strategies:
    
    1. Direct model search (for specific models)
    2. Company search (for general queries)
    3. Fallback mechanisms
    4. Multiple result attempts
    """
```

#### D. Content Processing Pipeline
```python
def _extract_relevant_summary(text: str, query: str) -> str:
    """
    Extracts relevant content based on query:
    - Keyword matching
    - Date extraction
    - Production information
    - Technical specifications
    """

def _extract_dates_info(text: str, query: str) -> dict:
    """
    Extracts date-related information:
    - Production dates
    - Introduction dates
    - Model year information
    """
```

### 3. AI Integration Layer (`logic/gemini_utils.py`)

**Responsibilities**:
- Google Gemini AI model management
- Context building and formatting
- Response generation
- Error handling and fallbacks

**Key Functions**:

#### A. Model Initialization
```python
@streamlit_cache_resource
def setup_gemini():
    """
    Initializes and caches Gemini AI model:
    1. API key validation
    2. Model configuration
    3. Connection testing
    4. Error handling
    """
```

#### B. Context Building
```python
def _build_context_string(context: dict) -> str:
    """
    Builds comprehensive context for AI:
    1. Page title and summary
    2. Infobox data (prioritized)
    3. Additional extracted information
    4. Founding date extraction
    """
```

#### C. Response Generation
```python
def generate_gemini_response(model, query: str, context: dict):
    """
    Generates AI responses:
    1. Model and context validation
    2. Prompt construction
    3. AI response generation
    4. Error handling and fallbacks
    """
```

### 4. Caching System

**Multi-Level Caching Architecture**:

#### A. Wikipedia Data Caching
```python
@streamlit_cache_data(ttl=3600, show_spinner=False, max_entries=100)
def retrieve_wikipedia_data(query: str):
    # Caches Wikipedia data for 1 hour
    # Maximum 100 cached queries
    # Automatic cache invalidation
```

#### B. AI Model Caching
```python
@streamlit_cache_resource(max_entries=1)
def setup_gemini():
    # Caches AI model instance
    # Persistent across sessions
    # Single model instance
```

#### C. Fallback Mechanisms
```python
def streamlit_cache(func):
    """Smart caching decorator with fallback support"""
    # Detects Streamlit context
    # Falls back to non-cached version
    # Error recovery mechanisms
```

## Data Flow Architecture

### 1. Query Processing Flow

```
User Input
    │
    ▼
Query Normalization
    │
    ▼
Model Detection
    │
    ▼
Search Strategy Selection
    │
    ▼
Wikipedia API Call
    │
    ▼
Content Extraction
    │
    ▼
Context Building
    │
    ▼
AI Response Generation
    │
    ▼
UI Display
```

### 2. Caching Flow

```
Request
    │
    ▼
Cache Check
    │
    ├─ Cache Hit ──► Return Cached Data
    │
    ▼
Cache Miss
    │
    ▼
API Call
    │
    ▼
Cache Store
    │
    ▼
Return Data
```

### 3. Error Handling Flow

```
Process Execution
    │
    ▼
Error Detection
    │
    ├─ Network Error ──► Retry Mechanism
    ├─ API Error ──► Fallback Response
    ├─ Data Error ──► Content Validation
    └─ AI Error ──► Error Message
    │
    ▼
User Notification
```

## API Integration Details

### 1. Wikipedia API Integration

**Base URL**: `https://en.wikipedia.org/w/api.php`

**Search Parameters**:
```python
search_params = {
    "action": "query",           # API action
    "format": "json",            # Response format
    "list": "search",            # Search type
    "srsearch": query,           # Search query
    "utf8": 1,                   # UTF-8 encoding
    "srlimit": 5                 # Result limit
}
```

**Content Retrieval Parameters**:
```python
content_params = {
    "action": "parse",           # Parse action
    "page": page_title,          # Page title
    "format": "json",            # JSON format
    "prop": "text|wikitext",     # Content properties
    "redirects": 1               # Follow redirects
}
```

**Error Handling**:
```python
try:
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    print(f"Wikipedia API error: {e}")
    return None
```

### 2. Google Gemini API Integration

**Model Configuration**:
```python
model = genai.GenerativeModel('models/gemini-flash-latest')
```

**Prompt Structure**:
```python
prompt = f"""You are an expert automotive assistant. Use the provided context to answer the user's question.

CONTEXT:
{context_str}

USER'S QUESTION: {query}

Please provide a helpful answer based on the context above.
ANSWER:"""
```

**Response Generation**:
```python
try:
    response = model.generate_content(prompt)
    if response and response.text:
        return response.text, context
    else:
        return "No response generated. Please try again.", None
except Exception as e:
    return f"Error generating response: {e}", None
```

## Performance Optimizations

### 1. Caching Optimizations

**Wikipedia Data Caching**:
- **TTL**: 1 hour (3600 seconds)
- **Max Entries**: 100 queries
- **Strategy**: Query-based caching
- **Invalidation**: Automatic TTL-based

**AI Model Caching**:
- **Type**: Resource caching
- **Persistence**: Across sessions
- **Strategy**: Single instance caching
- **Initialization**: Lazy loading

### 2. API Optimizations

**Request Optimization**:
- **Timeout Management**: 15-second timeouts
- **Retry Logic**: Multiple search attempts
- **Batch Processing**: Efficient API usage
- **Error Recovery**: Graceful degradation

**Content Optimization**:
- **Smart Extraction**: Relevant content only
- **Size Limits**: 3000 character summaries
- **Priority Fields**: Important data first
- **Fallback Content**: Default responses

### 3. UI Optimizations

**Session Management**:
- **State Persistence**: Session-based storage
- **Memory Efficiency**: Limited message history
- **Cleanup**: Automatic garbage collection

**Rendering Optimization**:
- **Lazy Loading**: On-demand content
- **Efficient Updates**: Minimal re-rendering
- **Responsive Design**: Mobile optimization

## Security Architecture

### 1. API Key Management

**Environment Variables**:
```python
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not set")
    return None
```

**Security Measures**:
- **No Hardcoding**: Keys never in code
- **Environment Isolation**: Separate dev/prod keys
- **Validation**: API key format validation
- **Error Handling**: Secure error messages

### 2. Data Privacy

**No Persistent Storage**:
- **Session-Only**: Temporary data storage
- **No Logging**: No user data logging
- **External APIs**: Data processed externally
- **Cleanup**: Automatic data cleanup

### 3. Input Validation

**Query Sanitization**:
```python
if not query or not query.strip():
    return None
```

**Error Boundaries**:
- **Input Validation**: Query format checking
- **Content Validation**: Data integrity checks
- **Response Validation**: Output verification

## Deployment Architecture

### 1. Local Development

**Requirements**:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Environment Setup**:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 2. Streamlit Cloud Deployment

**Repository Structure**:
```
project/
├── streamlit_app.py      # Main application
├── logic/                # Business logic
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
└── README.md            # Documentation
```

**Deployment Process**:
1. **Repository Connection**: GitHub integration
2. **Environment Variables**: API key configuration
3. **Automatic Deployment**: Git-based deployment
4. **Health Monitoring**: Application status tracking

### 3. Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

**Docker Commands**:
```bash
docker build -t automotive-rag .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key automotive-rag
```

## Monitoring and Debugging

### 1. Debug Information

**Session State Monitoring**:
```python
st.text(f"Messages count: {len(st.session_state.messages)}")
st.text(f"Last message role: {st.session_state.messages[-1]['role']}")
```

**API Status Monitoring**:
```python
api_key_status = "✅ Set" if os.getenv('GEMINI_API_KEY') else "❌ Missing"
st.text(f"GEMINI_API_KEY: {api_key_status}")
```

**Cache Status Monitoring**:
```python
st.text("Wikipedia cache: Active")
st.text("Gemini cache: Active")
```

### 2. Error Logging

**Console Logging**:
```python
print(f"Wikipedia API error: {e}")
print(f"Cache fallback: {e}")
```

**User Feedback**:
```python
st.error(f"❌ Error: {str(e)}")
st.warning("⚠️ No Wikipedia data found")
st.success("✅ Generated response: {len(response)} characters")
```

### 3. Performance Metrics

**Response Time Tracking**:
- **Wikipedia API**: Request/response timing
- **AI Generation**: Model response timing
- **Cache Performance**: Hit/miss ratios
- **UI Rendering**: Component load times

## Future Enhancements

### 1. Advanced Features

**Multi-Language Support**:
- **International Wikipedia**: Multi-language API integration
- **Language Detection**: Automatic language detection
- **Translation**: AI-powered translation

**Image Processing**:
- **Car Image Analysis**: Visual car identification
- **Specification Extraction**: Image-based data extraction
- **Visual Search**: Image-based queries

### 2. Performance Improvements

**Database Integration**:
- **Persistent Caching**: Database-backed caching
- **Query Optimization**: Advanced query processing
- **Data Analytics**: Usage pattern analysis

**CDN Integration**:
- **Content Delivery**: Global content distribution
- **Static Assets**: Optimized asset delivery
- **Caching Layers**: Multi-tier caching

### 3. AI Enhancements

**Model Fine-tuning**:
- **Custom Training**: Automotive-specific training
- **Domain Adaptation**: Specialized automotive knowledge
- **Performance Optimization**: Faster response times

**Advanced Caching**:
- **AI Response Caching**: Cached AI responses
- **Context Memory**: Conversation context retention
- **Smart Prefetching**: Predictive content loading

This technical documentation provides a comprehensive understanding of the Automotive RAG Assistant's architecture, implementation details, and operational characteristics.
