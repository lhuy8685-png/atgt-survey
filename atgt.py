import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát An toàn Giao thông - UTC", layout="wide")

st.title("📊 Phiếu Khảo sát Đánh giá An toàn Tuyến đường")
st.markdown("""
Chào bạn! Ý kiến của bạn sẽ giúp chúng tôi đánh giá mức độ an toàn của các tuyến đường trọng điểm tại Hà Nội.
*Vui lòng chọn mức độ từ **Kém** đến **Tốt** cho các mục dưới đây.*
""")

# --- 10 TIÊU CHÍ ĐÁNH GIÁ CHI TIẾT & DỄ HIỂU ---
criteria = {
    "1. Bề mặt đường": "Đường có bằng phẳng không? Có ổ gà hay bị trơn trượt không?",
    "2. Vạch kẻ đường": "Vạch sơn chia làn, vạch đi bộ có rõ nét, dễ nhìn không?",
    "3. Biển báo giao thông": "Biển báo tốc độ, biển cấm, chỉ dẫn có đặt đúng chỗ và dễ thấy không?",
    "4. Đèn chiếu sáng": "Ban đêm đèn đường có đủ sáng để nhìn rõ chướng ngại vật không?",
    "5. Dải phân cách": "Ngăn cách giữa hai chiều xe chạy có chắc chắn và an toàn không?",
    "6. Lối đi bộ & Vỉa hè": "Vỉa hè có rộng rãi, không bị lấn chiếm, có lối sang đường an toàn không?",
    "7. Phân làn xe máy": "Xe máy có làn riêng an toàn hay phải đi chung với xe tải, xe buýt?",
    "8. Điểm giao cắt (Ngõ/Ngã ba)": "Các lối ra vào ngõ nhỏ có tầm nhìn thoáng hay bị che khuất rủi ro?",
    "9. Thoát nước": "Khi trời mưa đường có bị ngập nước hay đọng nước gây nguy hiểm không?",
    "10. Cảm giác an toàn": "Tổng thể bạn cảm thấy yên tâm hay lo sợ khi đi qua đoạn đường này?"
}

star_options = ["1 ⭐ (Rất rủi ro)", "2 ⭐", "3 ⭐ (Trung bình)", "4 ⭐", "5 ⭐ (Rất an toàn)"]

with st.form("survey_form"):
    # Thông tin người tham gia
    with st.expander("👤 Thông tin người khảo sát (Không bắt buộc)"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            user_name = st.text_input("Tên của bạn:")
        with col_u2:
            vehicle = st.selectbox("Bạn thường đi qua đây bằng:", ["Xe máy", "Ô tô", "Xe đạp / Đi bộ"])

    st.write("---")
    # Hiển thị 3 đoạn đường nghiên cứu
    col1, col2, col3 = st.columns(3)

    def render_survey_column(header, key_prefix):
        st.header(header)
        for name, desc in criteria.items():
            st.write(f"**{name}**")
            st.select_slider(
                desc, 
                options=["Kém", "Tạm được", "Tốt"], 
                key=f"{key_prefix}_{name}", 
                value="Tạm được"
            )
        
        st.write("---")
        st.markdown("### 🎯 ĐÁNH GIÁ CHUNG")
        stars = st.select_slider(
            f"Mức độ an toàn tổng thể cho {header}:", 
            options=star_options, 
            key=f"{key_prefix}_stars", 
            value="3 ⭐ (Trung bình)" 
        )
        comment = st.text_area(f"Góp ý thêm cho {header}:", key=f"{key_prefix}_msg", placeholder="Ví dụ: Cần thêm đèn vàng, vỉa hè quá hẹp...")
        return stars

    with col1:
        stars_kl = render_survey_column("Hầm Kim Liên", "kl")

    with col2:
        stars_gp = render_survey_column("Đường Giải Phóng", "gp")

    with col3:
        stars_ql = render_survey_column("Quốc lộ 1A cũ", "ql")

    # Nút gửi cuối trang
    st.write("---")
    submitted = st.form_submit_button("GỬI ĐÁNH GIÁ CỦA BẠN")

if submitted:
    st.balloons()
    st.success("Cảm ơn Huy! Dữ liệu khảo sát đã được ghi nhận thành công.")
    
    # Bảng kết quả nhanh
    st.subheader("Tóm tắt đánh giá của bạn")
    summary = pd.DataFrame({
        "Tuyến đường": ["Hầm Kim Liên", "Đường Giải Phóng", "QL 1A cũ"],
        "Xếp hạng": [stars_kl, stars_gp, stars_ql]
    })
    st.table(summary)
    st.info("💡 Kết quả này sẽ được sử dụng để phân tích an toàn giao thông cho đồ án kỹ thuật.")
