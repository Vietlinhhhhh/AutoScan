import os
import sys
import csv
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext

class PaymentProcessorApp:
    def __init__(self, root):


         # Get correct base directory for both EXE and script
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).parent  # EXE mode
            print(str(self.base_dir) + "exe mode")
        else:
            self.base_dir = Path(__file__).parent  # Script mode
            print(str(self.base_dir) + "Script mode") 
        self.root = root
        self.root.title("Auto Payment Processing Scanner")
        simphony_root = self.base_dir / "Simphony"
        if not simphony_root.exists():
            self.log_message("❌ Không tìm thấy thư mục Simphony", 'error')
            self.log_message(f"⚠️ Vui lòng đặt file exe cùng cấp với thư mục Simphony", 'warning')
            return
        
        # Create GUI elements
        self.create_widgets()
        
        # Start the processing loop
        self.running = True
        self.after_id = None
        self.main_loop()

    def create_widgets(self):
        # Create a frame for the display
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a scrollable text widget
        self.console_output = scrolledtext.ScrolledText(
            self.display_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=('Courier New', 10)
        )
        self.console_output.pack(fill=tk.BOTH, expand=True)
        self.console_output.tag_config('error', foreground='red')
        self.console_output.tag_config('success', foreground='green')
        self.console_output.tag_config('warning', foreground='orange')
        self.console_output.tag_config('info', foreground='blue')
        
        # Control buttons frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Stop button
        self.stop_button = tk.Button(
            self.button_frame,
            text="Stop the program",
            command=self.stop_processing,
            bg='#ff9999'
        )
        self.stop_button.pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Running...")
        self.status_label = tk.Label(
            self.button_frame,
            textvariable=self.status_var,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def log_message(self, message, tag=None):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.console_output.insert(tk.END, timestamp + message + "\n", tag)
        self.console_output.see(tk.END)
        self.root.update()

    def process_failed_folder(self, failed_folder_path, root_folder_path):
        """Xử lý các file CSV trong thư mục ThatBai"""
        self.log_message(f"🔍 Looking in folder: {failed_folder_path}", 'info')
        
        csv_files = [f for f in os.listdir(failed_folder_path) if f.lower().endswith('.csv')]
        self.log_message(f"📂 Found {len(csv_files)} CSV files in {failed_folder_path}", 'info')
        
        moved_files = []
        
        for csv_file in csv_files:
            file_path = os.path.join(failed_folder_path, csv_file)
            self.log_message(f"\n📄 Processing: {csv_file}", 'info')
            
            try:
                # First read the file content while it's safely opened
                with open(file_path, mode='r', encoding='utf-8') as file:
                    try:
                        reader = csv.reader(file)
                        first_row = next(reader)
                        
                        if len(first_row) <= 20:
                            self.log_message("❌ Error: File doesn't have enough column", 'error')
                            continue
                            
                        room_charge = int(first_row[20])  # Cột U (index 20)
                        
                        if room_charge != 21:
                            self.log_message(f"⚠️ Found Room Charge {room_charge} - Need to process!", 'warning')
                            
                            # Generate destination path
                            dest_path = Path(root_folder_path) / csv_file
                            counter = 1
                            while dest_path.exists():
                                base, ext = os.path.splitext(csv_file)
                                new_name = f"{base}_{counter}{ext}"
                                dest_path = Path(root_folder_path) / new_name
                                counter += 1
                                                      
                            try:
                                file.close()
                                shutil.move(file_path, dest_path)
                                moved_files.append(str(dest_path))
                                self.log_message(f"✅ Moved to: {dest_path}", 'success')
                            except Exception as move_error:
                                self.log_message(f"❌ Error while moving this file: {str(move_error)}", 'error')
                                
                        else:
                            self.log_message("✔️ Room Charge is 21 - Good!", 'success')
                            
                    except StopIteration:
                        self.log_message("❌ Error: Empty file!", 'error')
                    except ValueError:
                        self.log_message("❌ Error: Invalid Room Charge value", 'error')
                        
            except Exception as e:
                self.log_message(f"❌ Error while processing the file: {str(e)}", 'error')
        
        return moved_files
    
    
    def main_loop(self):
        if not self.running:
            return
            
        try:
            current_time = datetime.now()
            current_date = current_time.strftime('%d-%m-%Y')
            
            
            self.log_message(f"\n⏰ Start scanning on {current_time.strftime('%H:%M:%S')}", 'info')
            self.status_var.set(f"🔍 Scanning date: {current_date}...")
            
            # Tự động xác định thư mục Simphony
            script_dir = Path(__file__).parent
            simphony_root = script_dir / "Simphony"
            simphony_root1 = Path(os.getcwd())/ "Simphony"
            print(simphony_root)
            print(simphony_root1)

           
            
            if not simphony_root.exists():
                try: 
                    simphony_root = simphony_root1
                    if not simphony_root.exists():
                        self.log_message("❌ Still Can not found Simphony folder")
                        self.log_message("❌ Still Can not found Simphony folder XX", 'error')
                        self.after_id = self.root.after(300000, self.main_loop)  # Thử lại sau 5 phút
                        return
                except Exception as e:
                       self.log_message("❌ Still Can not found Simphony folder")
                self.log_message("❌ Can not found Simphony folder, try to put AutoScan.exe same level with Simphony", 'error')
                self.after_id = self.root.after(300000, self.main_loop)  # Thử lại sau 5 phút
                return
                
            # Quét tất cả các outlet (101, 102,...)
            outlets = [d for d in simphony_root.iterdir() if d.is_dir() and d.name.isdigit()]
            
            if not outlets:
                self.log_message("❌ Can't find any outlets (101, 102,...)", 'error')
            else:
                total_moved = 0
                
                for outlet in outlets:
                    outlet_name = outlet.name
                    self.log_message(f"\n🏬 Processing outlet {outlet_name}", 'info')
                    
                    failed_folder = outlet / f"{outlet_name}-cash" / "ThatBai" / current_date
                    target_folder = outlet / f"{outlet_name}-cash"
                    
                    if not failed_folder.exists():
                        self.log_message(f"ℹ️ ThatBai folder doesn't exist /{current_date}", 'info')
                        continue
                        
                    moved_files = self.process_failed_folder(str(failed_folder), str(target_folder))
                    total_moved += len(moved_files)
                    
                    if moved_files:
                        self.log_message(f"📤 moved {len(moved_files)} files from outlet {outlet_name}", 'success')
            
            self.log_message(f"\n✅ Process finished! Moved {total_moved} files.", 'success')
            self.status_var.set(f"🟢 Process finished att {current_time.strftime('%H:%M:%S')}. Next scan after 5 minutes...")
            
        except Exception as e:
            self.log_message(f"❌ Critical Error: {str(e)}", 'error')
            self.status_var.set("🔴 Error. Trying again after 1 minutes...")
            self.after_id = self.root.after(60000, self.main_loop)  # Thử lại sau 1 phút
            return
            
        # Lên lịch chạy lại sau 5 phút
        self.after_id = self.root.after(300000, self.main_loop)

    def stop_processing(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.status_var.set("🛑 Program stopped")
        self.log_message("\n🛑 Program stopped by user.", 'info')
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentProcessorApp(root)
    root.mainloop()
