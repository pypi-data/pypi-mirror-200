
from fintekkers.models.util.local_date_pb2 import LocalDateProto
from fintekkers.models.util.local_timestamp_pb2 import LocalTimestampProto
from fintekkers.models.util.uuid_pb2 import UUIDProto
from fintekkers.models.transaction.transaction_type_pb2 import TransactionTypeProto
from fintekkers.models.security.identifier.identifier_pb2 import IdentifierProto

from fintekkers.wrappers.models.util.fintekkers_uuid import FintekkersUuid
from fintekkers.wrappers.models.security import Identifier
from fintekkers.wrappers.models.transaction import TransactionType

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import date, datetime
import time
from pytz import timezone

from uuid import UUID, uuid4

class ProtoEnum:
    def __init__(self, enum_name:str, enum_value:int):
        self.enum_name:str = enum_name
        self.enum_value:int = enum_value

class ProtoSerializationUtil:
    @staticmethod
    def serialize(obj):
        if isinstance(obj, UUID):
            return UUIDProto(raw_uuid=obj.bytes)
        if type(obj) is date:
            return LocalDateProto(year=obj.year, month=obj.month, day=obj.day)
        if isinstance(obj, datetime):
            seconds_in_float:float = time.mktime(obj.timetuple())
            timestamp = Timestamp(seconds=int(seconds_in_float), 
                nanos=int(obj.microsecond/1000))

            time_zone = obj.timetz().tzinfo.zone if obj.timetz().tzinfo is not None else "America/New_York"
            return LocalTimestampProto(timestamp=timestamp, time_zone=time_zone)
        if isinstance(obj, Identifier) or isinstance(obj, TransactionType):
            return obj.proto

        return obj
        

    @staticmethod
    def deserialize(obj):
        if isinstance(obj, UUIDProto):
            return FintekkersUuid.from_bytes(bytes=obj.raw_uuid)
        if isinstance(obj, LocalDateProto):
            return date(year=obj.year, month=obj.month, day=obj.day)
        if isinstance(obj, LocalTimestampProto):
            return datetime.fromtimestamp(obj.timestamp.seconds, timezone(obj.time_zone))
        if isinstance(obj, IdentifierProto):
            return Identifier(obj)
        if hasattr(obj, 'enum_name') and getattr(obj, 'enum_name') == "TRANSACTION_TYPE":
            return TransactionType(obj.enum_value)
        
        return obj

if __name__ == "__main__":
    serialized:UUIDProto = ProtoSerializationUtil.serialize(uuid4())
    assert isinstance(serialized, UUIDProto)
    deserialized:UUID = ProtoSerializationUtil.deserialize(serialized)
    assert isinstance(deserialized, UUID)

    serialized:LocalDateProto = ProtoSerializationUtil.serialize(date.today())
    assert isinstance(serialized, LocalDateProto)
    deserialized:date = ProtoSerializationUtil.deserialize(serialized)
    assert isinstance(deserialized, date)

    obj = datetime.today().replace(tzinfo=timezone("America/New_York"))
    serialized:LocalTimestampProto = ProtoSerializationUtil.serialize(obj)
    assert isinstance(serialized, LocalTimestampProto)
    deserialized:datetime = ProtoSerializationUtil.deserialize(serialized)
    assert isinstance(deserialized, datetime)
