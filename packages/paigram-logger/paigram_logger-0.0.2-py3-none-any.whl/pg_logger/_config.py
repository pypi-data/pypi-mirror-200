from multiprocessing import RLock as Lock
from pathlib import Path
from typing import (
    List,
    Optional,
    Union,
)

from pydantic import BaseSettings

from pg_logger._typedefs import COLOR_SYSTEM

__all__ = ("LoggerConfig",)


class LoggerConfig(BaseSettings):
    _lock = Lock()
    _instance: Optional["LoggerConfig"] = None

    def __new__(cls, *args, **kwargs) -> "LoggerConfig":
        with cls._lock:
            if cls._instance is None:
                cls.update_forward_refs()
                result = super(LoggerConfig, cls).__new__(cls)
                result.__init__(*args, **kwargs)
                cls._instance = result
        return cls._instance

    name: str = "PaiGram-Logger"
    """logger 的名称"""
    level: Optional[Union[str, int]] = None
    """logger 的 level"""

    debug: bool = False
    """是否 debug"""
    width: Optional[int] = None
    """输出时的宽度"""
    keywords: List[str] = []
    """高亮的关键字"""
    time_format: str = "[%Y-%m-%d %X]"
    """时间格式"""
    capture_warnings: bool = True
    """是否捕获 warning"""
    color_system: COLOR_SYSTEM = "auto"
    """颜色模式： 自动、标准、256色、真彩、Windows模式"""

    log_path: Union[str, Path] = "./logs"
    """log 所保存的路径，项目根目录的相对路径"""
    project_root: Union[str, Path] = Path(".")
    """项目根目录"""

    traceback_max_frames: int = 20
    """Traceback 的最大回溯帧数"""
    traceback_locals_max_depth: Optional[int] = None
    """Traceback 的 locals 变量的最大访问深度"""
    traceback_locals_max_length: int = 10
    """打印 Traceback 的 locals 变量时的最大长度"""
    traceback_locals_max_string: int = 80
    """打印 Traceback 的 locals 变量时的最大字符数"""

    class Config(BaseSettings.Config):
        env_prefix = "logger_"
