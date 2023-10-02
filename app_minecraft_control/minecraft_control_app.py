from flask import Flask, request, jsonify, Blueprint, render_template, redirect
from mcrcon import MCRcon
import threading
import signal
import os

app = Flask(__name__)

minecraft_control_bp = Blueprint('minecraft_control', __name__)


@minecraft_control_bp.route('/')
def redirect_to_amp():
    return redirect("http://192.168.160.5:8080", code=302)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
