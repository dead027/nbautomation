# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentParamConfig(Base):
    __tablename__ = 'agent_param_config'
    __table_args__ = {'comment': '参数字典配置表'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    param_code = Column(String(50, 'utf8mb4_0900_bin'), comment='名称代码')
    param_name = Column(String(50, 'utf8mb4_0900_bin'), comment='名称')
    param_type = Column(INTEGER(11), comment='类型: 1=固定值、2=充值金额,3=有效投注')
    param_value = Column(String(50, 'utf8mb4_0900_bin'), comment='值')
    param_type_limit = Column(INTEGER(11), comment='类型限制:  1=固定值、2=充值金额,3=有效投注\\n')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    create_name = Column(String(64, 'utf8mb4_0900_bin'), comment='创建者的账号')
    update_name = Column(String(64, 'utf8mb4_0900_bin'), comment='修改者的账号')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建日期')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改日期')
    job_handler = Column(String(255, 'utf8mb4_0900_bin'), comment=' 关联定时任务')
