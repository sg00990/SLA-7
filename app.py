import streamlit as st
import time
import datetime
import json

st.set_page_config(
    page_title="Tier 1 SLA Questionnaire",
    page_icon="💻",
    layout="wide"
)

conn = st.connection("snowflake")

st.markdown('<p style="font-family:sans-serif; color:#324a62; font-size: 28px; font-weight: bold">Tier 1 SLA Questionnaire</p>', unsafe_allow_html=True)
st.write("###")

st.markdown('<p style="font-family:sans-serif; color:#87c440; font-size: 20px; font-weight: bold">SLA 7</p>', unsafe_allow_html=True)


st.write("**Reason for Failed SLA**")
reason = st.text_area("reason", label_visibility="collapsed")
reason = reason.replace("\n", "  ").replace("'", "''").replace('"', r'\"')

st.write("**Total Possible Fields**")
total_fields = st.number_input("total_fields", step=1, min_value = 0, label_visibility="collapsed")

st.write("**Total Fields Passed**")
fields_passed = st.number_input("fields_passed", step=1, min_value = 0, label_visibility="collapsed")

st.write("**Percentage**")
perc = st.number_input("perc", label_visibility="collapsed")

st.write("**Date**")
survey_date = st.date_input("survey_date", format="MM/DD/YYYY", label_visibility="collapsed")
st.write("**Additional Comments**")
survey_text = st.text_area("survey_text", label_visibility="collapsed")
survey_text = survey_text.replace("\n", "  ").replace("'", "''").replace('"', r'\"')


col1, col2, col3 = st.columns(3)

with col3:
    if st.button("Submit", use_container_width=True):
        data = {
            "sla_7_reason_for_failure": reason,
            "sla_7_possible_fields": total_fields,
            "sla_7_fields_passed": fields_passed,
            "sla_7_percentage": perc,
            "sla_7_date": survey_date,
            "sla_7_comments": survey_text
        }

        json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

        date_submitted = datetime.datetime.now()

        try:
            conn.query(f""" INSERT INTO sla_tier_1_questionnaire (type, date_submitted, json_data) SELECT 'SLA 7', '{date_submitted}', (parse_json('{json_data}'))""")
        except:
            st.success("Thank you for your responses!")


col4, col5, col6 = st.columns([1, .5, 1])

with col4:
    st.write("##")
    st.image("img/blue_bar.png")
    
with col5:
    col17, col18, col19 = st.columns(3)
    with col18:
        st.write("######")
        st.image("img/moser_logo.png")
with col6:
    st.write("##")
    st.image("img/blue_bar.png")


