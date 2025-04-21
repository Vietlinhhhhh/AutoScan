# import os
# import csv
# import shutil
# import time
# from datetime import datetime
# from pathlib import Path
# import tkinter as tk
# from tkinter import scrolledtext

# def process_failed_folder(failed_folder_path, target_folder_path):
#     """Xử lý các file CSV trong thư mục ThatBai"""
#     print(f"🔍 Đang tìm kiếm trong thư mục: {failed_folder_path}")
#     # Chỉ lấy file CSV có tên ngắn hơn 41 ký tự
#     # csv_files = [f for f in os.listdir(failed_folder_path) 
#     #             if f.lower().endswith('.csv') and len(f) < 41]
    
#     # date_folder = os.path.basename(failed_folder_path)
#     # print(f"📂 Tìm thấy {len(csv_files)} file CSV hợp lệ trong ThatBai/{date_folder}")
    
#     csv_files = [f for f in os.listdir(failed_folder_path) if f.lower().endswith('.csv')]
#     print(f"📂 Tìm thấy {len(csv_files)} file CSV trong {failed_folder_path}")
    
#     moved_files = []
    
#     for csv_file in csv_files:
#         file_path = os.path.join(failed_folder_path, csv_file)
#         print(f"\n📄 Đang xử lý file: {csv_file}")
        
#         try:
#             with open(file_path, mode='r', encoding='utf-8') as file:
#                 reader = csv.reader(file)
#                 try:
#                     first_row = next(reader)
#                     if len(first_row) <= 20:
#                         print("❌ Lỗi: File không đủ số cột")
#                         continue
                        
#                     room_charge = int(first_row[20])  # Cột U (index 20)
                    
#                     if room_charge != 21:
#                         print(f"⚠️⚠️ Tìm thấy Room Charge {room_charge} - Cần xử lý lại.⚠️⚠️")
                        
#                         # Xử lý trùng tên file
#                         dest_path = Path(target_folder_path) / csv_file
#                         counter = 1
#                         while dest_path.exists():
#                             base, ext = os.path.splitext(csv_file)
#                             new_name = f"{base}_{counter}{ext}"
#                             dest_path = Path(target_folder_path) / new_name
#                             counter += 1
                        
#                         shutil.copy2(file_path, dest_path)
#                         moved_files.append(str(dest_path))
#                         print(f"✅ Đã sao chép tới: {dest_path}")
#                     else:
#                         print("✔️ Room charge là 21 - Good!")
                        
#                 except StopIteration:
#                     print("❌ Lỗi: File rỗng")
#                 except ValueError:
#                     print("❌ Lỗi: Giá trị room charge không hợp lệ")
                    
#         except Exception as e:
#             print(f"❌ Lỗi khi xử lý file: {str(e)}")
    
#     return moved_files

# def main_loop():
#     # Tự động xác định thư mục Symphony (từ thư mục chứa script)
#     script_dir = Path(__file__).parent
#     symphony_root = script_dir / "Symphony"
    
#     print("🟢 Bắt đầu chương trình chạy tự động.")
#     print(f"📁 Đang quét thư mục Symphony tại: {symphony_root}")
#     print("⏳ Chạy tự động mỗi 5 phút...")
    
#     while True:
#         try:
#             current_time = datetime.now()
#             current_date = current_time.strftime('%d-%m-%Y')
            
#             print(f"\n⏰ Bắt đầu chu kỳ kiểm tra lúc {current_time.strftime('%H:%M:%S')}")
            
#             # Quét tất cả các outlet (101, 102,...)
#             outlets = [d for d in symphony_root.iterdir() if d.is_dir() and d.name.isdigit()]
            
#             if not outlets:
#                 print("❌ Không tìm thấy thư mục outlet nào (101, 102,...)")
#             else:
#                 total_moved = 0
                
#                 for outlet in outlets:
#                     outlet_name = outlet.name
#                     print(f"\n🏬 Đang xử lý outlet {outlet_name}")
                    
#                     failed_folder = outlet / f"{outlet_name}-cash" / "ThatBai" / current_date
#                     target_folder = outlet / f"{outlet_name}-cash"
                    
#                     if not failed_folder.exists():
#                         print(f"ℹ️ Không có thư mục ThatBai/{current_date}")
#                         continue
                        
#                     moved_files = process_failed_folder(str(failed_folder), str(target_folder))
#                     total_moved += len(moved_files)
                    
#                     if moved_files:
#                         print(f"📤 Đã di chuyển {len(moved_files)} file từ outlet {outlet_name}")
            
#             print(f"\n✅ Đã xử lý xong. Tổng cộng di chuyển {total_moved} file")
#             print("⌛ Chờ 5 phút trước khi chạy lại...")
#             time.sleep(300)  # Chờ 5 phút
            
#         except KeyboardInterrupt:
#             print("\n🛑 Dừng chương trình theo yêu cầu")
#             break
#         except Exception as e: # Nếu có lỗi gì tự xảy ra, chương trình tự khời động lại sau 1 phút.
#             print(f"❌ Lỗi nghiêm trọng: {str(e)}")
#             print("🔄 Khởi động lại sau 1 phút...")
#             time.sleep(60)

# if __name__ == "__main__":
#     main_loop()
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
        symphony_root = self.base_dir / "Symphony"
        if not symphony_root.exists():
            self.log_message("❌ Không tìm thấy thư mục Symphony", 'error')
            self.log_message(f"⚠️ Vui lòng đặt file exe cùng cấp với thư mục Symphony", 'warning')
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
    # Boolean to check if should switch to the new folder 
    # def should_switch_to_new_date(current_processing_date):
    #     """Check if it's time to switch to new date folder (after 2:00 AM)"""
    #     now = datetime.now()
        
    #     # Only switch dates between 2:00 AM and 2:05 AM to avoid multiple switches
    #     if now.hour == 2 and now.minute < 5:
    #         new_date = now.strftime('%d-%m-%Y')
    #         if new_date != current_processing_date:
    #             return True
    #     return False
    # # 
    # def get_target_date(self):
    #     now = datetime.now()
    #     return (now + timedelta(days=1)).date() if now.hour >= 2 else now.date()
    
    def main_loop(self):
        if not self.running:
            return
            
        try:
            current_time = datetime.now()
            current_date = current_time.strftime('%d-%m-%Y')
            
            
            self.log_message(f"\n⏰ Start scanning on {current_time.strftime('%H:%M:%S')}", 'info')
            self.status_var.set(f"🔍 Scanning date: {current_date}...")
            
            # Tự động xác định thư mục Symphony
            script_dir = Path(__file__).parent
            symphony_root = script_dir / "Symphony"
            symphony_root1 = Path(os.getcwd())/ "Symphony"
            print(symphony_root)
            print(symphony_root1)

           
            
            if not symphony_root.exists():
                try: 
                    symphony_root = symphony_root1
                    if not symphony_root.exists():
                        self.log_message("❌ Still Can not found Symphony folder")
                        self.log_message("❌ Still Can not found Symphony folder XX", 'error')
                        self.after_id = self.root.after(300000, self.main_loop)  # Thử lại sau 5 phút
                        return
                except Exception as e:
                       self.log_message("❌ Still Can not found Symphony folder")
                self.log_message("❌ Can not found Symphony folder, try to put AutoScan.exe same level with Symphony", 'error')
                self.after_id = self.root.after(300000, self.main_loop)  # Thử lại sau 5 phút
                return
                
            # Quét tất cả các outlet (101, 102,...)
            outlets = [d for d in symphony_root.iterdir() if d.is_dir() and d.name.isdigit()]
            
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
