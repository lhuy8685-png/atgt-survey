import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Khảo sát iRAP - UTC", layout="wide")

# --- PHẦN 1: LOGO VÀ TIÊU ĐỀ KHOA ---
st.markdown(
    """
    <div style="display: flex; align-items: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/vi/8/81/Logo_dh_giaothongvantai.png" width="80" style="margin-right: 20px;">
        <div>
            <h2 style="margin: 0; color: #004a99;">TRƯỜNG ĐẠI HỌC GIAO THÔNG VẬN TẢI</h2>
            <h3 style="margin: 0; color: #333;">KHOA CÔNG TRÌNH</h3>
        </div>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# Khởi tạo bộ nhớ tạm để lưu dữ liệu
if 'data_store' not in st.session_state:
    st.session_state.data_store = []
if 'page' not in st.session_state:
    st.session_state.page = "survey"

# --- DANH SÁCH 10 TIÊU CHÍ ĐÁNH GIÁ CHI TIẾT ---
criteria = {
    "1. Bề mặt đường": "Đường có bằng phẳng không? Có ổ gà hay bị trơn trượt không?",
    "2. Vạch kẻ đường": "Vạch sơn chia làn, vạch đi bộ có rõ nét, dễ nhìn không?",
    "3. Biển báo giao thông": "Biển báo tốc độ, biển cấm có đặt đúng chỗ và dễ thấy không?",
    "4. Đèn chiếu sáng": "Ban đêm đèn đường có đủ sáng để nhìn rõ đường đi không?",
    "5. Dải phân cách": "Hàng rào ngăn cách giữa hai chiều xe chạy có an toàn không?",
    "6. Lối đi bộ & Vỉa hè": "Vỉa hè có rộng rãi, không bị lấn chiếm để đi bộ an toàn không?",
    "7. Phân làn xe": "Xe máy có làn riêng hay phải đi chung với ô tô lớn (xe tải, xe buýt)?",
    "8. Tầm nhìn giao cắt": "Tại các ngõ nhỏ, tầm nhìn có thoáng hay bị che khuất rủi ro?",
    "9. Thoát nước": "Khi trời mưa đường có bị ngập hay đọng nước gây nguy hiểm không?",
    "10. Cảm giác an toàn": "Tổng thể bạn cảm thấy yên tâm hay lo sợ khi đi qua đoạn đường này?"
}

star_options = ["1 ⭐ (Rất rủi ro)", "2 ⭐", "3 ⭐ (Trung bình)", "4 ⭐", "5 ⭐ (Rất an toàn)"]

# --- PHẦN 2: GIAO DIỆN KHẢO SÁT ---
if st.session_state.page == "survey":
    st.title("📊 Phiếu Khảo sát Đánh giá An toàn Tuyến đường")
    st.info("👋 **Lời chào:** Chào bạn! Cảm ơn bạn đã dành thời gian tham gia khảo sát. Ý kiến thực tế của bạn là dữ liệu quý giá cho đồ án nghiên cứu về An toàn giao thông (tiêu chuẩn iRAP) của chúng tôi tại Đại học Giao thông Vận tải.")

    with st.form("survey_form"):
        # Thông tin người dùng
        st.subheader("👤 Thông tin người khảo sát")
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("Họ và tên:", placeholder="Nhập tên của bạn...")
        with c2:
            u_age = st.number_input("Độ tuổi:", min_value=1, max_value=100, value=20)
        with c3:
            u_vehi = st.selectbox("Phương tiện di chuyển chính:", ["Xe máy", "Ô tô", "Người đi bộ", "Xe đạp"])

        st.write("---")
        st.subheader("📝 Đánh giá chi tiết các tuyến đường")
        st.caption("Hãy chọn mức độ từ **Kém** đến **Tốt** dựa trên trải nghiệm của bạn tại mỗi khu vực.")

        col1, col2, col3 = st.columns(3)

        def render_route(header, key_p):
            st.markdown(f"### 📍 {header}")
            results = {}
            for name, desc in criteria.items():
                st.write(f"**{name}**")
                results[name] = st.select_slider(desc, options=["Kém", "Tạm được", "Tốt"], key=f"{key_p}_{name}", value="Tạm được")
            st.write("---")
            stars = st.select_slider(f"Xếp hạng sao tổng thể cho {header}:", options=star_options, key=f"{key_p}_s", value="3 ⭐ (Trung bình)")
            return stars

        with col1: s_kl = render_route("Hầm Kim Liên", "kl")
        with col2: s_gp = render_route("Đường Giải Phóng", "gp")
        with col3: s_ql = render_route("Quốc lộ 1A cũ", "ql")

        st.write("---")
        submitted = st.form_submit_button("GỬI ĐÁNH GIÁ CỦA BẠN")

        if submitted:
            # Lưu dữ liệu vào hệ thống tạm thời
            st.session_state.data_store.append({
                "Họ tên": u_name,
                "Tuổi": u_age,
                "Phương tiện": u_vehi,
                "Hầm Kim Liên (Sao)": s_kl,
                "Đường Giải Phóng (Sao)": s_gp,
                "QL 1A cũ (Sao)": s_ql
            })
            st.session_state.page = "thanks"
            st.rerun()

# --- PHẦN 3: MÀN HÌNH CẢM ƠN (CHUYỂN ĐỘNG) ---
elif st.session_state.page == "thanks":
    st.balloons()
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 40px; border: 2px solid #004a99; border-radius: 15px;">
            <h1 style="color: #004a99;">🙏 XIN CHÂN THÀNH CẢM ƠN!</h1>
            <p style="font-size: 22px;">Kết quả đánh giá của bạn đã được ghi nhận thành công.</p>
            <p style="font-size: 18px; color: #555;">Những đóng góp này sẽ giúp ích rất nhiều cho việc phân tích an toàn hạ tầng giao thông trong đồ án của chúng tôi.</p>
            <p style="font-weight: bold; color: #004a99;">Chúc bạn luôn an toàn trên mọi nẻo đường!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Thực hiện lượt đánh giá mới"):
        st.session_state.page = "survey"
        st.rerun()

# --- PHẦN 4: CÔNG CỤ TỔNG HỢP DỮ LIỆU (DÀNH CHO BÁO CÁO) ---
st.write("---")
with st.expander("🔍 Dành cho người quản trị: Tổng hợp và Xuất dữ liệu"):
    if st.session_state.data_store:
        df = pd.DataFrame(st.session_state.data_store)
        st.write("### Danh sách các lượt khảo sát đã thực hiện:")
        st.dataframe(df, use_container_width=True)
        
        # Nút tải file Excel/CSV phục vụ báo cáo đồ án
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải toàn bộ kết quả về Excel (.csv)",
            data=csv,
            file_name="tong_hop_khao_sat_irap_utc.csv",
            mime="text/csv"
        )
    else:
        st.info("Hiện chưa có dữ liệu nào được gửi trong phiên làm việc này.")
