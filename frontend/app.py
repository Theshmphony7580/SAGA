import os
import requests
import streamlit as st
import pandas as pd

if "dataset_id" in st.session_state:
    if st.session_state["dataset_id"].startswith("dataset_"):
        st.error("FATAL: dataset_id is a table_name, not a UUID")
        st.stop()


# -------------------------------------
# BASIC CONFIG
# -------------------------------------
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/v1/api")

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
        dataset_id = data.get("dataset_id")
        
        if dataset_id:
            st.session_state["dataset_id"] = dataset_id
            st.success("File uploaded and processed successfully.")
            st.info(f"Dataset ID: {dataset_id}")
            st.info(f"File Name: {uploaded.name}")
        else:
            st.error("Upload succeeded but no dataset ID was returned.")
    else:
        st.error(f"Upload failed: {r.text}")



# Stop if no dataset
if not st.session_state.get("dataset_id"):
    st.stop()


dataset_id = st.session_state.dataset_id
st.write(f"**Current Dataset ID:** `{dataset_id}`")

# -------------------------------------
# 2️⃣ PROFILE DATASET
# -------------------------------------
st.subheader("2. Profile Dataset")

if st.button("Generate Profile"):
    r = requests.get(
        f"{API()}/profile",
        params={"dataset_id": dataset_id}
    )

    if r.ok:
        st.session_state["profile_response"] = r.json()
        st.success("Profile generated successfully")
    else:
        st.error(r.text)

# -------------------------------------
# RENDER PROFILE (CORRECT LEVEL)
# -------------------------------------
if "profile_response" in st.session_state:
    response = st.session_state["profile_response"]

    if "profile" not in response:
        st.error("Invalid profile response structure")
        st.json(response)
        st.stop()

    profile = response["profile"]

    # -------------------------------
    # TABLE INFO
    # -------------------------------
    if "table" in profile:
        st.markdown("### 📌 Dataset Overview")
        table_df = pd.DataFrame(
            [(k, str(v)) for k, v in profile["table"].items()],
            columns=["Metric", "Value"]
        )
        st.table(table_df)

    # -------------------------------
    # VARIABLES
    # -------------------------------
    summary_df = pd.DataFrame(
    profile["summary"].items(),
    columns=["Metric", "Value"]
    )
    st.table(summary_df)
    
    
    st.markdown("### 🔢 Numeric Columns")
    st.dataframe(pd.DataFrame(
    profile["numeric_columns"], columns=["Column"]
    ))



    # -------------------------------
    # MISSING
    # -------------------------------
    st.markdown("### ⚠ Missing Values")
    missing_df = pd.DataFrame(
    profile["missing_summary"].items(),
    columns=["Column", "Missing %"]
    )
    st.dataframe(missing_df)


    # -------------------------------
    # CORRELATIONS
    # -------------------------------
    if profile["strong_correlations"]:
        st.dataframe(pd.DataFrame(profile["strong_correlations"]))
    else:
        st.info("No strong correlations found")
# st.json(st.session_state.get("profile", {}))
        


# -------------------------------------
# 3️⃣ CLEANING
# -------------------------------------
st.subheader("3. Clean Dataset")

if st.button("Run Cleaning"):
    r = requests.post(f"{API()}/clean/{dataset_id}")

    if r.ok:
        st.success("Cleaning Completed!")
        cleaning_json = r.json()
        st.write("### Cleaning Report")
        cleaning_to_tabular_display = pd.DataFrame(cleaning_to_tabular_display := [
            {
                "Issue": issue,
                "Details": details
                
                # "Details": pd.json_normalize(details).to_dict(orient="records")[0]

            }
            for issue, details in cleaning_json["report"].items()
        ])
        st.dataframe(cleaning_to_tabular_display)
    else:
        st.error(r.text)


# -------------------------------------
# 4️⃣ INSIGHTS
# -------------------------------------
st.subheader("4. Auto Insights")

if st.button("Generate Insights"):
    r = requests.post(
        f"{API()}/insights/{dataset_id}",
    )

    if r.ok:
        # resp = r.json()
        # st.json(resp)
        insights_json = r.json()
        st.write("### Insights Report")
        insights_to_tabular_display = pd.DataFrame(insights_to_tabular_display := [
            {
                # str(value["mean"]) : str(value),
                "Inight values" : str(key),
                "Mean" : str(value["mean"]),
                "Median" : str(value["median"]),
                "Std Dev": str(value["std"]),
                "Min": str(value["min"]),
                "Max": str(value["max"]),
                "25%": str(value["25%"]),
                "75%": str(value["75%"]),
                # "Details": str(value)
            }
            for key, value in insights_json["numeric_summary"].items()
        ])
        st.dataframe(insights_to_tabular_display)

        # Optional correlation heatmap
        if insights_json.get("correlations"):
            corr_df = pd.DataFrame(insights_json["correlations"])
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
        f"{API()}/nlq/run",
        json={"dataset_id": dataset_id, "question": question}
    )

    if r.ok:
        data = r.json()
        # st.markdown("### Generated SQL")
        # st.code(data["sql"], language="sql")
        
        # if data.get("result_summary"):
        #     st.info(data["result_summary"])

        if data["rows"]:
            df = pd.DataFrame(data["rows"], columns=data["columns"])
            st.markdown(f"### Result ({data['row_count']} rows)")
            st.dataframe(df)
        else:
            st.info("Query executed successfully, but returned no rows.")
    else:
        st.error(r.text)


# -------------------------------------
# 6 INSIGHTS
# -------------------------------------
st.subheader("6. Recommended Charts")

if st.button("Recommend Charts"):
    r = requests.get(
        f"{API()}/charts",
        params={"dataset_id": dataset_id}
    )

    if r.ok:
        charts_json = r.json()
        st.write("### Recommended Charts")
        charts_to_tabular_display = pd.DataFrame(charts_to_tabular_display := [
            {
                "Chart Type": chart.get("chart_type", "N/A"),
                "Description": chart.get("description", "N/A")
            }
            for chart in charts_json["charts"]
        ])
        st.dataframe(charts_to_tabular_display)
    else:
        st.error(r.text)

# -------------------------------------
# 7 REPORT (COMING SOON)
# -------------------------------------
st.subheader("7. Export Report (Coming Soon)")
st.info("Report API will be added after report pipeline is complete.")