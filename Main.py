from tkinter import *
from subprocess import *
from tkinter import ttk,messagebox
import threading
class MainUI:
    def __init__(self):
        #初始化
        self.vm_cmd = ["qemu-system-x86_64"]
        self.root = Tk()
        self.root.title("Qemu启动器1.1")
        self.root.geometry("260x480")
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y")
        canvas = Canvas(self.root, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        self.main_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.main_frame.bind("<Configure>", configure_canvas)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)

        #虚拟机名字
        def vmruncmd():
            self.command_str = " ".join(self.vm_cmd)
            messagebox.showinfo("命令", self.command_str)
        self.vm_cmd_cmd = ttk.Button(self.main_frame,text="虚拟机命令",command=vmruncmd)
        self.vm_cmd_cmd.pack()
        self.vm_name_title = Label(self.main_frame,text="输入虚拟机名字")
        self.vm_name_title.pack()
        self.vm_name_1 = ttk.Entry(self.main_frame)
        self.vm_name_1.pack()
        def addname():
            self.vm_name = self.vm_name_1.get()
            self.vm_cmd.extend(["-name", self.vm_name])
        self.vm_name_button = ttk.Button(self.main_frame,text="确定",command=addname)
        self.vm_name_button.pack()
        #虚拟机类型
        self.vm_class_title = Label(self.main_frame,text="选择虚拟机类型")
        self.vm_class_title.pack()
        self.class_var = StringVar()
        self.class_combo = ttk.Combobox(self.main_frame, textvariable=self.class_var)
        self.class_combo['values'] = ("pc","q35")
        self.class_combo.pack()
        def addclass():
            selected_class = self.class_var.get()
            if selected_class and not selected_class.startswith("---"):
                self.vm_cmd.extend(["-M", selected_class])
        self.vm_class_button = ttk.Button(self.main_frame,text="确定",command=addclass)
        self.vm_class_button.pack()
        #虚拟机加速
        self.vm_kvm_title = Label(self.main_frame,text="选择加速器")
        self.vm_kvm_title.pack()
        self.kvm_var = StringVar()
        self.kvm_combo = ttk.Combobox(self.main_frame, textvariable=self.kvm_var)
        self.kvm_combo['values'] = ("kvm","tcg","whpx")
        self.kvm_combo.pack()
        def addkvm():
            selected_kvm = self.kvm_var.get()
            if selected_kvm and not selected_kvm.startswith("---"):
                self.vm_cmd.extend(["-accel", selected_kvm])
        self.vm_kvm_button = ttk.Button(self.main_frame,text="确定",command=addkvm)
        self.vm_kvm_button.pack()
        #虚拟机CPU
        self.vm_cpu_title = Label(self.main_frame,text="选择CPU型号")
        self.vm_cpu_title.pack()
        self.cpu_var = StringVar()
        self.cpu_combo = ttk.Combobox(self.main_frame, textvariable=self.cpu_var)
        self.cpu_combo['values'] = (
            "486", "pentium", "pentium2", "pentium3",
            "coreduo", "core2duo", "phenom", "athlon64",
            "qemu64", "host", "epyc","qemu32"
        )
        self.cpu_combo.pack()
        def addcpu():
            selected_cpu = self.cpu_var.get()
            if selected_cpu and not selected_cpu.startswith("---"):
                self.vm_cmd.extend(["-cpu", selected_cpu])
        self.vm_cpu_button = ttk.Button(self.main_frame,text="确定",command=addcpu)
        self.vm_cpu_button.pack()
        #虚拟机显卡
        self.vm_gpu_title = Label(self.main_frame,text="选择显卡型号")
        self.vm_gpu_title.pack()
        self.gpu_var = StringVar()
        self.gpu_combo = ttk.Combobox(self.main_frame, textvariable=self.gpu_var)
        self.gpu_combo['values'] = (
            "vmware", "cirrus", "std", "qxl",
        )
        self.gpu_combo.pack()
        def addgpu():
            selected_gpu = self.gpu_var.get()
            if selected_gpu and not selected_gpu.startswith("---"):
                self.vm_cmd.extend(["-vga", selected_gpu])
        self.vm_gpu_button = ttk.Button(self.main_frame,text="确定",command=addgpu)
        self.vm_gpu_button.pack()
        #虚拟机显存
        self.vm_vgpu_title = Label(self.main_frame,text="输入显存")
        self.vm_vgpu_title.pack()
        self.vm_vgpu_1 = ttk.Entry(self.main_frame)
        self.vm_vgpu_1.pack()
        self.vm_vgpu = self.vm_vgpu_1.get()
        def addvgpu():
            self.current_gpu = self.gpu_var.get()
            # 从输入框直接获取当前显卡类型，而不是依赖变量
            if self.current_gpu == "std":
                self.vm_cmd.extend(["-global", f"VGA.vgamem_mb={self.vm_vgpu}"])
            elif self.current_gpu == "qxl":
                self.vm_cmd.extend(["-global", f"qxl-vga.vram_size_mb={self.vm_vgpu}"])
            else:
                messagebox.showwarning("QEMU启动器","暂不支持此显卡增加显存")
        self.vm_vgpu_button = ttk.Button(self.main_frame,text="确定",command=addvgpu)
        self.vm_vgpu_button.pack()
        #虚拟机磁盘
        self.vm_hd_title = Label(self.main_frame,text="输入磁盘路径")
        self.vm_hd_title.pack()
        self.vm_hd_1 = ttk.Entry(self.main_frame)
        self.vm_hd_1.pack()
        def addhd():
            self.vm_hd = self.vm_hd_1.get()
            self.vm_cmd.extend(["-hda", self.vm_hd])
        self.vm_hd_button = ttk.Button(self.main_frame,text="确定",command=addhd)
        self.vm_hd_button.pack()
        #虚拟机内存
        self.vm_ram_title = Label(self.main_frame,text="输入内存容量MB")
        self.vm_ram_title.pack()
        self.vm_ram_1 = ttk.Entry(self.main_frame)
        self.vm_ram_1.pack()
        def addram():
            self.vm_ram = self.vm_ram_1.get()
            self.vm_cmd.extend(["-m", self.vm_ram])
        self.vm_ram_button = ttk.Button(self.main_frame,text="确定",command=addram)
        self.vm_ram_button.pack()
        #虚拟机核心
        self.vm_core_title = Label(self.main_frame,text="输入CPU核心")
        self.vm_core_title.pack()
        self.vm_core_1 = ttk.Entry(self.main_frame)
        self.vm_core_1.pack()
        def addcore():
            self.vm_core = self.vm_core_1.get()
            self.vm_cmd.extend(["-smp", self.vm_core])
        self.vm_core_button = ttk.Button(self.main_frame,text="确定",command=addcore)
        self.vm_core_button.pack()
        #虚拟机声卡
        self.vm_sound_title = Label(self.main_frame,text="选择声卡型号")
        self.vm_sound_title.pack()
        self.sound_var = StringVar()
        self.sound_combo = ttk.Combobox(self.main_frame, textvariable=self.sound_var)
        self.sound_combo['values'] = (
            "ac97", "sb16", "intel-hda", "es1370"
        )
        self.sound_combo.pack()
        def addsound():
            selected_sound = self.sound_var.get()
            if selected_sound and not selected_sound.startswith("---"):
                self.vm_cmd.extend(["-device", selected_sound])
        self.vm_sound_button = ttk.Button(self.main_frame,text="确定",command=addsound)
        self.vm_sound_button.pack()
        #虚拟机网卡
        self.vm_net_title = Label(self.main_frame, text="选择网卡型号")
        self.vm_net_title.pack()
        self.net_var = StringVar()
        self.net_combo = ttk.Combobox(self.main_frame, textvariable=self.net_var)
        self.net_combo['values'] = (
            "e1000", "rtl8139", "ne2k_pci",
        )
        self.net_combo.pack()

        def addnet():
            selected_net = self.net_var.get()
            if selected_net and not selected_net.startswith("---"):
                self.vm_cmd.extend(["-device", selected_net])

        self.vm_net_button = ttk.Button(self.main_frame, text="确定", command=addnet)
        self.vm_net_button.pack()
        #虚拟机共享文件夹
        self.vm_vvfat_title = Label(self.main_frame,text="输入共享文件夹路径")
        self.vm_vvfat_title.pack()
        self.vm_vvfat_1 = ttk.Entry(self.main_frame)
        self.vm_vvfat_1.pack()
        def addvvfat():
            self.vm_vvfat = self.vm_vvfat_1.get()
            self.vm_cmd.extend(["-drive", f"format=vvfat,dir={self.vm_vvfat},rw=on"])
        self.vm_vvfat_button = ttk.Button(self.main_frame,text="确定",command=addvvfat)
        self.vm_vvfat_button.pack()
        #虚拟机光盘
        self.vm_cd_title = Label(self.main_frame,text="输入光盘路径")
        self.vm_cd_title.pack()
        self.vm_cd_1 = ttk.Entry(self.main_frame)
        self.vm_cd_1.pack()
        def addcd():
            self.vm_cd = self.vm_cd_1.get()
            self.vm_cmd.extend(["-cdrom", self.vm_cd])
        self.vm_cd_button = ttk.Button(self.main_frame,text="确定",command=addcd)
        self.vm_cd_button.pack()
        #虚拟机软盘
        self.vm_f_title = Label(self.main_frame,text="输入软盘路径")
        self.vm_f_title.pack()
        self.vm_f_1 = ttk.Entry(self.main_frame)
        self.vm_f_1.pack()
        def addf():
            self.vm_f = self.vm_f_1.get()
            self.vm_cmd.extend(["-fda", self.vm_f])
        self.vm_f_button = ttk.Button(self.main_frame,text="确定",command=addf)
        self.vm_f_button.pack()
        #虚拟机启动选项
        self.vm_boot_title = Label(self.main_frame, text="选择启动选项")
        self.vm_boot_title.pack()
        self.boot_var = StringVar()
        self.boot_combo = ttk.Combobox(self.main_frame, textvariable=self.boot_var)
        self.boot_combo['values'] = (
            "c", "d", "a",
        )
        self.boot_combo.pack()

        def addboot():
            selected_boot = self.boot_var.get()
            if selected_boot and not selected_boot.startswith("---"):
                self.vm_cmd.extend(["-device", selected_boot])

        self.vm_boot_button = ttk.Button(self.main_frame, text="确定", command=addboot)
        self.vm_boot_button.pack()
        #虚拟机高级参数
        self.vm_tall_title = Label(self.main_frame,text="输入额外QEMU参数")
        self.vm_tall_title.pack()
        self.vm_tall_1 = ttk.Entry(self.main_frame)
        self.vm_tall_1.pack()
        def addtall():
            self.vm_tall = self.vm_tall_1.get()
            self.vm_cmd.extend([self.vm_tall])
        self.vm_tall_button = ttk.Button(self.main_frame,text="确定",command=addtall)
        self.vm_tall_button.pack()
        #虚拟机启动
        def vmrun1():
            run(self.vm_cmd)
        def vmrun():
            thread = threading.Thread(target=vmrun1, daemon=True)
            thread.start()
        self.vmrunbutton = ttk.Button(self.main_frame,text="启动",command=vmrun)
        self.vmrunbutton.pack()
        #清空按钮
        def clear_config():
            self.vm_cmd = ["qemu-system-x86_64"]
            self.clear_button = ttk.Button(self.main_frame,text="清空QEMU指令",command=clear_config).pack()
            self.vm_cmd = ["qemu-system-x86_64"]

            # 清空所有输入框 (Entry)
            entries = [
                self.vm_name_1, self.vm_hd_1, self.vm_vvfat_1,
                self.vm_ram_1, self.vm_core_1, self.vm_cd_1,
                self.vm_tall_1, self.vm_f_1, self.vm_vgpu_1
            ]
            for entry in entries:
                entry.delete(0, END)

            # 清空所有组合框 (Combobox)
            combos = [
                self.class_combo,  # 虚拟机类型
                self.kvm_combo,  # 加速器
                self.cpu_combo,  # CPU型号
                self.gpu_combo,  # 显卡型号
                self.sound_combo,  # 声卡型号
                self.net_combo,  # 网卡型号
                self.boot_combo  # 启动选项
            ]
            for combo in combos:
                combo.set('')  # 清空组合框选择

        self.clear_button_1 = ttk.Button(self.main_frame, text="清空所有参数", command=clear_config)
        self.clear_button_1.pack()
        self.root.mainloop()
MainUI()
