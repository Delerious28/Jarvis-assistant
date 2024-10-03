import os
import shutil
from flask import Flask, jsonify, request

app = Flask(__name__)  

def backup(source_folder, destination_folder):
    try:
        if not os.path.exists(source_folder):
            return {"text": f"Source folder '{source_folder}' does not exist."}

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)

        return {"text": f"Successfully backed up '{source_folder}' to '{destination_folder}'."}

    except Exception as e:
        return {"text": f"Error occurred during backup: {str(e)}"}

@app.route('/backup', methods=['POST'])
def trigger_backup():
    data = request.get_json()
    source_folder = data.get('source_folder', r'C:\Users\beaum\Desktop\Jarvis Web')
    destination_folder = data.get('destination_folder', r'C:\Users\beaum\Desktop\jarvis-backup')

    result = backup(source_folder, destination_folder) 

    return jsonify(result)  

if __name__ == '__main__':
    app.run(debug=True)  
