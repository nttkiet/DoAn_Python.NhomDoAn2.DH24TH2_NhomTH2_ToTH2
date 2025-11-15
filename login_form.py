# login_form.py - Form đăng nhập hệ thống
import tkinter as tk
from tkinter import messagebox
from db import connect_db
from employee_ui import open_employee_ui
from utils import center_window


def login_ui():
    root = tk.Tk()
    root.title("Đăng nhập hệ thống")
    center_window(root, 500, 500)
    root.resizable(False, False)
    # ===== Tiêu đề =====
    lbl_title = tk.Label(root, text="QUẢN LÝ NHÂN SỰ", font=("Segoe UI", 25, "bold"))
    lbl_title.pack(pady=15)

    # ===== Khung đăng nhập =====
    frame_login = tk.Frame(root, bd=3, relief="groove", padx=20, pady=20)
    frame_login.pack(pady=50)

    tk.Label(frame_login, text="Username", font=("Segoe UI", 13)).grid(row=0, column=0, pady=10, sticky="w")
    entry_user = tk.Entry(frame_login, font=("Segoe UI", 12), width=25)
    entry_user.grid(row=0, column=1, pady=10)

    tk.Label(frame_login, text="Password", font=("Segoe UI", 13)).grid(row=1, column=0, pady=10, sticky="w")
    entry_pass = tk.Entry(frame_login, show="*", font=("Segoe UI", 12), width=25)
    entry_pass.grid(row=1, column=1, pady=10)



    def check_login():
        if entry_user.get() == "" or entry_pass.get() == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT nv.manv, cv.tencv, pb.tenpb
            FROM nguoi_dung nd
            JOIN nhan_vien nv ON nd.manv = nv.manv
            JOIN chuc_vu cv ON nv.macv = cv.macv
            JOIN phong_ban pb ON nv.mapb = pb.mapb
            WHERE nd.username=%s AND nd.password=%s AND nd.trang_thai='ACTIVE'
        """, (entry_user.get(), entry_pass.get()))
        user = cur.fetchone()
        conn.close()

        if user:
            manv, chucvu, phongban = user
            root.destroy()

            open_employee_ui(chucvu, phongban)
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")
                # ===== Nút chức năng =====
    btn_login = tk.Button(frame_login, text="Đăng nhập", font=("Segoe UI", 13, "bold"),
                          width=15, command=check_login)
    btn_login.grid(row=2, column=0, columnspan=2, pady=15)

    btn_exit = tk.Button(frame_login, text="Thoát", font=("Segoe UI", 13),
                         width=15, command=root.quit)
    btn_exit.grid(row=3, column=0, columnspan=2, pady=17)

    root.mainloop()
