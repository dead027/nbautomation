# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class VenueInfo(Base):
    __tablename__ = 'venue_info'
    __table_args__ = {'comment': '场馆详情'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏场馆CODE')
    venue_type = Column(INTEGER(11), comment='1:体育,2:视讯,3:棋牌,4:电子,5:彩票,6:斗鸡,7:电竞')
    venue_platform = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='三方平台')
    venue_name = Column(String(20, 'utf8mb4_0900_bin'), comment='游戏场馆名称')
    venue_icon = Column(String(255, 'utf8mb4_0900_bin'), comment='场馆图标')
    venue_proportion = Column(DECIMAL(10, 2), comment='场馆费率')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='状态（ 1 开启中 2 维护中 0 已禁用）')
    bet_url = Column(String(255, 'utf8mb4_0900_bin'), comment='拉取注单地址')
    api_url = Column(String(255, 'utf8mb4_0900_bin'), comment='API URL\\n创建 登陆')
    game_url = Column(String(255, 'utf8mb4_0900_bin'), comment='游戏地址')
    merchant_no = Column(String(50, 'utf8mb4_0900_bin'), comment='商户编码')
    aes_key = Column(String(255, 'utf8mb4_0900_bin'), comment='AES密钥')
    merchant_key = Column(String(500, 'utf8mb4_0900_bin'), comment='商户密钥')
    bet_key = Column(String(500, 'utf8mb4_0900_bin'), comment='拉单key')
    creator = Column(BIGINT(20), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人名称')
    updated_time = Column(BIGINT(20), comment='更新时间')
    remark = Column(String(200, 'utf8mb4_0900_bin'), server_default=text("''"), comment='备注')
    maintenance_start_time = Column(BIGINT(20), comment='维护开始时间')
    maintenance_end_time = Column(BIGINT(20), comment='维护结束时间')
    name_prefix = Column(String(50, 'utf8mb4_0900_bin'), comment='用于区分环境的名字前缀,一般使用Utest_为前缀')
