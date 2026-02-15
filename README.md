# Country Financial Agent

An LLM-powered Streamlit application that provides comprehensive financial information for countries worldwide, including currency data, real-time exchange rates, stock market indices, and geographical locations of major stock exchanges.

## Required API Keys

To run this application, you'll need the following API keys:

### 1. Google Gemini API Key (Required)

- **Purpose**: Powers the LLM for natural language processing
- **How to get**:
  1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
  2. Create a new API key
  3. Copy the key to your `.env` file as `GOOGLE_API_KEY`

### 2. Exchange Rate API Key (Optional - has free tier)

- **Purpose**: Real-time currency exchange rates
- **How to get**:
  1. Visit [ExchangeRate-API](https://www.exchangerate-api.com/)
  2. Sign up for a free account (1,500 requests/month free)
  3. Copy your API key to `.env` as `EXCHANGE_RATE_API_KEY`
- **Note**: The app will work without this key using a free service, but with rate limits

### 3. Google Maps API Key (Optional)

- **Purpose**: Interactive maps for stock exchange locations
- **How to get**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Enable the Maps JavaScript API
  3. Create credentials and copy to `.env` as `GOOGLE_MAPS_API_KEY`
- **Note**: The app will show text-based location info without this key

## Quick Setup

1. **Clone and navigate to the project**:

   ```bash
   cd country-financial-agent
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.template .env
   # Edit .env file with your API keys
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Deployment

### 🚀 Streamlit Cloud Deployment (Recommended - FREE)

1. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select repository: `06DhanushBE/lab12-genai`
   - Set main file path: `app.py`
   - Click "Deploy"

2. **Configure Secrets in Streamlit Cloud**
   - In your deployed app, click "⚙️ Settings"
   - Go to "Secrets" tab
   - Add your API keys:
   ```toml
   GOOGLE_API_KEY = "AIzaSyBu8RmxMPG1kridRDNdLKJMXTnZf5xRBvg"
   EXCHANGE_RATE_API_KEY = "89fc1913420cd473fa63bdc2"
   ```

   - Click "Save"
   - Your app will automatically redeploy with the secrets!

### 💻 Local Development with Virtual Environment

1. **Create Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**

   ```bash
   cp .env.template .env
   # Edit .env file with your API keys
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

### 🐳 Docker Deployment

```bash
docker build -t country-financial-agent .
docker run -p 8501:8501 --env-file .env country-financial-agent
```

### ☁️ Other Cloud Platforms

**Heroku:**

- Add `Procfile`: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Set environment variables in Heroku dashboard

**Railway/Render:**

- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Add environment variables in platform settings

## Features

- Natural language queries for country financial information
- Real-time currency exchange rates (USD, INR, GBP, EUR)
- Major stock exchanges and current index values
- Interactive maps showing stock exchange locations
- Responsive web interface
- Error handling and fallback mechanisms

## Example Queries

- "Give me currency and stock market details for Japan"
- "Show me financial information for India"
- "What's the exchange rate and stock market data for UK?"
