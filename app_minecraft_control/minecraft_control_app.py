from flask import Flask, request, jsonify, Blueprint, render_template
import mcrcon

app = Flask(__name__)

minecraft_control_bp = Blueprint('minecraft_control', __name__)

@minecraft_control_bp.route('/send_command', methods=['POST'])
def send_command():
    command = request.json.get('command')
    with mcrcon.MCRcon("localhost", "your_password") as mcr:
        response = mcr.command(command)
        return jsonify({"response": response})


@minecraft_control_bp.route('/')
def menu():
    return render_template('minecraft.html', apps=app)


if __name__ == '__main__':
    app.run(debug=True)
