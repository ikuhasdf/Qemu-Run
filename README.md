```markdown
# QEMU Launcher 1.2 Release

A graphical frontend for QEMU virtualization, built with Python and Tkinter.

## New Features

### Expanded CPU Support
Added support for additional CPU models:
```python
cpu_models = [
    "486", "pentium", "pentium-v1", "pentium2", "pentium2-v1",
    "pentium3", "pentium3-v1", "coreduo", "core2duo", "phenom",
    "athlon64", "qemu64", "host", "EPYC", "qemu32", "base", "max"
]
```

Custom BIOS Support

Specify custom BIOS files for specialized virtualization needs:

```python
def add_bios():
    bios_path = self.bios_entry.get()
    if bios_path:
        self.vm_cmd.extend(["-bios", bios_path])
```

Secondary Disk Support

Configure multiple storage devices with second disk support:

```python
def add_secondary_disk():
    disk_path = self.hdb_entry.get()
    if disk_path:
        self.vm_cmd.extend(["-hdb", disk_path])
```

Image Factory

Create virtual disk images with multiple format support:

```python
def create_disk_image():
    formats = ["qcow2", "qcow", "raw", "vmdk", "vdi"]
    cmd = [
        "qemu-img", "create", "-f", selected_format,
        f"{output_path}/{image_name}.{selected_format}", 
        disk_size
    ]
    run(cmd)
```

Enhanced Device Selection

Improved hardware configuration with combobox selections:

```python
# Graphics cards
gpu_options = ["vmware", "cirrus", "std", "qxl"]

# Network adapters  
net_options = ["e1000", "rtl8139", "ne2k_pci"]

# Sound cards
sound_options = ["ac97", "sb16", "intel-hda", "es1370"]
```

Technical Specifications

· Base Command: qemu-system-x86_64
· Acceleration: KVM, TCG, WHPX support
· Memory: Configurable via -m parameter
· CPU Cores: SMP support with -smp
· Boot Options: Flexible boot device selection (a, c, d)

Usage Example

```bash
# Generated command example
qemu-system-x86_64 -name "TestVM" -M pc -accel kvm -cpu qemu64 \
  -vga std -hda /path/to/disk.qcow2 -hdb /path/to/disk2.qcow2 \
  -m 2048 -smp 4 -device e1000 -boot c \
  -drive format=vvfat,dir=/shared/path,rw=on
```

License

This project is licensed under the GNU General Public License v3.0. See LICENSE file for details.

Source Code

Available on GitHub: https://github.com/lkuhasdf/Qemu-Run

Requirements

· Python 3.x
· Tkinter
· QEMU system utilities
· Supported on Linux and Windows systems

```