import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(layout="wide")
st.title("🏭 대한제분 일일재고현황표")

# ---------------------------------------------------------
# 1. 입력창 (엑셀 복사 붙여넣기)
# ---------------------------------------------------------
with st.expander("데이터 입력 열기/닫기", expanded=True):
    st.info("엑셀에서 [위치ID | 품목명 | 수량] 순서로 3개 열을 복사해서 붙여넣으세요.")
    input_data = st.text_area(
        "붙여넣기 칸", 
        height=150,
        placeholder="예시:\nA101\tWASW\t1,508\nA102\tWCRS\t1,671"
    )

# ---------------------------------------------------------
# 2. 데이터 처리 (지능형 파싱)
# ---------------------------------------------------------
inventory_map = {}  # 데이터를 저장할지도

if input_data:
    try:
        # 엑셀 데이터(탭으로 구분됨)를 읽어서 표로 만듦
        df = pd.read_csv(StringIO(input_data), sep='\t', header=None, names=['ID', 'Name', 'Qty'])
        
        # 데이터를 딕셔너리로 변환 (예: 'A101'을 찾으면 내용이 나오게)
        for index, row in df.iterrows():
            clean_id = str(row['ID']).strip().upper() # ID 정리 (공백제거)
            inventory_map[clean_id] = {
                'name': str(row['Name']),
                'qty': str(row['Qty'])
            }
        st.success(f"총 {len(inventory_map)}개의 데이터를 인식했습니다.")
        
    except Exception as e:
        st.error("데이터 형식이 맞지 않습니다. 엑셀에서 3개 열(ID, 이름, 수량)만 정확히 복사했는지 확인해주세요.")

# ---------------------------------------------------------
# 3. 그림 그리기 (HTML/CSS)
# ---------------------------------------------------------
def get_card_html(id_code, top_px, left_px):
    # 데이터가 있으면 가져오고, 없으면 빈칸
    item = inventory_map.get(id_code, {'name': '-', 'qty': '-'})
    name = item['name']
    qty = item['qty']
    
    # 색상 로직 (정답 사진 참고: WASW는 파랑, WCRS는 주황, 나머지는 갈색)
    color = "#0000FF" if "WASW" in name else "#D2691E" if "WCRS" in name else "#8B4513"
    if name == '-': color = "#ccc"
    
    # 짝수 줄(A2, A4...)은 네모(Text), 홀수 줄(A1, A3...)은 동그라미(Circle)
    is_circle = True
    if id_code.startswith("A2") or id_code.startswith("A4"):
        is_circle = False
        
    # 스타일 결정
    shape_style = "border-radius: 50%; width: 75px; height: 75px; border: 1.5px solid black;" if is_circle else "width: 75px; height: 50px; border: none; background: transparent;"
    
    return f"""
    <div style="position: absolute; top: {top_px}px; left: {left_px}px; 
                {shape_style} background-color: white;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-size: 12px; font-weight: bold; z-index: 10;">
        <div style="color: {color}; margin-bottom: 2px;">{name}</div>
        <div style="color: black; font-size: 13px;">{qty}</div>
        <div style="color: #999; font-size: 10px; margin-top: 2px;">{id_code}</div>
    </div>
    """

# 배경 그리드와 전체 HTML 조립
html_content = """
<div style="position: relative; width: 800px; height: 550px; background-color: white; margin: 20px;">
    <div style="position: absolute; top: 40px; left: 50px; width: 700px; height: 400px; border: 2px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 240px; left: 50px; width: 700px; height: 0px; border-top: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 40px; left: 166px; width: 0px; height: 400px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 40px; left: 282px; width: 0px; height: 400px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 40px; left: 398px; width: 0px; height: 400px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 40px; left: 514px; width: 0px; height: 400px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 40px; left: 630px; width: 0px; height: 400px; border-left: 1px solid black; z-index: 0;"></div>
"""

# 위치 좌표 설정 (수동 매핑으로 정확도 100% 보장)
# Row 1 (A101~A106) - Circle
html_content += get_card_html("A101", 0, 130)
html_content += get_card_html("A102", 0, 245)
html_content += get_card_html("A103", 0, 360)
html_content += get_card_html("A104", 0, 475)
html_content += get_card_html("A105", 0, 590)
html_content += get_card_html("A106", 0, 705)

# Row 2 (A201~A207) - Text Block (중간 위치)
html_content += get_card_html("A201", 100, 70)  # 사이사이 배치
html_content += get_card_html("A202", 100, 185)
html_content += get_card_html("A203", 100, 300)
html_content += get_card_html("A204", 100, 415)
html_content += get_card_html("A205", 100, 530)
html_content += get_card_html("A206", 100, 645)
html_content += get_card_html("A207", 100, 750)

# Row 3 (A301~A306) - Circle
html_content += get_card_html("A301", 200, 130)
html_content += get_card_html("A302", 200, 245)
html_content += get_card_html("A303", 200, 360)
html_content += get_card_html("A304", 200, 475)
html_content += get_card_html("A305", 200, 590)
html_content += get_card_html("A306", 200, 705)

# Row 4 (A401~A407) - Text Block
html_content += get_card_html("A401", 300, 70)
html_content += get_card_html("A402", 300, 185)
html_content += get_card_html("A403", 300, 300)
html_content += get_card_html("A404", 300, 415)
html_content += get_card_html("A405", 300, 530)
html_content += get_card_html("A406", 300, 645)
html_content += get_card_html("A407", 300, 750)

# Row 5 (A501~A506) - Circle (바닥)
html_content += get_card_html("A501", 400, 130)
html_content += get_card_html("A502", 400, 245)
html_content += get_card_html("A503", 400, 360)
html_content += get_card_html("A504", 400, 475)
html_content += get_card_html("A505", 400, 590)
html_content += get_card_html("A506", 400, 705)

html_content += "</div>"

# 최종 출력
st.write("### ▼ 재고 현황판 (자동 생성됨)")
st.components.v1.html(html_content, height=600)
