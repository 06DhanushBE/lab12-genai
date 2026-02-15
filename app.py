import streamlit as st
import sys
import os
import folium
from streamlit_folium import st_folium

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.data_orchestrator import DataOrchestrator
from config import Config

# Page configuration
st.set_page_config(
    page_title="Country Financial Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "orchestrator" not in st.session_state:
    try:
        Config.validate_config()
        st.session_state.orchestrator = DataOrchestrator()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_data" not in st.session_state:
    st.session_state.current_data = None

if "show_data" not in st.session_state:
    st.session_state.show_data = False

# Sidebar
with st.sidebar:
    st.markdown("# 🌍 Financial Agent")
    st.markdown("---")
    
    st.markdown("## ✨ Features")
    st.markdown("💰 **Currency Information** - Official names, codes, symbols")
    st.markdown("💱 **Exchange Rates** - Real-time USD, INR, GBP, EUR")
    st.markdown("📈 **Stock Markets** - Live index values")
    st.markdown("🗺️ **Exchange Locations** - Interactive maps")
    st.markdown("🤖 **AI Summaries** - Natural language insights")
    
    st.markdown("---")
    st.markdown("## 🌏 Supported Countries")
    st.markdown("🇯🇵 Japan • 🇮🇳 India • 🇺🇸 United States")
    st.markdown("🇬🇧 United Kingdom • 🇨🇳 China • 🇰🇷 South Korea")
    
    st.markdown("---")
    st.markdown("## 💬 Quick Examples")
    
    if st.button("Japan Financial Data", use_container_width=True):
        st.session_state.example_query = "Give me currency and stock market details for Japan"
    
    if st.button("India Market Info", use_container_width=True):
        st.session_state.example_query = "Show me financial information for India"
    
    if st.button("UK Exchange Rates", use_container_width=True):
        st.session_state.example_query = "What's the exchange rate for UK pound?"
    
# Add sidebar chat management
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔧 Chat Management")
    
    if st.button("🗑️ Clear All Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.show_data = False
        st.session_state.current_data = None
        st.rerun()
    
    if st.session_state.chat_history:
        st.write(f"💬 Messages: {len(st.session_state.chat_history)}")
    else:
        st.write("💬 No messages yet")

# Main content
st.title("🌍 Country Financial Agent")
st.markdown("Ask me about currency information, exchange rates, and stock market data for any country!")

# Display persistent chat history first
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Handle example query
if "example_query" in st.session_state:
    query = st.session_state.example_query
    del st.session_state.example_query
else:
    query = st.chat_input("Ask about any country's financial information...")

# Process query
if query:
    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # Validate and process
    if not st.session_state.orchestrator.validate_query(query):
        error_msg = "I can only provide information about Japan, India, US, UK, China, or South Korea."
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        st.session_state.show_data = False
    else:
        # Add processing message
        processing_msg = "Processing your request..."
        st.session_state.chat_history.append({"role": "assistant", "content": processing_msg})
        
        # Get data
        with st.spinner("Fetching financial data..."):
            financial_data = st.session_state.orchestrator.get_country_financial_data(query)
        
        # Remove processing message and add result
        st.session_state.chat_history.pop()  # Remove processing message
        
        if financial_data:
            # Store data in session state
            st.session_state.current_data = financial_data
            st.session_state.show_data = True
            
            # Success message
            success_msg = f"✅ Here's the financial information for {financial_data.country_name}! (Scroll down to see details)"
            st.session_state.chat_history.append({"role": "assistant", "content": success_msg})
        
        else:
            error_msg = "❌ Sorry, I couldn't retrieve the financial data. Please try again."
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            st.session_state.show_data = False
    
    # Rerun to show updated chat
    st.rerun()

# Display stored data if available
if st.session_state.show_data and st.session_state.current_data:
    financial_data = st.session_state.current_data
    
    # Display data in main area
    st.markdown("---")
    
    # Country header
    st.header(f"🏛️ {financial_data.country_name}")
    
    # Currency and Exchange Rates
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Currency Information")
        st.write(f"**Currency:** {financial_data.currency.name}")
        st.write(f"**Code:** {financial_data.currency.code}")
        st.write(f"**Symbol:** {financial_data.currency.symbol}")
    
    with col2:
        st.subheader("💱 Exchange Rates")
        st.write(f"**1 {financial_data.currency.code} equals:**")
        for currency, rate in financial_data.exchange_rates.rates.items():
            if rate > 0:
                st.write(f"• **{currency}:** {rate:.4f}")
        st.caption(f"Last updated: {financial_data.exchange_rates.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Stock Market Information
    st.subheader("📈 Stock Market Information")
    
    for market in financial_data.stock_markets:
        st.write(f"**🏢 {market.exchange_name}**")
        st.caption(f"📍 {market.location.address}")
        
        if market.indices:
            cols = st.columns(len(market.indices))
            for i, index in enumerate(market.indices):
                with cols[i]:
                    change_color = "🟢" if index.change_percent >= 0 else "🔴"
                    change_symbol = "+" if index.change_percent >= 0 else ""
                    
                    st.metric(
                        label=index.name,
                        value=f"{index.current_value:,.2f}",
                        delta=f"{change_symbol}{index.change_percent:.2f}%"
                    )
    
    # Interactive Map
    if financial_data.exchange_locations:
        st.subheader("🗺️ Stock Exchange Locations")
        
        # Create map
        center_lat = sum(loc.latitude for loc in financial_data.exchange_locations) / len(financial_data.exchange_locations)
        center_lon = sum(loc.longitude for loc in financial_data.exchange_locations) / len(financial_data.exchange_locations)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        for location in financial_data.exchange_locations:
            folium.Marker(
                [location.latitude, location.longitude],
                popup=f"<b>{location.name}</b><br>{location.address}",
                tooltip=location.name
            ).add_to(m)
        
        st_folium(m, width=700, height=400)
        
        # Location details
        st.write("**Exchange Details:**")
        for location in financial_data.exchange_locations:
            st.write(f"• **{location.name}:** {location.address}")
    
    # AI Summary
    st.subheader("🤖 AI Summary")
    with st.spinner("Generating AI summary..."):
        summary = st.session_state.orchestrator.generate_summary(financial_data)
        st.info(summary)
    
    # Add clear button and chat clear button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Results", type="secondary"):
            st.session_state.show_data = False
            st.session_state.current_data = None
            st.rerun()
    
    with col2:
        if st.button("💬 Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")

# Remove the bottom chat history section since it's now at the top