# QEMU Launcher 1.2

[中文文档](README_ZH.md) | [English](README.md)

A graphical frontend for QEMU virtualization built with Python and Tkinter.

## 🚀 Features

### 🎯 Core Features
- **Visual VM Configuration**: Configure QEMU parameters through an intuitive GUI.
- **Image Factory**: Create disk images in multiple formats (qcow2, qcow, raw, vmdk, vdi).
- **Multi-Disk Support**: Configure primary (`-hda`) and secondary (`-hdb`) storage devices.
- **Custom BIOS Support**: Load custom BIOS files for specialized needs.
- **Hardware Selection**: Pre-configured device options for graphics, network, and sound.

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
```

🛠️ Usage

Quick Start

1. Launch QEMU Launcher.
2. Configure your VM settings through the intuitive interface.
3. Click "Start" to launch your virtual machine.

Example Generated Command

```bash
qemu-system-x86_64 -name "TestVM" -M pc -accel kvm -cpu qemu64 \
  -vga std -hda /path/to/disk.qcow2 -hdb /path/to/disk2.qcow2 \
  -m 2048 -smp 4 -device e1000 -boot c \
  -drive format=vvfat,dir=/shared/path,rw=on
```

📋 Technical Specifications

· Base Command: qemu-system-x86_64
· Acceleration: KVM, TCG, WHPX support
· Memory: Configurable via -m parameter
· CPU Cores: SMP support with -smp
· Boot Options: Flexible boot device selection (a, c, d)
· Platforms: Linux and Windows

🔧 Requirements

· Python 3.x
· Tkinter
· QEMU system utilities

📄 License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

🔗 Links

· Source Code: [GitHub Repository](https://github.com/ikuhasdf/Qemu-Run)
· Report Issues: [GitHub Issues](https://github.com/ikuhasdf/Qemu-Run/issues)
