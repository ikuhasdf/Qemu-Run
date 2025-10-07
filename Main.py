#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QScrollArea, QFrame, QDialog,
    QFormLayout, QFileDialog, QSpinBox
)
from PyQt5.QtCore import Qt

class ImageFactoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("镜像工厂")
        self.setMinimumSize(640, 480)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.img_name = QLineEdit()      # 名称（不含路径）
        self.img_dir = QLineEdit()       # 路径
        self.img_size = QLineEdit()      # 大小（如 10G）
        self.img_format = QComboBox()
        self.img_format.addItems(["qcow2", "qcow", "raw", "vmdk", "vdi"])

        form.addRow("镜像名 (不含扩展)：", self.img_name)
        dir_row = QHBoxLayout()
        dir_row.addWidget(self.img_dir)
        btn_browse = QPushButton("浏览")
        btn_browse.clicked.connect(self.browse_dir)
        dir_row.addWidget(btn_browse)
        form.addRow("创建路径：", dir_row)
        form.addRow("镜像大小（如 10G / 1024M）：", self.img_size)
        form.addRow("格式：", self.img_format)

        layout.addLayout(form)

        btn_create = QPushButton("创建镜像")
        btn_create.clicked.connect(self.create_image)
        layout.addWidget(btn_create)

        # 扩容
        layout.addWidget(QLabel("------ 磁盘扩容 ------"))
        self.resize_path = QLineEdit()
        self.resize_amount = QLineEdit()
        self.resize_unit = QComboBox()
        self.resize_unit.addItems(["K", "M", "G", "T", "P"])
        resize_row = QHBoxLayout()
        resize_row.addWidget(self.resize_path)
        btn_browse_resize = QPushButton("浏览文件")
        btn_browse_resize.clicked.connect(self.browse_file_for_resize)
        resize_row.addWidget(btn_browse_resize)
        layout.addLayout(QFormLayout().addRow("镜像路径：", resize_row) or [])

        rform = QFormLayout()
        rform.addRow("扩容大小 (数字)：", self.resize_amount)
        rform.addRow("单位：", self.resize_unit)
        layout.addLayout(rform)

        btn_resize = QPushButton("扩容镜像")
        btn_resize.clicked.connect(self.resize_image)
        layout.addWidget(btn_resize)

        # 缩减
        layout.addWidget(QLabel("------ 磁盘缩减 (危险!) ------"))
        self.shrink_path = QLineEdit()
        self.shrink_amount = QLineEdit()
        self.shrink_unit = QComboBox()
        self.shrink_unit.addItems(["K", "M", "G", "T", "P"])
        shrink_row = QHBoxLayout()
        shrink_row.addWidget(self.shrink_path)
        btn_browse_shrink = QPushButton("浏览文件")
        btn_browse_shrink.clicked.connect(self.browse_file_for_shrink)
        shrink_row.addWidget(btn_browse_shrink)
        layout.addLayout(QFormLayout().addRow("镜像路径：", shrink_row) or [])

        sform = QFormLayout()
        sform.addRow("缩减大小 (数字)：", self.shrink_amount)
        sform.addRow("单位：", self.shrink_unit)
        layout.addLayout(sform)

        btn_shrink = QPushButton("缩减镜像 (危险)")
        btn_shrink.clicked.connect(self.shrink_image)
        layout.addWidget(btn_shrink)

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if d:
            self.img_dir.setText(d)

    def browse_file_for_resize(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择镜像文件", "", "All Files (*)")
        if f:
            self.resize_path.setText(f)

    def browse_file_for_shrink(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择镜像文件", "", "All Files (*)")
        if f:
            self.shrink_path.setText(f)

    def run_cmd_in_thread(self, cmd, success_msg=None, error_msg=None):
        def target():
            try:
                subprocess.run(cmd, check=True)
                if success_msg:
                    QMessageBox.information(self, "完成", success_msg)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"{error_msg or '命令失败'}:\n{e}")
        threading.Thread(target=target, daemon=True).start()

    def create_image(self):
        name = self.img_name.text().strip()
        directory = self.img_dir.text().strip()
        size = self.img_size.text().strip()
        fmt = self.img_format.currentText().strip()
        if not name or not directory or not size:
            QMessageBox.warning(self, "警告", "请填写镜像名、路径和大小")
            return
        fullpath = f"{directory}/{name}.{fmt}"
        cmd = ["qemu-img", "create", "-f", fmt, fullpath, size]
        self.run_cmd_in_thread(cmd, success_msg=f"创建成功：{fullpath}", error_msg="创建镜像失败")

    def resize_image(self):
        path = self.resize_path.text().strip()
        amt = self.resize_amount.text().strip()
        unit = self.resize_unit.currentText().strip()
        if not path or not amt:
            QMessageBox.warning(self, "警告", "请填写镜像路径和扩容大小")
            return
        if not amt.isdigit():
            QMessageBox.warning(self, "警告", "扩容大小必须为数字")
            return
        cmd = ["qemu-img", "resize", path, f"+{amt}{unit}"]
        self.run_cmd_in_thread(cmd, success_msg="扩容命令已执行", error_msg="扩容失败")

    def shrink_image(self):
        path = self.shrink_path.text().strip()
        amt = self.shrink_amount.text().strip()
        unit = self.shrink_unit.currentText().strip()
        if not path or not amt:
            QMessageBox.warning(self, "警告", "请填写镜像路径和缩减大小")
            return
        if not amt.isdigit():
            QMessageBox.warning(self, "警告", "缩减大小必须为数字")
            return
        # 警告并确认
        r = QMessageBox.warning(self, "危险操作",
                                "缩减镜像很危险，可能导致数据丢失。确认继续？",
                                QMessageBox.Yes | QMessageBox.No)
        if r != QMessageBox.Yes:
            return
        cmd = ["qemu-img", "resize", path, f"-{amt}{unit}"]
        self.run_cmd_in_thread(cmd, success_msg="缩减命令已执行", error_msg="缩减失败")


class QemuLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qemu启动器 PyQt5 重写")
        self.setMinimumSize(500, 600)
        self.vm_cmd = ["qemu-system-x86_64"]

        main_layout = QVBoxLayout(self)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QFrame()
        content_layout = QVBoxLayout(content)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # 当前命令显示
        content_layout.addWidget(QLabel("当前QEMU命令:"))
        self.cmd_line = QLineEdit()
        self.cmd_line.setReadOnly(True)
        content_layout.addWidget(self.cmd_line)

        # 操作按钮行
        btn_row = QHBoxLayout()
        self.show_cmd_btn = QPushButton("显示命令详情")
        self.copy_btn = QPushButton("复制命令")
        self.refresh_btn = QPushButton("刷新显示")
        btn_row.addWidget(self.show_cmd_btn)
        btn_row.addWidget(self.copy_btn)
        btn_row.addWidget(self.refresh_btn)
        content_layout.addLayout(btn_row)

        self.show_cmd_btn.clicked.connect(self.show_command)
        self.copy_btn.clicked.connect(self.copy_command)
        self.refresh_btn.clicked.connect(self.update_display)

        # ---- 参数输入区（按原结构逐项实现） ----
        # vm name
        content_layout.addWidget(QLabel("输入虚拟机名字"))
        self.name_edit = QLineEdit()
        content_layout.addWidget(self.name_edit)
        name_btn = QPushButton("确定")
        name_btn.clicked.connect(self.add_name)
        content_layout.addWidget(name_btn)

        # vm class
        content_layout.addWidget(QLabel("选择虚拟机类型"))
        self.class_combo = QComboBox()
        self.class_combo.addItems(["", "pc", "q35"])
        content_layout.addWidget(self.class_combo)
        class_btn = QPushButton("确定")
        class_btn.clicked.connect(self.add_class)
        content_layout.addWidget(class_btn)

        # accel
        content_layout.addWidget(QLabel("选择加速器"))
        self.accel_combo = QComboBox()
        self.accel_combo.addItems(["", "kvm", "tcg", "whpx", "whpx,kernel-irqchip=off"])
        content_layout.addWidget(self.accel_combo)
        accel_btn = QPushButton("确定")
        accel_btn.clicked.connect(self.add_accel)
        content_layout.addWidget(accel_btn)

        # cpu
        content_layout.addWidget(QLabel("选择CPU型号"))
        self.cpu_combo = QComboBox()
        self.cpu_combo.addItems(["", "486", "pentium", "pentium-v1", "pentium2",
                                 "pentium2-v1", "pentium3", "pentium3-v1",
                                 "coreduo", "core2duo", "phenom", "athlon64",
                                 "qemu64", "host", "EPYC", "qemu32", "base", "max"])
        content_layout.addWidget(self.cpu_combo)
        cpu_btn = QPushButton("确定")
        cpu_btn.clicked.connect(self.add_cpu)
        content_layout.addWidget(cpu_btn)

        # 显示
        content_layout.addWidget(QLabel("选择显卡型号"))
        self.vga_combo = QComboBox()
        self.vga_combo.addItems(["", "vmware", "cirrus", "std", "qxl"])
        content_layout.addWidget(self.vga_combo)
        vga_btn = QPushButton("确定")
        vga_btn.clicked.connect(self.add_vga)
        content_layout.addWidget(vga_btn)

        # 显存
        content_layout.addWidget(QLabel("输入显存 (MB)"))
        self.vgpu_edit = QLineEdit()
        content_layout.addWidget(self.vgpu_edit)
        vgpu_btn = QPushButton("确定")
        vgpu_btn.clicked.connect(self.add_vgpu)
        content_layout.addWidget(vgpu_btn)

        # 磁盘
        for i in range(4):
            content_layout.addWidget(QLabel(f"输入磁盘路径 index={i}"))
            setattr(self, f"drive_edit_{i}", QLineEdit())
            content_layout.addWidget(getattr(self, f"drive_edit_{i}"))
            btn = QPushButton("确定")
            btn.clicked.connect(lambda _, idx=i: self.add_drive(idx))
            content_layout.addWidget(btn)

        # 内存
        content_layout.addWidget(QLabel("输入内存容量 MB"))
        self.ram_edit = QLineEdit()
        content_layout.addWidget(self.ram_edit)
        ram_btn = QPushButton("确定")
        ram_btn.clicked.connect(self.add_ram)
        content_layout.addWidget(ram_btn)

        # bios
        content_layout.addWidget(QLabel("输入BIOS路径"))
        self.bios_edit = QLineEdit()
        content_layout.addWidget(self.bios_edit)
        bios_btn = QPushButton("确定")
        bios_btn.clicked.connect(self.add_bios)
        content_layout.addWidget(bios_btn)

        # CPU核心
        content_layout.addWidget(QLabel("输入CPU核心数量"))
        self.cores_edit = QLineEdit()
        content_layout.addWidget(self.cores_edit)
        cores_btn = QPushButton("确定")
        cores_btn.clicked.connect(self.add_cores)
        content_layout.addWidget(cores_btn)

        # 声卡
        content_layout.addWidget(QLabel("选择声卡型号"))
        self.sound_combo = QComboBox()
        self.sound_combo.addItems(["", "ac97", "sb16", "intel-hda", "es1370"])
        content_layout.addWidget(self.sound_combo)
        sound_btn = QPushButton("确定")
        sound_btn.clicked.connect(self.add_sound)
        content_layout.addWidget(sound_btn)

        # 网络
        content_layout.addWidget(QLabel("选择网卡型号"))
        self.net_combo = QComboBox()
        self.net_combo.addItems(["", "e1000", "rtl8139", "ne2k_pci"])
        content_layout.addWidget(self.net_combo)
        net_btn = QPushButton("确定")
        net_btn.clicked.connect(self.add_net)
        content_layout.addWidget(net_btn)

        # 共享文件夹
        content_layout.addWidget(QLabel("输入共享文件夹路径 (vvfat)"))
        self.vvfat_edit = QLineEdit()
        content_layout.addWidget(self.vvfat_edit)
        vvfat_btn = QPushButton("确定")
        vvfat_btn.clicked.connect(self.add_vvfat)
        content_layout.addWidget(vvfat_btn)

        # 光盘
        content_layout.addWidget(QLabel("输入光盘路径 (ISO)"))
        self.cd_edit = QLineEdit()
        content_layout.addWidget(self.cd_edit)
        cd_btn = QPushButton("确定")
        cd_btn.clicked.connect(self.add_cd)
        content_layout.addWidget(cd_btn)

        # 软盘
        content_layout.addWidget(QLabel("输入软盘路径"))
        self.floppy_edit = QLineEdit()
        content_layout.addWidget(self.floppy_edit)
        floppy_btn = QPushButton("确定")
        floppy_btn.clicked.connect(self.add_floppy)
        content_layout.addWidget(floppy_btn)

        # 启动设备
        content_layout.addWidget(QLabel("选择启动设备 (a/b/c/d)"))
        self.boot_combo = QComboBox()
        self.boot_combo.addItems(["", "a", "b", "c", "d"])
        content_layout.addWidget(self.boot_combo)
        boot_btn = QPushButton("确定")
        boot_btn.clicked.connect(self.add_boot)
        content_layout.addWidget(boot_btn)

        # 额外参数
        content_layout.addWidget(QLabel("输入额外 QEMU 参数"))
        self.extra_edit = QLineEdit()
        content_layout.addWidget(self.extra_edit)
        extra_btn = QPushButton("确定")
        extra_btn.clicked.connect(self.add_extra)
        content_layout.addWidget(extra_btn)

        # 启动、镜像工厂和清空按钮
        action_row = QHBoxLayout()
        run_btn = QPushButton("启动")
        run_btn.clicked.connect(self.run_vm)
        img_btn = QPushButton("镜像工厂")
        img_btn.clicked.connect(self.open_image_factory)
        clear_cmd_btn = QPushButton("清空QEMU指令")
        clear_cmd_btn.clicked.connect(self.clear_command)
        clear_all_btn = QPushButton("清空所有参数")
        clear_all_btn.clicked.connect(self.clear_all_inputs)

        action_row.addWidget(run_btn)
        action_row.addWidget(img_btn)
        action_row.addWidget(clear_cmd_btn)
        action_row.addWidget(clear_all_btn)
        content_layout.addLayout(action_row)

        # 最后更新显示
        self.update_display()

    # ---------- 基本操作函数 ----------
    def update_display(self):
        self.cmd_line.setText(" ".join(self.vm_cmd))

    def show_command(self):
        QMessageBox.information(self, "虚拟机命令", " ".join(self.vm_cmd))

    def copy_command(self):
        QApplication.clipboard().setText(" ".join(self.vm_cmd))
        QMessageBox.information(self, "成功", "命令已复制到剪贴板")

    # ---------- 参数添加函数（和原 Tkinter 对应） ----------
    def add_name(self):
        v = self.name_edit.text().strip()
        if v:
            self.vm_cmd.extend(["-name", v])
            self.update_display()

    def add_class(self):
        v = self.class_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-M", v])
            self.update_display()

    def add_accel(self):
        v = self.accel_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-accel", v])
            self.update_display()

    def add_cpu(self):
        v = self.cpu_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-cpu", v])
            self.update_display()

    def add_vga(self):
        v = self.vga_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-vga", v])
            self.update_display()

    def add_vgpu(self):
        v = self.vgpu_edit.text().strip()
        cur = self.vga_combo.currentText().strip()
        if not v:
            QMessageBox.warning(self, "警告", "请输入显存数值 (MB)")
            return
        if not v.isdigit():
            QMessageBox.warning(self, "警告", "显存必须为数字")
            return
        if cur == "std":
            self.vm_cmd.extend(["-global", f"VGA.vgamem_mb={v}"])
        elif cur == "qxl":
            self.vm_cmd.extend(["-global", f"qxl-vga.vram_size_mb={v}"])
        else:
            QMessageBox.warning(self, "提示", "当前显卡类型不支持设置显存")
            return
        self.update_display()

    def add_drive(self, index):
        edit = getattr(self, f"drive_edit_{index}")
        path = edit.text().strip()
        if not path:
            QMessageBox.warning(self, "警告", "请输入磁盘路径")
            return
        self.vm_cmd.extend(["-drive", f"file={path},if=ide,index={index},media=disk"])
        self.update_display()

    def add_ram(self):
        v = self.ram_edit.text().strip()
        if not v:
            QMessageBox.warning(self, "警告", "请输入内存大小 (MB)")
            return
        if not v.isdigit():
            QMessageBox.warning(self, "警告", "内存大小必须为数字 (MB)")
            return
        self.vm_cmd.extend(["-m", v])
        self.update_display()

    def add_bios(self):
        v = self.bios_edit.text().strip()
        if v:
            self.vm_cmd.extend(["-bios", v])
            self.update_display()

    def add_cores(self):
        v = self.cores_edit.text().strip()
        if not v:
            QMessageBox.warning(self, "警告", "请输入CPU核心数")
            return
        if not v.isdigit():
            QMessageBox.warning(self, "警告", "核心数必须为数字")
            return
        self.vm_cmd.extend(["-smp", v])
        self.update_display()

    def add_sound(self):
        v = self.sound_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-device", v])
            self.update_display()

    def add_net(self):
        v = self.net_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-device", v])
            self.update_display()

    def add_vvfat(self):
        v = self.vvfat_edit.text().strip()
        if v:
            self.vm_cmd.extend(["-drive", f"format=vvfat,dir={v},rw=on"])
            self.update_display()

    def add_cd(self):
        v = self.cd_edit.text().strip()
        if v:
            self.vm_cmd.extend(["-drive", f"file={v},if=ide,media=cdrom"])
            self.update_display()

    def add_floppy(self):
        v = self.floppy_edit.text().strip()
        if v:
            self.vm_cmd.extend(["-drive", f"file={v},if=floppy"])
            self.update_display()

    def add_boot(self):
        v = self.boot_combo.currentText().strip()
        if v:
            self.vm_cmd.extend(["-boot", v])
            self.update_display()

    def add_extra(self):
        v = self.extra_edit.text().strip()
        if v:
            # 如果以逗号开头的参数，按原逻辑拼接-machine，else直接加入
            if v.startswith(","):
                machine = "pc"
                cls = self.class_combo.currentText().strip()
                if cls:
                    machine = cls
                self.vm_cmd.extend(["-machine", f"{machine}{v}"])
            else:
                self.vm_cmd.append(v)
            self.update_display()

    # ---------- 启动与镜像工厂 ----------
    def run_vm(self):
        def target():
            try:
                # 使用 Popen 而不是 run，让 qemu 在子进程中运行且不会阻塞
                subprocess.Popen(self.vm_cmd)
            except Exception as e:
                QMessageBox.critical(self, "启动失败", str(e))
        threading.Thread(target=target, daemon=True).start()
        QMessageBox.information(self, "提示", "已在后台启动虚拟机（若命令正确）")

    def open_image_factory(self):
        dlg = ImageFactoryDialog(self)
        dlg.exec_()

    # ---------- 清空 ----------
    def clear_command(self):
        self.vm_cmd = ["qemu-system-x86_64"]
        self.update_display()

    def clear_all_inputs(self):
        # 重置命令
        self.clear_command()
        # 清空所有输入框与下拉框
        widgets = [
            self.name_edit, self.vgpu_edit, self.ram_edit, self.bios_edit,
            self.cores_edit, self.vvfat_edit, self.cd_edit, self.floppy_edit,
            self.extra_edit
        ]
        for w in widgets:
            w.clear()
        combos = [
            self.class_combo, self.accel_combo, self.cpu_combo, self.vga_combo,
            self.sound_combo, self.net_combo, self.boot_combo
        ]
        for c in combos:
            c.setCurrentIndex(0)
        for i in range(4):
            getattr(self, f"drive_edit_{i}").clear()
        QMessageBox.information(self, "提示", "已清空所有参数与命令")

def main():
    app = QApplication(sys.argv)
    win = QemuLauncher()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
