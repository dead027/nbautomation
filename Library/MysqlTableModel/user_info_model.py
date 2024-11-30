# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserInfo(Base):
    __tablename__ = 'user_info'
    __table_args__ = (
        Index('account_sitecode_index', 'user_account', 'site_code', unique=True),
        Index('super_agent_id_combine', 'super_agent_id', 'register_time', 'first_deposit_time'),
        {'comment': '用户信息表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='会员id')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='会员账号')
    nick_name = Column(String(50), comment='昵称')
    password = Column(String(50, 'utf8mb4_0900_bin'), comment='密码')
    salt = Column(String(15, 'utf8mb4_0900_bin'), comment='加密盐')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='姓名')
    gender = Column(INTEGER(11), comment='性别')
    birthday = Column(String(50, 'utf8mb4_0900_bin'), comment='出生日期')
    area_code = Column(String(20), comment='区号')
    phone = Column(String(20, 'utf8mb4_0900_bin'), unique=True, comment='手机号码')
    email = Column(String(50, 'utf8mb4_0900_bin'), comment='邮箱')
    mail_status = Column(INTEGER(2), server_default=text("'0'"), comment='邮箱验证状态 0 未验证  1已验证')
    phone_status = Column(INTEGER(2), server_default=text("'0'"), comment='手机验证状态 0 未验证  1已验证')
    main_currency = Column(String(10, 'utf8mb4_0900_bin'), comment='主货币')
    account_type = Column(String(5, 'utf8mb4_0900_bin'), index=True, comment='账号类型 1-测试 2-正式')
    account_status = Column(String(20, 'utf8mb4_0900_bin'), comment='账号状态')
    risk_level_id = Column(BIGINT(20), comment='风控层级id')
    first_deposit_time = Column(BIGINT(20), comment='首存时间')
    first_deposit_amount = Column(DECIMAL(20, 2), comment='首存金额')
    second_deposit_time = Column(BIGINT(20), comment='次存时间')
    second_deposit_amount = Column(DECIMAL(10, 2), comment='次存金额')
    last_login_time = Column(BIGINT(20), comment='最后登录时间')
    last_login_ip = Column(String(50, 'utf8mb4_0900_bin'), comment='最后登录ip')
    offline_days = Column(INTEGER(11), comment='离线天数')
    register_time = Column(BIGINT(20), comment='注册时间')
    member_domain = Column(String(100, 'utf8mb4_0900_bin'), comment='注册域名')
    register_ip = Column(String(15, 'utf8mb4_0900_bin'), index=True, comment='注册ip')
    registry = Column(INTEGER(11), comment='注册端;0-后台,1-PC,2-IOS_H5,3-IOS_APP,4-Android_H5,5-Andriod_APP')
    super_agent_id = Column(BIGINT(20), comment='上级代理id')
    super_agent_account = Column(String(30, 'utf8mb4_0900_bin'), index=True, comment='上级代理账号')
    binding_agent_time = Column(BIGINT(20), comment='绑定代理的时间')
    user_label_id = Column(String(1000), comment='会员标签id')
    trans_agent_time = Column(INTEGER(11), server_default=text("'0'"), comment='转代次数')
    vip_grade_code = Column(INTEGER(11), comment='vip当前等级')
    vip_grade_up = Column(INTEGER(11), comment='vip升级后的等级')
    vip_rank = Column(TINYINT(4), server_default=text("'0'"), comment='vip段位')
    withdraw_pwd = Column(String(50, 'utf8mb4_0900_bin'), comment='取款密码')
    acount_remark = Column(String(400, 'utf8mb4_0900_bin'), comment=' 账号备注')
    avatar_code = Column(String(200, 'utf8mb4_0900_bin'), comment='用户头像code')
    device_no = Column(String(100, 'utf8mb4_0900_bin'), comment='设备号')
    device_control_id = Column(BIGINT(20), comment='设备风控层级id')
    last_device_no = Column(String(100, 'utf8mb4_0900_bin'), comment='最后登录的设备号')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    wallet_address = Column(String(100, 'utf8mb4_0900_bin'), comment='充值热钱包地址')
    change_agent_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='代理归属修改次数')
    friend_invite_code = Column(String(11, 'utf8mb4_0900_bin'), comment='邀请码')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, index=True, comment='站点code')
    inviter = Column(String(50), comment='邀请人')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
