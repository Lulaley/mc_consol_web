from flask import Flask, request, jsonify, render_template, Blueprint
import os
import subprocess
import re

app = Flask(__name__)


def generate_versions(base_version, start, end):
    """Génère une liste des versions de Minecraft de la forme base_version.start à base_version.end."""
    return [f"{base_version}.{i}" for i in range(start, end + 1)]


minecraft_1_8_versions = generate_versions("1.8", 0, 9)

java_8_path = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
java_16_path = "/usr/lib/jvm/java-16-openjdk-amd64/bin/java"
java_17_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
java_18_path = "/usr/lib/jvm/java-18-openjdk-amd64/bin/java"
# Dictionnaire pour la correspondance entre les versions de Minecraft et d'OpenJDK
minecraft_to_java_version = {
    version: java_8_path for version in minecraft_1_8_versions
}

minecraft_1_9_versions = generate_versions("1.9", 0, 5)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_9_versions
})

minecraft_1_10_versions = generate_versions("1.10", 0, 2)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_10_versions
})

minecraft_1_11_versions = generate_versions("1.11", 0, 2)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_11_versions
})

minecraft_1_12_versions = generate_versions("1.12", 0, 2)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_12_versions
})

minecraft_1_13_versions = generate_versions("1.13", 0, 2)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_13_versions
})

minecraft_1_14_versions = generate_versions("1.14", 0, 4)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_14_versions
})

minecraft_1_15_versions = generate_versions("1.15", 0, 2)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_15_versions
})

minecraft_1_16_versions = generate_versions("1.16", 0, 5)
minecraft_to_java_version.update({
    version: java_8_path for version in minecraft_1_16_versions
})

minecraft_1_17_versions = generate_versions("1.17", 0, 1)
minecraft_to_java_version.update({
    version: java_16_path for version in minecraft_1_17_versions
})

minecraft_1_18_versions = generate_versions("1.18", 0, 2)
minecraft_to_java_version.update({
    version: java_17_path for version in minecraft_1_18_versions
})

minecraft_1_19_versions = generate_versions("1.19", 0, 4)
minecraft_to_java_version.update({
    version: java_17_path for version in minecraft_1_19_versions
})

minecraft_1_20_versions = generate_versions("1.20", 0, 2)
minecraft_to_java_version.update({
    version: java_17_path for version in minecraft_1_20_versions
})

java_control_bp = Blueprint('java_control', __name__)


@java_control_bp.route('/')
def index():
    java_version_output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True)
    # Extraire le numéro de version
    match = re.search(r'openjdk version "(\d+\.\d+\.\d+)', java_version_output)
    if match:
        java_version = match.group(1)
    else:
        java_version = "inconnue"
    return render_template("select_version.html", minecraft_versions=minecraft_to_java_version.keys(), java_version=java_version)


@java_control_bp.route('/set_java_version', methods=['POST'])
def set_java_version():
    minecraft_version = request.form.get('minecraft_version')

    java_path = minecraft_to_java_version.get(minecraft_version)

    if not java_path:
        return render_template("select_version.html", minecraft_versions=minecraft_to_java_version.keys(), java_version=java_version)

    # Changer la version d'OpenJDK
    command = f"sudo update-alternatives --set java {java_path}"
    subprocess.run(command, shell=True)

    java_version_output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True)
    match = re.search(r'openjdk version "(\d+\.\d+\.\d+)', java_version_output)
    if match:
        java_version = match.group(1)
    else:
        java_version = "inconnue"
    
    return render_template("select_version.html", minecraft_versions=minecraft_to_java_version.keys(), java_version=java_version)


if __name__ == '__main__':
    app.run(debug=True)

    