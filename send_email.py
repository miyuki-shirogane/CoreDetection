from core_file import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_email_content():
    with app.app_context():
        files = get_unprocessed_files()
        email_content = "以下是待处理的core文件列表：\n\n"
        for file in files:
            file_info = f"{file.name}, {file.created_time}"
            process_link = f'{url_for("process_file", filename=file.name)}'
            email_content += f"""\
<html>
  <body>
    <p>{file_info}<a href="{process_link}" style="color:blue;"><span style="font-weight:bold;">阅</span></a></p>
  </body>
</html>
"""
        return email_content


def send_email(subject, body, sender_email, receiver_email, smtp_server, smtp_port, sender_password):
    # 创建 MIMEMultipart 对象，并设置邮件头
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    # 使用 SMTP 发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)




