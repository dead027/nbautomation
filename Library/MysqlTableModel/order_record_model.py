# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class OrderRecord(Base):
    __tablename__ = 'order_record'
    __table_args__ = {'comment': '注单记录表'}

    id = Column(BIGINT(30), primary_key=True, comment='id')
    agent_id = Column(String(50, 'utf8mb4_0900_bin'), comment='代理id')
    agent_acct = Column(String(50, 'utf8mb4_0900_bin'), comment='代理账号')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    site_name = Column(String(20, 'utf8mb4_0900_bin'), comment='站点名称')
    user_id = Column(String(50, 'utf8mb4_0900_bin'), comment='会员id')
    user_account = Column(String(50, 'utf8mb4_0900_bin'), comment='会员账号')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='会员姓名')
    account_type = Column(INTEGER(11), comment='账号类型 1测试 2正式 3商务 4置换')
    vip_rank = Column(INTEGER(11), comment='vip段位')
    vip_grade_code = Column(INTEGER(11), comment='vip等级')
    casino_user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='三方会员账号')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏平台CODE')
    venue_type = Column(INTEGER(11), comment='游戏类别')
    game_name = Column(String(80, 'utf8mb4_0900_bin'), comment='游戏名称')
    third_game_code = Column(String(60, 'utf8mb4_0900_bin'), comment='三方游戏code')
    room_type = Column(String(50, 'utf8mb4_0900_bin'), comment='房间类型')
    room_type_name = Column(String(50, 'utf8mb4_0900_bin'), comment='房间类型名称')
    play_type = Column(String(50, 'utf8mb4_0900_bin'), comment='玩法类型')
    bet_time = Column(BIGINT(20), comment='投注时间')
    settle_time = Column(BIGINT(20), comment='结算时间')
    first_settle_time = Column(BIGINT(20), comment='首次结算时间')
    bet_amount = Column(DECIMAL(20, 6), comment='投注额')
    valid_amount = Column(DECIMAL(20, 6), comment='有效投注')
    payout_amount = Column(DECIMAL(20, 6), comment='派彩金额')
    win_loss_amount = Column(DECIMAL(20, 6), comment='输赢金额')
    order_id = Column(String(100, 'utf8mb4_0900_bin'), unique=True, comment='注单ID')
    third_order_id = Column(String(100, 'utf8mb4_0900_bin'), comment='三方注单ID')
    order_status = Column(INTEGER(11), comment='注单状态')
    order_classify = Column(INTEGER(11), comment='注单归类')
    odds = Column(String(100, 'utf8mb4_0900_bin'), comment='赔率')
    game_no = Column(String(100, 'utf8mb4_0900_bin'), comment='局号/期号')
    desk_no = Column(String(100, 'utf8mb4_0900_bin'), comment='桌号')
    boot_no = Column(String(100, 'utf8mb4_0900_bin'), comment='靴号')
    result_list = Column(String(500, 'utf8mb4_0900_bin'), comment='结果牌 /结果')
    bet_content = Column(String(500, 'utf8mb4_0900_bin'), comment='下注内容')
    change_status = Column(INTEGER(11), comment='变更状态')
    change_time = Column(BIGINT(20), comment='变更时间')
    change_count = Column(INTEGER(11), comment='变更次数')
    bet_ip = Column(String(200, 'utf8mb4_0900_bin'), comment='投注IP')
    currency = Column(String(20, 'utf8mb4_0900_bin'), comment='币种')
    device_type = Column(INTEGER(11), comment='设备类型')
    parlay_info = Column(Text(collation='utf8mb4_0900_bin'), comment='串关信息')
    remark = Column(String(500, 'utf8mb4_0900_bin'), comment='备注')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    result_time = Column(BIGINT(20), comment='结果产生时间(重结算后结算时间不会变化的场景, 使用该字段来判断是否发生重结算)')
    latest_time = Column(BIGINT(20), comment='最新变更时间，有重结算和撤销等异常时变更，初始值为落库时间')
    order_info = Column(String(2000, 'utf8mb4_0900_bin'), comment='注单详情')
    play_info = Column(String(500, 'utf8mb4_0900_bin'), comment='玩法')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))