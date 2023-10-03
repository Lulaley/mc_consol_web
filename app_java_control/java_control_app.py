from flask import Flask, request, jsonify, render_template, Blueprint
import os
import subprocess
import re
import requests

app = Flask(__name__)


def generate_versions(base_version, start, end):
    """Génère une liste des versions de Minecraft de la forme base_version.start à base_version.end."""
    return [f"{base_version}.{i}" for i in range(start, end + 1)]


minecraft_1_8_versions = generate_versions("1.8", 0, 9)

# Dictionnaire pour la correspondance entre les versions de Minecraft, d'OpenJDK et du serveur à exécuter
java_8_path = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
java_16_path = "/usr/lib/jvm/java-16-openjdk-amd64/bin/java"
java_17_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
java_18_path = "/usr/lib/jvm/java-18-openjdk-amd64/bin/java"

minecraft_data = {}

versions_data = [
    {"range": (1, 8, 0, 9), "java": java_8_path},
    {"range": (1, 9, 0, 5), "java": java_8_path},
    {"range": (1, 10, 0, 2), "java": java_8_path},
    {"range": (1, 11, 0, 2), "java": java_8_path},
    {"range": (1, 12, 0, 2), "java": java_8_path},
    {"range": (1, 13, 0, 2), "java": java_8_path},
    {"range": (1, 14, 0, 4), "java": java_8_path},
    {"range": (1, 15, 0, 2), "java": java_8_path},
    {"range": (1, 16, 0, 5), "java": java_8_path},
    # ... ajoutez d'autres plages de versions ici
    {"range": (1, 17, 0, 1), "java": java_16_path},
    {"range": (1, 18, 0, 2), "java": java_17_path},
    {"range": (1, 19, 0, 2), "java": java_17_path},
    {"range": (1, 20, 0, 2), "java": java_17_path},
]

for version_info in versions_data:
    major, minor, start, end = version_info["range"]
    for i in range(start, end + 1):
        version_str = f"{major}.{minor}.{i}" if i != 0 else f"{major}.{minor}"
        minecraft_data[version_str] = {
            "java_path": version_info["java"],
            "path": f"/home/chimea/Bureau/server_{version_str}/server.jar",
            "url": f"https://www.mc-download.com/downloadfile.php?filename=minecraft_server.{version_str}.jar&directory=Minecraft%20Versions%20Official/Minecraft%20Server"
        }


def download_server(version):
    print(version)
    data = minecraft_data.get(version)
    print(data)
    if not data:
        return False

    os.makedirs(os.path.dirname(data["path"]), exist_ok=True)

    response = requests.get(data["url"])
    with open(data["path"], "wb") as f:
        f.write(response.content)
    return True


def get_java_version():
    java_version_output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True)
    match = re.search(r'openjdk version "(\d+\.\d+\.\d+)', java_version_output)
    if match:
        java_version = match.group(1)
    else:
        java_version = "inconnue"
    return java_version


def is_minecraft_server_running():
    """Vérifie si un serveur Minecraft est en cours d'exécution dans une session screen."""
    try:
        output = subprocess.check_output(['screen', '-ls'], universal_newlines=True)
        return 'mc' in output  # 'mc' est le nom de la session screen
    except Exception as e:
        print(f"Erreur lors de la vérification du serveur Minecraft: {e}")
        return False


def stop_minecraft_server():
    """Arrête le serveur Minecraft s'il est en cours d'exécution dans une session screen."""
    try:
        command = ['screen', '-S', 'mc', '-p', '0', '-X', 'stuff', 'quit\n']
        subprocess.run(command)
    except Exception as e:
        print(f"Erreur lors de l'arrêt du serveur Minecraft: {e}")


def start_minecraft_server(version):
    """Démarre le serveur Minecraft avec la version spécifiée dans une session screen."""
    java_path = minecraft_data[version]["java_path"]
    server_path = minecraft_data[version]["path"]

    command = f'screen -dmR mc {java_path} -jar {server_path} nogui'
    subprocess.run(command, shell=True)


html_page = "select_version.html"
java_control_bp = Blueprint('java_control', __name__)


@java_control_bp.route('/')
def index():
    server_version = request.form.get('minecraft_server_version')
    return render_template(html_page, minecraft_versions=minecraft_data.keys(), java_version=get_java_version(), current_mc_version=server_version)


@java_control_bp.route('/set_java_version', methods=['POST'])
def set_java_version():
    server_version = request.form.get('minecraft_server_version')
    minecraft_version = request.form.get('minecraft_version')

    version_data = minecraft_data.get(minecraft_version)
    if not version_data:
        java_version = "Erreur lors du téléchargement du serveur"
        return render_template(html_page, minecraft_versions=minecraft_data.keys(), java_version=java_version, current_mc_version=server_version)

    java_path = version_data["java_path"]

    # Changer la version d'OpenJDK
    command = f"sudo update-alternatives --set java {java_path}"
    subprocess.run(command, shell=True)

    if server_version is None:
        server_version = minecraft_version
    if not os.path.exists(minecraft_data[minecraft_version]["path"]):
        success = download_server(server_version)
        if not success:
            server_version = "Erreur lors du téléchargement du serveur"
            return render_template(html_page, minecraft_versions=minecraft_data.keys(), java_version=get_java_version(), current_mc_version=server_version)

    print(minecraft_data[minecraft_version]['path'])
    server_command = f"screen -R mc -dm java -jar {minecraft_data[minecraft_version]['path']}"
    subprocess.Popen(server_command, shell=True)
    return render_template(html_page, minecraft_versions=minecraft_data.keys(), java_version=get_java_version(), current_mc_version=server_version)


if __name__ == '__main__':
    app.run(debug=True)

    