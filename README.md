# EasyTfodToolchain

## An user-friendly toolchain for training v2 TensorFlow object detector models
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
3. Run the installer
```bash
python run.py
```

## Roadmap
- [ ] Installer script fully working
      * Update 11/23/23: Working besides some issues with built in logger panic crashing textual when downloading CUDA via wget, tries to install cudNN when not fully downloaded
      ![Screenshot from 2023-11-23 02-04-26](https://github.com/SeanErn/EasyTfodToolchain/assets/81441231/4b166ca5-3461-479f-b58d-838e5cd1605b)
- [ ] Install error handling (report errors to user, suggest fixes)
- [ ] Python-wide logger
- [ ] Project Manager
- [ ] Find annotation software (maybe labelImg or LabelStudio) OR create from scratch D:
- [ ] Prepare, Train, Export python scripts
- [ ] Test python script
- [ ] FULL USER GUIDE
- [ ] MVP
- [ ] Advanced purge dataset, purge logs, reinstall, etc
- [ ] TF v1 support 
