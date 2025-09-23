import subprocess as sp
import os
print("===Qemu启动器5.0电脑移植版===")
user_input = input("安装或卸载或跳过安装(只适合已安装Qemu的用户)Qemu(输入安装，卸载一键Linux命令,跳过(tg)),Windows版用户从官方网站下载QEMU：")
if user_input == "安装".strip():
    sp.run(["sudo","apt","install","qemu-system","qemu-utils","qemu-kvm"])
elif user_input == "卸载".strip():
    sp.run(["sudo","apt","remove","qemu-system","qemu-utils","qemu-kvm"])
elif user_input == "跳过" or user_input == "tg".lower().strip():
    bin = "qemu-system-x86_64"
    cls_command = "-M"
    cls_pc = "pc"
    name_command = "-name"
    user_input = input("输入虚拟机名字(默认VM)").strip() or "VM"
    name = user_input
    cpu_command = "-cpu"
    user_input = input("输入CPU型号(默认Core 2 Duo)").strip() or "core2duo"
    cpu = user_input
    core_command = "-smp"
    user_input = input("输入核心数(默认单核)").strip() or "1"
    core = user_input
    ram_command = "-m"
    user_input = input("输入内存数量(默认1GB)").strip() or "1024"
    ram = user_input
    rom_command = "-hda"
    user_input = input("输入硬盘路径：").strip()
    user_input = user_input.replace("\\", "/")
    rom = user_input
    user_input = input("输入任意声卡(默认Intel HDA)").strip() or "intel-hda"
    s_command = "-device"
    s = user_input
    user_input = input("输入任意网卡(默认Intel E1000)").strip() or "e1000"
    net_command = "-device"
    net = user_input
    user_input = input("输入任意显卡(默认VMware SVGA)").strip() or "vmware"
    vga_command = "-vga"
    vga = user_input
    kvm_cmd = "-accel"
    user_input = input("设置共享文件夹Windows选B,Linux共享文件夹选A:")
    if user_input.lower().strip() == "a":
        user_input = input("设置共享文件夹Linux输入共享文件夹路径:")
        user_input = user_input.replace("\\", "/")
        vvfat_L = f"format=vvfat,dir={user_input},rw=on"
        user_input = input("输入任意加速(默认KVM),A.KVM(Linux),B.TCG(通用)") or "-enable-kvm"
        if user_input.lower().strip() == "a":
                kvm = "-enable-kvm"
                print("虚拟机已成功运行")
                cmd = [bin,cls_command,cls_pc,name_command,name,kvm,cpu_command,cpu,core_command,core,ram_command,ram,rom_command,rom,s_command,s,net_command,net,vga_command,vga,"-drive",vvfat_L,"-monitor","stdio"]
                cmd_str = " ".join(cmd)
                print("\nQEMU命令（终端可直接执行）：")
                print(cmd_str)
                sp.run(cmd, check=True, shell=False)
        elif user_input.lower().strip() == "b":
                kvm_cmd = "-accel"
                kvm = "tcg"
                print("虚拟机已成功运行")
                cmd = [bin,cls_command,cls_pc,name_command,name,kvm_cmd,kvm,cpu_command,cpu,core_command,core,ram_command,ram,rom_command,rom,s_command,s,net_command,net,vga_command,vga,"-drive",vvfat_L,"-monitor","stdio"]
                cmd_str = " ".join(cmd)
                print("\nQEMU命令（终端可直接执行）：")
                print(cmd_str)
                sp.run(cmd, check=True, shell=False)
    elif user_input == "B".lower().strip():
                user_input = input("设置共享文件夹Windows输入共享文件夹路径:")
                user_input = user_input.replace("\\", "/")
                vvfat_W = f"format=vvfat,dir={user_input},rw=on"
                user_input = input("输入任意加速(默认KVM)A.TCG(通用),B.WHPX(Windows特有):") or "a"
                if user_input.lower().strip() == "a":
                    kvm_cmd = "-accel"
                    kvm = "tcg"
                    print("虚拟机已成功运行")
                    cmd = [bin,cls_command,cls_pc,name_command,name,kvm_cmd,kvm,cpu_command,cpu,core_command,core,ram_command,ram,rom_command,rom,s_command,s,net_command,net,vga_command,vga,"-drive",vvfat_W,"-monitor","stdio"]
                    cmd_str = " ".join(cmd)
                    print("\nQEMU命令（终端可直接执行）：")
                    print(cmd_str)
                    sp.run(cmd, check=True, shell=False)
                elif user_input.lower().strip() == "b":
                    kvm_cmd = "-accel"
                    kvm = "whpx"
                    print("虚拟机已成功运行")
                    cmd = [bin,cls_command,cls_pc,name_command,name,kvm_cmd,kvm,cpu_command,cpu,core_command,core,ram_command,ram,rom_command,rom,s_command,s,net_command,net,vga_command,vga,"-drive",vvfat_W,"-monitor","stdio"]
                    cmd_str = " ".join(cmd)
                    print("\nQEMU命令（终端可直接执行）：")
                    print(cmd_str)
                    sp.run(cmd, check=True, shell=False)
