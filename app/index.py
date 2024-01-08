import datetime
import math

from flask import request, redirect, render_template
from app import app, dao, login, db
import cloudinary.uploader
from flask_login import login_user, logout_user
from app.models import UserRole
from app.models import HocSinh, Thamso, MonHoc


@app.route('/')
def home():
    return render_template('index.html', UserRole=UserRole)


@app.route('/hocsinh')
def student():
    # hocsinh = dao.load_student()
    lop = dao.load_lop()
    page = request.args.get('page', 1)

    students = dao.load_student_page(page)
    sl = dao.count_hocsinh()

    return render_template('hocsinh.html', students=students, UserRole=UserRole, lop=lop,
                           pages=math.ceil(sl / app.config['PAGE_SIZE']))


@app.route('/lop', methods=['get', 'post'])
def lop():
    n = 0
    e = 0
    err_msg = ''
    khoi = dao.load_khoi()
    lop = dao.load_lop()
    thamso = dao.load_thamso()
    if request.method.__eq__('POST'):
        makhoi = request.form.get('c_khoi')
        tenlop = request.form.get('lop')
        siso = request.form.get('siso')
        try:
            if int(makhoi).__eq__(10):
                makhoi = 1
            elif int(makhoi).__eq__(11):
                makhoi = 2
            else:
                makhoi = 3

            for c in lop:
                if int(c.makhoi).__eq__(int(makhoi)):
                    n = n + 1

            for c in khoi:
                if int(c.makhoi).__eq__(int(makhoi)):
                    if int(n).__eq__(int(c.solop)):
                        e = e + 1
                        err_msg = 'Khối đã đủ lớp. Vui lòng tạo lớp cho khối khác !!!'

            if e != 1:
                for c in thamso:
                    if int(siso).__lt__(int(c.sisotoida)):
                        dao.add_lop(tenlop=tenlop, makhoi=makhoi, siso=siso)
                        err_msg = 'Đã tạo lớp thành công !!!'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('lop.html', khoi=khoi, UserRole=UserRole, err_msg=err_msg)


@app.route('/khoi', methods=['get', 'post'])
def khoi():
    err_msg = ''
    thamso = dao.load_thamso()
    if request.method.__eq__('POST'):
        tenkhoi = request.form.get('tenkhoi')
        solop = request.form.get('solop')
        try:
            for c in thamso:
                if int(solop).__lt__(int(c.soloptoithieu)):
                    solop = 1
                dao.add_khoi(tenkhoi=tenkhoi, solop=solop)
                err_msg = 'Đã tạo thành công'
        except Exception as ex:
            err_msg = 'He thong dang co loi ' + str(ex)

    return render_template('khoi.html', thamso=thamso, UserRole=UserRole, err_msg=err_msg)


@app.route('/tiep_nhan_hs', methods=['get', 'post'])
def tiepnhan():
    err_msg = ''
    khoi = dao.load_khoi()
    lop = dao.load_lop()
    hocsinh = dao.load_student()
    thamso = dao.load_thamso()
    if request.method.__eq__('POST'):
        hoten = request.form.get('hoten')
        gioitinh = request.form.get('gioitinh')
        email = request.form.get('email')
        diachi = request.form.get('diachi')
        ngaysinh = request.form.get('ngaysinh')
        sdt = request.form.get('sdt')
        malop = request.form.get('ml')
        lopkhac = request.form.get('lopkhac')
        if lopkhac is not None and lopkhac != '':
            for c in dao.load_lop_malop(lopkhac):
                malop = c.malop
        m = int((datetime.datetime.today()).year) - int(ngaysinh[6:10])
        try:
            for c in thamso:
                if int(m).__ge__(int(c.tuoitoithieu)):
                    if int(m).__le__(int(c.tuoitoida)):
                        dao.add_hs(hoten=hoten, gioitinh=gioitinh, email=email,
                                   diachi=diachi, sdt=sdt, ngaysinh=ngaysinh, malop=malop)
                        err_msg = "Đã thêm thành công"
                else:
                    err_msg = "Vui Lòng Xem Lại Tuổi Học Sinh !!!"
        except Exception as ex:
            err_msg = 'He thong dang co loi ' + str(ex)

    return render_template('TN_hocsinh.html', khoi=khoi, lop=lop, hocsinh=hocsinh, UserRole=UserRole,
                           err_msg=err_msg)


@app.route('/danhsachlop', methods=['get', 'post'])
def dslop():
    kw = request.form.get('kw')
    lop = dao.load_lop()
    lops = dao.load_lop_tenlop(kw)
    mlop = 0
    for c in lops:
        mlop = c.malop
    students = dao.load_hs_lop(mlop)
    return render_template('danhsachlop.html', lop=lop, lops=lops, students=students, UserRole=UserRole)


