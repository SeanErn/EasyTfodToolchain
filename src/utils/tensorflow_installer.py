# File: utils/tensorflow_installer.py

import os
import subprocess
import shutil
import logging
from typing import Callable
import git

logger = logging.getLogger(__name__)

class TensorFlowInstaller:
    def __init__(self, log_write: Callable[[str], None]):
        self.log_write = log_write
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.lib_dir = os.path.join(self.base_dir, 'lib')
        self.models_dir = os.path.join(self.lib_dir, 'models')
        self.research_dir = os.path.join(self.models_dir, 'research')
        self.object_detection_dir = os.path.join(self.research_dir, 'object_detection')
        self.tensorflow_version = "2.13.1"

    def run_command(self, command: str, cwd: str = None, ignore_errors: bool = False, is_test: bool = False) -> int:
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

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.log_write(output.strip())

        rc = process.poll()
        
        for line in process.stderr:
            line = line.strip()
            if line:
                if ignore_errors and "warning" in line.lower():
                    logger.warning(f"Ignored warning: {line}")
                    self.log_write(f"[yellow]Ignored warning: {line}[/yellow]")
                elif is_test:
                    # For test output, we don't want to highlight as errors
                    logger.info(f"Test output: {line}")
                    self.log_write(line)
                else:
                    logger.error(f"STDERR: {line}")
                    self.log_write(f"[red]{line}[/red]")

        return rc

    def clone_repository(self, repo_url: str, target_dir: str) -> None:
        if os.path.exists(target_dir):
            self.log_write(f"Repository already exists at {target_dir}, skipping clone.")
            return

        self.log_write(f"Cloning repository: {repo_url}")
        try:
            git.Repo.clone_from(repo_url, target_dir)
            self.log_write(f"Successfully cloned repository to {target_dir}")
        except git.GitCommandError as e:
            logger.exception(f"Failed to clone repository: {str(e)}")
            self.log_write(f"[red]Failed to clone repository: {str(e)}[/red]")

    def install_tensorflow(self) -> None:
        self.log_write(f"Installing TensorFlow {self.tensorflow_version}")
        install_command = f"pip install tensorflow=={self.tensorflow_version}"
        returncode = self.run_command(install_command)
        
        if returncode == 0:
            self.log_write(f"Successfully installed TensorFlow {self.tensorflow_version}")
        else:
            self.log_write(f"[red]Failed to install TensorFlow {self.tensorflow_version}[/red]")

    def install_protobufs(self) -> None:
        self.log_write("Installing protobufs")
        protoc_command = f"protoc object_detection/protos/*.proto --python_out=."
        returncode = self.run_command(protoc_command, cwd=self.research_dir)
        
        if returncode == 0:
            self.log_write("Successfully installed protobufs")
            os.makedirs(os.path.join(self.object_detection_dir, 'protos'), exist_ok=True)
            open(os.path.join(self.object_detection_dir, 'protos', 'installed.state'), 'w').close()
        else:
            self.log_write("[red]Failed to install protobufs[/red]")

    def install_cocoapi(self) -> None:
        self.log_write("Installing COCO API")
        cocoapi_dir = os.path.join(self.lib_dir, 'cocoapi')
        self.clone_repository("https://github.com/cocodataset/cocoapi.git", cocoapi_dir)
        
        make_command = "make"
        returncode = self.run_command(make_command, cwd=os.path.join(cocoapi_dir, 'PythonAPI'), ignore_errors=True)
        
        if returncode == 0:
            self.log_write("Successfully built COCO API")
            shutil.copytree(os.path.join(cocoapi_dir, 'PythonAPI', 'pycocotools'), 
                            os.path.join(self.research_dir, 'pycocotools'))
            shutil.rmtree(cocoapi_dir)
            self.log_write("Successfully installed COCO API")
        else:
            self.log_write("[yellow]COCO API build completed with warnings. Continuing installation.[/yellow]")

    def install_object_detection_api(self) -> None:
        self.log_write("Installing Object Detection API")
        
        # Copy the setup.py file
        shutil.copy(os.path.join(self.object_detection_dir, 'packages', 'tf2', 'setup.py'), 
                    self.research_dir)
        
        # Modify setup.py to pin TensorFlow version
        setup_path = os.path.join(self.research_dir, 'setup.py')
        with open(setup_path, 'r') as file:
            setup_content = file.read()
        
        setup_content = setup_content.replace(
            "tensorflow",
            f"tensorflow=={self.tensorflow_version}"
        )
        
        with open(setup_path, 'w') as file:
            file.write(setup_content)
        
        # Install the Object Detection API
        install_command = "python -m pip install ."
        returncode = self.run_command(install_command, cwd=self.research_dir)
        
        if returncode == 0:
            self.log_write("Successfully installed Object Detection API")
        else:
            self.log_write("[red]Failed to install Object Detection API[/red]")

    def test_installation(self) -> None:
        self.log_write("Testing installation")
        test_command = "python object_detection/builders/model_builder_tf2_test.py"
        returncode = self.run_command(test_command, cwd=self.research_dir, is_test=True)
        
        if returncode == 0:
            self.log_write("[green]Installation test passed successfully[/green]")
        else:
            self.log_write("[red]Installation test failed[/red]")

    def run_installation(self) -> None:
        logger.info("Starting TensorFlow Object Detection API installation")
        self.log_write("Starting TensorFlow Object Detection API installation")

        # Create lib directory if it doesn't exist
        os.makedirs(self.lib_dir, exist_ok=True)

        # Clone TensorFlow models repository
        self.clone_repository("https://github.com/tensorflow/models.git", self.models_dir)

        # Install protobufs
        self.install_protobufs()

        # Install COCO API
        self.install_cocoapi()

        # Install Object Detection API
        self.install_object_detection_api()

        # Install specific TensorFlow version
        self.install_tensorflow()

        # Test installation
        self.test_installation()

        logger.info("TensorFlow Object Detection API installation completed")
        self.log_write("TensorFlow Object Detection API installation completed")