#!/bin/bash

source /home/chimea/Bureau/mc_consol_web/set_up_minecraft/fabric_installer.sh
source /home/chimea/Bureau/mc_consol_web/set_up_minecraft/forge_installer.sh
source /home/chimea/Bureau/mc_consol_web/set_up_minecraft/install_java.sh

install_jdk() {
    if minecraft_jdk -eq "forge"; then
        install_forge minecraft_version
    elif minecraft_jdk -eq "fabric"; then
        install_fabric minecraft_version
    else
        echo "Version de JDK non reconnue ou non prise en charge."
    fi
}

switch_java_version() {
    local minecraft_version="$1"
    local minecraft_jdk="$2"

    echo "$minecraft_jdk"
    echo "$minecraft_version"

    case "$minecraft_version" in
        1.7.10|1.8.9|1.9.4|1.10.2|1.11.2|1.12.2|1.13.2|1.14.4|1.15.2|1.16.5)
            install_java_8
            case "$minecraft_version" in
            1.7.10|1.8.9|1.9.4|1.10.2|1.11.2|1.12.2)
                install_jdk
                ;;
            1.13.2|1.14.4|1.15.2|1.16.5)
                install_jdk
                ;;
            esac
            ;;
        1.17.*)
            install_java_16
            install_jdk
            ;;
        1.18.*|1.19.*|1.20.*)
            install_java_17
            install_jdk
            ;;
        *)
            echo "Version de Minecraft non reconnue ou non prise en charge."
            ;;
    esac
}

echo "Démarrage du téléchargement de Minecraft $1 avec $2"
switch_java_version $1 $2
