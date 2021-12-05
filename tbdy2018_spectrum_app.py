# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 22:20:04 2021

@author: hakan
"""

# simple_streamlit_app.py


import numpy as np
import streamlit as st
from bokeh.plotting import figure
from Deneme_Spectrum_Streamlit import soilType_func
from pandas import read_excel
from numpy import arange
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
 
# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


st.title("Turkish Building Seismic Code (TBEC) - 2018 SaR and SaE Calculation App")


"""
This application was developed to find out design (SaR) and elastic spectral acceleration (SaE) of the structure
that located in Turkey. 

To use the app you should choose at the following steps below:
    
    1- Write the exact location of the structure.
    2- Type of structure
    3- Ductility of structure
    4- Structure's supporting system against earthquake loads.
    5- Building importance Factor
    6- Soil Type
    7- Fundamental period of the structure that you want to find exact
        SaR and SaE values.
        
To find the more information about these parameters please check the TBEC 2018
Chapter 2, 3 & 4. You can download the TBEC 2018 in Turkish format at the following
link: https://www.imo.org.tr/resimler/dosya_ekler/89227ad223d3b7a_ek.pdf
    
After these choices this app will give the design point for fundamental period of the structure.

Note: These results calculated with enterpolation of the spectral values of the coordinates that
shared by AFAD (https://tdth.afad.gov.tr/TDTH/main.xhtml). These results cannot use for the design or any studies
please be sure the find design parameters from the AFAD system. This app just prepared to give an information.

"""

st.subheader("Exact Location of the Structure")

# This part uses for the get data from Excel sheet about the spectral variables.

my_sheet_main = 'Sayfa1' # change it to your sheet name
main_file_name = 'parametre_UPD.xlsx' # change it to the name of your excel file
df_main = read_excel(main_file_name, sheet_name = my_sheet_main, engine='openpyxl')
# print(df_main.head()) # shows headers with top 5 rows
# print(df_main.info())

my_sheet = 'Sayfa1' # change it to your sheet name
file_name = 'unique_lat_lon.xlsx' # change it to the name of your excel file
df = read_excel(file_name, sheet_name = my_sheet, engine='openpyxl')
# print(df.head()) # shows headers with top 5 rows
# print(df.info())

r_d = 'Sayfa1' # change it to your sheet name
file_name = 'r_d.xlsx' # change it to the name of your excel file
df_r_d = read_excel(file_name, sheet_name = r_d, engine='openpyxl')
# print(df.head()) # shows headers with top 5 rows
# print(df.info())

longitude = df["Boylam"].to_frame()
latitude = df["Enlem"].to_frame()

# Let's start the streamlit commands for inputs


st.sidebar.header("Structure Location")
x = st.sidebar.number_input("Longitude (Range: 26.00 - 45.00)",value=29.01, step=0.1)
y = st.sidebar.number_input("Latitude: (Range: 36.00 - 42.00)",value=41.10, step=0.1)

raw_data = {'lat': [y],
'lon': [x]}
df = pd.DataFrame(raw_data, columns = ['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=y,
        longitude=x,
        zoom=11,
        pitch=50,
        ),
    layers=[
        # pdk.Layer(
        #     'HexagonLayer',
        #     data=df,
        #     get_position='[lon, lat]',
        #     radius=200,
        #     elevation_scale=4,
        #     elevation_range=[0, 1000],
        #     pickable=True,
        #     extruded=True,
        #     ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=1000,
            ),
        ],
    ))

"""

Please be sure the coordinates of the structure by the help of map. 
This map will show your location that you selected from left side of the screen.

"""
# Displaying Latitude and Longitude
print("Latitude: ", str(y))
print("Longitude: ", str(x))
 
# Get location with geocode
location = geolocator.geocode(str(y)+","+str(x))

st.success("Adress: " + str(location))
st.success("Longitude: " + str(x) + " & Latitude: " + str(y))


st.subheader("Type of Structure")

"""
Please choose structure' type, ductility and supporting system from the list.

Tables that shared below will be updated according to your choices.

"""

"""
According to TBEC 2018, to draw SaR/SaE - Period(T) graphs, you should use
same parameters about the structural system. 

These parameters can be seen below:
    
    1- BTS (Building Supporting System)
    2- R (Response Modification Factor)
    3- D (System Overstrength Factor)

"""


structure_type = st.selectbox("Type of Structure: ", {"Steel", "Concrete"})
ductility = st.selectbox("Ductility of Structure: ", {"High", "Moderate", "Low"})
if structure_type == "Steel":
    if ductility == "High":
        df_r_d_sub = df_r_d[13:19]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"C11", "C12","C13","C14","C15","C16"})

    elif ductility == "Moderate":
        df_r_d_sub = df_r_d[19:22]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"C21", "C22"})
    else:
        df_r_d_sub = df_r_d[22:24]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"C31", "C32","C33"})
elif structure_type == "Concrete":
    if ductility == "High":
        df_r_d_sub = df_r_d[0:6]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"A11", "A12", "A13", "A14", "A15", "A16"})
    elif ductility == "Moderate":
        df_r_d_sub = df_r_d[6:10]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"A21", "A22", "A23","A24"})
    else:
        df_r_d_sub = df_r_d[10:13]
        st.write(df_r_d_sub[["BTS","R","D"]])
        structure_category = st.selectbox("Category: ", {"A31", "A32","A33"})

str_cat_final = df_r_d.loc[df_r_d['BTS']==structure_category]
R = str_cat_final['R'].iloc[0]
D = str_cat_final['D'].iloc[0]
ToSS = str_cat_final['BTS'].iloc[0]

# st.markdown("Type of Structural System: " + str(ToSS))
# st.markdown("R: " + str(R))
# st.markdown("D: " + str(D))

I_var = [1.0,1.2,1.5]

df_I = pd.DataFrame(list(I_var))
df_I.columns = ['I']
st.write(df_I)
# R = st.sidebar.selectbox("Seismic Response Modification Factor - R: ", {1,2,3,4,5,6,7,8})
# D = st.sidebar.selectbox("Overstrength Coefficient - D: ",{1, 1.5, 2, 2.5, 3})
I = st.selectbox("Building Importance Factor - I : ", {1, 1.2, 1.5})

soilType = st.selectbox("Soil Type: ", {"ZA","ZB","ZC","ZD","ZE","ZF"})
T = st.number_input("Period of Structure - T: ",value=0.20, step=0.1)

# print(latitude.iloc[(latitude['Enlem']-y).abs().argsort()[:2]])
# print(longitude.iloc[(longitude['Boylam']-x).abs().argsort()[:2]])

df_sort_y = latitude.iloc[(latitude['Enlem']-y).abs().argsort()[:2]]
# print(df_sort_y.index.tolist())
df_sort_x = longitude.iloc[(longitude['Boylam']-x).abs().argsort()[:2]]
# print(df_sort_x.index.tolist())

numbers_y = df_sort_y['Enlem'].tolist()
numbers_x = df_sort_x['Boylam'].tolist()


x1 = min(numbers_x)
x2 = max(numbers_x)
y1 = min(numbers_y)
y2 = max(numbers_y)  

x_f = (x-x1)/(x2-x1)
y_f = (y-y1)/(y2-y1)

var1_look = str(x1)+str(y1)
var2_look = str(x2)+str(y1)
var3_look = str(x1)+str(y2)
var4_look = str(x2)+str(y2)

variables_list = [var1_look, var2_look, var3_look,var4_look]
df_variables = pd.DataFrame(variables_list)
df_variables.columns = ['Merged']

var1_final = df_main.loc[df_main['Merged']==var1_look]
var2_final = df_main.loc[df_main['Merged']==var2_look]
var3_final = df_main.loc[df_main['Merged']==var3_look]
var4_final = df_main.loc[df_main['Merged']==var4_look]

var1_s1= var1_final['S12'].iloc[0]
var2_s1= var2_final['S12'].iloc[0]
var3_s1= var3_final['S12'].iloc[0]
var4_s1= var4_final['S12'].iloc[0]
var1_ss= var1_final['SS2'].iloc[0]
var2_ss= var2_final['SS2'].iloc[0]
var3_ss= var3_final['SS2'].iloc[0]
var4_ss= var4_final['SS2'].iloc[0]

var1_var2_s1 = var1_s1+x_f*(var2_s1-var1_s1)
var3_var4_s1 =var3_s1+x_f*(var4_s1-var3_s1)
var1_var2_ss = var1_ss+x_f*(var2_ss-var1_ss)
var3_var4_ss =var3_ss+x_f*(var4_ss-var3_ss)

s1 = var1_var2_s1 + y_f*(var3_var4_s1 - var1_var2_s1)
ss = var1_var2_ss + y_f*(var3_var4_ss - var1_var2_ss)
                            
# find center and radius
sDs, sD1, Fs, F1 = soilType_func(soilType, ss, s1)

tSpectrum = []
for i in arange(0.0, 8.0, 0.001):
    tSpectrum.append(format(i, ".3f"))

tA = (0.2*sD1/sDs)
tB = (sD1/sDs)
tL = 6.0
length_T = len(tSpectrum)

sAec = []
tRs = []

i = 0
while i < length_T:
    if float(tSpectrum[i]) >= 0.0 and float(tSpectrum[i]) < tA:
        sAe = (0.4+0.6*float(tSpectrum[i])/tA)*sDs
        tRs.append(format(sAe, ".3f"))
    elif float(tSpectrum[i]) >= tA and float(tSpectrum[i]) < tB:
        sAe = sDs
        tRs.append(format(sAe, ".3f"))
    elif float(tSpectrum[i]) >= tB and float(tSpectrum[i]) < tL:
        sAe = sD1/float(tSpectrum[i])
        tRs.append(format(sAe, ".3f"))
    elif float(tSpectrum[i]) >= tL:
        sAe = sD1*tL / float(tSpectrum[i])**2
        tRs.append(format(sAe, ".3f"))

    i += 1

df = pd.DataFrame(list(zip(tSpectrum, tRs)), columns =['Period', 'Sae'], dtype = float)
# df.plot(x ='Period', y='Sae', kind = 'line')
# plt.show()


rA = []

i = 0
while i < length_T:
    if float(tSpectrum[i]) >= tB:
        rAT = R/I
        rA.append(format(rAT, ".3f"))
    elif float(tSpectrum[i]) <= tB:
        rAT = D+(R/I-D)*float(tSpectrum[i])/tB
        rA.append(format(rAT, ".3f"))
    i += 1

df["R"] = rA
df["R"] = df["R"].astype(float)

# print(df.head())

period_spec = df["Period"].to_frame()
# print(period_spec.iloc[(period_spec['Period']-T).abs().argsort()[:2]])
df_period = period_spec.iloc[(period_spec['Period']-T).abs().argsort()[:2]]
numbers_period = df_period['Period'].tolist()
T = min(numbers_period)

df["Sar"] = df["Sae"]/df["R"]
# print(df.head())

t_final = df.loc[df['Period']==T]
Sar = t_final['Sar'].iloc[0]
Sae = t_final['Sae'].iloc[0]
exact_point = {'Period': [T], 'Sar': [Sar]}
design_point = pd.DataFrame(exact_point)


# print("Design Spectral Acceleration is: " + str(format(Sar, ".3f")) + "g")

st.sidebar.header("General Information of the Structural System")

st.sidebar.markdown("Type of the Structure: " + structure_type)
st.sidebar.markdown("Ductility: " + ductility )
st.sidebar.markdown("Supporting System Category: " + structure_category )
st.sidebar.markdown("Building Importance Factor: " + str(I))
st.sidebar.markdown("Soil Type: " + soilType )
st.sidebar.markdown("Location: Lon: " + str(x) + " & Lat: " + str(y))
st.sidebar.markdown("Period of Structure: " + str(format(T, ".2f")) + "s")
# st.sidebar.markdown("SaR: " + str(format(Sar, ".3f")) + "g")
# st.sidebar.markdown("SaE: " + str(format(Sae, ".3f")) + "g")
st.sidebar.success("SaE: " + str(format(Sae, ".3f")) + "g")
st.sidebar.success("SaR: " + str(format(Sar, ".3f")) + "g")
# p = figure(
#     title="Design Spectrum",
#     x_axis_label="Period",
#     y_axis_label="Spectral Acceleration",
#     match_aspect=True,
#     tools="pan,reset,save,wheel_zoom",
# )

# t_period = df["Period"].to_frame()
# Sar = df["Sar"].to_frame()
# p.line(t_period, Sar, color="#1f77b4", line_width=3, line_alpha=0.6)


# p.xaxis.fixed_location = 0
# p.yaxis.fixed_location = 0

# st.bokeh_chart(p)

import matplotlib.pyplot as plt


# fig_saE = plt.figure()
# ax = fig_saE.add_subplot(1,1,1)

# ax.scatter(df["Period"], df["Sae"],color='r',linewidth=1)
# # ax = design_point.plot(x ='Period', y='Sar', kind = 'scatter',c = "red", label = "Design Spectrum")

# ax.set_xlabel("Period (T)")
# ax.set_ylabel("SaE (g)")


# df.plot(ax=ax, x ='Period', y='Sar', kind = 'line', label = "Design Point")

# st.write(fig_saE)



# fig_saR = plt.figure()
# ax = fig_saR.add_subplot(1,1,1)

# ax.scatter(df["Period"], df["Sar"],color='r',linewidth=1)
# # ax = design_point.plot(x ='Period', y='Sar', kind = 'scatter',c = "red", label = "Design Spectrum")

# ax.set_xlabel("Period (T)")
# ax.set_ylabel("SaR (g)")

#Line Chart
as_list = df["Period"].tolist()

df.index = as_list

df_Sar = df['Sar']
df_Sae = df['Sae']

"""
Elastic Spectral Acceleration - Period Graph

"""
st.line_chart(df_Sae)

"""
Design Spectral Acceleration - Period Graph

"""

st.line_chart(df_Sar)

# df.plot(ax=ax, x ='Period', y='Sar', kind = 'line', label = "Design Point")

# st.write(fig_saR)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

