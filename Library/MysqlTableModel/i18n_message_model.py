# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class I18nMessage(Base):
    __tablename__ = 'i18n_message'
    __table_args__ = (
        Index('key_type_language_constraint', 'message_type', 'message_key', 'language', unique=True),
        {'comment': 'I18n訊息'}
    )

    id = Column(BIGINT(30), primary_key=True, comment='流水號')
    message_type = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, comment='類型')
    message_key = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, comment='鍵值')
    language = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='語系')
    message = Column(String(4000, 'utf8mb4_0900_bin'), nullable=False, comment='訊息內容')
    created_time = Column(BIGINT(30), nullable=False, comment='創建時間')
    updated_time = Column(BIGINT(30), comment='更新時間')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
