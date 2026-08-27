git add app.py
git commit -m "Update chart title and labels"
git push origin main

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Busy Buffet - Data Analytics Test 2026",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"

    sheets = ["133", "143", "153", "173", "183"]

    data_list = []

    for sheet in sheets:

        data = pd.read_excel(
            file_path,
            sheet_name=sheet
        )

        data["date"] = sheet

        data_list.append(data)

    data = pd.concat(
        data_list,
        ignore_index=True
    )

    data = data.drop(
        columns=[
            "Unnamed: 8",
            "Unnamed: 9"
        ],
        errors="ignore"
    )

    # Convert time columns
    for col in [
        "meal_start",
        "meal_end",
        "queue_start",
        "queue_end"
    ]:

        data[col] = pd.to_datetime(
            data[col].astype(str),
            format="%H:%M:%S",
            errors="coerce"
        )

    # Meal Duration
    data["meal_duration"] = (
        data["meal_end"]
        - data["meal_start"]
    ).dt.total_seconds() / 60

    # Waiting Time
    data["waiting_time"] = (
        data["queue_end"]
        - data["queue_start"]
    ).dt.total_seconds() / 60

    # Walk-away
    data["walk_away"] = (
        data["queue_start"].notna()
        & data["meal_start"].isna()
    )

    return data


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title(
    "Busy Buffet — Data Analytics Test 2026"
)

st.caption(
    "Presented by : Apirak Promdee"
)


# ============================================================
# TASK 1
# ============================================================

st.header("Task 1")

st.subheader(
    "In-house รอโต๊ะ / Walk-in รอนานจนเดินออก"
)

st.write(
    "ตรวจสอบว่า Guest Type มีความแตกต่างด้าน "
    "Waiting Time และ Walk-away หรือไม่"
)


# ----------------------------
# Waiting Time
# ----------------------------

waiting_summary = (

    df[
        df["waiting_time"].notna()
    ]

    .groupby("Guest_type")["waiting_time"]

    .agg(
        count="count",
        average="mean",
        median="median",
        maximum="max"
    )

    .round(2)
)


# ----------------------------
# Walk-away Rate
# ----------------------------

walkaway_rate = (

    df[
        df["waiting_time"].notna()
    ]

    .groupby("Guest_type")["walk_away"]

    .agg(
        waiting="count",
        walk_away="sum"
    )
)


walkaway_rate["rate"] = (

    walkaway_rate["walk_away"]
    /
    walkaway_rate["waiting"]
    *
    100

).round(2)


# ----------------------------
# Visual
# ----------------------------

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "### WAITING TIME"
    )

    st.bar_chart(
        waiting_summary["average"]
    )

    st.metric(
        "Walk-in Waiting Time",
        "38.4 min"
    )


with col2:

    st.markdown(
        "### WALK-AWAY RATE"
    )

    st.bar_chart(
        walkaway_rate["rate"]
    )

    st.metric(
        "In-house Walk-away Rate",
        "28.00%"
    )


# ----------------------------
# Analysis
# ----------------------------

st.markdown(
    "### หลังจากวิเคราะห์"
)

st.write(
    "WAITING TIME — Walk-in รอนานกว่า In-house +10.42 นาที"
)

st.write(
    "WALK-AWAY RATE — In-house สูงกว่า Walk-in"
)

st.write(
    "In-house 28.00% | Walk-in 14.58%"
)

st.write(
    "Walk-in รอนานกว่า แต่ไม่ได้ Walk-away มากกว่า"
)

st.info(
    "PARTIALLY SUPPORTED"
)


# ============================================================
# TASK 2
# ============================================================

st.header("Task 2")

st.subheader(
    "การวิเคราะห์ 3 แนวทางของโรงแรม"
)


# ============================================================
# ACTION 1
# ============================================================

st.markdown(
    "## 1. ลดเวลานั่ง 5 ชั่วโมงเป็นน้อยลง"
)


meal_summary = (

    df[
        df["meal_duration"].notna()
    ]

    .groupby("Guest_type")["meal_duration"]

    .agg(
        count="count",
        average="mean",
        median="median",
        maximum="max"
    )

    .round(2)
)


overall_meal = (

    df["meal_duration"]

    .dropna()

    .agg(
        count="count",
        average="mean",
        median="median",
        maximum="max"
    )

    .round(2)
)


st.write(
    f"Average Meal Duration = "
    f"{overall_meal['average']:.0f} นาที "
    f"ที่ Median = "
    f"{overall_meal['median']:.0f} นาที "
    f"และ Maximum = "
    f"{overall_meal['maximum']:.0f} นาที"
)


st.bar_chart(
    meal_summary["average"]
)


st.write(
    "ลูกค้าส่วนใหญ่ใช้เวลาไม่ถึง 5 ชั่วโมง "
    "การลดเวลานั่งอาจช่วยได้จำกัด "
    "เพราะลูกค้าส่วนใหญ่ไม่ได้ใช้เวลา 5 ชั่วโมงเต็ม"
)


# ============================================================
# ACTION 2
# ============================================================

st.markdown(
    "## 2. เพิ่มราคา Buffet เป็น 259 บาท"
)


daily_summary = (

    df

    .groupby("date")

    .agg(
        total_pax=("pax", "sum"),
        total_groups=("service_no.", "count")
    )
)


daily_summary["avg_pax_per_group"] = (

    daily_summary["total_pax"]
    /
    daily_summary["total_groups"]

).round(2)


st.write(
    "Demand อยู่ที่ 102–166 pax/day"
)


