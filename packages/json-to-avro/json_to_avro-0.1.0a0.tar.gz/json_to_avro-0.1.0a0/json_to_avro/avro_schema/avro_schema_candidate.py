import dataclasses

from .mergeable_avro_schema import MergeableAvroSchema
from .. import AvroableData


@dataclasses.dataclass
class AvroSchemaCandidate:
    schema: MergeableAvroSchema

    @classmethod
    def from_avroable_data(cls, msg: AvroableData) -> "AvroSchemaCandidate":
        return cls(MergeableAvroSchema.from_avroable_data(msg))