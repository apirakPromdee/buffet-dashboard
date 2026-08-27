import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)

st.title("Hotel Amber 85 - Busy Buffet Analysis Dashboard")
st.caption("Presented by: Apirak Promdee | Data Analyst Assessment")

# กำหนดสีมาตรฐานแยกตามประเภทลูกค้า (In-house=ฟ้า, Walk-in=ส้ม)
color_map = {
    "In house": "#0070C0",
    "Walk in": "#FF8C00",
    "In-house": "#0070C0",
    "Walk-in": "#FF8C00",
    "In-house (Target)": "#0070C0",
}

tab1, tab2, tab3 = st.tabs(
    [
        "Task 1: Staff Comments Verification",
        "Task 2: Disprove 3 Actions",
        "Task 3: Queue Skipping Solution",
    ]
)

# -----------------------------------------------------------------------------
# TASK 1
# -----------------------------------------------------------------------------
with tab1:
    st.header(
        "Task 1: In-house รอโต๊ะ / Walk-in รอนานจนเดินออก (Partially Supported)"
    )

    col1, col2 = st.columns(2)

    with col1:
        df_wait = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Waiting Time": [28.0, 38.4],
            }
        )
        fig_wait = px.bar(
            df_wait,
            x="Guest Type",
            y="Waiting Time",
            color="Guest Type",
            color_discrete_map=color_map,
            title="Waiting Time (นาที)",
            text="Waiting Time",
        )
        fig_wait.update_traces(
            texttemplate="%{text:.1f} นาที",
            textposition="outside",
            showlegend=False,
        )
        fig_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)", yaxis=dict(range=[0, 52]), height=400
        )
        st.plotly_chart(fig_wait, use_container_width=True)

    with col2:
        df_rate = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Walk-away Rate": [28.00, 14.58],
            }
        )
        fig_rate = px.bar(
            df_rate,
            x="Guest Type",
            y="Walk-away Rate",
            color="Guest Type",
            color_discrete_map=color_map,
            title="Walk-away Rate (%)",
            text="Walk-away Rate",
        )
        fig_rate.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            showlegend=False,
        )
        fig_rate.update_layout(
            yaxis_title="อัตราการเดินออก (%)", yaxis=dict(range=[0, 38]), height=400
        )
        st.plotly_chart(fig_rate, use_container_width=True)

    st.subheader("สรุปผลการวิเคราะห์:")
    st.write(
        "- **In-house Walk-away Rate สูงถึง 28.00%** (เทียบกับ Walk-in 14.58%)\n"
        "- **Walk-in Waiting Time อยู่ที่ 38.4 นาที** (เทียบกับ In-house 28.0 นาที)"
    )

