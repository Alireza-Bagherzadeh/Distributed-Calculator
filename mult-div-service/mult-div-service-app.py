from flask import Flask, request, jsonify
import time
app = Flask(__name__)

@app.route('/calc', methods=['POST'])
def calculate():
    time.sleep(3)
    data = request.get_json()
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
        op = data.get('op')

        if op == '*':
            res = a * b
        elif op == '/':
            if b == 0: return jsonify({"error": "Division by Zero"}), 400
            res = a / b
        else:
            return jsonify({"error": "Invalid op for MultDiv"}), 400

        return jsonify({"result": res, "service": "mult-div"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , threaded=False)




