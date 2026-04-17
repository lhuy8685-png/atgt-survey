import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát iRAP - UTC", layout="wide")

# --- PHẦN HIỂN THỊ LOGO VÀ TÊN KHOA ---
# Sử dụng link ảnh logo được lưu trữ trên nền tảng ổn định hơn
logo_url = "https://upload.wikimedia.org/wikipedia/vi/8/81/Logo_dh_giaothongvantai.png" 

col_l1, col_l2 = st.columns([1, 6])

with col_l1:
    # Thêm tham số width và xử lý lỗi nếu link ảnh không tải được
    try:
        st.image(logo_url, width=100)
    except:
        st.write("📌 **UTC**")

with col_l2:
    st.subheader("TRƯỜNG ĐẠI HỌC GIAO THÔNG VẬN TẢI")
    st.markdown("### KHOA CÔNG TRÌNH - BỘ MÔN ĐƯỜNG BỘ")

st.write("---")

# Khởi tạo bộ nhớ tạm để lưu dữ liệu
if 'data_store' not in st.session_state:
    st.session_state.data_store = []

st.title("📊 Phiếu Khảo sát Đánh giá An toàn Tuyến đường")
st.info("💡 Đồ án nghiên cứu ứng dụng tiêu chuẩn iRAP trong đánh giá an toàn giao thông.")

# --- 10 TIÊU CHÍ ĐÁNH GIÁ ---
criteria = {
    "1. Bề mặt đường": "Đường có bằng phẳng không? Có ổ gà không?",
    "2. Vạch kẻ đường": "Vạch sơn chia làn, vạch đi bộ có rõ nét không?",
    "3. Biển báo": "Biển báo có đặt đúng chỗ và dễ thấy không?",
    "4. Đèn chiếu sáng": "Ban đêm đèn đường có đủ sáng không?",
    "5. Dải phân cách": "Ngăn cách giữa hai chiều có an toàn không?",
    "6. Vỉa hè": "Vỉa hè có rộng, không bị lấn chiếm không?",
    "7. Xe máy": "Xe máy có làn riêng hay đi hỗn hợp nguy hiểm?",
    "8. Điểm giao cắt": "Các lối ra vào ngõ có tầm nhìn thoáng không?",
    "9. Thoát nước": "Trời mưa đường có bị ngập úng không?",
    "10. Cảm giác an toàn": "Bạn có yên tâm khi đi qua đoạn đường này không?"
}

star_options = ["1 ⭐ (Rất rủi ro)", "2 ⭐", "3 ⭐ (Trung bình)", "4 ⭐", "5 ⭐ (Rất an toàn)"]

# Form nhập liệu
with st.form("survey_form"):
    # Bổ sung mục đối tượng khảo sát
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        user_name = st.text_input("Họ tên người khảo sát:", placeholder="Nhập tên của bạn...")
    with col_u2:
        user_type = st.radio(
            "Bạn tham gia giao thông chủ yếu bằng:",
            ["Người đi bộ", "Xe máy", "Ô tô"],
            horizontal=True
        )
    
    st.write("---")
    col1, col2, col3 = st.columns(3)

    def render_survey(header, key_p):
        st.markdown(f"### {header}")
        for name, desc in criteria.items():
            st.write(f"**{name}**")
            st.select_slider(desc, options=["Kém", "Tạm được", "Tốt"], key=f"{key_p}_{name}", value="Tạm được")
        
        st.write("---")
        stars = st.select_slider(f"Xếp hạng sao cho {header}:", options=star_options, key=f"{key_p}_s", value="3 ⭐ (Trung bình)")
        return stars

    with col1: s_kl = render_survey("Hầm Kim Liên", "kl")
    with col2: s_gp = render_survey("Đường Giải Phóng", "gp")
    with col3: s_ql = render_survey("QL 1A cũ", "ql")

    st.write("---")
    submitted = st.form_submit_button("GỬI ĐÁNH GIÁ CỦA BẠN")

if submitted:
    st.session_state.data_store.append({
        "Người đánh giá": user_name,
        "Đối tượng": user_type,
        "Hầm Kim Liên": s_kl,
        "Đường Giải Phóng": s_gp,
        "QL 1A cũ": s_ql
    })
    st.balloons()
    st.success(f"Cảm ơn {user_name}! Đã ghi lại kết quả khảo sát.")

# --- PHẦN TỔNG HỢP DỮ LIỆU ---
st.write("---")
show_admin = st.checkbox("🔍 Hiển thị bảng tổng hợp dữ liệu (Dành cho báo cáo)")
if show_admin:
    if st.session_state.data_store:
        df = pd.DataFrame(st.session_state.data_store)
        st.subheader("📋 Bảng thống kê kết quả")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Tải về file Excel (.csv)", data=csv, file_name="tong_hop_khao_sat_irap.csv", mime="text/csv")
    else:
        st.warning("Chưa có dữ liệu nào được gửi.")
