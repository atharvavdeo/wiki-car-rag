# Automotive RAG Assistant - Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- Google Gemini API key
- Internet connection

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/automotive-rag-assistant.git
cd automotive-rag-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Get API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 4. Run the Application

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Add your `GEMINI_API_KEY` in the secrets section
   - Deploy!

### Option 2: Docker Deployment

```bash
# Build the Docker image
docker build -t automotive-rag .

# Run the container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key automotive-rag
```

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY=your_key_here

# Run the application
streamlit run streamlit_app.py
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Streamlit Configuration

The application uses default Streamlit settings. You can customize them in `streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not set"**
   - Make sure you've created a `.env` file
   - Verify your API key is correct
   - Restart the application

2. **"Failed to initialize Gemini AI model"**
   - Check your internet connection
   - Verify your API key is valid
   - Check the debug panel for more details

3. **"No Wikipedia data found"**
   - Try different search terms
   - Check your internet connection
   - Use more specific queries

### Debug Information

The application includes a debug panel in the sidebar that shows:
- Model status
- API key status
- Cache status
- Session state information

### Performance Tips

1. **Use specific queries**: "Ford Mustang" instead of "car"
2. **Check the debug panel**: Monitor API responses
3. **Clear cache**: Use the "Clear Chat History" button if needed

## API Usage

### Supported Queries

The system works best with:
- **Car manufacturers**: "Tesla", "BMW", "Toyota"
- **Specific models**: "Ford Mustang", "Tesla Model S"
- **Technical questions**: "When was Tesla founded?"
- **Specifications**: "BMW M3 specifications"

### Query Examples

- ✅ "When was Tesla founded?"
- ✅ "Tell me about Ford Mustang"
- ✅ "BMW M3 specifications"
- ✅ "Toyota Prius history"
- ❌ "What's the weather?" (not automotive)
- ❌ "Tell me a joke" (not automotive)

## Development

### Project Structure

```
automotive-rag-assistant/
├── streamlit_app.py          # Main application
├── logic/                    # Business logic
│   ├── __init__.py
│   ├── wiki_utils.py         # Wikipedia integration
│   └── gemini_utils.py       # AI integration
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── README.md                # Basic documentation
├── ARCHITECTURE.md          # Detailed architecture
├── TECHNICAL_DOCS.md        # Technical documentation
└── SETUP_GUIDE.md           # This file
```

### Adding New Features

1. **New Car Models**: Add to `model_keywords` in `wiki_utils.py`
2. **New API Endpoints**: Extend the Wikipedia API integration
3. **UI Improvements**: Modify `streamlit_app.py`
4. **AI Enhancements**: Update `gemini_utils.py`

### Testing

```bash
# Run the application
streamlit run streamlit_app.py

# Test with different queries
# Check the debug panel for issues
# Monitor the console for errors
```

## Support

### Getting Help

1. **Check the debug panel** in the application
2. **Review the logs** in the console
3. **Check the documentation** in `ARCHITECTURE.md` and `TECHNICAL_DOCS.md`
4. **Verify your API key** is correct and active

### Common Solutions

- **Restart the application** if you encounter issues
- **Clear the cache** using the debug panel
- **Check your internet connection** for API calls
- **Verify your API key** is valid and has sufficient quota

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

For more detailed information, see the `ARCHITECTURE.md` and `TECHNICAL_DOCS.md` files.
