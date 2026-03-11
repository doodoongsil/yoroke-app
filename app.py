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
    "배": {
        "level": "good",
        "title": "좋아요",
        "message": "수분감 있는 과일로 무난한 편입니다.",
        "tip": "과일만 믿기보다 물도 함께 챙겨보세요."
    },
    "귤": {
        "level": "good",
        "title": "좋아요",
        "message": "가볍게 먹기 좋은 과일입니다.",
        "tip": "간식처럼 적당량 드세요."
    },
    "오렌지": {
        "level": "good",
        "title": "좋아요",
        "message": "무난한 과일로 볼 수 있습니다.",
        "tip": "주스보다 과일 자체로 먹는 편이 더 좋습니다."
    },
    "샐러드": {
        "level": "good",
        "title": "좋아요",
        "message": "가볍게 먹기 좋은 선택입니다.",
        "tip": "드레싱이 너무 짜지 않으면 더 좋습니다."
    },
    "죽": {
        "level": "good",
        "title": "좋아요",
        "message": "상대적으로 부담이 적은 식사로 볼 수 있습니다.",
        "tip": "간을 너무 세게 하지 않는 편이 좋습니다."
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
    "보리차": {
        "level": "normal",
        "title": "보통이에요",
        "message": "가볍게 마실 수 있지만 기본은 물 중심이 좋습니다.",
        "tip": "차를 마셔도 물 섭취를 따로 챙겨보세요."
    },
    "옥수수수염차": {
        "level": "normal",
        "title": "보통이에요",
        "message": "가볍게 마실 수 있지만 물을 대신하는 개념보다는 보조 음료에 가깝습니다.",
        "tip": "기본 수분 보충은 물 중심으로 해보세요."
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
    "두유": {
        "level": "normal",
        "title": "보통이에요",
        "message": "무난하게 마실 수 있지만 물을 대신하는 용도는 아닙니다.",
        "tip": "달지 않은 제품이면 더 무난합니다."
    },
    "비빔밥": {
        "level": "normal",
        "title": "보통이에요",
        "message": "전체적으로는 무난하지만 양념이 강하면 아쉬울 수 있습니다.",
        "tip": "고추장 양을 조금 줄여보세요."
    },
    "김밥": {
        "level": "normal",
        "title": "보통이에요",
        "message": "간편식으로는 무난하지만 속재료 간이 센 경우가 있습니다.",
        "tip": "국물 음식과 함께 먹는 습관은 줄여보세요."
    },
    "순두부찌개": {
        "level": "normal",
        "title": "보통이에요",
        "message": "찌개류 중에서는 비교적 무난하지만 국물 간은 체크가 필요합니다.",
        "tip": "국물을 많이 먹지 않는 편이 좋습니다."
    },
    "설렁탕": {
        "level": "normal",
        "title": "보통이에요",
        "message": "추가 간을 많이 하지 않으면 무난할 수 있습니다.",
        "tip": "소금이나 깍두기 국물은 줄여보세요."
    },
    "곰탕": {
        "level": "normal",
        "title": "보통이에요",
        "message": "먹을 수는 있지만 국물과 추가 간이 중요합니다.",
        "tip": "국물을 전부 마시지 않는 쪽이 좋습니다."
    },
    "삼계탕": {
        "level": "normal",
        "title": "보통이에요",
        "message": "무난한 편이지만 국물 간과 함께 먹는 반찬에 따라 달라질 수 있습니다.",
        "tip": "소금 추가를 줄여보세요."
    },
    "치킨": {
        "level": "normal",
        "title": "보통이에요",
        "message": "가끔 먹는 것은 괜찮지만 자주 반복되면 아쉬울 수 있습니다.",
        "tip": "짠 양념과 함께 먹는 횟수를 줄여보세요."
    },
    "순대": {
        "level": "normal",
        "title": "보통이에요",
        "message": "먹을 수는 있지만 소금과 국물이 같이 들어가면 부담이 될 수 있습니다.",
        "tip": "곁들임 소금은 적게 드세요."
    },
    "튀김": {
        "level": "normal",
        "title": "보통이에요",
        "message": "가끔은 괜찮지만 자주 반복되면 생활관리에는 아쉬울 수 있습니다.",
        "tip": "짠 양념과 함께 먹는 습관은 줄여보세요."
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
    "에너지음료": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 마시는 습관은 생활관리 측면에서 아쉬울 수 있습니다.",
        "tip": "피곤할수록 음료보다 물과 휴식을 먼저 챙겨보세요."
    },
    "주스": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "과일주스도 물을 대신하는 음료로 보기에는 아쉬울 수 있습니다.",
        "tip": "주스를 마셨다면 물도 따로 챙겨보세요."
    },
    "맥주": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "테스트용 앱에서는 자주 마시는 습관을 주의 대상으로 봅니다.",
        "tip": "음주 뒤에는 물 섭취를 더 신경 써보세요."
    },
    "소주": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "음주류는 물을 대신할 수 없고 자주 마시는 습관은 점검이 필요합니다.",
        "tip": "마신 날에는 물을 평소보다 더 챙겨보세요."
    },
    "와인": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "술은 생활관리 측면에서 자주 마시지 않는 편이 좋습니다.",
        "tip": "술자리 전후에 물을 충분히 마셔보세요."
    },
    "막걸리": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 마시는 습관은 점검이 필요할 수 있습니다.",
        "tip": "술을 마신 날은 수분 보충을 더 신경 써보세요."
    },
    "위스키": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "음주 습관은 생활관리 측면에서 주의가 필요합니다.",
        "tip": "마신 뒤에는 물을 충분히 보충해보세요."
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
    },
    "국밥": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "국물과 간이 강한 편이라 자주 먹는 습관은 점검이 필요할 수 있습니다.",
        "tip": "국물을 줄이고 물을 따로 챙겨보세요."
    },
    "찌개": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "찌개류는 국물과 나트륨 때문에 주의가 필요할 수 있습니다.",
        "tip": "건더기 위주로 먹고 국물은 줄여보세요."
    },
    "짬뽕": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 국물과 자극적인 구성으로 자주 먹는 습관은 아쉬울 수 있습니다.",
        "tip": "국물 섭취를 줄이는 쪽이 좋습니다."
    },
    "우동": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "면보다 국물 간이 문제될 수 있어 주의가 필요합니다.",
        "tip": "국물을 적게 먹는 편이 좋습니다."
    },
    "해장국": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "국물 간이 센 편이라 자주 먹는 습관은 점검이 필요할 수 있습니다.",
        "tip": "국물은 남기는 방향으로 드셔보세요."
    },
    "김치찌개": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 국물류에 해당할 수 있어 주의가 필요합니다.",
        "tip": "국물과 함께 먹는 반찬 양도 조절해보세요."
    },
    "된장찌개": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "자주 먹는 국물 습관은 점검이 필요할 수 있습니다.",
        "tip": "국물 섭취를 줄여보세요."
    },
    "라면국물": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "라면국물은 짠 음식 습관으로 보기 쉽습니다.",
        "tip": "국물은 가능한 줄여보세요."
    },
    "시래기국": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "국물 간이 강한 경우가 있어 자주 먹는 습관은 점검이 필요합니다.",
        "tip": "간을 약하게 하고 국물 양을 조절해보세요."
    },
    "김치": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "반찬으로 자주 먹기 쉬워 나트륨 섭취가 늘 수 있습니다.",
        "tip": "양을 조금만 줄여도 도움이 될 수 있습니다."
    },
    "장아찌": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 반찬 계열이라 자주 먹는 습관은 점검이 필요합니다.",
        "tip": "조금만 곁들이는 편이 좋습니다."
    },
    "젓갈": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 반찬으로 볼 수 있어 주의가 필요합니다.",
        "tip": "식사 때 양을 줄여보세요."
    },
    "햄": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "가공식품 성격이 강해 자주 먹는 습관은 아쉬울 수 있습니다.",
        "tip": "반찬을 바꿀 수 있으면 더 좋습니다."
    },
    "소시지": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "가공육 계열이라 자주 반복되면 아쉬울 수 있습니다.",
        "tip": "횟수를 조금 줄여보세요."
    },
    "베이컨": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 편이고 가공식품 계열이라 주의가 필요합니다.",
        "tip": "소량만 드시는 쪽이 좋습니다."
    },
    "양념치킨": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠맛과 단맛이 강한 편이라 자주 먹는 습관은 아쉬울 수 있습니다.",
        "tip": "먹는 날에는 물 섭취를 더 챙겨보세요."
    },
    "피자": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 편이고 가공 재료가 겹치는 경우가 많습니다.",
        "tip": "자주 반복되지 않도록 조절해보세요."
    },
    "햄버거": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠맛과 가공식품 조합이라 주의가 필요할 수 있습니다.",
        "tip": "세트 음료 대신 물을 고르는 것도 방법입니다."
    },
    "떡볶이": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "맵고 짠 양념이 겹칠 수 있어 자주 먹는 것은 아쉬울 수 있습니다.",
        "tip": "국물이나 소스는 줄여보세요."
    },
    "과자": {
        "level": "care",
        "title": "주의가 필요해요",
        "message": "짠 과자나 가공 간식은 자주 먹을수록 생활관리에 아쉬울 수 있습니다.",
        "tip": "한 봉지를 다 먹기보다 양을 나눠보세요."
    }
}

