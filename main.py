import subprocess
import sys
import time
from core_file import *
from send_email import generate_email_content, send_email


def main():
    python_executable = sys.executable
    subprocess.Popen([python_executable, 'core_file.py'])
    # 加载配置信息
    with open('config.yaml', 'r') as file:
        config_info = yaml.safe_load(file)
        time_gap = config_info['time_gap']
        core_file_dir = config_info['core_file_dir']
        subject = config_info['subject']
        sender_email = config_info['sender_email']
        receiver_email = config_info['receiver_email']
        smtp_server = config_info['smtp_server']
        smtp_port = config_info['smtp_port']
        sender_password = config_info['sender_password']

    while True:
        try:
            start_time = time.time()
            reload_core_files(core_file_dir)
            flag = has_new_files_in_last_time_gap(time_gap)
            if flag is True:
                print("发邮件咯")
                email_content = generate_email_content()
                send_email(
                    subject, email_content, sender_email, receiver_email, smtp_server, smtp_port, sender_password
                )
            end_time = time.time()
            time_spent = end_time - start_time
            sleep_time = max(time_gap - time_spent, 0)
            time.sleep(sleep_time)
        except Exception as e:
            print("An error occurred:", str(e))


if __name__ == '__main__':
    """
    1. 服务：启动服务
    2. 服务：定时逻辑（假定5分钟），更新当前core文件及其状态
    3. 服务：判断是否有近5分钟新增core文件，如有，触发发送邮件。
    4. 用户：点邮件链接更新状态
    """
    main()