@app.route('/nhapdiem', methods=['get', 'post'])
def nhapdiem():
    err_msg = ''
    manghk = []
    hk1 = []
    global mn, mahs, ml, ky1
    lop = dao.load_lop()

    hk = dao.load_hk()
    for c in hk:
        if int(c.mahk) <= 2:
            hk1.append(c.mahk)

    dsmonh = dao.load_mh()
    kw = request.form.get('tenlop')
    lops = dao.load_lop_tenlop(kw)

    ml1 = request.form.get('ml1')
    students = dao.load_hs_lop(ml1)

    tenmon = request.form.get('tenmon')
    namhoc = request.form.get('namhoc')

    hkn = request.form.get('hkn')
    hks = dao.load_mahk(hkn)
    for c in hks:
        if str(c.namhoc).__eq__(str(namhoc)):
            manghk.append(c.mahk)

    mamon = dao.load_mamh(tenmon)
    mm = request.form.get('ma_m')
    ky = request.form.get('hk')

    if request.method.__eq__('POST'):
        mang = []
        mangm = []
        manghs = []

        for i in range(0, dao.count_hocsinh() + 1):
            ma_hs = request.form.get(str('ma_') + str(i + 1))

            d15_1 = request.form.get(str('15_1_' + str(i + 1)))

            d15_2 = request.form.get(str('15_2_' + str(i + 1)))

            d15_3 = request.form.get(str('15_3_' + str(i + 1)))

            d15_4 = request.form.get(str('15_4_' + str(i + 1)))

            d15_5 = request.form.get(str('15_5_' + str(i + 1)))

            d45_1 = request.form.get(str('45_1_' + str(i + 1)))

            d45_2 = request.form.get(str('45_2_' + str(i + 1)))

            d45_3 = request.form.get(str('45_3_' + str(i + 1)))

            dthi = request.form.get(str('thi_' + str(i + 1)))

            dao.add_thu(i)

            if d15_1 == '' and d15_2 == '' and d15_3 == '' and d15_4 == '' and d15_5 == '' and d45_1 == '' and d45_2 == '' and d45_3 == '' and dthi == '':
                pass
            else:
                mang.append([d15_1, d15_2, d15_3, d15_4, d15_5, d45_1, d45_2, d45_3, dthi])
                manghs.append(ma_hs)

        if mm is not None and ml1 is not None and ky is not None:
            mangm.append(mm)
            mangm.append(ml1)
            mangm.append(ky)

        try:
            for i in range(0, dao.count_hocsinh()):
                for j in range(0, 9):
                    if j == 0:
                        for c in range(0, len(mangm)):
                            if c == 0:
                                mn = mangm[0]
                            elif c == 1:
                                ml = mangm[1]
                            else:
                                ky1 = mangm[2]

                    if mang[i][j] is None or mang[i][j] == '':
                        pass
                    else:
                        if j < 5:
                            h = 1
                        elif 5 <= j < 8:
                            h = 2
                        else:
                            h = 3
                        dao.add_diem(mang[i][j], mn, ml, manghs[i], h, ky1)
                        err_msg = 'Đã nhập điểm thành công !!!'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('Nhap_diem.html', lop=lop, hk=hk, dsmonh=dsmonh,
                           UserRole=UserRole, err_msg=err_msg, lops=lops, manghk=manghk,
                           mamon=mamon, students=students, hk1=hk1)


@app.route('/taomonhoc', methods=['get', 'post'])
def tao_monhoc():
    err_msg = ''
    n = 0
    thamso = dao.load_thamso()
    mon = dao.load_mh()
    sl15p = request.form.get('15p')
    sl45p = request.form.get('45p')
    tenmon = request.form.get('mon')

    for c in mon:
        if str(c.tenmh).__eq__(str(tenmon)):
            err_msg = 'Môn này đã được tạo'

    if str(err_msg) == "Môn này đã được tạo":
        n = 1

    if sl45p and sl45p and n != 1:
        try:
            for d in thamso:
                if int(sl15p) < int(d.toida15p) and int(sl45p) < int(d.toida45p):
                    dao.add_mon(tenmon, sl15p, sl45p)
                    err_msg = 'Tạo môn thành công'
                else:
                    err_msg = 'Vui lòng xem lại số lượng bài kiểm tra'
        except Exception as ex:
            err_msg = 'He thong dang co loi ' + str(ex)

    return render_template('tao_mon.html', lop=lop, UserRole=UserRole, err_msg=err_msg)


