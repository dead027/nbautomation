# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteMedalInfo(Base):
    __tablename__ = 'site_medal_info'
    __table_args__ = {'comment': '站点勋章信息表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码 -1代表总站默认值')
    parent_id = Column(BIGINT(20), comment='上级勋章id')
    medal_code = Column(String(128, 'utf8mb4_0900_bin'), comment='勋章代码')
    medal_name = Column(String(128, 'utf8mb4_0900_bin'), comment='勋章名称')
    unlock_cond_name = Column(String(255, 'utf8mb4_0900_bin'), comment='解锁条件名称')
    reward_amount = Column(DECIMAL(20, 4), comment='奖励金额')
    typing_multiple = Column(DECIMAL(20, 4), comment='打码倍数')
    cond_num1 = Column(String(16, 'utf8mb4_0900_bin'), comment='达成条件1 N')
    cond_num2 = Column(String(16, 'utf8mb4_0900_bin'), comment='达成条件2 N')
    medal_desc = Column(Text(collation='utf8mb4_0900_bin'), comment='解锁条件说明')
    activated_pic = Column(String(255, 'utf8mb4_0900_bin'), comment='激活图片')
    inactivated_pic = Column(String(255, 'utf8mb4_0900_bin'), comment='未激活图片')
    medal_name_i18 = Column(String(128, 'utf8mb4_0900_bin'), comment='勋章名称多语言')
    medal_desc_i18 = Column(String(128, 'utf8mb4_0900_bin'), comment='勋章描述多语言')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')
