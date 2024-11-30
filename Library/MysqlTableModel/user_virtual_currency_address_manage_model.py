# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserVirtualCurrencyAddressManage(Base):
    __tablename__ = 'user_virtual_currency_address_manage'
    __table_args__ = (
        Index('idx_time', 'last_withdraw_time', 'created_time'),
        Index('idx_user_account_status', 'current_binding_user_account', 'black_status', 'binding_status'),
        {'comment': '会员虚拟币账号管理'}
    )

    id = Column(BIGINT(20), primary_key=True)
    virtual_currency_address = Column(String(100, 'utf8mb4_0900_bin'), unique=True, comment='虚拟币账号地址')
    virtual_currency_address_alias = Column(String(50, 'utf8mb4_0900_bin'), comment='虚拟币账号地址-别名')
    virtual_currency_type = Column(String(10, 'utf8mb4_0900_bin'), comment='虚拟币种类')
    virtual_currency_protocol = Column(String(10, 'utf8mb4_0900_bin'), comment='虚拟币协议')
    black_status = Column(INTEGER(11), comment='黑名单状态 0禁用 1启用')
    binding_status = Column(INTEGER(11), comment='绑定状态 0未绑定 1绑定中')
    risk_control_level_id = Column(BIGINT(20), comment='风控层级id')
    binding_account_times = Column(INTEGER(11), comment='绑定账号数量')
    current_binding_user_id = Column(BIGINT(20), comment='当前绑定会员id')
    current_binding_user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='当前绑定会员账号')
    user_withdraw_success_times = Column(INTEGER(11), comment='会员提款成功次数')
    user_withdraw_fail_times = Column(INTEGER(11), comment='会员提款失败次数')
    user_withdraw_sum_amount = Column(DECIMAL(20, 2), comment='会员提款总金额')
    agent_withdraw_success_times = Column(INTEGER(11), comment='代理提款成功次数')
    agent_withdraw_fail_times = Column(INTEGER(11), comment='代理提款失败次数')
    agent_withdraw_sum_amount = Column(DECIMAL(20, 2), comment='代理提款总金额')
    first_use_time = Column(BIGINT(20), comment='虚拟币账号新增时间')
    last_withdraw_time = Column(BIGINT(20), comment='最近提款时间')
    last_operator = Column(String(30, 'utf8mb4_0900_bin'))
    creator = Column(BIGINT(20))
    updater = Column(BIGINT(20))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    site_code = Column(String(50, 'utf8mb4_0900_bin'))
