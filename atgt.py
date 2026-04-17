import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát iRAP - UTC", layout="wide")

# --- PHẦN CHÈN HÌNH ẢNH / LOGO ---
# Bạn có thể thay link ảnh dưới đây bằng link ảnh thực tế của Khoa hoặc Trường
col_logo1, col_logo2 = st.columns([1, 5])

with col_logo1:
    # Chèn logo trường hoặc khoa (đây là ví dụ link ảnh)
    st.image("https://utc.edu.vn/logo.png", width=120) 

with col_logo2:
    st.markdown("### ĐẠI HỌC GIAO THÔNG VẬN TẢI")
    st.markdown("#### KHOA CÔNG TRÌNH - BỘ MÔN ĐƯỜNG BỘ")
    st.write("---")

# Khởi tạo bộ nhớ tạm
if 'data_store' not in st.session_state:
    st.session_state.data_store = []

st.title("📊 Phiếu Khảo sát Đánh giá An toàn Tuyến đường")
st.info("💡 Đồ án nghiên cứu ứng dụng tiêu chuẩn iRAP trong đánh giá an toàn giao thông.")

# --- TIẾP TỤC CÁC PHẦN CODE KHẢO SÁT NHƯ TRƯỚC ---
# (Phần danh sách 10 tiêu chí và Form nhập liệu giữ nguyên như bản trước)
