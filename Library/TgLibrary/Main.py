import time
import telegram
from telegram.ext import Updater  # 更新者
from telegram.ext import CommandHandler  # 注册处理 一般用 回答用
from Library.Common.Utils.Contexts import *
from Library.Dao import Dao
from Library.VO import VO
from Library.BO import BO
from Library.ApiRequests import ApiRequests
from Library.Common.ServerConnector.Redis import RedisBase
from Library.Common.ServerConnector.Mysql import MysqlBase
from Variables import *
from Library.TgLibrary.ReloadMenuTable import ReloadMenuTable
from Library.TgLibrary.GetRedisCode import RedisClient
from Library.Common.Utils.LoginUtil import LoginUtil
from Library.ApiRequests.XJobApi.BaseOperation import BaseOperation
from Library.Common.Utils.DateUtil import DateUtil

token_dic = {"sit": "6922163311:AAHTpqU7XPAAGSJWcRsgDpkw20PUCqsDwgA",
             "dev": "6922163311:AAHTpqU7XPAAGSJWcRsgDpkw20PUCqsDwgA"}
white_tg_list = ["GoodMan567"]
env = 'sit'
dao = Dao(env)
api = ApiRequests(env)
env_context.set(env)


class Services(object):
    def __init__(self):

        token = token_dic[env]
        self.CHAT_ID = 1390401344  # 个人ID
        self.api_id = 9418298
        self.api_hash = "26f630ff308bfab9ef97d01e4e2de282"
        self.client_ip = "149.154.167.50:443"
        self.phone_number = "+85581591228"
        self.updater = Updater(token=token, use_context=True)
        self.dp = self.updater.dispatcher
        self.bot = telegram.Bot(token)
        self.init_bot_commands()
        self.client = None
        print("Init done.")

    def init_bot_commands(self):
        """
        可用命令
        :return:
        """
        member_command_dic = {
            "/unlock_account": "后台账号解锁,格式:'/unlock_account 后台账号 站点编号(总台账号不用)'",
            "/get_chat_and_user_id": "获取TG用户ID和群ID,格式:'/get_chat_and_user_id'",
            "/create_user": "创建正式会员，格式: /create_user 用户名 代理(可选) 币种(可选,CNY-默认,"
                            "VND,PHP,MYR,USDT)  密码(可选,默认abcd1234)",
            "/recharge_by_manual": '人工充值，应为：/recharge_by_manual 会员账号 金额 流水倍数(默认1) 站点编号(可选)',
            "/decrease_by_manual": "人工后台减额,格式：/decrease_by_manual 账号 金额 站点编号(可选)",
            "/update_business_menu_table": "更新权限表，格式: /update_business_menu_table",
            "/get_verify_code": "获取手机或邮箱验证码，格式：/get_verify_code 站点编号 会员账号",
            "/increase_typing_amount": '增加打码量，格式：/increase_typing_amount 账号 数量  站点code(可选)',
            "/modify_platform_balance": '修改用户平台币，格式：/modify_platform_balance 账号 数量(负号为减额)  站点code(可选)',
            "/clean_typing_amount": '清空打码量，格式：/clean_typing_amount 账号 站点code(可选)',
            "/overflow": '溢出，格式：/overflow 会员账号 代理 站点code(可选)',
            "/transfer_agent": '转代，格式：/transfer_agent 会员账号 代理 站点code(可选)',
            "/agent_recharge": '代理人工充值，格式：/agent_recharge_by_manual 代理账号 金额 钱包类型(佣金钱包｜额度钱包-默认) '
                               '站点编号(可选)',
            "/get_agent_front_data": '代理人工充值，格式：/get_agent_front_data 代理账号 站点编号(可选)',
            "/withdraw_callback": "提款回调，格式：/withdraw_callback 订单ID 站点编号(可选)",
            # "/execute_commission_job": "刷新预期佣金报表，格式：/execute_commission_job 代理  站点(可选)",
            # "/execute_user_win_lose_job": "执行会员盈亏定时任务，格式：/execute_user_win_lose_job 日偏移 站点(可选)",
        }
        self.bot.set_my_commands([telegram.BotCommand(key, value) for key, value in member_command_dic.items()])

    def init_dispatcher(self):
        """
        设置客户端请求响应
        :return:
        """
        # 人工充值
        self.dp.add_handler(CommandHandler("unlock_account", self.unlock_admin))
        self.dp.add_handler(CommandHandler("get_chat_and_user_id", self.get_chat_and_user_id))
        self.dp.add_handler(CommandHandler("create_user", self.create_user))
        self.dp.add_handler(CommandHandler("recharge_by_manual", self.recharge_by_manual))
        self.dp.add_handler(CommandHandler("decrease_by_manual", self.decrease_by_manual))
        self.dp.add_handler(CommandHandler("update_business_menu_table", self.update_business_menu_table))
        self.dp.add_handler(CommandHandler("get_verify_code", self.get_verify_code))
        self.dp.add_handler(CommandHandler("increase_typing_amount", self.increase_typing_amount))
        self.dp.add_handler(CommandHandler("clean_typing_amount", self.clean_typing_amount))
        self.dp.add_handler(CommandHandler("modify_platform_balance", self.modify_platform_balance))
        self.dp.add_handler(CommandHandler("overflow", self.overflow))
        self.dp.add_handler(CommandHandler("transfer_agent", self.transfer_agent))
        self.dp.add_handler(CommandHandler("agent_recharge", self.recharge_by_manual_agent))
        self.dp.add_handler(CommandHandler("get_agent_front_data", self.get_agent_front_data))
        self.dp.add_handler(CommandHandler("withdraw_callback", self.withdraw_callback))
        self.dp.add_handler(CommandHandler("execute_commission_job", self.execute_commission_job))
        self.dp.add_handler(CommandHandler("execute_user_win_lose_job", self.execute_user_win_lose_job))

    def main(self):
        self.init_dispatcher()
        # 允许bot
        self.updater.start_polling()
        # 待命 若要停止按ctrl -c，在开始运作后你无法对机器人做任何动作，例如对指定人发讯
        # self.updater.idle()

    @staticmethod
    def get_chat_and_user_id(update, context):
        print(f'【get_chat_and_user_id】 收到消息')
        message = update.message.to_dict()
        update.message.reply_text(f'本群的ID为：{message["chat"]["id"]},你的ID为: {message["from"]["id"]}')

    @staticmethod
    def unlock_admin(update, context):
        """
        后台账号解锁
        :param update:
        :param context:
        :return:
        """
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【后台账号解锁】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 2:
            update.message.reply_text(f'格式不正确，应为："/unlock_admin 账号 站点编号(总台账号不用)"')
            return
        try:
            Dao.unlock_backend_account(input_list[1], input_list[2])
            update.message.reply_text(f'解锁完成')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def execute_commission_job(update, context):
        """
        执行佣金报表预期
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【执行佣金报表预期】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        input_len = len(input_list)
        if input_len < 2:
            update.message.reply_text(f'格式不正确，应为："/execute_commission_job 代理  站点(可选)')
            return
        try:
            LoginUtil.login_job()
            site_code = 'Vd438R' if input_len < 3 else input_list[2]
            agent_account = input_list[1]

            timezone = Dao.get_site_timezone(site_code)
            cycle_type = BO.get_agent_commission_plan_bo(site_code, agent_account)[agent_account]["结算周期"]
            date_type = cycle_type[-1]
            start_time, end_time = DateUtil.get_timestamp_range(0, 0, 0, date_type, timezone)
            param = {
                "timeZone": f"UTC{timezone}",
                "settleCycle": {"日": 0, "周": 1, "月": 2}[date_type],
                "isManual": 1,
                "siteCode": site_code,
                "startTime": start_time,
                "endTime": end_time
            }
            BaseOperation.trigger_task("预期佣金结算", param=param)
            update.message.reply_text('操作成功')
        except Exception as e:
            update.message.reply_text(f'失败: {str(e)}')

    @staticmethod
    def execute_user_win_lose_job(update, context):
        """
        执行会员盈亏报表预期
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【执行会员盈亏报表预期】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        input_len = len(input_list)
        if input_len < 2:
            update.message.reply_text(f'格式不正确，应为："/execute_user_win_lose_job 日偏移 站点(可选)')
            return
        try:
            LoginUtil.login_job()
            site_code = 'Vd438R' if input_len < 3 else input_list[2]

            timezone = Dao.get_site_timezone(site_code)
            start_time, end_time = DateUtil.get_timestamp_range(input_list[1], input_list[1], timezone=timezone)
            param = {
                "siteCode": "Vd438R",
                "startTime": start_time,
                "endTime": end_time
            }
            BaseOperation.trigger_task("会员盈亏", param=param)
            update.message.reply_text('操作成功')
        except Exception as e:
            update.message.reply_text(f'失败: {str(e)}')

    @staticmethod
    def create_user(update, context):
        """
        后台创建会员
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【后台创建会员】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        input_len = len(input_list)
        if input_len not in (2, 3, 4, 5):
            update.message.reply_text(f'格式不正确，应为："/create_user 用户名 代理(可选)  '
                                      f'币种(可选,CNY-默认,VND,PHP,MYR,USDT)  密码(可选,默认abcd1234)"')
            return
        try:
            site_code = 'Vd438R'
            LoginUtil.login_site_backend(site_code, site_account1, password)
            agent_account = "" if input_len < 3 else input_list[2]
            currency = "CNY" if input_len < 4 else input_list[3]
            pwd = "abcd1234" if input_len < 5 else input_list[4]
            msg = api.create_user_api(input_list[1], pwd, '正式', currency, parent_agent=agent_account, check_code=False)

            if msg not in ['success', '成功']:
                update.message.reply_text(msg)
                return
            order_no = Dao.wait_has_new_user_audit_order(input_list[1])
            LoginUtil.login_site_backend(site_code, site_account2, password)
            api.lock_register_order_api(order_no, "已锁", False)
            api.audit_register_order_api(order_no, check_code=False)
            update.message.reply_text(msg)
        except Exception as e:
            update.message.reply_text(f'创建 {input_list[1]} 失败: {str(e)}')

    @staticmethod
    def recharge_by_manual(update, context):
        """
        后台人工充值
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【后台人工充值】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为："/recharge_by_manual 会员账号 金额 流水倍数(默认1) 站点编号(可选)"')
            return
        site_code = input_list[3] if len(input_list) == 5 else 'Vd438R'
        try:
            user_account = input_list[1]
            amount = input_list[2]
            rate = 1 if len(input_list) < 4 else input_list[3]
            balance_before = dao.get_user_balance_dao(site_code, user_account)[2]
            LoginUtil.login_site_backend(site_code, site_account1, password)
            order_no = api.increase_user_balance_manually_api(site_code, user_account, '会员存款(后台)', amount, rate)
            LoginUtil.login_site_backend(site_code, site_account2, password)
            time.sleep(1)
            api.lock_user_manual_order_api(site_code, order_no, '已锁', '一审')
            api.audit_manual_increase_order_api(site_code, order_no, '通过')
            time.sleep(1)
            balance_after = dao.get_user_balance_dao(site_code, user_account)[2]
            update.message.reply_text(f'会员【{user_account}】充值成功:\n\t充值前 --> {balance_before}\n'
                                      f'\t充值金额 --> {amount}\n\t充值后 --> {balance_after}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def decrease_by_manual(update, context):
        """
        后台人工减额
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【人工扣除金额】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            a = update.message.reply_text(f'格式不正确，应为："/decrease_by_manual 账号 金额 站点编号(可选)"')
            print("消息返回:", a)
            return
        try:
            user_account = input_list[1]
            amount = input_list[2]
            site_code = input_list[3] if len(input_list) == 5 else 'Vd438R'
            remain = Dao.get_user_typing_amount_dao(site_code, user_account)
            if remain > 0:
                update.message.reply_text(f'操作失败,存在剩余打码量: {remain}')
                return

            balance_before = dao.get_user_balance_dao(site_code, user_account)[2]
            LoginUtil.login_site_backend(site_code, site_account1, password)
            api.decrease_user_balance_manually_api(site_code, user_account, '会员提款(后台)', amount)
            time.sleep(1)
            balance_after = dao.get_user_balance_dao(site_code, user_account)[2]
            update.message.reply_text(f'会员【{user_account}】人工扣除成功:\n\t扣除前 --> {balance_before}\n'
                                      f'\t扣除金额 --> {amount}\n\t扣除后 --> {balance_after}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def update_business_menu_table(update, context):
        """
        自动更新权限表
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【自动更新权限表】 收到消息: {message["text"]}')
        try:
            env_context.set('dev')
            ms_context.get().__init__()
            ReloadMenuTable.export_menu()
            env_context.set('sit')
            ms_context.get().__init__()
            ReloadMenuTable.truncate_table()
            ReloadMenuTable.import_menu()
            env_context.set(env)
            ms_context.get().__init__()
            update.message.reply_text(f'自动更新权限表 成功')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def get_verify_code(update, context):
        """
        获取手机或邮箱验证码
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【获取手机或邮箱验证码】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为："获取手机或邮箱验证码，格式：/get_verify_code 站点编号 会员账号')
            return
        try:
            msg = RedisClient.get_msg_code(input_list[1], input_list[2])[1:-1]
            update.message.reply_text(f'验证码:\t{msg}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def withdraw_callback(update, context):
        """
        提款回调
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【提款回调】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 2:
            update.message.reply_text(f'格式不正确，应为："提款回调，格式：/withdraw_callback 订单ID 站点编号(可选)')
            return
        try:
            # site_code = input_list[2] if len(input_list) == 3 else 'Vd438R'
            import requests
            requests.get(f'https://gw.playesoversea.pro/pay/callback/api/testPayoutCallback?orderId={input_list[1]}'
                         f'&status=1')
            update.message.reply_text(f'成功')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def increase_typing_amount(update, context):
        """
        增加打码量
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【增加打码量】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为：/increase_typing_amount 账号 数量  站点code(可选)')
            return
        try:
            site_code = input_list[3] if len(input_list) == 4 else 'Vd438R'
            user_account = input_list[1]
            LoginUtil.login_site_backend(site_code, site_account1, password)
            try:
                ApiRequests.add_flow_amount_api(user_account, input_list[2])
            except AssertionError as e:
                update.message.reply_text(f'提交申请操作失败: {str(e)}')
            audit_info = Dao.get_user_change_audit_list_sql(site_code, user_account=user_account)[0]
            order_id = audit_info.id
            LoginUtil.login_site_backend(site_code, site_account2, password)
            ApiRequests.lock_user_modify_order_api(order_id)
            ApiRequests.audit_user_modify_order_api(order_id)
            remain = Dao.get_user_typing_amount_dao(site_code, input_list[1])
            update.message.reply_text(f'操作成功,当前剩余打码量: {remain}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def clean_typing_amount(update, context):
        """
        清除打码量
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【增加打码量】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 2:
            update.message.reply_text(f'格式不正确，应为：/clean_typing_amount 账号 站点code(可选)')
            return
        try:
            site_code = input_list[2] if len(input_list) == 3 else 'Vd438R'
            LoginUtil.login_site_backend(site_code, site_account1, password)
            ApiRequests.clear_flow_amount_api(input_list[1])
            remain = Dao.get_user_typing_amount_dao(site_code, input_list[1])
            update.message.reply_text(f'操作成功,当前剩余打码量: {remain}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def overflow(update, context):
        """
        会员溢出
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【会员溢出】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为：/overflow 账号 代理 站点code(可选)')
            return
        try:
            site_code = input_list[-1] if len(input_list) == 4 else 'Vd438R'
            LoginUtil.login_site_backend(site_code, site_account1, password)
            ApiRequests.user_overflow_apply_api(input_list[1], input_list[2])
            order_id = Dao.get_user_overflow_record_sql(site_code, input_list[1])
            time.sleep(1)
            LoginUtil.login_site_backend(site_code, site_account2, password)
            ApiRequests.lock_overflow_order_api(order_id)
            time.sleep(1)
            ApiRequests.audit_overflow_order_api(order_id)
            update.message.reply_text(f'操作成功')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def transfer_agent(update, context):
        """
        会员转代
        @param update:
        @param context:
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【会员转代】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为：/transfer_agent 账号 代理 站点code(可选)')
            return
        try:
            site_code = input_list[-1] if len(input_list) == 4 else 'Vd438R'
            LoginUtil.login_site_backend(site_code, site_account1, password)
            ApiRequests.transfer_agent_apply_api(input_list[1], input_list[2])
            order_id = Dao.get_transfer_agent_record_sql(site_code, input_list[1])
            time.sleep(1)
            LoginUtil.login_site_backend(site_code, site_account2, password)
            ApiRequests.lock_transfer_agent_order_api(order_id)
            time.sleep(1)
            ApiRequests.audit_transfer_agent_order_api(order_id)
            update.message.reply_text(f'操作成功')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def modify_platform_balance(update, context):
        """
        修改平台币余额
        @return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【修改平台币余额】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为：/modify_platform_balance 账号 数量(负号为减额)  站点code(可选)')
            return
        try:
            site_code = input_list[3] if len(input_list) == 4 else 'Vd438R'
            user_account = input_list[1]
            amount = input_list[2]
            balance_before = dao.get_user_platform_balance_dao(site_code, user_account)[2]
            Dao.sql_update_user_platform_coin_dao(site_code, user_account, amount)
            balance_after = dao.get_user_platform_balance_dao(site_code, user_account)[2]
            update.message.reply_text(f'会员【{user_account}】平台币修改成功:\n\t修改前 --> {balance_before}\n'
                                      f'\t修改金额 --> {amount}\n\t修改后 --> {balance_after}')
            update.message.reply_text(f'操作成功,当前剩余平台币: {balance_after}')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def recharge_by_manual_agent(update, context):
        """
        代理后台人工充值
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【代理后台人工充值】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 3:
            update.message.reply_text(f'格式不正确，应为："/agent_recharge_by_manual 代理账号 金额 '
                                      f'钱包类型(佣金钱包｜额度钱包-默认) 站点编号(可选)"')
            return
        site_code = input_list[4] if len(input_list) == 5 else 'Vd438R'
        try:
            agent_account = input_list[1]
            amount = input_list[2]
            wallet_type = "额度钱包" if len(input_list) < 4 else input_list[3]
            LoginUtil.login_site_backend(site_code, site_account1, password)
            order_id = api.increase_agent_balance_manually_api(site_code, agent_account, amount,
                                                               wallet_type=wallet_type)
            LoginUtil.login_site_backend(site_code, site_account2, password)
            time.sleep(1)
            api.lock_agent_manual_order_api(order_id, '已锁')
            api.audit_agent_manual_increase_order_api(order_id, '通过')
            update.message.reply_text(f'成功')
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')

    @staticmethod
    def get_agent_front_data(update, context):
        """
        代理首页统计信息
        :param update:
        :param context:
        :return:
        """
        env_context.set(env)
        rds_context.set(RedisBase())
        ms_context.set(MysqlBase())
        message = update.message.to_dict()
        print(f'【代理首页统计信息】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) < 2:
            update.message.reply_text(f'格式不正确，应为："/get_agent_front_data 代理账号 站点编号(可选)"')
            return
        site_code = input_list[4] if len(input_list) == 5 else 'Vd438R'
        try:
            agent_account = input_list[1]
            rtn = VO.get_head_summary_vo(site_code, agent_account)
            update.message.reply_text(str(rtn))
        except Exception as e:
            update.message.reply_text(f'执行失败: {str(e)}')


if __name__ == "__main__":
    # env_context.set(env)
    bot = Services()
    bot.main()
    # pymysql.err.OperationalError
