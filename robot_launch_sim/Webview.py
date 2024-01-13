import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math


Speaker_Height_high = 6.90625
Speaker_Height_low = 6.5
Speaker_depth = 2 + (1/3)
global G
G = 32.174
time_max = 10000 # in millseconds


st.title('Robot Sim')
col1, col2 = st.columns(2)

with col1:
    v = st.number_input('Launch speed',value=1)
    walldist = st.number_input('Distance',value=1)
    yoffset = st.number_input('Shooter height',value=1)

def Anglecalc(v = 0.0,x = 0.0,y = 0.0):
    try:
        temp =(v**2 - math.sqrt(v**4 - G * (G*x**2 + 2*y*v**2)))
        temp2 = (math.atan(temp/(G*x)))
        return temp2
    except:
        ValueError
        return 0


angle = Anglecalc(v,walldist,(Speaker_Height_low - yoffset))
angleh = Anglecalc(v,walldist - Speaker_depth,(Speaker_Height_high - yoffset))
anglem = angleh - ((angleh - angle)/2)
sim_time = walldist/(math.cos(angle)*v)
with col1:
    st.write(f"Target Low Angle {math.degrees(angle):.2f} degrees")
    st.write(f"Target High Angle {math.degrees(angleh):.2f} degrees")
    st.write(f"Target Middle Angle {math.degrees(anglem):.2f} degrees")
    st.write(f"Air Time : {sim_time:.2f} seconds")
    





def trajectory(v,t,angle):
    x = [0]
    y = [0]
    for each in range(int(sim_time*1000)+100):
        t = each/1000
        x.append(v*t*math.cos(angle))
        y.append(v*t*math.sin(angle) - (1/2) *G*t**2)
    return (x,y)


df = pd.DataFrame()
df['x'], df['y'] = trajectory(v,sim_time,angle)
df['type'] = "Low Trajectory"
df2 = pd.DataFrame()
df2['x'] = [walldist - Speaker_depth, walldist]
df2['y'] = [Speaker_Height_high - yoffset, Speaker_Height_low - yoffset]
df2['type'] = 'Speaker'
df= pd.concat([df,df2])

df3 = pd.DataFrame()
df3['x'], df3['y'] = trajectory(v,sim_time,angleh)
df3['type'] = 'High Trajectory'
df = pd.concat([df,df3])
df4 = pd.DataFrame()
df4['x'],df4['y'] = trajectory(v,sim_time,anglem)
df4['type'] = 'Middle Trajectory'
df = pd.concat([df,df4])
print(df)

fig = px.line(df, x=df['x'], y=df['y'],title="Simulation",labels={'x':'Distance away (Feet)', 'y':'Height from shooter (Feet)'},color='type')
fig.add_vline(x=walldist, annotation_text="Target Distance",annotation_position="bottom right",annotation_font_color="blue")

with col2:
    st.plotly_chart(fig)