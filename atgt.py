import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát iRAP - UTC", layout="wide")

st.title("📊 Khảo sát Đánh giá An toàn Giao thông theo Tiêu chuẩn iRAP")
st.markdown("""
Hệ thống tiêu chí này được xây dựng dựa trên **Sổ tay kỹ thuật iRAP**. 
Vui lòng đánh giá chi tiết các thuộc tính đường để tính toán điểm xếp hạng sao (SRS).
""")

# --- DANH SÁCH TIÊU CHÍ CHI TIẾT THEO CHUẨN IRAP ---
criteria = {
    "Loại dải phân cách": "Có dải phân cách cứng, vạch sơn hay để trống? (Phòng va chạm đối đầu)",
    "Lề đường bên phải": "Chiều rộng lề đường và vật thể cố định bên lề (Cột điện, cây cây...)",
    "Điểm giao cắt": "Tần suất các điểm giao cắt, lối ra vào nhà dân, đường nhánh?",
    "Chất lượng mặt đường": "Độ gồ ghề và sức kháng trượt (Ảnh hưởng đến quãng đường phanh)",
    "Vạch kẻ & Biển báo": "Sự hiện diện của vạch tim đường, vạch lề đường và biển báo tốc độ",
    "Tiện ích đi bộ": "Sự hiện diện của vỉa hè và các vị trí sang đường an toàn",
    "Phân làn xe máy": "Xe máy có làn riêng hay đi hỗn hợp với ô tô tải?"
}

star_options = ["1 ⭐ (Rất rủi ro)", "2 ⭐", "3 ⭐ (Đạt chuẩn)", "4 ⭐", "5 ⭐ (Rất an toàn)"]

with st.form("survey_form"):
    # Thông tin người tham gia
    with st.expander("👤 Thông tin định danh người khảo sát"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            user_name = st.text_input("Họ và tên người thực hiện:")
        with col_u2:
            vehicle = st.selectbox("Đối tượng đánh giá chính:", ["Người lái ô tô", "Người đi xe máy", "Người đi bộ"])

    st.write("---")
    # Hiển thị 3 đoạn đường nghiên cứu
    col1, col2, col3 = st.columns(3)

    # Hàm xử lý nhập liệu cho từng đoạn đường để code gọn hơn
    def render_survey_column(header, key_prefix):
        st.header(header)
        ratings = {}
        for c, desc in criteria.items():
            st.write(f"**{c}**")
            ratings[c] = st.select_slider(
                desc, 
                options=["Kém", "Trung bình", "Tốt"], 
                key=f"{key_prefix}_{c}", 
                value="Trung bình"
            )
        
        st.markdown("### 🎯 XẾP HẠNG SAO iRAP")
        stars = st.select_slider(
            "Mức độ an toàn tổng thể cho đoạn tuyến:", 
            options=star_options, 
            key=f"{key_prefix}_stars", 
            value="3 ⭐ (Trung bình)"
        )
        comment = st.text_area(f"Ghi chú hiện trường ({header}):", key=f"{key_prefix}_msg")
        return stars

    with col1:
        stars_kl = render_survey_column("1. Hầm Kim Liên", "kl")

    with col2:
        stars_gp = render_survey_column("2. Đường Giải Phóng", "gp")

    with col3:
        stars_ql = render_survey_column("3. Quốc lộ 1A cũ", "ql")

    submitted = st.form_submit_button("LƯU DỮ LIỆU KHẢO SÁT")

if submitted:
    st.success("Dữ liệu đã được ghi nhận vào hệ thống!")
    
    # Hiển thị bảng tổng hợp
    st.subheader("Bảng tóm tắt kết quả xếp hạng")
    summary = pd.DataFrame({
        "Đoạn tuyến": ["Hầm Kim Liên", "Đường Giải Phóng", "QL 1A cũ"],
        "Xếp hạng sao iRAP": [stars_kl, stars_gp, stars_ql]
    })
    st.table(summary)

    st.markdown("---")
    st.info("🙏 **Cảm ơn bạn đã đóng góp trải nghiệm. Chúc bạn một ngày may mắn và an toàn khi tham gia giao thông!**")
