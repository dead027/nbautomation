# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityFreeGameRecord(Base):
    __tablename__ = 'site_activity_free_game_record'
    __table_args__ = {'comment': '游戏免费旋转领取记录'}

    id = Column(String(36), primary_key=True)
    user_id = Column(String(255), comment='会员id')
    user_account = Column(String(255), comment='会员账号')
    order_no = Column(String(255), comment='获取来源订单号 唯一值 做防重处理')
    order_time = Column(BIGINT(20), comment='订单时间')
    activity_id = Column(BIGINT(36), comment='活动id')
    activity_no = Column(String(255), comment='活动编号')
    activity_template = Column(String(255), comment='活动模板')
    activity_template_name = Column(String(255), comment='获取来源|活动名称')
    before_num = Column(String(255), comment='原次数')
    acquire_num = Column(INTEGER(11), comment='赠送次数')
    after_num = Column(String(255), comment='变更后次数')
    type = Column(INTEGER(10), comment='旋转次数变化类型 0:用户使用 1:活动赠送')
    currency_code = Column(String(255), comment='币种')
    venue_code = Column(String(64), comment='平台编号')
    creator = Column(String(255), comment='创建者')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(255), comment='更新者')
    updated_time = Column(BIGINT(20), comment='更新时间')
    site_code = Column(String(255), comment='站点编码')
    remark = Column(String(255), comment='备注')
    ip = Column(String(80, 'utf8mb4_0900_bin'), comment='发放时用户-ip')
