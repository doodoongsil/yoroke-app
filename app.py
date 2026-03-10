import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="요로케", page_icon="💧", layout="wide")

DB_NAME = "records.db"
DAILY_WATER_GOAL = 8

food_db = {
    "물": {
        "level": "good",
        "title": "좋아요",
        "message": "물은 수분 섭취에 도움이 됩니다.",
        "tip": "하루 물 섭취를 꾸준히 유지하는 습관이 중요합니다."
    },
    "레몬물": {
        "level": "good",
        "title": "좋아요",
        "message": "레몬물은 수분 보충에 도움이 될 수 있습니다.",
        "tip": "너무 진하지 않게 가볍게 마시는 쪽이 편합니다."
    },
    "오이": {
        "level": "good",
        "title": "좋아요",
        "message": "수분이 많은 음식은 가볍게 도움을 줄 수 있습니다.",
        "tip": "과하게 먹기보다 균형 있게 드세요."
    },
    "수박": {
        "level": "good",
        "title": "좋아요",
        "message": "수분이 많은 과일은 도움이 될 수 있습니다.",
        "tip": "당 섭취도 함께 생각하며 적당히 드세요."
    },
    "사과": {
        "level": "normal",
        "title": "보통이에요",
        "message": "일반적인 과일로 테스트용 앱에서는 무난한 음식으로 봅니다.",
        "tip": "한 가지 음식보다 전체 식습관을 함께 보는 것이 좋습니다."
    },
    "바나나": {
        "level": "normal",
        "title": "보통이에요",
        "message": "테스트용 기준에서는 무난한 음식입니다.",
        "tip": "간식은 양 조절이 중요합니다."
    },
    "커피": {
        "level": "normal",
        "title": "보통이에요",
        "message": "너무 많이 마시지 않도록 주의해보세요.",
        "tip": "커피를 마셨다면 물도 함께 챙겨보세요."
    },
    "녹차": {
        "level": "normal",
        "title": "보통이에요",
        "message": "적당량은 괜찮지만, 물을 대신할 정도로만 마시지는 않는 편이 좋습니다.",
        "tip": "차를 마신 날에는 순수한 물 섭취도 함께 체크해보세요."
    },
    "우유": {
        "level": "normal",
        "title": "보통이에요",
        "message": "테스트용 기준에서는 무난한 음식으로 분류합니다.",
        "tip": "개인에 따라 소화나 식습관 차이가 있을 수 있습니다."
    },
    "요거트": {
        "level": "normal",
        "title": "보통이에요",
        "message": "테스트용 기준에서는 무난한 음식입니다.",
        "tip": "당이 많은 제품은 양을 조절해보세요."
    },
    "시금치": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 많이 먹는 습관은 점검이 필요할 수 있습니다.",
        "tip": "한 가지 음식에 치우치지 않도록 균형을 맞춰보세요."
    },
    "견과류": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "건강 간식일 수 있지만 많이 먹는 습관은 점검이 필요할 수 있습니다.",
        "tip": "소량씩 나누어 먹는 방식이 좋습니다."
    },
    "초콜릿": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 많이 먹는 습관은 점검이 필요할 수 있습니다.",
        "tip": "간식은 횟수와 양을 함께 줄여보는 것이 좋습니다."
    },
    "탄산음료": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 많이 마시는 습관은 점검이 필요할 수 있습니다.",
        "tip": "탄산음료 대신 물이나 무가당 음료를 늘려보세요."
    },
    "맥주": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "테스트용 앱에서는 자주 마시는 습관을 주의 대상으로 봅니다.",
        "tip": "음주 뒤에는 물 섭취를 더 신경 써보세요."
    },
    "라면": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 음식 위주의 습관은 점검이 필요할 수 있습니다.",
        "tip": "국물 섭취를 줄이고 물 섭취를 늘려보세요."
    },
    "짠 음식": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 음식 위주의 습관은 점검이 필요할 수 있습니다.",
        "tip": "한 번에 줄이기보다 빈도를 줄여보세요."
    }
}