@app.route('/monhoc', methods=['get', 'post'])
def monhoc():
    mon = dao.load_mh()
    return render_template('monhoc.html', mon=mon, UserRole=UserRole)


@app.route('/xoamonhoc', methods=['get', 'post'])
def xoamon():
    err_msg = ''
    mon = dao.load_mh()
    tenmh = request.form.get('tenmon')
    found_mh = MonHoc.query.filter_by(tenmh=tenmh).first()
    if request.method.__eq__('POST'):
        tenxoa = request.form.get('tenxoa')
        if tenxoa:
            try:
                MonHoc.query.filter_by(tenmh=tenxoa).delete()
                db.session.commit()
                err_msg = 'Đã xóa môn thành công'
            except Exception as ex:
                err_msg = 'Hệ thống đang có lỗi ' + str(ex)
    return render_template('xoa_mon.html', UserRole=UserRole, mon=mon, found_mh=found_mh, err_msg=err_msg)


@app.route('/suamonhoc', methods=['get', 'post'])
def suamon():
    err_msg = ''
    mon = dao.load_mh()
    tenmh = request.form.get('tenmon')
    found_mh = MonHoc.query.filter_by(tenmh=tenmh).first()
    if request.method.__eq__('POST'):
        tenmon_cn = request.form.get('tenmon_cn')
        sl15p_cn = request.form.get('15p_cn')
        sl45p_cn = request.form.get('45p_cn')
        if tenmon_cn and sl15p_cn and sl45p_cn:
            try:
                mon_cn = MonHoc.query.filter_by(tenmh=tenmon_cn).first()
                mon_cn.soluongdiem15p = sl15p_cn
                mon_cn.soluongdiem45p = sl45p_cn
                db.session.commit()
                err_msg = 'Đã cập nhật môn thành công'
            except Exception as ex:
                err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('sua_mon.html', mon=mon, err_msg=err_msg, found_mh=found_mh, UserRole=UserRole)


@app.route('/timkiemmon', methods=['get', 'post'])
def timmon():
    mon = dao.load_mh()
    tenmh = request.form.get('tenmon')
    found_mh = MonHoc.query.filter_by(tenmh=tenmh).first()
    return render_template('tim_mh.html', UserRole=UserRole, found_mh=found_mh, mon=mon)


@app.route('/bangdiem_mon', methods=['get', 'post'])
# bổ sung thêm năm học vào đây
def bangdiem_mon():
    a = 0
    lop = dao.load_lop()
    mon1 = dao.load_mh()
    tenlop = request.form.get('tenlop')
    tenmon = request.form.get('tenmon')
    lop1 = dao.load_lop_tenlop(tenlop)
    for c in lop1:
        a = c.malop
    students = dao.load_hs_lop(a)
    mon = dao.load_mamh(tenmon)
    mangtk = []
    manghs = []
    dem15 = 0
    dem45 = 0

    for i in range(0, dao.count_hocsinh()):
        ma_hs = request.form.get(str('ma_') + str(i + 1))
        if ma_hs is not None:
            manghs.append(ma_hs)

    for c in mon:
        dem15 = c.soluongdiem15p
        dem45 = c.soluongdiem45p

    for c in range(0, len(manghs)):
        diem1 = dao.load_mahs_diem(manghs[c])
        if manghs[c] is not None:
            tong15_1 = 0
            tong45_1 = 0
            thi_1 = 0
            tong15_2 = 0
            tong45_2 = 0
            thi_2 = 0
            for d in mon:
                for f in diem1:
                    if f.mamh == d.mamh:
                        if f.mahk == 1:
                            if f.maloai == 1:
                                tong15_1 = tong15_1 + f.diem
                            if f.maloai == 2:
                                tong45_1 = tong45_1 + f.diem
                            if f.maloai == 3:
                                thi_1 = f.diem
                        if f.mahk == 2:
                            if f.maloai == 1:
                                tong15_2 = tong15_2 + f.diem
                            if f.maloai == 2:
                                tong45_2 = tong45_2 + f.diem
                            if f.maloai == 3:
                                thi_2 = f.diem

            hs = dao.load_hs_mahs(manghs[c])
            for a in hs:
                l = dao.load_lop_malop(a.malop)
                for c in l:
                    if tong15_1 >= 0 and tong45_1 >= 0 and thi_1 >= 0 and tong15_2 >= 0 and tong45_2 >= 0 and thi_2 >= 0:
                        diemtb_1 = (tong15_1 + tong45_1 * 2 + thi_1 * 3) / (dem15 + dem45 * 2 + 3)
                        diemtb_2 = (tong15_2 + tong45_2 * 2 + thi_2 * 3) / (dem15 + dem45 * 2 + 3)
                        if diemtb_1 >= 0:
                            if diemtb_2 >= 0:
                                mangtk.append([a.hoten, c.tenlop, round(diemtb_1, 2), round(diemtb_2, 2)])

    return render_template('bangdiem.html', lop=lop, students=students, mangtk=mangtk, mon1=mon1, mon=mon,
                           UserRole=UserRole)


