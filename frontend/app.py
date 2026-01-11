import os
import requests
import streamlit as st
import pandas as pd

# if "dataset_id" in st.session_state:
#     if st.session_state["dataset_id"].startswith("dataset_"):
#         st.error("FATAL: dataset_id is a table_name, not a UUID")
#         st.stop()
        
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None

dataset_id = st.session_state.dataset_id



# -------------------------------------0
# BASIC CONFIG
# -------------------------------------
# https://hdjh9khd-8000.inc1.devtunnels.ms/
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/v1/api")

st.set_page_config(page_title="AI Data Agent", layout="wide")
st.title("AI-Powered Data Analytics Assistant")

# Sidebar
with st.sidebar:
    st.header("Backend Settings")
    st.text_input("Backend URL", BACKEND_URL, key="backend_url")
    API = lambda: st.session_state.backend_url


# -------------------------------------
# 1️. UPLOAD DATASET
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
# 2️. PROFILE DATASET
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
# 3️. CLEANING
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
# 4️. INSIGHTS
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
# 5️. NLQ
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
# 6️. FETCH DATASET COLUMNS
# -------------------------------------


st.subheader("6️. Dataset Columns")


r = requests.get(
    f"{API()}/columns",
    params={"dataset_id": dataset_id}
)

if not r.ok:
    st.error(f"Failed to fetch columns: {r.text}")
    st.stop()

columns = r.json()["columns"]

cols_df = pd.DataFrame(columns)
st.dataframe(cols_df, use_container_width=True)


# -------------------------------------
# 7️. CHART CONFIGURATION
# -------------------------------------
st.subheader("7️. Create Your Own Chart")

numeric_cols = [c["name"] for c in columns if c["type"] == "numeric"]
all_cols = [c["name"] for c in columns]

if not numeric_cols:
    st.warning("No numeric columns available for charting.")
    st.stop()

x_col = st.selectbox("X Axis", all_cols)
y_col = st.selectbox("Y Axis (Numeric)", all_cols)

chart_type = st.selectbox(
    "Chart Type",
    ["line", "bar", "scatter"]
)


# -------------------------------------
# 8️. GENERATE CHART
# -------------------------------------
if st.button("8. Generate Chart"):
    payload = {
        "dataset_id": dataset_id,
        "x": x_col,
        "y": y_col,
        "chart_type": chart_type
    }

    r = requests.post(
        f"{API()}/charts/plot",
        json=payload
    )

    if not r.ok:
        st.error(f"Chart generation failed: {r.text}")
        st.stop()

    chart_data = r.json()
    df_plot = pd.DataFrame({
        x_col: chart_data["x"],
        y_col: chart_data["y"]
    })

    st.markdown("### 📈 Chart Output")

    if chart_type == "line":
        st.line_chart(df_plot.set_index(x_col))
    elif chart_type == "bar":
        st.bar_chart(df_plot.set_index(x_col))
    elif chart_type == "scatter":
        st.scatter_chart(df_plot, x=x_col, y=y_col)




# -------------------------------------
# 9. EXPORT REPORT (COMING SOON)
# -------------------------------------
st.subheader("9. Export Report (Coming Soon)")
st.info("Report API will be added after report pipeline is complete.")