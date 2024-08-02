from flask import Flask, jsonify, send_from_directory
import psycopg2
import subprocess

def get_speedtest_results():
    result = subprocess.run(['speedtest', '--json'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Speedtest command failed")
    import json
    data = json.loads(result.stdout)
    download_speed = data['download'] / 1_000_000
    upload_speed = data['upload'] / 1_000_000
    return download_speed, upload_speed
    download, upload = get_speedtest_results()
    conn = psycopg2.connect(host="localhost", database="Ajith", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("INSERT INTO results (download, upload) VALUES (%s, %s)", (download, upload))
    conn.commit()
    cur.close()
    conn.close()


app = Flask(__name__)

conn = psycopg2.connect(host="localhost", database="Ajith", user="postgres", password="root")
cur = conn.cursor()
cur.execute("SELECT download, upload FROM results ORDER BY Id DESC LIMIT 1")
download, upload = cur.fetchone()
cur.close()
conn.close()
data = {
    'download': download,
    'upload': upload
}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/')
def index():
    return send_from_directory('.', 'Test.html')

if __name__ == '__main__':
    app.run(debug=True)