@app.route('/tongket', methods=['get', 'post'])
def tongket():
    global diemtb_1, dem
    hk = []
    mangnam = []
    hocky = dao.load_hk()
    lop = dao.load_lop()
    m = dao.load_mh()

    for c in hocky:
        if int(c.mahk) <= 2:
            hk.append(c.mahk)

    for c in hocky:
        mangnam.append(str(c.namhoc))

    mangnam1 = set(mangnam)

    ky = request.form.get('hk')
    namhoc = request.form.get('namhoc')
    tenm = request.form.get('mh')
    mon1 = dao.load_mamh(tenm)
    ky1 = []
    tenhk = []
    tennh = []
    mangky = dao.load_namhoc_hk(namhoc)

    for c in mangky:
        if int(c.tenhk) == int(ky):
            ky1.append(c.mahk)
            tenhk.append(c.tenhk)
            tennh.append(c.namhoc)

    hk1 = request.form.get('ky1')

    mangtenlop = []
    mangtile = []
    mangtk = []
    dem15 = 0
    dem45 = 0

    for c in mon1:
        dem15 = c.soluongdiem15p
        dem45 = c.soluongdiem45p

    for c in lop:
        students = dao.load_hs_lop(c.malop)
        siso = 0
        dem = 0
        for d in students:
            siso = siso + 1
            tong15_1 = 0
            tong45_1 = 0
            thi_1 = 0
            tong15_2 = 0
            tong45_2 = 0
            thi_2 = 0
            diem1 = dao.load_mahs_diem(d.mahs)
            dao.add_thu(hk1)
            for e in mon1:
                for f in diem1:
                    if f.mamh == e.mamh:
                        if str(f.mahk) == hk1:
                            if f.maloai == 1:
                                tong15_1 = tong15_1 + f.diem
                            if f.maloai == 2:
                                tong45_1 = tong45_1 + f.diem
                            if f.maloai == 3:
                                thi_1 = f.diem

                if tong15_1 >= 0 and tong45_1 >= 0 and thi_1 >= 0 and tong15_2 >= 0 and tong45_2 >= 0 and thi_2 >= 0:
                    diemtb_1 = (tong15_1 + tong45_1 * 2 + thi_1 * 3) / (dem15 + dem45 * 2 + 3)

                if diemtb_1 >= 5:
                    dem = dem + 1

        if siso != 0:
            mangtenlop.append(c.tenlop)
            mangtile.append(round((dem / siso) * 100, 2))
            mangtk.append([c.tenlop, siso, dem, round((dem / siso) * 100, 2)])

    return render_template('tk_mh.html', hk=hk, lop=lop, m=m, UserRole=UserRole, mangnam1=mangnam1,
                           ky1=ky1, mangtk=mangtk, mangtenlop=mangtenlop,
                           mangtile=mangtile, mon1=mon1, tenhk=tenhk, tennh=tennh)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        chucvu = request.form.get('cv')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                if chucvu == 'NV':
                    user_role = 'NV'
                if chucvu == 'GV':
                    user_role = 'GV'
                if chucvu == 'ADMIN':
                    user_role = "ADMIN"
                dao.add_user(name=name, username=username, password=password, user_role=user_role, email=email,
                             avatar=avatar_path)
                return redirect('/signin')
            else:
                err_msg = "Mat khau khong khop!!!!"
        except Exception as ex:
            err_msg = 'He thong dang co loi ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/signin', methods=['get', 'post'])
def user_sigin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect('/')
        else:
            err_msg = 'Username hoặc password KHÔNG chính xác !!!!'

    return render_template('login.html', err_msg=err_msg)


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/signout')
def user_signout():
    logout_user()
    return redirect('/signin')


