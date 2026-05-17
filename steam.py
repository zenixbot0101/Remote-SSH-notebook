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
ACCOUNT_FILE = "accounts.txt"

class SteamAutoLogin:
    def __init__(self):
        self.username = ""
        self.password = ""

        self.root = tk.Tk()
        self.root.withdraw()  # Ẩn cửa sổ chính

    # ====================== FILE ACCOUNT ======================

    def save_account(self):
        try:
            with open(ACCOUNT_FILE, "w", encoding="utf-8") as f:
                f.write(f"{self.username}:{self.password}")
            print("[+] Đã lưu tài khoản")
        except Exception as e:
            print("Lỗi lưu account:", e)

    def load_account(self):
        if os.path.exists(ACCOUNT_FILE):
            try:
                with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
                    data = f.read().strip()

                if ":" in data:
                    self.username, self.password = data.split(":", 1)

                    use_saved = messagebox.askyesno(
                        "Tài khoản đã lưu",
                        f"Dùng tài khoản đã lưu?\n\nUsername: {self.username}"
                    )

                    if use_saved:
                        return True

            except:
                pass

        return False

    # ====================== SYSTEM ======================

    def clear_temp(self):
        print("[+] Đang xóa temp...")

        temp_paths = [
            os.getenv('TEMP'),
            os.getenv('TMP'),
            r"C:\Windows\Temp"
        ]

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
            try:
                if proc.info['name'] and 'steam' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass

        time.sleep(3)

    def start_steam(self):
        self.kill_steam()

        print("[+] Mở Steam...")
        subprocess.Popen(STEAM_PATH)

        time.sleep(8)

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

    # ====================== AUTO LOGIN ======================

    def auto_login(self):
        print("[+] Đang auto login...")

        self.focus_steam()

        time.sleep(4)

        screen_w, screen_h = pyautogui.size()

        # Username
        pyautogui.moveTo(screen_w // 2, screen_h // 2 - 80, duration=1)
        pyautogui.click()

        time.sleep(1)

        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')

        time.sleep(0.5)

        pyautogui.typewrite(self.username, interval=0.05)

        print("[+] Đã nhập Username")

        time.sleep(1)

        # Password
        pyautogui.press('tab')

        time.sleep(1)

        pyautogui.typewrite(self.password, interval=0.05)

        print("[+] Đã nhập Password")

        time.sleep(1)

        # Login
        pyautogui.press('enter')

        print("[+] Đã nhấn Enter")

    # ====================== LOGIN FLOW ======================

    def ask_account(self):

        loaded = self.load_account()

        if not loaded:
            self.username = simpledialog.askstring(
                "Username",
                "Nhập Steam Username:"
            )

            self.password = simpledialog.askstring(
                "Password",
                "Nhập Password:",
                show='*'
            )

            if not self.username or not self.password:
                return False

            save = messagebox.askyesno(
                "Lưu tài khoản",
                "Muốn lưu tài khoản để lần sau không cần nhập lại?"
            )

            if save:
                self.save_account()

        confirm = messagebox.askyesno(
            "Xác nhận",
            f"Username: {self.username}\n"
            f"Password: {'*' * len(self.password)}\n\n"
            f"Thông tin đúng chưa?"
        )

        return confirm

    def retry_login(self):
        print("[+] Retry login...")

        self.kill_steam()

        time.sleep(2)

        self.start_steam()

        self.auto_login()

    def handle_login(self):

        if not os.path.exists(STEAM_PATH):
            messagebox.showerror("Lỗi", "Không tìm thấy Steam!")
            return

        ok = self.ask_account()

        if not ok:
            return

        self.clear_temp()

        self.start_steam()

        self.auto_login()

        while True:

            retry = messagebox.askyesno(
                "Steam Error 50?",
                "Nếu Steam bị Error 50 hoặc login lỗi:\n\n"
                "Bấm YES để tool tự restart Steam và login lại.\n\n"
                "Bấm NO nếu đã login thành công."
            )

            if retry:
                self.retry_login()
            else:
                break

        messagebox.showinfo("Hoàn tất", "Đã kết thúc tool.")

    # ====================== MENU ======================

    def main_menu(self):
        while True:

            choice = simpledialog.askstring(
                "Steam Auto Login",
                "1: Bắt đầu Auto Login\n"
                "2: Xóa account đã lưu\n"
                "0: Thoát\n\n"
                "Nhập lựa chọn:",
                initialvalue="1"
            )

            if choice == "1":
                self.handle_login()

            elif choice == "2":
                if os.path.exists(ACCOUNT_FILE):
                    os.remove(ACCOUNT_FILE)
                    messagebox.showinfo("OK", "Đã xóa account lưu.")
                else:
                    messagebox.showinfo("Thông báo", "Không có account lưu.")

            else:
                break


# ====================== START ======================

if __name__ == "__main__":

    print("🚀 Steam Auto Login Tool")

    app = SteamAutoLogin()

    app.main_menu()
