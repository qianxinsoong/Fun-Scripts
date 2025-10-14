import streamlit as st
import random
import datetime
import json
import os
import pandas as pd
import altair as alt

# --- File paths ---
OPTIONS_FILE = "lunch_options_with_theme.json"
RECORD_FILE = "lunch_record.json"

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
    st.session_state.lunch_options = load_data(OPTIONS_FILE, [])

if "lunch_record" not in st.session_state:
    st.session_state.lunch_record = load_data(RECORD_FILE, [])

if "suggested_spot" not in st.session_state:
    st.session_state.suggested_spot = None

# --- Title ---
st.title("🍽️ Lunch Decision Dashboard")

# --- Sidebar: Add new lunch option ---
st.sidebar.header("➕ Add Lunch Option")
name = st.sidebar.text_input("Restaurant Name")
location = st.sidebar.text_input("Location")
diet = st.sidebar.selectbox("Dietary Preference", ["Any", "Halal", "Non-Halal", "Vegetarian", "Vegan", "Gluten-Free"])
theme = st.sidebar.text_input("Theme")
lat = st.sidebar.text_input("Latitude")
lon = st.sidebar.text_input("Longitude")

if st.sidebar.button("Add Option"):
    if name and location and lat and lon and theme:
        try:
            lat_val = float(lat)
            lon_val = float(lon)
            new_option = {"name": name, "location": location, "diet": diet, "theme": theme, "votes": 0, "lat": lat_val, "lon": lon_val}
            if not any(opt["name"].lower() == name.lower() for opt in st.session_state.lunch_options):
                st.session_state.lunch_options.append(new_option)
                save_data(OPTIONS_FILE, st.session_state.lunch_options)
                st.sidebar.success(f"Added {name} to lunch options.")
            else:
                st.sidebar.warning(f"{name} is already in the list.")
        except ValueError:
            st.sidebar.error("Latitude and Longitude must be valid numbers.")
    else:
        st.sidebar.error("Please enter all fields including coordinates and theme.")

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
    filter_location = st.selectbox("Filter by Location", ["Any"] + sorted(set(opt["location"] for opt in st.session_state.lunch_options)))
    filter_diet = st.selectbox("Filter by Dietary Preference", sorted(set(opt["diet"] for opt in st.session_state.lunch_options)))
    filter_theme = st.selectbox("Filter by Theme", ["Any"] + sorted(set(opt["theme"] for opt in st.session_state.lunch_options)))

    filtered_options = [
        opt for opt in st.session_state.lunch_options
        if (filter_location == "Any" or opt["location"] == filter_location) and
           (filter_diet == "Any" or opt["diet"] == filter_diet) and
           (filter_theme == "Any" or opt["theme"] == filter_theme)
    ]

    if st.button("🎲 Suggest Lunch Spot"):
        if filtered_options:
            suggestion = random.choice(filtered_options)
            st.session_state.suggested_spot = suggestion
            st.markdown(
                f"""
                <div style="padding: 10px; background-color: #e6f7ff; border-radius: 8px; border: 1px solid #1890ff;">
                    <p style="margin: 0; font-size: 16px;">
                    🎯 <strong>{suggestion['name']}</strong> | 📍 Location: {suggestion['location']} | 🥗 Diet: {suggestion['diet']} | 🎨 Theme: {suggestion['theme']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("No matching lunch options found.")

    st.subheader("🍴 Today's Lunch Record")
    today = datetime.date.today().strftime("%Y-%m-%d")
    selected_place = st.selectbox("Where did you go for lunch today?", options=[opt["name"] for opt in st.session_state.lunch_options], index=0, placeholder="Type or select a restaurant...")
    if st.button("📍 Record Today's Lunch"):
        record_entry = {"date": today, "place": selected_place}
        st.session_state.lunch_record.append(record_entry)
        save_data(RECORD_FILE, st.session_state.lunch_record)
        st.success(f"Recorded: {selected_place} on {today}")

    st.markdown("### 📆 Past Lunch Records")
    for record in reversed(st.session_state.lunch_record):
        st.write(f"{record['date']}: {record['place']}")

with st.expander("📊 Vote for Your Favorite"):
    vote_location = st.selectbox("Filter by Location (Voting)", ["Any"] + sorted(set(opt["location"] for opt in st.session_state.lunch_options)))
    vote_diet = st.selectbox("Filter by Dietary Preference (Voting)", sorted(set(opt["diet"] for opt in st.session_state.lunch_options)))
    vote_theme = st.selectbox("Filter by Theme (Voting)", ["Any"] + sorted(set(opt["theme"] for opt in st.session_state.lunch_options)))
    
    vote_filtered_options = [opt for opt in st.session_state.lunch_options
                             if (vote_location == "Any" or opt["location"] == vote_location) and
                             (vote_diet == "Any" or opt["diet"] == vote_diet) and
                             (vote_theme == "Any" or opt["theme"] == vote_theme)]
    
    for i, opt in enumerate(vote_filtered_options):
        with st.expander(f"🍽️ {opt['name']}"):
            st.markdown(f"""
                **Location**: {opt['location']}  
                **Diet**: {opt['diet']}  
                **Theme**: {opt['theme']}  
                **Votes**: {opt['votes']}
                """)
    if st.button(f"👍 Vote for {opt['name']}", key=f"vote_{i}"): opt["votes"] += 1
        save_data(OPTIONS_FILE, st.session_state.lunch_options)
        st.success(f"Thanks for voting for {opt['name']}!")
     
with st.expander("📋 Current Lunch Options"):
    for opt in st.session_state.lunch_options:
        st.write(f"{opt['name']} ({opt['location']}, {opt['diet']}, {opt['theme']}) - Votes: {opt['votes']}")
        
# --- Suggestion Column ---
with suggestion_col:
    st.markdown("<h3>🤔 Suggestion</h3><p>You Vote la, then see how</p>", unsafe_allow_html=True)
    if st.session_state.lunch_options:
        scores = {opt['name']: opt['votes'] for opt in st.session_state.lunch_options}
        sorted_options = sorted(st.session_state.lunch_options, key=lambda x: scores.get(x['name'], 0), reverse=True)
        top_pick = sorted_options[0]
        st.success(f"Today's Top Pick: {top_pick['name']} ({top_pick['location']}, {top_pick['diet']}, {top_pick['theme']})")

        st.markdown("### 🗺️ Lunch Location")
        if st.session_state.suggested_spot and "lat" in st.session_state.suggested_spot and "lon" in st.session_state.suggested_spot:
            map_data = pd.DataFrame([{
                "lat": st.session_state.suggested_spot["lat"],
                "lon": st.session_state.suggested_spot["lon"]
            }])
            st.map(map_data)
        else:
            default_map_data = pd.DataFrame([{"lat": 5.2189, "lon": 100.4491}])  # Batu Kawan default
            st.map(default_map_data)

        st.markdown("### 📊 Voting Trends")
        df_votes = pd.DataFrame(st.session_state.lunch_options)
        chart = alt.Chart(df_votes).mark_bar().encode(
            x=alt.X('name', sort='-y', title='Restaurant'),
            y=alt.Y('votes', title='Votes'),
            color='theme'
        ).properties(width=300, height=300)
        st.altair_chart(chart, use_container_width=True)

        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔁 Suggest Again"):
                if filtered_options:
                    suggestion = random.choice(filtered_options)
                    st.session_state.suggested_spot = suggestion
                    st.experimental_rerun()
        with col2:
            st.button("📌 Pin This Spot")
        with col3:
            st.button("🗺️ Nearby Options")

        st.markdown("### 📈 Dashboard Stats")
        st.metric("Total Votes", sum(opt["votes"] for opt in st.session_state.lunch_options))
        st.metric("Lunch Records", len(st.session_state.lunch_record))
    else:
        st.info("Add lunch options to get smart suggestions.")
