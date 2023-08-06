from datetime import datetime
from enum import Enum
from typing import Dict, List, Set

from marshmallow import Schema, fields, post_load
from tqdm.asyncio import tqdm, tqdm_asyncio

from openfabric_pysdk.utility import SchemaUtil


#######################################################
#  Ray Status
#######################################################
class RayStatus(Enum):
    QUEUED = 'queued',
    PENDING = 'pending',
    COMPLETED = 'completed',
    RUNNING = 'running',
    CANCELED = 'canceled',
    REMOVED = 'removed',
    UNKNOWN = 'unknown',
    FAILED = 'failed'

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.name


#######################################################
#  Baar
#######################################################
class Bar:
    percent: str = 0
    remaining: str = 'NaN'


class BarSchema(Schema):
    percent = fields.String(allow_none=True)
    remaining = fields.String(allow_none=True)

    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(Bar(), data)


#######################################################
#  Message
#######################################################
class MessageType(Enum):
    INFO = 'info',
    ERROR = 'error',
    WARNING = 'warning'

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.name


class Message:
    type: MessageType = 0
    content: str = None
    created_at: datetime = datetime.now()

    # ------------------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return self.type == other.type and self.content == other.content

    def __key(self):
        return self.type, self.content

    def __hash__(self):
        return hash(self.__key())


class MessageSchema(Schema):
    type = fields.Enum(MessageType)
    content = fields.String()
    created_at = fields.DateTime()

    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(Message(), data)


#######################################################
#  Ray
#######################################################
class RaySchema(Schema):
    sid = fields.String()
    uid = fields.String()
    qid = fields.String()
    bars = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(BarSchema),
        allow_none=True
    )
    messages = fields.Nested(MessageSchema(many=True))
    status = fields.Enum(RayStatus)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(Ray(None), data)


class Ray:
    uid: str = None
    sid: str = None
    qid: str = None
    finished: bool = None
    bars: Dict[str, Bar] = None
    status: RayStatus = None
    created_at: datetime = None
    updated_at: datetime = None
    messages: Set[Message] = None
    __tqdms: Dict[str, tqdm_asyncio] = None

    # ------------------------------------------------------------------------
    def __init__(self, qid):
        self.__tqdms = dict()
        self.qid = qid
        self.bars = dict(default=Bar())
        self.finished = False
        self.status = RayStatus.UNKNOWN
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.messages = set()

    # ------------------------------------------------------------------------
    def progress(self, name='default', step=1, total=100) -> tqdm_asyncio:
        if self.__tqdms.get(name) is None:
            self.__tqdms[name] = tqdm(total=total)
        tqdm_bar = self.__tqdms[name]
        # --
        bar = self.bars.get(name, Bar())
        self.bars[name] = bar
        f_dict = tqdm_bar.format_dict
        rate = f_dict.get("rate")
        total = tqdm_bar.total
        n = tqdm_bar.n
        remaining = (total - n) / rate if rate and total else 0
        bar.remaining = max(0, remaining)
        bar.percent = n
        # --
        tqdm_bar.update(step)
        return tqdm_bar

    # ------------------------------------------------------------------------
    def message(self, message_type: MessageType, content: str):
        message = Message()
        message.type = message_type
        message.content = content
        self.messages.add(message)

    # ------------------------------------------------------------------------
    def clear_messages(self):
        self.messages.clear()

    # ------------------------------------------------------------------------
    def tqdms(self):
        return self.__tqdms


#######################################################
#  Execution State
#######################################################
class StateStatus(Enum):
    UNKNOWN = 'unknown',
    STARTING = 'starting',
    RUNNING = 'running',
    CRASHED = 'crashed',
    PENDING_CONFIG = 'pending_config'

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.name


class State:
    status: StateStatus = None
    started_at: datetime = None

    # ------------------------------------------------------------------------
    def __init__(self):
        self.status = StateStatus.UNKNOWN
        self.started_at = datetime.now()


class StateSchema(Schema):
    status = fields.Enum(StateStatus)
    started_at = fields.DateTime()
