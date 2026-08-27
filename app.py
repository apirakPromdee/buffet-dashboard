import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------------------------------------------------
# 1. กราฟ Demand Breakdown (จำนวนกลุ่มลูกค้า)
# ---------------------------------------------------------
df_demand = pd.DataFrame({
    'Guest Type': ['In-house', 'Walk-in'],
    'Count': [45, 73]
})

fig_demand = px.bar(
    df_demand, 
    x='Guest Type', 
    y='Count',
    title='<b>Guest Volume Breakdown (Demand)</b>',
    text='Count',  # แสดงตัวเลข 45 และ 73 บนหัวแท่งกราฟ
    color='Guest Type',
    color_discrete_sequence=['#64B5F6', '#2196F3']
)

fig_demand.update_traces(
    textposition='outside', 
    textfont_size=16,
    textfont_weight='bold'
)
fig_demand.update_layout(
    xaxis_title="Guest Category",
    yaxis_title="Number of Groups (Count)",
    showlegend=False,
    height=420,
    yaxis=dict(range=[0, 90])  # ขยายขอบเขตแกน Y ให้ตัวเลขไม่ชนขอบบน
)

st.plotly_chart(fig_demand, use_container_width=True)


# ---------------------------------------------------------
# 2. กราฟ Meal Duration (เวลาทานอาหารเฉลี่ย - นาที)
# ---------------------------------------------------------
df_duration = pd.DataFrame({
    'Guest Type': ['In-house', 'Walk-in'],
    'Duration': [45, 73]  # ใส่ค่าเวลาทานอาหารจริงตาม Dataset ของคุณ
})

fig_duration = px.bar(
    df_duration, 
    x='Guest Type', 
    y='Duration',
    title='<b>Average Meal Duration by Guest Type</b>',
    text_template='%{y} นาที',  # ระบุหน่วย "นาที" บนแท่งกราฟ
    color_discrete_sequence=['#42A5F5']
)

fig_duration.update_traces(
    textposition='outside', 
    textfont_size=16,
    textfont_weight='bold'
)
fig_duration.update_layout(
    xaxis_title="Guest Category",
    yaxis_title="Duration (Minutes)",
    height=420,
    yaxis=dict(range=[0, 90])
)

st.plotly_chart(fig_duration, use_container_width=True)
