# Import necessary libraries
import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
import time
from chatbot import chatbot_button

# Load Dataset
@st.cache_data
def load_data():
    file_path = r"C:\Users\RISHIRAJ\OneDrive\Desktop\final_cleaned_city_day.csv"  
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Month"] = df["Date"].dt.month

    return df

# Load the data
df = load_data()

# Initialize session state for authentication and theme
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.users = {"admin": "password123"}  # Default user
    st.session_state.theme = "light"

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

# Apply theme styles
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        body { background-color: #1E1E1E; color: white; }
        .stButton>button { background-color: #444; color: white; border-radius: 8px; font-weight: bold; }
        .stTextInput>div>div>input { background-color: #444; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function for user authentication
def authenticate(username, password):
    return st.session_state.users.get(username) == password

# Function to handle login/logout
def login():
    st.subheader("🔐 Login to Access the Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Login successful! Access granted.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("🚫 Incorrect username or password!")

# Function to handle new user registration
def register():
    st.subheader("🆕 Register New Account")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    
    if st.button("Register"):
        if new_username in st.session_state.users:
            st.error("⚠️ Username already exists! Choose a different one.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("✅ Registration successful! Please log in.")
            time.sleep(1)
            st.rerun()

# Login or Register page with theme toggle
if not st.session_state.authenticated:
    st.sidebar.title("🔑 User Access")
    choice = st.sidebar.radio("Select an option:", ["Login", "Register"])
    st.sidebar.button("🌙 Toggle Theme", on_click=toggle_theme)
    
    if choice == "Login":
        login()
    else:
        register()
    st.stop()

# Navigation Sidebar with icons
st.sidebar.title("🌍 Navigation")
st.sidebar.button("🏠 Home", on_click=lambda: st.session_state.update(page="Home"), use_container_width=True)
st.sidebar.button("📊 Dashboard", on_click=lambda: st.session_state.update(page="Dashboard"), use_container_width=True)
st.sidebar.button("💬 Feedback", on_click=lambda: st.session_state.update(page="Feedback"), use_container_width=True)
chatbot_button()

# Logout Button
st.sidebar.button("🔓 Logout", on_click=lambda: (st.session_state.update(authenticated=False), st.rerun()))

# Determine current page
page = st.session_state.get("page", "Home")

# Home Page
if page == "Home":
    st.title("🌍 Welcome to Air Quality Hub")
    st.write("""
             
Transform data into action! This platform isn't just a dashboard—it's a gateway to understanding and addressing air pollution challenges worldwide. Stay informed, explore trends, and contribute to a cleaner future.  

### 🚀 Discover What’s Inside  
- **🌐 Real-World Impact:** See how air quality affects daily life, health, and climate.  
- **📊 Data-Powered Insights:** Unlock meaningful trends through interactive charts and visualizations.  
- **🔍 Deep Dives into Pollutants:** Learn about **PM2.5, NO2, O3, and more**—what they are and why they matter.  
- **🌎 Local & Global Perspectives:** Compare air quality between cities and regions to uncover pollution patterns.  
- **📢 Empower Change:** Use data-backed evidence to advocate for better environmental policies and healthier communities.  

### 🎯 How to Get Started  
1. **Navigate with Ease** – Use the sidebar to explore different insights.  
2. **Interact & Analyze** – Click on charts, apply filters, and uncover key takeaways.  
3. **Turn Insights into Action** – Share findings, raise awareness, and inspire change.  

🔔 Let’s make every breath count—explore, learn, and be part of the solution! 🌱✨
    """)

# Dashboard Section
elif page == "Dashboard":
    st.title("📊 Air Quality Dashboard")
    tab1, tab2 = st.tabs(["📊 Dashboard View", "📂 Dataset Explorer"])

    # ------------ TAB 1: DASHBOARD VIEW ------------
    with tab1: 
        st.write(
        """
        ## 📌 About This Dashboard  
        Air pollution is a growing concern that impacts millions worldwide. Understanding historical air quality trends is essential for making informed decisions about public health and environmental policies. This interactive dashboard provides a comprehensive analysis of air quality from **2015 to 2020** across multiple cities.  
        """
        )

        # Power BI Dashboard Embed
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=54d8a369-c0df-4169-9974-99eb03333fb3&autoAuth=true&ctid=c7835ab2-81ec-41a0-a97d-7d3cec3e4aa7"
        st.markdown(
            f'<iframe width="1000" height="600" src="{power_bi_url}" frameborder="0" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )

        st.success("✅ Dashboard loaded successfully!")

        st.write(
        """
        ### 🌟 Key Features  
        - **📈 Track Air Quality Changes:** View historical trends in **Air Quality Index (AQI)** and key pollutants such as **PM2.5, PM10, NO2, SO2, CO, and O3**.  
        - **🏙 Compare City-wise AQI Levels:** Analyze and compare the air quality of different cities to understand regional pollution variations.  
        - **📊 Interactive Visualizations:** Use dynamic charts and heatmaps to explore air quality fluctuations over time.  
        - **🔍 Identify Pollution Trends & Patterns:** Gain insights into seasonal changes, extreme pollution events, and long-term environmental impacts.  
        - **📌 Custom Filters & Search:** Select specific years, cities, or pollutants to tailor your analysis.  
        - **📥 Download Reports:** Export visualizations and data for offline analysis or presentations.  

        ### 🔄 How to Use This Dashboard  
        1. **Navigate the Sidebar:** Use the left panel to switch between different sections.  
        2. **Explore the Insights:** View AQI trends, city comparisons, and pollutant breakdowns.  
        3. **Customize Filters:** Adjust parameters like year, city, and pollutant type for personalized analysis.  
        4. **Interpret the Results:** Each chart includes explanations to help you understand key findings.  

        ### 🌱 Why Air Quality Matters  
        Poor air quality has significant health effects, including respiratory diseases, cardiovascular problems, and reduced life expectancy. This dashboard empowers users—researchers, policymakers, and citizens—to monitor pollution trends and take informed actions for a cleaner environment.  
        """
        )

    # ------------ TAB 2: DATASET EXPLORER ------------
    with tab2: 
        st.subheader("📂 Explore Air Quality Data")

        # Raw Data Preview
        st.write("### 📋 Raw Dataset Preview")
        st.dataframe(df)

        # Filtering Options
        st.write("### 🔍 Filter Data")
        city_list = df["City"].unique().tolist()
        selected_city = st.selectbox("Select a City", ["All"] + city_list)

        if selected_city != "All":
            df_filtered = df[df["City"] == selected_city]
        else:
            df_filtered = df

        st.dataframe(df_filtered)

        # Statistical Summary
        st.write("### 📊 Summary Statistics")
        st.write(df_filtered.describe())

        # AQI Trends Over Time
        st.write("### 📈 AQI Trends Over Time")
        fig = px.line(df_filtered, x="Date", y="AQI", color="City", title="AQI Trends Over Time")
        st.plotly_chart(fig)

        # Most & Least Polluted Cities
        st.write("### 🌆 Most & Least Polluted Cities")
        avg_aqi = df.groupby("City")["AQI"].mean().reset_index()
        most_polluted = avg_aqi.nlargest(5, "AQI")
        least_polluted = avg_aqi.nsmallest(5, "AQI")

        st.write("#### 🚨 Most Polluted Cities")
        st.dataframe(most_polluted)
        st.write("#### 🌿 Least Polluted Cities")
        st.dataframe(least_polluted)

        # City-wise AQI Comparison
        st.write("### 🏙 City-wise AQI Comparison")
        fig = px.bar(avg_aqi, x="City", y="AQI", title="Average AQI by City", color="AQI", height=600)
        st.plotly_chart(fig)

        # Pollutant Distribution
        st.write("### 🌫️ Pollutant Distribution")
        pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
        selected_pollutant = st.selectbox("Select a Pollutant", pollutants)
        fig = px.box(df_filtered, x="City", y=selected_pollutant, title=f"{selected_pollutant} Levels Across Cities")
        st.plotly_chart(fig)

        # Correlation Heatmap
        st.write("### 🔬 Correlation Between Pollutants")
        numeric_df = df_filtered.select_dtypes(include=["float64", "int64"])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)

        # Seasonal AQI Patterns
        st.write("### 📅 Seasonal AQI Patterns")
        df_filtered["Month"] = df_filtered["Date"].dt.month
        monthly_aqi = df_filtered.groupby("Month")["AQI"].mean().reset_index()
        fig = px.line(monthly_aqi, x="Month", y="AQI", title="Average AQI by Month", markers=True)
        st.plotly_chart(fig)

        # Download Data Feature
        st.write("### 📥 Download Filtered Data")
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        data_csv = convert_df(df_filtered)
        st.download_button(
            label="Download CSV",
            data=data_csv,
            file_name="filtered_air_quality_data.csv",
            mime="text/csv"
        )

    # Sidebar Information
    with st.sidebar.expander("ℹ️ More Information"):
        st.markdown("## 📌 About This Project")
        st.write(
            "This project provides an interactive visualization of air quality data "
            "for cities in India, helping users explore AQI trends, pollution sources, and patterns."
        )

        st.divider()

        st.markdown("## 🌍 Air Quality in India")
        st.write(
            "Air quality in India is a major concern due to its **severe health impacts, economic losses,** "
            "and **environmental damage**. High pollution levels are often linked to industrial activities, "
            "vehicular emissions, and crop burning."
        )

        st.info(
            "**🚀 Key Insights:**\n"
            "- 🌫️ India has some of the most polluted cities in the world.\n"
            "- 💨 PM2.5 & PM10 levels often exceed WHO safety limits.\n"
            "- 🌱 Government policies and sustainable initiatives are being implemented to combat pollution."
        )

# Feedback form
elif page == "Feedback":
    
    # Load secrets from secrets.toml
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]
    smtp_user = st.secrets["email"]["smtp_user"]
    smtp_password = st.secrets["email"]["smtp_password"]
    sender_email = st.secrets["email"]["sender_email"]
    receiver_emails = st.secrets["email"]["receiver_emails"]

    st.title("💬 We Value Your Feedback")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Feedback")

    if st.button("Submit"):
        if name and email and message:
            try:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = ", ".join(receiver_emails)
                msg["Subject"] = f"Feedback from {name}"
                body = f"Name: {name}\nEmail: {email}\n\nFeedback:\n{message}"
                msg.attach(MIMEText(body, "plain"))

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(sender_email, receiver_emails, msg.as_string())

                st.success("✅ Thank you for your feedback! We've received your message.")
            except Exception as e:
                st.error(f"❌ Failed to send feedback. Error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")








