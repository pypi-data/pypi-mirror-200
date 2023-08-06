# (generated with --quick)

import copy
import io
import logging
import os
import pickle
import queue
import re
import socket
import struct
import threading
import time
from typing import Any, Dict, List, Optional, TypeVar, Union

DEFAULT_HTTP_LOGGING_PORT: int
DEFAULT_SOAP_LOGGING_PORT: int
DEFAULT_TCP_LOGGING_PORT: int
DEFAULT_UDP_LOGGING_PORT: int
ST_DEV: int
ST_INO: int
ST_MTIME: int
SYSLOG_TCP_PORT: int
SYSLOG_UDP_PORT: int
_MIDNIGHT: int

_T0 = TypeVar('_T0')

class BaseRotatingHandler(logging.FileHandler):
    __doc__: str
    encoding: Any
    mode: Any
    namer: None
    rotator: None
    def __init__(self, filename, mode, encoding = ..., delay = ...) -> None: ...
    def emit(self, record) -> None: ...
    def rotate(self, source, dest) -> None: ...
    def rotation_filename(self, default_name) -> Any: ...

class BufferingHandler(logging.Handler):
    __doc__: str
    buffer: list
    capacity: Any
    def __init__(self, capacity) -> None: ...
    def close(self) -> None: ...
    def emit(self, record) -> None: ...
    def flush(self) -> None: ...
    def shouldFlush(self, record) -> bool: ...

class DatagramHandler(SocketHandler):
    __doc__: str
    address: Any
    closeOnError: bool
    host: Any
    port: Any
    retryFactor: float
    retryMax: float
    retryPeriod: float
    retryStart: float
    retryTime: Optional[float]
    sock: Any
    def __init__(self, host, port) -> None: ...
    def makeSocket(self) -> socket.socket: ...
    def send(self, s) -> None: ...

class HTTPHandler(logging.Handler):
    __doc__: str
    context: Any
    credentials: Any
    host: Any
    method: Any
    secure: Any
    url: Any
    def __init__(self, host, url, method = ..., secure = ..., credentials = ..., context = ...) -> None: ...
    def emit(self, record) -> None: ...
    def mapLogRecord(self, record) -> Any: ...

class MemoryHandler(BufferingHandler):
    __doc__: str
    buffer: List[nothing]
    capacity: Any
    flushLevel: Any
    flushOnClose: Any
    target: Any
    def __init__(self, capacity, flushLevel = ..., target = ..., flushOnClose = ...) -> None: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def setTarget(self, target) -> None: ...
    def shouldFlush(self, record) -> Any: ...

class NTEventLogHandler(logging.Handler):
    __doc__: str
    _welu: Optional[module]
    appname: Any
    deftype: int
    dllname: Any
    logtype: Any
    typemap: Dict[int, int]
    def __init__(self, appname, dllname = ..., logtype = ...) -> None: ...
    def close(self) -> None: ...
    def emit(self, record) -> None: ...
    def getEventCategory(self, record) -> int: ...
    def getEventType(self, record) -> int: ...
    def getMessageID(self, record) -> int: ...

class QueueHandler(logging.Handler):
    __doc__: str
    queue: Any
    def __init__(self, queue) -> None: ...
    def emit(self, record) -> None: ...
    def enqueue(self, record) -> None: ...
    def prepare(self, record: _T0) -> _T0: ...

class QueueListener:
    __doc__: str
    _sentinel: None
    _thread: Optional[threading.Thread]
    handlers: tuple
    queue: Any
    respect_handler_level: Any
    def __init__(self, queue, *handlers, respect_handler_level = ...) -> None: ...
    def _monitor(self) -> None: ...
    def dequeue(self, block) -> Any: ...
    def enqueue_sentinel(self) -> None: ...
    def handle(self, record) -> None: ...
    def prepare(self, record: _T0) -> _T0: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...

