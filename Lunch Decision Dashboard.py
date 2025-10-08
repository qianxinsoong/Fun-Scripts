import streamlit as st
import random
import datetime
import json
import os

# --- File paths for persistent storage ---
OPTIONS_FILE = "lunch_options.json"
HISTORY_FILE = "lunch_history.json"

# --- Default lunch options ---
default_options = [
    {"name": "Nasi Kandar Nasmeer", "location": "Borealis", "diet": "Halal", "votes": 0},
    {"name": "Taiwan Palace", "location": "Borealis", "diet": "Non-Halal", "votes": 0},
    {"name": "Korean BBQ", "location": "Borealis", "diet": "Non-Halal", "votes": 0},
    {"name": "Sushi Ya", "location": "Borealis", "diet": "Halal", "votes": 0},
    {"name": "Nasi Kandar Ali Khan", "location": "Borealis", "diet": "Halal", "votes": 0},
    {"name": "Secret Recipe", "location": "Borealis", "diet": "Halal", "votes": 0},
    {"name": "Nasi Lemak Ketua Kampung", "location": "Borealis", "diet": "Halal", "votes": 0},
    {"name": "Dragon Noodles", "location": "Borealis", "diet": "Non-Halal", "votes": 0},
    {"name": "Inside Scoop", "location": "Borealis", "diet": "Desert", "votes": 0},
    {"name": "Burger King", "location": "Design Village", "diet": "Any", "votes": 0},
    {"name": "Padi House", "location": "Design Village", "diet": "Any", "votes": 0},
    {"name": "Design Village Food Court", "location": "Design Village", "diet": "Any", "votes": 0},
    {"name": "Thai Tuk Tuk", "location": "Utropolis", "diet": "Non-Halal", "votes": 0},
    {"name": "The Ship Chinese Food", "location": "Batu Kawan", "diet": "Halal", "votes": 0},
    {"name": "Subway", "location": "Batu Kawan", "diet": "Gluten-Free", "votes": 0}
]

# --- Load data from JSON files ---
def load_data(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return default_data

# --- Save data to JSON files ---
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# --- Initialize session state ---
if "lunch_options" not in st.session_state:
    st.session_state.lunch_options = load_data(OPTIONS_FILE, default_options)

if "history" not in st.session_state:
    st.session_state.history = load_data(HISTORY_FILE, [])

# --- Title ---
st.title("🍽️ Lunch Decision Dashboard")

# --- Sidebar: Add new lunch option ---
st.sidebar.header("➕ Add Lunch Option")
name = st.sidebar.text_input("Restaurant Name")
location = st.sidebar.text_input("Location")
diet = st.sidebar.selectbox("Dietary Preference", ["Any", "Halal", "Vegetarian", "Vegan", "Gluten-Free"])

if st.sidebar.button("Add Option"):
    if name and location:
        new_option = {"name": name, "location": location, "diet": diet, "votes": 0}
        if not any(opt["name"].lower() == name.lower() for opt in st.session_state.lunch_options):
            st.session_state.lunch_options.append(new_option)
            save_data(OPTIONS_FILE, st.session_state.lunch_options)
            st.sidebar.success(f"Added {name} to lunch options.")
        else:
            st.sidebar.warning(f"{name} is already in the list.")
    else:
        st.sidebar.error("Please enter both name and location.")

# --- Layout: Two columns ---
main_col, suggestion_col = st.columns([3, 2])

# --- Main Column ---
with main_col:
    st.subheader("🔍 Filter & Suggest Lunch Spot")
    filter_location = st.selectbox("Filter by Location", ["Any"] + list(set([opt["location"] for opt in st.session_state.lunch_options])))
    filter_diet = st.selectbox("Filter by Dietary Preference", ["Any", "Halal", "Vegetarian", "Vegan", "Gluten-Free"])

    filtered_options = [
        opt for opt in st.session_state.lunch_options
        if (filter_location == "Any" or opt["location"] == filter_location) and
           (filter_diet == "Any" or opt["diet"] == filter_diet)
    ]

    if st.button("🎲 Suggest Lunch Spot"):
        if filtered_options:
            suggestion = random.choice(filtered_options)
            st.success(f"Today's suggestion: {suggestion['name']} ({suggestion['location']}, {suggestion['diet']})")
            new_entry = {
                "name": suggestion["name"],
                "location": suggestion["location"],
                "diet": suggestion["diet"],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.history.append(new_entry)
            save_data(HISTORY_FILE, st.session_state.history)
        else:
            st.warning("No matching lunch options found.")

    st.subheader("📊 Vote for Your Favorite")
    for i, opt in enumerate(st.session_state.lunch_options):
        cols = st.columns([3, 1])
        cols[0].write(f"{opt['name']} ({opt['location']}, {opt['diet']}) - Votes: {opt['votes']}")
        if cols[1].button(f"Vote {i}"):
            st.session_state.lunch_options[i]["votes"] += 1
            save_data(OPTIONS_FILE, st.session_state.lunch_options)

    st.subheader("🗂️ Lunch Decision History")
    for entry in reversed(st.session_state.history):
        st.write(f"{entry['timestamp']}: {entry['name']} ({entry['location']}, {entry['diet']})")

    st.subheader("📋 Current Lunch Options")
    for opt in st.session_state.lunch_options:
        st.write(f"{opt['name']} ({opt['location']}, {opt['diet']}) - Votes: {opt['votes']}")

# --- Smart Suggestion Box ---
with suggestion_col:
    st.markdown("## 🤔 Smart Suggestion Box")
    if st.session_state.lunch_options:
        scores = {}
        for opt in st.session_state.lunch_options:
            scores[opt['name']] = opt['votes']

        recent_names = [entry['name'] for entry in st.session_state.history[-5:]]
        for name in recent_names:
            if name in scores:
                scores[name] += 2  # boost recent picks

        sorted_options = sorted(st.session_state.lunch_options, key=lambda x: scores.get(x['name'], 0), reverse=True)
        top_pick = sorted_options[0]

        st.markdown(
            f"""
            <div style="padding: 20px; background-color: #dff0d8; border-radius: 10px; border: 2px solid #3c763d;">
                <h2 style="color: #3c763d;">🍴 Today's Top Pick</h2>
                <h3>{top_pick['name']}</h3>
                <p><strong>Location:</strong> {top_pick['location']}</p>
                <p><strong>Dietary Preference:</strong> {top_pick['diet']}</p>
                <p><strong>Votes:</strong> {top_pick['votes']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Add lunch options to get smart suggestions.")
