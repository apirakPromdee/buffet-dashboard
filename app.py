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
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์ Excel Dataset: {e}")
    st.stop()

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

    col1, col2 = st.columns([1.2, 1])

    with col1:
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

        # Chart 1: Waiting Time Bar Chart
        df_wait = pd.DataFrame(
            {
                "Guest Type": ["In house", "Walk in"],
                "Waiting Time (min)": [avg_wait_inhouse, avg_wait_walkin],
            }
        )
        fig_wait = px.bar(
            df_wait,
            x="Guest Type",
            y="Waiting Time (min)",
            title="WAITING TIME",
            text_auto=".1f",
            color_discrete_sequence=["#0070C0"],
        )
        fig_wait.update_layout(
            height=250, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )
        st.plotly_chart(fig_wait, use_container_width=True)
        st.caption(f"Walk-in Waiting Time: **{avg_wait_walkin:.1f} min**")

        # Chart 2: Walk-away Rate Bar Chart
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
            title="WALK-AWAY RATE",
            text_auto=".2f",
            color_discrete_sequence=["#0070C0"],
        )
        fig_rate.update_layout(
            height=250, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )
        st.plotly_chart(fig_rate, use_container_width=True)
        st.caption(f"In-house Walk-away Rate: **{walkaway_inhouse:.2f}%**")

    with col2:
        st.subheader(
            "ลูกค้าไม่พอใจเรื่องเวลารอคิวและเดินออกจากร้าน"
        )
        st.write(
            f"""
        **ผลการวิเคราะห์: Partially Supported (จริงเพียงบางส่วน)**
        
        * **ลูกค้า In-house มี Walk-away Rate สูงถึง 28.00%** สูงกว่ากลุ่ม Walk-in (14.58%) เกือบ 2 เท่า
        * แม้กลุ่ม **Walk-in จะมีเวลารอคิวเฉลี่ยสูงกว่า** (38.4 นาที vs In-house 28.0 นาที)
        * แต่กลุ่ม In-house กลับยกเลิกคิวมากกว่า สะท้อนว่าลูกค้าที่พักในโรงแรมไวต่อเวลารอคิวอย่างมีนัยสำคัญ
        """
        )

# -----------------------------------------------------------------------------
# TASK 2
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: การวิเคราะห์ 3 แนวทางของโรงแรม")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            "1. ลดเวลานั่ง (5 ชม.)",
            "Median = 52 นาที",
            "Avg = 61 นาที | Max = 321 นาที",
        )
    with m2:
        st.metric(
            "2. เพิ่มราคา 259 บาท",
            "Avg Demand = 132.4 pax/day",
            "Demand อยู่ที่ 102-166 pax/day",
        )
    with m3:
        st.metric(
            "3. In-house ข้ามคิว",
            "Walk-away 28.00%",
            "Avg Wait 28.0 min",
        )

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. ลดเวลานั่ง?")
        st.write(
            """
        * **5 ชั่วโมงเป็นข้อจำกัดจริงหรือไม่?**
        * Average Meal Duration = **61 นาที** | Median = **52 นาที**
        * **สรุป:** ลูกค้าส่วนใหญ่ใช้เวลาไม่ถึง 5 ชั่วโมง การลดเวลานั่งอาจช่วยได้จำกัด
        """
        )

        st.subheader("2. เพิ่มราคา 259 บาท?")
        st.write(
            """
        * **ราคาที่สูงขึ้นจะลด Demand ได้จริงหรือไม่?**
        * Average Demand = **132.4 pax/day**
        * **สรุป:** ไม่มีข้อมูลหลังขึ้นราคา ยืนยันไม่ได้ว่าการขึ้นราคา 259 บาทจะลด Demand ได้มากพอที่จะลด Queue
        """
        )

    with col_b:
        st.subheader("3. In-house ข้ามคิว?")
        st.write(
            """
        * **ช่วยลดปัญหาของ In-house ได้หรือไม่?**
        * In-house มี Walk-away Rate สูงกว่า (28.00% vs 14.58%)
        * **สรุป:** สะท้อนว่าเป็นกลุ่มที่ได้รับผลกระทบจากการรอ แต่การข้ามคิวไม่ได้เพิ่มจำนวนโต๊ะหรือ Capacity ของร้าน
        """
        )

        st.info(
            "**สรุปการวิเคราะห์ 3 แนวทาง:** ทั้ง 3 แนวทางสามารถช่วยแก้ปัญหาได้บางส่วน แต่ยังไม่มีแนวทางใดที่สามารถแก้ปัญหาได้อย่างสมบูรณ์"
        )

# -----------------------------------------------------------------------------
# TASK 3
# -----------------------------------------------------------------------------
with tab3:
    st.header("Task 3: ข้อเสนอแนะ Queue Skipping for In-house Guests")

    col_t3_1, col_t3_2 = st.columns(2)

    with col_t3_1:
        st.subheader("ทำไมเลือกแนวทางนี้?")
        st.write(
            """
        * **In-house Walk-away Rate = 28.00%** (สูงกว่า Walk-in ที่ 14.58%)
        * **เหตุผลสำคัญ:** มองว่า In-house มีอัตรา Walk-away สูงกว่าเกือบ 2 เท่า จึงควรให้ความสำคัญกับกลุ่มนี้เป็นอันดับแรก
        * เป็นแนวทางที่สามารถทดลองใช้ได้ทันที **โดยไม่ต้องลงทุนเพิ่มในโต๊ะหรืออุปกรณ์**
        """
        )

    with col_t3_2:
        st.subheader("คาดหวังผลอะไร และวัดผลอย่างไร")
        st.write(
            """
        * **ผลลัพธ์ที่คาดหวัง:** ลด In-house Walk-away และ ลดเวลารอของ In-house
        * **KPI ที่ใช้ติดตาม:**
          * In-house Walk-away (ค่าปัจจุบัน **28.00%**)
          * In-house รอเฉลี่ย (ค่าปัจจุบัน **28.0 นาที**)
        * **เป้าหมายหลัก:** ลด In-house Walk-away โดยไม่กระทบ Walk-in มากเกินไป
        """
        )
