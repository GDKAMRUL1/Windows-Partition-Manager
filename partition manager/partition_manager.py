import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import wmi
import win32api
import win32file
from threading import Thread
import ctypes

class PartitionManager:
    def __init__(self):
        self.diskpart_script = "diskpart_commands.txt"

    def run_diskpart_command(self, commands):
        # Write commands to temporary script file
        with open(self.diskpart_script, "w") as f:
            for cmd in commands:
                f.write(cmd + "\n")
        
        # Run diskpart with the script
        try:
            result = subprocess.run(["diskpart", "/s", self.diskpart_script], 
                                  capture_output=True, 
                                  text=True)
            print(result.stdout)
            return result.stdout
        except Exception as e:
            print(f"Error executing diskpart: {e}")
        finally:
            # Clean up temporary script file
            if os.path.exists(self.diskpart_script):
                os.remove(self.diskpart_script)

    def list_disks(self):
        commands = ["list disk"]
        return self.run_diskpart_command(commands)

    def list_partitions(self, disk_number):
        commands = [
            f"select disk {disk_number}",
            "list partition"
        ]
        return self.run_diskpart_command(commands)

    def create_partition(self, disk_number, size_mb):
        commands = [
            f"select disk {disk_number}",
            f"create partition primary size={size_mb}"
        ]
        return self.run_diskpart_command(commands)

    def delete_partition(self, disk_number, partition_number):
        commands = [
            f"select disk {disk_number}",
            f"select partition {partition_number}",
            "delete partition"
        ]
        return self.run_diskpart_command(commands)

    def extend_partition(self, disk_number, partition_number):
        commands = [
            f"select disk {disk_number}",
            f"select partition {partition_number}",
            "extend"
        ]
        return self.run_diskpart_command(commands)

    def extend_partition_with_size(self, disk_number, partition_number, size_mb):
        commands = [
            f"select disk {disk_number}",
            f"select partition {partition_number}",
            f"extend size={size_mb}"
        ]
        return self.run_diskpart_command(commands)

    def get_disk_details(self, disk_number):
        commands = [
            f"select disk {disk_number}",
            "detail disk"
        ]
        return self.run_diskpart_command(commands)

    def get_partition_details(self, disk_number, partition_number):
        commands = [
            f"select disk {disk_number}",
            f"select partition {partition_number}",
            "detail partition"
        ]
        return self.run_diskpart_command(commands)

    def shrink_partition(self, disk_number, partition_number, size_mb):
        commands = [
            f"select disk {disk_number}",
            f"select partition {partition_number}",
            f"shrink desired={size_mb}"
        ]
        return self.run_diskpart_command(commands)

    def convert_disk(self, disk_number, type_to):
        """Convert disk between MBR and GPT"""
        if type_to not in ['gpt', 'mbr']:
            raise ValueError("Type must be 'gpt' or 'mbr'")
        commands = [
            f"select disk {disk_number}",
            f"convert {type_to}"
        ]
        return self.run_diskpart_command(commands)

class PartitionManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Partition Manager - by Kamrul Mollah")
        self.root.geometry("800x600")
        self.wmi = wmi.WMI()
        self.pm = PartitionManager()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create disk list
        self.create_disk_view()
        
        # Create partition list
        self.create_partition_view()
        
        # Create buttons
        self.create_buttons()
        
        # Create advanced options
        self.create_advanced_menu()
        
        # Add developer info
        self.create_developer_info()
        
        # Initialize displays
        self.refresh_disk_list()

    def create_disk_view(self):
        # Disk list frame
        disk_frame = ttk.LabelFrame(self.main_frame, text="Disks", padding="5")
        disk_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Disk Treeview
        self.disk_tree = ttk.Treeview(disk_frame, columns=("Size", "Interface"), show="headings")
        self.disk_tree.heading("Size", text="Size (GB)")
        self.disk_tree.heading("Interface", text="Interface")
        self.disk_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for disk list
        disk_scroll = ttk.Scrollbar(disk_frame, orient=tk.VERTICAL, command=self.disk_tree.yview)
        disk_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.disk_tree.configure(yscrollcommand=disk_scroll.set)
        
        # Bind selection event
        self.disk_tree.bind("<<TreeviewSelect>>", self.on_disk_select)

    def create_partition_view(self):
        # Partition list frame
        part_frame = ttk.LabelFrame(self.main_frame, text="Partitions", padding="5")
        part_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Partition Treeview
        self.part_tree = ttk.Treeview(part_frame, 
                                     columns=("Size", "Free", "FS", "Letter"),
                                     show="headings")
        self.part_tree.heading("Size", text="Size (GB)")
        self.part_tree.heading("Free", text="Free (GB)")
        self.part_tree.heading("FS", text="File System")
        self.part_tree.heading("Letter", text="Drive Letter")
        self.part_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for partition list
        part_scroll = ttk.Scrollbar(part_frame, orient=tk.VERTICAL, command=self.part_tree.yview)
        part_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.part_tree.configure(yscrollcommand=part_scroll.set)

    def create_buttons(self):
        btn_frame = ttk.Frame(self.main_frame, padding="5")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_disk_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Create Partition", command=self.create_partition_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Partition", command=self.delete_partition_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Extend Partition", command=self.extend_partition_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Change Drive Letter", command=self.change_letter_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Advanced Options", command=self.create_advanced_menu).pack(side=tk.LEFT, padx=5)

    def refresh_disk_list(self):
        # Clear existing items
        self.disk_tree.delete(*self.disk_tree.get_children())
        self.part_tree.delete(*self.part_tree.get_children())
        
        # Get physical disks
        for disk in self.wmi.Win32_DiskDrive():
            try:
                size_gb = round(int(disk.Size) / (1024**3), 2) if disk.Size else 0
                self.disk_tree.insert("", tk.END, 
                                    values=(size_gb, disk.InterfaceType or "Unknown"),
                                    iid=disk.Index)
            except (ValueError, TypeError, AttributeError):
                # Handle case where disk size or other attributes are not available
                self.disk_tree.insert("", tk.END, 
                                    values=("Unknown", disk.InterfaceType or "Unknown"),
                                    iid=disk.Index)

    def on_disk_select(self, event):
        selection = self.disk_tree.selection()
        if not selection:
            return
            
        disk_index = selection[0]
        self.refresh_partition_list(disk_index)

    def refresh_partition_list(self, disk_index):
        self.part_tree.delete(*self.part_tree.get_children())
        
        try:
            # Get partitions for selected disk
            disk = self.wmi.Win32_DiskDrive(Index=int(disk_index))[0]
            for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    try:
                        size_gb = round(int(logical_disk.Size) / (1024**3), 2) if logical_disk.Size else 0
                        free_gb = round(int(logical_disk.FreeSpace) / (1024**3), 2) if logical_disk.FreeSpace else 0
                        self.part_tree.insert("", tk.END,
                                            values=(size_gb, free_gb,
                                                   logical_disk.FileSystem or "Unknown",
                                                   logical_disk.DeviceID or "None"))
                    except (ValueError, TypeError, AttributeError):
                        self.part_tree.insert("", tk.END,
                                            values=("Unknown", "Unknown",
                                                   "Unknown",
                                                   logical_disk.DeviceID or "None"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get partition information: {str(e)}")

    def create_partition_dialog(self):
        if not self.disk_tree.selection():
            messagebox.showwarning("Warning", "Please select a disk first")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Partition")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Size (MB):").pack(pady=5)
        size_entry = ttk.Entry(dialog)
        size_entry.pack(pady=5)
        
        def create():
            try:
                disk_index = self.disk_tree.selection()[0]
                size = size_entry.get()
                Thread(target=self._create_partition, args=(disk_index, size)).start()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Create", command=create).pack(pady=10)

    def _create_partition(self, disk_index, size):
        try:
            self.pm.create_partition(disk_index, size)
            self.root.after(1000, self.refresh_disk_list)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_partition_dialog(self):
        if not self.disk_tree.selection():
            messagebox.showwarning("Warning", "Please select a disk first")
            return
            
        if not self.part_tree.selection():
            messagebox.showwarning("Warning", "Please select a partition first")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this partition? This cannot be undone!"):
            disk_index = self.disk_tree.selection()[0]
            partition = self.part_tree.selection()[0]
            Thread(target=self._delete_partition, args=(disk_index, partition)).start()

    def _delete_partition(self, disk_index, partition):
        try:
            self.pm.delete_partition(disk_index, partition)
            self.root.after(1000, self.refresh_disk_list)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extend_partition_dialog(self):
        if not self.disk_tree.selection():
            messagebox.showwarning("Warning", "Please select a disk first")
            return
            
        if not self.part_tree.selection():
            messagebox.showwarning("Warning", "Please select a partition first")
            return
            
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Extend Partition")
        dialog.geometry("400x200")
        
        # Add input fields
        ttk.Label(dialog, text="Size to extend (MB):").pack(pady=5)
        size_entry = ttk.Entry(dialog)
        size_entry.pack(pady=5)
        
        # Add warning label
        warning_text = ("Warning: Make sure there is unallocated space available.\n"
                       "The space must be contiguous and after the partition.\n"
                       "Example: To extend by 50GB, enter: 51200")
        ttk.Label(dialog, text=warning_text, wraplength=350).pack(pady=10)
        
        def extend():
            try:
                disk_index = self.disk_tree.selection()[0]
                partition_index = self.part_tree.selection()[0]
                size_mb = size_entry.get()
                if not size_mb.isdigit():
                    raise ValueError("Size must be a positive number")
                Thread(target=self._extend_partition_with_size, 
                       args=(disk_index, partition_index, size_mb)).start()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Extend", command=extend).pack(pady=10)

    def _extend_partition_with_size(self, disk_index, partition_index, size_mb):
        try:
            self.pm.extend_partition_with_size(disk_index, partition_index, size_mb)
            self.root.after(1000, self.refresh_disk_list)
            messagebox.showinfo("Success", "Partition extended successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extend partition: {str(e)}")

    def change_letter_dialog(self):
        # Implementation for drive letter change would go here
        messagebox.showinfo("Info", "Drive letter change feature coming soon!")

    def create_advanced_menu(self):
        advanced_frame = ttk.LabelFrame(self.main_frame, text="Advanced Options", padding="5")
        advanced_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Advanced buttons
        ttk.Button(advanced_frame, text="Disk Details", 
                   command=self.show_disk_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(advanced_frame, text="Partition Details", 
                   command=self.show_partition_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(advanced_frame, text="Shrink Partition", 
                   command=self.shrink_partition_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(advanced_frame, text="Convert Disk", 
                   command=self.convert_disk_dialog).pack(side=tk.LEFT, padx=5)

    def show_disk_details(self):
        if not self.disk_tree.selection():
            messagebox.showwarning("Warning", "Please select a disk first")
            return
        
        disk_index = self.disk_tree.selection()[0]
        details = self.pm.get_disk_details(disk_index)
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Disk {disk_index} Details")
        details_window.geometry("600x400")
        
        # Add text widget with scrollbar
        text_widget = tk.Text(details_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(details_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, details)
        text_widget.configure(state='disabled')

    def show_partition_details(self):
        if not all([self.disk_tree.selection(), self.part_tree.selection()]):
            messagebox.showwarning("Warning", "Please select both disk and partition")
            return
        
        disk_index = self.disk_tree.selection()[0]
        partition_index = self.part_tree.selection()[0]
        details = self.pm.get_partition_details(disk_index, partition_index)
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Partition Details")
        details_window.geometry("600x400")
        
        text_widget = tk.Text(details_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(details_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, details)
        text_widget.configure(state='disabled')

    def shrink_partition_dialog(self):
        if not all([self.disk_tree.selection(), self.part_tree.selection()]):
            messagebox.showwarning("Warning", "Please select both disk and partition")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Shrink Partition")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Amount to shrink (MB):").pack(pady=5)
        size_entry = ttk.Entry(dialog)
        size_entry.pack(pady=5)
        
        warning_text = ("Warning: Shrinking a partition may make some files inaccessible.\n"
                       "Make sure to backup important data before proceeding.\n"
                       "Example: To shrink by 50GB, enter: 51200")
        ttk.Label(dialog, text=warning_text, wraplength=350).pack(pady=10)
        
        def shrink():
            try:
                disk_index = self.disk_tree.selection()[0]
                partition_index = self.part_tree.selection()[0]
                size_mb = size_entry.get()
                if not size_mb.isdigit():
                    raise ValueError("Size must be a positive number")
                Thread(target=self._shrink_partition, 
                       args=(disk_index, partition_index, size_mb)).start()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Shrink", command=shrink).pack(pady=10)

    def _shrink_partition(self, disk_index, partition_index, size_mb):
        try:
            self.pm.shrink_partition(disk_index, partition_index, size_mb)
            self.root.after(1000, self.refresh_disk_list)
            messagebox.showinfo("Success", "Partition shrunk successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to shrink partition: {str(e)}")

    def convert_disk_dialog(self):
        if not self.disk_tree.selection():
            messagebox.showwarning("Warning", "Please select a disk first")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Convert Disk")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Convert disk to:").pack(pady=5)
        disk_type = tk.StringVar(value="gpt")
        ttk.Radiobutton(dialog, text="GPT (UEFI)", variable=disk_type, 
                        value="gpt").pack(pady=5)
        ttk.Radiobutton(dialog, text="MBR (Legacy BIOS)", variable=disk_type, 
                        value="mbr").pack(pady=5)
        
        warning_text = ("WARNING: Converting a disk will delete all partitions!\n"
                       "Make sure to backup all data before proceeding.")
        ttk.Label(dialog, text=warning_text, wraplength=350).pack(pady=10)
        
        def convert():
            if messagebox.askyesno("Confirm", 
                                  "This will DELETE ALL DATA on the disk. Continue?"):
                try:
                    disk_index = self.disk_tree.selection()[0]
                    Thread(target=self._convert_disk, 
                           args=(disk_index, disk_type.get())).start()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Convert", command=convert).pack(pady=10)

    def _convert_disk(self, disk_index, type_to):
        try:
            self.pm.convert_disk(disk_index, type_to)
            self.root.after(1000, self.refresh_disk_list)
            messagebox.showinfo("Success", "Disk converted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert disk: {str(e)}")

    def create_developer_info(self):
        # Create developer info frame at the bottom
        dev_frame = ttk.Frame(self.main_frame, padding="5")
        dev_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Developer information
        dev_info = "Developer: KAMRUL MOLLAH | Mobile: 01990646194 | Website: kamrulmollah.com"
        dev_label = ttk.Label(dev_frame, text=dev_info, 
                             font=('Arial', 9), foreground='#666666')
        dev_label.pack(side=tk.LEFT)
        
        # Make website clickable
        website_label = ttk.Label(dev_frame, text="Visit Website", 
                                font=('Arial', 9, 'underline'), 
                                foreground='blue', cursor='hand2')
        website_label.pack(side=tk.RIGHT)
        website_label.bind("<Button-1>", lambda e: self.open_website())

    def open_website(self):
        import webbrowser
        webbrowser.open("http://kamrulmollah.com")

def main():
    # Replace the Unix-specific check with a Windows admin check
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("Error", "This application must be run as administrator")
        sys.exit(1)

    root = tk.Tk()
    app = PartitionManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 