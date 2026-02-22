from flask import Flask, request, jsonify

app = Flask(__name__)

# Stored message state
state = {
    "msg": "",
    "beep": True,
    "duration": 20
}

@app.route("/send")
def send():
    global state
    msg = request.args.get("msg", "")
    beep = request.args.get("beep", "1") == "1"
    duration = int(request.args.get("duration", "20"))

    state["msg"] = msg
    state["beep"] = beep
    state["duration"] = duration

    return "OK"

@app.route("/get")
def get():
    return jsonify(state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)