food_alias = {
    "생수": "물",
    "정수물": "물",
    "미네랄워터": "물",
    "레몬 워터": "레몬물",
    "아메리카노": "커피",
    "카페라떼": "커피",
    "라떼": "커피",
    "에스프레소": "커피",
    "콜드브루": "커피",
    "홍차": "녹차",
    "보리차": "물",
    "옥수수수염차": "물",
    "탄산수": "탄산음료",
    "콜라": "탄산음료",
    "사이다": "탄산음료",
    "환타": "탄산음료",
    "제로콜라": "탄산음료",
    "제로사이다": "탄산음료",
    "소주": "맥주",
    "와인": "맥주",
    "막걸리": "맥주",
    "위스키": "맥주",
    "브랜디": "맥주",
    "아몬드": "견과류",
    "호두": "견과류",
    "캐슈넛": "견과류",
    "땅콩": "견과류",
    "피스타치오": "견과류",
    "초코": "초콜릿",
    "초코과자": "초콜릿",
    "초코바": "초콜릿",
    "초코렛": "초콜릿",
    "국밥": "짠 음식",
    "찌개": "짠 음식",
    "짬뽕": "짠 음식",
    "국물요리": "짠 음식",
    "국물음식": "짠 음식",
    "우동": "짠 음식",
    "김치찌개": "짠 음식",
    "된장찌개": "짠 음식",
    "라면국물": "짠 음식",
    "시래기국": "짠 음식",
    "라면땅": "라면",
    "신라면": "라면",
    "너구리": "라면"
}


def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            기록시각 TEXT,
            물섭취컵 INTEGER,
            통증여부 TEXT,
            소변상태 TEXT,
            소변횟수 INTEGER,
            땀배출 TEXT,
            짠음식섭취 TEXT,
            메모 TEXT
        )
    """)
    conn.commit()
    conn.close()


def load_data():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM records ORDER BY 기록시각 DESC", conn)
    conn.close()

    if len(df) == 0:
        return pd.DataFrame(columns=[
            "id", "기록시각", "물섭취컵", "통증여부", "소변상태",
            "소변횟수", "땀배출", "짠음식섭취", "메모"
        ])
    return df


def insert_record(record_time, water, pain, urine, urine_count, sweat, salty_food, memo):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO records (
            기록시각, 물섭취컵, 통증여부, 소변상태,
            소변횟수, 땀배출, 짠음식섭취, 메모
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (record_time, water, pain, urine, urine_count, sweat, salty_food, memo))
    conn.commit()
    conn.close()


def update_record(record_id, water, pain, urine, urine_count, sweat, salty_food, memo):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE records
        SET 물섭취컵 = ?, 통증여부 = ?, 소변상태 = ?, 소변횟수 = ?,
            땀배출 = ?, 짠음식섭취 = ?, 메모 = ?
        WHERE id = ?
    """, (water, pain, urine, urine_count, sweat, salty_food, memo, record_id))
    conn.commit()
    conn.close()


