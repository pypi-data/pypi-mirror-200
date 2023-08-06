from fintekkers.models.transaction.transaction_type_pb2 import TransactionTypeProto

class TransactionType():
    def __init__(self, proto: TransactionTypeProto):
        self.proto = proto

    def __str__(self) -> str:
        return TransactionTypeProto.Name(self.proto)

