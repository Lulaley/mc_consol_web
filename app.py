from flask import Flask, render_template, redirect, url_for, request
import os
import subprocess

app = Flask(__name__)

def screen_session_exists(session_name):
    try:
        output = subprocess.check_output("screen -ls", shell=True).decode("utf-8")
        return session_name in output
    except subprocess.CalledProcessError:
        return False
        
@app.route("/")
def index():
    http_button_state = "disabled" if screen_session_exists("http_server") else "enable"
    ttyd_button_state = "disabled" if screen_session_exists("ttyd_server") else "enable"
    message = request.args.get('message', default=None)
    return render_template('index.html', http_button_state=http_button_state, ttyd_button_state=ttyd_button_state, message=message)


@app.route("/start_http_server")
def start_http_server():
    if not screen_session_exists("http_server"):
        os.system("screen -S http_server -dm python3 -m http.server 8000")
        message = "Serveur HTTP démarré!"
    else:
        message = "Serveur HTTP déjà en cours d'exécution!"
    return redirect(url_for('index', message=message))


@app.route("/stop_http_server")
def stop_http_server():
    if screen_session_exists("http_server"):
        os.system("screen -X -S http_server quit")
        message = "Serveur HTTP arrêté!"
    else:
        message = "Serveur 'HTTP' non trouvé!"
    return redirect(url_for('index', message=message))

@app.route("/start_ttyd_server")
def start_ttyd_server():
    if not screen_session_exists("ttyd_server"):
        os.system("screen -S ttyd_server -dm ttyd --allowed-origins='http://127.0.0.1:5000' -p 8080 screen -S serveur")
        message = "Serveur 'TTYD' démarré!"
    else:
        os.system("screen -R serveur")
        message = "Serveur 'TTYD' déjà en cours d'exécution!"
    return redirect(url_for('index', message=message))

@app.route("/stop_ttyd_server")
def stop_ttyd_server():
    if screen_session_exists("ttyd_server"):
        os.system("screen -X -S ttyd_server quit")
        message = "Serveur TTYD arrêté!"
    else:
        message = "Serveur TTYD non trouvé!"
    return redirect(url_for('index', message=message))

if __name__ == "__main__":
    app.run(debug=True)
    