from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from app.models import Thamso, UserRole, MonHoc
from flask_login import current_user
from flask import redirect


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', index_view=MyAdmin())


admin = Admin(app=app, name="QUẢN TRỊ HỌC SINH", template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class StatsView(BaseView):
    @expose("/")
    def index(self):
        return redirect("/tongket")


class MonHocView(BaseView):
    @expose("/")
    def index(self):
        return redirect("/monhoc")


class QuyDinhView(BaseView):
    @expose("/")
    def index(self):
        return redirect("/suadk")


class NamHoc(BaseView):
    @expose("/")
    def index(self):
        return redirect("/namhoc")


class DangXuat(BaseView):
    @expose("/")
    def index(self):
        return redirect("/signout")


admin.add_view(MonHocView(name='Môn Học'))
admin.add_view(QuyDinhView(name='Quy Định'))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(NamHoc(name='Năm Học'))
admin.add_view(DangXuat(name='Đăng Xuất'))
