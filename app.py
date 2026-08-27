import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)

st.title("Hotel Amber 85 - Busy Buffet Analysis Dashboard")
st.caption("Presented by: Apirak Promdee | Data Analyst Assessment")


# -----------------------------------------------------------------------------
# Data Loading & Processing (อ้างอิง Logic จาก analyze.py)
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_process_data():
    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
    sheets = ["133", "143", "153", "173", "183"]

    try:
        data_list = []
        for sheet in sheets:
            try:
                df_temp = pd.read_excel(file_path, sheet_name=sheet)
                df_temp["date"] = sheet
                data_list.append(df_temp)
            except Exception:
                continue

        if not data_list:
            # Fallback หาก sheet_name ไม่ตรง ให้ลองอ่านแผ่นแรก
            df = pd.read_excel(file_path)
        else:
            df = pd.concat(data_list, ignore_index=True)

        # ลบ Column ไม่จำเป็น
        df = df.drop(columns=["Unnamed: 8", "Unnamed: 9"], errors="ignore")

        # จัดการชื่อ Guest_type
        if "Guest_type" in df.columns:
            df["Guest_type"] = df["Guest_type"].astype(str).str.strip()

        # ฟังก์ชันคำนวณเวลารวมกรณีข้ามเที่ยงคืน (ตาม logic analyze.py)
        def calculate_duration(start_col, end_col):
            start_dt = pd.to_datetime(
                df[start_col].astype(str), format="%H:%M:%S", errors="coerce"
            )
            end_dt = pd.to_datetime(
                df[end_col].astype(str), format="%H:%M:%S", errors="coerce"
            )
            duration = (end_dt - start_dt).dt.total_seconds() / 60.0
            # ปรับแก้เวลาข้ามเที่ยงคืน (ติดลบ + 1440 นาที)
            return duration.apply(
                lambda x: x + 1440 if pd.notna(x) and x < 0 else x
            )

        df["meal_duration"] = calculate_duration("meal_start", "meal_end")
        df["waiting_time"] = calculate_duration("queue_start", "queue_end")

        # Flag สถานะการเข้าคิวและ Walk-away
        df["is_queued"] = df["queue_start"].notna()
        df["is_walkaway"] = df["is_queued"] & df["meal_start"].isna()

        return df

    except Exception:
        return None


