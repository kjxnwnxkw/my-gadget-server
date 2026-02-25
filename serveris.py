from flask import Flask, request, render_template_string

app = Flask(__name__)

latest_message = "No messages yet"

HTML_PAGE = """
<!doctype html>
<title>My Gadget Server</title>
<h2>Send a Message</h2>
<form action="/send" method="POST">
  <input type="text" name="message">
  <input type="submit" value="Send">
</form>
<p>Latest message: {{ latest_message }}</p>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, latest_message=latest_message)

@app.route("/send", methods=["POST"])
def send():
    global latest_message
    latest_message = request.form["message"]
    return render_template_string(HTML_PAGE, latest_message=latest_message)

@app.route("/get")
def get_message():
    return latest_message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)