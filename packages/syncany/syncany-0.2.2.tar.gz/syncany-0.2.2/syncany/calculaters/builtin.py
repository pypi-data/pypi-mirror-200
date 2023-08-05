# -*- coding: utf-8 -*-
# 18/8/15
# create by: snower

import struct
import math
import hashlib
import datetime
import uuid

import pytz
import json
import re
from ..utils import get_timezone, sorted_by_keys
from .calculater import Calculater, TypeFormatCalculater, TypingCalculater, MathematicalCalculater
try:
    from bson.objectid import ObjectId
except ImportError:
    ObjectId = None


class TypeCalculater(TypingCalculater):
    def typing_calculate(self, value, args):
        if value is None:
            return "null"
        if value is True or value is False:
            return "bool"
        if isinstance(value, dict):
            return "map"
        if isinstance(value, (list, tuple, set)):
            return "array"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "str"
        if ObjectId and isinstance(value, ObjectId):
            return "objectid"
        if isinstance(value, uuid.UUID):
            return "uuid"
        if isinstance(value, datetime.datetime):
            return "datetime"
        if isinstance(value, datetime.date):
            return "date"
        if isinstance(value, datetime.time):
            return "time"
        return type(value).__module__ + "." + type(value).__name__


class MakeCalculater(Calculater):
    def calculate(self, *args):
        return args


class IsNullCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return True
        if isinstance(data, list):
            for value in data:
                if value is not None:
                    return False
            return True
        return data is None


class IsIntCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, int):
                    return False
            return default_result
        return isinstance(data, int)


class IsFloatCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, float):
                    return False
            return default_result
        return isinstance(data, float)


class IsNumberCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, (int, float)):
                    return False
            return default_result
        return isinstance(data, (int, float))


class IsStringCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, str):
                    return False
            return default_result
        return isinstance(data, str)


class IsBytesCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, bytes):
                    return False
            return default_result
        return isinstance(data, bytes)


class IsBooleanCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, bool):
                    return False
            return default_result
        return isinstance(data, bool)


class IsArrayCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        return isinstance(data, list)


class IsMapCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, dict):
                    return False
            return default_result
        return isinstance(data, dict)


class IsObjectIdCalculater(Calculater):
    def calculate(self, data=None):
        if ObjectId is None:
            raise ImportError(u"bson required")

        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, ObjectId):
                    return False
            return default_result
        return isinstance(data, ObjectId)


class IsUUIDCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, uuid.UUID):
                    return False
            return default_result
        return isinstance(data, uuid.UUID)


class IsDateTimeCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, datetime.datetime):
                    return False
            return default_result
        return isinstance(data, datetime.datetime)


class IsDateCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, datetime.date):
                    return False
            return default_result
        return isinstance(data, datetime.date)


class IsTimeCalculater(Calculater):
    def calculate(self, data=None):
        if data is None:
            return False
        if isinstance(data, list):
            default_result = True
            for value in data:
                if value is None:
                    default_result = False
                    continue
                if not isinstance(value, datetime.time):
                    return False
            return default_result
        return isinstance(data, datetime.time)


class IsCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        return left_value is right_value


class RangeCalculater(Calculater):
    def calculate(self, *args):
        return range(*args)


class AddCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        if left_value is None:
            return 0 if right_value is None else right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        return left_value + right_value


class SubCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        if left_value is None:
            return 0 if right_value is None else -right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        return left_value - right_value


class MulCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        if left_value is None:
            return 0 if right_value is None else right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        return left_value * right_value


class DivCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        if left_value is None:
            return 0 if right_value is None else -right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        if right_value == 0:
            return 0
        return left_value / right_value


class ModCalculater(MathematicalCalculater):
    def mathematical_calculate(self, left_value, right_value, args):
        if left_value is None:
            return 0 if right_value is None else right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        if right_value == 0:
            return 0
        return left_value % right_value


class BitCalculater(MathematicalCalculater):
    def get_left_datas(self, args):
        return args[1] if len(args) >= 2 else None

    def get_right_datas(self, args):
        return args[2] if len(args) >= 3 else None

    def get_args_datas(self, args):
        return args[3:]

    def mathematical_calculate(self, left_value, right_value, args):
        if args[0] == "~":
            if left_value is None:
                return 0
            return ~ left_value

        if left_value is None:
            return 0 if right_value is None else right_value
        if right_value is None:
            return 0 if left_value is None else left_value
        if right_value == 0:
            return 0
        if args[0] == ">>":
            return left_value >> right_value
        if args[0] == "<<":
            return left_value << right_value
        if args[0] == "&":
            return left_value & right_value
        if args[0] == "|":
            return left_value | right_value
        if args[0] == "^":
            return left_value ^ right_value
        return None


