import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO

# 화면을 넓게 씀
st.set_page_config(layout="wide", page_title="대한제분 재고관리 대시보드")

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
# 2. 데이터 처리 및 분석
# ---------------------------------------------------------
inventory_map = {} 
df_chart = pd.DataFrame() # 차트용 데이터프레임

if input_data:
    try:
        # 데이터 파싱
        df = pd.read_csv(StringIO(input_data), sep='\t', header=None, names=['ID', 'Name', 'Qty'])
        
        # 데이터 정제 (소수점 제거 및 숫자 변환)
        clean_data_list = []
        
        for index, row in df.iterrows():
            clean_id = str(row['ID']).strip().upper()
            name = str(row['Name']).strip()
            
            # 수량 처리 로직
            raw_qty = str(row['Qty']).replace(',', '')
            try:
                if raw_qty.replace('.','',1).isdigit():
                    qty_num = int(float(raw_qty)) # 숫자형 (계산용)
                    qty_str = "{:,}".format(qty_num) # 문자형 (표시용)
                else:
                    qty_num = 0
                    qty_str = str(row['Qty'])
            except:
                qty_num = 0
                qty_str = str(row['Qty'])

            # 맵핑 저장 (그림 그리기용)
            inventory_map[clean_id] = {
                'name': name,
                'qty': qty_str,
                'qty_num': qty_num  # 그래프 그리기 위해 숫자도 저장
            }
            
            # 차트용 리스트에 추가
            clean_data_list.append({
                '위치': clean_id,
                '품목': name,
                '재고량': qty_num
            })
            
        # 차트용 데이터프레임 생성
        df_chart = pd.DataFrame(clean_data_list)
        
        # -----------------------------------------------------
        # [신규 기능 1] 핵심 요약 정보 (KPI Dashboard)
        # -----------------------------------------------------
        st.markdown("### 📊 재고 현황 요약")
        kpi1, kpi2, kpi3 = st.columns(3)

        # 1. 총 재고량 계산
        total_stock = df_chart['재고량'].sum()
        
        # 2. 재고 0인 곳 카운트
        zero_stock_count = len(df_chart[df_chart['재고량'] == 0])
        
        # 3. 가장 재고 많은 곳
        if not df_chart.empty:
            max_row = df_chart.loc[df_chart['재고량'].idxmax()]
            max_info = f"{max_row['품목']} ({max_row['위치']})"
        else:
            max_info = "-"

        # KPI 카드 출력
        kpi1.metric("📦 총 재고량 합계", f"{total_stock:,} kg")
        kpi2.metric("🚨 재고 소진(0) 탱크", f"{zero_stock_count} 곳", delta_color="inverse")
        kpi3.metric("🏆 최다 보유 품목", max_info)
        
        st.divider() # 구분선

    except Exception as e:
        st.error(f"데이터 형식이 올바르지 않습니다. ({e})")

# ---------------------------------------------------------
# 3. 그림 그리기 (HTML/CSS) - 기존 유지
# ---------------------------------------------------------
def get_card_html(id_code, top_px, left_px):
    item = inventory_map.get(id_code, {'name': '', 'qty': '', 'qty_num': 0})
    name = item['name']
    qty = item['qty']
    
    # 색상 로직
    if name in ['WASW', 'WUSH', 'WASWP', 'WUSL9.0', 'WUSL', 'WASW']:
        color = "#0000FF"
    elif name == '' or name == '-':
         color = "transparent"
    else:
        color = "#D35400"
        
    qty_color = "black"
    if qty == '0' or item['qty_num'] == 0:
        qty_color = "red"
        
    # 모양 결정
    is_circle = True
    if id_code.startswith("A2") or id_code.startswith("A4"):
        is_circle = False
        
    if is_circle:
        container_style = "border-radius: 50%; width: 90px; height: 90px; border: 1.5px solid black; background-color: white; z-index: 10;"
    else:
        container_style = "width: 90px; height: 60px; border: none; background: transparent; z-index: 10;"

    return f"""
    <div style="position: absolute; top: {top_px}px; left: {left_px}px; {container_style}
                display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: bold;">
        <div style="color: {color}; font-size: 14px; margin-bottom: 2px;">{name}</div>
        <div style="color: {qty_color}; font-size: 15px;">{qty}</div>
        <div style="color: #ccc; font-size: 10px; margin-top: 2px;">{id_code}</div>
    </div>
    """

# 전체 레이아웃 HTML 생성
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

# 좌표값 매핑 (A107 삭제됨)
# Row 1
html_content += get_card_html("A101", 20, 110) + get_card_html("A102", 20, 220) + get_card_html("A103", 20, 330)
html_content += get_card_html("A104", 20, 440) + get_card_html("A105", 20, 550) + get_card_html("A106", 20, 660)
# Row 2
html_content += get_card_html("A201", 130, 55) + get_card_html("A202", 130, 165) + get_card_html("A203", 130, 275)
html_content += get_card_html("A204", 130, 385) + get_card_html("A205", 130, 495) + get_card_html("A206", 130, 605) + get_card_html("A207", 130, 715)
# Row 3
html_content += get_card_html("A301", 210, 110) + get_card_html("A302", 210, 220) + get_card_html("A303", 210, 330)
html_content += get_card_html("A304", 210, 440) + get_card_html("A305", 210, 550) + get_card_html("A306", 210, 660)
# Row 4
html_content += get_card_html("A401", 320, 55) + get_card_html("A402", 320, 165) + get_card_html("A403", 320, 275)
html_content += get_card_html("A404", 320, 385) + get_card_html("A405", 320, 495) + get_card_html("A406", 320, 605) + get_card_html("A407", 320, 715)
# Row 5
html_content += get_card_html("A501", 400, 110) + get_card_html("A502", 400, 220) + get_card_html("A503", 400, 330)
html_content += get_card_html("A504", 400, 440) + get_card_html("A505", 400, 550) + get_card_html("A506", 400, 660)

html_content += "</div>"

# 도면 출력
st.write("### ▼ 사일로(Silo) 배치도")
st.components.v1.html(html_content, height=600)

# -----------------------------------------------------
# [신규 기능 3] 데이터 시각화 차트
# -----------------------------------------------------
if not df_chart.empty:
    st.divider()
    st.markdown("### 📈 품목별 재고량 분석")
    
    # 막대 그래프 그리기 (Altair 사용)
    chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('위치', sort=None, title='저장 위치'),
        y=alt.Y('재고량', title='재고량 (kg)'),
        color=alt.Color('품목', title='품목명', legend=alt.Legend(orient="top")), # 품목별 색상 자동 구분
        tooltip=['위치', '품목', '재고량']
    ).properties(
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
