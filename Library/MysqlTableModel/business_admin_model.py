# coding: utf-8
from sqlalchemy import CHAR, Column, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BusinessAdmin(Base):
    __tablename__ = 'business_admin'
    __table_args__ = (
        Index('idx_uk_name_code', 'site_code', 'user_name', unique=True),
        {'comment': '职员信息'}
    )

    id = Column(BIGINT(30), primary_key=True)
    business_system = Column(String(20, 'utf8mb4_0900_bin'), comment='业务系统（ADMIN_CENTER总台 SITE站点）')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='站点CODE')
    user_name = Column(String(30, 'utf8mb4_0900_bin'), comment='用户名')
    nick_name = Column(String(30, 'utf8mb4_0900_bin'), comment='姓名')
    password = Column(String(64, 'utf8mb4_0900_bin'), comment='密码')
    google_auth_key = Column(String(50, 'utf8mb4_0900_bin'), comment='google验证--key')
    status = Column(TINYINT(4), server_default=text("'0'"), comment='状态（0禁用 1启用）')
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
    creator = Column(String(64, 'utf8mb4_0900_bin'))
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注信息')
    user_id = Column(BIGINT(10), unique=True, comment='管理员ID')
    is_set_google = Column(TINYINT(2), server_default=text("'0'"), comment='是否重置了google   1 是  0 否')
