from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


st.markdown(
        """
    <style>
    .stButton>button {
        border-radius: 0%;
        height: 75px;
        width: 390px;
        font-size: 30px;
    
    }

    .stProgress .st-bo {
    background-color: green; 
  
    
    }

    div.block-container{
        padding-top:2rem;
        padding-bottom:2rem
        }

    button {
        display: inline-block;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def color_survived(val):
    color = 'red' if val=="Ended Not OK" else 'yellow' if val in ("Wait User", "Wait Condition") else 'lightblue' if val == 'Executing' else 'green'
    return f'background-color: {color}'


td_data = pd.read_csv(r'\\auspwdsapp01.aus.amer.dell.com\aus_hana_offline$\controlM_logs\ctm-logs.csv')
rgn_data = pd.read_excel('Jobs_Rgn.xlsx')

logs_data = pd.merge(td_data, rgn_data, on='job_name', how ='left')

ord_dates = sorted(list(set(logs_data['orderDate'])), reverse=True)
choice = st.sidebar.selectbox("Order Date", ord_dates)

logs_data = logs_data[logs_data['orderDate']==choice]


df_endedok = len(logs_data[logs_data['status']=='Ended OK'])
df_endednotok = len(logs_data[logs_data['status']=='Ended Not OK'])
df_wait = len(logs_data[logs_data['status'].str.contains('Wait')])


amer_jobs = len(logs_data[logs_data['region']=='AMER'])
apj_jobs = len(logs_data[logs_data['region']=='APJ'])
emea_jobs = len(logs_data[logs_data['region']=='EMEA'])


amer_succ = len(logs_data[(logs_data["region"]=="AMER") & (logs_data["status"]=="Ended OK")])
amer_exec = len(logs_data[(logs_data["region"]=="AMER") & (logs_data["status"]=="Executing")])
amer_fail = len(logs_data[(logs_data["region"]=="AMER") & (logs_data["status"]=="Ended Not OK")])
amer_wait = len(logs_data[(logs_data["region"]=="AMER") & (logs_data["status"].str.contains('Wait'))])

apj_succ = len(logs_data[(logs_data["region"]=="APJ") & (logs_data["status"]=="Ended OK")])
apj_exec = len(logs_data[(logs_data["region"]=="APJ") & (logs_data["status"]=="Executing")])
apj_fail = len(logs_data[(logs_data["region"]=="APJ") & (logs_data["status"]=="Ended Not OK")])
apj_wait = len(logs_data[(logs_data["region"]=="APJ") & (logs_data["status"].str.contains('Wait'))])

emea_succ = len(logs_data[(logs_data["region"]=="EMEA") & (logs_data["status"]=="Ended OK")])
emea_exec = len(logs_data[(logs_data["region"]=="EMEA") & (logs_data["status"]=="Executing")])
emea_fail = len(logs_data[(logs_data["region"]=="EMEA") & (logs_data["status"]=="Ended Not OK")])
emea_wait = len(logs_data[(logs_data["region"]=="EMEA") & (logs_data["status"].str.contains('Wait'))])


amer_succ_pct = int(amer_succ/amer_jobs*100)
apj_succ_pct = int(apj_succ/apj_jobs*100)
emea_succ_pct = int(emea_succ/emea_jobs*100)

if amer_fail > 0:
    amer_status = "PROBLEM"
elif amer_exec > 0:
    amer_status = "Executing"
elif amer_jobs == amer_succ:
    amer_status = "COMPLETED"
else:
    amer_status = "WAITING"


if apj_fail > 0:
    apj_status = "PROBLEM"
elif apj_exec > 0:
    apj_status = "EXECUTING"
elif apj_jobs == apj_succ:
    apj_status = "COMPLETED"
else:
    apj_status = "WAITING"

if emea_fail > 0:
    emea_status = "PROBLEM"
elif emea_exec > 0:
    emea_status = "Executing"
elif emea_jobs == apj_succ:
    emea_status = "COMPLETED"
else:
    emea_status = "WAITING"

def global_rgn():
    
    if bt_global:

        amer, apj, emea = st.columns(3)

        with amer:
            amer.write(f"({amer_succ}/{amer_jobs}) jobs completed")
            pro = amer.progress(0)
            pro.progress(amer_succ_pct)

            bt_amer1 = amer.button('AMER',key=1)

            if amer_status == 'PROBLEM':
                components.html(
                    """
                <script>
                 const elements = window.parent.document.querySelectorAll('.stButton button')
                elements[0].style.backgroundColor = 'red'
                </script>
                """
                )
            elif amer_status == 'EXECUTING':
                components.html(
                    """
                <script>
                const elements = window.parent.document.querySelectorAll('.stButton button')
                elements[0].style.backgroundColor = 'lightblue'
                </script>
                """
                )
            elif amer_status == 'COMPLETED':
                components.html(
                    """
                <script>
                const elements = window.parent.document.querySelectorAll('.stButton button')
                elements[0].style.backgroundColor = 'green'
                </script>
                """
                )
            else:
                components.html(
                    """
                <script>
                const elements = window.parent.document.querySelectorAll('.stButton button')
                elements[0].style.backgroundColor = 'yellow'
                </script>
                """
                )
      