# -----------------------------------------------------------------------------
# TASK 2
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: การวิเคราะห์ 3 แนวทางแก้ไขปัญหา (Disprove Actions)")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_dur = pd.DataFrame(
            {
                "Metric": ["Median", "Average", "Maximum"],
                "Duration": [52.0, 61.0, 321.0],
            }
        )
        fig_dur = px.bar(
            df_dur,
            x="Metric",
            y="Duration",
            title="1. Meal Duration (นาที)",
            text="Duration",
            color_discrete_sequence=["#0070C0"],
        )
        fig_dur.update_traces(
            texttemplate="%{text:.0f} นาที", textposition="outside"
        )
        fig_dur.update_layout(
            xaxis_title="ตัววัดระยะเวลานั่ง",
            yaxis_title="เวลา (นาที)",
            yaxis=dict(range=[0, 360]),
            height=360,
        )
        st.plotly_chart(fig_dur, use_container_width=True)
        st.write(
            "**ข้อสรุป Action 1:** ไม่สนับสนุนการจำกัดเวลา 1.5 ชม. เพราะ Median อยู่ที่เพียง 52 นาที การจำกัดเวลาจึงไม่ช่วยเพิ่ม Capacity อย่างมีนัยสำคัญ"
        )

    with col_b:
        df_dem = pd.DataFrame(
            {
                "Metric": ["Min Demand", "Average Demand", "Max Demand"],
                "Pax / Day": [102.0, 132.4, 166.0],
            }
        )
        fig_dem = px.bar(
            df_dem,
            x="Metric",
            y="Pax / Day",
            title="2. Daily Demand (คน/วัน)",
            text="Pax / Day",
            color_discrete_sequence=["#0070C0"],
        )
        fig_dem.update_traces(
            texttemplate="%{text:.1f}", textposition="outside"
        )
        fig_dem.update_layout(
            xaxis_title="ระดับ Demand ปัจจุบัน",
            yaxis_title="จำนวนลูกค้า (คน/วัน)",
            yaxis=dict(range=[0, 200]),
            height=360,
        )
        st.plotly_chart(fig_dem, use_container_width=True)
        st.write(
            "**ข้อสรุป Action 2:** ยืนยันผลไม่ได้ เนื่องจากขาดข้อมูล Demand และพฤติกรรมลูกค้าหลังการปรับราคาเป็น 259 บาท"
        )

    with col_c:
        df_act3 = pd.DataFrame(
            {
                "Guest Type": ["In-house", "Walk-in"],
                "Walk-away Rate": [28.00, 14.58],
            }
        )
        fig_act3 = px.bar(
            df_act3,
            x="Guest Type",
            y="Walk-away Rate",
            color="Guest Type",
            color_discrete_map=color_map,
            title="3. Walk-away Rate (%)",
            text="Walk-away Rate",
        )
        fig_act3.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            showlegend=False,
        )
        fig_act3.update_layout(
            xaxis_title="ประเภทลูกค้า",
            yaxis_title="อัตราการเดินออก (%)",
            yaxis=dict(range=[0, 38]),
            height=360,
        )
        st.plotly_chart(fig_act3, use_container_width=True)
        st.write(
            "**ข้อสรุป Action 3:** การข้ามคิวไม่เพิ่ม Capacity แต่เหมาะสมสำหรับใช้ลด In-house Walk-away Rate ที่สูงถึง 28.00%"
        )

# -----------------------------------------------------------------------------
# TASK 3
# -----------------------------------------------------------------------------
with tab3:
    st.header("Task 3: KPI ติดตามผล Queue Skipping for In-house Guests")

    col_t3_1, col_t3_2 = st.columns(2)

    with col_t3_1:
        df_kpi_rate = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Baseline Rate": [28.00, 14.58],
            }
        )
        fig_kpi_rate = px.bar(
            df_kpi_rate,
            x="Guest Type",
            y="Baseline Rate",
            color="Guest Type",
            color_discrete_map=color_map,
            title="KPI 1: Target In-house Walk-away Baseline",
            text="Baseline Rate",
        )
        fig_kpi_rate.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            showlegend=False,
        )
        fig_kpi_rate.update_layout(
            yaxis_title="Walk-away Rate (%)", yaxis=dict(range=[0, 38]), height=380
        )
        st.plotly_chart(fig_kpi_rate, use_container_width=True)

    with col_t3_2:
        df_kpi_wait = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Baseline Waiting Time": [28.0, 38.4],
            }
        )
        fig_kpi_wait = px.bar(
            df_kpi_wait,
            x="Guest Type",
            y="Baseline Waiting Time",
            color="Guest Type",
            color_discrete_map=color_map,
            title="KPI 2: Target In-house Waiting Time Baseline",
            text="Baseline Waiting Time",
        )
        fig_kpi_wait.update_traces(
            texttemplate="%{text:.1f} นาที",
            textposition="outside",
            showlegend=False,
        )
        fig_kpi_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)", yaxis=dict(range=[0, 52]), height=380
        )
        st.plotly_chart(fig_kpi_wait, use_container_width=True)

    st.subheader("สรุปข้อเสนอแนะและตัวชี้วัด (Action Strategy & KPIs):")
    st.write(
        "- **ข้อเสนอแนะ (Recommendation):** ให้สิทธิ์ In-house Guests ข้ามคิวเมื่อมีโต๊ะว่าง เนื่องจากไม่มีต้นทุนเพิ่มและช่วยรักษาความพึงพอใจลูกค้าโรงแรม\n"
        "- **KPI 1 (Walk-away Rate):** ติดตามการลดลงของ In-house Walk-away Rate จากระดับ Baseline ปัจจุบันที่ 28.00%\n"
        "- **KPI 2 (Waiting Time):** ติดตามการลดลงของเวลารอเฉลี่ยของลูกค้า In-house จากระดับ Baseline ปัจจุบันที่ 28.0 นาที"
    )
