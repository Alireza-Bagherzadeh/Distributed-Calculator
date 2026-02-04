from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import psycopg2
import os
import time
app = Flask(__name__)
CORS(app)
# آدرس میکروسرویس‌ها
ADD_SUB_URL = "http://add-sub-service:5000/calc"
MULT_DIV_URL = "http://mult-div-service:5000/calc"
PAREN_URL = "http://paren-service:5000/simplify"

# تنظیمات دیتابیس
DB_HOST = "postgres-master"
DB_NAME = "calculator_db"
DB_USER = "admin"
DB_PASS = "password"

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

def init_db():
    """ساخت جدول اگر وجود نداشته باشد"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS history (id SERIAL PRIMARY KEY, expression TEXT, result TEXT);')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

def save_to_db(expr, res):
    """ذخیره نتیجه در دیتابیس"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO history (expression, result) VALUES (%s, %s)', (expr, str(res)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Save Error: {e}")
@app.route('/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # دریافت ۱۰ رکورد آخر از جدول history
        cur.execute('SELECT expression, result FROM history ORDER BY id DESC LIMIT 10;')
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Save Error: {e}")
@app.route('/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # دریافت ۱۰ رکورد آخر از جدول history
        cur.execute('SELECT expression, result FROM history ORDER BY id DESC LIMIT 10;')
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # تبدیل داده‌ها به فرمت JSON برای فرانت‌ند
        history_list = [{'expression': row[0], 'result': row[1]} for row in rows]
        return jsonify(history_list)
    except Exception as e:
        print(f"History Error: {e}")
        return jsonify({"error": str(e)}), 500
def call_microservice(url, payload):
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        raise Exception(f"Service Error: {resp.text}")
    return resp.json()

def solve_flat(expr):
    tokens = re.findall(r'\d+\.?\d*|[\+\-\*\/]', expr.replace(" ", ""))
    def process(tkns, ops, url):
        i = 1
        while i < len(tkns) - 1:
            if tkns[i] in ops:
                res = call_microservice(url, {"a": tkns[i-1], "b": tkns[i+1], "op": tkns[i]})
                tkns[i-1:i+2] = [str(res["result"])]
                i = 0
            else:
                i += 1
        return tkns
    tokens = process(tokens, ['*', '/'], MULT_DIV_URL)
    tokens = process(tokens, ['+', '-'], ADD_SUB_URL)
    return float(tokens[0])

@app.route('/parse', methods=['POST'])
def parse_handler():
    # اولین بار که درخواستی می آید مطمئن میشویم جدول ساخته شده
    init_db()

    data = request.get_json()
    time.sleep(1)
    expression = data.get('expression')
    original_expr = expression # برای ذخیره در دیتابیس نگه میداریم

    try:
        if '(' in expression:
            resp = call_microservice(PAREN_URL, {"expression": expression})
            expression = resp["result"]

        result = solve_flat(expression)

        # *** ذخیره در دیتابیس ***
        save_to_db(original_expr, result)

        return jsonify({"final_result": result, "status": "success", "db_saved": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)