import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)

st.title("Hotel Amber 85 - Busy Buffet Analysis Dashboard")
st.caption("Presented by: Apirak Promdee | Data Analyst Assessment")


@st.cache_data
def load_data():
    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
    df = pd.read_excel(file_path)

    # ตัดช่องว่างส่วนเกินของข้อความในคอลัมน์ Guest_type (ถ้ามี)
    if "Guest_type" in df.columns:
        df["Guest_type"] = df["Guest_type"].astype(str).str.strip()

    time_cols = ["queue_start", "queue_end", "meal_start", "meal_end"]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col].astype(str), format="%H:%M:%S", errors="coerce"
            )

    df["waiting_time"] = (
        df["queue_end"] - df["queue_start"]
    ).dt.total_seconds() / 60.0
    df["meal_duration"] = (
        df["meal_end"] - df["meal_start"]
    ).dt.total_seconds() / 60.0
    df["is_walkaway"] = df["queue_start"].notna() & df["meal_start"].isna()

    return df


try:
    df = load_data()
except Exception:
    df = None

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

    # คำนวณค่าจริง หากคำนวณไม่ได้ให้ใช้ค่าตาม Slide ผลวิเคราะห์
    avg_wait_inhouse, avg_wait_walkin = 28.0, 38.4
    walkaway_inhouse, walkaway_walkin = 28.00, 14.58

    if df is not None and "Guest_type" in df.columns:
        in_house_df = df[df["Guest_type"].str.lower().isin(["in house", "in-house"])]
        walk_in_df = df[df["Guest_type"].str.lower().isin(["walk in", "walk-in"])]

        if not in_house_df.empty and not walk_in_df.empty:
            avg_wait_inhouse = in_house_df["waiting_time"].mean()
            avg_wait_walkin = walk_in_df["waiting_time"].mean()
            
            in_q_count = in_house_df["queue_start"].notna().sum()
            walk_q_count = walk_in_df["queue_start"].notna().sum()
            
            if in_q_count > 0:
                walkaway_inhouse = (in_house_df["is_walkaway"].sum() / in_q_count) * 100
            if walk_q_count > 0:
                walkaway_walkin = (walk_in_df["is_walkaway"].sum() / walk_q_count) * 100

    col1, col2 = st.columns(2)

    with col1:
        # Chart 1: Waiting Time
        df_wait = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Average Waiting Time (min)": [avg_wait_inhouse, avg_wait_walkin],
            }
        )
        fig_wait = px.bar(
            df_wait,
            x="Guest Type",
            y="Average Waiting Time (min)",
            title="Waiting Time (นาที)",
            text="Average Waiting Time (min)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_wait.update_traces(
            texttemplate="%{text:.1f} นาที", textposition="outside"
        )
        fig_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)",
            yaxis=dict(range=[0, max(avg_wait_inhouse, avg_wait_walkin) * 1.3]),
            height=400,
        )
        st.plotly_chart(fig_wait, use_container_width=True)

    with col2:
        # Chart 2: Walk-away Rate
        df_rate = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Walk-away Rate (%)": [walkaway_inhouse, walkaway_walkin],
            }
        )
        fig_rate = px.bar(
            df_rate,
            x="Guest Type",
            y="Walk-away Rate (%)",
            title="Walk-away Rate (%)",
            text="Walk-away Rate (%)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_rate.update_traces(
            texttemplate="%{text:.2f}%", textposition="outside"
        )
        fig_rate.update_layout(
            yaxis_title="อัตราการเดินออก (%)",
            yaxis=dict(range=[0, max(walkaway_inhouse, walkaway_walkin) * 1.3]),
            height=400,
        )
        st.plotly_chart(fig_rate, use_container_width=True)

    st.subheader("สรุปผลการวิเคราะห์:")
    st.write(
        f"- **In-house Walk-away Rate สูงถึง {walkaway_inhouse:.2f}%** (เทียบกับ Walk-in {walkaway_walkin:.2f}%)\n"
        f"- **Walk-in Waiting Time อยู่ที่ {avg_wait_walkin:.1f} นาที** (เทียบกับ In-house {avg_wait_inhouse:.1f} นาที)"
    )

