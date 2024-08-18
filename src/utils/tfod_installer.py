# File: utils/tfod_installer.py

import os
import subprocess
import logging
import shutil
from typing import Callable

logger = logging.getLogger(__name__)

class TFODInstaller:
    def __init__(self, log_write: Callable[[str], None]):
        self.log_write = log_write
        self.base_dir = os.getcwd()
        self.models_dir = os.path.join(self.base_dir, 'models')
        self.research_dir = os.path.join(self.models_dir, 'research')
        logger.info("TFODInstaller initialized")

    def run_command(self, command: str, cwd: str = None) -> int:
        logger.debug(f"Running command: {command}")
        self.log_write(f"Running: {command}")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=cwd
        )

        for line in process.stdout:
            line = line.strip()
            if line:
                logger.debug(f"STDOUT: {line}")
                self.log_write(line)

        for line in process.stderr:
            line = line.strip()
            if line:
                logger.error(f"STDERR: {line}")
                self.log_write(f"[red]{line}[/red]")

        return process.wait()

    def clone_models_repo(self):
        self.log_write("Cloning TensorFlow models repository...")
        return self.run_command("git clone https://github.com/tensorflow/models.git")

    def install_protobufs(self):
        self.log_write("Installing protobufs...")
        commands = [
            "cd models/research && protoc object_detection/protos/*.proto --python_out=.",
            "cd models/research/object_detection/protos && touch installed.state"
        ]
        for cmd in commands:
            if self.run_command(cmd) != 0:
                return False
        return True

    def install_cocoapi(self):
        self.log_write("Installing COCO API...")
        commands = [
            "git clone https://github.com/cocodataset/cocoapi.git",
            "cd cocoapi/PythonAPI && make",
            "cp -r cocoapi/PythonAPI/pycocotools models/research/",
            "rm -rf cocoapi"
        ]
        for cmd in commands:
            if self.run_command(cmd) != 0:
                return False
        return True

    def install_object_detection_api(self):
        self.log_write("Installing Object Detection API...")
        commands = [
            "cd models/research && cp object_detection/packages/tf2/setup.py .",
            "cd models/research && python -m pip install ."
        ]
        for cmd in commands:
            if self.run_command(cmd) != 0:
                return False
        return True

    def test_installation(self):
        self.log_write("Testing installation...")
        return self.run_command("cd models/research && python object_detection/builders/model_builder_tf2_test.py")

    def run_installation(self):
        steps = [
            (self.clone_models_repo, "Cloning TensorFlow models repository"),
            (self.install_protobufs, "Installing protobufs"),
            (self.install_cocoapi, "Installing COCO API"),
            (self.install_object_detection_api, "Installing Object Detection API"),
            (self.test_installation, "Testing installation")
        ]

        for step_func, step_description in steps:
            self.log_write(f"[blue]Starting: {step_description}[/blue]")
            if step_func() != 0:
                self.log_write(f"[red]Failed: {step_description}[/red]")
                return False
            self.log_write(f"[green]Completed: {step_description}[/green]")

        self.log_write("[green]TensorFlow Object Detection API installation completed successfully![/green]")
        return True

logger.info("TFODInstaller module loaded")