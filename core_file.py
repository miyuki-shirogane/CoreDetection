import os
from datetime import datetime, timedelta

import yaml
from flask import Flask, url_for
from flask_cors import CORS

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:7777'
CORS(
    app,
    origins='http://localhost:8080',
    supports_credentials=True,
    methods=['GET', 'POST', 'OPTIONS'],
    headers=['Content-Type', 'Authorization']
)


class CoreFile:
    def __init__(self, name, created_time, status="unprocessed"):
        self.name = name
        self.created_time = created_time
        self.status = status


def load_files():
    with open('core_files_info.yaml', 'r') as file:
        return yaml.safe_load(file)


def save_files(files):
    # 将文件列表保存到 YAML 文件中
    with open('core_files_info.yaml', 'w') as file:
        yaml.dump(files, file)


def update_file_status(filename, status):
    # 更新文件状态
    files = load_files()
    for file in files:
        if file['name'] == filename:
            file['status'] = status
    save_files(files)


def get_unprocessed_files():
    # 获取未处理的文件列表
    files = load_files()
    return [
        CoreFile(file['name'], file['created_time'], file['status'])
        for file in files
        if file['status'] == 'unprocessed'
    ]


def has_new_files_in_last_time_gap(time_out: int):
    files = load_files()
    if files is None:
        return False

    current_time = datetime.now()
    time_gap_ago = current_time - timedelta(seconds=time_out)
    return any(
        datetime.fromisoformat(file['created_time']) >= time_gap_ago
        for file in files
        if file['status'] == 'unprocessed'
    )


@app.route('/process/<filename>')
def process_file(filename):
    update_file_status(filename, 'processed')
    return f"File {filename} processed successfully."


def reload_core_files(directory):
    files = load_files()
    if files is None:
        files = []
    existing_files = [f for f in os.listdir(directory) if f.startswith('core')]
    if not existing_files:
        return
    for filename in existing_files:
        if not any(file['name'] == filename for file in files):
            file_path = os.path.join(directory, filename)
            file_stat = os.stat(file_path)
            created_time = datetime.fromtimestamp(file_stat.st_ctime)
            file_data = {
                'name': filename, 'created_time': created_time.strftime('%Y-%m-%d %H:%M:%S'), 'status': 'unprocessed'
            }
            files.append(file_data)
    save_files(files)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
