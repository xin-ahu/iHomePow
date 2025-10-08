# coding = "utf-8"
import logging
import colorlog
from datetime import datetime

# 创建一个全局的日志记录器实例
logger = logging.getLogger('iHomePowLogger')
logger.setLevel(level=logging.ERROR)
logger.disabled = False

# 避免重复添加处理器
if not logger.hasHandlers():
    """创建支持字体颜色显示的格式化器"""
    coloredFormatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)d]>>>>>>>>>>%(message)s",
        log_colors={
            "DEBUG": "white",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_black"
        }
    )

    """创建日志控制台处理器并为其设置支持字体颜色显示的格式化器，指定输出格式"""
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(coloredFormatter)
    logger.addHandler(consoleHandler)  # 为日志记录器添加控制台处理器

    """创建日志文件处理器并为其设置普通格式化器，指定输出格式"""
    cur_time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")  # 获取当前时间
    fileHandler = logging.FileHandler(filename=f"./logs/{cur_time}.log", mode="a", encoding="utf-8")
    formatter = logging.Formatter(fmt="%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)d]>>>>>>>>>>%(message)s")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)     # 为日志记录器添加文件处理器


def get_logger():
    """返回全局日志记录器实例"""
    return logger


if __name__ == "__main__":
    log = get_logger()
    """日志调用"""
    log.debug("this is a debug message")
    log.info("this is an info message")
    log.warning("this is an warning message")
    log.error("this is an error message")
    log.critical("this is an critical message")
