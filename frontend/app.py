import os
import requests
import streamlit as st


BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="AI Data Agent", layout="wide")
st.title("AI-Powered Data Analytics Assistant")


with st.sidebar:
    st.header("Backend")
    st.text_input("Backend URL", value=BACKEND_URL, key="backend_url")


st.subheader("1. Upload Dataset")
uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
uploaded_path = st.session_state.get("uploaded_path")

if uploaded and st.button("Upload"):
    name = uploaded.name
    data = uploaded.getvalue()
    if name.lower().endswith(".csv"):
        ctype = "text/csv"
    elif name.lower().endswith(".xlsx"):
        ctype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        ctype = "application/octet-stream"
    files = {"file": (name, data, ctype)}
    api_base = f"{st.session_state.backend_url}/v1"
    r = requests.post(f"{api_base}/upload", files=files)
    if r.ok:
        data = r.json()
        uploaded_path = data["stored_path"]
        st.session_state["uploaded_path"] = uploaded_path
        st.success(f"Uploaded: {data['filename']}\nStored at: {uploaded_path}")
    else:
        st.error(r.text)

if uploaded_path:
    st.subheader("2. Profile")
    if st.button("Generate Profile"):
        api_base = f"{st.session_state.backend_url}/v1"
        r = requests.post(f"{api_base}/profile", json={"path": uploaded_path})
        if r.ok:
            st.json(r.json()["summary"])
        else:
            st.error(r.text)

    st.subheader("3. Clean")
    if st.button("Run Cleaning"):
        api_base = f"{st.session_state.backend_url}/v1"
        r = requests.post(f"{api_base}/clean", json={"path": uploaded_path})
        if r.ok:
            data = r.json()
            st.session_state["cleaned_path"] = data["cleaned_path"]
            st.json(data["report"])
        else:
            st.error(r.text)

    st.subheader("4. Auto Insights")
    if st.button("Generate Insights"):
        api_base = f"{st.session_state.backend_url}/v1"
        r = requests.post(f"{api_base}/insights/auto", json={"path": uploaded_path})
        if r.ok:
            st.json(r.json())
        else:
            st.error(r.text)

    st.subheader("5. NLQ (Ask a question)")
    q = st.text_input("Question", value="Show a sample of the data")
    if st.button("Run NLQ"):
        api_base = f"{st.session_state.backend_url}/v1"
        r = requests.post(
            f"{api_base}/nlq/run",
            json={"path": uploaded_path, "question": q},
        )
        if r.ok:
            data = r.json()
            st.code(data["code"], language="python")
            if data.get("result_summary"):
                st.info(data["result_summary"])
        else:
            st.error(r.text)

    st.subheader("6. Export Report")
    format_choice = st.selectbox("Format", ["pdf", "xlsx"])
    if st.button("Export"):
        api_base = f"{st.session_state.backend_url}/v1"
        r = requests.post(
            f"{api_base}/report/export",
            json={"path": uploaded_path, "sections": [], "include_charts": True, "format": format_choice},
        )
        if r.ok:
            out = r.json()["output_path"]
            st.success(f"Report generated: {out}")
        else:
            st.error(r.text)


