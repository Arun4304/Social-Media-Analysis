import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Digital Platform Usage Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")

    # Clean column names: replace spaces with underscores for easier access
    df.columns = df.columns.str.replace(" ", "_").str.strip()

    return df

# Load and clean data
df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")
platforms = df["Platform"].unique().tolist()
selected_platform = st.sidebar.multiselect("Select Platform(s)", platforms, default=platforms)

age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (18, 50))

# Filtered Data
filtered_df = df[
    (df["Platform"].isin(selected_platform)) &
    (df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])
]

# Main Title
st.title("📱 Digital Habits & Behavioral Insights Dashboard")
st.markdown("Analyze social media/video platform usage behavior with real user data.")

# --- Q1: Time Spent vs. Video Length (Boxplot) ---
st.subheader("⏳ Time Spent vs. Video Length")

# Create video length bins
filtered_df["Video_Length_Bin"] = pd.cut(
    filtered_df["Video_Length"],
    bins=[0, 5, 10, 15, 20, 25, 30],
    labels=["0-5", "6-10", "11-15", "16-20", "21-25", "26-30"]
)

# Plot
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.boxplot(data=filtered_df, x="Video_Length_Bin", y="Time_Spent_On_Video", ax=ax1)
ax1.set_title("Time Spent by Binned Video Length")
ax1.set_xlabel("Video Length Bin (minutes)")
ax1.set_ylabel("Time Spent (minutes)")
st.pyplot(fig1)

# --- Q2: Addiction Level by Age Group ---
st.subheader("💥 Addiction Level by Age Group")

filtered_df["Age_Group"] = pd.cut(
    filtered_df["Age"],
    bins=[0, 18, 25, 35, 50, 100],
    labels=["<18", "18-25", "26-35", "36-50", "50+"]
)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=filtered_df, x="Age_Group", y="Addiction_Level", ax=ax2)
ax2.set_title("Addiction Level by Age Group")
ax2.set_ylabel("Addiction Level")
st.pyplot(fig2)

# --- Q3: Productivity Loss by Platform and Watch Reason ---
st.subheader("📉 Productivity Loss by Platform and Watch Reason")

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.boxplot(data=filtered_df, x="Platform", y="Productivity_Loss", hue="Watch_Reason", ax=ax3)
ax3.set_title("Productivity Loss by Platform and Watch Reason")
ax3.set_ylabel("Productivity Loss Score")
ax3.set_xlabel("Platform")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)
