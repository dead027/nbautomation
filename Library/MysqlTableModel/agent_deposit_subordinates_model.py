# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentDepositSubordinate(Base):
    __tablename__ = 'agent_deposit_subordinates'
    __table_args__ = {'comment': '代理代存记录'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    agent_id = Column(BIGINT(20), index=True, comment='代理ID')
    agent_account = Column(String(100, 'utf8mb4_0900_bin'), index=True, comment='代理账号')
    agent_name = Column(String(100, 'utf8mb4_0900_bin'), comment='代理名称')
    parent_id = Column(BIGINT(20), comment='代理ID父节点')
    path = Column(String(500, 'utf8mb4_0900_bin'), comment='层次id逗号分隔')
    level = Column(INTEGER(11), server_default=text("'1'"), comment='层级')
    deposit_subordinates_type = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='代存类型（1 佣金代存 2额度代存）')
    user_account = Column(String(50, 'utf8mb4_0900_bin'), index=True, comment='代存会员账号')
    user_name = Column(String(100, 'utf8mb4_0900_bin'), comment='会员名称')
    amount = Column(DECIMAL(10, 2), comment='代存金额')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), comment='订单号')
    deposit_time = Column(BIGINT(20), index=True, comment='代存时间')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建日期')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改日期')
    running_water_multiple = Column(DECIMAL(8, 2), comment='流水倍数')
