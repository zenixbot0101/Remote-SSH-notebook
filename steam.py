import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import time
import pyautogui
import psutil
import shutil

# ====================== CẤU HÌNH ======================
STEAM_PATH = r"C:\Program Files (x86)\Steam\steam.exe"

class SteamAutoLogin:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.root = tk.Tk()
        self.root.title("Steam Auto Login Tool - Fixed 2")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

    def clear_temp(self):
        print("[+] Đang xóa temp...")
        temp_paths = [os.getenv('TEMP'), os.getenv('TMP'), r"C:\Windows\Temp"]
        for folder in temp_paths:
            if folder and os.path.exists(folder):
                try:
                    shutil.rmtree(folder, ignore_errors=True)
                    os.makedirs(folder, exist_ok=True)
                except:
                    pass

    def kill_steam(self):
        print("[+] Tắt Steam...")
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'steam' in proc.info['name'].lower():
                try:
                    proc.kill()
                except:
                    pass
        time.sleep(3)

    def start_steam(self):
        self.kill_steam()
        print("[+] Mở Steam...")
        subprocess.Popen(STEAM_PATH)
        time.sleep(7)  # Chờ lâu hơn

    def focus_steam(self):
        time.sleep(2)
        try:
            for win in pyautogui.getWindowsWithTitle("Steam"):
                if "Steam" in win.title:
                    win.activate()
                    win.maximize()
                    time.sleep(1.5)
                    return True
        except:
            pass
        return False

    def auto_login(self):
        print("[+] Đang auto login...")
        self.focus_steam()
        time.sleep(4)

        # === CÁCH MỚI - AN TOÀN HƠN ===
        screen_w, screen_h = pyautogui.size()

        # Click vào vùng ô Username (phía trên)
        pyautogui.moveTo(screen_w//2, screen_h//2 - 80, duration=1)
        pyautogui.click()
        time.sleep(1)

        # Xóa sạch ô username
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.press('delete')
        time.sleep(0.5)

        # Nhập Username
        pyautogui.typewrite(self.username, interval=0.08)
        print("[+] Đã nhập Username")
        time.sleep(1)

        # Chuyển sang ô Password
        pyautogui.press('tab')
        time.sleep(1)

        # Nhập Password
        pyautogui.typewrite(self.password, interval=0.08)
        print("[+] Đã nhập Password")
        time.sleep(1)

        # Nhấn Enter để login
        pyautogui.press('enter')
        print("[+] Đã nhấn Enter - Đang login...")

    def handle_login(self):
        if not self.username or not self.password:
            self.username = simpledialog.askstring("Username", "Nhập Steam Username:")
            self.password = simpledialog.askstring("Password", "Nhập Password:", show='*')

        confirm = messagebox.askyesno("Xác nhận", 
            f"Username: {self.username}\nPassword: {'*' * len(self.password)}\n\nThông tin đúng chưa?")
        
        if not confirm:
            self.username = self.password = ""
            return self.handle_login()

        if not os.path.exists(STEAM_PATH):
            messagebox.showerror("Lỗi", "Không tìm thấy Steam!")
            return

        self.clear_temp()
        self.start_steam()
        self.auto_login()

        messagebox.showinfo("Hoàn tất", 
            "Tool đã nhập Username + Password + Enter.\n\nNếu vẫn không login được (Error 50), bấm OK và thử lại.")

        retry = messagebox.askyesno("Thử lại?", "Muốn thử login lại không?")
        if retry:
            self.kill_steam()
            time.sleep(2)
            self.start_steam()
            self.auto_login()

    def main_menu(self):
        while True:
            choice = simpledialog.askstring("Steam Auto Login", 
                "1: Bắt đầu Auto Login\n\nNhập lựa chọn:", initialvalue="1")
            
            if choice == "1":
                self.handle_login()
            else:
                break


if __name__ == "__main__":
    print("🚀 Steam Auto Login Tool")
    app = SteamAutoLogin()
    app.main_menu()
