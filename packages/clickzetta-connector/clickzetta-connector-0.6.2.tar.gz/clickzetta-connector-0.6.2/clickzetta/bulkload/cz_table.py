import string
from clickzetta.proto.generated import metadata_entity_pb2, ingestion_pb2, table_meta_pb2


class CZTable:
    def __init__(self, table_meta: metadata_entity_pb2.Entity, schema_name: string, table_name: string,
                 table_type: ingestion_pb2.IGSTableType):
        self.table_id = table_meta.table.table_id
        self.schema_name = schema_name
        self.table_name = table_name
        self.table_meta = table_meta
        self.table_type = table_type
        self.schema = {}
        fields = table_meta.table.table_schema.fields
        for field in fields:
            if not field.virtual:
                self.schema[field.name] = field.type

