from flask import Flask, request, render_template_string

app = Flask(__name__)

# -----------------------------
# Messages to ESP32
# -----------------------------
latest_title = " "
latest_message = "No messages yet"

# -----------------------------
# Remote messages from ESP32
# -----------------------------
latest_remote = ""
remote_counter = 0

HTML_PAGE = """
<!doctype html>
<html>

<head>
    <title>My Gadget Server</title>
</head>

<body>

<h2>Send a Message</h2>

<form action="/send" method="POST">
  <p><b>Header / Subject</b></p>
  <input type="text" name="title" style="width:300px; font-size:18px;"><br><br>

  <p><b>Message</b></p>
  <textarea name="message" rows="4" style="width:300px; font-size:18px;"></textarea><br><br>

  <input type="submit" value="Send" style="font-size:18px;">
</form>

<hr>

<h2>Latest Remote Button</h2>

<p id="remote" style="font-size:28px; color:blue;">
    {{ latest_remote }}
</p>

<hr>

<p><b>Latest header:</b> {{ latest_title }}</p>
<p><b>Latest message:</b> {{ latest_message }}</p>

<script>
async function updateRemote() {
    try {
        const response = await fetch("/get_remote");
        const text = await response.text();

        const parts = text.split("|||");

        if(parts.length > 1){
            document.getElementById("remote").innerText = parts[1];
        }
    }
    catch(err){
        console.log(err);
    }
}

// Update every second
setInterval(updateRemote,1000);

// Update immediately when page opens
updateRemote();

</script>

</body>
</html>
"""

# ---------------------------------------
# Home page
# ---------------------------------------
@app.route("/")
def home():
    return render_template_string(
        HTML_PAGE,
        latest_title=latest_title,
        latest_message=latest_message,
        latest_remote=latest_remote
    )

# ---------------------------------------
# Send message to ESP32
# ---------------------------------------
@app.route("/send", methods=["POST"])
def send():
    global latest_title, latest_message

    latest_title = request.form["title"]
    latest_message = request.form["message"]

    return home()

# ---------------------------------------
# ESP32 reads latest message
# ---------------------------------------
@app.route("/get")
def get_message():
    return f"{latest_title}|||{latest_message}"

# ---------------------------------------
# ESP32 sends remote button
# ---------------------------------------
@app.route("/remote", methods=["POST"])
def remote():
    global latest_remote, remote_counter

    latest_remote = request.form["button"]
    remote_counter += 1

    print("Remote:", latest_remote)

    return "OK"

# ---------------------------------------
# Browser reads latest remote button
# ---------------------------------------
@app.route("/get_remote")
def get_remote():
    return f"{remote_counter}|||{latest_remote}"

# ---------------------------------------
# Run
# ---------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
