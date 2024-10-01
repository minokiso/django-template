import logging
import os
from logging.handlers import RotatingFileHandler


# 创建一个通用的日志记录器配置函数
def setup_logger(name, log_file, level=logging.DEBUG, max_bytes=5 * 1024 * 1024, backup_count=3, need_console=True):
    """创建并配置一个 logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # 创建格式器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s')

    # 构建日志文件的绝对路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(project_root, log_file)
    # 创建处理器，写入到指定的日志文件，设置日志轮转
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # 添加到 logger
    logger.addHandler(file_handler)

    # 如果需要控制台输出，添加一个 StreamHandler
    if need_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    return logger


# 使用通用函数创建logger
http_logger = setup_logger('http', 'logs/http.log')
sio_client_logger = setup_logger('sio_client', 'logs/sio_client.log')
sio_server_logger = setup_logger('sio_server', 'logs/sio_server.log')

# 测试日志
if __name__ == '__main__':
    http_logger.info("This is a debug message from sync logger")
    sio_client_logger.info("This is an info message from async logger")
