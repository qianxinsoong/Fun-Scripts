import streamlit as st
import random
import datetime
import json
import os
import pandas as pd
import altair as alt

# --- File paths ---
OPTIONS_FILE = "lunch_options.json"
RECORD_FILE = "lunch_record.json"

# --- Default lunch options with coordinates ---
default_options = [
    {"name": "Nasi Kandar Nasmeer", "location": "Borealis", "diet": "Halal", "votes": 0, "lat": 5.336, "lon": 100.445},
    {"name": "Taiwan Palace", "location": "Borealis", "diet": "Non-Halal", "votes": 0, "lat": 5.337, "lon": 100.446},
    {"name": "Korean BBQ", "location": "Borealis", "diet": "Non-Halal", "votes": 0, "lat": 5.338, "lon": 100.447},
    {"name": "Sushi Ya", "location": "Borealis", "diet": "Halal", "votes": 0, "lat": 5.339, "lon": 100.448},
    {"name": "Burger King", "location": "Design Village", "diet": "Any", "votes": 0, "lat": 5.350, "lon": 100.460},
    {"name": "Subway", "location": "Batu Kawan", "diet": "Gluten-Free", "votes": 0, "lat": 5.370, "lon": 100.480}
]

# --- Load and Save JSON ---
def load_data(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return default_data

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# --- Initialize session state ---
if "lunch_options" not in st.session_state:
    st.session_state.lunch_options = load_data(OPTIONS_FILE, default_options)

if "lunch_record" not in st.session_state:
    st.session_state.lunch_record = load_data(RECORD_FILE, [])

if "suggested_spot" not in st.session_state:
    st.session_state.suggested_spot = None

# --- Title ---
st.title("🍽️ Lunch Decision Dashboard")

# --- Suggestion Section ---
st.subheader("🔍 Filter & Suggest Lunch Spot")
filter_location = st.selectbox("Filter by Location", ["Any"] + list(set([opt["location"] for opt in st.session_state.lunch_options])))
filter_diet = st.selectbox("Filter by Dietary Preference", ["Any", "Halal", "Non-Halal", "Vegetarian", "Vegan", "Gluten-Free"])

filtered_options = [
    opt for opt in st.session_state.lunch_options
    if (filter_location == "Any" or opt["location"] == filter_location) and
       (filter_diet == "Any" or opt["diet"] == filter_diet)
]

if st.button("🎲 Suggest Lunch Spot"):
    if filtered_options:
        suggestion = random.choice(filtered_options)
        st.session_state.suggested_spot = suggestion
        st.success(f"Suggested: {suggestion['name']} ({suggestion['location']}, {suggestion['diet']})")
    else:
        st.warning("No matching lunch options found.")

# --- Map Section ---
st.subheader("🗺️ Lunch Spot Location")
if st.session_state.suggested_spot:
    spot = st.session_state.suggested_spot
    if "lat" in spot and "lon" in spot:
        st.map(pd.DataFrame([{"lat": spot["lat"], "lon": spot["lon"]}]))
    else:
        st.warning("Suggested spot has no coordinates.")
else:
    st.map(pd.DataFrame([{"lat": 5.370, "lon": 100.480}]))  # Default to Batu Kawan

# --- Voting Trends ---
st.subheader("📊 Voting Trends")
df_votes = pd.DataFrame(st.session_state.lunch_options)
if not df_votes.empty:
    chart = alt.Chart(df_votes).mark_bar().encode(
        x=alt.X('name', sort='-y', title='Restaurant'),
        y=alt.Y('votes', title='Votes'),
        color='diet'
    ).properties(width=600, height=300)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No voting data available.")

# --- Record Today's Lunch ---
st.subheader("🍴 Record Today's Lunch")
today = datetime.date.today().strftime("%Y-%m-%d")
selected_place = st.selectbox("Where did you go for lunch today?", [opt["name"] for opt in st.session_state.lunch_options])
if st.button("📍 Record Today's Lunch"):
    record_entry = {"date": today, "place": selected_place}
    st.session_state.lunch_record.append(record_entry)
    save_data(RECORD_FILE, st.session_state.lunch_record)
    st.success(f"Recorded: {selected_place} on {today}")

# --- Past Records ---
st.subheader("📆 Past Lunch Records")
for record in reversed(st.session_state.lunch_record):
    st.write(f"{record['date']}: {record['place']}")
