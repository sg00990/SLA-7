import streamlit as st
import time
from datetime import datetime
import json
from calendar import month_abbr

st.set_page_config(
    page_title="SLA 7 Questionnaire",
    page_icon="💻",
    layout="wide"
)

conn = st.connection("snowflake")

st.markdown('<p style="font-family:sans-serif; color:#324a62; font-size: 28px; font-weight: bold">Tier 1 SLA Questionnaire</p>', unsafe_allow_html=True)
st.write("###")

st.markdown('<p style="font-family:sans-serif; color:#87c440; font-size: 20px; font-weight: bold">SLA 7</p>', unsafe_allow_html=True)


st.write("**Total Possible Fields**")
total_fields = st.number_input("total_fields", step=1, min_value = 0, label_visibility="collapsed")

st.write("**Total Fields Passed**")
fields_passed = st.number_input("fields_passed", step=1, min_value = 0, label_visibility="collapsed")

st.write("**Percentage**")
perc = st.number_input("perc", label_visibility="collapsed")


this_year = datetime.now().year
this_month = datetime.now().month

st.write("**Month Reviewed**")
month_abbr = month_abbr[1:]
month_str = st.selectbox("month", options=month_abbr, index=this_month-1, label_visibility="collapsed")
month_reviewed = month_abbr.index(month_str) + 1

st.write("**Year Reviewed**")
year_reviewed = st.selectbox("year", range(this_year, this_year - 10, -1), label_visibility="collapsed")

date_reviewed = datetime(year_reviewed, month_reviewed, 1)

st.write("**Additional Comments**")
survey_text = st.text_area("survey_text", label_visibility="collapsed")
survey_text = survey_text.replace("\n", "  ").replace("'", "''").replace('"', r'\"')


col1, col2, col3 = st.columns(3)

with col3:
    if st.button("Submit", use_container_width=True):
        data = {
            "sla_7_possible_fields": total_fields,
            "sla_7_fields_passed": fields_passed,
            "sla_7_percentage": perc,
            "sla_7_date_reviewed": date_reviewed,
            "sla_7_comments": survey_text
        }

        json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

        date_submitted = datetime.now()

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


