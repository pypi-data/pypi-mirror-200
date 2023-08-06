from fintekkers.models.position.field_pb2 import FieldProto
from fintekkers.models.position.measure_pb2 import MeasureProto
from fintekkers.models.position.position_pb2 import PositionProto
from fintekkers.models.position.position_util_pb2 import FieldMapEntry, MeasureMapEntry

from fintekkers.models.portfolio.portfolio_pb2 import PortfolioProto
from fintekkers.models.security.security_pb2 import SecurityProto
from fintekkers.models.security.identifier.identifier_pb2 import IdentifierProto

from fintekkers.models.util.local_date_pb2 import LocalDateProto
from fintekkers.models.util.uuid_pb2 import UUIDProto

from fintekkers.wrappers.models.util.serialization import ProtoSerializationUtil, ProtoEnum

from google.protobuf import wrappers_pb2 as wrappers
from google.protobuf.any_pb2 import Any

from decimal import Decimal

class Position():
    positionProto:PositionProto

    def __init__(self, positionProto:PositionProto) -> None:
        self.positionProto = positionProto

    def get_field(self, field_to_get:FieldProto):
        tmp_field:FieldMapEntry
        for tmp_field in self.positionProto.fields:
            if tmp_field.field == field_to_get:
                return ProtoSerializationUtil.deserialize(Position.unpack_field(tmp_field))

        raise ValueError("Could not find field in position")
        

    def get_measure(self, measure_to_get:MeasureProto):
        tmp_measure:MeasureMapEntry
        for tmp_measure in self.positionProto.measures:
            if tmp_measure.measure == measure_to_get:
                return ProtoSerializationUtil.deserialize(Position.unpack_measure(tmp_measure))


        raise ValueError("Could not find measure in position")

    def get_field_display(self, field_to_get:FieldProto):
        return self.get_field(field_to_get=field_to_get).__str__()

    def get_measures(self):
        return self.positionProto.measures

    def get_fields(self):
        return self.positionProto.fields

    @staticmethod
    def wrap_string_to_any(my_string:str):
        my_any = Any()
        my_any.Pack(wrappers.StringValue(value=my_string))
        return my_any

    # @staticmethod
    # def unwrap_string_from_any(msg):
    #     any:Any = Any()
    #     any.Unpack(msg)
    #     return any.value


    @staticmethod
    def pack_field(field_to_pack):
        if field_to_pack.__class__ == LocalDateProto:
            my_any = Any()
            my_any.Pack(field_to_pack)
            return my_any

        # if field_to_unpack.field == FieldProto.PORTFOLIO_ID:
        #     return UUIDProto.FromString(field_to_unpack.field_value_packed.value)
        # if field_to_unpack.field == FieldProto.TRADE_DATE or field_to_unpack.field == FieldProto.SETTLEMENT_DATE \
        #     or field_to_unpack.field == FieldProto.TAX_LOT_OPEN_DATE\
        #         or field_to_unpack.field == FieldProto.TAX_LOT_CLOSE_DATE:
        #     return LocalDateProto.FromString(field_to_unpack.field_value_packed.value)
        # if field_to_unpack.field == FieldProto.IDENTIFIER:
        #     return IdentifierProto.FromString(field_to_unpack.field_value_packed.value)
        # if field_to_unpack.field == FieldProto.TRANSACTION_TYPE:
        #     name:str = FieldProto.DESCRIPTOR.values_by_number[field_to_unpack.field].name
        #     return ProtoEnum(name, field_to_unpack.enum_value)
        # if field_to_unpack.field == FieldProto.PORTFOLIO_NAME or field_to_unpack.field == FieldProto.SECURITY_DESCRIPTION \
        #     or field_to_unpack.field == FieldProto.PRODUCT_TYPE:
        #     return wrappers.StringValue.FromString(field_to_unpack.field_value_packed.value).value
        # if field_to_unpack.field == FieldProto.PORTFOLIO:
        #     return PortfolioProto.FromString(field_to_unpack.field_value_packed.value)
        # if field_to_unpack.field == FieldProto.SECURITY:
        #     return SecurityProto.FromString(field_to_unpack.field_value_packed.value)

        # raise ValueError(f"Field not found. Could not unpack {field_to_unpack.field}")

    @staticmethod
    def unpack_field(field_to_unpack:FieldMapEntry):
        if field_to_unpack.field == FieldProto.PORTFOLIO_ID:
            return UUIDProto.FromString(field_to_unpack.field_value_packed.value)
        if field_to_unpack.field == FieldProto.TRADE_DATE or field_to_unpack.field == FieldProto.SETTLEMENT_DATE \
            or field_to_unpack.field == FieldProto.TAX_LOT_OPEN_DATE\
                or field_to_unpack.field == FieldProto.TAX_LOT_CLOSE_DATE:
            return LocalDateProto.FromString(field_to_unpack.field_value_packed.value)
        if field_to_unpack.field == FieldProto.IDENTIFIER:
            return IdentifierProto.FromString(field_to_unpack.field_value_packed.value)
        if field_to_unpack.field == FieldProto.TRANSACTION_TYPE:
            name:str = FieldProto.DESCRIPTOR.values_by_number[field_to_unpack.field].name
            return ProtoEnum(name, field_to_unpack.enum_value)
        if field_to_unpack.field == FieldProto.PORTFOLIO_NAME or field_to_unpack.field == FieldProto.SECURITY_DESCRIPTION \
            or field_to_unpack.field == FieldProto.PRODUCT_TYPE:
            return wrappers.StringValue.FromString(field_to_unpack.field_value_packed.value).value
        if field_to_unpack.field == FieldProto.PORTFOLIO:
            return PortfolioProto.FromString(field_to_unpack.field_value_packed.value)
        if field_to_unpack.field == FieldProto.SECURITY:
            return SecurityProto.FromString(field_to_unpack.field_value_packed.value)

        raise ValueError(f"Field not found. Could not unpack {field_to_unpack.field}")

    @staticmethod
    def unpack_measure(measure_to_unpack:MeasureProto):
        if measure_to_unpack.measure == MeasureProto.DIRECTED_QUANTITY:
            return Decimal(measure_to_unpack.measure_decimal_value.arbitrary_precision_value)
        
        raise ValueError(f"Field not found. Could not unpack {measure_to_unpack.field}")

