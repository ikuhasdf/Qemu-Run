# QEMU Launcher 1.2

A graphical frontend for QEMU virtualization built with Python and Tkinter.

## 🚀 Features

### 🎯 Core Features
- **Visual VM Configuration**: Configure QEMU parameters through intuitive GUI
- **Image Factory**: Create disk images in multiple formats (qcow2, raw, vmdk, vdi)
- **Multi-Disk Support**: Configure primary and secondary storage devices
- **Custom BIOS Support**: Load custom BIOS files for specialized needs
- **Hardware Selection**: Pre-configured device options for graphics, network, and sound

### ⚡ Enhanced Hardware Support
```python
# Expanded CPU Model Support
cpu_models = [
    "486", "pentium", "pentium-v1", "pentium2", "pentium2-v1",
    "pentium3", "pentium3-v1", "coreduo", "core2duo", "phenom",
    "athlon64", "qemu64", "host", "EPYC", "qemu32", "base", "max"
]

# Device Options
gpu_options = ["vmware", "cirrus", "std", "qxl"]
net_options = ["e1000", "rtl8139", "ne2k_pci"]  
sound_options = ["ac97", "sb16", "intel-hda", "es1370"]