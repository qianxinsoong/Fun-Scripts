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

# --- Default lunch options (shortened for brevity) ---
default_options = [
    {"name": "Meetcha Cafe & Eatery", "location": "Vervea", "diet": "Any", "theme": "Fusion (Local & Western)", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Pan Pan Restaurant", "location": "Vervea", "diet": "Halal", "theme": "Asian, Muslim-friendly", "votes": 0, "lat": 5.2646, "lon": 100.4376},
    {"name": "Temp Cafe", "location": "Vervea", "diet": "Halal", "theme": "Cafe, Western", "votes": 0, "lat": 5.2647, "lon": 100.4377},
    {"name": "Shunka Japanese Restaurant", "location": "Vervea", "diet": "Non-Halal", "theme": "Japanese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Ren Wafu Ramen & Don", "location": "Vervea", "diet": "Non-Halal", "theme": "Japanese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "WG Wondrous Gastronomy", "location": "Vervea", "diet": "Any", "theme": "Fusion", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "A Pause Restaurant", "location": "Vervea", "diet": "Any", "theme": "Western", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Cili Giling", "location": "Vervea", "diet": "Halal", "theme": "Malay", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Harenee Spice House", "location": "Vervea", "diet": "Halal", "theme": "Indian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "The Wok & Flame Restaurant", "location": "Vervea", "diet": "Halal", "theme": "Asian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Wen Kee Restaurant", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "SanTai", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Five Grains Noodles", "location": "Vervea", "diet": "Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Nasi Ayam Kawan", "location": "Vervea", "diet": "Halal", "theme": "Malay", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "AB Home & Café", "location": "Vervea", "diet": "Any", "theme": "Cafe", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Kopi Saigon Batu Kawan", "location": "Vervea", "diet": "Halal", "theme": "Vietnamese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Nasi Lemak Datin", "location": "Vervea", "diet": "Halal", "theme": "Malay", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Rare Brew Café", "location": "Vervea", "diet": "Halal", "theme": "Cafe", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Safa Matcha", "location": "Vervea", "diet": "Halal", "theme": "Japanese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Hello! Ma La Tang", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Shao Lak Restaurant", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Face to Face Noodle House", "location": "Vervea", "diet": "Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Chicken Claypot House", "location": "Vervea", "diet": "Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "SK Bhavan", "location": "Vervea", "diet": "Halal", "theme": "Indian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Medrich Café", "location": "Vervea", "diet": "Any", "theme": "Cafe", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Snacks! Bakery & Café", "location": "Vervea", "diet": "Any", "theme": "Bakery, Cafe", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "King Kong Ramen", "location": "Vervea", "diet": "Non-Halal", "theme": "Japanese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Yusuf Restaurant", "location": "Vervea", "diet": "Halal", "theme": "Indian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Indian Heritage Restaurant", "location": "Vervea", "diet": "Halal", "theme": "Indian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Le Man Tang Restaurant", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Sri Meenackshi Bhavan", "location": "Vervea", "diet": "Halal", "theme": "Indian", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "18 Garden (Uncle Kin Chili Pan Mee)", "location": "Vervea", "diet": "Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Unggul Nasi Campur", "location": "Vervea", "diet": "Halal", "theme": "Malay", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "M&L Food House", "location": "Vervea", "diet": "Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Dynasty Porridge", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Hao Yun", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "James Foo Western Food", "location": "Vervea", "diet": "Any", "theme": "Western", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Mala Miss Me", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "MaoPaiHuo", "location": "Vervea", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.2645, "lon": 100.4375},
    {"name": "Asian Houze", "location": "Utropolis", "diet": "Any", "theme": "Asian Fusion, Halal", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "OoriDoori Utropolis", "location": "Utropolis", "diet": "Halal", "theme": "Korean BBQ", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "JY Kopitiam", "location": "Utropolis", "diet": "Non-Halal", "theme": "Local Kopitiam", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Lang Hiam Kopitiam", "location": "Utropolis", "diet": "Non-Halal", "theme": "Local Kopitiam", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Kobab Korea Bbq", "location": "Utropolis", "diet": "Non-Halal", "theme": "Korean BBQ", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "CAFE ONE TWENTY 9", "location": "Utropolis", "diet": "Any", "theme": "Cafe, Western", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Mulam Hongkong Economy Canteen", "location": "Utropolis", "diet": "Non-Halal", "theme": "Hong Kong Street Food", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Mala Miss Me", "location": "Utropolis", "diet": "Non-Halal", "theme": "Chinese Mala", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Tai Jia Lam Thai Cuisine", "location": "Utropolis", "diet": "Non-Halal", "theme": "Thai Cuisine", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Last Time Coffee Shop", "location": "Utropolis", "diet": "Any", "theme": "Local Coffee Shop", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "James Foo Western Food", "location": "Utropolis", "diet": "Any", "theme": "Western", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Ideal Genki Sushi", "location": "Utropolis", "diet": "Halal", "theme": "Japanese Sushi", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Makan Nasi", "location": "Utropolis", "diet": "Halal", "theme": "Local Rice Dishes", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Refresh (RF Coffee)", "location": "Utropolis", "diet": "Any", "theme": "Cafe, Coffee", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Ai-CHA", "location": "Utropolis", "diet": "Any", "theme": "Bubble Tea, Snacks", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Little June Sushi", "location": "Utropolis", "diet": "Halal", "theme": "Japanese Sushi", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Ready to E.A.T", "location": "Utropolis", "diet": "Any", "theme": "Fusion, Western", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "QQ", "location": "Utropolis", "diet": "Non-Halal", "theme": "Chinese Noodles", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Thai Tuk Tuk", "location": "Utropolis", "diet": "Non-Halal", "theme": "Thai Cuisine", "votes": 0, "lat": 5.2404, "lon": 100.4383},
    {"name": "Sand Wish", "location": "Borealis", "diet": "Halal", "theme": "Sandwiches, Bowls, Pork-free", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Pitstop Borealis Cafe", "location": "Borealis", "diet": "Non-Halal", "theme": "Fusion Café", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Sushi Ya", "location": "Borealis", "diet": "Halal", "theme": "Sushi", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Nasi Lemak Ketua Kampung", "location": "Borealis", "diet": "Halal", "theme": "Nasi Lemak", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Starbucks", "location": "Borealis", "diet": "Halal", "theme": "Coffee & Pastries", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Le Man Tang Restaurant", "location": "Borealis", "diet": "Non-Halal", "theme": "Chinese", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Taiwanese Palace", "location": "Borealis", "diet": "Non-Halal", "theme": "Taiwan Food", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Nom Nom Eatery", "location": "Borealis", "diet": "Halal", "theme": "Asian Fusion", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Dotori Restaurant", "location": "Borealis", "diet": "Non-Halal", "theme": "Korean", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Mi Ban Café", "location": "Borealis", "diet": "Halal", "theme": "Local Café", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "King Kong Ramen", "location": "Borealis", "diet": "Non-Halal", "theme": "Japanese Ramen", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Dragon Noodle", "location": "Borealis", "diet": "Non-Halal", "theme": "Chinese Noodles", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Ayam Penyet Mummy", "location": "Borealis", "diet": "Halal", "theme": "Indonesian", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Taco Bell", "location": "Borealis", "diet": "Halal", "theme": "Mexican Fast Food", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Nasi Kandar Nasmir", "location": "Borealis", "diet": "Halal", "theme": "Nasi Kandar", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Secret Recipe", "location": "Borealis", "diet": "Halal", "theme": "Western & Cakes", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Subway", "location": "Borealis", "diet": "Halal", "theme": "Sandwiches", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Nasi Kandar Ali Khan", "location": "Borealis", "diet": "Halal", "theme": "Nasi Kandar", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Pizza Hut", "location": "Borealis", "diet": "Halal", "theme": "Pizza", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "Zus", "location": "Borealis", "diet": "Halal", "theme": "Coffee & Pastries", "votes": 0, "lat": 5.265, "lon": 100.44},
    {"name": "IKEA", "location": "IKEA Area", "diet": "Halal", "theme": "Swedish, Family Dining", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "Phat Bee Café", "location": "IKEA Area", "diet": "Halal", "theme": "Asian Fusion Café", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "Gerai Makan Pergi Haji", "location": "IKEA Area", "diet": "Halal", "theme": "Local Malay Cuisine", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "The Coffee Bean & Tea Leaf", "location": "IKEA Area", "diet": "Halal", "theme": "Coffee, Western Café", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "KFC", "location": "IKEA Area", "diet": "Halal", "theme": "Fast Food, Fried Chicken", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "Mc Donalds", "location": "IKEA Area", "diet": "Halal", "theme": "Fast Food, Burgers", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "Kenny Rogers", "location": "IKEA Area", "diet": "Halal", "theme": "Western, Rotisserie Chicken", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "TeaLive", "location": "IKEA Area", "diet": "Halal", "theme": "Bubble Tea, Beverages", "votes": 0, "lat": 5.24, "lon": 100.44},
    {"name": "A&W", "location": "IKEA Area", "diet": "Halal", "theme": "Fast Food, American", "votes": 0, "lat": 5.24, "lon": 100.44}
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

# --- HTML Rendering ---
def render_suggestion_card(suggestion):
    return f"""
    <div style="padding: 10px; background-color: #e6f7ff; border-radius: 8px; border: 1px solid #1890ff;">
        <p style="margin: 0; font-size: 16px;">
        🎯 <strong>{suggestion['name']}</strong> | 📍 Location: {suggestion['location']} | 🥗 Diet: {suggestion['diet']} | 🍽️ Theme: {suggestion.get('theme', 'N/A')}
        </p>
    </div>
    """

def render_vote_card(option):
    return f"""
    <div style="padding: 10px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 10px;">
        <strong style="font-size: 18px;">{option['name']}</strong><br>
        <span style="font-size: 14px;">Location: {option['location']} | Diet: {option['diet']} | Theme: {option.get('theme', 'N/A')}</span><br>
        <span style="font-size: 14px;">Votes: {option['votes']}</span>
    </div>
    """

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
theme = st.sidebar.text_input("Food Theme")
lat = st.sidebar.text_input("Latitude")
lon = st.sidebar.text_input("Longitude")

if st.sidebar.button("Add Option"):
    if name and location and lat and lon and theme:
        try:
            lat_val = float(lat)
            lon_val = float(lon)
            new_option = {"name": name, "location": location, "diet": diet, "theme": theme, "votes": 0, "lat": lat_val, "lon": lon_val}
            if not any(opt["name"].lower() == name.lower() and opt["location"].lower() == location.lower() for opt in st.session_state.lunch_options):
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
    filter_diet = st.selectbox("Filter by Dietary Preference", ["Any"] + sorted(set(opt["diet"] for opt in st.session_state.lunch_options)))
    filter_theme = st.selectbox("Filter by Food Theme", ["Any"] + sorted(set(opt["theme"] for opt in st.session_state.lunch_options)))

    filtered_options = [
        opt for opt in st.session_state.lunch_options
        if (filter_location == "Any" or opt["location"] == filter_location) and
           (filter_diet == "Any" or opt["diet"] == filter_diet) and
           (filter_theme == "Any" or opt.get("theme", "N/A") == filter_theme)
    ]

    if st.button("🎲 Suggest Lunch Spot"):
        if filtered_options:
            suggestion = random.choice(filtered_options)
            st.session_state.suggested_spot = suggestion
            st.markdown(render_suggestion_card(suggestion), unsafe_allow_html=True)
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

    if st.button("📤 Export Lunch Records"):
        df_record = pd.DataFrame(st.session_state.lunch_record)
        st.download_button("Download CSV", df_record.to_csv(index=False), "lunch_records.csv", "text/csv")

    st.markdown("### 📆 Past Lunch Records")
    for record in reversed(st.session_state.lunch_record):
        st.write(f"{record['date']}: {record['place']}")

    st.subheader("📊 Vote for Your Favorite")
    vote_location = st.selectbox("Filter by Location (Voting)", ["Any"] + sorted(set(opt["location"] for opt in st.session_state.lunch_options)))
    vote_diet = st.selectbox("Filter by Dietary Preference (Voting)", ["Any"] + sorted(set(opt["diet"] for opt in st.session_state.lunch_options)))
    vote_theme = st.multiselect("Filter by Food Theme (Voting)", sorted(set(opt.get("theme", "N/A") for opt in st.session_state.lunch_options)))

    vote_filtered_options = [
        opt for opt in st.session_state.lunch_options
        if (vote_location == "Any" or opt["location"] == vote_location) and
           (vote_diet == "Any" or opt["diet"] == vote_diet) and
           (not vote_theme or opt.get("theme", "N/A") in vote_theme)
    ]
    vote_filtered_options = sorted(vote_filtered_options, key=lambda x: x["votes"], reverse=True)

    for i, opt in enumerate(vote_filtered_options):
        with st.container():
            st.markdown(render_vote_card(opt), unsafe_allow_html=True)
            if st.button(f"👍 Vote for {opt['name']}", key=f"vote_{i}"):
                opt["votes"] += 1
                save_data(OPTIONS_FILE, st.session_state.lunch_options)
                st.success(f"Thanks for voting for {opt['name']}!")

    st.subheader("📋 Current Lunch Options")
    for opt in st.session_state.lunch_options:
        st.write(f"{opt['name']} ({opt['location']}, {opt['diet']}, {opt.get('theme', 'N/A')}) - Votes: {opt['votes']}")

# --- Suggestion Column ---
with suggestion_col:
    st.markdown("<h3>🤔 Today's Suggestion</h3><p>You Vote la, then see how</p>", unsafe_allow_html=True)
    if st.session_state.lunch_options:
        scores = {opt['name']: opt['votes'] for opt in st.session_state.lunch_options}
        sorted_options = sorted(st.session_state.lunch_options, key=lambda x: scores.get(x['name'], 0), reverse=True)
        top_pick = sorted_options[0]
        st.success(f"Today's Top Pick: {top_pick['name']} ({top_pick['location']}, {top_pick['diet']}, {top_pick.get('theme', 'N/A')})")

        st.markdown("### 🗺️ Lunch Spot Location")
        if st.session_state.suggested_spot and "lat" in st.session_state.suggested_spot and "lon" in st.session_state.suggested_spot:
            map_data = pd.DataFrame([{
                "lat": st.session_state.suggested_spot["lat"],
                "lon": st.session_state.suggested_spot["lon"]
            }])
            st.map(map_data)
        else:
            default_map_data = pd.DataFrame([{"lat": 5.2189, "lon": 100.4491}])
            st.map(default_map_data)

        # Optional: Show all filtered options on map
        # map_data = pd.DataFrame([{"lat": opt["lat"], "lon": opt["lon"]} for opt in filtered_options])
        # st.map(map_data)

        st.markdown("### 📊 Voting Trends")
        df_votes = pd.DataFrame(st.session_state.lunch_options)
        if "theme" not in df_votes.columns:
            df_votes["theme"] = "N/A"
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