class NegCalculater(TypingCalculater):
    def typing_calculate(self, value, args):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return -value
        if isinstance(value, (str, bytes, list, tuple)):
            return value[::-1]
        if isinstance(value, bool):
            return True if value is False else False
        return value


class NotCalculater(TypingCalculater):
    def typing_calculate(self, value, args):
        return not value


class SubstringCalculater(TypingCalculater):
    def typing_calculate(self, value, args):
        if not args:
            return ""
        if value is None:
            return ""
        if len(args) == 1:
            return value
        if len(args) == 2:
            return value[args[1]:]
        if len(args) == 3:
            return value[args[1]: args[2]]
        return value[args[1]: args[2]: args[3]]


class SplitCalculater(TypingCalculater):
    def typing_calculate(self, value, args):
        if value is None:
            return ""
        if isinstance(value, str):
            return value.split(args[1])
        if isinstance(value, bytes):
            return value.decode("utf-8").split(args[1])
        return str(value).split(args[1])


class JoinCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return ""
        if args[0] is None:
            return ""
        return str(args[1]).join([str(value) for value in args[0]])


class NowCalculater(Calculater):
    TIMEDELTAS = {"Y": 365 * 24 * 60 * 60, "m": 30 * 24 * 60 * 60, "d": 24 * 60 * 60, "H": 60 * 60, "M": 60, "S": 1}

    def calculate(self, *args):
        if not args:
            return datetime.datetime.now(tz=get_timezone())

        if isinstance(args[0], int):
            return self.at(datetime.datetime.now(tz=get_timezone()), *tuple(args))
        if not args[0]:
            return datetime.datetime.now(tz=get_timezone())
        if args[0][0] in ("-", "+") and args[0][-1] in ("Y", "m", "d", "H", "M", "S"):
            try:
                seconds = int(args[0][1:-1]) * self.TIMEDELTAS[args[0][-1]]
            except:
                if len(args) >= 2:
                    return self.at(datetime.datetime.now(tz=pytz.timezone(args[0])), *tuple(args[1:]))
                return datetime.datetime.now(tz=pytz.timezone(args[0]))

            if len(args) >= 3:
                if isinstance(args[1], int):
                    now = self.at(datetime.datetime.now(), *tuple(args[1:]))
                else:
                    now = self.at(datetime.datetime.now(tz=pytz.timezone(args[1])), *tuple(args[2:]))
            elif len(args) >= 2:
                if isinstance(args[1], int):
                    now = self.at(datetime.datetime.now(tz=get_timezone()), *tuple(args[1:]))
                else:
                    now = datetime.datetime.now(tz=pytz.timezone(args[1]))
            else:
                now = datetime.datetime.now(tz=get_timezone())

            if args[0][0] == "-":
                return now - datetime.timedelta(seconds=seconds)
            return now + datetime.timedelta(seconds=seconds)
        if len(args) >= 2:
            return self.at(datetime.datetime.now(tz=pytz.timezone(args[0])), *tuple(args[1:]))
        return datetime.datetime.now(tz=pytz.timezone(args[0]))

    def at(self, dt, hour=0, minute=0, second=0, microsecond=0):
        return datetime.datetime(dt.year, dt.month, dt.day,
                                 hour if hour is not None else dt.hour, minute if minute is not None else dt.minute,
                                 second if second is not None else dt.second, microsecond if microsecond is not None else dt.microsecond,
                                 tzinfo=dt.tzinfo)



class EmptyCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return True
        if isinstance(args[0], list):
            for value in args[0]:
                if value is None:
                    continue
                if not bool(value):
                    return False
            return True
        if args[0] is None:
            return True
        return bool(args[0])


class ContainCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return True
        if isinstance(args[0], list):
            default_result = True
            for value in args[0]:
                if value is None:
                    default_result = False
                    continue
                if args[1] not in value:
                    return False
            return default_result
        if args[0] is None:
            return False
        return args[1] in args[0]


class GtCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return False
        if left_value and not right_value:
            return True
        if not left_value and right_value:
            return False
        return left_value > right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class GteCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return True
        if left_value and not right_value:
            return True
        if not left_value and right_value:
            return False
        return left_value >= right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class LtCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return False
        if left_value and not right_value:
            return False
        if not left_value and right_value:
            return True
        return left_value < right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class LteCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return True
        if left_value and not right_value:
            return False
        if not left_value and right_value:
            return True
        return left_value <= right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class EqCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return True
        if left_value and not right_value:
            return False
        if not left_value and right_value:
            return False
        return left_value == right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class NeqCalculater(TypeFormatCalculater):
    def cmp(self, left_value, right_value):
        if not left_value and not right_value:
            return False
        if left_value and not right_value:
            return True
        if not left_value and right_value:
            return True
        return left_value != right_value

    def calculate(self, *args):
        if not args:
            return False
        if isinstance(args[0], list):
            return False

        self.type_cls = None
        left_value, right_value = self.format_type(args[0]), None
        for value in args[1:]:
            right_value = self.format_type(value)
            if not self.cmp(left_value, right_value):
                return False
            left_value, right_value = right_value, None
        return True


class AndCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None
        result = None
        for value in args:
            if value is None:
                continue
            result = value if result is None else (result and value)
        return result


class OrCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None
        result = None
        for value in args:
            if value is None:
                continue
            result = value if result is None else (result or value)
        return result


class InCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return False
        try:
            result = args[0]
            for i in range(1, len(args)):
                if result not in args[i]:
                    return False
        except:
            return False
        return True


class MaxCalculater(TypeFormatCalculater):
    def max(self, values):
        result = None
        for value in values:
            if value is None:
                continue
            if result is None:
                result = self.format_type(value)
                continue
            value = self.format_type(value)
            if value > result:
                result = value
        return result

    def calculate(self, *args):
        self.type_cls = None
        if not args:
            return None

        if not isinstance(args[0], list):
            if len(args) > 1:
                return self.max(args)
            return args[0]

        if len(args) == 2 and isinstance(args[1], str):
            if len(args[0]) == 1:
                return args[0][0]

            datas = {}
            for d in args[0]:
                if isinstance(d, dict) and args[1] in d:
                    datas[d[args[1]]] = d
            if not datas:
                return None
            max_key = max(*tuple(datas.keys()))
            return datas[max_key]

        max_key_value = max(*tuple(args[0]))
        if len(args) >= 2:
            if isinstance(args[1], list):
                try:
                    return args[1][args[0].index(max_key_value)]
                except:
                    return None

            if isinstance(args[1], dict):
                return args[1].get(max_key_value)
            return self.max([max_key_value] + list(args[1:]))
        return max_key_value


class MinCalculater(TypeFormatCalculater):
    def min(self, values):
        result = None
        for value in values:
            if value is None:
                continue
            if result is None:
                result = self.format_type(value)
                continue
            value = self.format_type(value)
            if value < result:
                result = value
        return result

    def calculate(self, *args):
        self.type_cls = None
        if not args:
            return None

        if not isinstance(args[0], list):
            if len(args) >= 1:
                return self.min(args)
            return args[0]

        if len(args) == 2 and isinstance(args[1], str):
            if len(args[0]) == 1:
                return args[0][0]

            datas = {}
            for d in args[0]:
                if isinstance(d, dict) and args[1] in d:
                    datas[d[args[1]]] = d
            if not datas:
                return None
            min_key = min(*tuple(datas.keys()))
            return datas[min_key]

        min_key_value = min(*tuple(args[0]))
        if len(args) >= 2:
            if isinstance(args[1], list):
                try:
                    return args[1][args[0].index(min_key_value)]
                except:
                    return None

            if isinstance(args[1], dict):
                return args[1].get(min_key_value)
            return self.min([min_key_value] + list(args[1:]))
        return min_key_value


class LenCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return 0

        if isinstance(args[0], list):
            return [len(value) for value in args[0]]
        return len(args[0])


class AbsCalculater(Calculater):
    def abs(self, arg):
        if isinstance(arg, (int, float)):
            return abs(arg)
        if isinstance(arg, str):
            try:

                return abs(float(arg) if "." in arg else int(arg))
            except:
                return 0
        if isinstance(arg, list):
            return [self.abs(child_arg) for child_arg in arg]
        if isinstance(arg, dict):
            return {child_key: self.abs(child_arg) for child_key, child_arg in arg.items()}
        return 0

    def calculate(self, *args):
        if not args:
            return 0
        return self.abs(args[0])


