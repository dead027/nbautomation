# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentInfo(Base):
    __tablename__ = 'agent_info'
    __table_args__ = {'comment': '代理基本信息'}

    id = Column(String(50, 'utf8mb4_0900_bin'), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    agent_id = Column(String(10), comment='代理编号')
    agent_account = Column(String(15, 'utf8mb4_0900_bin'), unique=True, comment='代理账号')
    name = Column(String(50, 'utf8mb4_0900_bin'), comment='代理姓名')
    gender = Column(String(5, 'utf8mb4_0900_bin'), comment='性别')
    birthday = Column(BIGINT(20), comment='出生日期')
    phone = Column(String(20, 'utf8mb4_0900_bin'), comment='手机号码')
    email = Column(String(100, 'utf8mb4_0900_bin'), comment='邮箱')
    qq = Column(String(30, 'utf8mb4_0900_bin'), comment='QQ')
    telegram = Column(String(30, 'utf8mb4_0900_bin'), comment='telegram')
    avatar_code = Column(String(30, 'utf8mb4_0900_bin'), comment='代理头像code')
    language = Column(String(30, 'utf8mb4_0900_bin'), server_default=text("'en-US'"), comment='当前语言')
    parent_id = Column(String(10), comment='父节点 存父节点agent_id')
    path = Column(String(200, 'utf8mb4_0900_bin'), comment='层次id 逗号分隔')
    level = Column(INTEGER(11), comment='代理层级')
    max_level = Column(INTEGER(11), comment='代理线层级上限')
    salt = Column(String(15, 'utf8mb4_0900_bin'), comment='加密盐')
    agent_password = Column(String(50, 'utf8mb4_0900_bin'), comment='登录密码')
    pay_password = Column(String(50, 'utf8mb4_0900_bin'), comment='支付密码')
    google_auth_key = Column(String(50, 'utf8mb4_0900_bin'), comment='google验证密钥')
    first_deposit_time = Column(BIGINT(20), comment='首存时间')
    first_deposit_amount = Column(DECIMAL(20, 2), comment='首存金额')
    agent_type = Column(INTEGER(11), comment='代理类型 1正式 2商务 3置换')
    contract_model_commission = Column(INTEGER(11), comment='代理契约模式-佣金契约 1是 0否')
    contract_model_rebate = Column(INTEGER(11), comment='代理契约模式-返点契约 1是 0否')
    status = Column(String(10, 'utf8mb4_0900_bin'), comment='账号状态 1正常 2登录锁定 3充提锁定(状态多选,用逗号分开)')
    contract_status = Column(INTEGER(11), comment='契约状态 1已签约 0未签约')
    entrance_perm = Column(INTEGER(11), comment='入口权限 1开启 0关闭')
    force_contract_effect = Column(INTEGER(11), comment='强制编辑契约生效 1开启 0关闭')
    remove_recharge_limit = Column(INTEGER(11), comment='解除充值限制 1被限制 0解除')
    register_way = Column(INTEGER(11), comment='注册方式 1手动 2自动')
    register_device_type = Column(INTEGER(11), comment='注册端')
    register_time = Column(BIGINT(20), comment='注册时间')
    register_ip = Column(String(64, 'utf8mb4_0900_bin'), comment='注册ip')
    last_login_time = Column(BIGINT(20), comment='最后登录时间')
    offline_days = Column(INTEGER(11), comment='离线天数')
    invite_code = Column(String(10, 'utf8mb4_0900_bin'), comment='合营代码')
    agent_label_id = Column(String(255), comment='代理标签id')
    risk_level_id = Column(BIGINT(20), comment='风控层级id')
    is_agent_arrears = Column(INTEGER(11), comment='是否有欠款  该代理对下级代理是否存在欠款 1有欠款 0无欠款')
    wallet_address = Column(String(100, 'utf8mb4_0900_bin'), comment='充值热钱包地址')
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注信息')
    short_url = Column(String(500, 'utf8mb4_0900_bin'), index=True, comment='短码链接')
    security_set = Column(INTEGER(11), server_default=text("'0'"), comment='是否设置密保问题 1设置 0未设置')
    super_remark = Column(String(500, 'utf8mb4_0900_bin'), comment='上级备注')
    home_button_entrance = Column(String(3000, 'utf8mb4_0900_bin'), comment='代理客户端 首页功能入口 PC端')
    home_button_entrance_h5 = Column(String(3000, 'utf8mb4_0900_bin'), comment='代理客户端 首页功能入口 H5端')
    agent_attribution = Column(INTEGER(11), comment='代理归属 1推广 2招商 3官资')
    agent_category = Column(INTEGER(11), comment='代理类别 1常规代理 2流量代理')
    agent_white_list = Column(String(255, 'utf8mb4_0900_bin'), comment='IP白名单(只有流量代理需要)，使用英文逗号隔开')
    aes_secret_key = Column(String(100, 'utf8mb4_0900_bin'), comment='AES密钥(只有流量代理需要)，Base64编码的字符串')
    plan_code = Column(String(64), comment='方案代码')
    user_benefit = Column(String(255), comment='会员福利 多个中间逗号分隔')
    creator = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    updater = Column(String(50, 'utf8mb4_0900_bin'), comment='修改人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')