from flask import Flask, render_template
from app_gestionnaire_control.gestionnaire_control_app import gestionnaire_control_bp
from app_java_control.java_control_app import java_control_bp
from app_minecraft_control.minecraft_control_app import minecraft_control_bp

app = Flask(__name__)

app.register_blueprint(gestionnaire_control_bp, url_prefix='/gestionnaire_control')
app.register_blueprint(java_control_bp, url_prefix='/java_control')
app.register_blueprint(minecraft_control_bp, url_prefix='/minecraft_control')

@app.route('/')
def menu():
    apps = [
        {'name': 'Gestionnaire App', 'url': '/gestionnaire_control'},
        {'name': 'Java Control', 'url': '/java_control'},
        {'name': 'Minecraft Control', 'url': '/minecraft_control'}
    ]
    return render_template('menu.html', apps=apps)

if __name__ == '__main__':
    app.run(debug=True)
    