# QEMU 启动器 1.2

[English Documentation](README.md) | [中文文档](README_ZH.md)

使用 Python 和 Tkinter 构建的 QEMU 虚拟化图形前端。

## 🚀 功能特性

### 🎯 核心功能
- **可视化虚拟机配置**：通过直观的图形界面配置 QEMU 参数
- **镜像工厂**：创建多种格式的磁盘镜像（qcow2、qcow、raw、vmdk、vdi）
- **多磁盘支持**：配置主（`-hda`）和从（`-hdb`）存储设备
- **自定义 BIOS 支持**：加载自定义 BIOS 文件以满足特殊需求
- **硬件选择**：预配置的显卡、网卡和声卡设备选项

### ⚡ 增强的硬件支持
```python
# 扩展的 CPU 型号支持
cpu_models = [
    "486", "pentium", "pentium-v1", "pentium2", "pentium2-v1",
    "pentium3", "pentium3-v1", "coreduo", "core2duo", "phenom",
    "athlon64", "qemu64", "host", "EPYC", "qemu32", "base", "max"
]

# 设备选项
gpu_options = ["vmware", "cirrus", "std", "qxl"]
net_options = ["e1000", "rtl8139", "ne2k_pci"]
sound_options = ["ac97", "sb16", "intel-hda", "es1370"]
```

🛠️ 使用指南

快速开始

1. 启动 QEMU 启动器
2. 通过直观的界面配置虚拟机设置
3. 点击"启动"运行您的虚拟机

镜像工厂使用

使用内置的镜像工厂创建虚拟磁盘，支持多种格式和容量设置。

示例生成命令

```bash
qemu-system-x86_64 -name "TestVM" -M pc -accel kvm -cpu qemu64 \
  -vga std -hda /path/to/disk.qcow2 -hdb /path/to/disk2.qcow2 \
  -m 2048 -smp 4 -device e1000 -boot c \
  -drive format=vvfat,dir=/shared/path,rw=on
```

📋 技术规格

· 基础命令：qemu-system-x86_64
· 加速支持：KVM、TCG、WHPX
· 内存配置：通过 -m 参数配置
· CPU 核心：通过 -smp 支持多核
· 启动选项：灵活的启动设备选择（a、c、d）
· 支持平台：Linux 和 Windows

🔧 环境要求

· Python 3.x
· PyQT5 图形库
· QEMU 系统工具

📄 许可证

本项目采用 GNU 通用公共许可证 v3.0。详见 LICENSE 文件。

🔗 相关链接

· 源代码：[GitHub 仓库](https://github.com/ikuhasdf/Qemu-Run)
· 问题反馈：[GitHub Issues](github.com/ikuhasdf/Qemu-Run/issues)

---

注意：本工具旨在简化 QEMU 的使用，同时保持与标准 QEMU 参数和功能的完全兼容。
