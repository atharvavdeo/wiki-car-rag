import streamlit as st
from datetime import datetime
from logic.wiki_utils import retrieve_wikipedia_data
from logic.gemini_utils import setup_gemini, generate_gemini_response

st.set_page_config(
    page_title="Automotive RAG Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .source-info {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0;
            margin: -1rem -1rem 1rem -1rem;
        }
        
        .user-message, .bot-message {
            max-width: 95%;
            padding: 0.8rem 1rem;
        }
        
        .chat-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Automotive RAG Assistant</h1>
        <p>Ask questions about cars, manufacturers, and automotive technology</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'gemini_model' not in st.session_state:
        with st.spinner("Initializing AI model..."):
            st.session_state.gemini_model = setup_gemini()
            
        # Check if model initialization failed
        if st.session_state.gemini_model is None:
            st.error("⚠️ Failed to initialize Gemini AI model. Please check your API key configuration.")
            st.info("💡 Make sure you have set your `GEMINI_API_KEY` environment variable")
            st.stop()
    if 'example_query' not in st.session_state:
        st.session_state.example_query = None

    with st.sidebar:
        st.markdown("""
        <div class="sidebar-info">
            <h3>💡 Tips</h3>
            <ul>
                <li>Ask about car brands, models, or specifications</li>
                <li>Try queries like "When was Tesla founded?"</li>
                <li>Ask about specific models: "Tell me about Ford Mustang"</li>
                <li>Inquire about automotive technologies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("🧪 Test Chat Display"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Test message",
                "timestamp": datetime.now()
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": "This is a test response to verify the chat display is working correctly.",
                "timestamp": datetime.now()
            })
            st.rerun()
        
        st.markdown("**📊 Session Stats**")
        st.metric("Messages", len(st.session_state.messages))
        
        # Debug information
        with st.expander("🔧 Debug Information", expanded=False):
            st.markdown("**Model Status:**")
            if st.session_state.gemini_model:
                st.success("✅ Gemini model loaded")
            else:
                st.error("❌ Gemini model not available")
            
            st.markdown("**Environment:**")
            import os
            api_key_status = "✅ Set" if os.getenv('GEMINI_API_KEY') else "❌ Missing"
            st.text(f"GEMINI_API_KEY: {api_key_status}")
            
            st.markdown("**Cache Status:**")
            st.text("Wikipedia cache: Active")
            st.text("Gemini cache: Active")
            
            st.markdown("**Session State:**")
            st.text(f"Messages count: {len(st.session_state.messages)}")
            if st.session_state.messages:
                st.text(f"Last message role: {st.session_state.messages[-1]['role']}")
                st.text(f"Last message length: {len(st.session_state.messages[-1]['content'])}")
        
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💬 Ask Your Question")
        
        with st.form(key="query_form", clear_on_submit=True):
            # Use example query if set, otherwise use empty string
            default_query = st.session_state.example_query if st.session_state.example_query else ""
            user_query = st.text_input(
                "Enter your automotive question:",
                value=default_query,
                placeholder="e.g., When was BMW founded?",
                help="Ask anything about cars, manufacturers, or automotive technology"
            )
            submit_button = st.form_submit_button("🚀 Ask Assistant", use_container_width=True)
            
            # Clear example query after using it
            if st.session_state.example_query:
                st.session_state.example_query = None
        
        st.markdown("**🔥 Popular Questions:**")
        example_queries = [
            "When was Tesla founded?",
            "Tell me about Toyota Prius",
            "What is the Ford Mustang history?",
            "BMW M3 specifications"
        ]
        
        for i, example in enumerate(example_queries):
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state.example_query = example
                st.rerun()
    
    with col2:
        st.markdown("### 🤖 Assistant Response")
        
        if submit_button and user_query and user_query.strip():
            st.session_state.messages.append({
                "role": "user",
                "content": user_query,
                "timestamp": datetime.now()
            })
            
            with st.spinner("🔍 Searching Wikipedia and generating response..."):
                try:
                    # Debug: Show what we're searching for
                    st.info(f"🔍 Searching for: {user_query}")
                    
                    context_data = retrieve_wikipedia_data(user_query)
                    
                    # Debug: Show context data status
                    if context_data:
                        st.success(f"✅ Found Wikipedia page: {context_data.get('title', 'Unknown')}")
                        st.info(f"📊 Infobox keys: {len(context_data.get('infobox', {}))}")
                        st.info(f"📝 Summary length: {len(context_data.get('summary', ''))}")
                    else:
                        st.warning("⚠️ No Wikipedia data found")
                    
                    if context_data and context_data.get('summary'):
                        # Debug: Show context being passed to Gemini
                        with st.expander("🔍 Debug: Context being sent to AI", expanded=False):
                            st.text("Summary preview:")
                            st.text(context_data.get('summary', '')[:500] + "...")
                            st.text(f"Infobox keys: {list(context_data.get('infobox', {}).keys())}")
                            if context_data.get('infobox'):
                                st.text("Sample infobox data:")
                                for key, value in list(context_data.get('infobox', {}).items())[:3]:
                                    st.text(f"  {key}: {value}")
                        
                        response, context = generate_gemini_response(
                            st.session_state.gemini_model, 
                            user_query, 
                            context_data
                        )
                        
                        # Debug: Show response status
                        if response:
                            st.success(f"✅ Generated response: {len(response)} characters")
                        else:
                            st.warning("⚠️ Empty response generated")
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "context": context_data,
                            "timestamp": datetime.now()
                        })
                    else:
                        # Fallback response when no context is found
                        fallback_response = f"I couldn't find specific information about '{user_query}' in Wikipedia. This might be because:\n\n• The topic is too specific or niche\n• The search terms don't match Wikipedia page titles\n• The page doesn't contain sufficient information\n\nPlease try:\n• Using more general terms (e.g., 'BMW' instead of 'BMW M3 2024')\n• Asking about well-known automotive brands or models\n• Rephrasing your question"
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": fallback_response,
                            "timestamp": datetime.now()
                        })
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I encountered an error while processing your request: {str(e)}. Please try again.",
                        "timestamp": datetime.now()
                    })
        
        # Chat display area
        st.markdown("### 💬 Chat History")
        
        if not st.session_state.messages:
            st.info("👋 Start a conversation by asking a question about automotive topics!")
        else:
            chat_container = st.container(height=600)
            
            with chat_container:
                for message in st.session_state.messages[-10:]:
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div class="user-message">
                            <strong>You:</strong> {message["content"]}
                            <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="bot-message">
                            <strong>Assistant:</strong> {message["content"]}
                            <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if "context" in message and message["context"]:
                            context = message["context"]
                            st.markdown(f"""
                            <div class="source-info">
                                <strong>📚 Source:</strong> <a href="{context.get('url', '#')}" target="_blank">{context['title']}</a>
                                <br><strong>🔑 Key Info:</strong> {len(context.get('infobox', {}))} data points extracted
                            </div>
                            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🔒 Powered by Google Gemini AI & Wikipedia | Built with Streamlit</p>
        <p><small>Real-time automotive information retrieval and AI-powered responses</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