def delete_record(record_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")


def has_today_record(df):
    if len(df) == 0:
        return False
    record_dates = df["기록시각"].astype(str).str[:10]
    return get_today_string() in record_dates.values


def get_latest_records(df, count=5):
    return df.head(count)


def get_recent_water_chart_data(df, count=7):
    if len(df) == 0:
        return pd.DataFrame()

    chart_df = df.head(count).copy()
    chart_df = chart_df.iloc[::-1].reset_index(drop=True)
    chart_df["표시날짜"] = pd.to_datetime(chart_df["기록시각"], errors="coerce").dt.strftime("%m-%d %H:%M")
    chart_df["표시날짜"] = chart_df["표시날짜"].fillna("날짜없음")
    chart_df["물섭취컵"] = pd.to_numeric(chart_df["물섭취컵"], errors="coerce").fillna(0)

    return chart_df[["표시날짜", "물섭취컵"]].set_index("표시날짜")


def get_pain_chart_data(df):
    if len(df) == 0:
        return pd.DataFrame()

    pain_order = ["없음", "조금 있음", "심함"]
    pain_counts = df["통증여부"].astype(str).value_counts()

    rows = []
    for pain in pain_order:
        rows.append({"통증여부": pain, "횟수": int(pain_counts.get(pain, 0))})

    return pd.DataFrame(rows).set_index("통증여부")


def get_today_latest_record(df):
    if len(df) == 0:
        return None

    df_copy = df.copy()
    df_copy["날짜"] = df_copy["기록시각"].astype(str).str[:10]
    today_df = df_copy[df_copy["날짜"] == get_today_string()].copy()

    if len(today_df) == 0:
        return None

    today_df["정렬용시각"] = pd.to_datetime(today_df["기록시각"], errors="coerce")
    today_df = today_df.sort_values(by="정렬용시각", ascending=False)

    return today_df.iloc[0]


def normalize_food_name(food_input):
    text = str(food_input).strip()
    if text == "":
        return "", "", False

    compact = text.replace(" ", "")

    if text in food_db:
        return text, text, False

    if text in food_alias:
        return food_alias[text], text, True

    if compact in food_db:
        return compact, text, False

    if compact in food_alias:
        return food_alias[compact], text, True

    for alias, canonical in food_alias.items():
        if alias in text or alias in compact:
            return canonical, text, True

    for canonical in food_db.keys():
        if canonical in text or canonical in compact:
            return canonical, text, False

    return "", text, False


def show_menu_flash(menu_name):
    flash_menu = st.session_state.get("flash_menu")
    flash_message = st.session_state.get("flash_message")
    flash_level = st.session_state.get("flash_level", "success")

    if flash_menu == menu_name and flash_message:
        if flash_level == "success":
            st.success(flash_message)
        elif flash_level == "warning":
            st.warning(flash_message)
        elif flash_level == "error":
            st.error(flash_message)
        else:
            st.info(flash_message)

        st.session_state.flash_menu = None
        st.session_state.flash_message = None
        st.session_state.flash_level = "success"


init_db()
df_all = load_data()
today_done = has_today_record(df_all)
today_record = get_today_latest_record(df_all)

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "flash_menu" not in st.session_state:
    st.session_state.flash_menu = None

if "flash_message" not in st.session_state:
    st.session_state.flash_message = None

if "flash_level" not in st.session_state:
    st.session_state.flash_level = "success"

st.title("요로케 테스트 앱")
st.write("신장결석·요로결석 예방을 위한 테스트용 앱입니다.")
st.write("아직은 작은 기능만 넣은 첫 버전입니다.")

menu = st.radio(
    "원하는 메뉴를 선택하세요",
    ["홈", "오늘 체크", "음식 확인", "기록 보기"]
)

if menu == "홈":
    st.subheader("홈")
    show_menu_flash("홈")

    st.write("요로케에 오신 것을 환영합니다.")
    st.write("이 앱은 생활 습관을 간단히 기록하고 확인해보는 테스트용 버전입니다.")

    if today_done:
        st.success("오늘 기록을 이미 완료했습니다.")
    else:
        st.warning("오늘 기록이 아직 없습니다. 오늘 체크 메뉴에서 기록해보세요.")

    total_count = len(df_all)

    if len(df_all) > 0:
        recent_df = get_latest_records(df_all, count=min(7, len(df_all)))
        avg_water = pd.to_numeric(recent_df["물섭취컵"], errors="coerce").fillna(0).mean()
        avg_water_text = f"{avg_water:.1f}컵"
    else:
        avg_water_text = "0컵"

    col1, col2, col3 = st.columns(3)
    col1.metric("총 기록 수", f"{total_count}개")
    col2.metric("오늘 기록 여부", "완료" if today_done else "미완료")
    col3.metric("최근 평균 물 섭취", avg_water_text)

    st.write("### 오늘 요약")
    if today_record is not None:
        today_water = pd.to_numeric(today_record["물섭취컵"], errors="coerce")
        if pd.isna(today_water):
            today_water = 0

        today_urine_count = pd.to_numeric(today_record["소변횟수"], errors="coerce")
        if pd.isna(today_urine_count):
            today_urine_count = 0

        today_salty = str(today_record["짠음식섭취"])
        today_pain = str(today_record["통증여부"])

        tcol1, tcol2, tcol3, tcol4 = st.columns(4)
        tcol1.metric("오늘 물 섭취", f"{int(today_water)}컵")
        tcol2.metric("오늘 소변 횟수", f"{int(today_urine_count)}회")
        tcol3.metric("오늘 짠 음식", today_salty)
        tcol4.metric("오늘 통증", today_pain)

        today_summary_df = pd.DataFrame([today_record]).drop(columns=["날짜", "정렬용시각"], errors="ignore")
        st.dataframe(today_summary_df, use_container_width=True)
    else:
        st.info("오늘 기록이 아직 없어 오늘 요약 카드가 비어 있습니다. 오늘 체크에서 먼저 기록해보세요.")

elif menu == "오늘 체크":
    st.subheader("오늘 체크")
    show_menu_flash("오늘 체크")

    if today_done:
        st.success("오늘은 이미 기록이 있습니다. 추가로 저장하면 오늘 기록이 하나 더 쌓입니다.")
    else:
        st.info("오늘 기록이 아직 없습니다. 아래 내용을 입력해 저장해보세요.")

    water = st.number_input("오늘 물을 몇 컵 마셨나요?", min_value=0, max_value=30, value=0)
    progress_ratio = min(water / DAILY_WATER_GOAL, 1.0)
    remaining_water = max(DAILY_WATER_GOAL - water, 0)

    st.write(f"오늘 물 목표: {DAILY_WATER_GOAL}컵")
    st.progress(progress_ratio)

    if water < DAILY_WATER_GOAL:
        st.info(f"현재 {water}컵 마셨습니다. 목표까지 {remaining_water}컵 남았습니다.")
    elif water == DAILY_WATER_GOAL:
        st.success("오늘 물 목표 8컵을 딱 채웠습니다.")
    else:
        st.success(f"오늘 물 목표를 달성했습니다. 목표보다 {water - DAILY_WATER_GOAL}컵 더 마셨습니다.")

    pain = st.radio("오늘 통증이 있었나요?", ["없음", "조금 있음", "심함"])
    urine = st.selectbox("오늘 소변 상태는 어땠나요?", ["맑음", "보통", "진함", "잘 모르겠음"])
    urine_count = st.number_input("오늘 소변은 몇 번 정도 봤나요?", min_value=0, max_value=30, value=0, step=1)
    sweat = st.radio("오늘 땀 배출은 어땠나요?", ["적음", "보통", "많음"])
    salty_food = st.radio("오늘 짠 음식을 먹었나요?", ["아니오", "조금", "예"])
    memo = st.text_area("메모가 있으면 적어주세요", placeholder="예: 커피를 많이 마셨음, 운동을 했음")

    if st.button("오늘 기록 저장"):
        insert_record(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            water, pain, urine, urine_count, sweat, salty_food, memo
        )
        st.session_state.flash_menu = "오늘 체크"
        st.session_state.flash_message = "기록이 SQLite DB에 저장되었습니다."
        st.session_state.flash_level = "success"
        st.rerun()

elif menu == "음식 확인":
    st.subheader("음식 확인")
    show_menu_flash("음식 확인")

    st.write("음식 이름을 입력하면 테스트용 기준으로 간단한 안내를 보여줍니다.")
    st.write("이제 비슷한 음식 이름도 어느 정도 알아듣습니다.")

    food = st.text_input("음식 이름을 입력하세요", placeholder="예: 아메리카노, 콜라, 소주, 국밥")

    if food:
        canonical_food, original_food, matched_by_alias = normalize_food_name(food)

        if canonical_food in food_db:
            result = food_db[canonical_food]

            if matched_by_alias:
                st.info(f"입력한 '{original_food}'를(을) '{canonical_food}' 기준으로 안내합니다.")

            if result["level"] == "good":
                st.success(f"{result['title']}: {result['message']}")
            elif result["level"] == "normal":
                st.warning(f"{result['title']}: {result['message']}")
            else:
                st.error(f"{result['title']}: {result['message']}")

            st.write(f"한 줄 팁: {result['tip']}")
        else:
            st.info("아직 등록되지 않은 음식입니다.")

elif menu == "기록 보기":
    st.subheader("기록 보기")
    show_menu_flash("기록 보기")

    if len(df_all) > 0:
        st.dataframe(df_all, use_container_width=True)

        st.write("### 기록 그래프")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("최근 물 섭취량")
            water_chart_df = get_recent_water_chart_data(df_all, count=7)
            if len(water_chart_df) > 0:
                st.bar_chart(water_chart_df)

        with chart_col2:
            st.write("통증 여부 요약")
            pain_chart_df = get_pain_chart_data(df_all)
            if len(pain_chart_df) > 0:
                st.bar_chart(pain_chart_df)

        st.write("### 기록 수정")
        edit_id = st.number_input(
            "수정할 id를 입력하세요",
            min_value=1,
            max_value=int(df_all["id"].max()),
            value=1,
            step=1
        )

        if st.button("선택한 기록 불러오기"):
            st.session_state.edit_mode = True
            st.session_state.edit_id = int(edit_id)
            st.rerun()

        if st.session_state.edit_mode and st.session_state.edit_id is not None:
            selected_rows = df_all[df_all["id"] == st.session_state.edit_id]

            if len(selected_rows) > 0:
                selected_row = selected_rows.iloc[0]

                current_water = pd.to_numeric(selected_row["물섭취컵"], errors="coerce")
                if pd.isna(current_water):
                    current_water = 0

                current_urine_count = pd.to_numeric(selected_row["소변횟수"], errors="coerce")
                if pd.isna(current_urine_count):
                    current_urine_count = 0

                pain_options = ["없음", "조금 있음", "심함"]
                urine_options = ["맑음", "보통", "진함", "잘 모르겠음"]
                sweat_options = ["적음", "보통", "많음"]
                salty_options = ["아니오", "조금", "예"]

                edit_water = st.number_input("수정할 물 섭취량(컵)", min_value=0, max_value=30, value=int(current_water))
                edit_pain = st.radio("수정할 통증 여부", pain_options, index=pain_options.index(str(selected_row["통증여부"])) if str(selected_row["통증여부"]) in pain_options else 0)
                edit_urine = st.selectbox("수정할 소변 상태", urine_options, index=urine_options.index(str(selected_row["소변상태"])) if str(selected_row["소변상태"]) in urine_options else 0)
                edit_urine_count = st.number_input("수정할 소변 횟수", min_value=0, max_value=30, value=int(current_urine_count))
                edit_sweat = st.radio("수정할 땀 배출", sweat_options, index=sweat_options.index(str(selected_row["땀배출"])) if str(selected_row["땀배출"]) in sweat_options else 1)
                edit_salty = st.radio("수정할 짠 음식 섭취", salty_options, index=salty_options.index(str(selected_row["짠음식섭취"])) if str(selected_row["짠음식섭취"]) in salty_options else 0)
                edit_memo = st.text_area("수정할 메모", value="" if str(selected_row["메모"]) == "nan" else str(selected_row["메모"]))

                if st.button("수정 내용 저장"):
                    update_record(st.session_state.edit_id, edit_water, edit_pain, edit_urine, edit_urine_count, edit_sweat, edit_salty, edit_memo)
                    st.session_state.edit_mode = False
                    st.session_state.flash_menu = "기록 보기"
                    st.session_state.flash_message = "기록이 수정되었습니다."
                    st.session_state.flash_level = "success"
                    st.rerun()

                if st.button("수정 취소"):
                    st.session_state.edit_mode = False
                    st.rerun()

        st.write("### 기록 삭제")
        delete_id = st.number_input(
            "삭제할 id를 입력하세요",
            min_value=1,
            max_value=int(df_all["id"].max()),
            value=1,
            step=1
        )

        if st.button("선택한 기록 삭제"):
            delete_record(int(delete_id))
            st.session_state.edit_mode = False
            st.session_state.flash_menu = "기록 보기"
            st.session_state.flash_message = "선택한 기록이 삭제되었습니다."
            st.session_state.flash_level = "success"
            st.rerun()
    else:
        st.info("아직 저장된 기록이 없습니다. 먼저 오늘 체크에서 기록해보세요.")