food_alias = {
    "생수": "물",
    "정수물": "물",
    "미네랄워터": "물",
    "생물": "물",

    "레몬 워터": "레몬물",
    "레몬워터": "레몬물",

    "아메리카노": "커피",
    "아아": "커피",
    "아이스아메리카노": "커피",
    "뜨아": "커피",
    "카페라떼": "커피",
    "라떼": "커피",
    "에스프레소": "커피",
    "콜드브루": "커피",
    "바닐라라떼": "커피",
    "카페모카": "커피",

    "홍차": "녹차",
    "허브차": "녹차",

    "보리물": "보리차",
    "옥수수차": "옥수수수염차",
    "수염차": "옥수수수염차",

    "탄산수": "탄산음료",
    "콜라": "탄산음료",
    "사이다": "탄산음료",
    "환타": "탄산음료",
    "제로콜라": "탄산음료",
    "제로사이다": "탄산음료",
    "탄산": "탄산음료",

    "레드불": "에너지음료",
    "핫식스": "에너지음료",
    "몬스터": "에너지음료",
    "에너지드링크": "에너지음료",

    "오렌지주스": "주스",
    "사과주스": "주스",
    "포도주스": "주스",
    "과일주스": "주스",

    "플레인요거트": "요거트",
    "그릭요거트": "요거트",

    "검은콩두유": "두유",
    "무가당두유": "두유",

    "소주": "소주",
    "와인": "와인",
    "막걸리": "막걸리",
    "위스키": "위스키",
    "브랜디": "위스키",
    "하이볼": "위스키",
    "맥주": "맥주",

    "아몬드": "견과류",
    "호두": "견과류",
    "캐슈넛": "견과류",
    "땅콩": "견과류",
    "피스타치오": "견과류",
    "잣": "견과류",
    "마카다미아": "견과류",

    "초코": "초콜릿",
    "초코과자": "초콜릿",
    "초코바": "초콜릿",
    "초코렛": "초콜릿",

    "국밥": "국밥",
    "돼지국밥": "국밥",
    "순대국밥": "국밥",
    "소머리국밥": "국밥",

    "찌개": "찌개",
    "짬뽕": "짬뽕",
    "국물요리": "짠 음식",
    "국물음식": "짠 음식",
    "국": "짠 음식",
    "탕": "짠 음식",

    "우동": "우동",
    "해장국": "해장국",
    "선지해장국": "해장국",
    "뼈해장국": "해장국",

    "김치찌개": "김치찌개",
    "된장찌개": "된장찌개",
    "순두부": "순두부찌개",
    "순두부찌개": "순두부찌개",
    "설렁탕": "설렁탕",
    "곰탕": "곰탕",
    "삼계탕": "삼계탕",
    "시래기국": "시래기국",

    "라면국물": "라면국물",
    "컵라면": "라면",
    "봉지라면": "라면",
    "라면땅": "라면",
    "신라면": "라면",
    "너구리": "라면",
    "짜파게티": "라면",
    "불닭볶음면": "라면",

    "김치": "김치",
    "장아찌": "장아찌",
    "오이지": "장아찌",
    "젓갈": "젓갈",
    "명란젓": "젓갈",
    "새우젓": "젓갈",

    "햄": "햄",
    "소세지": "소시지",
    "소시지": "소시지",
    "베이컨": "베이컨",

    "후라이드치킨": "치킨",
    "프라이드치킨": "치킨",
    "양념치킨": "양념치킨",
    "피자": "피자",
    "햄버거": "햄버거",
    "버거": "햄버거",
    "떡볶이": "떡볶이",
    "순대": "순대",
    "튀김": "튀김",
    "김말이": "튀김",
    "오징어튀김": "튀김",

    "새우깡": "과자",
    "감자칩": "과자",
    "포카칩": "과자",
    "과자": "과자",

    "오렌지": "오렌지",
    "귤": "귤",
    "배": "배",
    "샐러드": "샐러드",
    "비빔밥": "비빔밥",
    "김밥": "김밥",
    "야채죽": "죽",
    "전복죽": "죽",
    "죽": "죽"
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


def update_today_record(water, pain, urine, urine_count, sweat, salty_food, memo):
    conn = get_conn()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT id
        FROM records
        WHERE substr(기록시각, 1, 10) = ?
        ORDER BY 기록시각 DESC
        LIMIT 1
    """, (today,))
    row = cursor.fetchone()

    if row is not None:
        record_id = row[0]
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

def insert_sample_records():
    conn = get_conn()
    cursor = conn.cursor()

    sample_rows = [
        ("2026-03-03 08:30:00", 8, "없음", "맑음", 6, "적음", "아니오", "샘플 기록 1"),
        ("2026-03-04 09:10:00", 7, "없음", "보통", 5, "보통", "조금", "샘플 기록 2"),
        ("2026-03-05 08:45:00", 5, "조금 있음", "진함", 3, "많음", "예", "샘플 기록 3"),
        ("2026-03-06 07:50:00", 9, "없음", "맑음", 7, "보통", "아니오", "샘플 기록 4"),
        ("2026-03-07 10:20:00", 6, "없음", "보통", 4, "적음", "조금", "샘플 기록 5"),
        ("2026-03-08 08:05:00", 4, "조금 있음", "진함", 3, "많음", "예", "샘플 기록 6"),
        ("2026-03-09 09:00:00", 8, "없음", "맑음", 6, "보통", "아니오", "샘플 기록 7"),
        ("2026-03-10 08:40:00", 7, "없음", "보통", 5, "적음", "조금", "샘플 기록 8"),
    ]

    for row in sample_rows:
        cursor.execute("""
            INSERT INTO records (
                기록시각, 물섭취컵, 통증여부, 소변상태,
                소변횟수, 땀배출, 짠음식섭취, 메모
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

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


def get_urine_count_chart_data(df, count=7):
    if len(df) == 0:
        return pd.DataFrame()

    chart_df = df.head(count).copy()
    chart_df = chart_df.iloc[::-1].reset_index(drop=True)
    chart_df["표시날짜"] = pd.to_datetime(chart_df["기록시각"], errors="coerce").dt.strftime("%m-%d %H:%M")
    chart_df["표시날짜"] = chart_df["표시날짜"].fillna("날짜없음")
    chart_df["소변횟수"] = pd.to_numeric(chart_df["소변횟수"], errors="coerce").fillna(0)

    return chart_df[["표시날짜", "소변횟수"]].set_index("표시날짜")


def get_salty_chart_data(df):
    if len(df) == 0:
        return pd.DataFrame()

    order = ["아니오", "조금", "예"]
    counts = df["짠음식섭취"].astype(str).value_counts()

    rows = []
    for item in order:
        rows.append({"짠음식섭취": item, "횟수": int(counts.get(item, 0))})

    return pd.DataFrame(rows).set_index("짠음식섭취")


def get_sweat_chart_data(df):
    if len(df) == 0:
        return pd.DataFrame()

    order = ["적음", "보통", "많음"]
    counts = df["땀배출"].astype(str).value_counts()

    rows = []
    for item in order:
        rows.append({"땀배출": item, "횟수": int(counts.get(item, 0))})

    return pd.DataFrame(rows).set_index("땀배출")


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


def get_recent_7day_summary(df):
    if len(df) == 0:
        return {
            "기록일수": 0,
            "평균물섭취": 0,
            "통증기록수": 0,
            "짠음식기록수": 0
        }

    temp = df.copy()
    temp["기록시각_dt"] = pd.to_datetime(temp["기록시각"], errors="coerce")
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
    recent_df = temp[temp["기록시각_dt"] >= cutoff].copy()

    if len(recent_df) == 0:
        return {
            "기록일수": 0,
            "평균물섭취": 0,
            "통증기록수": 0,
            "짠음식기록수": 0
        }

    recent_df["날짜"] = recent_df["기록시각_dt"].dt.strftime("%Y-%m-%d")

    avg_water = pd.to_numeric(recent_df["물섭취컵"], errors="coerce").fillna(0).mean()
    pain_count = (recent_df["통증여부"].astype(str) != "없음").sum()
    salty_count = (recent_df["짠음식섭취"].astype(str) != "아니오").sum()

    return {
        "기록일수": int(recent_df["날짜"].nunique()),
        "평균물섭취": round(avg_water, 1),
        "통증기록수": int(pain_count),
        "짠음식기록수": int(salty_count)
    }


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


def draw_box(label, value):
    st.markdown(
        f"""
        <div style="
            border:1px solid #d9e2f1;
            border-radius:16px;
            padding:16px 18px;
            background-color:#f8fbff;
            min-height:96px;
            box-shadow:0 1px 4px rgba(0,0,0,0.04);
            margin-bottom:8px;
        ">
            <div style="
                font-size:14px;
                color:#5b6575;
                margin-bottom:8px;
            ">{label}</div>
            <div style="
                font-size:26px;
                font-weight:700;
                color:#16324f;
            ">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_section_box(title):
    st.markdown(
        f"""
        <div style="
            font-size:22px;
            font-weight:800;
            color:#183b56;
            margin-top:6px;
            margin-bottom:10px;
        ">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_helper_text(text):
    st.markdown(
        f"""
        <div style="
            font-size:14px;
            color:#7a8798;
            line-height:1.6;
            margin-top:2px;
            margin-bottom:14px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def draw_info_card(title, body):
    st.markdown(
        f"""
        <div style="
            border:1px solid #d9e2f1;
            border-radius:16px;
            padding:18px;
            background-color:#f8fbff;
            box-shadow:0 1px 4px rgba(0,0,0,0.04);
            margin-top:10px;
        ">
            <div style="
                font-size:20px;
                font-weight:700;
                color:#16324f;
                margin-bottom:10px;
            ">{title}</div>
            <div style="
                font-size:15px;
                color:#334155;
                line-height:1.7;
                white-space:pre-line;
            ">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_food_result_box(title, message, tip):
    st.markdown(
        f"""
        <div style="
            border:1px solid #d9e2f1;
            border-radius:16px;
            padding:18px;
            background-color:#f8fbff;
            box-shadow:0 1px 4px rgba(0,0,0,0.04);
            margin-top:10px;
        ">
            <div style="
                font-size:20px;
                font-weight:700;
                color:#16324f;
                margin-bottom:10px;
            ">{title}</div>
            <div style="
                font-size:15px;
                color:#334155;
                margin-bottom:8px;
            ">{message}</div>
            <div style="
                font-size:14px;
                color:#5b6575;
            "><b>한 줄 팁</b>: {tip}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_evaluation_badge(grade, score, label_text="오늘의 평가"):
    if grade == "좋아요" or grade == "비교적 잘 관리되고 있어요":
        bg_color = "#eef9f1"
        border_color = "#b9e2c2"
        title_color = "#17663a"
        score_bg = "#dff3e5"
    elif grade == "조금 더 관리가 필요해요" or grade == "조금 더 꾸준한 관리가 필요해요":
        bg_color = "#fff8e8"
        border_color = "#f1d89a"
        title_color = "#8a5a00"
        score_bg = "#ffefc2"
    else:
        bg_color = "#fff1f1"
        border_color = "#efb5b5"
        title_color = "#9f1f1f"
        score_bg = "#ffd9d9"

    st.markdown(
        f"""
        <div style="
            border:1px solid {border_color};
            border-radius:18px;
            padding:18px;
            background-color:{bg_color};
            box-shadow:0 1px 6px rgba(0,0,0,0.03);
            margin-top:10px;
            margin-bottom:10px;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
                flex-wrap:wrap;
            ">
                <div>
                    <div style="
                        font-size:14px;
                        color:#5b6575;
                        margin-bottom:6px;
                    ">{label_text}</div>
                    <div style="
                        font-size:28px;
                        font-weight:800;
                        color:{title_color};
                    ">{grade}</div>
                </div>
                <div style="
                    background:{score_bg};
                    border:1px solid {border_color};
                    border-radius:999px;
                    padding:10px 16px;
                    font-size:20px;
                    font-weight:800;
                    color:{title_color};
                ">{score}점</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def evaluate_today_record(record):
    water = pd.to_numeric(record["물섭취컵"], errors="coerce")
    if pd.isna(water):
        water = 0

    urine_count = pd.to_numeric(record["소변횟수"], errors="coerce")
    if pd.isna(urine_count):
        urine_count = 0

    pain = str(record["통증여부"])
    sweat = str(record["땀배출"])
    salty_food = str(record["짠음식섭취"])

    score = 100
    reasons = []
    good_points = []
    next_actions = []

    if water >= 8:
        good_points.append("물 섭취가 목표 수준에 도달했습니다.")
    elif water >= 6:
        score -= 10
        reasons.append("물 섭취가 목표보다 조금 부족했습니다.")
        next_actions.append("내일은 물을 1~2컵 더 챙겨보세요.")
    else:
        score -= 25
        reasons.append("물 섭취가 목표보다 많이 부족했습니다.")
        next_actions.append("물을 한 번에 많이 마시기보다 나누어 자주 마셔보세요.")

    if salty_food == "아니오":
        good_points.append("짠 음식 섭취를 잘 줄였습니다.")
    elif salty_food == "조금":
        score -= 10
        reasons.append("짠 음식 섭취가 조금 있었습니다.")
        next_actions.append("짠 음식이 있는 날은 물을 더 챙겨보세요.")
    elif salty_food == "예":
        score -= 20
        reasons.append("짠 음식 섭취가 있었습니다.")
        next_actions.append("내일은 짠 음식 빈도를 조금 줄여보세요.")

    if pain == "없음":
        good_points.append("통증 기록은 없었습니다.")
    elif pain == "조금 있음":
        score -= 10
        reasons.append("통증이 조금 있었습니다.")
        next_actions.append("통증이 반복되는지 며칠 더 기록을 확인해보세요.")
    elif pain == "심함":
        score -= 25
        reasons.append("통증이 심한 편으로 기록되었습니다.")
        next_actions.append("통증이 계속되거나 심하면 의료진 상담을 고려해보세요.")

    if sweat == "보통":
        score -= 5
        reasons.append("오늘은 땀 배출이 있어 수분 보충이 더 중요했습니다.")
    elif sweat == "많음":
        if water <= 7:
            score -= 10
            reasons.append("땀 배출이 많아 수분 보충이 더 필요했습니다.")
        else:
            reasons.append("땀 배출이 많아 평소보다 수분을 더 챙기면 좋습니다.")
        next_actions.append("땀을 많이 흘린 날은 평소보다 일찍 물을 챙겨보세요.")

    if urine_count >= 5:
        good_points.append("소변 횟수는 무난한 편으로 보입니다.")
    elif urine_count >= 3:
        score -= 5
        reasons.append("소변 횟수가 조금 적은 편일 수 있습니다.")
        next_actions.append("수분 섭취를 조금 더 늘려보세요.")
    else:
        score -= 10
        reasons.append("소변 횟수가 적은 편으로 보입니다.")
        next_actions.append("오늘보다 물 섭취를 늘려 변화를 확인해보세요.")

    score = max(0, min(100, int(score)))

    if score >= 85:
        grade = "좋아요"
        summary = "오늘은 결석 예방을 위한 생활관리가 전반적으로 잘 유지되었습니다."
    elif score >= 60:
        grade = "조금 더 관리가 필요해요"
        summary = "오늘 기록을 보면 몇 가지 생활 습관을 조금 더 챙기면 좋겠습니다."
    else:
        grade = "주의가 필요해요"
        summary = "오늘은 수분 섭취와 생활 습관 면에서 더 신경 써야 하는 하루였습니다."

    if len(reasons) == 0:
        reasons_text = "전반적으로 무난한 하루였습니다."
    else:
        reasons_text = " / ".join(reasons[:3])

    if len(good_points) == 0:
        good_text = "오늘 기록에서는 특별히 잘 유지된 항목이 두드러지지 않았습니다."
    else:
        good_text = " / ".join(good_points[:3])

    if len(next_actions) == 0:
        action_text = "지금처럼 생활 기록을 꾸준히 이어가보세요."
    else:
        dedup_actions = []
        for action in next_actions:
            if action not in dedup_actions:
                dedup_actions.append(action)
        action_text = " / ".join(dedup_actions[:3])

    return {
        "score": score,
        "grade": grade,
        "summary": summary,
        "reasons_text": reasons_text,
        "good_text": good_text,
        "action_text": action_text
    }


def evaluate_recent_7days(df):
    if len(df) == 0:
        return None

    temp = df.copy()
    temp["기록시각_dt"] = pd.to_datetime(temp["기록시각"], errors="coerce")
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
    recent_df = temp[temp["기록시각_dt"] >= cutoff].copy()

    if len(recent_df) == 0:
        return None

    scores = []
    for _, row in recent_df.iterrows():
        result = evaluate_today_record(row)
        scores.append(result["score"])

    avg_score = int(round(sum(scores) / len(scores), 0))

    record_days = recent_df["기록시각_dt"].dt.strftime("%Y-%m-%d").nunique()
    avg_water = pd.to_numeric(recent_df["물섭취컵"], errors="coerce").fillna(0).mean()
    pain_days = (recent_df["통증여부"].astype(str) != "없음").sum()
    salty_days = (recent_df["짠음식섭취"].astype(str) != "아니오").sum()
    low_urine_days = (pd.to_numeric(recent_df["소변횟수"], errors="coerce").fillna(0) <= 3).sum()
    goal_water_days = (pd.to_numeric(recent_df["물섭취컵"], errors="coerce").fillna(0) >= DAILY_WATER_GOAL).sum()

    good_points = []
    weak_points = []

    if record_days >= 5:
        good_points.append(f"최근 7일 중 {record_days}일 기록을 남겼습니다.")
    else:
        weak_points.append(f"최근 7일 기록 일수는 {record_days}일입니다.")

    if avg_water >= 8:
        good_points.append("평균 물 섭취가 목표 수준에 가깝습니다.")
    elif avg_water >= 6:
        weak_points.append("평균 물 섭취가 목표보다 조금 부족합니다.")
    else:
        weak_points.append("평균 물 섭취가 전반적으로 부족한 편입니다.")

    if salty_days <= 1:
        good_points.append("짠 음식 섭취 빈도가 낮은 편입니다.")
    else:
        weak_points.append("짠 음식이 있는 날이 자주 보입니다.")

    if pain_days == 0:
        good_points.append("통증 기록이 없었습니다.")
    else:
        weak_points.append("통증이 있었던 기록이 반복되었습니다.")

    if low_urine_days >= 2:
        weak_points.append("소변 횟수가 적은 날이 반복된 것으로 보입니다.")

    if goal_water_days >= 4:
        good_points.append("물 목표를 채운 날이 여러 번 있었습니다.")

    if avg_score >= 85:
        grade = "비교적 잘 관리되고 있어요"
        summary = "최근 7일 기록을 보면 전반적으로 생활관리가 안정적으로 유지되고 있습니다."
    elif avg_score >= 60:
        grade = "조금 더 꾸준한 관리가 필요해요"
        summary = "최근 7일 기록을 보면 기본 흐름은 있지만 조금 더 꾸준함이 필요합니다."
    else:
        grade = "주의가 필요해요"
        summary = "최근 7일 기록을 보면 수분 섭취와 생활 습관을 더 신경 써야 하는 흐름이 보입니다."

    good_text = " / ".join(good_points[:3]) if good_points else "최근 7일 기록에서 두드러진 강점은 아직 많지 않습니다."
    weak_text = " / ".join(weak_points[:3]) if weak_points else "전반적으로 무난한 흐름입니다."

    return {
        "score": avg_score,
        "grade": grade,
        "summary": summary,
        "good_text": good_text,
        "weak_text": weak_text
    }


def get_today_prefill_values(today_record):
    if today_record is None:
        return {
            "water": 0,
            "pain": "없음",
            "urine": "맑음",
            "urine_count": 0,
            "sweat": "적음",
            "salty_food": "아니오",
            "memo": ""
        }

    water = pd.to_numeric(today_record["물섭취컵"], errors="coerce")
    if pd.isna(water):
        water = 0

    urine_count = pd.to_numeric(today_record["소변횟수"], errors="coerce")
    if pd.isna(urine_count):
        urine_count = 0

    return {
        "water": int(water),
        "pain": str(today_record["통증여부"]) if str(today_record["통증여부"]) in ["없음", "조금 있음", "심함"] else "없음",
        "urine": str(today_record["소변상태"]) if str(today_record["소변상태"]) in ["맑음", "보통", "진함", "잘 모르겠음"] else "맑음",
        "urine_count": int(urine_count),
        "sweat": str(today_record["땀배출"]) if str(today_record["땀배출"]) in ["적음", "보통", "많음"] else "적음",
        "salty_food": str(today_record["짠음식섭취"]) if str(today_record["짠음식섭취"]) in ["아니오", "조금", "예"] else "아니오",
        "memo": "" if str(today_record["메모"]) == "nan" else str(today_record["메모"])
    }


init_db()
df_all = load_data()
today_done = has_today_record(df_all)
today_record = get_today_latest_record(df_all)
recent7_eval = evaluate_recent_7days(df_all)
prefill = get_today_prefill_values(today_record)

if "flash_menu" not in st.session_state:
    st.session_state.flash_menu = None

if "flash_message" not in st.session_state:
    st.session_state.flash_message = None

if "flash_level" not in st.session_state:
    st.session_state.flash_level = "success"

if "today_eval" not in st.session_state:
    st.session_state.today_eval = None

st.title("💧 요로케")
st.caption("요로결석 예방을 위한 생활관리 테스트 앱")


st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)



top_box_col1, top_box_col2 = st.columns(2)

lang_box_html = """
<div style="border:1px solid #e3ebf5; border-radius:18px; padding:16px 18px; background-color:#ffffff; box-shadow:0 1px 6px rgba(0,0,0,0.03); min-height:148px;">
    <div style="font-size:15px; font-weight:700; color:#183b56; margin-bottom:16px;">언어 선택</div>
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:14px;">
        <span style="display:inline-block; padding:6px 14px; border:1px solid #dbe4f0; border-radius:999px; background-color:#fbfdff; font-size:14px; font-weight:700; color:#48607a; box-shadow:0 1px 2px rgba(0,0,0,0.03);">KR</span>
        <span style="display:inline-block; padding:6px 14px; border:1px solid #dbe4f0; border-radius:999px; background-color:#fbfdff; font-size:14px; font-weight:700; color:#48607a; box-shadow:0 1px 2px rgba(0,0,0,0.03);">VN</span>
        <span style="display:inline-block; padding:6px 14px; border:1px solid #dbe4f0; border-radius:999px; background-color:#fbfdff; font-size:14px; font-weight:700; color:#48607a; box-shadow:0 1px 2px rgba(0,0,0,0.03);">EN</span>
    </div>
    <div style="font-size:13px; color:#7a8798; line-height:1.5;">추후 언어 전환 기능 추가 예정</div>
</div>
"""

account_box_html = """
<div style="border:1px solid #e3ebf5; border-radius:18px; padding:16px 18px; background-color:#ffffff; box-shadow:0 1px 6px rgba(0,0,0,0.03); min-height:148px;">
    <div style="font-size:15px; font-weight:700; color:#183b56; margin-bottom:16px;">계정</div>
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:14px;">
        <span style="display:inline-block; padding:7px 16px; border:1px solid #dbe4f0; border-radius:999px; background-color:#fbfdff; font-size:14px; font-weight:700; color:#48607a; box-shadow:0 1px 2px rgba(0,0,0,0.03);">로그인</span>
        <span style="display:inline-block; padding:7px 16px; border:1px solid #dbe4f0; border-radius:999px; background-color:#fbfdff; font-size:14px; font-weight:700; color:#48607a; box-shadow:0 1px 2px rgba(0,0,0,0.03);">회원가입</span>
    </div>
    <div style="font-size:13px; color:#7a8798; line-height:1.5;">추후 로그인 및 회원가입 기능 추가 예정</div>
</div>
"""

with top_box_col1:
    st.markdown(lang_box_html, unsafe_allow_html=True)

with top_box_col2:
    st.markdown(account_box_html, unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)


test_tool_col1, test_tool_col2 = st.columns([6.2, 3.8])

with test_tool_col1:
    draw_section_box("테스트 도구")

    sample_btn_col1, sample_btn_col2 = st.columns([4.2, 5.8])

    with sample_btn_col1:
        sample_clicked = st.button("샘플 기록 8일 넣기", use_container_width=True)

    st.markdown(
        """
        <div style="
            font-size:13px;
            color:#7a8798;
            line-height:1.45;
            margin-top:-6px;
            white-space:nowrap;
        ">
            테스트/시연용 기록입니다. 한 번 누르면 8일치 기록이 추가됩니다.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    div.stButton > button[kind="secondary"] {
        border: 1px solid #dbe4f0;
        border-radius: 999px;
        background-color: #fbfdff;
        color: #48607a;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if sample_clicked:
    insert_sample_records()
    st.session_state.flash_menu = "홈"
    st.session_state.flash_message = "샘플 기록 8일이 추가되었습니다."
    st.session_state.flash_level = "success"
    st.rerun()

st.markdown("---")
st.markdown(
    """
    <div style="
        font-size:22px;
        font-weight:800;
        color:#183b56;
        margin-top:2px;
        margin-bottom:8px;
    ">
        메뉴
    </div>
    """,
    unsafe_allow_html=True
)

menu = st.radio(
    "메뉴",
    ["홈", "오늘 체크", "음식 확인", "기록 보기"],
    horizontal=True,
    label_visibility="collapsed"
)




if menu == "홈":
    show_menu_flash("홈")

    # 1. 헤더 영역
    draw_section_box("앱 소개")
    draw_helper_text("오늘 상태와 최근 7일 흐름을 한눈에 볼 수 있는 메인 화면입니다.")

    header_col1, header_col2 = st.columns([1.2, 1.2])

    with header_col1:
        if today_done:
            draw_info_card("오늘 기록 상태", "오늘 기록이 있습니다.")
        else:
            draw_info_card("오늘 기록 상태", "오늘 기록이 아직 없습니다. 오늘 체크에서 기록해보세요.")

    with header_col2:
        total_count = len(df_all)

        if len(df_all) > 0:
            recent_df = get_latest_records(df_all, count=min(7, len(df_all)))
            avg_water = pd.to_numeric(recent_df["물섭취컵"], errors="coerce").fillna(0).mean()
            avg_water_text = f"{avg_water:.1f}컵"
        else:
            avg_water_text = "0컵"

        draw_info_card(
            "전체 기록 요약",
            f"총 기록 수: {total_count}개\n최근 평균 물 섭취: {avg_water_text}"
        )

    st.markdown("---")

    # 2. 오늘 상태 영역
    draw_section_box("오늘 상태")
    draw_helper_text("오늘 기록된 내용과 오늘의 평가를 확인합니다.")

    today_summary_col1, today_summary_col2, today_summary_col3, today_summary_col4 = st.columns(4)

    if today_record is not None:
        today_water = pd.to_numeric(today_record["물섭취컵"], errors="coerce")
        if pd.isna(today_water):
            today_water = 0

        today_urine_count = pd.to_numeric(today_record["소변횟수"], errors="coerce")
        if pd.isna(today_urine_count):
            today_urine_count = 0

        with today_summary_col1:
            draw_box("오늘 물 섭취", f"{int(today_water)}컵")
        with today_summary_col2:
            draw_box("오늘 소변 횟수", f"{int(today_urine_count)}회")
        with today_summary_col3:
            draw_box("오늘 짠 음식", str(today_record["짠음식섭취"]))
        with today_summary_col4:
            draw_box("오늘 통증", str(today_record["통증여부"]))
    else:
        with today_summary_col1:
            draw_box("오늘 물 섭취", "-")
        with today_summary_col2:
            draw_box("오늘 소변 횟수", "-")
        with today_summary_col3:
            draw_box("오늘 짠 음식", "-")
        with today_summary_col4:
            draw_box("오늘 통증", "-")

    if today_record is not None:
        evaluation = evaluate_today_record(today_record)
        draw_evaluation_badge(evaluation["grade"], evaluation["score"], "오늘의 평가")

        today_eval_col1, today_eval_col2 = st.columns(2)
        with today_eval_col1:
            draw_info_card("한줄 요약", evaluation["summary"])
            draw_info_card("잘한 점", evaluation["good_text"])
        with today_eval_col2:
            draw_info_card("아쉬운 점", evaluation["reasons_text"])
            draw_info_card("내일 제안", evaluation["action_text"])

        st.caption("이 평가는 생활관리용 참고 안내이며, 의료 진단을 대신하지 않습니다.")
    else:
        st.info("오늘 기록이 있어야 오늘의 평가를 볼 수 있습니다.")

    st.markdown("---")

    # 3. 최근 7일 흐름 영역
    draw_section_box("최근 7일 흐름")
    draw_helper_text("최근 7일 생활기록 흐름과 주간 요약을 확인합니다.")

    if recent7_eval is not None:
        draw_evaluation_badge(recent7_eval["grade"], recent7_eval["score"], "최근 7일 평가")

        week_eval_col1, week_eval_col2 = st.columns(2)
        with week_eval_col1:
            draw_info_card("최근 7일 한줄 요약", recent7_eval["summary"])
            draw_info_card("최근 7일 잘한 점", recent7_eval["good_text"])
        with week_eval_col2:
            draw_info_card("최근 7일 보완점", recent7_eval["weak_text"])
    else:
        st.info("최근 7일 기록이 쌓이면 이곳에 주간 요약이 보입니다.")

    summary = get_recent_7day_summary(df_all)

    week_summary_col1, week_summary_col2, week_summary_col3, week_summary_col4 = st.columns(4)
    with week_summary_col1:
        draw_box("기록 일수", f"{summary['기록일수']}일")
    with week_summary_col2:
        draw_box("평균 물 섭취", f"{summary['평균물섭취']}컵")
    with week_summary_col3:
        draw_box("통증 기록 수", f"{summary['통증기록수']}회")
    with week_summary_col4:
        draw_box("짠 음식 기록 수", f"{summary['짠음식기록수']}회")

    st.markdown("---")

    # 4. 하단 정보 영역
    draw_section_box("추가 정보")
    draw_helper_text("가장 최근 기록과 제품 소개 영역을 확인합니다.")

    draw_section_box("최근 기록 1개")

    if today_record is not None:
        draw_food_result_box(
            f"기록 시각: {today_record['기록시각']}",
            f"물 {today_record['물섭취컵']}컵 / 소변 {today_record['소변횟수']}회 / 통증 {today_record['통증여부']} / 짠 음식 {today_record['짠음식섭취']}",
            str(today_record["메모"]) if str(today_record["메모"]) != "nan" and str(today_record["메모"]).strip() != "" else "메모 없음"
        )
    else:
        latest_df = get_latest_records(df_all, count=1)
        if len(latest_df) > 0:
            latest_row = latest_df.iloc[0]
            draw_food_result_box(
                f"기록 시각: {latest_row['기록시각']}",
                f"물 {latest_row['물섭취컵']}컵 / 소변 {latest_row['소변횟수']}회 / 통증 {latest_row['통증여부']} / 짠 음식 {latest_row['짠음식섭취']}",
                str(latest_row["메모"]) if str(latest_row["메모"]) != "nan" and str(latest_row["메모"]).strip() != "" else "메모 없음"
            )
        else:
            st.info("아직 기록이 없습니다.")

elif menu == "오늘 체크":
    show_menu_flash("오늘 체크")

    draw_section_box("오늘 체크")

    if today_done:
        st.info("오늘 기록이 이미 있습니다. 아래 값을 바꾸고 ‘오늘 기록 수정’을 누르면 오늘 기록이 업데이트됩니다.")
    else:
        st.info("오늘 상태를 간단히 기록해보세요.")

    pain_options = ["없음", "조금 있음", "심함"]
    urine_options = ["맑음", "보통", "진함", "잘 모르겠음"]
    sweat_options = ["적음", "보통", "많음"]
    salty_options = ["아니오", "조금", "예"]

    draw_section_box("💧 물 섭취")
    water = st.number_input(
        "오늘 물을 몇 컵 마셨나요?",
        min_value=0,
        max_value=30,
        value=prefill["water"]
    )
    progress_ratio = min(water / DAILY_WATER_GOAL, 1.0)
    remaining_water = max(DAILY_WATER_GOAL - water, 0)

    st.progress(progress_ratio)

    if water < DAILY_WATER_GOAL:
        st.caption(f"현재 {water}컵 마셨습니다. 목표까지 {remaining_water}컵 남았습니다.")
    elif water == DAILY_WATER_GOAL:
        st.success("오늘 물 목표 8컵을 채웠습니다.")
    else:
        st.success(f"오늘 물 목표를 달성했습니다. 목표보다 {water - DAILY_WATER_GOAL}컵 더 마셨습니다.")

    draw_section_box("🩺 몸 상태")
    pain = st.radio(
        "오늘 통증이 있었나요?",
        pain_options,
        index=pain_options.index(prefill["pain"]),
        horizontal=True
    )
    urine = st.selectbox(
        "오늘 소변 상태는 어땠나요?",
        urine_options,
        index=urine_options.index(prefill["urine"])
    )
    urine_count = st.number_input(
        "오늘 소변은 몇 번 정도 봤나요?",
        min_value=0,
        max_value=30,
        value=prefill["urine_count"],
        step=1
    )

    draw_section_box("🍜 생활 습관")
    sweat = st.radio(
        "오늘 땀 배출은 어땠나요?",
        sweat_options,
        index=sweat_options.index(prefill["sweat"]),
        horizontal=True
    )
    salty_food = st.radio(
        "오늘 짠 음식을 먹었나요?",
        salty_options,
        index=salty_options.index(prefill["salty_food"]),
        horizontal=True
    )
    memo = st.text_area(
        "메모가 있으면 적어주세요",
        value=prefill["memo"],
        placeholder="예: 커피를 많이 마셨음, 운동을 했음"
    )

    if not today_done:
        if st.button("오늘 기록 저장", use_container_width=True):
            record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_record(record_time, water, pain, urine, urine_count, sweat, salty_food, memo)

            temp_record = {
                "기록시각": record_time,
                "물섭취컵": water,
                "통증여부": pain,
                "소변상태": urine,
                "소변횟수": urine_count,
                "땀배출": sweat,
                "짠음식섭취": salty_food,
                "메모": memo
            }
            st.session_state.today_eval = evaluate_today_record(temp_record)

            st.session_state.flash_menu = "오늘 체크"
            st.session_state.flash_message = "오늘 기록이 저장되었습니다."
            st.session_state.flash_level = "success"
            st.rerun()
    else:
        if st.button("오늘 기록 수정", use_container_width=True):
            update_today_record(water, pain, urine, urine_count, sweat, salty_food, memo)

            temp_record = {
                "기록시각": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "물섭취컵": water,
                "통증여부": pain,
                "소변상태": urine,
                "소변횟수": urine_count,
                "땀배출": sweat,
                "짠음식섭취": salty_food,
                "메모": memo
            }
            st.session_state.today_eval = evaluate_today_record(temp_record)

            st.session_state.flash_menu = "오늘 체크"
            st.session_state.flash_message = "오늘 기록이 수정되었습니다."
            st.session_state.flash_level = "success"
            st.rerun()

    if st.session_state.today_eval is not None:
        evaluation = st.session_state.today_eval

        st.markdown("---")
        draw_section_box("저장된 기록의 오늘 평가")
        draw_evaluation_badge(evaluation["grade"], evaluation["score"], "오늘의 평가")
        draw_info_card("한줄 요약", evaluation["summary"])
        draw_info_card("잘한 점", evaluation["good_text"])
        draw_info_card("아쉬운 점", evaluation["reasons_text"])
        draw_info_card("내일 제안", evaluation["action_text"])
        st.caption("이 평가는 생활관리용 참고 안내이며, 의료 진단을 대신하지 않습니다.")

elif menu == "음식 확인":
    show_menu_flash("음식 확인")

    draw_section_box("음식 확인")
    st.caption("음식 이름을 입력하면 테스트용 기준으로 간단한 안내를 보여줍니다.")

    food = st.text_input("음식 이름을 입력하세요", placeholder="예: 아메리카노, 콜라, 소주, 국밥")

    if st.button("음식 확인하기", use_container_width=True):
        canonical_food, original_food, matched_by_alias = normalize_food_name(food)

        if str(food).strip() == "":
            st.warning("음식 이름을 먼저 입력해주세요.")
        elif canonical_food in food_db:
            result = food_db[canonical_food]

            if matched_by_alias:
                st.info(f"입력한 '{original_food}'를 '{canonical_food}' 기준으로 안내합니다.")

            if result["level"] == "good":
                st.success(result["title"])
            elif result["level"] == "normal":
                st.warning(result["title"])
            else:
                st.error(result["title"])

            draw_food_result_box(result["title"], result["message"], result["tip"])
        else:
            st.info("아직 등록되지 않은 음식입니다.")

    st.markdown("---")
    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1:
        draw_box("예시", "아메리카노")
    with ex2:
        draw_box("예시", "콜라")
    with ex3:
        draw_box("예시", "국밥")
    with ex4:
        draw_box("예시", "아몬드")

elif menu == "기록 보기":
    show_menu_flash("기록 보기")

    draw_section_box("기록 보기")

    if len(df_all) > 0:
        if recent7_eval is not None:
            draw_section_box("최근 7일 평가")
            draw_evaluation_badge(recent7_eval["grade"], recent7_eval["score"], "최근 7일 평가")
            draw_info_card("최근 7일 한줄 요약", recent7_eval["summary"])
            draw_info_card("최근 7일 잘한 점", recent7_eval["good_text"])
            draw_info_card("최근 7일 보완점", recent7_eval["weak_text"])
            st.caption("이 평가는 최근 7일 기록을 바탕으로 한 생활관리용 참고 안내입니다.")

            st.markdown("---")

        summary = get_recent_7day_summary(df_all)

        draw_section_box("최근 7일 요약")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            draw_box("기록 일수", f"{summary['기록일수']}일")
        with s2:
            draw_box("평균 물 섭취", f"{summary['평균물섭취']}컵")
        with s3:
            draw_box("통증 기록 수", f"{summary['통증기록수']}회")
        with s4:
            draw_box("짠 음식 기록 수", f"{summary['짠음식기록수']}회")

        st.markdown("---")
        draw_section_box("기록 그래프")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("최근 물 섭취량")
            water_chart_df = get_recent_water_chart_data(df_all, count=7)
            if len(water_chart_df) > 0:
                st.bar_chart(water_chart_df)

            st.write("최근 소변 횟수")
            urine_chart_df = get_urine_count_chart_data(df_all, count=7)
            if len(urine_chart_df) > 0:
                st.bar_chart(urine_chart_df)

        with chart_col2:
            st.write("통증 여부 요약")
            pain_chart_df = get_pain_chart_data(df_all)
            if len(pain_chart_df) > 0:
                st.bar_chart(pain_chart_df)

            st.write("짠 음식 섭취 요약")
            salty_chart_df = get_salty_chart_data(df_all)
            if len(salty_chart_df) > 0:
                st.bar_chart(salty_chart_df)

            st.write("땀 배출 요약")
            sweat_chart_df = get_sweat_chart_data(df_all)
            if len(sweat_chart_df) > 0:
                st.bar_chart(sweat_chart_df)

        st.markdown("---")
        draw_section_box("기록 표")
        st.dataframe(df_all, use_container_width=True)

        st.markdown("---")
        draw_section_box("기록 수정")

        record_options = df_all["id"].tolist()
        selected_edit_id = st.selectbox("수정할 기록 선택", record_options, key="edit_select")

        selected_rows = df_all[df_all["id"] == selected_edit_id]

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

            edit_water = st.number_input("수정할 물 섭취량(컵)", min_value=0, max_value=30, value=int(current_water), key="edit_water")
            edit_pain = st.radio(
                "수정할 통증 여부",
                pain_options,
                index=pain_options.index(str(selected_row["통증여부"])) if str(selected_row["통증여부"]) in pain_options else 0,
                key="edit_pain"
            )
            edit_urine = st.selectbox(
                "수정할 소변 상태",
                urine_options,
                index=urine_options.index(str(selected_row["소변상태"])) if str(selected_row["소변상태"]) in urine_options else 0,
                key="edit_urine"
            )
            edit_urine_count = st.number_input("수정할 소변 횟수", min_value=0, max_value=30, value=int(current_urine_count), key="edit_urine_count")
            edit_sweat = st.radio(
                "수정할 땀 배출",
                sweat_options,
                index=sweat_options.index(str(selected_row["땀배출"])) if str(selected_row["땀배출"]) in sweat_options else 1,
                key="edit_sweat"
            )
            edit_salty = st.radio(
                "수정할 짠 음식 섭취",
                salty_options,
                index=salty_options.index(str(selected_row["짠음식섭취"])) if str(selected_row["짠음식섭취"]) in salty_options else 0,
                key="edit_salty"
            )
            edit_memo = st.text_area(
                "수정할 메모",
                value="" if str(selected_row["메모"]) == "nan" else str(selected_row["메모"]),
                key="edit_memo"
            )

            if st.button("선택한 기록 수정", use_container_width=True):
                update_record(selected_edit_id, edit_water, edit_pain, edit_urine, edit_urine_count, edit_sweat, edit_salty, edit_memo)
                st.session_state.flash_menu = "기록 보기"
                st.session_state.flash_message = "기록이 수정되었습니다."
                st.session_state.flash_level = "success"
                st.rerun()

st.markdown("---")
draw_section_box("제품 소개")
st.caption("현재는 테스트용 배너 영역입니다. 추후 각 칸에 제품 이미지와 링크를 연결할 수 있습니다.")

banner_col1, banner_col2, banner_col3 = st.columns(3)

def draw_empty_banner(title_text):
    st.markdown(
        f"""
        <div style="
            width:100%;
            aspect-ratio: 5 / 2;
            border:1.5px dashed #cbd5e1;
            border-radius:18px;
            background:linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%);
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            padding:16px;
            box-sizing:border-box;
            color:#5b6575;
            font-size:15px;
            font-weight:600;
            margin-bottom:8px;
            white-space:pre-line;
        ">
            {title_text}
        </div>
        """,
        unsafe_allow_html=True
    )

with banner_col1:
    draw_empty_banner("배너 1\n(추후 제품 이미지 예정)")

with banner_col2:
    draw_empty_banner("배너 2\n(추후 제품 이미지 예정)")

with banner_col3:
    draw_empty_banner("배너 3\n(추후 제품 이미지 예정)")
