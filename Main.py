from tkinter import *
from subprocess import *
from tkinter import ttk,messagebox
import threading
class MainUI:
    def __init__(self):
        self.vm_cmd = ["qemu-system-x86_64"]
        self.root = Tk()
        self.root.title("Qemu启动器1.0")
        self.root.geometry("300x900")
        #虚拟机名字
        def vmruncmd():
            self.command_str = " ".join(self.vm_cmd)
            messagebox.showerror("命令", self.command_str)
        self.vm_cmd_cmd = ttk.Button(self.root,text="虚拟机命令",command=vmruncmd)
        self.vm_cmd_cmd.pack()
        self.vm_name_title = Label(self.root,text="输入虚拟机名字")
        self.vm_name_title.pack()
        self.vm_name_1 = Entry(self.root)
        self.vm_name_1.pack()
        def addname():
            self.vm_name = self.vm_name_1.get()
            self.vm_cmd.extend(["-name", self.vm_name])
        self.vm_name_button = ttk.Button(self.root,text="确定",command=addname)
        self.vm_name_button.pack()
        #虚拟机类型
        self.vm_class_title = Label(self.root,text="输入虚拟机类型")
        self.vm_class_title.pack()
        self.vm_class_1 = Entry(self.root)
        self.vm_class_1.pack()
        def addclass():
            self.vm_class = self.vm_class_1.get()
            self.vm_cmd.extend(["-M", self.vm_class])
        self.vm_class_button = ttk.Button(self.root,text="确定",command=addclass)
        self.vm_class_button.pack()
        #虚拟机加速
        self.vm_kvm_title = Label(self.root,text="输入虚拟机加速")
        self.vm_kvm_title.pack()
        self.vm_kvm_1 = Entry(self.root)
        self.vm_kvm_1.pack()
        def addkvm():
            self.vm_kvm = self.vm_kvm_1.get()
            self.vm_cmd.extend(["-accel", self.vm_kvm])
        self.vm_kvm_button = ttk.Button(self.root,text="确定",command=addkvm)
        self.vm_kvm_button.pack()
        #虚拟机CPU
        self.vm_cpu_title = Label(self.root,text="输入CPU型号")
        self.vm_cpu_title.pack()
        self.vm_cpu_1 = Entry(self.root)
        self.vm_cpu_1.pack()
        def addcpu():
            self.vm_cpu = self.vm_cpu_1.get()
            self.vm_cmd.extend(["-cpu", self.vm_cpu])
        self.vm_cpu_button = ttk.Button(self.root,text="确定",command=addcpu)
        self.vm_cpu_button.pack()
        #虚拟机显卡
        self.vm_gpu_title = Label(self.root,text="输入显卡型号")
        self.vm_gpu_title.pack()
        self.vm_gpu_1 = Entry(self.root)
        self.vm_gpu_1.pack()
        def addgpu():
            self.vm_gpu = self.vm_gpu_1.get()
            self.vm_cmd.extend(["-vga", self.vm_gpu])
        self.vm_gpu_button = ttk.Button(self.root,text="确定",command=addgpu)
        self.vm_gpu_button.pack()
        #虚拟机磁盘
        self.vm_hd_title = Label(self.root,text="输入磁盘路径")
        self.vm_hd_title.pack()
        self.vm_hd_1 = Entry(self.root)
        self.vm_hd_1.pack()
        def addhd():
            self.vm_hd = self.vm_hd_1.get()
            self.vm_cmd.extend(["-hda", self.vm_hd])
        self.vm_hd_button = ttk.Button(self.root,text="确定",command=addhd)
        self.vm_hd_button.pack()
        #虚拟机内存
        self.vm_ram_title = Label(self.root,text="输入内存容量MB")
        self.vm_ram_title.pack()
        self.vm_ram_1 = Entry(self.root)
        self.vm_ram_1.pack()
        def addram():
            self.vm_ram = self.vm_ram_1.get()
            self.vm_cmd.extend(["-m", self.vm_ram])
        self.vm_ram_button = ttk.Button(self.root,text="确定",command=addram)
        self.vm_ram_button.pack()
        #虚拟机核心
        self.vm_core_title = Label(self.root,text="输入CPU核心")
        self.vm_core_title.pack()
        self.vm_core_1 = Entry(self.root)
        self.vm_core_1.pack()
        def addcore():
            self.vm_core = self.vm_core_1.get()
            self.vm_cmd.extend(["-smp", self.vm_core])
        self.vm_core_button = ttk.Button(self.root,text="确定",command=addcore)
        self.vm_core_button.pack()
        #虚拟机声卡
        self.vm_sound_title = Label(self.root,text="输入声卡型号")
        self.vm_sound_title.pack()
        self.vm_sound_1 = Entry(self.root)
        self.vm_sound_1.pack()
        def addsound():
            self.vm_sound = self.vm_sound_1.get()
            self.vm_cmd.extend(["-device", self.vm_sound])
        self.vm_sound_button = ttk.Button(self.root,text="确定",command=addsound)
        self.vm_sound_button.pack()
        #虚拟机网卡
        self.vm_net_title = Label(self.root,text="输入网卡型号")
        self.vm_net_title.pack()
        self.vm_net_1 = Entry(self.root)
        self.vm_net_1.pack()
        def addnet():
            self.vm_net = self.vm_net_1.get()
            self.vm_cmd.extend(["-device", self.vm_net])
        self.vm_net_button = ttk.Button(self.root,text="确定",command=addnet)
        self.vm_net_button.pack()
        #虚拟机共享文件夹
        self.vm_vvfat_title = Label(self.root,text="输入共享文件夹路径")
        self.vm_vvfat_title.pack()
        self.vm_vvfat_1 = Entry(self.root)
        self.vm_vvfat_1.pack()
        def addvvfat():
            self.vm_vvfat = self.vm_vvfat_1.get()
            self.vm_cmd.extend(["-drive", f"format=vvfat,dir={self.vm_vvfat},rw=on"])
        self.vm_vvfat_button = ttk.Button(self.root,text="确定",command=addvvfat)
        self.vm_vvfat_button.pack()
        #虚拟机启动
        def vmrun1():
            run(self.vm_cmd)
        def vmrun():
            thread = threading.Thread(target=vmrun1, daemon=True)
            thread.start()
        self.vmrunbutton = ttk.Button(self.root,text="启动",command=vmrun)
        self.vmrunbutton.pack()
        #清空按钮
        def clear_config():
            self.vm_cmd = ["qemu-system-x86_64"]
            entries = [
                self.vm_name_1, self.vm_class_1, self.vm_kvm_1,
                self.vm_cpu_1, self.vm_gpu_1, self.vm_hd_1,
                self.vm_vvfat_1, self.vm_ram_1, self.vm_core_1,self.vm_sound_1,self.vm_net_1
            ]
        self.clear_button = ttk.Button(self.root,text="清空",command=clear_config).pack()
        self.root.mainloop()
MainUI()
