# paigram-logger
A logger for PaiGram's projects.

## 使用方法

### 使用默认配置

```python
from pg_logger import Logger

logger = Logger()

logger.info("info log")
logger.success("success log")
```

### 自定义配置 Logger

```python
from pg_logger import Logger, LoggerConfig

logger = Logger(
    LoggerConfig(
        width=120,
        keywords=['GET', 'PUT', 'POST']
    )
)

logger.info("[GET] info log")
logger.success("[PUT] success log")

```