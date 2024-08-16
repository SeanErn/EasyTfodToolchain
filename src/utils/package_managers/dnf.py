# File: utils/package_managers/dnf.py

import subprocess
import logging
import os

logger = logging.getLogger(__name__)

RPM_REPOSITORIES = [
    "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm",
    "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"
]

REPO_REPOSITORIES = [
    "https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/cuda-fedora39.repo",
    "https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo"
]

PACKAGES = [
    "gcc",
    "akmod-nvidia",
    "cuda",
    "cudnn9-cuda-12"
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

def add_rpm_repository(repo: str, sudo_password: str, log_write: callable) -> None:
    log_write(f"Attempting to install RPM repository: {repo}")
    
    command = f"dnf install -y {repo}"
    returncode = run_command(command, sudo_password, log_write)
    
    if returncode == 0:
        log_write(f"Successfully installed RPM repository: {repo}")
    else:
        log_write(f"Failed to install RPM repository: {repo}")

def add_repo_repository(repo: str, sudo_password: str, log_write: callable) -> None:
    log_write(f"Attempting to add .repo repository: {repo}")
    
    command = f"dnf config-manager --add-repo {repo}"
    returncode = run_command(command, sudo_password, log_write)
    
    if returncode == 0:
        log_write(f"Successfully added .repo repository: {repo}")
    else:
        log_write(f"Failed to add .repo repository: {repo}")

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
    
    # Add RPM repositories
    log_write("Adding RPM repositories")
    for repo in RPM_REPOSITORIES:
        add_rpm_repository(repo, sudo_password, log_write)
    
    # Add .repo repositories
    log_write("Adding .repo repositories")
    for repo in REPO_REPOSITORIES:
        add_repo_repository(repo, sudo_password, log_write)
    
    # Update system after adding repositories
    log_write("Updating system")
    update_system(sudo_password, log_write)
    
    # Install packages
    log_write("Installing packages")
    for package in PACKAGES:
        install_package(package, sudo_password, log_write)
    
    log_write("System setup completed")

logger.info("DNF package manager module loaded")