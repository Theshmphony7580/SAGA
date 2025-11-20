import os
import requests
import streamlit as st
import pandas as pd

# -------------------------------------
# BASIC CONFIG
# -------------------------------------
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/v1")

st.set_page_config(page_title="AI Data Agent", layout="wide")
st.title("AI-Powered Data Analytics Assistant")

# Sidebar
with st.sidebar:
    st.header("Backend Settings")
    st.text_input("Backend URL", BACKEND_URL, key="backend_url")
    API = lambda: st.session_state.backend_url


# -------------------------------------
# 1️⃣ UPLOAD DATASET
# -------------------------------------
st.subheader("1. Upload Dataset")

uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
dataset_id = st.session_state.get("dataset_id")

if uploaded and st.button("Upload"):
    files = {
        "file": (uploaded.name, uploaded.getvalue(), uploaded.type)
    }

    r = requests.post(f"{API()}/upload", files=files)

    if r.ok:
        data = r.json()
        # backend returns stored_path = backend/storage/datasets/<dataset_id>.csv
        st.write("DEBUG upload response:", data)
        stored = data["file_path"]
        dataset_id = os.path.splitext(os.path.basename(stored))[0]
        st.session_state["dataset_id"] = dataset_id

        st.success(f"Uploaded successfully!")
        st.info(f"Dataset ID: {dataset_id}")
    else:
        st.error(r.text)


# Stop if no dataset
if not st.session_state.get("dataset_id"):
    st.stop()


dataset_id = st.session_state.dataset_id
st.write(f"**Current Dataset ID:** `{dataset_id}`")


# -------------------------------------
# 2️⃣ PROFILE
# -------------------------------------
st.subheader("2. Profile Dataset")

if st.button("Generate Profile"):
    r = requests.get(f"{API()}/profile/{dataset_id}")

    if r.ok:
        st.json(r.json())
    else:
        st.error(r.text)


# -------------------------------------
# 3️⃣ CLEANING
# -------------------------------------
st.subheader("3. Clean Dataset")

if st.button("Run Cleaning"):
    r = requests.post(f"{API()}/clean/{dataset_id}")

    if r.ok:
        st.success("Cleaning Completed!")
        st.json(r.json())
    else:
        st.error(r.text)


# -------------------------------------
# 4️⃣ INSIGHTS
# -------------------------------------
st.subheader("4. Auto Insights")

if st.button("Generate Insights"):
    r = requests.get(f"{API()}/insights/{dataset_id}")

    if r.ok:
        resp = r.json()
        st.json(resp)

        # Optional correlation heatmap
        if resp.get("correlations"):
            corr_df = pd.DataFrame(resp["correlations"])
            st.write("### Correlation Heatmap")
            st.dataframe(corr_df)
    else:
        st.error(r.text)


# -------------------------------------
# 5️⃣ NLQ
# -------------------------------------
st.subheader("5. NLQ (Ask Your Dataset)")

question = st.text_input("Ask a question about your data:")

if st.button("Run NLQ"):
    r = requests.post(
        f"{API()}/nlq/{dataset_id}",
        json={"question": question}
    )

    if r.ok:
        data = r.json()
        st.code(data["code"], language="python")

        if data.get("result_summary"):
            st.info(data["result_summary"])

        if data.get("result_table"):
            df = pd.DataFrame(data["result_table"])
            st.dataframe(df)
    else:
        st.error(r.text)


# -------------------------------------
# 6️⃣ REPORT (COMING SOON)
# -------------------------------------
st.subheader("6. Export Report (Coming Soon)")
st.info("Report API will be added after report pipeline is complete.")
