import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Busy Buffet Analysis - Data Analyst Test", layout="wide"
)

st.title("Buffet Dashboard")


# โหลดข้อมูล
@st.cache_data
def load_data():
    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
    df = pd.read_excel(file_path)

    # แปลง time/datetime คอลัมน์ให้เป็น datetime object ที่ถูกต้อง
    time_cols = ["queue_start", "queue_end", "meal_start", "meal_end"]
    for col in time_cols:
        if col in df.columns:
            # แปลงเป็น string ก่อนแล้วค่อยแปลงเป็น datetime
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

    # สร้าง Flag สำหรับ Walk-away
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
# TASK 1
# -----------------------------------------------------------------------------
with tab1:
    st.header("Task 1: Prove / Disprove Staff Comments")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Waiting Time & Walk-away Rate")
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

        st.metric("In-house Avg Waiting Time", f"{avg_wait_inhouse:.1f} mins")
        st.metric(
            "Walk-in Avg Waiting Time",
            f"{avg_wait_walkin:.1f} mins",
            delta=f"{avg_wait_walkin - avg_wait_inhouse:.1f} mins longer",
        )

        st.metric("In-house Walk-away Rate", f"{walkaway_inhouse:.2f}%")
        st.metric("Walk-in Walk-away Rate", f"{walkaway_walkin:.2f}%")

    with col2:
        st.subheader("Key Findings & Commentary")
        st.write(
            """
        - **Partially Supported:** แม้ Walk-in จะรอนานกว่า In-house (+10.42 นาที) แต่ **In-house กลับมี Walk-away Rate สูงกว่าอย่างชัดเจน (28.00% vs 14.58%)**
        - **Insight:** แขกโรงแรม (In-house) มีความคาดหวังสูงและมีทางเลือกอื่น การต้องรอคิวทำให้เกิดความไม่พอใจจนยกเลิกการทานมากกว่า
        """
        )

# -----------------------------------------------------------------------------
# TASK 2
# -----------------------------------------------------------------------------
with tab2:
    st.header("Task 2: Disprove Recommended Actions")

    st.subheader("1. Reduce Seating Time (5 Hours to Less)")
    avg_duration = df["meal_duration"].mean()
    st.write(f"**Actual Avg Meal Duration:** {avg_duration:.1f} minutes")
    st.info(
        "**Disprove Reason:** ลูกค้าไม่ได้นั่งเต็ม 5 ชั่วโมง การลดเวลาสิทธิ์นั่งจึงไม่ช่วยเพิ่ม Table Turnover Rate ในทางปฏิบัติ"
    )

    st.subheader("2. Increase Price to 259 Baht Everyday")
    st.info(
        "**Disprove Reason:** การขึ้นราคาไม่ได้แก้ปัญหาคอขวด (Bottleneck) ที่จำนวนโต๊ะและความล่าช้าในการบริหารจัดการคิว"
    )

# -----------------------------------------------------------------------------
# TASK 3
# -----------------------------------------------------------------------------
with tab3:
    st.header("Task 3: Supported Solution - Queue Skipping for In-house")
    st.success(
        """
    **Recommendation:** ให้สิทธิ์ In-house Guest แทรกคิวหรือมีแถวพิเศษ (Priority Queue)
    
    **Why it works:**
    1. แก้ปัญหาตรงจุดเพราะ In-house มี Walk-away Rate สูงถึง 28.00%
    2. ช่วยรักษา Guest Satisfaction ของผู้พักในโรงแรมซึ่งเป็น Revenue หลัก
    3. ตั้งเป้าหมาย KPI จาก Pilot Test ลด Walk-away Rate ของ In-house ลงให้ต่ำกว่า 15%
    """
    )
