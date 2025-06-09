
import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(
    page_title="Chatbot Evaluation Survey",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal header
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <h3>Chatbot Evaluation Survey</h3>
    <p><em>MSc AI Online – University of Hull</em></p>
</div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("### Instructions")
st.markdown("""
Please try all three chatbots with the test questions and rate them on the four criteria below (0-10 scale):

**Chatbot Links:**
- Centralized RAG: [Try Here](https://centralizedragfederatedragretrievalextraction-muzd7d9dyusdfdx8.streamlit.app/)
- Federated RAG: [Try Here](https://centralizedragfederatedragretrievalextraction-5wpagru28pbenjvj.streamlit.app/)
- Retrieval-Based: [Try Here](https://centralizedragfederatedragretrievalextraction-cbu8gfp3nwzjwfdt.streamlit.app/)
""")
criteria = [
    {"name": "Relevance", "key": "relevance"},
    {"name": "Coherence", "key": "coherence"},
    {"name": "Ambiguity Handling", "key": "ambiguity"},
    {"name": "User Satisfaction", "key": "satisfaction"}
]
chatbots = [
    {"name": "Centralized RAG", "key": "centralized"},
    {"name": "Federated RAG", "key": "federated"},
    {"name": "Retrieval-Based", "key": "retrieval"}
]

if 'survey_data' not in st.session_state:
    st.session_state.survey_data = {}

for criterion in criteria:
    st.markdown(f"#### {criterion['name']}")
    col1, col2, col3 = st.columns(3)
    for i, col in enumerate([col1, col2, col3]):
        with col:
            chatbot = chatbots[i]
            score_key = f"{criterion['key']}_{chatbot['key']}"
            score = st.slider(f"{chatbot['name']}", 0, 10, st.session_state.survey_data.get(score_key, 5), key=score_key)
            st.session_state.survey_data[score_key] = score

st.markdown("### Feedback")
feedback = st.text_area("Additional feedback:", height=100, key="open_feedback")
st.session_state.survey_data['open_feedback'] = feedback

st.markdown("### Participant Info (Optional)")
col1, col2 = st.columns(2)
with col1:
    participant_id = st.text_input("Participant ID:", key="participant_id")
    st.session_state.survey_data['participant_id'] = participant_id
with col2:
    background = st.selectbox("Educational Background:", ["", "CS", "Eng", "Math", "Biz", "Other"], key="background")
    st.session_state.survey_data['background'] = background

def save_survey_data(data):
    data['timestamp'] = datetime.datetime.now().isoformat()
    df = pd.DataFrame([data])
    csv_file = "survey_responses.csv"
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(csv_file, index=False)
    return len(df)

if st.button("Submit Survey"):
    required_scores = [f"{c['key']}_{b['key']}" for c in criteria for b in chatbots]
    if all(k in st.session_state.survey_data for k in required_scores):
        count = save_survey_data(st.session_state.survey_data)
        st.success(f"Submitted! Response #{count}")
    else:
        st.error("Please complete all ratings before submitting.")
