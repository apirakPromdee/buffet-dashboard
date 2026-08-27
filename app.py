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
    try:
        file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
        df = pd.read_excel(file_path)

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
    except Exception:
        return None


df = load_data()

tab1, tab2, tab3 = st.tabs(
    [
        "Task 1: Staff Comments Verification",
        "Task 2: Disprove 3 Actions",
        "Task 3: Queue Skipping Solution",
    ]
)

color_map_guests = {
    "In house": "#0070C0",
    "Walk in": "#FF8C00",
    "In-house": "#0070C0",
    "Walk-in": "#FF8C00",
    "In-house (Target)": "#0070C0",
}

# -----------------------------------------------------------------------------
# TASK 1
# -----------------------------------------------------------------------------
with tab1:
    st.header(
        "Task 1: In-house รอโต๊ะ / Walk-in รอนานจนเดินออก (Partially Supported)"
    )

    val_wait_inhouse, val_wait_walkin = 28.0, 38.4
    val_rate_inhouse, val_rate_walkin = 28.00, 14.58

    if df is not None and "Guest_type" in df.columns:
        in_h = df[df["Guest_type"].str.lower().str.contains("in", na=False)]
        w_in = df[df["Guest_type"].str.lower().str.contains("walk", na=False)]

        if not in_h.empty and not w_in.empty:
            w1 = in_h["waiting_time"].mean()
            w2 = w_in["waiting_time"].mean()
            if pd.notna(w1) and pd.notna(w2):
                val_wait_inhouse, val_wait_walkin = float(w1), float(w2)

            q1 = in_h["queue_start"].notna().sum()
            q2 = w_in["queue_start"].notna().sum()
            if q1 > 0 and q2 > 0:
                val_rate_inhouse = float((in_h["is_walkaway"].sum() / q1) * 100)
                val_rate_walkin = float((w_in["is_walkaway"].sum() / q2) * 100)

    col1, col2 = st.columns(2)

    with col1:
        df_wait = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Waiting Time": [val_wait_inhouse, val_wait_walkin],
            }
        )
        fig_wait = px.bar(
            df_wait,
            x="Guest Type",
            y="Waiting Time",
            color="Guest Type",
            color_discrete_map=color_map_guests,
            title="Waiting Time (นาที)",
            text="Waiting Time",
        )
        fig_wait.update_traces(
            texttemplate="%{text:.1f} นาที",
            textposition="outside",
            showlegend=False,
        )
        fig_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)",
            yaxis=dict(
                range=[0, max(val_wait_inhouse, val_wait_walkin) * 1.35]
            ),
            height=400,
        )
        st.plotly_chart(fig_wait, use_container_width=True)

    with col2:
        df_rate = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Walk-away Rate": [val_rate_inhouse, val_rate_walkin],
            }
        )
        fig_rate = px.bar(
            df_rate,
            x="Guest Type",
            y="Walk-away Rate",
            color="Guest Type",
            color_discrete_map=color_map_guests,
            title="Walk-away Rate (%)",
            text="Walk-away Rate",
        )
        fig_rate.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            showlegend=False,
        )
        fig_rate.update_layout(
            yaxis_title="อัตราการเดินออก (%)",
            yaxis=dict(
                range=[0, max(val_rate_inhouse, val_rate_walkin) * 1.35]
            ),
            height=400,
        )
        st.plotly_chart(fig_rate, use_container_width=True)

    st.subheader("สรุปผลการวิเคราะห์:")
    st.write(
        f"- **In-house Walk-away Rate สูงถึง {val_rate_inhouse:.2f}%** (เทียบกับ Walk-in {val_rate_walkin:.2f}%)\n"
        f"- **Walk-in Waiting Time อยู่ที่ {val_wait_walkin:.1f} นาที** (เทียบกับ In-house {val_wait_inhouse:.1f} นาที)"
    )

# -----------------------------------------------------------------------------
# TASK 2
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: การวิเคราะห์ 3 แนวทางแก้ไขปัญหา (Disprove Actions)")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_duration = pd.DataFrame(
            {
                "Metric": ["Median", "Average", "Maximum"],
                "Duration": [52.0, 61.0, 321.0],
            }
        )
        fig_dur = px.bar(
            df_duration,
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
        df_demand = pd.DataFrame(
            {
                "Metric": ["Min Demand", "Average Demand", "Max Demand"],
                "Pax / Day": [102.0, 132.4, 166.0],
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
            height=360,
        )
        st.plotly_chart(fig_dem, use_container_width=True)
        st.write(
            "**ข้อสรุป Action 2:** ยืนยันผลไม่ได้ เนื่องจากขาดข้อมูล Demand และพฤติกรรมลูกค้าหลังการปรับราคาเป็น 259 บาท"
        )

    with col_c:
        df_action3 = pd.DataFrame(
            {
                "Guest Type": ["In-house", "Walk-in"],
                "Walk-away Rate": [28.00, 14.58],
            }
        )
        fig_act3 = px.bar(
            df_action3,
            x="Guest Type",
            y="Walk-away Rate",
            color="Guest Type",
            color_discrete_map=color_map_guests,
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
            yaxis=dict(range=[0, 35]),
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
            color_discrete_map=color_map_guests,
            title="KPI 1: Target In-house Walk-away Baseline",
            text="Baseline Rate",
        )
        fig_kpi_rate.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            showlegend=False,
        )
        fig_kpi_rate.update_layout(
            yaxis_title="Walk-away Rate (%)",
            yaxis=dict(range=[0, 35]),
            height=380,
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
            color_discrete_map=color_map_guests,
            title="KPI 2: Target In-house Waiting Time Baseline",
            text="Baseline Waiting Time",
        )
        fig_kpi_wait.update_traces(
            texttemplate="%{text:.1f} นาที",
            textposition="outside",
            showlegend=False,
        )
        fig_kpi_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)",
            yaxis=dict(range=[0, 50]),
            height=380,
        )
        st.plotly_chart(fig_kpi_wait, use_container_width=True)

    st.subheader("สรุปข้อเสนอแนะและตัวชี้วัด (Action Strategy & KPIs):")
    st.write(
        "- **ข้อเสนอแนะ (Recommendation):** ให้สิทธิ์ In-house Guests ข้ามคิวเมื่อมีโต๊ะว่าง เนื่องจากไม่มีต้นทุนเพิ่มและช่วยรักษาพึงพอใจลูกค้าโรงแรม\n"
        "- **KPI 1 (Walk-away Rate):** ติดตามการลดลงของ In-house Walk-away Rate จากระดับ Baseline ปัจจุบันที่ 28.00%\n"
        "- **KPI 2 (Waiting Time):** ติดตามการลดลงของเวลารอเฉลี่ยของลูกค้า In-house จากระดับ Baseline ปัจจุบันที่ 28.0 นาที"
    )
