import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát An toàn Giao thông", layout="wide")

# Tiêu đề ứng dụng
st.title("📊 Khảo sát Ý kiến về An toàn Giao thông Đường bộ")
st.markdown("""
Hãy dành ít phút để đánh giá mức độ an toàn của các đoạn đường. 
Dựa trên cảm nhận của bạn, hãy cho biết mức độ 'Sao' an toàn (5 sao là cao nhất).
""")

# Tiêu chí đánh giá chi tiết
criteria = {
    "Chất lượng mặt đường": "Đường bằng phẳng, không ổ gà, không trơn trượt?",
    "Hệ thống chiếu sáng": "Đèn đường đủ sáng vào ban đêm/trong hầm?",
    "Vạch kẻ & Biển báo": "Vạch chỉ dẫn, biển báo rõ ràng, dễ quan sát?",
    "Dải phân cách": "Mức độ an toàn khi phân chia các làn xe?",
    "Lối đi bộ/Xe đạp": "Vỉa hè, vạch sang đường thuận tiện và an toàn?",
}

# Tùy chọn xếp hạng sao
star_options = ["1 ⭐ (Rất nguy hiểm)", "2 ⭐", "3 ⭐ (Trung bình)", "4 ⭐", "5 ⭐ (Rất an toàn)"]

# Form khảo sát chính
with st.form("survey_form"):
    # Thông tin người tham gia (Tùy chọn)
    with st.expander("Thông tin người tham gia (Tùy chọn)"):
        user_name = st.text_input("Họ và tên:")
        vehicle = st.selectbox("Phương tiện bạn thường đi qua đây:", ["Xe máy", "Ô tô", "Xe đạp", "Đi bộ"])

    st.write("---")
    col1, col2, col3 = st.columns(3)

    # Đoạn 1: Hầm Kim Liên
    with col1:
        st.header("1. Hầm Kim Liên")
        rating_kl = {}
        for c, desc in criteria.items():
            rating_kl[c] = st.select_slider(f"**{c}**", options=["Kém", "TB", "Tốt"], key=f"kl_{c}")
        
        st.subheader("🎯 CHỐT: XẾP HẠNG SAO")
        stars_kl = st.select_slider("Mức độ an toàn tổng thể:", options=star_options, key="stars_kl", value="3 ⭐ (Trung bình)")
        comment_kl = st.text_area("Góp ý thêm cho Hầm Kim Liên:", key="comment_kl")

    # Đoạn 2: Giải Phóng (Giáp Bát - Vọng)
    with col2:
        st.header("2. Đường Giải Phóng")
        rating_gp = {}
        for c, desc in criteria.items():
            rating_gp[c] = st.select_slider(f"**{c}**", options=["Kém", "TB", "Tốt"], key=f"gp_{c}")
        
        st.subheader("🎯 CHỐT: XẾP HẠNG SAO")
        stars_gp = st.select_slider("Mức độ an toàn tổng thể:", options=star_options, key="stars_gp", value="3 ⭐ (Trung bình)")
        comment_gp = st.text_area("Góp ý thêm cho đường Giải Phóng:", key="comment_gp")

    # Đoạn 3: Quốc lộ 1A cũ
    with col3:
        st.header("3. Quốc lộ 1A cũ")
        rating_ql = {}
        for c, desc in criteria.items():
            rating_ql[c] = st.select_slider(f"**{c}**", options=["Kém", "TB", "Tốt"], key=f"ql_{c}")
        
        st.subheader("🎯 CHỐT: XẾP HẠNG SAO")
        stars_ql = st.select_slider("Mức độ an toàn tổng thể:", options=star_options, key="stars_ql", value="3 ⭐ (Trung bình)")
        comment_ql = st.text_area("Góp ý thêm cho QL 1A cũ:", key="comment_ql")

    # Nút gửi
    submitted = st.form_submit_button("Gửi đánh giá của bạn")

# Xử lý kết quả
if submitted:
    st.success("Dữ liệu của bạn đã được ghi nhận thành công!")
    
    # Hiển thị bảng tổng hợp kết quả sao
    st.subheader("Kết quả xếp hạng sao của bạn")
    res_data = {
        "Đoạn đường": ["Hầm Kim Liên", "Đường Giải Phóng", "Quốc lộ 1A cũ"],
        "Xếp hạng": [stars_kl, stars_gp, stars_ql]
    }
    st.table(pd.DataFrame(res_data))

    # LỜI CHÚC CUỐI APP
    st.markdown("---")
    st.info("🙏 **Cảm ơn bạn đã đóng góp trải nghiệm, chúc bạn một ngày may mắn và luôn an toàn khi tham gia giao thông!**")