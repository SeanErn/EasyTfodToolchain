# File: utils/package_managers/dnf.py

import subprocess
import logging
import os

logger = logging.getLogger(__name__)

REPOSITORIES = [
    "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm",
    "https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"
]

PACKAGES = [
    "python3-devel",
    "python3-pip",
    "mesa-libGL",
    "glib2"
]

def run_command(command: str, sudo_password: str, log_write: callable) -> int:
    sudo_command = f"sudo -S {command}"
    process = subprocess.Popen(
        sudo_command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    process.stdin.write(f"{sudo_password}\n")
    process.stdin.flush()

    for line in process.stdout:
        line = line.strip()
        if line:
            logger.debug(f"STDOUT: {line}")
            log_write(line)

    for line in process.stderr:
        line = line.strip()
        if line:
            logger.error(f"STDERR: {line}")
            log_write(f"[red]{line}[/red]")

    return process.wait()

def add_repository(repo: str, sudo_password: str, log_write: callable) -> None:
    log_write(f"Attempting to add repository: {repo}")
    
    # Check if the repository is already installed
    repo_name = os.path.basename(repo).replace(".rpm", "")
    check_command = f"rpm -q {repo_name}"
    returncode = run_command(check_command, sudo_password, log_write)
    
    if returncode == 0:
        log_write(f"Repository {repo_name} is already installed")
    else:
        # Install the repository RPM
        install_command = f"dnf install -y {repo}"
        returncode = run_command(install_command, sudo_password, log_write)
        
        if returncode != 0:
            log_write(f"Failed to install repository RPM: {repo}")
            return

    # Enable the repository
    enable_command = f"dnf config-manager --set-enabled {repo_name}"
    returncode = run_command(enable_command, sudo_password, log_write)
    
    if returncode == 0:
        log_write(f"Successfully added and enabled repository: {repo}")
    else:
        log_write(f"Failed to enable repository: {repo}")

def install_package(package_name: str, sudo_password: str, log_write: callable) -> None:
    log_write(f"Attempting to install {package_name} using dnf")
    command = f"dnf install -y {package_name}"
    returncode = run_command(command, sudo_password, log_write)
    
    if returncode == 0:
        log_write(f"Successfully installed {package_name}")
    else:
        log_write(f"Failed to install {package_name}")

def update_system(sudo_password: str, log_write: callable) -> None:
    log_write("Updating system packages")
    command = "dnf update -y"
    returncode = run_command(command, sudo_password, log_write)
    
    if returncode == 0:
        log_write("Successfully updated system packages")
    else:
        log_write("Failed to update system packages")

def setup_system(sudo_password: str, log_write: callable) -> None:
    log_write("Starting system setup")
    
    # Add repositories
    log_write("Adding repositories")
    for repo in REPOSITORIES:
        add_repository(repo, sudo_password, log_write)
    
    # Update system after adding repositories
    log_write("Updating system")
    update_system(sudo_password, log_write)
    
    # Install packages
    log_write("Installing packages")
    for package in PACKAGES:
        install_package(package, sudo_password, log_write)
    
    log_write("System setup completed")