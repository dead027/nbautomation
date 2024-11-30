# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserDepositWithdrawal(Base):
    __tablename__ = 'user_deposit_withdrawal'
    __table_args__ = (
        Index('type_user_time_index', 'user_id', 'type', 'created_time'),
        {'comment': '会员客户端存取款信息'}
    )

    id = Column(BIGINT(20), primary_key=True)
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), comment='会员ID')
    user_account = Column(String(50, 'utf8mb4_0900_bin'), comment='会员账号')
    type = Column(INTEGER(11), nullable=False, comment='订单类型 1 存款 2 取款 ')
    deposit_withdraw_type_id = Column(BIGINT(20), comment='存取款类型id')
    deposit_withdraw_type_code = Column(String(50, 'utf8mb4_0900_bin'), comment='存取款类型CODE')
    deposit_withdraw_way_id = Column(String(50, 'utf8mb4_0900_bin'), comment='存取款方式id')
    deposit_withdraw_way = Column(String(50, 'utf8mb4_0900_bin'), comment='存取款方式')
    deposit_withdraw_channel_id = Column(BIGINT(20), comment='存取款通道id')
    deposit_withdraw_channel_code = Column(String(255, 'utf8mb4_0900_bin'), comment='存取款通道code')
    deposit_withdraw_channel_name = Column(String(100, 'utf8mb4_0900_bin'), comment='存取通道name')
    deposit_withdraw_channel_type = Column(String(20, 'utf8mb4_0900_bin'), comment='充值通道类型（THIRD 三方 OFFLINE线下）')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='订单号')
    currency_code = Column(String(20, 'utf8mb4_0900_bin'), comment='币种')
    exchange_rate = Column(DECIMAL(20, 4), comment='汇率')
    trade_currency_amount = Column(DECIMAL(20, 8), comment='交易币种金额')
    apply_amount = Column(DECIMAL(20, 2), server_default=text("'0'"), comment='申请金额')
    arrive_amount = Column(DECIMAL(20, 2), server_default=text("'0'"), comment='实际到账金额')
    fee_rate = Column(DECIMAL(20, 4), server_default=text("'0'"), comment='手续费率')
    fee_amount = Column(DECIMAL(20, 2), server_default=text("'0.0000'"), comment='手续费')
    settlement_fee_rate = Column(DECIMAL(20, 4), server_default=text("'0'"), comment='结算手续费率')
    way_fee_amount = Column(DECIMAL(20, 4), comment='方式手续费')
    settlement_fee_amount = Column(DECIMAL(20, 4), server_default=text("'0'"), comment='结算手续费')
    account_type = Column(String(255, 'utf8mb4_0900_bin'), comment='账户类型（ 银行卡为银行名称，虚拟币为币种）')
    account_branch = Column(String(255, 'utf8mb4_0900_bin'), comment='账户分支（银行卡为开户行，虚拟币为链协议 如ERC20 TRC20)')
    deposit_withdraw_address = Column(String(50, 'utf8mb4_0900_bin'), comment='存取款地址（银行卡账号，虚拟币地址）')
    deposit_withdraw_name = Column(String(255, 'utf8mb4_0900_bin'), comment='存取款名字')
    deposit_withdraw_surname = Column(String(20, 'utf8mb4_0900_bin'), comment='存取款姓')
    area_code = Column(String(10, 'utf8mb4_0900_bin'), comment='区号')
    telephone = Column(String(20, 'utf8mb4_0900_bin'), comment='手机号')
    email = Column(String(255, 'utf8mb4_0900_bin'), comment='邮箱')
    cpf = Column(String(20, 'utf8mb4_0900_bin'), comment='cpf')
    address = Column(String(255, 'utf8mb4_0900_bin'), comment='地址')
    province = Column(String(64, 'utf8mb4_0900_bin'), comment='省')
    city = Column(String(64, 'utf8mb4_0900_bin'), comment='城市')
    postal_code = Column(String(10, 'utf8mb4_0900_bin'), comment='邮政编码')
    country = Column(String(64, 'utf8mb4_0900_bin'), comment='国家')
    is_first_out = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='是否首次出款')
    is_continue = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='是否连续出款')
    status = Column(CHAR(4, 'utf8mb4_0900_bin'), server_default=text("'1'"), comment='状态 1待一审 2一审审核 3一审拒绝 4待二审 5二审审核 6二审拒绝  7待三审 8三审审核 9 三审拒绝 10 待出款 20待处理  21处理中   90 已关闭 96出款失败 97出款取消 98取消订单（申请人） 100失败 101成功')
    review_operation = Column(INTEGER(11), comment='审核操作，system_param user_withdraw_review_operation值')
    is_big_money = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='是否大额出款;0-否，1-是')
    customer_status = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='客户端状态 0处理中 1成功 2失败')
    pay_audit_user = Column(String(50, 'utf8mb4_0900_bin'), comment='出款审核人')
    pay_lock_time = Column(BIGINT(20), comment='出款锁单时间')
    pay_audit_time = Column(BIGINT(20), comment='出款时间')
    pay_audit_remark = Column(String(500, 'utf8mb4_0900_bin'), comment='出款备注')
    pay_process_status = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='三方消息状态(1:获取中,2:已超时,3:异常,4:成功)')
    pay_fail_reason = Column(String(255, 'utf8mb4_0900_bin'), comment='支付失败原因')
    pay_third_url = Column(String(2048, 'utf8mb4_0900_bin'), comment='存取三方支付URL')
    pay_tx_id = Column(String(100, 'utf8mb4_0900_bin'), comment='三方关联流水id')
    channel_code = Column(String(50, 'utf8mb4_0900_bin'), comment='三方支付通道code')
    apply_ip = Column(String(100, 'utf8mb4_0900_bin'), comment='申请ip')
    apply_domain = Column(String(50, 'utf8mb4_0900_bin'), comment='申请域名')
    file_key = Column(String(100, 'utf8mb4_0900_bin'), comment='进出款凭证附件key')
    cash_flow_file = Column(String(500, 'utf8mb4_0900_bin'), comment='存款流水凭证')
    cash_flow_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='资金流水备注')
    device_type = Column(String(20, 'utf8mb4_0900_bin'), comment='设备终端')
    lock_status = Column(INTEGER(11), server_default=text("'0'"), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_bin'), comment='锁单人')
    lock_time = Column(BIGINT(20), comment='锁单时间')
    apply_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='申请备注')
    remark = Column(String(500, 'utf8mb4_0900_bin'), comment='备注')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    agent_id = Column(BIGINT(20), comment='代理ID')
    agent_account = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    activity_base_id = Column(BIGINT(20), comment='活动ID')
    discount_percent = Column(DECIMAL(10, 2), comment='优惠百分比')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    urge_order = Column(INTEGER(1), server_default=text("'0'"), comment='催单(0 未催单 1已催单0')
    collect_info = Column(String(500, 'utf8mb4_0900_bin'), comment='提款搜集信息')
    combined_recharge = Column(INTEGER(1), server_default=text("'0'"), comment='合并充值标记（虚拟币小额多笔）1 是 0否')
    recharge_withdraw_time_consuming = Column(BIGINT(20), comment='通道存款/提款耗时 秒')
    coin_code = Column(String(20, 'utf8mb4_0900_bin'), comment='交易币种')
    device_no = Column(String(100, 'utf8mb4_0900_bin'), comment='终端设备号')
