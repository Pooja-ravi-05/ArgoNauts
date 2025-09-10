import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import re
from datetime import datetime

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="FloatChat - ARGO Data Explorer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CSS Styling --------------------
st.markdown("""
<style>
.main-header { font-size: 3rem; color: #1f77b4; text-align: center; margin-bottom: 1rem; }
.sub-header { font-size: 1.5rem; color: #2ca02c; margin-bottom: 1rem; }
.chat-message { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #ddd; }
.user-message { background-color: #e6f7ff; border-left: 4px solid #1890ff; }
.assistant-message { background-color: #f6ffed; border-left: 4px solid #52c41a; }
.stButton button { width: 100%; background-color: #1890ff; color: white; }
</style>
""", unsafe_allow_html=True)

# -------------------- Session State --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# -------------------- Database Connection --------------------
# Replace with your credentials
engine = create_engine("postgresql://postgres:mypassword@localhost:5432/floatchat")

# -------------------- Helper Functions --------------------
def fetch_argo_data(float_ids=None, limit=1000):
    sql_query = "SELECT float_id_text AS float_id, latitude, longitude, temperature, salinity, pressure, measurement_time FROM argo_data WHERE 1=1"
    params = {}
    
    if float_ids:
        placeholders = ",".join([f":fid{i}" for i in range(len(float_ids))])
        sql_query += f" AND float_id_text IN ({placeholders})"
        params = {f"fid{i}": fid for i, fid in enumerate(float_ids)}
    
    sql_query += f" ORDER BY measurement_time ASC LIMIT {limit}"
    df = pd.read_sql(text(sql_query), con=engine, params=params)
    return df

def extract_float_ids(user_query):
    return re.findall(r"[0-9_]+", user_query)

def get_ai_response(user_query, ocean_basin="Indian Ocean"):
    float_ids = extract_float_ids(user_query)
    df = fetch_argo_data(float_ids=float_ids)
    
    response_text = ""
    plot = None
    
    if df.empty:
        response_text = "No data found for the given float ID(s)."
    else:
        # Determine which parameters to plot
        params = []
        user_lower = user_query.lower()
        if any(word in user_lower for word in ["temperature", "temp"]):
            params.append("temperature")
        if any(word in user_lower for word in ["salinity", "salt"]):
            params.append("salinity")
        if any(word in user_lower for word in ["pressure", "press"]):
            params.append("pressure")
        if not params:
            params = ["temperature", "salinity", "pressure"]  # default all

        # Create multi-line plot
        fig = go.Figure()
        for param in params:
            for fid in df['float_id'].unique():
                float_data = df[df['float_id'] == fid]
                fig.add_trace(go.Scatter(
                    x=float_data['measurement_time'],
                    y=float_data[param],
                    mode='lines+markers',
                    name=f"{fid} - {param}"
                ))
        fig.update_layout(title=f"ARGO Data Trends ({', '.join(params)})",
                          xaxis_title="Time", yaxis_title="Value",
                          height=500)
        plot = fig
        response_text = f"Showing {', '.join(params)} trends for float(s): {', '.join(float_ids)}."

    return {"text": response_text, "plot": plot, "data": df}

# -------------------- Main App --------------------
def main():
    # Header
    st.markdown('<h1 class="main-header">🌊 FloatChat</h1>', unsafe_allow_html=True)
    st.markdown('### AI-Powered Conversational Interface for ARGO Ocean Data Discovery')
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/ocean.png", width=80)
        st.markdown("---")
        st.header("🌐 Data Controls")
        ocean_basin = st.selectbox(
            "Select Ocean Basin",
            ("Indian Ocean", "Global", "Pacific Ocean", "Atlantic Ocean", "Southern Ocean"),
            index=0
        )
        st.markdown("---")
        st.header("💡 Example Queries")
        examples = [
            "Show me temperature for float 1_339",
            "Compare salinity at 100m depth",
            "Plot trajectory of float 1_340"
        ]
        for example in examples:
            if st.button(example, key=example):
                st.session_state.user_input = example
                st.rerun()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Interface", "📊 Data Explorer", "🗺️ Float Map"])
    
    # --- Chat Interface ---
    with tab1:
        st.markdown('<h3 class="sub-header">Chat with ARGO Data</h3>', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><b>FloatChat:</b> {message["content"]}</div>', unsafe_allow_html=True)
                if "plot" in message and message["plot"] is not None:
                    st.plotly_chart(message["plot"], use_container_width=True)
                if "data" in message and message["data"] is not None:
                    with st.expander("View Data Table"):
                        st.dataframe(message["data"].head(10))
        
        user_input = st.chat_input("Ask about ocean data...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Analyzing ocean data..."):
                response = get_ai_response(user_input, ocean_basin)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["text"],
                "plot": response["plot"],
                "data": response["data"]
            })
            st.rerun()
    
    # --- Data Explorer ---
    with tab2:
        st.markdown('<h3 class="sub-header">Direct Data Exploration</h3>', unsafe_allow_html=True)
        float_ids_input = st.text_input("Enter float IDs (comma-separated)", value="1_339,1_340")
        if st.button("Load Data"):
            float_ids = [fid.strip() for fid in float_ids_input.split(",")]
            df = fetch_argo_data(float_ids=float_ids, limit=1000)
            if not df.empty:
                st.dataframe(df)
                fig = px.line(df, x='measurement_time', y=['temperature','salinity','pressure'], color='float_id')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data found for these float IDs.")
    
    # --- Float Map ---
    with tab3:
        st.markdown('<h3 class="sub-header">ARGO Float Locations</h3>', unsafe_allow_html=True)
        df_map = fetch_argo_data(limit=500).drop_duplicates('float_id')
        if not df_map.empty:
            fig_map = px.scatter_map(
                df_map,
                lat="latitude",
                lon="longitude",
                hover_name="float_id",
                hover_data=["temperature","salinity","pressure"],
                color="float_id",
                zoom=3,
                height=600
            )
            fig_map.update_layout(map_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
            st.info(f"Showing {len(df_map)} active ARGO floats in the {ocean_basin} region.")

# Run the app
if __name__ == "__main__":
    main()