class RotatingFileHandler(BaseRotatingHandler):
    __doc__: str
    backupCount: Any
    encoding: Any
    maxBytes: Any
    mode: Any
    namer: None
    rotator: None
    stream: Optional[io.TextIOWrapper]
    def __init__(self, filename, mode = ..., maxBytes = ..., backupCount = ..., encoding = ..., delay = ...) -> None: ...
    def doRollover(self) -> None: ...
    def shouldRollover(self, record) -> int: ...

class SMTPHandler(logging.Handler):
    __doc__: str
    fromaddr: Any
    mailhost: Any
    mailport: Any
    password: Any
    secure: Any
    subject: Any
    timeout: Any
    toaddrs: Any
    username: Any
    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials = ..., secure = ..., timeout = ...) -> None: ...
    def emit(self, record) -> None: ...
    def getSubject(self, record) -> Any: ...

class SocketHandler(logging.Handler):
    __doc__: str
    address: Any
    closeOnError: bool
    host: Any
    port: Any
    retryFactor: float
    retryMax: float
    retryPeriod: float
    retryStart: float
    retryTime: Optional[float]
    sock: Optional[socket.socket]
    def __init__(self, host, port) -> None: ...
    def close(self) -> None: ...
    def createSocket(self) -> None: ...
    def emit(self, record) -> None: ...
    def handleError(self, record) -> None: ...
    def makePickle(self, record) -> bytes: ...
    def makeSocket(self, timeout = ...) -> socket.socket: ...
    def send(self, s) -> None: ...

class SysLogHandler(logging.Handler):
    LOG_ALERT: int
    LOG_AUTH: int
    LOG_AUTHPRIV: int
    LOG_CRIT: int
    LOG_CRON: int
    LOG_DAEMON: int
    LOG_DEBUG: int
    LOG_EMERG: int
    LOG_ERR: int
    LOG_FTP: int
    LOG_INFO: int
    LOG_KERN: int
    LOG_LOCAL0: int
    LOG_LOCAL1: int
    LOG_LOCAL2: int
    LOG_LOCAL3: int
    LOG_LOCAL4: int
    LOG_LOCAL5: int
    LOG_LOCAL6: int
    LOG_LOCAL7: int
    LOG_LPR: int
    LOG_MAIL: int
    LOG_NEWS: int
    LOG_NOTICE: int
    LOG_SYSLOG: int
    LOG_USER: int
    LOG_UUCP: int
    LOG_WARNING: int
    __doc__: str
    address: Any
    append_nul: bool
    facility: Any
    facility_names: Dict[str, int]
    ident: str
    priority_map: Dict[str, str]
    priority_names: Dict[str, int]
    socket: Optional[socket.socket]
    socktype: Any
    unixsocket: bool
    def __init__(self, address = ..., facility = ..., socktype = ...) -> None: ...
    def _connect_unixsocket(self, address) -> None: ...
    def close(self) -> None: ...
    def emit(self, record) -> None: ...
    def encodePriority(self, facility, priority) -> Any: ...
    def mapPriority(self, levelName) -> str: ...

class TimedRotatingFileHandler(BaseRotatingHandler):
    __doc__: str
    atTime: Any
    backupCount: Any
    dayOfWeek: int
    encoding: Any
    extMatch: re.Pattern[str]
    interval: Any
    mode: str
    namer: None
    rolloverAt: Any
    rotator: None
    stream: Optional[io.TextIOWrapper]
    suffix: str
    utc: Any
    when: Any
    def __init__(self, filename, when = ..., interval = ..., backupCount = ..., encoding = ..., delay = ..., utc = ..., atTime = ...) -> None: ...
    def computeRollover(self, currentTime) -> Any: ...
    def doRollover(self) -> None: ...
    def getFilesToDelete(self) -> List[str]: ...
    def shouldRollover(self, record) -> int: ...

class WatchedFileHandler(logging.FileHandler):
    __doc__: str
    dev: Union[float, int]
    ino: Union[float, int]
    stream: io.TextIOWrapper
    def __init__(self, filename, mode = ..., encoding = ..., delay = ...) -> None: ...
    def _statstream(self) -> None: ...
    def emit(self, record) -> None: ...
    def reopenIfNeeded(self) -> None: ...
