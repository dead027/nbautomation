# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemWithdrawChannel(Base):
    __tablename__ = 'system_withdraw_channel'
    __table_args__ = {'comment': '提款通道配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    channel_type = Column(String(64, 'utf8mb4_0900_bin'), comment='通道类型')
    withdraw_way_id = Column(BIGINT(20), comment='提款方式ID')
    withdraw_way = Column(String(64, 'utf8mb4_0900_bin'), comment='提款方式')
    channel_code = Column(String(64, 'utf8mb4_0900_bin'), comment='通道代码')
    channel_name = Column(String(128, 'utf8mb4_0900_bin'), comment='通道名称')
    mer_no = Column(String(128, 'utf8mb4_0900_bin'), comment='商户号')
    private_key = Column(String(512, 'utf8mb4_0900_bin'), comment='密钥')
    pub_key = Column(String(512, 'utf8mb4_0900_bin'), comment='公钥')
    sort_order = Column(INTEGER(11), server_default=text("'1'"), comment='排序')
    withdraw_min = Column(DECIMAL(16, 4), comment='提款最小值')
    withdraw_max = Column(DECIMAL(16, 4), comment='提款最大值')
    use_scope = Column(String(512, 'utf8mb4_0900_bin'), comment='使用范围')
    weight = Column(INTEGER(11), comment='同类型权重')
    auth_num = Column(INTEGER(11), comment='授权数量')
    memo = Column(String(128, 'utf8mb4_0900_bin'), comment='备注')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')
