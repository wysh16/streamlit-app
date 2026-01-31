import streamlit as st
import pandas as pd
from pymongo import MongoClient
import certifi

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

    if "_Id" in df.columns:
        df = df.drop(columns=["_Id"])

    return df


st.set_page_config(page_title="Customer Analytics App", layout="wide")
st.title("📊 Customer Data Analytics Application")

# ===============================
# Load data
# ===============================
df_pd = load_data()

# 👉 Chuyển sang Vaex (CỐT LÕI CÂU 2)
df_vaex = vaex.from_pandas(df_pd, copy_index=False)

st.caption("⚙️ Data processed using **Vaex** for scalable analytics")


# ===============================
# Dataset Overview (Vaex)
# ===============================
st.subheader("🔍 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df_vaex))
col2.metric("Countries", df_vaex["Country"].nunique())
col3.metric("Customer Segments", df_vaex["Customer_Segment"].nunique())


# ===============================
# Gender Distribution (Vaex → Pandas)
# ===============================
st.subheader("👥 Gender Distribution")

gender_dist = (
    df_vaex.groupby("Gender", agg={"count": vaex.agg.count()})
    .to_pandas_df()
    .set_index("Gender")
)

st.bar_chart(gender_dist)


# ===============================
# Age Analysis (Vaex)
# ===============================
st.subheader("🎂 Age Analysis")

age_stats = df_vaex["Age"].describe()
st.write(age_stats)


# ===============================
# Income Distribution (Categorical – Vaex)
# ===============================
st.subheader("💰 Income Level Distribution")

income_dist = (
    df_vaex.groupby("Income", agg={"count": vaex.agg.count()})
    .to_pandas_df()
    .set_index("Income")
)

st.bar_chart(income_dist)


# ===============================
# Purchase Behavior (Vaex)
# ===============================
st.subheader("🛒 Purchase Behavior by Customer Segment")

segment_purchase = (
    df_vaex.groupby(
        "Customer_Segment",
        agg={"Avg_Purchases": vaex.agg.mean("Total_Purchases")}
    )
    .to_pandas_df()
)

st.dataframe(segment_purchase)


# ===============================
# Interactive Filter
# ===============================
st.subheader("🎯 Explore Customers by Country")

countries = sorted(df_vaex["Country"].unique())
selected_country = st.selectbox("Select Country", countries)

filtered_vaex = df_vaex[df_vaex["Country"] == selected_country]
st.dataframe(filtered_vaex.head(10).to_pandas_df())
