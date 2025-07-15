from flask import Flask, render_template, request
import requests
from amadeus import Client, ResponseError
import os
import random
import json
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Amadeus API
amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET")
)

# Hugging Face config
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")
HUGGINGFACE_MODEL = "facebook/bart-large-cnn"

# Mapping full city names to IATA codes
CITY_NAME_TO_IATA = {
    'sydney': 'SYD',
    'melbourne': 'MEL',
    'brisbane': 'BNE',
    'singapore': 'SIN',
    'bangkok': 'BKK',
    'hong kong': 'HKG',
    'kuala lumpur': 'KUL',
    'auckland': 'AKL'
}

ORIGINS = ['SYD', 'MEL', 'BNE']
DESTINATIONS = ['SIN', 'BKK', 'HKG', 'KUL', 'AKL']

def fetch_flight_data():
    flight_data = []
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            if origin == destination:
                continue
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate='2025-07-20',
                    adults=1,
                    max=1
                )
                offer = response.data[0]
                price = float(offer['price']['total'])
                demand = random.randint(5, 100)  # Randomized demand
                flight_data.append({
                    'origin': origin,
                    'destination': destination,
                    'price': price,
                    'demand': demand
                })
            except ResponseError as e:
                print(f"❌ Error for {origin} → {destination}: {e}")
                continue
    print(f"✅ Flights fetched: {flight_data}")
    return flight_data

def generate_summary(data):
    if not data:
        return "⚠️ No insights available at the moment."

    lines = []
    for row in data[:5]:
        lines.append(
            f"Route {row['origin']} to {row['destination']} has an average price of ${row['price']} and a demand score of {row['demand']}."
        )

    prompt = " ".join(lines) + " Provide a concise summary of market demand trends."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
            headers=headers,
            json=payload
        )
        output = response.json()
        print("📥 Hugging Face response:", output)

        if isinstance(output, list) and 'summary_text' in output[0]:
            return output[0]['summary_text']
        else:
            return "⚠️ Could not generate insight."
    except Exception as e:
        print("❌ Error generating summary:", e)
        return "⚠️ Could not generate insight."

@app.route('/')
def index():
    origin_input = request.args.get('origin', '').strip().lower()
    destination_input = request.args.get('destination', '').strip().lower()

    origin_filter = CITY_NAME_TO_IATA.get(origin_input, origin_input.upper())
    destination_filter = CITY_NAME_TO_IATA.get(destination_input, destination_input.upper())

    all_flights = fetch_flight_data()

    if origin_filter and destination_filter:
        filtered_flights = [
            f for f in all_flights
            if f['origin'] == origin_filter and f['destination'] == destination_filter
        ]
    else:
        filtered_flights = all_flights

    summary = generate_summary(filtered_flights)

    # Aggregate demand by destination
    destination_demand = defaultdict(int)
    for f in filtered_flights:
        destination_demand[f['destination']] += f['demand']

    chart_labels = list(destination_demand.keys())
    chart_values = list(destination_demand.values())

    return render_template(
        'index.html',
        flights=filtered_flights,
        summary=summary,
        chart_labels=json.dumps(chart_labels),
        chart_values=json.dumps(chart_values)
    )

if __name__ == '__main__':
    app.run(debug=True)
