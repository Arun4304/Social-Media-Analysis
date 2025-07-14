import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Platform Usage Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

st.title("📱 Digital Habits & Behavioral Insights Dashboard")
st.markdown("Analyze social media/video platform usage behavior with real user data.")

# Sidebar Filters
platforms = df["Platform"].unique().tolist()
selected_platform = st.sidebar.multiselect("Select Platform(s)", platforms, default=platforms)

age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (18, 50))

# Filtered Data
filtered_df = df[
    (df["Platform"].isin(selected_platform)) &
    (df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])
]

st.subheader("⏳ Time Spent vs. Video Length")

fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x="Video_Length", y="Time_Spent_On_Video", hue="Platform", ax=ax)
st.pyplot(fig)

st.subheader("💥 Addiction Level by Age Group")

fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x="Platform", y="Addiction_Level", ax=ax)
st.pyplot(fig)

st.subheader("📉 Productivity Loss by Watch Reason")

fig, ax = plt.subplots()
sns.barplot(data=filtered_df, x="Watch_Reason", y="Productivity_Loss", estimator="mean", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
