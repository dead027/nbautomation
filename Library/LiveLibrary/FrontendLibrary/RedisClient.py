#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/10/4 18:50
# redis-server
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.Common.Utils.Contexts import *

redis_path_dic = {"room": "roomList::roomInfo::", "token": "userInfo::token", "room_id_list": "roomIdList",
                  "sid_uid": "sid::uid", "uid_sid": "uid::sid", "uid_room_id": "uid::rid",
                  "system_config": "systemConfig", "round_data": "game::roundData::"}


class RedisClient(object):
    """
    存非对象
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def record_boot_no(desk_no, boot_no):
        origin_boot_no = live_rds_context.get().hash_get("TempGameNo", desk_no)
        if origin_boot_no != boot_no:
            live_rds_context.get().hash_multi_set("TempGameNo", {desk_no: boot_no})

    @staticmethod
    def get_boot_no(desk_no):
        return live_rds_context.get().hash_get("TempGameNo", desk_no)


if __name__ == "__main__":
    rc = RedisClient("sit")
    rc.record_boot_no("GG01", "aaa1")
