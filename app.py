import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 Page Config
st.set_page_config(page_title="Data Intelligence Dashboard", layout="wide")

# 🔥 Custom UI Styling
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(120deg, #1f1c2c, #928dab);
    color: white;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #141e30, #243b55);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    transition: 0.3s;
}

div[data-testid="metric-container"]:hover {
    transform: scale(1.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Titles */
h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# 🔹 Header
st.title("🚀 Data Intelligence Dashboard")
st.caption("Smart Insights • Clean Analytics • Modern UI")

# 🔹 Upload CSV
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 🔹 Sidebar Filters
    st.sidebar.header("🔍 Filters")

    for col in df.select_dtypes(include='object').columns:
        values = df[col].dropna().unique()
        if len(values) < 50:
            selected = st.sidebar.selectbox(col, ["All"] + list(values))
            if selected != "All":
                df = df[df[col] == selected]

    # 📌 Preview
    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # 📊 KPI Metrics
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Missing", int(df.isnull().sum().sum()))

    # 🧹 Cleaning
    df = df.drop_duplicates()
    df = df.fillna(method='ffill')

    # 🔍 Column Types
    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns

    # 📈 Numeric Analysis
    if len(numeric_cols) > 0:
        st.subheader("📈 Numeric Analysis")

        colA, colB = st.columns(2)

        selected_num = colA.selectbox("Select Numeric Column", numeric_cols)
        colA.write(df[selected_num].describe())

        fig, ax = plt.subplots()
        df[selected_num].plot(ax=ax)
        colB.pyplot(fig)

    # 📊 Categorical Analysis
    if len(categorical_cols) > 0:
        st.subheader("📊 Categorical Analysis")

        colA, colB = st.columns(2)

        selected_cat = colA.selectbox("Select Category Column", categorical_cols)

        counts = df[selected_cat].value_counts().head(10)

        colA.write(counts)
        colB.bar_chart(counts)

    # 🧠 CLEAN INSIGHTS SECTION
    st.subheader("🧠 Key Insights")

    col1, col2, col3 = st.columns(3)

    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        col1.metric(f"{col} Avg", f"{df[col].mean():.1f}")

    if len(numeric_cols) > 1:
        col = numeric_cols[1]
        col2.metric(f"{col} Max", f"{df[col].max()}")

    if len(categorical_cols) > 0:
        col = categorical_cols[0]
        top = df[col].value_counts().idxmax()
        col3.metric(f"{col} Top", f"{top}")

    st.info("💡 Insights are automatically generated from your dataset.")

    # 🚨 Anomaly Detection
    if len(numeric_cols) > 0:
        st.subheader("🚨 Anomaly Detection")

        anomaly_col = st.selectbox("Select column for anomaly detection", numeric_cols)

        threshold = df[anomaly_col].mean() + 2 * df[anomaly_col].std()
        anomalies = df[df[anomaly_col] > threshold]

        st.warning(f"Threshold: {threshold:.2f}")
        st.dataframe(anomalies, use_container_width=True)