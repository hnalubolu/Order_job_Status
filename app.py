from email import header
from secrets import choice
import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from st_aggrid import AgGrid,GridUpdateMode,JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(layout="wide")



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


td_data = pd.read_csv('ctm-logs.csv')
rgn_data = pd.read_csv('regions.csv')
file = open('refresh_time.csv')
content = file.readlines()
r_date = datetime.strptime(content[1][:-4], '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%b-%Y %H:%M:%S") + ' CST'

 
logs_data1 = pd.merge(td_data, rgn_data, on='job_name', how ='left')
logs_data = logs_data1.replace(np.nan, '',regex=True)


logs_data['orderDate'] = pd.to_datetime(logs_data['orderDate'], format='%y%m%d')
logs_data['orderDate'] = logs_data['orderDate'].dt.strftime('%d-%b-%Y')


image = Image.open('Delllogo2.png')
st.sidebar.image(image)
st.sidebar.header('Order Jobs Status')

ord_dates = sorted(list(logs_data['orderDate'].unique()), reverse=True)
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
    amer_status = "EXECUTING"
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
    emea_status = "EXECUTING"
elif emea_jobs == emea_succ:
    emea_status = "COMPLETED"
else:
    emea_status = "WAITING"


def main():

    

    


    amer, apj, emea = st.columns(3)

    with amer:
        st.subheader('AMER')
        amer.write(f"({amer_succ}/{amer_jobs}) jobs completed")
        pro = amer.progress(0)
        pro.progress(amer_succ_pct)

        bt_amer = amer.button(amer_status,key=1)

        if amer_status == "PROBLEM":
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
            elements[0].style.backgroundColor = 'orange'
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
            elements[0].style.backgroundColor = 'pink'
            </script>
            """
            )

    with apj:
        st.subheader('APJ')
        apj.write(f"({apj_succ}/{apj_jobs}) jobs completed")
        pro = apj.progress(0)
        pro.progress(apj_succ_pct)

        bt_apj = apj.button(apj_status,key=2)

        if apj_status == "PROBLEM":
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[1].style.backgroundColor = 'red'
            </script>
            """
            )

        elif apj_status == 'EXECUTING':
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[1].style.backgroundColor = 'orange'
            </script>
            """
            )
        elif apj_status == 'COMPLETED':
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[1].style.backgroundColor = 'green'
            </script>
            """
            )
        else:
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[1].style.backgroundColor = 'pink'
            </script>
            """
            )

    with emea:
        st.subheader('EMEA')
        emea.write(f"({emea_succ}/{emea_jobs}) jobs completed")
        pro = emea.progress(0)
        pro.progress(emea_succ_pct)

        bt_emea = emea.button(emea_status,key=3)

        if emea_status == "PROBLEM":
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[2].style.backgroundColor = 'red'
            </script>
            """
            )

        elif emea_status == 'EXECUTING':
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[2].style.backgroundColor = 'orange'
            </script>
            """
            )
        elif emea_status == 'COMPLETED':
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[2].style.backgroundColor = 'green'
            </script>
            """
            )
        else:
            components.html(
                """
            <script>
            const elements = window.parent.document.querySelectorAll('.stButton button')
            elements[2].style.backgroundColor = 'pink'
            </script>
            """
            )
      
    
    srch = st.sidebar.text_input('Job Name',max_chars=100)

    if srch != "":

        srch = srch.upper()

        mylst1 = logs_data[['job_name', 'status', 'startTime', 'endTime', 'estimatedStartTime', 'estimatedEndTime', 'description']].where(logs_data['job_name'].str.contains(srch))
        mylst = mylst1.dropna(subset=['job_name'])
        

    else:
        
        if bt_amer:
            mylst1 = logs_data[['job_name', 'status', 'startTime', 'endTime', 'estimatedStartTime', 'estimatedEndTime', 'description']].where(logs_data.region=='AMER')
            mylst = mylst1.dropna(subset=['job_name'])
            
        elif bt_apj:
            mylst1 = logs_data[['job_name', 'status', 'startTime', 'endTime', 'estimatedStartTime', 'estimatedEndTime', 'description']].where(logs_data.region=='APJ')
            mylst = mylst1.dropna(subset=['job_name'])
          

        elif bt_emea:
            mylst1 = logs_data[['job_name', 'status', 'startTime', 'endTime', 'estimatedStartTime', 'estimatedEndTime', 'description']].where(logs_data.region=='EMEA')
            mylst = mylst1.dropna(subset=['job_name'])
         
        else: 
            mylst1 = logs_data[['job_name', 'status', 'startTime', 'endTime', 'estimatedStartTime', 'estimatedEndTime', 'description']]
            mylst = mylst1.dropna(subset=['job_name'])
            

    mylst.rename(columns = {'job_name':'JOB NAME', 'status':'STATUS',
                'startTime': 'START TIME', 'endTime':'END TIME',
                'estimatedStartTime':'ESTIMATED START TIME', 'estimatedEndTime':'ESTIMATED END TIME'
                , 'description':'DESCRIPTION'}, inplace = True)

    


    cellstyle_jscode = JsCode("""
        function(params){
            if (params.value == 'Ended OK') {
                return {
                    'color': 'white',
                    'backgroundColor' : 'green'
            }
            }
            if (params.value == 'Ended Not OK') {
                return{
                    'color'  : 'white',
                    'backgroundColor' : 'red'
                }
            }
            if (params.value == 'Executing') {
                return{
                    'color'  : 'black',
                    'backgroundColor' : 'orange'
                }
            }
            else{
                return{
                    'color': 'black',
                    'backgroundColor': 'lightpink'
                }
            }
           
    };
    """)
    
    gd = GridOptionsBuilder.from_dataframe(mylst)
    gd.configure_pagination(enabled=True)
    gd.configure_columns("STATUS", cellStyle=cellstyle_jscode)
    gd.configure_default_column(tooltipField = 'DESCRIPTION')
    gridoptions = gd.build()
    AgGrid(mylst, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, height=400,
                allow_unsafe_jscode=True,theme='dark')
    

    st.sidebar.header('Data Refreshed at')
    st.sidebar.subheader(r_date)

main()










