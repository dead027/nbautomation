# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteUserFeedback(Base):
    __tablename__ = 'site_user_feedback'
    __table_args__ = {'comment': '会员意见建议反馈'}

    id = Column(BIGINT(30), primary_key=True)
    user_id = Column(String(30, 'utf8mb4_0900_bin'), nullable=False, comment='用户id')
    content = Column(String(500, 'utf8mb4_0900_bin'), nullable=False, comment='建议内容')
    pic_url1 = Column(String(100, 'utf8mb4_0900_bin'), comment='截图1')
    pic_url2 = Column(String(100, 'utf8mb4_0900_bin'), comment='截图2')
    pic_url3 = Column(String(100, 'utf8mb4_0900_bin'), comment='截图3')
    site_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')
