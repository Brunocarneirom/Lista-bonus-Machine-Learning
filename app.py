import streamlit as st
import pandas as pd
import plotly as pt
import plotly.express as px
#from plotly.subplots import make_subplots
import re

personnel_url = "https://raw.githubusercontent.com/Brunocarneirom/Dashboard-Russia-Ukraine/main/russia_losses_personnel.csv"
equipment_url = "https://raw.githubusercontent.com/Brunocarneirom/Dashboard-Russia-Ukraine/main/russia_losses_equipment.csv"

# read csv from a URL
def get_data() -> pd.DataFrame:
    return pd.read_csv(personnel_url)

personnel = get_data()

# read csv from a URL
def get_data() -> pd.DataFrame:
    return pd.read_csv(equipment_url)

equipment = get_data()

war = pd.merge(equipment, personnel, on=["date", "day"])
war["equipment_loss"] = war['aircraft'] + war['helicopter'] + war['tank'] + war['APC'] + war['field artillery'] + war['naval ship']


st.set_page_config(
    page_title="Russia-Ukraine war dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Russia-Ukraine War")

st.header("Database overview")
st.dataframe(war)

st.header("War data overview")

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Casualties")
    fig1 = px.line(data_frame=war, x="day", y="personnel")
    st.write(fig1)

with fig_col2:
    st.markdown("### Equipment loss")
    fig2 = px.line(data_frame=war, x="day", y="equipment_loss")
    st.write(fig2)

def df_filter(message,war):

        slider_1, slider_2 = st.slider('%s' % (message),0,len(war)-1,[0,len(war)-1],1)

        while len(str(war.iloc[slider_1][1]).replace('.0','')) < 4:
            war.iloc[slider_1,1] = '0' + str(war.iloc[slider_1][1]).replace('.0','')
            
        while len(str(war.iloc[slider_2][1]).replace('.0','')) < 4:
            war.iloc[slider_2,1] = '0' + str(war.iloc[slider_1][1]).replace('.0','')
        
        filtered_df = war.iloc[slider_1:slider_2+1][:].reset_index(drop=True)

        return filtered_df

if __name__ == '__main__':

    st.title('Datetime Filter')
    filtered_df = df_filter('Move sliders to filter dataframe',war)

    column_1, column_2 = st.columns(2)

    with column_1:
        st.title('APC loss')
        st.line_chart(filtered_df['APC'])   

    with column_2:
        st.title('Aircraft loss')
        st.line_chart(filtered_df['aircraft'])                 

    column_3, column_4 = st.columns(2)      

    with column_3:
        st.title('Tank loss')
        st.line_chart(filtered_df['tank'])

    with column_4:
        st.title('Helicopter loss')
        st.line_chart(filtered_df['helicopter']) 

## Time frame from https://github.com/mkhorasani/interactive_datetime_filter/blob/main/interactive_datetime_filter.py       