@app.route('/sualop', methods=['get', 'post'])
def sua_lop():
    err_msg = ''
    lop = dao.load_lop()
    mahs = request.form.get('mahs')
    hs = dao.load_hs_mahs(mahs)
    if request.method.__eq__('POST'):
        ma_hs = request.form.get('mahs1')
        lopsua = request.form.get('lopsua')
        found_hs = HocSinh.query.filter_by(mahs=ma_hs).first()
        try:
            for c in lop:
                if str(c.tenlop).__eq__(str(lopsua)):
                    dao.add_thu(c.malop)
                    found_hs.malop = int(c.malop)
                    db.session.commit()
                    err_msg = 'Đã sửa lớp thành công'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('sua_lop.html', UserRole=UserRole, hs=hs, lop=lop, err_msg=err_msg)


@app.route('/suadk')
def sua_dk():
    thamso = dao.load_thamso()

    return render_template('sua_dk.html', thamso=thamso, UserRole=UserRole)


@app.route('/suatuoi', methods=['get', 'post'])
def sua_tuoi():
    err_msg = ''
    if request.method.__eq__('POST'):
        tuoitt = request.form.get('tuoitt')
        tuoitd = request.form.get('tuoitd')
        dieukien = Thamso.query.filter_by(id=1).first()
        try:
            dieukien.tuoitoithieu = int(tuoitt)
            dieukien.tuoitoida = int(tuoitd)
            db.session.commit()
            err_msg = 'Đã sửa điều kiện thành công'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('sua_tuoi.html', UserRole=UserRole, err_msg=err_msg)


@app.route('/suasiso', methods=['get', 'post'])
def sua_siso():
    err_msg = ''
    if request.method.__eq__('POST'):
        siso = request.form.get('siso')
        dieukien = Thamso.query.filter_by(id=1).first()
        try:
            dieukien.sisotoida = int(siso)
            db.session.commit()
            err_msg = 'Đã sửa điều kiện thành công'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi ' + str(ex)

    return render_template('sua_siso.html', UserRole=UserRole, err_msg=err_msg)


@app.route('/bangdiem_nam', methods=['get', 'post'])
def bangdiem_nam():
    a = 0
    mangnam = []
    manghs = []
    mangtk = []

    lop = dao.load_lop()
    hk = dao.load_hk()
    mon = dao.load_mh()

    for c in hk:
        mangnam.append(c.namhoc)

    mangnam1 = set(mangnam)

    tenlop = request.form.get('tenlop')
    namhoc = request.form.get('namhoc')
    lop1 = dao.load_lop_tenlop(tenlop)

    for c in lop1:
        a = c.malop

    students = dao.load_hs_lop(a)

    manghk = dao.load_namhoc_hk(namhoc)

    for i in range(0, dao.count_hocsinh()):
        ma_hs = request.form.get(str('ma_') + str(i + 1))
        if ma_hs is not None:
            manghs.append(ma_hs)

    for c in range(0, len(manghs)):
        diem1 = dao.load_mahs_diem(manghs[c])
        if manghs[c] is not None:
            tong_2 = 0
            tong_1 = 0
            for d in mon:
                tong15_1 = 0
                tong45_1 = 0
                thi_1 = 0
                tong15_2 = 0
                tong45_2 = 0
                thi_2 = 0
                for h in manghk:
                    for f in diem1:
                        if f.mamh == d.mamh:
                            if f.mahk == h.mahk and int(h.tenhk) == 1:
                                if f.maloai == 1:
                                    tong15_1 = tong15_1 + f.diem
                                if f.maloai == 2:
                                    tong45_1 = tong45_1 + f.diem
                                if f.maloai == 3:
                                    thi_1 = f.diem

                            if f.mahk == h.mahk and int(h.tenhk) == 2:
                                if f.maloai == 1:
                                    tong15_2 = tong15_2 + f.diem
                                if f.maloai == 2:
                                    tong45_2 = tong45_2 + f.diem
                                if f.maloai == 3:
                                    thi_2 = f.diem

                tong_1 = tong_1 + (
                        (tong15_1 + tong45_1 * 2 + thi_1 * 3)
                        / (int(d.soluongdiem15p) + int(d.soluongdiem45p) * 2 + 3))

                tong_2 = tong_2 + (
                        (tong15_2 + tong45_2 * 2 + thi_2 * 3)
                        / (int(d.soluongdiem15p) + int(d.soluongdiem45p) * 2 + 3))

            hs = dao.load_hs_mahs(manghs[c])
            for a in hs:
                l = dao.load_lop_malop(a.malop)
                for c in l:
                    mangtk.append([a.hoten, c.tenlop, round(tong_1 / int(dao.count_monhoc()), 2),
                                   round(tong_2 / int(dao.count_monhoc()), 2)])

    return render_template('bangdiem_nam.html', lop=lop, students=students, hk=hk, mon=mon,
                           UserRole=UserRole, mangtk=mangtk, mangnam1=mangnam1)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