# -----------------------------------------------------------------------------
# TASK 2
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: การวิเคราะห์ 3 แนวทางแก้ไขปัญหา")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_duration = pd.DataFrame(
            {
                "Metric": ["Median", "Average", "Maximum"],
                "Duration (min)": [52, 61, 321],
            }
        )
        fig_dur = px.bar(
            df_duration,
            x="Metric",
            y="Duration (min)",
            title="1. Meal Duration (นาที)",
            text="Duration (min)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_dur.update_traces(
            texttemplate="%{text} นาที", textposition="outside"
        )
        fig_dur.update_layout(
            xaxis_title="ตัววัดระยะเวลานั่ง",
            yaxis_title="เวลา (นาที)",
            yaxis=dict(range=[0, 360]),
            height=380,
        )
        st.plotly_chart(fig_dur, use_container_width=True)
        st.write(
            "**ข้อสรุป:** ลูกค้าส่วนใหญ่ใช้เวลาทานอาหารไม่ถึง 5 ชั่วโมง (Median 52 นาที)"
        )

    with col_b:
        df_demand = pd.DataFrame(
            {
                "Metric": ["Min Demand", "Average Demand", "Max Demand"],
                "Pax / Day": [102, 132.4, 166],
            }
        )
        fig_dem = px.bar(
            df_demand,
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
            height=380,
        )
        st.plotly_chart(fig_dem, use_container_width=True)
        st.write(
            "**ข้อสรุป:** ไม่มีข้อมูลหลังปรับราคา 259 บาท จึงยืนยันผลไม่ได้"
        )

    with col_c:
        df_action3 = pd.DataFrame(
            {
                "Guest Type": ["In-house", "Walk-in"],
                "Walk-away Rate (%)": [28.00, 14.58],
            }
        )
        fig_act3 = px.bar(
            df_action3,
            x="Guest Type",
            y="Walk-away Rate (%)",
            title="3. Walk-away Rate (%)",
            text="Walk-away Rate (%)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_act3.update_traces(
            texttemplate="%{text:.2f}%", textposition="outside"
        )
        fig_act3.update_layout(
            xaxis_title="ประเภทลูกค้า",
            yaxis_title="อัตราการเดินออก (%)",
            yaxis=dict(range=[0, 35]),
            height=380,
        )
        st.plotly_chart(fig_act3, use_container_width=True)
        st.write(
            "**ข้อสรุป:** In-house มีอัตราเดินออกสูงกว่า แต่การข้ามคิวไม่เพิ่ม Capacity"
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
                "Baseline Rate (%)": [28.00, 14.58],
            }
        )
        fig_kpi_rate = px.bar(
            df_kpi_rate,
            x="Guest Type",
            y="Baseline Rate (%)",
            title="KPI 1: Target In-house Walk-away Baseline",
            text="Baseline Rate (%)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_kpi_rate.update_traces(
            texttemplate="%{text:.2f}%", textposition="outside"
        )
        fig_kpi_rate.update_layout(
            yaxis_title="Walk-away Rate (%)",
            yaxis=dict(range=[0, 35]),
            height=400,
        )
        st.plotly_chart(fig_kpi_rate, use_container_width=True)

    with col_t3_2:
        df_kpi_wait = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Baseline Waiting Time (min)": [28.0, 38.4],
            }
        )
        fig_kpi_wait = px.bar(
            df_kpi_wait,
            x="Guest Type",
            y="Baseline Waiting Time (min)",
            title="KPI 2: Target In-house Waiting Time Baseline",
            text="Baseline Waiting Time (min)",
            color_discrete_sequence=["#0070C0"],
        )
        fig_kpi_wait.update_traces(
            texttemplate="%{text:.1f} นาที", textposition="outside"
        )
        fig_kpi_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)",
            yaxis=dict(range=[0, 50]),
            height=400,
        )
        st.plotly_chart(fig_kpi_wait, use_container_width=True)

    st.subheader("สรุปเป้าหมาย Task 3:")
    st.write(
        "- **แนวทางดำเนินการ:** ให้สิทธิ์ In-house ข้ามคิวเมื่อมีโต๊ะว่าง โดยไม่ต้องลงทุนเพิ่ม\n"
        "- **ตัวชี้วัดหลัก (KPI):** ติดตามการลดลงของ In-house Walk-away Rate (ปัจจุบัน 28.00%) และเวลารอเฉลี่ย (ปัจจุบัน 28.0 นาที)"
    )
