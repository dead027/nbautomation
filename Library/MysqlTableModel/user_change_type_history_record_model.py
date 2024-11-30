# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserChangeTypeHistoryRecord(Base):
    __tablename__ = 'user_change_type_history_record'
    __table_args__ = {'comment': '会员remark变更记录'}

    id = Column(BIGINT(30), primary_key=True, unique=True)
    member_account = Column(String(45, 'utf8mb4_0900_bin'), comment=' 会员账号')
    code = Column(INTEGER(11))
    remark = Column(String(100, 'utf8mb4_0900_bin'), comment='备注')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(BIGINT(30))
    created_time = Column(BIGINT(30))
    updater = Column(BIGINT(30))
    updated_time = Column(BIGINT(30))
