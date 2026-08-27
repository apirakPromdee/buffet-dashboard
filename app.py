Python
# ---------------------------------------------------------
# 2. กราฟ Meal Duration (แก้ไขโค้ดบรรทัด 47)
# ---------------------------------------------------------
fig_duration = px.bar(
    df_duration, 
    x='Guest Type', 
    y='Duration',
    title='<b>Average Meal Duration by Guest Type</b>',
    text='Duration',
    color='Guest Type',
    color_discrete_sequence=['#64B5F6', '#2196F3']
)

fig_duration.update_traces(
    texttemplate='%{y} นาที',  # ย้าย texttemplate มาไว้ใน update_traces
    textposition='outside', 
    textfont_size=16,
    textfont_weight='bold'
)
fig_duration.update_layout(
    xaxis_title="Guest Category",
    yaxis_title="Duration (Minutes)",
    showlegend=False,
    height=420,
    yaxis=dict(range=[0, 90])
)

st.plotly_chart(fig_duration, use_container_width=True)
