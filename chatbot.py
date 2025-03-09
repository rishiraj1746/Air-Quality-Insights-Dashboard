import pandas as pd
import streamlit as st
import google.generativeai as genai

# Load API key securely from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")  # model

# Load dataset from app.py
@st.cache_data
def load_data():
    file_path = r"C:\Users\RISHIRAJ\OneDrive\Desktop\final_cleaned_city_day.csv"
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.month
    return df

df = load_data()  # Load dataset

# predefined questions for faster responses
predefined_responses = {
    "what is air quality index": "The Air Quality Index (AQI) is a scale that measures the level of pollution in the air.",
    "how is aqi calculated": "AQI is calculated based on concentrations of major pollutants like PM2.5, PM10, NO2, SO2, CO, and O3.",
    "which city has the worst air quality": "The city with the worst air quality is determined by the highest AQI value in the dataset.",
    "what are the effects of bad air quality": "Bad air quality can cause respiratory issues, heart disease, and other health problems.",
    "how can we improve air quality": "Air quality can be improved by reducing vehicle emissions, using renewable energy, and planting more trees.",
    "what is the safe level of pm2.5": "The WHO guideline suggests PM2.5 should not exceed 15 µg/m³ annually and 25 µg/m³ daily.",
    "what is the safest city in terms of air pollution": "The safest city is the one with the lowest average AQI in the dataset.",
    "what are the major pollutants in air": "The major pollutants include PM2.5, PM10, NO2, SO2, CO, and O3.",
    "how does weather affect air quality": "Weather factors such as temperature, wind, and humidity influence pollutant dispersion.",
    "how to check air quality in my area": "Use government monitoring websites, mobile apps, or real-time sensors.",
    "what are the main causes of air pollution": "Air pollution is caused by industrial emissions, vehicle exhaust, deforestation, and wildfires.",
    "how does air pollution affect human health": "Long-term exposure to air pollution can cause respiratory diseases, heart problems, and even cancer.",
    "how can i reduce indoor air pollution": "Use air purifiers, improve ventilation, avoid smoking indoors, and keep air-purifying plants.",
    "what is the impact of electric vehicles on air pollution": "Electric vehicles reduce emissions and improve air quality compared to gasoline and diesel cars.",
    "what are the effects of pm2.5 on health": "PM2.5 can penetrate deep into the lungs and bloodstream, causing respiratory and cardiovascular diseases.",
    "which country has the worst air pollution": "The worst air pollution levels are often found in countries with high industrial activity and poor regulations.",
    "what is acid rain and how is it related to air pollution": "Acid rain is caused by SO2 and NO2 emissions reacting with water, leading to environmental damage.",
    "how does public transport help reduce air pollution": "Public transport reduces individual car use, leading to lower emissions and less congestion.",
    "what role do forests play in air quality": "Forests act as carbon sinks, absorbing CO2 and filtering pollutants from the air.",
    "how does air pollution contribute to climate change": "Air pollution releases greenhouse gases like CO2, which trap heat and contribute to global warming.",
    "how do wildfires impact air quality": "Wildfires release large amounts of PM2.5, CO, and VOCs, leading to hazardous air quality.",
    "what are the different aqi categories": "AQI categories range from Good (0-50) to Hazardous (300+), indicating different levels of health risk.",
}

# Auto-generate city-specific AQI responses
for city in df["City"].unique():
    predefined_responses[f"what is the aqi in {city.lower()}"] = f"The AQI in {city} varies daily. Check the dataset for specific values."

def search_dataset(query):
    """Search dataset for relevant data or predefined responses"""
    query = query.lower()

    # First, check predefined responses
    if query in predefined_responses:
        return predefined_responses[query]

    # Get list of cities
    if "list of cities" in query:
        unique_cities = df["City"].unique().tolist()
        return f"The dataset contains air quality data for:\n\n{', '.join(unique_cities)}"

    # Find the most polluted city
    elif "most polluted city" in query:
        most_polluted = df.loc[df["AQI"].idxmax()]
        return f"The most polluted city is **{most_polluted['City']}** with an AQI of **{most_polluted['AQI']}** on {most_polluted['Date'].date()}."

    # Find the least polluted city
    elif "least polluted city" in query:
        least_polluted = df.loc[df["AQI"].idxmin()]
        return f"The least polluted city is **{least_polluted['City']}** with an AQI of **{least_polluted['AQI']}** on {least_polluted['Date'].date()}."

    # Check dataset for matching data
    results = df[df.apply(lambda row: query in row.to_string().lower(), axis=1)]
    
    if not results.empty:
        return results.to_string(index=False)

    return None  # Return None if no dataset match

def chatbot_ui():
    """Chatbot UI for Air Quality Assistant"""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.text_input("Ask me about the dataset or dashboard!", key="user_query")

    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)

        try:
            # First, check predefined responses & dataset
            bot_response = search_dataset(user_query)

            if bot_response is None:  # If no dataset match, use AI model
                prompt = f"""
                You are an AI assistant helping users understand an air quality dataset and Power BI dashboard.
                - Dataset contains air quality metrics for multiple cities.
                - The Power BI dashboard visualizes trends, pollutant levels, and air quality insights.
                - If the question is about a specific city or time period, provide dataset insights first.
                - If the question is about the dashboard, explain its purpose, usage, and key visualizations.

                Question: {user_query}
                """
                response = model.generate_content(prompt)
                bot_response = response.text

            with st.chat_message("assistant"):
                st.markdown(bot_response)

            st.session_state.messages.append({"role": "user", "content": user_query})
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

        except Exception as e:
            st.error(f"Error fetching response: {e}")

chatbot_ui()

def chatbot_button():
    """Button to toggle chatbot visibility, only on allowed pages."""
    
    # Check if session state has 'page' variable, if not, set a default
    if "page" not in st.session_state:
        st.session_state.page = "Home"  # Default page

    # pages where the chatbot should be available
    allowed_pages = ["Dashboard"]

    # chatbot button only if on an allowed page
    if st.session_state.page in allowed_pages:
        if "show_chatbot" not in st.session_state:
            st.session_state.show_chatbot = False

        if st.sidebar.button("🤖 Open Chatbot", use_container_width=True):
            st.session_state.show_chatbot = not st.session_state.show_chatbot

        if st.session_state.show_chatbot:
            chatbot_ui()  # Load chatbot UI only when button is clicked

# Call chatbot button in the main sidebar
chatbot_button()

