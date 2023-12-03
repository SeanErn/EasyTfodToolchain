#!/bin/bash
LOGFILE="logs/_installDependencies_$(date +%Y%m%d-%H%M%S).log"
exec 3>&1 1> >(tee -a "$LOGFILE") 2>&1
trap "echo 'ERROR: An error occurred during execution, check log $LOGFILE for details.' >&3" ERR
trap '{ set +x; } 2>/dev/null; echo -n "[$(date -Is)] "; set -x' DEBUG


if ! command -v pyenv &> /dev/null
then
    sudo apt update -y

    sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl \
    git

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    {
    echo 'export PYENV_ROOT="$HOME/.pyenv"';
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"';
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi';
    } >> ~/.bashrc
    
    echo "Restart your terminal and then run ./install/installDependencies.sh again"
else
    # Install python v3.11.x if not already exists, activate it
    pyenv install 3.11 -s
    pyenv global 3.11

    # Install all PIP requirements
    pip install -r install/requirements.txt
    echo "Dependency install finished! Run 'python run.py' in your terminal to continue installation"
fi
