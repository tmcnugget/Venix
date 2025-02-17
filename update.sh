#!/bin/bash

# Function to check if a Python module exists and install if missing
install_python_lib() {
    local module=$1
    local install_cmd=$2

    python3 -c "import importlib.util; exit(0 if importlib.util.find_spec('$module') else 1)"
    if [ $? -ne 0 ]; then
        echo "Python module $module not found. Installing..."
        eval "$install_cmd"
    else
        echo "Python module $module is already installed."
    fi
}

echo "Checking required Python libraries..."
declare -A LIBRARIES
LIBRARIES=(
    ["approxeng.input"]="pip3 install approxeng.input"
    ["adafruit_pca9685"]="pip3 install adafruit-circuitpython-pca9685"
    ["icm20948"]="{ install_command git git && git clone https://github.com/pimoroni/icm20948-python && cd icm20948-python && ./install.sh; }"
    ["board"]="pip3 install adafruit-blinka"
    ["busio"]="pip3 install adafruit-blinka"
)

for lib in "${!LIBRARIES[@]}"; do
    install_python_lib "$lib" "${LIBRARIES[$lib]}"
done

echo "All required packages and libraries are checked and installed if necessary."
