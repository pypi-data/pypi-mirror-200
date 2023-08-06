from typing import Dict, List
from datetime import datetime, timedelta, timezone

from gm.csdk.c_sdk import gmi_get_ext_errormsg
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.pyext._message import (
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
    ScalarMapContainer,
)


def invalid_status(status: int) -> bool:
    if status == 0:
        return False
    gmi_get_ext_errormsg()
    return True


def timestamp_to_str(timestamp):
    # type: (Timestamp) -> str
    begin = datetime(1970, 1, 1, 8, 0, tzinfo=PRC_TZ)
    date = begin + timedelta(seconds=timestamp.seconds+timestamp.nanos)
    return date.strftime("%Y-%m-%d")


# 需要四舍五入的字段
_round_fields = {
    ("Tick", "open"),
    ("Tick", "high"),
    ("Tick", "low"),
    ("Tick", "price"),
    ("Quote", "bid_p"),
    ("Quote", "ask_p"),
    ("Bar", "open"),
    ("Bar", "high"),
    ("Bar", "low"),
    ("Bar", "close"),
    ("Bar", "pre_close"),
    ("Order", "price"),
    ("ExecRpt", "price"),
    ("Position", "vwap_diluted"),
    ("Position", "vwap"),
    ("Position", "vwap_open"),
    ("Position", "price"),
}


PRC_TZ = timezone(timedelta(hours=8), name="Asia/Shanghai")  # 东八区, 北京时间
TIMESTAMP_NONE = Timestamp()


def timestamp_to_datetime(ts):
    # type: (float) -> datetime
    begin = datetime(1970, 1, 1, 8, 0, tzinfo=PRC_TZ)
    return begin + timedelta(seconds=ts)


def pb_to_dict(pb, convert_to_date_str=True, include_default_value=True):
    # type: (Message, bool, bool) -> Dict
    def convert(pb, field, value):
        if isinstance(value, Timestamp):
            if value == TIMESTAMP_NONE:
                return None
            d = timestamp_to_datetime(value.seconds + value.nanos / 1e9)
            if convert_to_date_str:
                d = d.strftime("%Y-%m-%d")
            return d
        elif isinstance(value, Message):
            return pb_to_dict(value,
                              convert_to_date_str=convert_to_date_str,
                              include_default_value=include_default_value,
                              )
        if isinstance(value, ScalarMapContainer):
            return dict(value)
        elif isinstance(value, RepeatedScalarContainer):
            return [i for i in value]
        elif isinstance(value, RepeatedCompositeContainer):
            return [convert(pb, field, i) for i in value]
        elif isinstance(value, float) and (pb.DESCRIPTOR.name, field.name) in _round_fields:
            return round(value, 4)
        else:
            return value
    result = {}
    if include_default_value:
        for field in pb.DESCRIPTOR.fields:
            value = getattr(pb, field.name)
            result[field.name] = convert(pb, field, value)
    else:
        for field, value in pb.ListFields():
            result[field.name] = convert(pb, field, value)
    return result


def unfold_field(dictory, field):
    # type: (Dict, str) -> None
    """展开字典内嵌套的字段"""
    if field in dictory:
        dictory.update(dictory.pop(field))


def rename_field(dictory, after_field, before_field):
    # type: (Dict, str, str) -> None
    """重命名字典内的字段"""
    if before_field in dictory:
        dictory[after_field] = dictory.pop(before_field)


def filter_field(dictory, fields):
    # type: (Dict, List[str]|str) -> Dict
    """过滤字典内的字段, 只保留 fields 内的字段"""
    if not fields:
        return dictory
    if isinstance(fields, str):
        fields = fields.split(',')
    fields = [field.strip() for field in fields]
    res = {}
    for field in fields:
        if field in dictory:
            res[field] = dictory[field]
    return res


def param_convert_iter_to_str(values):
    # type: (List|str) -> str|None
    """参数转换"""
    if not values:
        return None
    if isinstance(values, str):
        values = values.split(',')
    values = [str(value).strip() for value in values]
    return ','.join(values)


def param_convert_iter_to_list(values):
    # type: (List[str]|str) -> str|None
    """参数转换"""
    if not values:
        return None
    if isinstance(values, str):
        values = values.split(',')
    values = [value.strip() for value in values]
    return values


def param_convert_date(date):
    # type: (str|datetime) -> str|None
    """参数转换, 日期类型"""
    if not date:
        return None
    if isinstance(date, str):
        return date
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    raise ValueError("错误日期格式")
