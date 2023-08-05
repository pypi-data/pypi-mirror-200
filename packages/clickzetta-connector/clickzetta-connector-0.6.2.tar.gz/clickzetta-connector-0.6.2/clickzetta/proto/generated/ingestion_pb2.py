# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ingestion.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import file_format_type_pb2 as file__format__type__pb2
from . import metadata_entity_pb2 as metadata__entity__pb2
from . import row_operations_pb2 as row__operations__pb2
from . import kudu_common_pb2 as kudu__common__pb2
from . import data_type_pb2 as data__type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fingestion.proto\x12\x12\x63z.proto.ingestion\x1a\x16\x66ile_format_type.proto\x1a\x15metadata_entity.proto\x1a\x14row_operations.proto\x1a\x11kudu_common.proto\x1a\x0f\x64\x61ta_type.proto\"\xa7\x01\n\x13GetTableMetaRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12\x11\n\tworkspace\x18\x04 \x01(\t\x12\x13\n\x0binstance_id\x18\x05 \x01(\x03\x12,\n\x07\x61\x63\x63ount\x18\x06 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\"\xbb\x01\n\x14GetTableMetaResponse\x12$\n\ntable_meta\x18\x01 \x01(\x0b\x32\x10.cz.proto.Entity\x12\x34\n\ntable_type\x18\x02 \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x13\n\x0binstance_id\x18\x03 \x01(\x03\x12\x32\n\x06status\x18\x04 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"\xcd\x02\n\x1d\x43ontrollerCreateTabletRequest\x12\x13\n\x0bschema_name\x18\x01 \x01(\t\x12\x12\n\ntable_name\x18\x02 \x01(\t\x12$\n\ntable_meta\x18\x03 \x01(\x0b\x32\x10.cz.proto.Entity\x12\x13\n\x0btablet_nums\x18\x04 \x01(\x03\x12\x34\n\ntable_type\x18\x05 \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x11\n\tkey_names\x18\x06 \x03(\t\x12\x15\n\rbuckets_count\x18\x07 \x01(\x04\x12\x12\n\nsort_names\x18\x08 \x03(\t\x12\x11\n\tworkspace\x18\t \x01(\t\x12\x13\n\x0binstance_id\x18\n \x01(\x03\x12,\n\x07\x61\x63\x63ount\x18\x0b \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\"\xea\x03\n\x19WorkerCreateTabletRequest\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12#\n\x0btablet_meta\x18\x04 \x01(\x0b\x32\x0e.kudu.SchemaPB\x12\x11\n\tworker_id\x18\x05 \x01(\x03\x12$\n\ntable_meta\x18\x06 \x01(\x0b\x32\x10.cz.proto.Entity\x12\x12\n\ntable_path\x18\x07 \x01(\t\x12\x34\n\ntable_type\x18\x08 \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x11\n\tkey_names\x18\t \x03(\t\x12\x17\n\x0fhash_range_list\x18\n \x03(\x04\x12\x14\n\x0c\x62uckets_list\x18\x0b \x03(\r\x12\x12\n\nsort_names\x18\x0c \x03(\t\x12\x11\n\tworkspace\x18\r \x01(\t\x12\x13\n\x0binstance_id\x18\x0e \x01(\x03\x12@\n\x0fpartition_infos\x18\x0f \x03(\x0b\x32\'.cz.proto.ingestion.PartitionColumnInfo\x12)\n\x0ftable_full_meta\x18\x10 \x01(\x0b\x32\x10.cz.proto.Entity\"\xab\x01\n\x13PartitionColumnInfo\x12%\n\x1dvirtual_partition_column_name\x18\x01 \x01(\t\x12#\n\x1bvirtual_partition_column_id\x18\x02 \x01(\r\x12$\n\x1csource_partition_column_name\x18\x03 \x01(\t\x12\"\n\x1asource_partition_column_id\x18\x04 \x01(\r\"`\n\x14\x43reateTabletResponse\x12\x14\n\x0c\x63reated_time\x18\x01 \x01(\x03\x12\x32\n\x06status\x18\x02 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"\xb8\x01\n\x13\x43ommitTabletRequest\x12\x13\n\x0binstance_id\x18\x01 \x01(\x03\x12\x11\n\tworkspace\x18\x02 \x01(\t\x12\x13\n\x0bschema_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x0f\n\x07tableId\x18\x05 \x01(\x03\x12\x11\n\ttablet_id\x18\x06 \x03(\x03\x12,\n\x07\x61\x63\x63ount\x18\x07 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\"J\n\x14\x43ommitTabletResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"\xca\x01\n\x11\x44ropTabletRequest\x12\x13\n\x0binstance_id\x18\x01 \x01(\x03\x12\x11\n\tworkspace\x18\x02 \x01(\t\x12\x13\n\x0bschema_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x0f\n\x07tableId\x18\x05 \x01(\x03\x12\x11\n\ttablet_id\x18\x06 \x03(\x03\x12,\n\x07\x61\x63\x63ount\x18\x07 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x12\n\nrequest_id\x18\x08 \x01(\t\"H\n\x12\x44ropTabletResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\":\n\x14RestartTabletRequest\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"o\n\x15RestartTabletResponse\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x32\n\x06status\x18\x03 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"6\n\x10\x44\x65lTabletRequest\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"k\n\x11\x44\x65lTabletResponse\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x32\n\x06status\x18\x03 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"a\n\x10\x42roadcastRequest\x12\x13\n\x0binstance_id\x18\x01 \x01(\x03\x12\x10\n\x08table_id\x18\x02 \x01(\x03\x12\x11\n\ttablet_id\x18\x03 \x03(\x03\x12\x13\n\x0b\x63lear_cache\x18\x04 \x01(\x08\"G\n\x11\x42roadcastResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"_\n\x0fWorkerHBRequest\x12\x11\n\tworker_id\x18\x01 \x01(\x03\x12\x13\n\x0bworker_port\x18\x02 \x01(\x03\x12\x13\n\x0bworker_host\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\"j\n\x10WorkerHBResponse\x12\x11\n\tworker_id\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x32\n\x06status\x18\x03 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"V\n\x18GetTabletsMappingRequest\x12\x11\n\tworker_id\x18\x01 \x01(\x03\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\"\x81\x02\n\x19GetTabletsMappingResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12X\n\x0etablet_mapping\x18\x02 \x03(\x0b\x32@.cz.proto.ingestion.GetTabletsMappingResponse.TabletMappingEntry\x1aV\n\x12TabletMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12/\n\x05value\x18\x02 \x01(\x0b\x32 .cz.proto.ingestion.TabletIdList:\x02\x38\x01\"!\n\x0cTabletIdList\x12\x11\n\ttablet_id\x18\x01 \x03(\x03\"+\n\rHostPortTuple\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\\\n\x1eGetTabletPhysicsMappingRequest\x12\x11\n\ttablet_id\x18\x01 \x01(\x03\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\"j\n\x11TabletPhysicsInfo\x12\x11\n\tworker_id\x18\x01 \x01(\x03\x12\x11\n\ttablet_id\x18\x02 \x01(\x03\x12/\n\x04host\x18\x03 \x01(\x0b\x32!.cz.proto.ingestion.HostPortTuple\"\x8d\x01\n\x1fGetTabletPhysicsMappingResponse\x12\x36\n\x07tablets\x18\x01 \x03(\x0b\x32%.cz.proto.ingestion.TabletPhysicsInfo\x12\x32\n\x06status\x18\x02 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"-\n\x18GetWorkersMappingRequest\x12\x11\n\tworker_id\x18\x01 \x01(\x03\"\x85\x02\n\x19GetWorkersMappingResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12Z\n\x0fworkers_mapping\x18\x02 \x03(\x0b\x32\x41.cz.proto.ingestion.GetWorkersMappingResponse.WorkersMappingEntry\x1aX\n\x13WorkersMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.cz.proto.ingestion.HostPortTuple:\x02\x38\x01\"\xa7\x01\n\x17\x43heckTableExistsRequest\x12\x10\n\x08instance\x18\x01 \x01(\x03\x12\x11\n\tworkspace\x18\x02 \x01(\t\x12\x13\n\x0bschema_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x10\n\x08table_id\x18\x05 \x01(\x03\x12,\n\x07\x61\x63\x63ount\x18\x06 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\"N\n\x18\x43heckTableExistsResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"\x84\x05\n\x11\x44\x61taMutateRequest\x12\x10\n\x08\x62\x61tch_id\x18\x01 \x01(\x03\x12\x17\n\x0fwrite_timestamp\x18\x02 \x01(\x03\x12-\n\x0erow_operations\x18\x03 \x01(\x0b\x32\x15.kudu.RowOperationsPB\x12\x13\n\x0bschema_name\x18\x04 \x01(\t\x12\x12\n\ntable_name\x18\x05 \x01(\t\x12 \n\x06schema\x18\x06 \x01(\x0b\x32\x10.cz.proto.Entity\x12!\n\tschema_pb\x18\x07 \x01(\x0b\x32\x0e.kudu.SchemaPB\x12\x34\n\ntable_type\x18\x08 \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x15\n\rbuckets_count\x18\t \x01(\x04\x12\x13\n\x0bis_dispatch\x18\n \x01(\x08\x12\x11\n\ttablet_id\x18\x0b \x01(\x03\x12\x11\n\tkey_names\x18\x0c \x03(\t\x12\x12\n\nsort_names\x18\r \x03(\t\x12\x31\n\x12key_row_operations\x18\x0e \x01(\x0b\x32\x15.kudu.RowOperationsPB\x12%\n\rkey_schema_pb\x18\x0f \x01(\x0b\x32\x0e.kudu.SchemaPB\x12\x12\n\nbucket_ids\x18\x10 \x03(\r\x12\x0f\n\x07indexes\x18\x11 \x03(\x05\x12\x13\n\x0binstance_id\x18\x12 \x01(\x03\x12\x11\n\tworkspace\x18\x13 \x01(\t\x12,\n\x07\x61\x63\x63ount\x18\x14 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\r\n\x05token\x18\x15 \x01(\t\x12\x12\n\nrequest_id\x18\x16 \x01(\t\x12\x13\n\x0b\x62\x61tch_count\x18\x17 \x01(\x05\"\x96\x03\n\x19\x44\x61taMutateRequestInternal\x12\x10\n\x08\x62\x61tch_id\x18\x01 \x01(\x03\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12 \n\x06schema\x18\x04 \x01(\x0b\x32\x10.cz.proto.Entity\x12!\n\tschema_pb\x18\x05 \x01(\x0b\x32\x0e.kudu.SchemaPB\x12\x34\n\ntable_type\x18\x06 \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x13\n\x0bis_dispatch\x18\x07 \x01(\x08\x12\x12\n\ntablet_ids\x18\x08 \x03(\x03\x12\x13\n\x0binstance_id\x18\t \x01(\x03\x12\x11\n\tworkspace\x18\n \x01(\t\x12\x12\n\nrequest_id\x18\x0b \x01(\t\x12\x38\n\x19\x64ispatched_row_operations\x18\x0c \x03(\x0b\x32\x15.kudu.RowOperationsPB\x12\x0f\n\x07indexes\x18\r \x03(\x05\x12\x13\n\x0b\x62\x61tch_count\x18\x0e \x01(\x05\"\xb9\x01\n\x12\x44\x61taMutateResponse\x12\x10\n\x08\x62\x61tch_id\x18\x01 \x01(\x03\x12\x10\n\x08rows_num\x18\x02 \x01(\x03\x12\x32\n\x06status\x18\x03 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12\x12\n\nrequest_id\x18\x04 \x01(\t\x12\x37\n\nrow_status\x18\x05 \x03(\x0b\x32#.cz.proto.ingestion.MutateRowStatus\"m\n\x12GetWorkerIdRequest\x12\x13\n\x0bworker_host\x18\x01 \x01(\t\x12\x18\n\x10\x63reate_timestamp\x18\x02 \x01(\x03\x12\x13\n\x0bworker_port\x18\x03 \x01(\x03\x12\x13\n\x0bworker_name\x18\x04 \x01(\t\"\\\n\x13GetWorkerIdResponse\x12\x11\n\tworker_id\x18\x01 \x01(\x03\x12\x32\n\x06status\x18\x02 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"]\n\x0fMutateRowStatus\x12&\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x18.cz.proto.ingestion.Code\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\trow_index\x18\x03 \x01(\x05\"]\n\x0eResponseStatus\x12&\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x18.cz.proto.ingestion.Code\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x12\n\nrequest_id\x18\x03 \x01(\t\"-\n\x07\x41\x63\x63ount\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\x12\x11\n\tuser_name\x18\x02 \x01(\t\"\xb3\x01\n\x17GetMutateWorkersRequest\x12\x10\n\x08table_id\x18\x01 \x01(\x03\x12\x13\n\x0bschema_name\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12\x35\n\x0c\x63onnect_mode\x18\x04 \x01(\x0e\x32\x1f.cz.proto.ingestion.ConnectMode\x12\x11\n\ttablet_id\x18\x05 \x03(\x03\x12\x13\n\x0binstance_id\x18\x06 \x01(\x03\"\x93\x01\n\x18GetMutateWorkersResponse\x12\x30\n\x05tuple\x18\x01 \x03(\x0b\x32!.cz.proto.ingestion.HostPortTuple\x12\x11\n\ttablet_id\x18\x02 \x03(\x03\x12\x32\n\x06status\x18\x03 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"w\n\x12\x46lushTabletRequest\x12\x13\n\x0bschema_name\x18\x01 \x01(\t\x12\x12\n\ntable_name\x18\x02 \x01(\t\x12\x11\n\ttablet_id\x18\x03 \x01(\x03\x12\x10\n\x08table_id\x18\x04 \x01(\x03\x12\x13\n\x0binstance_id\x18\x05 \x01(\x03\"I\n\x13\x46lushTabletResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"^\n\x0eGatewayRequest\x12\x17\n\x0fmethodEnumValue\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x12\n\ninstanceId\x18\x03 \x01(\x03\x12\x0e\n\x06userId\x18\x04 \x01(\x03\"V\n\x0fGatewayResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12\x0f\n\x07message\x18\x02 \x01(\t\"+\n\tTimestamp\x12\x0f\n\x07seconds\x18\x01 \x01(\x03\x12\r\n\x05nanos\x18\x02 \x01(\x05\"b\n\x0fTableIdentifier\x12\x13\n\x0binstance_id\x18\x01 \x01(\x03\x12\x11\n\tworkspace\x18\x02 \x01(\t\x12\x13\n\x0bschema_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\"\x93\x03\n\x12\x42ulkloadStreamInfo\x12\x11\n\tstream_id\x18\x01 \x01(\t\x12=\n\x0cstream_state\x18\x02 \x01(\x0e\x32\'.cz.proto.ingestion.BulkloadStreamState\x12\x12\n\nsql_job_id\x18\x03 \x01(\t\x12\x37\n\nidentifier\x18\x04 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12>\n\toperation\x18\x05 \x01(\x0e\x32+.cz.proto.ingestion.BulkloadStreamOperation\x12\x16\n\x0epartition_spec\x18\x06 \x01(\t\x12\x13\n\x0brecord_keys\x18\x07 \x03(\t\x12$\n\ntable_meta\x18\x08 \x01(\x0b\x32\x10.cz.proto.Entity\x12\x34\n\ntable_type\x18\t \x01(\x0e\x32 .cz.proto.ingestion.IGSTableType\x12\x15\n\rsql_error_msg\x18\n \x01(\t\"\xc9\x01\n\x1a\x42ulkloadStreamWriterConfig\x12\x39\n\x0cstaging_path\x18\x01 \x01(\x0b\x32#.cz.proto.ingestion.StagingPathInfo\x12-\n\x0b\x66ile_format\x18\x02 \x01(\x0e\x32\x18.cz.proto.FileFormatType\x12\x1d\n\x15max_num_rows_per_file\x18\x03 \x01(\x03\x12\"\n\x1amax_size_in_bytes_per_file\x18\x04 \x01(\x03\"\x86\x02\n\x1b\x43reateBulkloadStreamRequest\x12,\n\x07\x61\x63\x63ount\x18\x01 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x37\n\nidentifier\x18\x03 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12>\n\toperation\x18\x04 \x01(\x0e\x32+.cz.proto.ingestion.BulkloadStreamOperation\x12\x16\n\x0epartition_spec\x18\x05 \x01(\t\x12\x13\n\x0brecord_keys\x18\x06 \x03(\t\"\x9d\x01\n\x1c\x43reateBulkloadStreamResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x34\n\x04info\x18\x03 \x01(\x0b\x32&.cz.proto.ingestion.BulkloadStreamInfo\"\xc2\x01\n\x18GetBulkloadStreamRequest\x12,\n\x07\x61\x63\x63ount\x18\x01 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x37\n\nidentifier\x18\x03 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12\x11\n\tstream_id\x18\x04 \x01(\t\x12\x17\n\x0fneed_table_meta\x18\x05 \x01(\x08\"\x9a\x01\n\x19GetBulkloadStreamResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x34\n\x04info\x18\x03 \x01(\x0b\x32&.cz.proto.ingestion.BulkloadStreamInfo\"\x80\x03\n\x1b\x43ommitBulkloadStreamRequest\x12,\n\x07\x61\x63\x63ount\x18\x01 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x37\n\nidentifier\x18\x03 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12\x11\n\tstream_id\x18\x04 \x01(\t\x12\x19\n\x11\x65xecute_workspace\x18\x05 \x01(\t\x12\x17\n\x0f\x65xecute_vc_name\x18\x06 \x01(\t\x12O\n\x0b\x63ommit_mode\x18\x07 \x01(\x0e\x32:.cz.proto.ingestion.CommitBulkloadStreamRequest.CommitMode\x12\x1a\n\x12spec_partition_ids\x18\x08 \x03(\r\"1\n\nCommitMode\x12\x11\n\rCOMMIT_STREAM\x10\x00\x12\x10\n\x0c\x41\x42ORT_STREAM\x10\x01\"\x88\x01\n\x1c\x43ommitBulkloadStreamResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12\x34\n\x04info\x18\x03 \x01(\x0b\x32&.cz.proto.ingestion.BulkloadStreamInfo\"\xc6\x01\n\x1fOpenBulkloadStreamWriterRequest\x12,\n\x07\x61\x63\x63ount\x18\x01 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x37\n\nidentifier\x18\x03 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12\x11\n\tstream_id\x18\x04 \x01(\t\x12\x14\n\x0cpartition_id\x18\x05 \x01(\r\"\x96\x01\n OpenBulkloadStreamWriterResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\x12>\n\x06\x63onfig\x18\x03 \x01(\x0b\x32..cz.proto.ingestion.BulkloadStreamWriterConfig\"\xf8\x01\n!FinishBulkloadStreamWriterRequest\x12,\n\x07\x61\x63\x63ount\x18\x01 \x01(\x0b\x32\x1b.cz.proto.ingestion.Account\x12\x13\n\x0binstance_id\x18\x02 \x01(\x03\x12\x37\n\nidentifier\x18\x03 \x01(\x0b\x32#.cz.proto.ingestion.TableIdentifier\x12\x11\n\tstream_id\x18\x04 \x01(\t\x12\x14\n\x0cpartition_id\x18\x05 \x01(\r\x12\x15\n\rwritten_files\x18\x06 \x03(\t\x12\x17\n\x0fwritten_lengths\x18\x07 \x03(\x04\"X\n\"FinishBulkloadStreamWriterResponse\x12\x32\n\x06status\x18\x01 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus\"\x94\x01\n\x12OSSStagingPathInfo\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x11\n\tsts_ak_id\x18\x03 \x01(\t\x12\x15\n\rsts_ak_secret\x18\x04 \x01(\t\x12\x11\n\tsts_token\x18\x05 \x01(\t\x12\x14\n\x0coss_endpoint\x18\x06 \x01(\t\x12\x1d\n\x15oss_internal_endpoint\x18\x07 \x01(\t\"Z\n\x0fStagingPathInfo\x12:\n\x08oss_path\x18\x01 \x01(\x0b\x32&.cz.proto.ingestion.OSSStagingPathInfoH\x00\x42\x0b\n\tpath_info\"\xa2\x01\n\x14StreamReadIdentifier\x12\x13\n\x0binstance_id\x18\x01 \x01(\x03\x12\x11\n\tworkspace\x18\x02 \x01(\t\x12\x13\n\x0bschema_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x10\n\x08table_id\x18\x05 \x01(\x03\x12\x11\n\ttablet_id\x18\x06 \x01(\x03\x12\x14\n\x0c\x63omponent_id\x18\x07 \x01(\x03\"\xde\x01\n\x11StreamReadOptions\x12<\n\nidentifier\x18\x01 \x01(\x0b\x32(.cz.proto.ingestion.StreamReadIdentifier\x12\'\n\x0bread_schema\x18\x02 \x01(\x0b\x32\x12.cz.proto.DataType\x12\x11\n\tbucket_id\x18\x03 \x01(\r\x12\x37\n\x10\x63utoff_timestamp\x18\x04 \x01(\x0b\x32\x1d.cz.proto.ingestion.Timestamp\x12\x16\n\x0erow_batch_size\x18\x05 \x01(\x04\"Z\n\x11StreamReadRequest\x12\x36\n\x07options\x18\x01 \x01(\x0b\x32%.cz.proto.ingestion.StreamReadOptions\x12\r\n\x05\x63lose\x18\x02 \x01(\x08\"\xaa\x01\n\x16StreamReadDeltaOptions\x12<\n\nidentifier\x18\x01 \x01(\x0b\x32(.cz.proto.ingestion.StreamReadIdentifier\x12\x37\n\x10\x63utoff_timestamp\x18\x04 \x01(\x0b\x32\x1d.cz.proto.ingestion.Timestamp\x12\x19\n\x11record_batch_size\x18\x05 \x01(\x04\"d\n\x16StreamReadDeltaRequest\x12;\n\x07options\x18\x01 \x01(\x0b\x32*.cz.proto.ingestion.StreamReadDeltaOptions\x12\r\n\x05\x63lose\x18\x02 \x01(\x08\"C\n\x12StreamReadOpenInfo\x12\x19\n\x11\x66\x61llback_oss_path\x18\x01 \x01(\t\x12\x12\n\nrequest_id\x18\x02 \x01(\t\"\xe7\x01\n\x12StreamReadResponse\x12\x39\n\topen_info\x18\x01 \x01(\x0b\x32&.cz.proto.ingestion.StreamReadOpenInfo\x12\x18\n\x10payload_metadata\x18\x02 \x01(\x0c\x12\x1b\n\x13payload_body_buffer\x18\x03 \x01(\x0c\x12\x14\n\x0c\x65nd_of_batch\x18\x04 \x01(\x08\x12\x15\n\rend_of_stream\x18\x05 \x01(\x08\x12\x32\n\x06status\x18\x06 \x01(\x0b\x32\".cz.proto.ingestion.ResponseStatus*>\n\x0cIGSTableType\x12\n\n\x06NORMAL\x10\x00\x12\x0b\n\x07\x43LUSTER\x10\x01\x12\x08\n\x04\x41\x43ID\x10\x02\x12\x0b\n\x07UNKNOWN\x10\x03*\x9f\x01\n\x04\x43ode\x12\x0b\n\x07SUCCESS\x10\x00\x12\n\n\x06\x46\x41ILED\x10\x01\x12\x17\n\x13IGS_WORKER_REGISTED\x10\x02\x12\r\n\tTHROTTLED\x10\x03\x12\r\n\tNOT_FOUND\x10\x04\x12\x13\n\x0f\x41LREADY_PRESENT\x10\x05\x12\x0f\n\x0bTABLE_EXIST\x10\x06\x12\x11\n\rTABLE_DROPPED\x10\x07\x12\x0e\n\nCORRUPTION\x10\x08*<\n\x0b\x43onnectMode\x12\n\n\x06\x44IRECT\x10\x00\x12\x0b\n\x07GATEWAY\x10\x01\x12\x14\n\x10GATEWAY_INTERNAL\x10\x02*\x9d\x03\n\nMethodEnum\x12\x14\n\x10GATEWAY_RPC_CALL\x10\x00\x12\x12\n\x0eGET_TABLE_META\x10\x01\x12\x11\n\rCREATE_TABLET\x10\x02\x12\x15\n\x11GET_MUTATE_WORKER\x10\x03\x12\x11\n\rCOMMIT_TABLET\x10\x04\x12\x0f\n\x0b\x44ROP_TABLET\x10\x05\x12\x16\n\x12\x43HECK_TABLE_EXISTS\x10\x06\x12\x19\n\x15\x43REATE_PENDING_STREAM\x10\x07\x12\x19\n\x15\x43OMMIT_PENDING_STREAM\x10\x08\x12\x16\n\x12GET_PENDING_STREAM\x10\t\x12\x17\n\x13JOIN_PENDING_STREAM\x10\n\x12\x1b\n\x17\x43REATE_BULK_LOAD_STREAM\x10\x0b\x12\x18\n\x14GET_BULK_LOAD_STREAM\x10\x0c\x12\x1b\n\x17\x43OMMIT_BULK_LOAD_STREAM\x10\r\x12 \n\x1cOPEN_BULK_LOAD_STREAM_WRITER\x10\x0e\x12\"\n\x1e\x46INISH_BULK_LOAD_STREAM_WRITER\x10\x0f*\x8a\x01\n\x13\x42ulkloadStreamState\x12\x0e\n\nBS_CREATED\x10\x00\x12\r\n\tBS_SEALED\x10\x01\x12\x17\n\x13\x42S_COMMIT_SUBMITTED\x10\x02\x12\x15\n\x11\x42S_COMMIT_SUCCESS\x10\x03\x12\x14\n\x10\x42S_COMMIT_FAILED\x10\x04\x12\x0e\n\nBS_ABORTED\x10\x05*I\n\x17\x42ulkloadStreamOperation\x12\r\n\tBS_APPEND\x10\x00\x12\x10\n\x0c\x42S_OVERWRITE\x10\x01\x12\r\n\tBS_UPSERT\x10\x02*T\n\x12StreamReadDataType\x12\x0e\n\nSCHEMAMETA\x10\x00\x12\x0e\n\nSCHEMABODY\x10\x01\x12\x0e\n\nRECORDMETA\x10\x02\x12\x0e\n\nRECORDBODY\x10\x03\x32\x95\x03\n\x10IGSWorkerService\x12\x61\n\x0c\x43ommitTablet\x12\'.cz.proto.ingestion.CommitTabletRequest\x1a(.cz.proto.ingestion.CommitTabletResponse\x12[\n\x06Mutate\x12%.cz.proto.ingestion.DataMutateRequest\x1a&.cz.proto.ingestion.DataMutateResponse(\x01\x30\x01\x12X\n\tBroadcast\x12$.cz.proto.ingestion.BroadcastRequest\x1a%.cz.proto.ingestion.BroadcastResponse\x12g\n\x0eMutateInternal\x12-.cz.proto.ingestion.DataMutateRequestInternal\x1a&.cz.proto.ingestion.DataMutateResponse2z\n\x18IGSWorkerInternalService\x12^\n\x0b\x46lushTablet\x12&.cz.proto.ingestion.FlushTabletRequest\x1a\'.cz.proto.ingestion.FlushTabletResponse2\xdd\n\n\x14IGSControllerService\x12Y\n\x0eGatewayRpcCall\x12\".cz.proto.ingestion.GatewayRequest\x1a#.cz.proto.ingestion.GatewayResponse\x12\x61\n\x0cGetTableMeta\x12\'.cz.proto.ingestion.GetTableMetaRequest\x1a(.cz.proto.ingestion.GetTableMetaResponse\x12k\n\x0c\x43reateTablet\x12\x31.cz.proto.ingestion.ControllerCreateTabletRequest\x1a(.cz.proto.ingestion.CreateTabletResponse\x12\x61\n\x0c\x43ommitTablet\x12\'.cz.proto.ingestion.CommitTabletRequest\x1a(.cz.proto.ingestion.CommitTabletResponse\x12[\n\nDropTablet\x12%.cz.proto.ingestion.DropTabletRequest\x1a&.cz.proto.ingestion.DropTabletResponse\x12m\n\x10GetMutateWorkers\x12+.cz.proto.ingestion.GetMutateWorkersRequest\x1a,.cz.proto.ingestion.GetMutateWorkersResponse\x12m\n\x10\x43heckTableExists\x12+.cz.proto.ingestion.CheckTableExistsRequest\x1a,.cz.proto.ingestion.CheckTableExistsResponse\x12y\n\x14\x43reateBulkloadStream\x12/.cz.proto.ingestion.CreateBulkloadStreamRequest\x1a\x30.cz.proto.ingestion.CreateBulkloadStreamResponse\x12p\n\x11GetBulkloadStream\x12,.cz.proto.ingestion.GetBulkloadStreamRequest\x1a-.cz.proto.ingestion.GetBulkloadStreamResponse\x12y\n\x14\x43ommitBulkloadStream\x12/.cz.proto.ingestion.CommitBulkloadStreamRequest\x1a\x30.cz.proto.ingestion.CommitBulkloadStreamResponse\x12\x85\x01\n\x18OpenBulkloadStreamWriter\x12\x33.cz.proto.ingestion.OpenBulkloadStreamWriterRequest\x1a\x34.cz.proto.ingestion.OpenBulkloadStreamWriterResponse\x12\x8b\x01\n\x1a\x46inishBulkloadStreamWriter\x12\x35.cz.proto.ingestion.FinishBulkloadStreamWriterRequest\x1a\x36.cz.proto.ingestion.FinishBulkloadStreamWriterResponse2\xd6\x01\n\x14IGSWorkerDataService\x12Y\n\x04Read\x12%.cz.proto.ingestion.StreamReadRequest\x1a&.cz.proto.ingestion.StreamReadResponse(\x01\x30\x01\x12\x63\n\tReadDelta\x12*.cz.proto.ingestion.StreamReadDeltaRequest\x1a&.cz.proto.ingestion.StreamReadResponse(\x01\x30\x01\x42\x14\n\x12\x63z.proto.ingestionb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ingestion_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022cz.proto.ingestion'
  _GETTABLETSMAPPINGRESPONSE_TABLETMAPPINGENTRY._options = None
  _GETTABLETSMAPPINGRESPONSE_TABLETMAPPINGENTRY._serialized_options = b'8\001'
  _GETWORKERSMAPPINGRESPONSE_WORKERSMAPPINGENTRY._options = None
  _GETWORKERSMAPPINGRESPONSE_WORKERSMAPPINGENTRY._serialized_options = b'8\001'
  _IGSTABLETYPE._serialized_start=10653
  _IGSTABLETYPE._serialized_end=10715
  _CODE._serialized_start=10718
  _CODE._serialized_end=10877
  _CONNECTMODE._serialized_start=10879
  _CONNECTMODE._serialized_end=10939
  _METHODENUM._serialized_start=10942
  _METHODENUM._serialized_end=11355
  _BULKLOADSTREAMSTATE._serialized_start=11358
  _BULKLOADSTREAMSTATE._serialized_end=11496
  _BULKLOADSTREAMOPERATION._serialized_start=11498
  _BULKLOADSTREAMOPERATION._serialized_end=11571
  _STREAMREADDATATYPE._serialized_start=11573
  _STREAMREADDATATYPE._serialized_end=11657
  _GETTABLEMETAREQUEST._serialized_start=145
  _GETTABLEMETAREQUEST._serialized_end=312
  _GETTABLEMETARESPONSE._serialized_start=315
  _GETTABLEMETARESPONSE._serialized_end=502
  _CONTROLLERCREATETABLETREQUEST._serialized_start=505
  _CONTROLLERCREATETABLETREQUEST._serialized_end=838
  _WORKERCREATETABLETREQUEST._serialized_start=841
  _WORKERCREATETABLETREQUEST._serialized_end=1331
  _PARTITIONCOLUMNINFO._serialized_start=1334
  _PARTITIONCOLUMNINFO._serialized_end=1505
  _CREATETABLETRESPONSE._serialized_start=1507
  _CREATETABLETRESPONSE._serialized_end=1603
  _COMMITTABLETREQUEST._serialized_start=1606
  _COMMITTABLETREQUEST._serialized_end=1790
  _COMMITTABLETRESPONSE._serialized_start=1792
  _COMMITTABLETRESPONSE._serialized_end=1866
  _DROPTABLETREQUEST._serialized_start=1869
  _DROPTABLETREQUEST._serialized_end=2071
  _DROPTABLETRESPONSE._serialized_start=2073
  _DROPTABLETRESPONSE._serialized_end=2145
  _RESTARTTABLETREQUEST._serialized_start=2147
  _RESTARTTABLETREQUEST._serialized_end=2205
  _RESTARTTABLETRESPONSE._serialized_start=2207
  _RESTARTTABLETRESPONSE._serialized_end=2318
  _DELTABLETREQUEST._serialized_start=2320
  _DELTABLETREQUEST._serialized_end=2374
  _DELTABLETRESPONSE._serialized_start=2376
  _DELTABLETRESPONSE._serialized_end=2483
  _BROADCASTREQUEST._serialized_start=2485
  _BROADCASTREQUEST._serialized_end=2582
  _BROADCASTRESPONSE._serialized_start=2584
  _BROADCASTRESPONSE._serialized_end=2655
  _WORKERHBREQUEST._serialized_start=2657
  _WORKERHBREQUEST._serialized_end=2752
  _WORKERHBRESPONSE._serialized_start=2754
  _WORKERHBRESPONSE._serialized_end=2860
  _GETTABLETSMAPPINGREQUEST._serialized_start=2862
  _GETTABLETSMAPPINGREQUEST._serialized_end=2948
  _GETTABLETSMAPPINGRESPONSE._serialized_start=2951
  _GETTABLETSMAPPINGRESPONSE._serialized_end=3208
  _GETTABLETSMAPPINGRESPONSE_TABLETMAPPINGENTRY._serialized_start=3122
  _GETTABLETSMAPPINGRESPONSE_TABLETMAPPINGENTRY._serialized_end=3208
  _TABLETIDLIST._serialized_start=3210
  _TABLETIDLIST._serialized_end=3243
  _HOSTPORTTUPLE._serialized_start=3245
  _HOSTPORTTUPLE._serialized_end=3288
  _GETTABLETPHYSICSMAPPINGREQUEST._serialized_start=3290
  _GETTABLETPHYSICSMAPPINGREQUEST._serialized_end=3382
  _TABLETPHYSICSINFO._serialized_start=3384
  _TABLETPHYSICSINFO._serialized_end=3490
  _GETTABLETPHYSICSMAPPINGRESPONSE._serialized_start=3493
  _GETTABLETPHYSICSMAPPINGRESPONSE._serialized_end=3634
  _GETWORKERSMAPPINGREQUEST._serialized_start=3636
  _GETWORKERSMAPPINGREQUEST._serialized_end=3681
  _GETWORKERSMAPPINGRESPONSE._serialized_start=3684
  _GETWORKERSMAPPINGRESPONSE._serialized_end=3945
  _GETWORKERSMAPPINGRESPONSE_WORKERSMAPPINGENTRY._serialized_start=3857
  _GETWORKERSMAPPINGRESPONSE_WORKERSMAPPINGENTRY._serialized_end=3945
  _CHECKTABLEEXISTSREQUEST._serialized_start=3948
  _CHECKTABLEEXISTSREQUEST._serialized_end=4115
  _CHECKTABLEEXISTSRESPONSE._serialized_start=4117
  _CHECKTABLEEXISTSRESPONSE._serialized_end=4195
  _DATAMUTATEREQUEST._serialized_start=4198
  _DATAMUTATEREQUEST._serialized_end=4842
  _DATAMUTATEREQUESTINTERNAL._serialized_start=4845
  _DATAMUTATEREQUESTINTERNAL._serialized_end=5251
  _DATAMUTATERESPONSE._serialized_start=5254
  _DATAMUTATERESPONSE._serialized_end=5439
  _GETWORKERIDREQUEST._serialized_start=5441
  _GETWORKERIDREQUEST._serialized_end=5550
  _GETWORKERIDRESPONSE._serialized_start=5552
  _GETWORKERIDRESPONSE._serialized_end=5644
  _MUTATEROWSTATUS._serialized_start=5646
  _MUTATEROWSTATUS._serialized_end=5739
  _RESPONSESTATUS._serialized_start=5741
  _RESPONSESTATUS._serialized_end=5834
  _ACCOUNT._serialized_start=5836
  _ACCOUNT._serialized_end=5881
  _GETMUTATEWORKERSREQUEST._serialized_start=5884
  _GETMUTATEWORKERSREQUEST._serialized_end=6063
  _GETMUTATEWORKERSRESPONSE._serialized_start=6066
  _GETMUTATEWORKERSRESPONSE._serialized_end=6213
  _FLUSHTABLETREQUEST._serialized_start=6215
  _FLUSHTABLETREQUEST._serialized_end=6334
  _FLUSHTABLETRESPONSE._serialized_start=6336
  _FLUSHTABLETRESPONSE._serialized_end=6409
  _GATEWAYREQUEST._serialized_start=6411
  _GATEWAYREQUEST._serialized_end=6505
  _GATEWAYRESPONSE._serialized_start=6507
  _GATEWAYRESPONSE._serialized_end=6593
  _TIMESTAMP._serialized_start=6595
  _TIMESTAMP._serialized_end=6638
  _TABLEIDENTIFIER._serialized_start=6640
  _TABLEIDENTIFIER._serialized_end=6738
  _BULKLOADSTREAMINFO._serialized_start=6741
  _BULKLOADSTREAMINFO._serialized_end=7144
  _BULKLOADSTREAMWRITERCONFIG._serialized_start=7147
  _BULKLOADSTREAMWRITERCONFIG._serialized_end=7348
  _CREATEBULKLOADSTREAMREQUEST._serialized_start=7351
  _CREATEBULKLOADSTREAMREQUEST._serialized_end=7613
  _CREATEBULKLOADSTREAMRESPONSE._serialized_start=7616
  _CREATEBULKLOADSTREAMRESPONSE._serialized_end=7773
  _GETBULKLOADSTREAMREQUEST._serialized_start=7776
  _GETBULKLOADSTREAMREQUEST._serialized_end=7970
  _GETBULKLOADSTREAMRESPONSE._serialized_start=7973
  _GETBULKLOADSTREAMRESPONSE._serialized_end=8127
  _COMMITBULKLOADSTREAMREQUEST._serialized_start=8130
  _COMMITBULKLOADSTREAMREQUEST._serialized_end=8514
  _COMMITBULKLOADSTREAMREQUEST_COMMITMODE._serialized_start=8465
  _COMMITBULKLOADSTREAMREQUEST_COMMITMODE._serialized_end=8514
  _COMMITBULKLOADSTREAMRESPONSE._serialized_start=8517
  _COMMITBULKLOADSTREAMRESPONSE._serialized_end=8653
  _OPENBULKLOADSTREAMWRITERREQUEST._serialized_start=8656
  _OPENBULKLOADSTREAMWRITERREQUEST._serialized_end=8854
  _OPENBULKLOADSTREAMWRITERRESPONSE._serialized_start=8857
  _OPENBULKLOADSTREAMWRITERRESPONSE._serialized_end=9007
  _FINISHBULKLOADSTREAMWRITERREQUEST._serialized_start=9010
  _FINISHBULKLOADSTREAMWRITERREQUEST._serialized_end=9258
  _FINISHBULKLOADSTREAMWRITERRESPONSE._serialized_start=9260
  _FINISHBULKLOADSTREAMWRITERRESPONSE._serialized_end=9348
  _OSSSTAGINGPATHINFO._serialized_start=9351
  _OSSSTAGINGPATHINFO._serialized_end=9499
  _STAGINGPATHINFO._serialized_start=9501
  _STAGINGPATHINFO._serialized_end=9591
  _STREAMREADIDENTIFIER._serialized_start=9594
  _STREAMREADIDENTIFIER._serialized_end=9756
  _STREAMREADOPTIONS._serialized_start=9759
  _STREAMREADOPTIONS._serialized_end=9981
  _STREAMREADREQUEST._serialized_start=9983
  _STREAMREADREQUEST._serialized_end=10073
  _STREAMREADDELTAOPTIONS._serialized_start=10076
  _STREAMREADDELTAOPTIONS._serialized_end=10246
  _STREAMREADDELTAREQUEST._serialized_start=10248
  _STREAMREADDELTAREQUEST._serialized_end=10348
  _STREAMREADOPENINFO._serialized_start=10350
  _STREAMREADOPENINFO._serialized_end=10417
  _STREAMREADRESPONSE._serialized_start=10420
  _STREAMREADRESPONSE._serialized_end=10651
  _IGSWORKERSERVICE._serialized_start=11660
  _IGSWORKERSERVICE._serialized_end=12065
  _IGSWORKERINTERNALSERVICE._serialized_start=12067
  _IGSWORKERINTERNALSERVICE._serialized_end=12189
  _IGSCONTROLLERSERVICE._serialized_start=12192
  _IGSCONTROLLERSERVICE._serialized_end=13565
  _IGSWORKERDATASERVICE._serialized_start=13568
  _IGSWORKERDATASERVICE._serialized_end=13782
# @@protoc_insertion_point(module_scope)