st.write(
    f"Average Demand = "
    f"{daily_summary['total_pax'].mean():.1f} pax/day"
)


st.bar_chart(
    daily_summary["total_pax"]
)


st.write(
    "แต่ไม่มีข้อมูลหลังขึ้นราคา "
    "จึงยังยืนยันไม่ได้ว่าการขึ้นราคาเป็น 259 บาท "
    "จะลด Demand ได้มากพอที่จะลด Queue"
)


# ============================================================
# ACTION 3
# ============================================================

st.markdown(
    "## 3. In-house ข้ามคิว"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "In-house Walk-away Rate",
        "28.00%"
    )

    st.metric(
        "Walk-in Walk-away Rate",
        "14.58%"
    )


with col2:

    st.metric(
        "In-house Avg. Waiting",
        "28.0 min"
    )

    st.metric(
        "Walk-in Avg. Waiting",
        "38.4 min"
    )


st.write(
    "In-house มี Walk-away Rate สูงกว่า "
    "จึงสะท้อนว่าเป็นกลุ่มที่ได้รับผลกระทบจากการรอ"
)


st.write(
    "แต่การข้ามคิวไม่ได้เพิ่มจำนวนโต๊ะหรือ Capacity ของร้าน"
)


# ----------------------------
# Task 2 Summary
# ----------------------------

st.markdown(
    "### สรุปการวิเคราะห์ 3 แนวทาง"
)


st.write(
    "ทั้ง 3 แนวทางสามารถช่วยแก้ปัญหาได้บางส่วน "
    "แต่ยังไม่มีแนวทางใดที่สามารถแก้ปัญหาได้อย่างสมบูรณ์"
)


# ============================================================
# TASK 3
# ============================================================

st.header("Task 3")


st.subheader(
    "Queue Skipping for In-house Guests"
)


# ============================================================
# WHY
# ============================================================

st.markdown(
    "### ทำไมเลือกแนวทางนี้?"
)


st.write(
    "In-house Walk-away Rate = 28.00%"
)


st.write(
    "สูงกว่า Walk-in ที่ 14.58%"
)


st.write(
    "In-house เป็นกลุ่มที่ควรให้ความสำคัญ "
    "เพราะมี Walk-away Rate สูงกว่า Walk-in"
)


st.write(
    "การ Skipping Queue มีโอกาสลดการ Walk-away "
    "ของ In-house และช่วยเพิ่ม Customer Experience"
)


st.write(
    "เป็นแนวทางที่สามารถทดลองใช้ได้ทันที "
    "โดยไม่ต้องลงทุนเพิ่มในโต๊ะหรืออุปกรณ์"
)


# ============================================================
# REASON
# ============================================================

st.markdown(
    "### เหตุผลสำคัญ"
)


st.write(
    "มองว่า In-house มีอัตรา Walk-away สูงกว่าเกือบ 2 เท่า "
    "จึงควรให้ความสำคัญกับกลุ่มนี้เป็นอันดับแรก"
)


# ============================================================
# EXPECTED IMPACT & KPI
# ============================================================

st.markdown(
    "### คาดหวังผลอะไรและวัดผลอย่างไร"
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "#### ผลลัพธ์ที่คาดหวัง"
    )

    st.write(
        "- ลด In-house Walk-away"
    )

    st.write(
        "- ลดเวลารอของ In-house"
    )


with col2:

    st.markdown(
        "#### KPI ที่ใช้ติดตาม"
    )

    st.write(
        "- In-house Walk-away 28.00%"
    )

    st.write(
        "- In-house รอเฉลี่ย 28.0 นาที"
    )

    st.write(
        "- Walk-in รอเฉลี่ย 38.4 นาที"
    )


# ============================================================
# MAIN GOAL
# ============================================================

st.markdown(
    "### เป้าหมายหลัก"
)


st.write(
    "ลด In-house Walk-away "
    "โดยไม่กระทบ Walk-in มากเกินไป"
)


# ============================================================
# RECOMMENDATION
# ============================================================

st.markdown(
    "### ข้อเสนอแนะ"
)


st.write(
    "แนะนำ Queue Skipping สำหรับลูกค้า In-house"
)


st.write(
    "In-house มี Walk-away สูงกว่า Walk-in"
)


st.write(
    "ลูกค้า In-house มี Waiting Time "
    "ที่ควรได้รับการปรับปรุง"
)


st.write(
    "Queue Skipping เป็นแนวทางที่ตรงกับปัญหา "
    "ที่พบจากข้อมูล"
)


# ============================================================
# IMPLEMENTATION
# ============================================================

st.markdown(
    "#### แนวทางดำเนินการ"
)


st.write(
    "ให้ลูกค้า In-house ได้รับสิทธิ์ข้ามคิวเมื่อมีโต๊ะว่าง "
    "เพื่อช่วยลดโอกาสที่ลูกค้าจะ Walk-away"
)


# ============================================================
# MONITORING
# ============================================================

st.markdown(
    "#### สิ่งที่ต้องติดตาม"
)


st.write(
    "หลังนำไปใช้ติดตาม In-house Walk-away "
    "และเวลารอ เพื่อประเมินผลของแนวทาง"
)


# ============================================================
# FINAL RECOMMENDATION
# ============================================================

st.markdown(
    "### สรุป"
)


st.write(
    "ใช้ Queue Skipping เป็นแนวทางทดลอง "
    "เพื่อแก้ปัญหา In-house Walk-away โดยตรง"
)
