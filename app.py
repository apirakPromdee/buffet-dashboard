import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Busy Buffet - Data Analytics Test 2026",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS ตกแต่งให้ระเบียบอ่านง่าย สไตล์ Dashboard ส่งอาจารย์/พี่เลี้ยง
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E88E5; margin-bottom: 0px; }
    .sub-title { font-size: 16px; color: #555555; margin-bottom: 20px; }
    .card { background-color: #F8F9FA; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #1E88E5; }
    </style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD & PREPROCESS DATA
# ============================================================
@st.cache_data
def load_data():
    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"
    sheets = ["133", "143", "153", "173", "183"]
    data_list = []

    for sheet in sheets:
        data = pd.read_excel(file_path, sheet_name=sheet)
        data["date"] = sheet
        data_list.append(data)

    data = pd.concat(data_list, ignore_index=True)
    data = data.drop(columns=["Unnamed: 8", "Unnamed: 9"], errors="ignore")

    # แปลงเวลา
    for col in ["meal_start", "meal_end", "queue_start", "queue_end"]:
        data[col] = pd.to_datetime(data[col].astype(str), format="%H:%M:%S", errors="coerce")

    # คำนวณเวลา (นาที)
    data["meal_duration"] = (data["meal_end"] - data["meal_start"]).dt.total_seconds() / 60
    data["waiting_time"] = (data["queue_end"] - data["queue_start"]).dt.total_seconds() / 60
    data["walk_away"] = data["queue_start"].notna() & data["meal_start"].isna()

    return data

df = load_data()


# ============================================================
# SIDEBAR (ข้อมูลผู้จัดทำ & ตัวกรอง)
# ============================================================
with st.sidebar:
    st.header("📌 ข้อมูลแบบทดสอบ")
    st.write("**ตำแหน่ง:** Data Analyst Intern")
    st.write("**ผู้จัดทำ:** อภิรักษ์ พร้อมดี")
    st.write("**โครงการ:** Busy Buffet Operational Analysis")
    st.divider()
    
    st.subheader("🔍 ตัวกรองข้อมูล")
    selected_dates = st.multiselect("เลือกวันที่ต้องการดู:", options=df["date"].unique(), default=df["date"].unique())
    
    # Filter Data
    df_filtered = df[df["date"].isin(selected_dates)]


# ============================================================
# HEADER SECTION
# ============================================================
st.markdown('<p class="main-title">🍽️ Busy Buffet — Data Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">รายงานการวิเคราะห์ข้อมูลการดำเนินงาน และข้อเสนอแนะเชิงกลยุทธ์ (Internship Assessment 2026)</p>', unsafe_allow_html=True)

# Navigation Tabs ให้ดูเป็นสัดส่วน
tab1, tab2, tab3 = st.tabs(["📊 Task 1: Proof of Staff Comments", "🧪 Task 2: Evaluate 3 Proposed Actions", "💡 Task 3: Strategic Recommendation"])


# ============================================================
# TAB 1: TASK 1
# ============================================================
with tab1:
    st.header("Task 1: การตรวจสอบข้อเท็จจริงจาก Staff Comments")
    st.write("วิเคราะห์เปรียบเทียบความแตกต่างระหว่างกลุ่ม **In-house** และ **Walk-in** ในมิติ Waiting Time และ Walk-away Rate")
    st.divider()

    # Data Calculation
    waiting_summary = df_filtered[df_filtered["waiting_time"].notna()].groupby("Guest_type")["waiting_time"].mean().reset_index()
    waiting_summary["waiting_time"] = waiting_summary["waiting_time"].round(2)

    walkaway_summary = df_filtered[df_filtered["waiting_time"].notna()].groupby("Guest_type")["walk_away"].agg(
        waiting="count", walk_away="sum"
    ).reset_index()
    walkaway_summary["rate"] = ((walkaway_summary["walk_away"] / walkaway_summary["waiting"]) * 100).round(2)

    # Layout Graphs & Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. เวลารอคิวเฉลี่ย (Waiting Time)")
        fig1 = px.bar(
            waiting_summary, 
            x="Guest_type", 
            y="waiting_time", 
            text="waiting_time",
            color="Guest_type",
            color_discrete_map={"In house": "#64B5F6", "Walk in": "#1E88E5"},
            labels={"Guest_type": "ประเภทลูกค้า", "waiting_time": "เวลารอเฉลี่ย (นาที)"}
        )
        fig1.update_traces(texttemplate='%{text} นาที', textposition='outside')
        fig1.update_layout(showlegend=False, yaxis=dict(range=[0, 50]))
        st.plotly_chart(fig1, use_container_width=True)

        st.metric(label="Walk-in Avg. Waiting Time", value="38.4 นาที", delta="นานกว่า In-house +10.4 นาที")

    with col2:
        st.subheader("2. อัตราการยกเลิกคิว (Walk-away Rate)")
        fig2 = px.bar(
            walkaway_summary, 
            x="Guest_type", 
            y="rate", 
            text="rate",
            color="Guest_type",
            color_discrete_map={"In house": "#E57373", "Walk in": "#81C784"},
            labels={"Guest_type": "ประเภทลูกค้า", "rate": "อัตรา Walk-away (%)"}
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        fig2.update_layout(showlegend=False, yaxis=dict(range=[0, 35]))
        st.plotly_chart(fig2, use_container_width=True)

        st.metric(label="In-house Walk-away Rate", value="28.00%", delta="สูงกว่า Walk-in (14.58%)", delta_color="inverse")

    # Conclusion Box
    st.subheader("📝 สรุปผลการวิเคราะห์ (Analysis Finding)")
    st.warning("""
    **สรุปผล: PARTIALLY SUPPORTED (จริงเพียงบางส่วน)**
    * **ข้อเท็จจริง:** แม้ว่ากลุ่ม **Walk-in** จะต้องรอคิวนานกว่า (+10.42 นาที) แต่กลุ่ม **In-house** กลับมีอัตราการเดินออกจากร้าน (Walk-away Rate) สูงถึง **28.00%** (เทียบกับ Walk-in 14.58%)
    * **ข้อสันนิษฐาน:** ลูกค้าที่พักในโรงแรมมีความคาดหวังสูงกว่าและอดทนต่อการรอคิวน้อยกว่ากลุ่ม Walk-in อย่างมีนัยสำคัญ
    """)


# ============================================================
# TAB 2: TASK 2
# ============================================================
with tab2:
    st.header("Task 2: การวิเคราะห์และหักล้าง 3 แนวทางของโรงแรม")
    st.write("ประเมินความสมเหตุสมผลของข้อเสนอแนะในการแก้ปัญหาหน้าร้าน")
    st.divider()

    # ACTION 1
    st.subheader("1. การลดเวลานั่งกินอาหาร (เดิม 5 ชั่วโมง)")
    overall_meal = df_filtered["meal_duration"].dropna().agg(["mean", "median", "max"]).round(1)
    meal_by_type = df_filtered[df_filtered["meal_duration"].notna()].groupby("Guest_type")["meal_duration"].mean().reset_index().round(1)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("**สถิติเวลาการรับประทานอาหาร:**")
        st.metric("เวลาเฉลี่ย (Mean)", f"{overall_meal['mean']} นาที")
        st.metric("ค่ากลาง (Median)", f"{overall_meal['median']} นาที")
        st.metric("เวลานานที่สุด (Max)", f"{overall_meal['max']} นาที")

    with c2:
        fig_meal = px.bar(
            meal_by_type, 
            x="Guest_type", 
            y="meal_duration", 
            text="meal_duration",
            title="เวลาทานอาหารเฉลี่ยจำแนกตามประเภทลูกค้า (นาที)",
            color="Guest_type",
            color_discrete_sequence=["#4FC3F7", "#0288D1"]
        )
        fig_meal.update_traces(texttemplate='%{text} นาที', textposition='outside')
        fig_meal.update_layout(showlegend=False, yaxis=dict(range=[0, 90]))
        st.plotly_chart(fig_meal, use_container_width=True)

    st.error("**ผลการประเมิน Action 1:** ปฏิเสธแนวทางนี้ เนื่องจากเวลาทานอาหารเฉลี่ยจริงอยู่ที่เพียง **61 นาที** (Median 52 นาที) ไม่ได้มีลูกค้านั่งแช่ถึง 5 ชั่วโมง การลดเวลานั่งจึงแก้ปัญหาคอขวดหน้าร้านไม่ได้")
    st.divider()

    # ACTION 2 & 3 Side by Side
    st.subheader("2 & 3. การปรับราคาเป็น 259 บาท และ การให้ In-house ข้ามคิว")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Action 2: ปรับขึ้นราคา Buffet เป็น 259 บาท")
        daily_pax = df_filtered.groupby("date")["pax"].sum().reset_index()
        fig_pax = px.line(daily_pax, x="date", y="pax", markers=True, title="ปริมาณลูกค้าต่อวัน (Daily Demand)")
        st.plotly_chart(fig_pax, use_container_width=True)
        st.info("**วิเคราะห์:** Demand เฉลี่ยอยู่ที่ **122 pax/day** การขึ้นราคาอาจช่วยลด Demand Walk-in ได้ แต่เป็นการแก้ปัญหาที่อาจกระทบรายได้รวม และยังไม่มีข้อมูลทดสอบความยืดหยุ่นของราคา (Price Elasticity)")

    with col_b:
        st.markdown("#### Action 3: ให้ลูกค้า In-house ข้ามคิว (Queue Skipping)")
        st.write("เปรียบเทียบอัตราการ Walk-away ของลูกค้าทั้งสองกลุ่ม:")
        st.write("- **In-house Walk-away:** 28.00%")
        st.write("- **Walk-in Walk-away:** 14.58%")
        st.info("**วิเคราะห์:** แม้ In-house จะเป็นกลุ่มที่ได้รับผลกระทบสูงสุด แต่การข้ามคิวโดยไม่จัดสรร Capacity/โต๊ะสำรอง จะส่งผลให้คิวของ Walk-in สะสมรอนานยิ่งขึ้น และเกิดการ Walk-away ฝั่ง Walk-in พุ่งสูงขึ้นแทน")

    st.warning("**สรุป Task 2:** ทั้ง 3 แนวทางเดิมยังไม่สามารถแก้ปัญหาได้อย่างสมบูรณ์ ต้องอาศัยการจัดสรร Capacity ร่วมด้วย")


# ============================================================
# TAB 3: TASK 3
# ============================================================
with tab3:
    st.header("Task 3: ข้อเสนอแนะทางออกที่ดีที่สุด (Strategic Recommendation)")
    st.subheader("🎯 เลือกแนวทาง: Queue Skipping with Managed Capacity for In-house Guests")
    st.divider()

    st.markdown("### 💡 เหตุผลที่เลือกแนวทางนี้ (Why This Strategy?)")
    st.write("จากข้อมูลการวิเคราะห์พบว่า **In-house Walk-away Rate สูงถึง 28.00%** (สูงกว่า Walk-in เกือบ 2 เท่า) แสดงว่าลูกค้าโรงแรมเสียความรู้สึกจากการรอคิวและเลือกที่จะไม่กินอาหารที่ร้าน การแก้ปัญหากลุ่มนี้จึงเป็น Priority สูงสุดเพื่อรักษาภาพลักษณ์ของโรงแรม")

    st.divider()

    col_rec1, col_rec2 = st.columns(2)

    with col_rec1:
        st.markdown("### 🛠️ แนวทางการดำเนินงานหน้างาน (Implementation Plan)")
        st.markdown("""
        1. **Buffer Table Allocation (สำรองโต๊ะ):**
           * กั้นสัดส่วนโต๊ะ Indoor ประมาณ **30% - 40%** ไว้รองรับลูกค้า In-house ในช่วง Peak Hours (07:00 - 09:00 น.)
        2. **Digital Pre-Booking System (ระบบจองคิวล่วงหน้า):**
           * ให้ลูกค้า In-house สามารถสแกน QR Code จากห้องพักเพื่อกดรับคิวก่อนลงมาที่ห้องอาหาร
        3. **Fast-track Lane:**
           * จัดช่องทางเดินคิวพิเศษสำหรับ In-house เพื่อความรวดเร็วในการเข้าโต๊ะ
        """)

    with col_rec2:
        st.markdown("### 📈 เป้าหมายและการวัดผล (Expected Impact & KPIs)")
        st.success("""
        * **Primary KPI:** ลดอัตรา In-house Walk-away Rate จาก **28.00% ให้เหลือ < 10%** ภายใน 2 สัปดาห์
        * **Secondary KPI:** ควบคุมเวลารอเฉลี่ยของ In-house ไม่ให้เกิน **15 นาที**
        * **Control Metric:** รักษาระดับ Walk-in Waiting Time ไม่ให้เกิน **45 นาที** เพื่อป้องกันกระทบรายได้จาก Walk-in
        """)

    st.divider()
    st.info("📌 **สรุปส่งท้าย:** การใช้ Queue Skipping ควบคู่กับการทำ Buffer Capacity เป็นแนวทางที่ตรงจุด ใช้ต้นทุนต่ำที่สุด และสามารถลงมือปฏิบัติได้ทันที")
