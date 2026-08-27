import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ตั้งค่าหน้า Dashboard
st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)

st.title("Hotel Amber 85 - Busy Buffet Analysis Dashboard")
st.caption("Data Analyst Assessment | Deployed via Streamlit")


# โหลดข้อมูล
@st.cache_data
def load_data():
    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
    df = pd.read_excel(file_path)

    # แปลงเวลา
    time_cols = ["queue_start", "queue_end", "meal_start", "meal_end"]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col].astype(str), format="%H:%M:%S", errors="coerce"
            )

    # คำนวณ waiting_time และ meal_duration (นาที)
    df["waiting_time"] = (
        df["queue_end"] - df["queue_start"]
    ).dt.total_seconds() / 60.0
    df["meal_duration"] = (
        df["meal_end"] - df["meal_start"]
    ).dt.total_seconds() / 60.0

    # Flag Walk-away
    df["is_walkaway"] = df["queue_start"].notna() & df["meal_start"].isna()

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์ Excel Dataset: {e}")
    st.stop()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    [
        "Task 1: Staff Comments Verification",
        "Task 2: Disprove Actions",
        "Task 3: Proposed Solution",
    ]
)

# -----------------------------------------------------------------------------
# TASK 1: VERIFICATION & CHARTS
# -----------------------------------------------------------------------------
with tab1:
    st.header("Task 1: Prove / Disprove Staff Comments")

    # Metrics Overview
    in_house_df = df[df["Guest_type"] == "In house"]
    walk_in_df = df[df["Guest_type"] == "Walk in"]

    avg_wait_inhouse = in_house_df["waiting_time"].mean()
    avg_wait_walkin = walk_in_df["waiting_time"].mean()

    walkaway_inhouse = (
        in_house_df["is_walkaway"].sum()
        / in_house_df["queue_start"].notna().sum()
    ) * 100
    walkaway_walkin = (
        walk_in_df["is_walkaway"].sum()
        / walk_in_df["queue_start"].notna().sum()
    ) * 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("In-house Avg Wait Time", f"{avg_wait_inhouse:.1f} mins")
    m2.metric(
        "Walk-in Avg Wait Time",
        f"{avg_wait_walkin:.1f} mins",
        delta=f"+{avg_wait_walkin - avg_wait_inhouse:.1f} mins",
    )
    m3.metric("In-house Walk-away Rate", f"{walkaway_inhouse:.2f}%")
    m4.metric("Walk-in Walk-away Rate", f"{walkaway_walkin:.2f}%")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Chart 1.1: Walk-away Rate Comparison")
        # Visual 1: Bar chart Walk-away Rate
        walkaway_data = pd.DataFrame(
            {
                "Guest Type": ["In-house", "Walk-in"],
                "Walk-away Rate (%)": [walkaway_inhouse, walkaway_walkin],
            }
        )
        fig_rate = px.bar(
            walkaway_data,
            x="Guest Type",
            y="Walk-away Rate (%)",
            color="Guest Type",
            text_auto=".2f",
            title="Walk-away Rate by Guest Type",
            color_discrete_map={
                "In-house": "#EF553B",
                "Walk-in": "#636EFA",
            },
        )
        fig_rate.update_traces(texttemplate="%{y:.2f}%", textposition="outside")
        fig_rate.update_layout(yaxis_range=[0, 35], showlegend=False)
        st.plotly_chart(fig_rate, use_container_width=True)

    with col_chart2:
        st.subheader("Chart 1.2: Average Waiting Time Comparison")
        # Visual 2: Bar chart Wait Time
        wait_data = pd.DataFrame(
            {
                "Guest Type": ["In-house", "Walk-in"],
                "Avg Wait Time (mins)": [avg_wait_inhouse, avg_wait_walkin],
            }
        )
        fig_wait = px.bar(
            wait_data,
            x="Guest Type",
            y="Avg Wait Time (mins)",
            color="Guest Type",
            text_auto=".1f",
            title="Average Waiting Time by Guest Type",
            color_discrete_map={
                "In-house": "#EF553B",
                "Walk-in": "#636EFA",
            },
        )
        fig_wait.update_traces(texttemplate="%{y:.1f} mins", textposition="outside")
        fig_wait.update_layout(yaxis_range=[0, 45], showlegend=False)
        st.plotly_chart(fig_wait, use_container_width=True)

    st.subheader("Key Findings")
    st.write(
        """
    - **Partially Supported:** แม้ Walk-in จะรอนานกว่า In-house (+10.42 นาที) แต่ **In-house กลับมี Walk-away Rate สูงกว่าอย่างชัดเจน (28.00% vs 14.58%)**
    - **Insight:** แขกโรงแรม (In-house) มีความคาดหวังสูงกว่า และมีทางเลือกอื่น การต้องรอคิวทำให้เกิดความไม่พอใจจนยกเลิกการทานมากกว่า
    """
    )

