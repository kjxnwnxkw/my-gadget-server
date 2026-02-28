from flask import Flask, request, render_template_string

app = Flask(__name__)

latest_title = " "
latest_message = "No messages yet"

HTML_PAGE = """
<!doctype html>
<title>My Gadget Server</title>

<h2>Send a Message</h2>

<form action="/send" method="POST">
  <p><b>Header / Subject</b></p>
  <input type="text" name="title" style="width:300px; font-size:18px;"><br><br>

  <p><b>Message</b></p>
  <textarea name="message" rows="4" style="width:300px; font-size:18px;"></textarea><br><br>

  <input type="submit" value="Send" style="font-size:18px;">
</form>

<p><b>Latest header:</b> {{ latest_title }}</p>
<p><b>Latest message:</b> {{ latest_message }}</p>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML_PAGE,
        latest_title=latest_title,
        latest_message=latest_message
    )

@app.route("/send", methods=["POST"])
def send():
    global latest_title, latest_message
    latest_title = request.form["title"]
    latest_message = request.form["message"]
    return home()

@app.route("/get")
def get_message():
    return f"{latest_title}|||{latest_message}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)