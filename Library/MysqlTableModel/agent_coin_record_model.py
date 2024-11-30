# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCoinRecord(Base):
    __tablename__ = 'agent_coin_record'
    __table_args__ = {'comment': '代理账变记录'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    agent_account = Column(String(15, 'utf8mb4_0900_bin'), comment='代理账号')
    currency = Column(String(50, 'utf8mb4_0900_bin'), comment='币种')
    agent_name = Column(String(50, 'utf8mb4_0900_bin'), comment='代理名称')
    parent_id = Column(BIGINT(20), comment='代理ID父节点')
    path = Column(String(500, 'utf8mb4_general_ci'), comment='层次id逗号分隔')
    level = Column(INTEGER(11), server_default=text("'1'"), comment='层级')
    account_status = Column(String(10, 'utf8mb4_0900_bin'), comment='账号状态')
    risk_control_level_id = Column(BIGINT(20), comment='风控层级ID')
    risk_control_level = Column(String(255, 'utf8mb4_0900_bin'), comment='风控级别')
    wallet_type = Column(CHAR(1), index=True, comment='钱包类型 (1佣金钱包 2额度钱包）')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), index=True, comment='关联订单号')
    business_coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), index=True, comment='账变业务类型 ')
    coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), index=True, comment='账变类型')
    customer_coin_type = Column(CHAR(2, 'utf8mb4_0900_bin'), index=True, comment='客户端账变类型')
    balance_type = Column(CHAR(1, 'utf8mb4_0900_bin'), index=True, comment='收支类型1收入,2支出 3冻结 4 解冻')
    coin_from = Column(DECIMAL(20, 2), comment='账变前金额')
    coin_to = Column(DECIMAL(20, 2), comment='账变后金额')
    coin_amount = Column(DECIMAL(20, 2), comment='账变金额')
    creator = Column(String(32, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updater = Column(String(32, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注信息')
