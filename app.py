import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(layout="wide")

# 제목 스타일링
st.markdown("""
    <h1 style='text-align: center; text-decoration: underline; text-underline-offset: 10px;'>일 일 재 고 현 황 표</h1>
    <br>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. 입력창 (엑셀 복사 붙여넣기)
# ---------------------------------------------------------
with st.expander("데이터 입력 열기/닫기", expanded=True):
    st.info("엑셀에서 [위치ID | 품목명 | 수량] 순서로 3개 열을 복사해서 붙여넣으세요.")
    input_data = st.text_area(
        "붙여넣기 칸", 
        height=150,
        placeholder="예시:\nA101\tWASW\t1508\nA102\tWCRS\t1671"
    )

# ---------------------------------------------------------
# 2. 데이터 처리 (소수점 제거 및 파싱)
# ---------------------------------------------------------
inventory_map = {} 

if input_data:
    try:
        df = pd.read_csv(StringIO(input_data), sep='\t', header=None, names=['ID', 'Name', 'Qty'])
        
        for index, row in df.iterrows():
            clean_id = str(row['ID']).strip().upper()
            
            # 소수점 제거 로직
            try:
                raw_qty = str(row['Qty']).replace(',', '') # 쉼표 제거
                if raw_qty.replace('.','',1).isdigit(): # 숫자인지 확인
                    qty_num = int(float(raw_qty)) # 실수 변환 후 정수로 자름
                    qty_str = "{:,}".format(qty_num) # 쉼표 추가
                else:
                    qty_str = str(row['Qty'])
            except:
                qty_str = str(row['Qty'])

            inventory_map[clean_id] = {
                'name': str(row['Name']).strip(),
                'qty': qty_str
            }
        
    except Exception as e:
        st.error("데이터 형식이 맞지 않습니다. 엑셀 데이터를 정확히 복사해주세요.")

# ---------------------------------------------------------
# 3. 그림 그리기 (HTML/CSS)
# ---------------------------------------------------------
def get_card_html(id_code, top_px, left_px):
    item = inventory_map.get(id_code, {'name': '', 'qty': ''})
    name = item['name']
    qty = item['qty']
    
    # 색상 로직
    if name in ['WASW', 'WUSH', 'WASWP', 'WUSL9.0', 'WUSL', 'WASW']:
        color = "#0000FF" # 파란색
    elif name == '' or name == '-':
         color = "transparent"
    else:
        color = "#D35400" # 진한 주황/갈색
        
    # 수량 0일 때 빨간색
    qty_color = "black"
    if qty == '0':
        qty_color = "red"
        
    # 모양 결정 (짝수줄 네모 / 홀수줄 동그라미)
    is_circle = True
    if id_code.startswith("A2") or id_code.startswith("A4"):
        is_circle = False
        
    # 스타일 적용
    if is_circle:
        container_style = """
            border-radius: 50%; width: 90px; height: 90px; 
            border: 1.5px solid black; background-color: white;
            z-index: 10;
        """
        name_size = "14px"
        qty_size = "15px"
        id_color = "#ccc"
    else:
        container_style = """
            width: 90px; height: 60px; 
            border: none; background: transparent;
            z-index: 10;
        """
        name_size = "14px"
        qty_size = "15px"
        id_color = "#ccc"

    return f"""
    <div style="position: absolute; top: {top_px}px; left: {left_px}px; 
                {container_style}
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-weight: bold;">
        <div style="color: {color}; font-size: {name_size}; margin-bottom: 2px;">{name}</div>
        <div style="color: {qty_color}; font-size: {qty_size};">{qty}</div>
        <div style="color: {id_color}; font-size: 10px; margin-top: 2px;">{id_code}</div>
    </div>
    """

# 전체 레이아웃 (오른쪽 잘림 해결 + A107 삭제)
html_content = """
<div style="position: relative; width: 860px; height: 600px; background-color: white; margin: 0 auto;">
    
    <div style="position: absolute; top: 65px; left: 45px; width: 770px; height: 380px; border: 2px solid black; z-index: 0;"></div>
    
    <div style="position: absolute; top: 255px; left: 45px; width: 770px; height: 0px; border-top: 1px solid black; z-index: 0;"></div>
    
    <div style="position: absolute; top: 65px; left: 155px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 65px; left: 265px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 65px; left: 375px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 65px; left: 485px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 65px; left: 595px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
    <div style="position: absolute; top: 65px; left: 705px; width: 0px; height: 380px; border-left: 1px solid black; z-index: 0;"></div>
"""

# 좌표값 매핑
# Row 1 (A101~A106) - Circle (A107 삭제됨)
html_content += get_card_html("A101", 20, 110)
html_content += get_card_html("A102", 20, 220)
html_content += get_card_html("A103", 20, 330)
html_content += get_card_html("A104", 20, 440)
html_content += get_card_html("A105", 20, 550)
html_content += get_card_html("A106", 20, 660)

# Row 2 (A201~A207) - Text Block
html_content += get_card_html("A201", 130, 55)
html_content += get_card_html("A202", 130, 165)
html_content += get_card_html("A203", 130, 275)
html_content += get_card_html("A204", 130, 385)
html_content += get_card_html("A205", 130, 495)
html_content += get_card_html("A206", 130, 605)
html_content += get_card_html("A207", 130, 715)

# Row 3 (A301~A306) - Circle
html_content += get_card_html("A301", 210, 110)
html_content += get_card_html("A302", 210, 220)
html_content += get_card_html("A303", 210, 330)
html_content += get_card_html("A304", 210, 440)
html_content += get_card_html("A305", 210, 550)
html_content += get_card_html("A306", 210, 660)

# Row 4 (A401~A407) - Text Block
html_content += get_card_html("A401", 320, 55)
html_content += get_card_html("A402", 320, 165)
html_content += get_card_html("A403", 320, 275)
html_content += get_card_html("A404", 320, 385)
html_content += get_card_html("A405", 320, 495)
html_content += get_card_html("A406", 320, 605)
html_content += get_card_html("A407", 320, 715)

# Row 5 (A501~A506) - Circle
html_content += get_card_html("A501", 400, 110)
html_content += get_card_html("A502", 400, 220)
html_content += get_card_html("A503", 400, 330)
html_content += get_card_html("A504", 400, 440)
html_content += get_card_html("A505", 400, 550)
html_content += get_card_html("A506", 400, 660)

html_content += "</div>"

st.components.v1.html(html_content, height=600)
