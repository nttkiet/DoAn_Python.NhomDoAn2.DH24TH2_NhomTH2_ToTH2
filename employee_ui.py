import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import connect_db
from utils import center_window

def open_employee_ui(chucvu, phongban, current_username=None):
    root = tk.Tk()
    root.title("Quản lý nhân sự")
    center_window(root, 1150, 720)

    # ====== Styles ======
    style = ttk.Style()
    style.configure("Treeview", rowheight=26, font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    # ====== Frame nhập thông tin ======
    frame_info = tk.Frame(root)
    frame_info.pack(pady=10, padx=20, fill="x")

    # Dòng 1: Mã số, Họ lót, Tên
    tk.Label(frame_info, text="Mã số", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_maso = tk.Entry(frame_info, font=("Arial", 12), width=15)
    entry_maso.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame_info, text="Họ lót", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
    entry_holot = tk.Entry(frame_info, font=("Arial", 12), width=25)
    entry_holot.grid(row=0, column=3, padx=10, pady=10)

    tk.Label(frame_info, text="Tên", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=10, sticky="w")
    entry_ten = tk.Entry(frame_info, font=("Arial", 12), width=15)
    entry_ten.grid(row=0, column=5, padx=10, pady=10)

    # Dòng 2: Phái, Ngày sinh
    tk.Label(frame_info, text="Phái", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    gender_var = tk.StringVar(value="Nam")
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam", font=("Arial", 11)).grid(row=1, column=1, padx=5, pady=10, sticky="w")
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ", font=("Arial", 11)).grid(row=1, column=1, padx=80, pady=10, sticky="w")

    tk.Label(frame_info, text="Ngày sinh", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10, sticky="w")
    date_entry = DateEntry(frame_info, font=("Arial", 12), width=15, date_pattern="yyyy-mm-dd")
    date_entry.grid(row=1, column=3, padx=10, pady=10)

    # Dòng 3: Chức vụ, Phòng ban
    tk.Label(frame_info, text="Chức vụ", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    cbb_chucvu = ttk.Combobox(frame_info, font=("Arial", 12), width=20, state="readonly")
    cbb_chucvu["values"] = ["Quản lý", "Trưởng phòng", "Nhân viên"]
    cbb_chucvu.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(frame_info, text="Phòng ban", font=("Arial", 12)).grid(row=2, column=2, padx=10, pady=10, sticky="w")
    cbb_phongban = ttk.Combobox(frame_info, font=("Arial", 12), width=25, state="readonly")
    cbb_phongban.grid(row=2, column=3, padx=10, pady=10)

    # Dòng 4: Username, Password
    tk.Label(frame_info, text="Username", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_username = tk.Entry(frame_info, font=("Arial", 12), width=20)
    entry_username.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(frame_info, text="Password", font=("Arial", 12)).grid(row=3, column=2, padx=10, pady=10, sticky="w")
    entry_password = tk.Entry(frame_info, font=("Arial", 12), show="*", width=20)
    entry_password.grid(row=3, column=3, padx=10, pady=10)

    # ====== Treeview ======
    columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu", "phongban")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    tree.heading("maso", text="Mã số");        tree.column("maso", width=90, anchor="center")
    tree.heading("holot", text="Họ lót");      tree.column("holot", width=180, anchor="w")
    tree.heading("ten", text="Tên");           tree.column("ten", width=100, anchor="w")
    tree.heading("phai", text="Phái");         tree.column("phai", width=80, anchor="center")
    tree.heading("ngaysinh", text="Ngày sinh"); tree.column("ngaysinh", width=120, anchor="center")
    tree.heading("chucvu", text="Chức vụ");    tree.column("chucvu", width=140, anchor="w")
    tree.heading("phongban", text="Phòng ban"); tree.column("phongban", width=180, anchor="w")
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ====== Functions ======
    def clear_input():
        entry_maso.delete(0, tk.END)
        entry_holot.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        gender_var.set("Nam")
        date_entry.set_date("2000-01-01")
        cbb_chucvu.set(""); cbb_phongban.set("")
        entry_username.config(state="normal")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db(); cur = conn.cursor()
        if chucvu == "Quản lý":
            cur.execute("""SELECT nv.manv,nv.holot,nv.ten,nv.phai,nv.ngaysinh,cv.tencv,pb.tenpb
                           FROM nhan_vien nv
                           JOIN chuc_vu cv ON nv.macv=cv.macv
                           JOIN phong_ban pb ON nv.mapb=pb.mapb
                           WHERE nv.manv <> '000'""")
        elif chucvu == "Trưởng phòng":
            cur.execute("""SELECT nv.manv,nv.holot,nv.ten,nv.phai,nv.ngaysinh,cv.tencv,pb.tenpb
                           FROM nhan_vien nv
                           JOIN chuc_vu cv ON nv.macv=cv.macv
                           JOIN phong_ban pb ON nv.mapb=pb.mapb
                           WHERE pb.tenpb=%s AND nv.manv <> '000'""",(phongban,) )
        else: 
            cur.execute("""SELECT nv.manv,nv.holot,nv.ten,nv.phai,nv.ngaysinh,cv.tencv,pb.tenpb
                           FROM nhan_vien nv
                           JOIN chuc_vu cv ON nv.macv=cv.macv
                           JOIN phong_ban pb ON nv.mapb=pb.mapb
                           WHERE nv.manv <> '000'""")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    def lam_moi():
        load_data()
        clear_input()
# chỉ trưởng phòng ban mới kiểm soát được nhân viên của chính mình
    def validate_head_department(phongban_nv):
        if chucvu == "Trưởng phòng" and phongban_nv != phongban:
            messagebox.showwarning("Phân quyền","Bạn chỉ được quản lý nhân viên thuộc phòng ban của mình.")
            return False
        return True

    def them_nv():
        if chucvu not in ("Quản lý", "Trưởng phòng"):
            messagebox.showwarning("Cảnh báo", "Nhân viên không có quyền thêm.")
            return

        maso = entry_maso.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        phai = gender_var.get().strip()
        ngaysinh = date_entry.get().strip()
        chucvu_nv = cbb_chucvu.get().strip()
        phongban_nv = cbb_phongban.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if "" in [maso, holot, ten, phai, ngaysinh, chucvu_nv, phongban_nv, username, password]:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin.")
            return
        if not validate_head_department(phongban_nv):
            return

        conn = connect_db(); cur = conn.cursor()
        cur.execute("SELECT macv FROM chuc_vu WHERE tencv=%s", (chucvu_nv,))
        macv_row = cur.fetchone()
        cur.execute("SELECT mapb FROM phong_ban WHERE tenpb=%s", (phongban_nv,))
        mapb_row = cur.fetchone()
        if not macv_row or not mapb_row:
            conn.close()
            messagebox.showerror("Lỗi dữ liệu", "Chức vụ hoặc phòng ban không hợp lệ.")
            return
        macv, mapb = macv_row[0], mapb_row[0]

        try:
            cur.execute("INSERT INTO nhan_vien (manv, holot, ten, phai, ngaysinh, macv, mapb) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (maso, holot, ten, phai, ngaysinh, macv, mapb))
            cur.execute("INSERT INTO nguoi_dung (username, password, manv) VALUES (%s,%s,%s)",
                        (username, password, maso))
            conn.commit()
            load_data(); clear_input()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def xoa_nv():
        if chucvu not in ("Quản lý", "Trưởng phòng"):
            messagebox.showwarning("Phân quyền", "Nhân viên không có quyền xóa.")
            return
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn nhân viên để xóa.")
            return
        values = tree.item(selected)["values"]
        maso, holot, ten, phai, ngaysinh, chucvu_nv, phongban_nv = values

        if not validate_head_department(phongban_nv):
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên mã {maso}?"):
            return

        conn = connect_db(); cur = conn.cursor()
        try:
            cur.execute("DELETE FROM nguoi_dung WHERE manv=%s", (maso,))
            cur.execute("DELETE FROM nhan_vien WHERE manv=%s", (maso,))
            conn.commit()
            load_data()
            messagebox.showinfo("Thành công", f"Đã xóa nhân viên mã {maso}.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()
    def sua_nv():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn nhân viên để sửa.")
            return
        values = tree.item(selected)["values"]
        maso, holot, ten, phai, ngaysinh, chucvu_nv, phongban_nv = values

        # Nhân viên chỉ được sửa chính mình
        if chucvu == "Nhân viên":
            conn = connect_db(); cur = conn.cursor()
            cur.execute("SELECT manv FROM nguoi_dung WHERE username=%s", (current_username,))
            my_manv = cur.fetchone()
            conn.close()
            if not my_manv or str(maso) != str(my_manv[0]):
                messagebox.showwarning("Phân quyền", "Bạn chỉ được sửa thông tin của chính mình.")
                return

        if chucvu == "Trưởng phòng" and phongban_nv != phongban:
            messagebox.showwarning("Phân quyền", "Bạn chỉ được sửa nhân viên thuộc phòng ban của mình.")
            return

        entry_maso.delete(0, tk.END); entry_maso.insert(0, maso)
        entry_holot.delete(0, tk.END); entry_holot.insert(0, holot)
        entry_ten.delete(0, tk.END); entry_ten.insert(0, ten)
        gender_var.set(phai)
        date_entry.set_date(ngaysinh)
        cbb_chucvu.set(chucvu_nv)
        cbb_phongban.set(phongban_nv)
        entry_username.config(state="disabled")
        entry_password.delete(0, tk.END)

    def luu_nv():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn một dòng để lưu thay đổi.")
            return

        maso = entry_maso.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        phai = gender_var.get().strip()
        ngaysinh = date_entry.get().strip()
        chucvu_nv = cbb_chucvu.get().strip()
        phongban_nv = cbb_phongban.get().strip()
        password = entry_password.get().strip()

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn lưu thay đổi cho nhân viên mã {maso}?"):
            return

        if chucvu == "Trưởng phòng" and not validate_head_department(phongban_nv):
            return
        if chucvu == "Nhân viên":
            conn_chk = connect_db(); cur_chk = conn_chk.cursor()
            cur_chk.execute("SELECT manv FROM nguoi_dung WHERE username=%s", (current_username,))
            my_manv = cur_chk.fetchone()
            conn_chk.close()
            if not my_manv or str(maso) != str(my_manv[0]):
                messagebox.showwarning("Phân quyền", "Bạn chỉ được lưu thông tin của chính mình.")
                return

        conn = connect_db(); cur = conn.cursor()
        cur.execute("SELECT macv FROM chuc_vu WHERE tencv=%s", (chucvu_nv,))
        macv_row = cur.fetchone()
        cur.execute("SELECT mapb FROM phong_ban WHERE tenpb=%s", (phongban_nv,))
        mapb_row = cur.fetchone()
        if not macv_row or not mapb_row:
            conn.close()
            messagebox.showerror("Lỗi dữ liệu", "Chức vụ hoặc phòng ban không hợp lệ.")
            return
        macv, mapb = macv_row[0], mapb_row[0]

        try:
            cur.execute("""UPDATE nhan_vien
                           SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, macv=%s, mapb=%s
                           WHERE manv=%s""", (holot, ten, phai, ngaysinh, macv, mapb, maso))
            if password != "":
                cur.execute("UPDATE nguoi_dung SET password=%s WHERE manv=%s", (password, maso))
            conn.commit()
            load_data(); clear_input()
            entry_username.config(state="normal")
            messagebox.showinfo("Thành công", f"Đã lưu thay đổi cho nhân viên mã {maso}.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def tim_nv():
        maso = entry_maso.get().strip()
        if maso == "":
            messagebox.showwarning("Thiếu dữ liệu", "Nhập mã nhân viên để tìm.")
            return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db(); cur = conn.cursor()
        if chucvu == "Trưởng phòng":
            cur.execute("""SELECT nv.manv,nv.holot,nv.ten,nv.phai,nv.ngaysinh,cv.tencv,pb.tenpb
                           FROM nhan_vien nv
                           JOIN chuc_vu cv ON nv.macv=cv.macv
                           JOIN phong_ban pb ON nv.mapb=pb.mapb
                           WHERE nv.manv=%s AND pb.tenpb=%s AND nv.manv <> '000'""",(maso, phongban))
        else:
            cur.execute("""SELECT nv.manv,nv.holot,nv.ten,nv.phai,nv.ngaysinh,cv.tencv,pb.tenpb
                           FROM nhan_vien nv
                           JOIN chuc_vu cv ON nv.macv=cv.macv
                           JOIN phong_ban pb ON nv.mapb=pb.mapb
                           WHERE nv.manv=%s AND nv.manv <> '000'""",(maso,))
        row = cur.fetchone()
        if row:
            tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy nhân viên.")
        conn.close()
    # ====== Frame nút ======
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=10)

    if chucvu == "Quản lý":
        ttk.Button(frame_btn, text="Thêm", width=12, command=them_nv).grid(row=0, column=0, padx=6)
        ttk.Button(frame_btn, text="Lưu", width=12, command=luu_nv).grid(row=0, column=1, padx=6)
        ttk.Button(frame_btn, text="Sửa", width=12, command=sua_nv).grid(row=0, column=2, padx=6)
        ttk.Button(frame_btn, text="Xóa", width=12, command=xoa_nv).grid(row=0, column=3, padx=6)
        ttk.Button(frame_btn, text="Hủy", width=12, command=clear_input).grid(row=0, column=4, padx=6)

    elif chucvu == "Trưởng phòng":
        ttk.Button(frame_btn, text="Thêm", width=12, command=them_nv).grid(row=0, column=0, padx=6)
        ttk.Button(frame_btn, text="Lưu", width=12, command=luu_nv).grid(row=0, column=1, padx=6)
        ttk.Button(frame_btn, text="Sửa", width=12, command=sua_nv).grid(row=0, column=2, padx=6)
        ttk.Button(frame_btn, text="Xóa", width=12, command=xoa_nv).grid(row=0, column=3, padx=6)
        ttk.Button(frame_btn, text="Hủy", width=12, command=clear_input).grid(row=0, column=4, padx=6)

    else:  # Nhân viên: chỉ được Sửa/Lưu chính mình
        ttk.Button(frame_btn, text="Sửa", width=12, command=sua_nv).grid(row=0, column=2, padx=6)
        ttk.Button(frame_btn, text="Lưu", width=12, command=luu_nv).grid(row=0, column=3, padx=6)

    # Nút Làm mới (chức vụ nào cũng có)
    ttk.Button(frame_btn, text="Làm mới", width=12, command=lam_moi).grid(row=0, column=5, padx=6)

    # Các nút chung
    ttk.Button(frame_btn, text="Tìm kiếm", width=12, command=tim_nv).grid(row=0, column=6, padx=6)
    ttk.Button(frame_btn, text="Thoát", width=12, command=root.quit).grid(row=0, column=7, padx=6)

    # ====== Khởi tạo ======
    if chucvu == "Trưởng phòng":
        cbb_phongban.set(phongban)
        cbb_phongban.config(state="disabled")

    load_data()
    root.mainloop()
