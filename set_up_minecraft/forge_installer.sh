#!/bin/bash

install_forge() {
    # Version variables (change these to the versions you want)
    if [ $# -gt 0 ]; then
        MC_VERSION=$1
        FORGE_VERSION=$2
    else
        MC_VERSION="1.17.1"
        FORGE_VERSION="37.0.58"
    fi

    # Create directory for Minecraft server and move into it
    mkdir minecraft_forge_server
    cd minecraft_forge_server

    # Download the Forge installer
    wget "https://files.minecraftforge.net/maven/net/minecraftforge/forge/${MC_VERSION}-${FORGE_VERSION}/forge-${MC_VERSION}-${FORGE_VERSION}-installer.jar"

    # Run the Forge installer with the --installServer flag
    java -jar "forge-${MC_VERSION}-${FORGE_VERSION}-installer.jar" --installServer

    # Remove installer files (optional)
    rm "forge-${MC_VERSION}-${FORGE_VERSION}-installer.jar"

    # Display message to indicate completion
    echo "Forge server setup complete!"
}    
