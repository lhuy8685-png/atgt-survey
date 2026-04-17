import streamlit as st
import pandas as pd
import time

# Cấu hình trang
st.set_page_config(page_title="Khảo sát iRAP - UTC", layout="wide")

# --- PHẦN HIỂN THỊ LOGO (DÙNG HTML ĐỂ CỐ ĐỊNH) ---
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/vi/8/81/Logo_dh_giaothongvantai.png" width="80" style="margin-right: 20px;">
        <div>
            <h2 style="margin: 0;">TRƯỜNG ĐẠI HỌC GIAO THÔNG VẬN TẢI</h2>
            <h3 style="margin: 0; color: #555;">KHOA CÔNG TRÌNH</h3>
        </div>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# Khởi tạo bộ nhớ tạm để lưu dữ liệu
if 'data_store' not in st.session_state:
    st.session_state.data_store = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- HÀM XỬ LÝ KHI GỬI ĐÁNH GIÁ ---
def submit_survey():
    st.session_state.submitted = True

# --- GIAO DIỆN CHÍNH ---
placeholder = st.empty()

if not st.session_state.submitted:
    with placeholder.container():
        st.title("📊 Phiếu Khảo sát Đánh giá An toàn Tuyến đường")
        st.info("👋 Chào bạn! Cảm ơn bạn đã dành thời gian tham gia khảo sát đóng góp cho đồ án nghiên cứu iRAP của chúng tôi.")
        
        # Form nhập liệu
        with st.form("survey_form"):
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                user_name = st.text_input("Họ tên người khảo sát:", placeholder="Nhập tên...")
            with col_u2:
                user_age = st.number_input("Độ tuổi của bạn:", min_value=5, max_value=100, value=20)
            with col_u3:
                user_type = st.selectbox("Bạn tham gia giao thông bằng:", ["Người đi bộ", "Xe máy", "Ô tô"])
            
            st.write("---")
            st.subheader("📝 Đánh giá các tiêu chí kỹ thuật")
            
            # Danh sách tiêu chí
            criteria = ["Bề mặt đường", "Vạch kẻ & Biển báo", "Chiếu sáng", "Dải phân cách", "Vỉa hè/Lề đường"]
            star_options = ["1 ⭐", "2 ⭐", "3 ⭐", "4 ⭐", "5 ⭐"]
            
            col1, col2, col3 = st.columns(3)
            
            def render_section(title, key_p):
                st.markdown(f"#### 📍 {title}")
                res = {}
                for c in criteria:
                    res[c] = st.select_slider(f"{c}:", options=["Kém", "Tạm được", "Tốt"], key=f"{key_p}_{c}", value="Tạm được")
                st.write("---")
                stars = st.select_slider(f"Xếp hạng tổng thể {title}:", options=star_options, key=f"{key_p}_s", value="3 ⭐")
                return stars, res

            with col1: s_kl, r_kl = render_section("Hầm Kim Liên", "kl")
            with col2: s_gp, r_gp = render_section("Đường Giải Phóng", "gp")
            with col3: s_ql, r_ql = render_section("QL 1A cũ", "ql")

            submitted = st.form_submit_button("GỬI ĐÁNH GIÁ NGAY", on_click=submit_survey)
            
            if submitted:
                # Lưu dữ liệu vào session_state
                st.session_state.data_store.append({
                    "Họ tên": user_name,
                    "Tuổi": user_age,
                    "Phương tiện": user_type,
                    "Hầm Kim Liên": s_kl,
                    "Đường Giải Phóng": s_gp,
                    "QL 1A cũ": s_ql
                })

else:
    # --- MÀN HÌNH CẢM ƠN (CHUYỂN ĐỘNG) ---
    with placeholder.container():
        st.balloons()
        st.success("🎉 Gửi thành công!")
        st.markdown(f"""
            <div style="text-align: center; padding: 50px;">
                <h1>🙏 Chân thành cảm ơn bạn!</h1>
                <p style="font-size: 20px;">Những ý kiến đóng góp quý báu của bạn sẽ giúp đồ án iRAP của chúng tôi hoàn thiện hơn.</p>
                <p>Chúc bạn có một ngày tham gia giao thông an toàn!</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Thực hiện đánh giá mới"):
            st.session_state.submitted = False
            st.rerun()

# --- PHẦN QUẢN TRỊ DỮ LIỆU (ẨN Ở DƯỚI) ---
st.write("---")
with st.expander("🔍 Dành cho người quản trị: Xem tổng hợp kết quả"):
    if st.session_state.data_store:
        df = pd.DataFrame(st.session_state.data_store)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Tải về file Excel (.csv)", data=csv, file_name="du_lieu_irap_utc.csv")
    else:
        st.info("Chưa có dữ liệu đánh giá nào được lưu.")
