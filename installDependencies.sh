#!/bin/bash

# Install Gum
if ! command -v gum &> /dev/null
then
    echo "Installing Gum..."
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
    sudo apt update
    sudo apt install gum
    sleep 3 # wait for Gum to install and configure
fi

gum spin --spinner line --show-output --title "Updating dependencies..." -- sudo apt update -y

gum spin --spinner line --show-output --title "Installing Pyenv dependencies..." -- \
> sudo apt install -y make build-essential libssl-dev zlib1g-dev \
> libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
> libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl \
> git

gum spin --spinner line --show-output --title "Cloning pyenv..." -- git clone https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc

echo "Restart your terminal and then run install.sh"