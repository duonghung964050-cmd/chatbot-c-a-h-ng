import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

data_mau = {
    "loại tiêu tiền": ["ăn", "đi chơi", "mua đồ","xe cộ","quà","game","cá nhân","sống"],
    "tiền": [600000, 123454, 900000, 402930, 323232, 453423, 234234, 656565]
}
df_default = pd.DataFrame(data_mau)

st.subheader("Dữ liệu chi tiêu")

uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = None
# tạo web
st.set_page_config(page_title = "bờ dồ chét của hưng",layout = "wide")
st.title("con bot đơn giản")
#dữ liệu
info = {"tên":"Dương Quốc Hưng" , "tuổi" : "20" , "nghề nghiệp" : "sinh viên"}
#câu hỏi chính
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào mày! Tao là bot của hưng, mày muốn hỏi gì? (tao là ai,Lái xe, Bảng cửu chương, hay biểu đồ từ excel, biểu đồ có sẵn, đọc file excel)"}
    ]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Nếu nội dung là hình ảnh (biểu đồ) thì vẽ ra, còn lại là chữ
        if isinstance(message["content"], plt.Figure):
            st.pyplot(message["content"])
        else:
            st.markdown(message["content"])
#nhập dữ liệu
if prompt := st.chat_input('"nhập câu hỏi của mày ở đây'):
    #hiện câu hỏi
    with st.chat_message("user"):
        st.markdown(prompt)
    #lưu câu hỏi
    st.session_state.messages.append({"role":"user","content": prompt })
#câu trả lời của bot
    phản_hồi = ""
    phản_hồi_biểu_đồ = None
    #chuyển về chững thường
    low = prompt.lower()
    #câu 1
    if "lái xe" in low:
        số = re.findall(r'\d+',low)
        if số:
            tuổi = int(số[0])
            if 18<= tuổi <90:
                phản_hồi = f"{tuổi} tuổi thì dc lái xe"
            elif tuổi >=90:
                phản_hồi = f"{tuổi}tuổi này cụ nên ở nhà ạ"
            else:
                phản_hồi = f"{tuổi}tuổi này nên ở nhà đi nhóc"
        else:
            phản_hồi = "mày bao nhieu tuổi? nhập câu như: 18 tuổi lái xe được không"
    #câu 2
    elif "mày là ai" in low:
        phản_hồi = "tao là bot của hưng,mày có thể hỏi về chủ nhân tao(tên,tuổi,nghề nghiệp)"
    elif low in info:
        phản_hồi = f"{info[low]}"
    #câu 3
    elif "bảng cửu chương" in low:
        số = re.findall(r'\d+',low)
        if số:
            n = int(số[0])
            phản_hồi = f"bảng cửu chương{n}\n\n"
            for i in range(1,11):
                phản_hồi += f"{i}x{n} = {i*n} \n"
        else:
            phản_hồi = "nhập đúng cú pháp đi!!! ví dụ: bảng cửu chương 7"
    #câu 4
    elif"biểu đồ có sẵn" in low:
        fig, ax  = plt.subplots()
        ax.bar(df_default["loại tiêu tiền"], df_default ["tiền"],color = "blue")
        ax.set_title("biểu đồ loại tiêu tiền mẫu")
        phản_hồi_biểu_đồ = fig
        phản_hồi = "đây là biểu đồ mẫu"
    elif "tiền" in low or "excel" in low or "biểu đồ" in low:
        if df is not None:
            if "biểu đồ" in low:
                fig, ax  = plt.subplots()
                try:
                    ax.bar(df["loại tiêu tiền"], df ["tiền"],color = "red")
                    ax.set_title("biểu đồ loại tiêu tiền")
                    phản_hồi_biểu_đồ = fig
                    phản_hồi = "đây là biểu đồ mày cần"
                except KeyError:
                        phản_hồi = "Lỗi: Tên cột trong file Excel không đúng (cần cột 'loại tiêu tiền' và 'TIỀN')."
            else:
                st.write("Dữ liệu trong file đây:")
                st.dataframe(df)
        else:
            phản_hồi = "Tao không hiểu. Thử hỏi: 'lái xe 20 tuổi', 'bảng cửu chương 9', hoặc 'vẽ biểu đồ' xem, hoặc tao chưa dc lập trình để trả lời câu hỏi đó"
    else:
        phản_hồi = "Tao không hiểu câu hỏi của mày."
    with st.chat_message("assistant"):
        st.markdown(phản_hồi)
        if phản_hồi_biểu_đồ:
            st.pyplot(phản_hồi_biểu_đồ)
    # các câu chư thiết lập
    st.session_state.messages.append({"role": "assistant", "content": phản_hồi})
    if phản_hồi_biểu_đồ:
        pass






