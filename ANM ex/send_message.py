import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from encrypt import encrypt_message

def send_email_with_key(sender_email, sender_password, receiver_email, subject, encrypted_message, public_key):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Tạo phần nội dung email chứa tin nhắn mã hóa và khóa công khai
    body = f"Encrypted Message:\n{encrypted_message}\n\nPublic Key:\n{json.dumps(public_key)}"
    msg.attach(MIMEText(body, 'plain'))

    # Thiết lập máy chủ SMTP và gửi email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def encrypt_and_send_message(sender_email, sender_password, receiver_email, subject, message, public_key):
    encrypted_message = encrypt_message(message, public_key)
    send_email_with_key(sender_email, sender_password, receiver_email, subject, encrypted_message, public_key)

if __name__ == "__main__":
    sender_email = input("Nhập email của bạn: ")
    sender_password = input("Nhập mật khẩu ứng dụng của bạn: ")
    receiver_email = input("Nhập email người nhận: ")
    subject = input("Nhập tiêu đề email: ")
    message = input("Nhập tin nhắn: ")

    # Tải khóa công khai của người nhận từ file
    public_key_path = input("Nhập đường dẫn tới file khóa công khai của người nhận: ")
    with open(public_key_path, 'r', encoding='utf-8') as f:
        public_key = json.loads(f.read())

    encrypt_and_send_message(sender_email, sender_password, receiver_email, subject, message, public_key)
    print("Tin nhắn đã được gửi.")
