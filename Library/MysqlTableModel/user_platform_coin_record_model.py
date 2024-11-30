# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserPlatformCoinRecord(Base):
    __tablename__ = 'user_platform_coin_record'
    __table_args__ = (
        Index('idx_coin_type', 'business_coin_type', 'coin_type', 'customer_coin_type', 'balance_type'),
        Index('idx_order_no', 'order_no', 'balance_type'),
        {'comment': '用户平台币账变记录表'}
    )

    id = Column(BIGINT(20), primary_key=True)
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    user_id = Column(BIGINT(20), comment='会员ID')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='用户名称')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), index=True, comment='会员账号')
    account_status = Column(String(10, 'utf8mb4_0900_bin'), comment='账号状态')
    user_label_id = Column(String(1000, 'utf8mb4_0900_bin'), comment='会员标签IDS')
    account_status_name = Column(String(50, 'utf8mb4_0900_bin'), comment='账号状态名称')
    risk_control_level_id = Column(BIGINT(20), comment='风控层级ID')
    vip_rank = Column(INTEGER(11), comment='vip等级')
    vip_grade_code = Column(INTEGER(11), comment='vip段位')
    agent_id = Column(BIGINT(20), comment='代理ID')
    agent_name = Column(String(100, 'utf8mb4_0900_bin'), comment='代理名称')
    currency = Column(String(50, 'utf8mb4_0900_bin'), comment='币种')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), comment='关联订单号')
    business_coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), comment='账变业务类型 ')
    coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), comment='账变类型 ')
    customer_coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), comment='客户端账变类型')
    balance_type = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='收支类型1收入,2支出 3冻结 4 解冻')
    coin_value = Column(DECIMAL(20, 2), comment='账变金额')
    coin_from = Column(DECIMAL(20, 2), comment='账变前金额')
    coin_to = Column(DECIMAL(20, 2), comment='账变后金额')
    coin_amount = Column(DECIMAL(20, 2), comment='当前金额')
    remark = Column(String(500, 'utf8mb4_0900_bin'), comment='备注')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
