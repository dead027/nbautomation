# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityEventRecord(Base):
    __tablename__ = 'site_activity_event_record'
    __table_args__ = (
        Index('acativity_user_index', 'day', 'activity_template', 'user_id', 'code', unique=True),
        Index('idx_user_account', 'user_id', 'activity_id'),
        Index('index_01', 'site_code', 'day', 'activity_template', 'user_id'),
        {'comment': '会员活动参与记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    code = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='这个字段\\n主要是使 site_code+day+activity_template+user_id。\\n唯一索引生效。\\n但是针对转盘活动不需要这个约束,所以加多一个code字段,\\n在活动是转盘活动则存随机数,是其他活动则固定，使\\nsite_code+day+activity_template+user_id+code 唯一约束生效')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    activity_id = Column(BIGINT(20), comment='所属活动')
    day = Column(BIGINT(20), comment='参与当天的开始时间戳')
    calculate_type = Column(INTEGER(11), comment='结算周期,0:日结,1:周结,2:月结')
    status = Column(INTEGER(11), comment='发放状态,0=未发放，1=已发放')
    activity_template = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='会员id')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员账号')
    vip_rank = Column(INTEGER(11), comment='vip等级')
    device_no = Column(String(80, 'utf8mb4_0900_bin'), comment='用户-设备号')
    ip = Column(String(80, 'utf8mb4_0900_bin'), index=True, comment='用户-ip')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
