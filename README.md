✈️ Airline Demand Dashboard
A simple yet powerful Flask web app that visualizes flight demand trends between major cities using real-time airline data and AI-generated insights.

🚀 Features
🔍 Search Flights by origin and destination cities

📊 Visualize Demand via dynamic bar charts

🤖 AI Market Summary using Hugging Face model

💸 Price Trends and simulated demand display

🎯 Clean, responsive UI for both desktop and mobile

🛠️ Tech Stack
Backend: Flask, Amadeus API, Hugging Face Inference API

Frontend: HTML, CSS, JavaScript, Chart.js

AI Model: Hugging Face summarization (with API token)

Others: dotenv, requests

📦 Installation
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/airline-demand-dashboard.git
cd airline-demand-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🔐 Setup Environment Variables
Create a .env file with the following variables:

env
Copy
Edit
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
HF_API_KEY=your_huggingface_api_token
▶️ Run the App
bash
Copy
Edit
python app.py
Then open http://127.0.0.1:5000 in your browser.

📝 Notes
The demand values are randomized for demo purposes.

Make sure your Hugging Face token has inference access.

Real-time flight data is fetched using Amadeus APIs.