# -----------------------------------------------------------------------------
# TASK 2: DISPROVE ACTIONS & CHARTS
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: Disprove Recommended Actions")

    col_t2_1, col_t2_2 = st.columns(2)

    with col_t2_1:
        st.subheader("1. Disprove: Reduce Seating Time (5 Hours to Less)")
        # Boxplot/Histogram of Actual Meal Duration
        valid_meal_df = df[df["meal_duration"].notna()]
        fig_duration = px.histogram(
            valid_meal_df,
            x="meal_duration",
            nbins=15,
            title="Distribution of Actual Meal Duration (Minutes)",
            labels={"meal_duration": "Meal Duration (Mins)"},
            color_discrete_sequence=["#00CC96"],
        )
        avg_dur = valid_meal_df["meal_duration"].mean()
        fig_duration.add_vline(
            x=avg_dur,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Avg: {avg_dur:.1f} mins",
        )
        st.plotly_chart(fig_duration, use_container_width=True)

        st.info(
            f"**Data Analysis:** ระยะเวลาทานอาหารจริงเฉลี่ยคือ **{avg_dur:.1f} นาที** (ไม่มีลูกค้านั่งเต็ม 5 ชั่วโมงเลย) ดังนั้นการลดเวลาจำกัดนั่งจาก 5 ชั่วโมงลงมา จึงไม่ช่วยเพิ่มอัตราหมุนเวียนโต๊ะ (Table Turnover)"
        )

    with col_t2_2:
        st.subheader("2. Disprove: Increase Price to 259 Baht Everyday")
        # Guest Type Breakdown Chart
        guest_count = (
            df["Guest_type"].value_counts().reset_index()
        )
        guest_count.columns = ["Guest Type", "Count"]

        fig_guest = px.pie(
            guest_count,
            values="Count",
            names="Guest Type",
            title="Guest Volume Share (In-house vs Walk-in)",
            hole=0.4,
            color_discrete_sequence=["#636EFA", "#EF553B"],
        )
        st.plotly_chart(fig_guest, use_container_width=True)

        st.info(
            "**Data Analysis:** สัดส่วนลูกค้าส่วนใหญ่เป็น Walk-in การขึ้นราคาเป็น 259 บาทเป็นการแก้ปัญหาผิดจุด เพราะปัญหาหลักคือ Bottleneck ในการบริหารคิว ไม่ใช่เรื่องราคา"
        )

# -----------------------------------------------------------------------------
# TASK 3: PROPOSED SOLUTION & KPI IMPACT
# -----------------------------------------------------------------------------
with tab3:
    st.header("Task 3: Supported Solution - Queue Skipping for In-house")

    col_t3_1, col_t3_2 = st.columns(2)

    with col_t3_1:
        st.subheader("Target Impact: In-house Walk-away Rate Reduction")
        # Comparison Chart (Current Baseline vs Target)
        kpi_df = pd.DataFrame(
            {
                "Stage": ["Current Baseline", "Target (Post Pilot)"],
                "Walk-away Rate (%)": [28.00, 10.00],
            }
        )
        fig_kpi = px.bar(
            kpi_df,
            x="Stage",
            y="Walk-away Rate (%)",
            color="Stage",
            text_auto=".2f",
            title="In-house Walk-away Rate Projection",
            color_discrete_map={
                "Current Baseline": "#EF553B",
                "Target (Post Pilot)": "#00CC96",
            },
        )
        fig_kpi.update_traces(
            texttemplate="%{y:.2f}%", textposition="outside"
        )
        fig_kpi.update_layout(yaxis_range=[0, 35], showlegend=False)
        st.plotly_chart(fig_kpi, use_container_width=True)

    with col_t3_2:
        st.subheader("Strategic Reasoning")
        st.success(
            """
        **ทำไม Queue Skipping ถึงเป็นวิธีที่ดีที่สุด:**
        1. **แก้ปัญหาตรงจุด:** ปัจจุบัน In-house เสียโอกาสและยกเลิกคิวสูงถึง **28.00%**
        2. **รักษา Revenue หลัก:** แขกที่พักโรงแรมจ่ายค่าห้องพัก การให้บริการมื้อเช้าที่ราบรื่นช่วยรักษาภาพลักษณ์และคะแนนรีวิวโรงแรม
        3. **ไม่ต้องลงทุนเพิ่ม:** ใช้การจัดการลำดับคิว (Priority Lane) แทนการลดเวลาหรือปรับราคาที่กระทบฐานลูกค้า
        """
        )
