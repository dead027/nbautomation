# coding: utf-8
from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BusinessMenu(Base):
    __tablename__ = 'business_menu'
    __table_args__ = {'comment': '菜单信息'}

    id = Column(BIGINT(30), primary_key=True, comment='菜单ID')
    menu_key = Column(String(500, 'utf8mb4_0900_bin'), comment='菜单KEY唯一标识')
    name = Column(String(50, 'utf8mb4_0900_bin'), comment='菜单名称')
    parent_id = Column(BIGINT(20), server_default=text("'0'"), comment='父菜单ID')
    order_num = Column(INTEGER(11), server_default=text("'0'"), comment='显示顺序')
    path = Column(String(200, 'utf8mb4_0900_bin'), server_default=text("''"), comment='菜单上下级全路径 ')
    api_url = Column(String(500, 'utf8mb4_0900_bin'), comment='API权限标识')
    url = Column(String(500, 'utf8mb4_0900_bin'), comment='菜单路径')
    type = Column(TINYINT(4), server_default=text("'0'"), comment='菜单类型（1目录 2菜单 9按钮）')
    level = Column(TINYINT(4), comment='层次')
    visible = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='菜单状态（0显示 1隐藏）')
    status = Column(TINYINT(4), server_default=text("'0'"), comment='菜单状态（0正常 1停用）')
    creator = Column(BIGINT(20), comment='创建人')
    updater = Column(BIGINT(20), comment='更新人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    remark = Column(String(500, 'utf8mb4_0900_bin'), server_default=text("''"), comment='备注')
    super_admin_only_visible = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='1: 超級管理员只能看到這个菜单')
    business_id = Column(INTEGER(11))
