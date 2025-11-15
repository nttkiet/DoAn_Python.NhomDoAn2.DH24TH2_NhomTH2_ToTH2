-- Tạo database
CREATE DATABASE qlnhansu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE qlnhansu;

-- Bảng phòng ban
CREATE TABLE phong_ban (
  mapb INT AUTO_INCREMENT PRIMARY KEY,
  tenpb VARCHAR(100) NOT NULL UNIQUE,
  mo_ta VARCHAR(255)
);

-- Bảng chức vụ
CREATE TABLE chuc_vu (
  macv INT AUTO_INCREMENT PRIMARY KEY,
  tencv ENUM('Quản lý','Trưởng phòng','Nhân viên') NOT NULL UNIQUE
);

-- Bảng nhân viên
CREATE TABLE nhan_vien (
  manv INT PRIMARY KEY,
  holot VARCHAR(100) NOT NULL,
  ten VARCHAR(50) NOT NULL,
  phai ENUM('Nam','Nữ') NOT NULL,
  ngaysinh DATE NOT NULL,
  macv INT NOT NULL,
  mapb INT NOT NULL,
  ghi_chu VARCHAR(255),
  CONSTRAINT fk_nv_cv FOREIGN KEY (macv) REFERENCES chuc_vu(macv),
  CONSTRAINT fk_nv_pb FOREIGN KEY (mapb) REFERENCES phong_ban(mapb)
);

-- Bảng người dùng (đăng nhập)
CREATE TABLE nguoi_dung (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,   -- lưu trực tiếp mật khẩu (đơn giản)
  manv INT NOT NULL,
  trang_thai ENUM('ACTIVE','LOCKED') DEFAULT 'ACTIVE',
  CONSTRAINT fk_nd_nv FOREIGN KEY (manv) REFERENCES nhan_vien(manv)
    ON DELETE CASCADE
);



-- ===========================
-- Dữ liệu mẫu
-- ===========================

-- Phòng ban
INSERT INTO phong_ban (tenpb, mo_ta) VALUES
('Phòng Hành chính', 'Quản lý hành chính tổng hợp'),
('Phòng Kế toán', 'Xử lý tài chính và kế toán'),
('Phòng Nhân sự', 'Quản lý nhân sự và tuyển dụng'),
('Phòng IT', 'Hỗ trợ kỹ thuật và phát triển phần mềm');

-- Chức vụ
INSERT INTO chuc_vu (tencv) VALUES
('Quản lý'),
('Trưởng phòng'),
('Nhân viên');

-- Nhân viên mẫu
INSERT INTO nhan_vien (manv, holot, ten, phai, ngaysinh, macv, mapb)
VALUES
-- Admin mặc định (sẽ bị ẩn trong giao diện)
(000,'Nguyễn Văn','Admin','Nam','1980-01-01',
 (SELECT macv FROM chuc_vu WHERE tencv='Quản lý'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng Hành chính')),

-- Trưởng phòng
(1001,'Trần Thị','Lan','Nữ','1990-05-20',
 (SELECT macv FROM chuc_vu WHERE tencv='Trưởng phòng'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng Kế toán')),

(1002,'Lê Văn','Hùng','Nam','1988-03-15',
 (SELECT macv FROM chuc_vu WHERE tencv='Trưởng phòng'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng IT')),

-- Nhân viên
(2001,'Phạm Văn','Bình','Nam','1995-07-15',
 (SELECT macv FROM chuc_vu WHERE tencv='Nhân viên'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng Kế toán')),

(2002,'Nguyễn Thị','Mai','Nữ','1996-08-22',
 (SELECT macv FROM chuc_vu WHERE tencv='Nhân viên'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng IT')),

(2003,'Hoàng Văn','Tú','Nam','1992-11-30',
 (SELECT macv FROM chuc_vu WHERE tencv='Nhân viên'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng Nhân sự')),

(2004,'Đặng Thị','Hạnh','Nữ','1993-04-10',
 (SELECT macv FROM chuc_vu WHERE tencv='Nhân viên'),
 (SELECT mapb FROM phong_ban WHERE tenpb='Phòng Hành chính'));

-- Người dùng mẫu
INSERT INTO nguoi_dung (username, password, manv)
VALUES
('admin', '123456', 000),  -- mặc định admin
('tp_ketoan', 'tp123', 1001),
('tp_it', 'tp456', 1002),
('nv_binh', 'nv123', 2001),
('nv_mai', 'nv456', 2002),
('nv_tu', 'nv789', 2003),
('nv_hanh', 'nv321', 2004);



