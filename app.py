import streamlit as st
import pandas as pd
from pymongo import MongoClient
import certifi

# ===============================
# Load data from MongoDB
# ===============================
@st.cache_data
def load_data():
    MONGO_URI = "mongodb+srv://huongntt22406_db_user:T5colen10diemmmm@cluster0.togqgmv.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where()
    )

    db = client["bigdata_midterm"]
    collection = db["retail_new_data"]

    df = pd.DataFrame(list(collection.find()))

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.title()

    # Xóa _id của MongoDB nếu có
    if "_Id" in df.columns:
        df = df.drop(columns=["_Id"])

    return df


# ===============================
# App Config
# ===============================
st.set_page_config(
    page_title="Customer Analytics App",
    layout="wide"
)

st.title("📊 Customer Data Analytics Application")
st.caption("⚙️ Data processed using **Pandas** (Streamlit Cloud compatible)")

# ===============================
# Load dataset
# ===============================
df = load_data()

# ===============================
# Dataset Overview
# ===============================
st.subheader("🔍 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Countries", df["Country"].nunique())
col3.metric("Customer Segments", df["Customer_Segment"].nunique())

# ===============================
# Gender Distribution
# ===============================
st.subheader("👥 Gender Distribution")

gender_dist = (
    df["Gender"]
    .value_counts()
    .to_frame(name="Count")
)

st.bar_chart(gender_dist)

# ===============================
# Age Analysis
# ===============================
st.subheader("🎂 Age Analysis")

age_stats = df["Age"].describe()
st.dataframe(age_stats)

# ===============================
# Income Level Distribution
# ===============================
st.subheader("💰 Income Level Distribution")

income_dist = (
    df["Income"]
    .value_counts()
    .to_frame(name="Count")
)

st.bar_chart(income_dist)

# ===============================
# Purchase Behavior by Segment
# ===============================
st.subheader("🛒 Purchase Behavior by Customer Segment")

segment_purchase = (
    df.groupby("Customer_Segment", as_index=False)
      .agg(Avg_Purchases=("Total_Purchases", "mean"))
)

st.dataframe(segment_purchase)

# ===============================
# Interactive Filter
# ===============================
st.subheader("🎯 Explore Customers by Country")

countries = sorted(df["Country"].dropna().unique())
selected_country = st.selectbox("Select Country", countries)

filtered_df = df[df["Country"] == selected_country]
st.dataframe(filtered_df.head(10))