class IndexCalculater(Calculater):
    def calculate(self, *args):
        if not args or len(args) < 2:
            return None

        if isinstance(args[0], list):
            for data in args[0]:
                if len(args) >= 3:
                    if not isinstance(data, dict) or args[2] not in data:
                        continue
                    if data[args[2]] == args[1]:
                        return data
                elif data == args[1]:
                    return data

            if isinstance(args[1], (int, float)):
                return args[0][int(args[1])] if len(args[0]) < args[1] else None

        elif isinstance(args[0], dict):
            if len(args) >= 3:
                if args[2] not in args[0]:
                    return None

                if args[0][args[2]] == args[1]:
                    return args[0][args[2]]

            if args[1] in args[0]:
                return args[0][args[1]]

        return None


class FilterCalculater(Calculater):
    def calculate(self, *args):
        if not args or len(args) < 2:
            return []

        result = []
        if isinstance(args[0], list):
            for data in args[0]:
                if len(args) >= 3:
                    if not isinstance(data, dict) or args[2] not in data:
                        continue
                    if data[args[2]] == args[1]:
                        result.append(data)
                elif data == args[1]:
                    result.append(data)

        elif isinstance(args[0], dict):
            if len(args) >= 3:
                if args[2] in args[0] and args[0][args[2]] == args[1]:
                    result.append(args[0])
            elif args[1] == args[0]:
                result.append(args[0])

        elif args[1] == args[0]:
            result.append(args[0])
        return result


class SumCalculater(Calculater):
    def add(self, v):
        if isinstance(v, (int, float)):
            return v
        elif v is True:
            return 1
        elif isinstance(v, str):
            try:
                return float(v)
            except:
                pass
        return 0

    def calculate(self, *args):
        if not args:
            return 0

        result = 0
        if isinstance(args[0], list):
            for data in args[0]:
                if isinstance(data, dict) and len(args) >= 2:
                    if args[1] not in data:
                        continue
                    result += self.add(data[args[1]])
                else:
                    result += self.add(data)
        elif isinstance(args[0], dict):
            if len(args) >= 2:
                if args[1] in args[0]:
                    result += self.add(args[0][args[1]])
            else:
                result += self.add(args[0])
        else:
            result += self.add(args[0])
        return result


class SortCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None

        if not isinstance(args[0], list):
            return args[0]
        if len(args) == 2 and not isinstance(args[1], bool):
            return sorted_by_keys(args[0], keys=args[1], reverse=False)

        keys = args[2] if len(args) >= 3 else None
        return sorted_by_keys(args[0], keys=keys,
                              reverse=True if len(args) >= 2 and args[1] else False)


class StringCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return ''

        func_name = self.name[8:]
        if isinstance(args[0], str):
            if func_name == "contains":
                for cs in args[1:]:
                    if not isinstance(cs, str) or cs not in args[0]:
                        return False
                return True
            if func_name == "join":
                return str(args[0]).join([str(value) for value in args[1]])

            if hasattr(args[0], func_name):
                try:
                    return getattr(args[0], func_name)(*tuple(args[1:]))
                except:
                    return ''
        return ''


class ArrayCalculater(Calculater):
    def to_map(self, args):
        if len(args) == 2 and isinstance(args[0], list) and isinstance(args[1], str):
            result = {}
            for v in args[0]:
                if not isinstance(v, dict) or args[1] not in v:
                    continue
                vk = v[args[1]]
                if vk in result:
                    if not isinstance(result[vk], list):
                        result[vk] = [result[vk], v]
                    else:
                        result[vk].append(v)
                else:
                    result[vk] = v
            return result

        if len(args) == 1 and isinstance(args[0], list):
            if len(args[0]) == 1 and isinstance(args[0][0], dict):
                return args[0]
            return {"index" + str(i): args[0][i] for i in range(len(args[0]))}

        if isinstance(args[0], dict):
            if len(args) == 2 and isinstance(args[1], str):
                if args[1] in args[0]:
                    return {args[0][args[1]]: args[0]}
                return {}
            return args[0]
        return {}

    def flat(self, args):
        if len(args) == 1:
            if isinstance(args[0], list):
                result = []
                for d in args[0]:
                    if isinstance(d, list):
                        result.extend(d)
                    else:
                        result.append(d)
                return result
            return [args[0]]

        result = []
        for d in args:
            if isinstance(d, list):
                result.extend(d)
            else:
                result.append(d)
        return result

    def calculate(self, *args):
        if not args:
            return None

        func_name = self.name[7:]
        if func_name == "map":
            return self.to_map(args)
        if func_name == "flat":
            return self.flat(args)
        data = args[0] if isinstance(args[0], list) else [args[0]]
        if not data:
            return None

        if func_name == "contains":
            return args[1] in data
        if func_name == "sum":
            return sum(data)
        if func_name == "max":
            return max(*tuple(data))
        if func_name == "min":
            return max(*tuple(data))
        if func_name == "avg":
            return sum(data) / len(data)
        if func_name == "join":
            return str(args[1]).join([str(value) for value in data])
        if func_name == "first":
            return data[0]
        if func_name == "last":
            return data[-1]
        if func_name == "gt":
            return [value for value in data if value is not None and value > args[1]]
        if func_name == "gte":
            return [value for value in data if value is not None and value >= args[1]]
        if func_name == "lt":
            return [value for value in data if value is not None and value < args[1]]
        if func_name == "lte":
            return [value for value in data if value is not None and value <= args[1]]
        if func_name == "eq":
            return [value for value in data if value is not None and value == args[1]]
        if func_name == "neq":
            return [value for value in data if value is not None and value != args[1]]
        if func_name == "slice":
            if len(args) == 1:
                return data[:]
            if len(args) == 2:
                return data[args[1]:]
            if len(args) == 3:
                return data[args[1]: args[2]]
            return data[args[1]: args[2]: args[3]]

        if hasattr(data, func_name):
            try:
                result = getattr(data, func_name)(*tuple(args[1:]))
                if func_name in ("append", "clear", "extend", "insert", "reverse", "sort"):
                    return data
                return result
            except:
                return None
        return None


class MapCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None

        func_name = self.name[5:]
        if isinstance(args[0], dict) and hasattr(args[0], func_name):
            try:
                result = getattr(args[0], func_name)(*tuple(args[1:]))
                if func_name in ("clear", "update"):
                    return args[0]
                if func_name == "contains":
                    for cs in args[1:]:
                        if cs not in args[0]:
                            return False
                    return True
                return result
            except:
                return None
        return None


class MathCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return 0

        func_name = self.name[6:]
        if hasattr(math, func_name):
            if isinstance(args[0], list):
                result = []
                for value in args[0]:
                    try:
                        result.append(getattr(math, func_name)(float(value) if not isinstance(args[0], (int, float)) else value,
                                                               *tuple(args[1:])))
                    except:
                        result.append(0)
                return result

            try:
                return getattr(math, func_name)(float(args[0]) if not isinstance(args[0], (int, float)) else args[0],
                                                *tuple(args[1:]))
            except:
                return 0
        return 0


class HashCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None

        b = b''
        for arg in args:
            b += (arg if isinstance(arg, bytes) else str(arg).encode("utf-8"))

        if self.name == "hash::md5":
            return hashlib.md5(b).hexdigest()
        if self.name == "hash::sha1":
            return hashlib.sha1(b).hexdigest()
        if self.name == "hash::sha256":
            return hashlib.sha256(b).hexdigest()
        if self.name == "hash::sha384":
            return hashlib.sha384(b).hexdigest()
        if self.name == "hash::sha512":
            return hashlib.sha512(b).hexdigest()
        return None


class JsonCalculater(Calculater):
    def calculate(self, *args):
        if self.name == "json::encode":
            return self.encode(args)
        if self.name == "json::decode":
            return self.decode(args)
        return None

    def encode(self, args):
        if not args:
            return None
        try:
            return json.dumps(args[0], default=str, ensure_ascii=False)
        except:
            return None

    def decode(self, args):
        if not args:
            return None
        try:
            return json.loads(args[0])
        except:
            return None


class StructCalculater(Calculater):
    def calculate(self, *args):
        if self.name == "struct::pack":
            return self.pack(args)
        if self.name == "json::unpack":
            return self.unpack(args)
        return None

    def pack(self, args):
        if len(args) < 2:
            return None
        try:
            return struct.pack(args[0], args[1])
        except:
            return None

    def unpack(self, args):
        if len(args) < 2:
            return None
        try:
            return list(struct.unpack(args[0], args[1]))
        except:
            return None


class ReCalculater(Calculater):
    def calculate(self, *args):
        if not args:
            return None

        if isinstance(args[0], re.Match):
            try:
                return getattr(args[0], self.name[4:])(*tuple(args[1:]))
            except:
                return None
        if not isinstance(args[0], str) or not args[0]:
            return None

        if args[0] == "/":
            index = args[0].rindex("/")
            pattern, flags = args[1: index], re.DOTALL
            for fc in args[index + 1:]:
                flags |= re.RegexFlag.__members__.get(fc.upper(), 0)
        else:
            pattern, flags = args[0], re.DOTALL
        r = re.compile(pattern, flags)
        try:
            return getattr(r, self.name[4:])(args[1], *tuple(args[2:]))
        except:
            return None