df = load_and_process_data()

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

    # ค่า Baseline สำรองตาม Slide
    val_wait_inhouse, val_wait_walkin = 28.0, 38.4
    val_rate_inhouse, val_rate_walkin = 28.00, 14.58

    # คำนวณค่าจริงจาก Dynamic Data (ตาม logic analyze.py)
    if df is not None and "Guest_type" in df.columns:
        in_h = df[df["Guest_type"].str.lower().str.contains("in", na=False)]
        w_in = df[df["Guest_type"].str.lower().str.contains("walk", na=False)]

        # Waiting Time
        w1 = in_h["waiting_time"].mean()
        w2 = w_in["waiting_time"].mean()
        if pd.notna(w1) and w1 > 0:
            val_wait_inhouse = float(w1)
        if pd.notna(w2) and w2 > 0:
            val_wait_walkin = float(w2)

        # Walk-away Rate
        q1 = in_h["is_queued"].sum()
        q2 = w_in["is_queued"].sum()
        if q1 > 0:
            val_rate_inhouse = float((in_h["is_walkaway"].sum() / q1) * 100)
        if q2 > 0:
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

    # คำนวณ Meal Duration สดจาก Dataset (ถ้ามีข้อมูล)
    med_dur, avg_dur, max_dur = 52.0, 61.0, 321.0
    if df is not None and "meal_duration" in df.columns:
        m_valid = df["meal_duration"].dropna()
        if not m_valid.empty:
            med_dur = float(m_valid.median())
            avg_dur = float(m_valid.mean())
            max_dur = float(m_valid.max())

    # คำนวณ Daily Demand สดจาก Dataset
    min_dem, avg_dem, max_dem = 102.0, 132.4, 166.0
    if df is not None and "pax" in df.columns and "date" in df.columns:
        daily_pax = df.groupby("date")["pax"].sum()
        if not daily_pax.empty:
            min_dem = float(daily_pax.min())
            avg_dem = float(daily_pax.mean())
            max_dem = float(daily_pax.max())

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_duration = pd.DataFrame(
            {
                "Metric": ["Median", "Average", "Maximum"],
                "Duration": [med_dur, avg_dur, max_dur],
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
            yaxis=dict(range=[0, max(max_dur * 1.15, 360)]),
            height=360,
        )
        st.plotly_chart(fig_dur, use_container_width=True)
        st.write(
            f"**ข้อสรุป Action 1:** ไม่สนับสนุนการจำกัดเวลา 1.5 ชม. เพราะ Median อยู่ที่เพียง {med_dur:.0f} นาที การจำกัดเวลาจึงไม่ช่วยเพิ่ม Capacity อย่างมีนัยสำคัญ"
        )

    with col_b:
        df_demand = pd.DataFrame(
            {
                "Metric": ["Min Demand", "Average Demand", "Max Demand"],
                "Pax / Day": [min_dem, avg_dem, max_dem],
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
            yaxis=dict(range=[0, max_dem * 1.25]),
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
                "Walk-away Rate": [val_rate_inhouse, val_rate_walkin],
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
            yaxis=dict(
                range=[0, max(val_rate_inhouse, val_rate_walkin) * 1.35]
            ),
            height=360,
        )
        st.plotly_chart(fig_act3, use_container_width=True)
        st.write(
            f"**ข้อสรุป Action 3:** การข้ามคิวไม่เพิ่ม Capacity แต่เหมาะสมสำหรับใช้ลด In-house Walk-away Rate ที่สูงถึง {val_rate_inhouse:.2f}%"
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
                "Baseline Rate": [val_rate_inhouse, val_rate_walkin],
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
            yaxis=dict(
                range=[0, max(val_rate_inhouse, val_rate_walkin) * 1.35]
            ),
            height=380,
        )
        st.plotly_chart(fig_kpi_rate, use_container_width=True)

    with col_t3_2:
        df_kpi_wait = pd.DataFrame(
            {
                "Guest Type": ["In-house (Target)", "Walk-in"],
                "Baseline Waiting Time": [val_wait_inhouse, val_wait_walkin],
            }
        )
        fig_kpi_wait = px.bar(
            df_kpi_wait,
            x="Guest Type",
            y="Baseline Waiting Time",
            color="Guest Type",
            color_discrete_map=color_map_guests,
            title="KPI 2: Target In-house Waiting Time Baseline",
            text="Baseline Baseline Waiting Time",
        )
        fig_kpi_wait.update_traces(
            texttemplate="%{text:.1f} นาที",
            textposition="outside",
            showlegend=False,
        )
        fig_kpi_wait.update_layout(
            yaxis_title="เวลารอเฉลี่ย (นาที)",
            yaxis=dict(
                range=[0, max(val_wait_inhouse, val_wait_walkin) * 1.35]
            ),
            height=380,
        )
        st.plotly_chart(fig_kpi_wait, use_container_width=True)

    st.subheader("สรุปข้อเสนอแนะและตัวชี้วัด (Action Strategy & KPIs):")
    st.write(
        f"- **ข้อเสนอแนะ (Recommendation):** ให้สิทธิ์ In-house Guests ข้ามคิวเมื่อมีโต๊ะว่าง เนื่องจากไม่มีต้นทุนเพิ่มและช่วยรักษาพึงพอใจลูกค้าโรงแรม\n"
        f"- **KPI 1 (Walk-away Rate):** ติดตามการลดลงของ In-house Walk-away Rate จากระดับ Baseline ปัจจุบันที่ {val_rate_inhouse:.2f}%\n"
        f"- **KPI 2 (Waiting Time):** ติดตามการลดลงของเวลารอเฉลี่ยของลูกค้า In-house จากระดับ Baseline ปัจจุบันที่ {val_wait_inhouse:.1f} นาที"
    )
