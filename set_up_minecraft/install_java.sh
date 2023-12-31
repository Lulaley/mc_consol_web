#!/bin/bash

# Récupère la version de Java actuelle
crrt_java() {
    CURRENT_JAVA_VERSION=$(java -version 2>&1 | grep 'version' | sed 's/.* version "\(.*\)\.\(.*\)\..*"/\1\2/; 1q')
}

# Fonction pour télécharger Java 8 (par exemple pour les anciennes versions de Minecraft)
install_java_8() {
    echo "Téléchargement de Java 8..."
    wget -O jdk8.tar.gz "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241526_1f5b5a70bf22433b84d0e960903adac8"
    mkdir jdk8
    tar -zxvf jdk8.tar.gz -C jdk8 --strip-components=1
    rm jdk8.tar.gz
    echo "Téléchargement finit"
}

# Fonction pour télécharger Java 16 (par exemple pour Minecraft 1.17)
install_java_16() {
    echo "Téléchargement de Java 16..."
    wget -O jdk16.tar.gz "https://download.oracle.com/otn/java/jdk/16.0.2%2B7/d4a915d82b4c4fbb9bde534da945d746/jdk-16.0.2_linux-aarch64_bin.tar.gz"
    mkdir jdk16
    tar -zxvf jdk16.tar.gz -C jdk16 --strip-components=1
    rm jdk16.tar.gz
    echo "Téléchargement finit"
}

# Fonction pour télécharger Java 16 (par exemple pour Minecraft 1.18)
install_java_17() {
    echo "Téléchargement de Java 17..."
    wget -O jdk17.tar.gz "https://download.oracle.com/java/17/archive/jdk-17.0.8_linux-aarch64_bin.tar.gz"
    mkdir jdk17
    tar -zxvf jdk17.tar.gz -C jdk17 --strip-components=1
    rm jdk17.tar.gz
    echo "Téléchargement finit"
}

# Change java version
change_java() {
    crrt_java
    if [[ "$CURRENT_JAVA_VERSION" -lt "18" ]]; then
        if [[ ! -d "jdk8" ]]; then
            install_java_8
        fi
        echo "Changement d'utilisation a Java 8"
        export PATH="$PWD/jdk8/bin:$PATH"
    elif [[ "$CURRENT_JAVA_VERSION" -lt "17" && "$CURRENT_JAVA_VERSION" -gt "8" ]]; then
        if [[ ! -d "jdk16" ]]; then
            install_java_16
        fi
        export PATH="$PWD/jdk16/bin:$PATH"
        echo "Changement d'utilisation a Java 16"
    elif [[ "$CURRENT_JAVA_VERSION" -lt "18" && "$CURRENT_JAVA_VERSION" -gt "16" ]]; then
        if [[ ! -d "jdk17" ]]; then
            install_java_17
        fi
        export PATH="$PWD/jdk17/bin:$PATH"
        echo "Changement d'utilisation a Java 17"
    fi

    # Affiche la version de Java après la mise à jour
    java -version
}
