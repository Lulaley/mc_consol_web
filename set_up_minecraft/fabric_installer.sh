#!/bin/bash

install_fabric() {
    # Version variables (change these to the versions you want)
    if [ $# -gt 0 ]; then
        MC_VERSION=$1
        FABRIC_INSTALLER_VERSION=$2
    else
        MC_VERSION="1.17.1"
        FABRIC_INSTALLER_VERSION="0.7.4"
    fi

    # Create directory for Minecraft server and move into it
    mkdir minecraft_fabric_server
    cd minecraft_fabric_server

    # Download the Fabric installer
    wget "https://maven.fabricmc.net/net/fabricmc/fabric-installer/${FABRIC_INSTALLER_VERSION}/fabric-installer-${FABRIC_INSTALLER_VERSION}.jar"

    # Install the Fabric server
    java -jar "fabric-installer-${FABRIC_INSTALLER_VERSION}.jar" server -downloadMinecraft

    # Remove installer files (optional)
    rm "fabric-installer-${FABRIC_INSTALLER_VERSION}.jar"

    # Display message to indicate completion
    echo "Fabric server setup complete!"
}
