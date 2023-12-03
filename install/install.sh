#!/bin/bash
LOGFILE="logs/_install_$(date +%Y%m%d-%H%M%S).log"
exec 3>&1 1> >(tee -a "$LOGFILE") 2>&1
# shellcheck disable=SC2064
trap "echo 'ERROR: An error occurred during execution, check log $LOGFILE for details.' >&3" ERR
trap '{ set +x; } 2>/dev/null; echo -n "[$(date -Is)] "; set -x' DEBUG

# Cuda install v12.3.1
function installCuda {
    wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
    sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget -q https://developer.download.nvidia.com/compute/cuda/12.3.1/local_installers/cuda-repo-ubuntu2204-12-3-local_12.3.1-545.23.08-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu2204-12-3-local_12.3.1-545.23.08-1_amd64.deb
    sudo cp /var/cuda-repo-ubuntu2204-12-3-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-12-3
    sudo rm cuda-repo-ubuntu2204-12-3-local_12.3.1-545.23.08-1_amd64.deb
    echo "prog10"
}

# CudNN install v8.9.6 for CUDA 12
function installCudnn {
    sudo apt-get install zlib1g
    echo "You will be redirected to login to NVIDIA developer and download cudNN to this directory!"
    echo "Redirecting in 10 seconds"
    sleep 10s
    xdg-open https://developer.nvidia.com/downloads/compute/cudnn/secure/8.9.6/local_installers/12.x/cudnn-local-repo-ubuntu2204-8.9.6.50_1.0-1_amd64.deb/
    while [ ! -f ./cudnn-local-repo-ubuntu2204-8.9.6.50_1.0-1_amd64.deb ] || [ -f ./cudnn-local-repo-ubuntu2204-8.9.6.50_1.0-1_amd64.deb.part ]; do
        echo "Waiting for download to finish! Please sign in to NVIDIA developer and download cudNN to this directory!"
        echo "Retrying in 30s..."
        sleep 30s
    done
    sudo dpkg -i cudnn-local-repo-ubuntu2204-8.9.6.50_1.0-1_amd64.deb
    sudo cp /var/cudnn-local-repo-*/cudnn-local-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get install libcudnn8=8.9.6.50-1+cuda12.2
    sudo rm cudnn-local-repo-ubuntu2204-8.9.6.50_1.0-1_amd64.deb
    echo "prog20"
}

# Git install
function installGit {
    sudo apt update
    sudo apt install git
    echo "prog30"
}

# TensorFlow Model Garden clone for v2.15.0
function cloneModelGarden {
    git clone https://github.com/tensorflow/models.git
    echo "prog40"
}

# Protobuf install for 3.12.4-1ubuntu7.22.04.1
function installProtobuf {
    sudo apt update
    sudo apt install protobuf-compiler=3.12.4-1ubuntu7.22.04.1
    echo "prog50"
}

# Protobuf install for tensorflow model garden
function installTensorflowProtobufs {
    ( cd models/research && protoc object_detection/protos/*.proto --python_out=. )
    ( cd models/research/object_detection/protos && touch installed.state)
    echo "prog60"
}

# make install
function installMake {
    sudo apt update
    sudo apt install make
    echo "prog70"
}

# COCO API install
function installCocoApi {
    git clone https://github.com/cocodataset/cocoapi.git
    ( cd cocoapi/PythonAPI && make )
    cp -r cocoapi/PythonAPI/pycocotools models/research/
    rm -rf cocoapi
    echo "prog80"
}

# Object Detection API install
function installObjectDetectionApi {
    ( cd models/research && cp object_detection/packages/tf2/setup.py . )
    ( cd models/research && python -m pip install . )
    echo "prog90"
}

# Check if CUDA is installed. If not, install it.
apt show cuda-toolkit-12-3 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "CUDA already installed. Skipping!"
    echo "prog10"
else
    echo "Installing CUDA..."
    installCuda
    echo "Done installing CUDA!"
fi

# Check if cudNN is installed. If not, install it.
apt show libcudnn8=8.9.6.50-1+cuda12.2 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "cudNN already installed. Skipping!"
    echo "prog20"
else
    echo "Installing cudNN..."
    installCudnn
    echo "Done installing cudNN!"
fi

# Check if Git is installed. If not, install it.
apt show git > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Git already installed. Skipping!"
    echo "prog30"
else
    echo "Installing Git..."
    installGit
    echo "Done installing Git!"
fi

# Check if Model Garden is cloned. If not, clone it.
if [ -d models ]; then
    echo "Model Garden already downloaded. Skipping!"
    echo "prog40"
else
    echo "Cloning Model Garden..."
    cloneModelGarden
    echo "Done cloning TensorFlow Model Garden!"
fi

# Check if protobuf is installed. If not, install it.
apt show protobuf-compiler=3.12.4-1ubuntu7.22.04.1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "protobuf already installed. Skipping!"
    echo "prog50"
else
    echo "Installing protobuf..."
    installProtobuf
    echo "Done installing protobuf!"
fi

# Check if tf protobufs are installed. If not, install them.
if [ -f models/research/object_detection/protos/installed.state ]; then
    echo "TensorFlow protobufs already installed. Skipping!"
    echo "prog60"
else
    echo "Installing TensorFlow protobufs..."
    installTensorflowProtobufs
    echo "Done installing TensorFlow protobufs!"
fi

# Check if make is installed. If not, install it.
apt show make > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "make already installed. Skipping!"
    echo "prog70"
else
    echo "Installing make..."
    installMake
    echo "Done installing make!"
fi

# Check if coco api is installed. If not, install it.
if [ -d models/research/pycocotools ]; then
    echo "COCO API already installed. Skipping!"
    echo "prog80"
else
    echo "Installing COCO API..."
    installCocoApi
    echo "Done installing COCO API!"
fi

# Check if object detection api is installed. If not, install it.
if [ -f models/research/setup.py ]; then
    echo "TensorFlow Object Detection API already installed. Skipping!"
    echo "prog90"
else
    echo "Installing TensorFlow Object Detection API..."
    installObjectDetectionApi
    echo "Done installing TensorFlow Object Detection API!"
fi

echo "Testing install..."
( cd models/research && python object_detection/builders/model_builder_tf2_test.py )
echo "prog100"
echo "progDone"