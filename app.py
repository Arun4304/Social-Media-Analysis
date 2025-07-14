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

df["Video_Length_Bin"] = pd.cut(df["Video_Length"], bins=[0, 5, 10, 15, 20, 25, 30], labels=["0-5", "6-10", "11-15", "16-20", "21-25", "26-30"])
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="Video_Length_Bin", y="Time_Spent_On_Video")
plt.title("Time Spent by Binned Video Length")
plt.xlabel("Video Length Bin (minutes)")
plt.tight_layout()
plt.show()


st.subheader("💥 Addiction Level by Age Group")

df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 25, 35, 50, 100], labels=['<18', '18-25', '26-35', '36-50', '50+'])
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='Age_Group', y='Addiction_Level')
plt.title("Addiction Level by Age Group")
plt.show()


st.subheader("📉 Productivity loss by platform, watch reason, and current activity")

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Platform", y="Productivity_Loss", hue="Watch_Reason")
plt.title("Productivity Loss by Platform and Watch Reason")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
