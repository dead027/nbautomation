# coding: utf-8
from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteAdmin(Base):
    __tablename__ = 'site_admin'
    __table_args__ = {'comment': '职员信息'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_id = Column(BIGINT(10), comment='管理员ID')
    user_name = Column(String(30, 'utf8mb4_0900_bin'), unique=True, comment='用户名')
    nick_name = Column(String(30, 'utf8mb4_0900_bin'), comment='姓名')
    password = Column(String(64, 'utf8mb4_0900_bin'), comment='密码')
    google_auth_key = Column(String(50, 'utf8mb4_0900_bin'), comment='google验证--key')
    status = Column(TINYINT(4), server_default=text("'0'"), comment='状态 0 正常 1 禁用')
    verify_code_type = Column(TINYINT(4), server_default=text("'1'"), comment='验证码类型: 1 谷歌')
    is_super_admin = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='是否超管')
    is_first_time = Column(INTEGER(11), server_default=text("'1'"), comment='1: 首次登入，只要成功登入之后，就改成 0')
    last_login_time = Column(BIGINT(20), comment='最后登入时间')
    last_login_ip = Column(String(21, 'utf8mb4_0900_bin'), comment='最后登入ip')
    phone = Column(String(100, 'utf8mb4_0900_bin'))
    lock_status = Column(TINYINT(4), server_default=text("'0'"), comment='0: 未锁定;  1: 已锁定')
    staff_no = Column(String(10, 'utf8mb4_0900_bin'), comment='员工编号')
    allow_ips = Column(String(300, 'utf8mb4_0900_bin'), comment='ip')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(BIGINT(20))
    updater = Column(BIGINT(20))
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注信息')
