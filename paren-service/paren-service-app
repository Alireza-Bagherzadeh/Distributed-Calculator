from flask import Flask, request, jsonify
import requests
import re
import sys
import time
app = Flask(__name__)

# آدرس پارسر برای حل محتویات داخل پرانتز
PARSER_URL = "http://parser-service:5000/parse"

@app.route('/simplify', methods=['POST'])
def simplify():
    time.sleep(3)
    data = request.get_json()
    expr = data.get('expression')
    print(f"DEBUG: Paren service received: {expr}", file=sys.stderr)

    try:
        # پیدا کردن پرانتزهای داخلی
        while '(' in expr:
            match = re.search(r'\(([^()]+)\)', expr)
            if not match:
                break

            inner = match.group(1) # مثلا "100 + 5"
            full = match.group(0)  # مثلا "(100 + 5)"

            print(f"DEBUG: Found parenthesis: {inner}", file=sys.stderr)

            # ارسال به پارسر برای حل کردن داخل پرانتز
            # نکته: ما فقط عبارت داخل را میفرستیم
            resp = requests.post(PARSER_URL, json={"expression": inner})

            if resp.status_code != 200:
                 print(f"ERROR: Parser returned {resp.status_code}", file=sys.stderr)
                 raise Exception("Error contacting parser")

            # پارسر ممکن است "final_result" برگرداند (طبق کد جدید v3)
            res_json = resp.json()
            val = res_json.get("final_result")

            # جایگزینی در رشته اصلی
            expr = expr.replace(full, str(val))
            print(f"DEBUG: New expression: {expr}", file=sys.stderr)

        return jsonify({"result": expr, "status": "success"})

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False)