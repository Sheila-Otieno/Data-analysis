import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import pydeck as pdk
warnings.filterwarnings('ignore')

st.set_page_config(page_title="LinkedIn Jobs", page_icon=":office:",layout="wide")

st.title(" :bar_chart: Analysis of Jobs in USA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\Sheila\Desktop\LinkedIn_jobs")
    df = pd.read_csv("LinkedInJobs.csv", encoding = "ISO-8859-1")

st.subheader("Table form view")
with st.expander("View Data"):
    st.dataframe(data=df)

##sidebar section
st.sidebar.header("Choose your filter: ")
#Filter for the state    
state = st.sidebar.multiselect("Pick the state", df["st_code"].unique())
if not state:
    df2 = df.copy()
else:
    df2 = df[df["st_code"].isin(state)]

##Filter for the city
city = st.sidebar.multiselect("Pick the city", df2["loc"].unique())
if not city:
    df3 = df2.copy()
else:
    df3 = df2[df2["loc"].isin(city)]


# Filter for experience level
level = st.sidebar.multiselect("Pick experience level",df3["xp_lvl"].unique())

# Filter the data based on State, city, and level

if not state and not city and not level:
    filtered_df = df
elif not city and not level:
    filtered_df = df[df["st_code"].isin(state)]
elif not state and not level:
    filtered_df = df[df["loc"].isin(city)]
elif state and city:
    filtered_df = df3[df["st_code"].isin(state) & df3["loc"].isin(city)]
elif state and level:
    filtered_df = df3[df["st_code"].isin(state) & df3["xp_lvl"].isin(level)]
elif city and level:
    filtered_df = df3[df["loc"].isin(city) & df3["xp_lvl"].isin(level)]
elif level:
    filtered_df = df3[df3["xp_lvl"].isin(level)]
else:
    filtered_df = df3[df3["st_code"].isin(state) & df3["loc"].isin(city) & df3["xp_lvl"].isin(level)]

max_salary = df3["max_sal"].max()
min_salary = df3["min_sal"].min()

#salary = st.sidebar.slider(
        #"Salary range",
         #min_value=min_salary,
         #max_value=max_salary,
         #value=(min_salary,max_salary)     
    #)

#salmax, salmin = salary

###df2= df2.loc[(df2['min_sal'] >= salmin) & (df2['max_sal'] <= salmax)]
with st.container(border=True):
    st.metric(label="Maximum salary :moneybag:", value=f"{max_salary}")
# Create a scatter plot
data1 = px.scatter(filtered_df, x = "max_sal", y = "views", size = "Emp_Cnt")
data1['layout'].update(title="Relationship between Salary and Number of views.",
                       titlefont = dict(size=20),xaxis = dict(title="Salary",titlefont=dict(size=19)),
                       yaxis = dict(title = "Views", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

category_df = filtered_df.groupby(by = ["xp_lvl"], as_index = False)[["max_sal","min_sal"]].sum()

st.subheader("Experience level and the maximum and minimum salaries")
fig = px.bar(category_df, x = "xp_lvl", y = "max_sal", text = ['${:,.2f}'.format(x) for x in category_df["max_sal"]],
            template = "seaborn")
fig1 = px.bar(category_df, x = "xp_lvl", y = "min_sal", text = ['${:,.2f}'.format(x) for x in category_df["min_sal"]],
            template = "seaborn")
st.plotly_chart(fig,use_container_width=True, height = 200)
st.plotly_chart(fig1,use_container_width=True, height = 200)



