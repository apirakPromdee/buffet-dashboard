import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)
st.title("Hotel Amber 85 - Busy Buffet Analysis Dashboard")
st.caption("Presented by: Apirak Promdee | Data Analyst Assessment")

COLOR_MAP = {
    "In house": "#0070C0",
    "Walk in": "#FF8C00",
    "In-house": "#0070C0",
    "Walk-in": "#FF8C00",
    "In-house (Target)": "#0070C0",
}
# ฟังก์ชันสร้าง Bar Chart ลดความซ้ำซ้อนของโค้ด
def create_bar_chart(
    df, x, y, title, y_title, fmt, y_max, color_col=None, height=380
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color_col or x,
        color_discrete_map=COLOR_MAP,
        color_discrete_sequence=["#0070C0"],
        title=title,
        text=y,
    )
    fig.update_traces(texttemplate=fmt, textposition="outside", showlegend=False)
    fig.update_layout(
        xaxis_title="",
        yaxis_title=y_title,
        yaxis=dict(range=[0, y_max]),
        height=height,
    )
    return fig
tab1, tab2, tab3 = st.tabs(
    [
        "Task 1: Staff Comments Verification",
        "Task 2: Disprove 3 Actions",
        "Task 3: Queue Skipping Solution",
    ]
)
# --- TASK 1 ---
with tab1:
    st.header(
        "Task 1: In-house รอโต๊ะ / Walk-in รอนานจนเดินออก (Partially Supported)"
    )
    col1, col2 = st.columns(2)
    with col1:
        df_wait = pd.DataFrame(
            {"Guest Type": ["In house", "Walk in"], "Val": [28.0, 38.4]}
        )
        st.plotly_chart(
            create_bar_chart(
                df_wait,
                "Guest Type",
                "Val",
                "Waiting Time (นาที)",
                "เวลารอเฉลี่ย (นาที)",
                "%{text:.1f} นาที",
                52,
            ),
            use_container_width=True,
        )
    with col2:
        df_rate = pd.DataFrame(
            {"Guest Type": ["In house", "Walk in"], "Val": [28.00, 14.58]}
        )
        st.plotly_chart(
            create_bar_chart(
                df_rate,
                "Guest Type",
                "Val",
                "Walk-away Rate (%)",
                "อัตราการเดินออก (%)",
                "%{text:.2f}%",
                38,
            ),
            use_container_width=True,
        )
    st.subheader("สรุปผลการวิเคราะห์:")
    st.write(
        "- **In-house Walk-away Rate สูงถึง 28.00%** (เทียบกับ Walk-in 14.58%)\n"
        "- **Walk-in Waiting Time อยู่ที่ 38.4 นาที** (เทียบกับ In-house 28.0 นาที)"
    )
# --- TASK 2 ---
with tab2:
    st.header("Task 2: การวิเคราะห์ 3 แนวทางแก้ไขปัญหา (Disprove Actions)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        df_dur = pd.DataFrame(
            {
                "Metric": ["Median", "Average", "Maximum"],
                "Val": [52.0, 61.0, 321.0],
            }
        )
        st.plotly_chart(
            create_bar_chart(
                df_dur,
                "Metric",
                "Val",
                "1. Meal Duration (นาที)",
                "เวลา (นาที)",
                "%{text:.0f} นาที",
                360,
                color_col="Metric",
                height=340,
            ),
            use_container_width=True,
        )
        st.write(
            "**ข้อสรุป Action 1:** ไม่สนับสนุนการจำกัดเวลา 1.5 ชม. เพราะ Median อยู่ที่เพียง 52 นาที"
        )
    with col_b:
        df_dem = pd.DataFrame(
            {
                "Metric": ["Min Demand", "Average Demand", "Max Demand"],
                "Val": [102.0, 132.4, 166.0],
            }
        )
        st.plotly_chart(
            create_bar_chart(
                df_dem,
                "Metric",
                "Val",
                "2. Daily Demand (คน/วัน)",
                "จำนวนลูกค้า (คน/วัน)",
                "%{text:.1f}",
                200,
                color_col="Metric",
                height=340,
            ),
            use_container_width=True,
        )
        st.write(
            "**ข้อสรุป Action 2:** ยืนยันผลไม่ได้ เนื่องจากขาดข้อมูล Demand หลังการปรับราคาเป็น 259 บาท"
        )
    with col_c:
        df_act3 = pd.DataFrame(
            {"Guest Type": ["In-house", "Walk-in"], "Val": [28.00, 14.58]}
        )
        st.plotly_chart(
            create_bar_chart(
                df_act3,
                "Guest Type",
                "Val",
                "3. Walk-away Rate (%)",
                "อัตราการเดินออก (%)",
                "%{text:.2f}%",
                38,
                height=340,
            ),
            use_container_width=True,
        )
        st.write(
            "**ข้อสรุป Action 3:** การข้ามคิวไม่เพิ่ม Capacity แต่เหมาะสมสำหรับใช้ลด In-house Walk-away Rate"
        )

# --- TASK 3 ---
with tab3:
    st.header("Task 3: KPI ติดตามผล Queue Skipping for In-house Guests")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        df_kpi1 = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Val": [28.00, 14.58],
            }
        )
        st.plotly_chart(
            create_bar_chart(
                df_kpi1,
                "Guest Type",
                "Val",
                "KPI 1: Target In-house Walk-away Baseline",
                "Walk-away Rate (%)",
                "%{text:.2f}%",
                38,
            ),
            use_container_width=True,
        )
    with col_t2:
        df_kpi2 = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Val": [28.0, 38.4],
            }
        )
        st.plotly_chart(
            create_bar_chart(
                df_kpi2,
                "Guest Type",
                "Val",
                "KPI 2: Target In-house Waiting Time Baseline",
                "เวลารอเฉลี่ย (นาที)",
                "%{text:.1f} นาที",
                52,
            ),
            use_container_width=True,
        )

    st.subheader("สรุปข้อเสนอแนะและตัวชี้วัด (Action Strategy & KPIs):")
    st.write(
        "- **ให้ลูกค้า In-house ได้รับสิทธิ์ข้ามคิว เมื่อมีโต๊ะว่าง เพื่อช่วยลดโอกาสที่ลูกค้าจะ Walk-away\n"
        "- **KPI 1 (Walk-away Rate):** ติดตามการลดลงของ In-house Walk-away Rate จาก Baseline 28.00%\n"
        "- **KPI 2 (Waiting Time):** ติดตามการลดลงของเวลารอเฉลี่ยของลูกค้า In-house จาก Baseline 28.0 นาที"
    )
