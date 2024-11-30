# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteTaskConfig(Base):
    __tablename__ = 'site_task_config'
    __table_args__ = {'comment': '任务配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    task_name_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='任务名称-多语言')
    task_type = Column(String(20, 'utf8mb4_0900_bin'), comment='任务类型')
    sub_task_type = Column(String(20, 'utf8mb4_0900_bin'), comment='子任务类型')
    min_bet_amount = Column(DECIMAL(10, 2), comment='最小配置金额')
    reward_amount = Column(DECIMAL(10, 2), comment='彩金奖励')
    currency_code = Column(String(10, 'utf8mb4_0900_bin'), comment='币种')
    wash_ratio = Column(DECIMAL(10, 2), comment='洗码倍率')
    venue_type = Column(INTEGER(11), comment='场馆类型:1:体育 2:视讯 3:棋牌 4:电子')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏场馆CODE')
    task_picture_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='移动端任务图标')
    task_picture_pc_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='PC任务图标')
    task_desc_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='任务说明,多语言')
    sort = Column(INTEGER(11), comment='顺序')
    status = Column(INTEGER(11), comment='状态 0已禁用 1开启中')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
