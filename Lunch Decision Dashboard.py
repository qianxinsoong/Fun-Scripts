import streamlit as st
import random
import datetime

# Initialize session state variables
if "lunch_options" not in st.session_state:
    st.session_state.lunch_options = []

if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.title("🍽️ Lunch Decision Dashboard")

# Sidebar for adding new lunch options
st.sidebar.header("➕ Add Lunch Option")
name = st.sidebar.text_input("Restaurant Name")
location = st.sidebar.text_input("Location")
diet = st.sidebar.selectbox("Dietary Preference", ["Any", "Halal", "Vegetarian", "Vegan", "Gluten-Free"])

if st.sidebar.button("Add Option"):
    if name and location:
        st.session_state.lunch_options.append({
            "name": name,
            "location": location,
            "diet": diet,
            "votes": 0
        })
        st.sidebar.success(f"Added {name} to lunch options.")
    else:
        st.sidebar.error("Please enter both name and location.")

# Create two columns for layout
main_col, suggestion_col = st.columns([3, 2])

# Main column with interactive features
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
            st.session_state.history.append({
                "name": suggestion["name"],
                "location": suggestion["location"],
                "diet": suggestion["diet"],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            st.warning("No matching lunch options found.")

    st.subheader("📊 Vote for Your Favorite")
    for i, opt in enumerate(st.session_state.lunch_options):
        cols = st.columns([3, 1])
        cols[0].write(f"{opt['name']} ({opt['location']}, {opt['diet']}) - Votes: {opt['votes']}")
        if cols[1].button(f"Vote {i}"):
            st.session_state.lunch_options[i]["votes"] += 1

    st.subheader("🗂️ Lunch Decision History")
    for entry in reversed(st.session_state.history):
        st.write(f"{entry['timestamp']}: {entry['name']} ({entry['location']}, {entry['diet']})")

    st.subheader("📋 Current Lunch Options")
    for opt in st.session_state.lunch_options:
        st.write(f"{opt['name']} ({opt['location']}, {opt['diet']}) - Votes: {opt['votes']}")

# Smart suggestion box in the right column
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
