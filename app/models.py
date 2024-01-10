from sqlalchemy import Column, Integer, String, Enum, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    GV = 2
    NV = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.NV)

    def __str__(self):
        return self.name


class Thamso(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tuoitoithieu = Column(Integer)
    tuoitoida = Column(Integer)
    soloptoithieu = Column(Integer)
    sisotoida = Column(Integer)
    toida15p = Column(Integer)
    toida45p = Column(Integer)
    toidathi = Column(Integer, default=1)


class Khoi(db.Model):
    __tablename__ = 'Khoi'

    makhoi = Column(Integer, primary_key=True, autoincrement=True)
    tenkhoi = Column(Integer, unique=True)
    solop = Column(String(10))
    lop = relationship('Lop', backref='khoi', lazy=True)

    def __str__(self):
        return self.tenkhoi


class Lop(db.Model):
    malop = Column(Integer, primary_key=True, autoincrement=True)
    tenlop = Column(String(50), unique=True)
    makhoi = Column(Integer, ForeignKey(Khoi.makhoi), nullable=False)
    siso = Column(Integer)
    hocsinh = relationship('HocSinh', backref='lop', lazy=True)

    def __str__(self):
        return self.tenlop


class HocSinh(db.Model):
    mahs = Column(Integer, primary_key=True, autoincrement=True)
    hoten = Column(String(50), nullable=False)
    gioitinh = Column(String(10))
    ngaysinh = Column(String(50))
    diachi = Column(String(50), nullable=False)
    sdt = Column(String(20))
    email = Column(String(50), unique=True)
    malop = Column(Integer, ForeignKey(Lop.malop), nullable=False)

    def __str__(self):
        return self.hoten


class HocKy(db.Model):
    mahk = Column(Integer, primary_key=True, autoincrement=True)
    tenhk = Column(String(50), nullable=False)
    namhoc = Column(String(50), nullable=False)


class MonHoc(db.Model):
    mamh = Column(Integer, primary_key=True, autoincrement=True)
    tenmh = Column(String(50), nullable=False)
    soluongdiem15p = Column(Integer, nullable=False)
    soluongdiem45p = Column(Integer, nullable=False)


class LoaiDiem(db.Model):
    maloai = Column(Integer, primary_key=True, autoincrement=True)
    tenloai = Column(String(50), nullable=False)


class Diem(db.Model):
    madiem = Column(Integer, primary_key=True, autoincrement=True)
    diem = Column(Float, nullable=False)
    mamh = Column(Integer, ForeignKey(MonHoc.mamh), nullable=False)
    malop = Column(Integer, ForeignKey(Lop.malop), nullable=False)
    mahs = Column(Integer, ForeignKey(HocSinh.mahs), nullable=False)
    maloai = Column(Integer, ForeignKey(LoaiDiem.maloai), nullable=False)
    mahk = Column(Integer, ForeignKey(HocKy.mahk), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
