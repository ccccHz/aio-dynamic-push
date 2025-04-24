import threading
import time
from typing import List

import schedule

import push_channel
import query_task
from common.config import global_config
from common.logger import log
from web_ui import server


def init_push_channel(push_channel_config_list: list):
    log.info("开始初始化推送通道")
    for config in push_channel_config_list:
        if config.get('enable', False):
            if push_channel.push_channel_dict.get(config.get('name', '')) is not None:
                raise ValueError(f"推送通道名称重复: {config.get('name', '')}")

            log.info(f"初始化推送通道: {config.get('name', '')}，通道类型: {config.get('type', None)}")
            push_channel.push_channel_dict[config.get('name', '')] = push_channel.get_push_channel(config)


def init_push_channel_test(common_config: dict):
    push_channel_config: dict = common_config.get("push_channel", {})
    send_test_msg_when_start = push_channel_config.get("send_test_msg_when_start", False)
    if send_test_msg_when_start:
        for channel_name, channel in push_channel.push_channel_dict.items():
            log.info(f"推送通道【{channel_name}】发送测试消息")
            channel.push(title=f"【{channel_name}】通道测试",
                         content=f"可正常使用🎉",
                         jump_url="https://www.baidu.com",
                         pic_url=None,
                         extend_data={})


class TaskStore:
    def __init__(self):
        self._tasks: List[query_task.QueryTask] = []
        self._lock = threading.Lock()

    def add(self, task: query_task.QueryTask):
        with self._lock:
            self._tasks.append(task)

    def all(self) -> List[query_task.QueryTask]:
        with self._lock:
            return list(self._tasks)  # 返回副本，避免被外部改动

def init_query_task(query_task_config_list: list, taskStore: TaskStore):
    log.info("初始化查询任务")
    for config in query_task_config_list:
        if config.get('enable', False):
            task = query_task.get_query_task(config)
            schedule.every(config.get("intervals_second", 60)).seconds.do(task.query)
            log.info(f"初始化查询任务: {config.get('name', '')}，任务类型: {config.get('type', None)}")
            # 先执行一次
            task.query()
            taskStore.add(task)

    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    taskStore = TaskStore()
    common_config = global_config.get_common_config()
    query_task_config_list = global_config.get_query_task_config()
    push_channel_config_list = global_config.get_push_channel_config()
    # 初始化推送通道
    init_push_channel(push_channel_config_list)
    # 初始化推送通道测试
    init_push_channel_test(common_config)
        # 创建线程
    server_thread = threading.Thread(target=lambda: server.start_web_ui(taskStore))
    query_task_thread = threading.Thread(target=lambda: init_query_task(query_task_config_list,taskStore))
    
    # 设置为守护线程，这样主程序退出时，线程也会被强制退出
    server_thread.daemon = True
    query_task_thread.daemon = True
    
    # 启动线程
    server_thread.start()
    query_task_thread.start()
    
    server_thread.join()
    query_task_thread.join()
 

if __name__ == '__main__':
    main()
