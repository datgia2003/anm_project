import streamlit as st
import json
from createkey import RSA_Key_Generator
from encrypt import encrypt_message, encrypt_file
from decrypt import decrypt_message, decrypt_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_with_key(sender_email, sender_password, receiver_email, subject, encrypted_message, sender_public_key):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body = f"Encrypted Message:\n{encrypted_message}\n\nSender's Public Key:\n{json.dumps(sender_public_key)}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def encrypt_and_send_message(sender_email, sender_password, receiver_email, subject, message, public_key, sender_public_key):
    encrypted_message = encrypt_message(message, public_key)
    encrypted_message_str = '\n'.join(map(str, encrypted_message))
    send_email_with_key(sender_email, sender_password, receiver_email, subject, encrypted_message_str, sender_public_key)

st.title("Chương trình RSA")

tab1, tab2, tab3, tab4= st.tabs(["Tạo khoá", "Mã hoá", "Giải mã", "Gửi tin nhắn"])

with tab1:
    st.header("Tạo khoá")
    key_size = st.selectbox("Độ dài khoá:", ["4096", "2048", "1024"])
    
    if st.button("Tạo"):
        size = int(key_size)
        key_instance = RSA_Key_Generator(size)
        public_key_path, private_key_path = key_instance.save_keys("public_key.json", "private_key.json")
    
        st.success("Khóa công khai được tạo và lưu trong file public_key.json")
        st.success("Khóa bí mật được tạo và lưu trong file private_key.json")

with tab2:
    st.header("Mã hoá")
    pub_key_file = st.file_uploader("Khoá công khai", type=["json"])
    
    data_type = st.radio("Dữ liệu:", ("File", "Văn bản"))
    data = None
    
    if data_type == "File":
        data = st.file_uploader("Chọn file")
    else:
        data = st.text_area("Nhập văn bản", key="text_area_encrypt")

    if st.button("Mã hoá"):
        if pub_key_file is None:
            st.error("Vui lòng tải lên khoá công khai.")
        else:
            pub_key = json.loads(pub_key_file.read().decode('utf-8'))
            if 'e' not in pub_key or 'n' not in pub_key:
                st.error("Khoá công khai không hợp lệ. Vui lòng kiểm tra lại.")
            else:
                if data_type == "File":
                    if data is not None:
                        data_path = data.name
                        with open(data_path, 'wb') as f:
                            f.write(data.read())
                else:
                    data_path = "text_data.txt"
                    with open(data_path, 'w', encoding='utf-8') as f:
                        f.write(data)
                
                encrypted_file_path = encrypt_file(data_path, pub_key, "encrypted_data.txt")
                st.success("Dữ liệu đã được mã hoá!")
                st.success("Lưu trong encryped_data.txt")

with tab3:
    st.header("Giải mã")
    priv_key_file = st.file_uploader("Khoá bí mật", type=["json"])
    encrypted_message = st.text_area("Tin nhắn đã mã hoá", key="text_area_decrypt")

    if st.button("Giải mã"):
        if priv_key_file is None:
            st.error("Vui lòng tải lên khoá bí mật của bạn.")
        else:
            priv_key = json.loads(priv_key_file.read().decode('utf-8'))
            if 'd' not in priv_key or 'n' not in priv_key:
                st.error("Khoá bí mật không hợp lệ. Vui lòng kiểm tra lại.")
            else:
                encrypted_message_list = list(map(int, encrypted_message.split()))
                decrypted_message = decrypt_message(encrypted_message_list, priv_key)
                st.success("Dữ liệu đã được giải mã!")
                st.text_area("Dữ liệu đã giải mã", decrypted_message, key="decrypted_data")

with tab4:
    st.header("Gửi tin nhắn")
    sender_email = st.text_input("Email của bạn")
    sender_password = st.text_input("Mật khẩu ứng dụng của bạn", type="password")
    receiver_email = st.text_input("Email người nhận")
    subject = st.text_input("Tiêu đề email")
    message = st.text_area("Tin nhắn", key="message_to_send")

    pub_key_file = st.file_uploader("Khoá công khai của người nhận", type=["json"])
    sender_pub_key_file = st.file_uploader("Khoá công khai của bạn", type=["json"])

    if st.button("Gửi tin nhắn"):
        if not sender_email or not sender_password or not receiver_email or not subject or not message or not pub_key_file or not sender_pub_key_file:
            st.error("Vui lòng điền đầy đủ thông tin và tải lên khoá công khai.")
        else:
            public_key = json.loads(pub_key_file.read().decode('utf-8'))
            sender_public_key = json.loads(sender_pub_key_file.read().decode('utf-8'))
            encrypt_and_send_message(sender_email, sender_password, receiver_email, subject, message, public_key, sender_public_key)
            st.success("Tin nhắn đã được gửi.")
