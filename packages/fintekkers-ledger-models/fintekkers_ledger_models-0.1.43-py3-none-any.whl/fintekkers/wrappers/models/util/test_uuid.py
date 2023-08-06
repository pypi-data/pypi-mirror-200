from fintekkers.wrappers.models.util import uuid

def test_conversion():
    tmp_uuid = uuid.FintekkersUuid.new_uuid()

    uuid_as_str = tmp_uuid.__str__()

    uuid_from_bytes_as_str = uuid.FintekkersUuid.from_bytes(tmp_uuid.uuid.bytes).__str__()
    
    assert uuid_as_str.__str__() == uuid_from_bytes_as_str.__str__()

    uuid_from_uuid = uuid.FintekkersUuid.from_uuid(tmp_uuid.uuid).__str__()

    assert uuid_from_uuid.__str__() == uuid_from_bytes_as_str.__str__()
    
    