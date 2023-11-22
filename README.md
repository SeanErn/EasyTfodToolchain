# EasyTfodToolchain

An user-friendly toolchain for training v2 TensorFlow object detector models
---
### Requirements:
- Git
- Ubuntu-based OS (Windows is not supported at this time. Other linux distros may work, but they need to be able to run the `apt` package manager)
- A GPU with CUDA support (Nvidia GPUs are recommended)
- Training and Validation videos

### Installation:
1. Clone this repository
```bash
git clone https://github.com/SeanErn/EasyTfodToolchain.git
```
2. Enter the directory
```bash
cd EasyTfodToolchain
```
3. Install the prerequisites
```bash
./installDependencies
```
4. Run the installer
```bash
python run.py
```
