import subprocess as sp

print("===Qemu启动器电脑移植版===")

user_input = input("安装或卸载或跳过安装(只适合已安装Qemu的用户)Qemu(输入安装，卸载一键Linux命令,跳过(tg)),Windows版用户从官方网站下载QEMU(默认跳过)") or "tg"
if user_input == "安装".strip():
    sp.run(["sudo", "apt", "install", "qemu-system", "qemu-utils", "qemu-kvm", "qemu-system-gui"])
elif user_input == "卸载".strip():
    sp.run(["sudo", "apt", "remove", "qemu-system", "qemu-utils", "qemu-kvm", "qemu-system-gui"])
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
    user_input = input("输入硬盘路径(默认无)").lower().strip() or "none"
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
    user_input = input("输入任意ISO路径(默认无)").strip() or "none"
    cd_command = "-cdrom"
    cd = user_input
    user_input = input("输入引导磁盘(默认磁盘(C),磁盘启动输入C,CD启动输入D)").lower().strip() or "c"
    boot_command = "-boot"
    boot = user_input

    user_input = input("设置共享文件夹Linux共享文件夹选A,Windows选B,(回车默认无共享文件夹)") or "none"

    cmd = [bin, cls_command, cls_pc, name_command, name, cpu_command, cpu,
           core_command, core, ram_command, ram, boot_command, boot,
           s_command, s, net_command, net, vga_command, vga]

    if user_input.lower().strip() == "a":
        user_input = input("设置共享文件夹Linux输入共享文件夹路径:")
        user_input = user_input.replace("\\", "/")
        vvfat_L = f"format=vvfat,dir={user_input},rw=on"
        user_input = input("输入任意加速(默认KVM),A.KVM(Linux),B.TCG(通用)") or "a"
        if user_input.lower().strip() == "a":
            kvm = "-enable-kvm"
            cmd.insert(5, kvm)  # 在适当位置插入KVM参数
            print("虚拟机已成功运行")
        elif user_input.lower().strip() == "b":
            kvm_cmd = "-accel"
            kvm = "tcg,thread=multi"
            cmd.insert(5, kvm_cmd)
            cmd.insert(6, kvm)
            print("虚拟机已成功运行")

        if cd != "none":
            cmd.extend([cd_command, cd])
        if rom != "none":
            cmd.extend([rom_command, rom])

        cmd.extend(["-drive", vvfat_L, "-monitor", "stdio"])

        cmd_str = " ".join(cmd)
        print("\nQEMU命令（终端可直接执行）：")
        print(cmd_str)
        sp.run(cmd, check=True, shell=False)

    elif user_input.lower().strip() == "b":
        user_input = input("设置共享文件夹Windows输入共享文件夹路径:")
        user_input = user_input.replace("\\", "/")
        vvfat_W = f"format=vvfat,dir={user_input},rw=on"
        user_input = input("输入任意加速(默认TCG)A.TCG(通用),B.WHPX(Windows特有):") or "a"

        if user_input.lower().strip() == "a":
            kvm_cmd = "-accel"
            kvm = "tcg,thread=multi"
        elif user_input.lower().strip() == "b":
            kvm_cmd = "-accel"
            kvm = "whpx"


        cmd.insert(5, kvm_cmd)
        cmd.insert(6, kvm)
        print("虚拟机已成功运行")


        if cd != "none":
            cmd.extend([cd_command, cd])
        if rom != "none":
            cmd.extend([rom_command, rom])

        cmd.extend(["-drive", vvfat_W, "-monitor", "stdio"])

        cmd_str = " ".join(cmd)
        print("\nQEMU命令（终端可直接执行）：")
        print(cmd_str)
        sp.run(cmd, check=True, shell=False)

    else:
        user_input = input("Linux输入A,Windows输入B").lower().strip() or "b"
        if user_input == "a":
            user_input = input("输入任意加速(默认KVM),A.KVM(Linux),B.TCG(通用)") or "a"
            if user_input.lower().strip() == "a":
                kvm = "-enable-kvm"
                cmd.insert(5, kvm)
            elif user_input.lower().strip() == "b":
                kvm_cmd = "-accel"
                kvm = "tcg"
                cmd.insert(5, kvm_cmd)
                cmd.insert(6, kvm)
        else:
            user_input = input("输入任意加速(默认TCG)A.TCG(通用),B.WHPX(Windows特有):") or "a"
            kvm_cmd = "-accel"
            if user_input.lower().strip() == "a":
                kvm = "tcg"
            elif user_input.lower().strip() == "b":
                kvm = "whpx"
            cmd.insert(5, kvm_cmd)
            cmd.insert(6, kvm)

        print("虚拟机已成功运行")

        if cd != "none":
            cmd.extend([cd_command, cd])
        if rom != "none":
            cmd.extend([rom_command, rom])

        cmd.extend(["-monitor", "stdio"])

        cmd_str = " ".join(cmd)
        print("\nQEMU命令（终端可直接执行）：")
        print(cmd_str)
        sp.run(cmd, check=True, shell=False)
