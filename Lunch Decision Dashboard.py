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
    {"name": "Subway", "location": "Batu Kawan", "diet": "Gluten-Free", "votes": 0, "lat": 5.371, "lon": 100.481}
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

# --- Title ---
st.title("🍽️ Lunch Decision Dashboard")

# --- Sidebar: Add new lunch option ---
st.sidebar.header("➕ Add Lunch Option")
name = st.sidebar.text_input("Restaurant Name")
location = st.sidebar.text_input("Location")
diet = st.sidebar.selectbox("Dietary Preference", ["Any", "Halal", "Non-Halal", "Vegetarian", "Vegan", "Gluten-Free"])
lat = st.sidebar.text_input("Latitude")
lon = st.sidebar.text_input("Longitude")

if st.sidebar.button("Add Option"):
    if name and location and lat and lon:
        try:
            lat_val = float(lat)
            lon_val = float(lon)
            new_option = {"name": name, "location": location, "diet": diet, "votes": 0, "lat": lat_val, "lon": lon_val}
            if not any(opt["name"].lower() == name.lower() for opt in st.session_state.lunch_options):
                st.session_state.lunch_options.append(new_option)
                save_data(OPTIONS_FILE, st.session_state.lunch_options)
                st.sidebar.success(f"Added {name} to lunch options.")
            else:
                st.sidebar.warning(f"{name} is already in the list.")
        except ValueError:
            st.sidebar.error("Latitude and Longitude must be valid numbers.")
    else:
        st.sidebar.error("Please enter all fields including coordinates.")

# --- Admin Panel ---
st.sidebar.header("🔐 Admin Panel")
admin_password = st.sidebar.text_input("Enter Admin Password", type="password")

if admin_password == "admin123":
    st.sidebar.subheader("🔄 Reset Voting System")
    if st.sidebar.button("🔄 Reset All Votes"):
        for option in st.session_state.lunch_options:
            option["votes"] = 0
        save_data(OPTIONS_FILE, st.session_state.lunch_options)
        st.sidebar.success("✅ All votes have been reset to zero.")
elif admin_password:
    st.sidebar.error("❌ Incorrect password.")

# --- Layout: Two columns ---
main_col, suggestion_col = st.columns([3, 2])

# --- Main Column ---
with main_col:
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
            st.markdown(
                f"""
                <div style="padding: 13px; background-color: #e6f7ff; border-radius: 10px; border: 2px solid #1890ff;">
                    <h3 style="color: #1890ff;">
                    🎲 <strong>{suggestion['name']}</strong>  |  Location: {suggestion['location']}  |  Diet: {suggestion['diet']}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("No matching lunch options found.")

    st.subheader("🍴 Today's Lunch Record")
    today = datetime.date.today().strftime("%Y-%m-%d")
    selected_place = st.selectbox("Where did you go for lunch today?", [opt["name"] for opt in st.session_state.lunch_options])
    if st.button("📍 Record Today's Lunch"):
        record_entry = {"date": today, "place": selected_place}
        st.session_state.lunch_record.append(record_entry)
        save_data(RECORD_FILE, st.session_state.lunch_record)
        st.success(f"Recorded: {selected_place} on {today}")

    st.markdown("### 📆 Past Lunch Records")
    for record in reversed(st.session_state.lunch_record):
        st.write(f"{record['date']}: {record['place']}")

    st.subheader("📊 Vote for Your Favorite")
    vote_location = st.selectbox("Filter by Location (Voting)", ["Any"] + sorted(set(opt["location"] for opt in st.session_state.lunch_options)))
    vote_diet = st.selectbox("Filter by Dietary Preference (Voting)", ["Any"] + sorted(set(opt["diet"] for opt in st.session_state.lunch_options)))

    vote_filtered_options = [
        opt for opt in st.session_state.lunch_options
        if (vote_location == "Any" or opt["location"] == vote_location) and
           (vote_diet == "Any" or opt["diet"] == vote_diet)
    ]

    for i, opt in enumerate(vote_filtered_options):
        with st.container():
            st.markdown(
                f"""
                <div style="padding: 10px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 10px;">
                    <strong style="font-size: 18px;">{opt['name']}</strong><br>
                    <span style="font-size: 14px;">Location: {opt['location']} | Diet: {opt['diet']}</span><br>
                    <span style="font-size: 14px;">Votes: {opt['votes']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"👍 Vote for {opt['name']}", key=f"vote_{i}"):
                opt["votes"] += 1
                save_data(OPTIONS_FILE, st.session_state.lunch_options)
                st.success(f"Thanks for voting for {opt['name']}!")

    st.subheader("📋 Current Lunch Options")
    for opt in st.session_state.lunch_options:
        st.write(f"{opt['name']} ({opt['location']}, {opt['diet']}) - Votes: {opt['votes']}")

# --- Suggestion Column ---
with suggestion_col:
    st.markdown("""<p style='font-size:24px; font-weight:bold; margin-bottom:0;'>🤔 Today's Suggestion</p><p style='font-size:14px; margin-top: 0;'>You Vote la, then see how</p>""", unsafe_allow_html=True)
    if st.session_state.lunch_options:
        scores = {opt['name']: opt['votes'] for opt in st.session_state.lunch_options}
        sorted_options = sorted(st.session_state.lunch_options, key=lambda x: scores.get(x['name'], 0), reverse=True)
        top_pick = sorted_options[0]
        st.success(f"Today's Top Pick: {top_pick['name']} ({top_pick['location']}, {top_pick['diet']})")

        st.markdown("### 🗺️ Lunch Spot Locations (Filtered)")
        map_filtered_data = pd.DataFrame([
            {"lat": opt["lat"], "lon": opt["lon"]}
            for opt in filtered_options if "lat" in opt and "lon" in opt
        ])
        if not map_filtered_data.empty:
            st.map(map_filtered_data)
        else:
            st.info("No matching locations to display on the map.")

        st.markdown("### 📍 Today's Lunch Location")
        selected_spot = next((opt for opt in st.session_state.lunch_options if opt["name"] == selected_place), None)
        if selected_spot and "lat" in selected_spot and "lon" in selected_spot:
            st.map(pd.DataFrame([{"lat": selected_spot["lat"], "lon": selected_spot["lon"]}]))

        st.markdown("### 📊 Voting Trends")
        df_votes = pd.DataFrame(st.session_state.lunch_options)
        chart = alt.Chart(df_votes).mark_bar().encode(
            x=alt.X('name', sort='-y', title='Restaurant'),
            y=alt.Y('votes', title='Votes'),
            color='diet'
        ).properties(width=300, height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Add lunch options to get smart suggestions.")
