# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentTransferRecord(Base):
    __tablename__ = 'agent_transfer_record'
    __table_args__ = {'comment': '代理转账记录表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    agent_id = Column(String(10, 'utf8mb4_0900_bin'), comment='代理编号')
    order_no = Column(String(30, 'utf8mb4_0900_bin'), comment='订单号')
    agent_account = Column(String(30, 'utf8mb4_0900_bin'), comment='代理账号')
    transfer_type = Column(CHAR(2, 'utf8mb4_0900_ai_ci'), comment='转账类型(1:佣金转账,2:额度转账)')
    transfer_amount = Column(DECIMAL(20, 2), comment='转账金额')
    transfer_agent_id = Column(INTEGER(20), comment='转账账号id')
    transfer_account = Column(String(30, 'utf8mb4_0900_bin'), comment='转账账号')
    transfer_time = Column(BIGINT(20), comment='转账时间')
    report_day = Column(BIGINT(20), server_default=text("'0'"), comment='佣金日期，只针对佣金转账有效')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    transfer_status = Column(INTEGER(11), comment='转账状态(0:成功,1:失败)')
    creator = Column(String(32, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(32, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')
