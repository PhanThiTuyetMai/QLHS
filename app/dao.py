import hashlib
from app.models import HocSinh, Khoi, Thamso, User, Lop, MonHoc, HocKy, Diem
from app import db, app


def load_student():
    return HocSinh.query.all()


def load_student_page(page=None):
    students = HocSinh.query
    page = int(page)
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return students.slice(start, start + page_size).all()


def load_lop():
    return Lop.query.all()


def load_thamso():
    return Thamso.query.all()


def load_khoi():
    return Khoi.query.all()


def load_mh():
    return MonHoc.query.all()


def load_hk():
    return HocKy.query.all()


def count_hocsinh():
    return HocSinh.query.count()


def count_monhoc():
    return MonHoc.query.count()


def add_hs(hoten, gioitinh, ngaysinh, diachi, email, sdt, malop):
    s1 = HocSinh(hoten=hoten, gioitinh=gioitinh, ngaysinh=ngaysinh, diachi=diachi, email=email, sdt=sdt, malop=malop)
    db.session.add(s1)
    db.session.commit()


def add_khoi(tenkhoi, solop):
    k1 = Khoi(tenkhoi=tenkhoi, solop=solop)
    db.session.add(k1)
    db.session.commit()


def add_lop(tenlop, makhoi, siso):
    l1 = Lop(tenlop=tenlop, makhoi=makhoi, siso=siso)
    db.session.add(l1)
    db.session.commit()


def add_nam(namhoc=None):
    s1 = HocKy(tenhk="1", namhoc=namhoc)
    db.session.add(s1)
    s2 = HocKy(tenhk="2", namhoc=namhoc)
    db.session.add(s2)
    db.session.commit()


def load_lop_tenlop(kw=None):
    lops = Lop.query
    lops = lops.filter(Lop.tenlop.__eq__(kw))
    return lops.all()


def load_lop_malop(malop=None):
    lops = Lop.query
    lops = lops.filter(Lop.malop.__eq__(malop))
    return lops.all()


def load_hs_lop(malop=None):
    students = HocSinh.query
    students = students.filter(HocSinh.malop.__eq__(malop))
    return students.all()


def load_hs_mahs(mahs=None):
    students = HocSinh.query
    students = students.filter(HocSinh.mahs.__eq__(mahs))
    return students.all()


def load_mahk(hkn=None):
    h = HocKy.query
    h = h.filter(HocKy.tenhk.__eq__(hkn))
    return h.all()


def load_namhoc_hk(namhoc=None):
    hk = HocKy.query
    hk = hk.filter(HocKy.namhoc.__eq__(namhoc))
    return hk.all()


def load_mamh(tenmon=None):
    mon = MonHoc.query
    mon = mon.filter(MonHoc.tenmh.__eq__(tenmon))
    return mon.all()


def load_mahs_diem(mahs=None):
    diem = Diem.query
    diem = diem.filter(Diem.mahs.__eq__(mahs))
    return diem.all()


def add_diem(diem, mamh, malop, mahs, maloai, mahk):
    d1 = Diem(diem=diem, mamh=mamh, malop=malop, mahs=mahs, maloai=maloai, mahk=mahk)
    db.session.add(d1)
    db.session.commit()


def add_mon(tenmh=None, soluongdiem15p=None, soluongdiem45p=None):
    d1 = MonHoc(tenmh=tenmh, soluongdiem15p=soluongdiem15p, soluongdiem45p=soluongdiem45p)
    db.session.add(d1)
    db.session.commit()


def add_user(name, username, password, user_role, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(),
                password=password, user_role=user_role, email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
