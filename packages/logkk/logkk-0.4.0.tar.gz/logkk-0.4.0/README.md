# Logkk

**易于使用**且**线程安全**的日志模块

### 安装
```shell
pip install logkk
```

### 基础使用：
```python
from logkk import LogManager

log_manager = LogManager()
log_manager.info("this is a info log")
log_manager.warn("this is a warn log")

logger = log_manager.get_logger(name="hello")
logger.info("this is a info log")
logger.warn("this is a warn log")
```

### 使用文件记录日志：

```python
from logkk import LogManager, Level
from logkk.handlers import FileHandler

fmt = "[{datetime}] [{level}] [{name}] {message}"
handler = FileHandler(filepath="/var/log/demo.log")
log_manager = LogManager(level=Level.INFO, fmt=fmt, handlers=[handler])
logger = log_manager.get_logger(name="hello")
logger.info("this is a info log")
logger.warn("this is a warn log")
```