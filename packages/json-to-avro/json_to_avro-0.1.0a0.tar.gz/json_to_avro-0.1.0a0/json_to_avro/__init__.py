import dataclasses
from loguru import logger
from schema_registry.serializers import AvroMessageSerializer
from typing import (
    TypeAlias,
)

from .avro_schema import RegisteredAvroSchemaId, AvroSchemaCandidate, RegisteredAvroSchema
from .schema_provider import SchemaProvider

Json: TypeAlias = str | float | int | bool | dict[str, "Json"] | list["Json"] | None


@dataclasses.dataclass
class AvroableData:
    record_name: str
    subject_name: str
    data: Json


def init_schema_cache() -> dict[str, RegisteredAvroSchema]:
    return {}


def serialize_as_avro(
    msg: AvroableData,
    provider: SchemaProvider,
    ser: AvroMessageSerializer,
):
    schema_candidate = AvroSchemaCandidate.from_avroable_data(msg)
    maybe_existing_registered_schema = provider.get(msg.subject_name)
    logger.debug("Existing Schema: %s" % maybe_existing_registered_schema)
    schema_id: RegisteredAvroSchemaId = (
        maybe_existing_registered_schema.schema_id
        if maybe_existing_registered_schema is not None
        else provider.register_and_set(msg.subject_name, schema_candidate)
    )
    logger.debug("Registered Schema: %s", provider[msg.subject_name])

    try:
        return ser.encode_record_with_schema_id(schema_id, msg.data)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        logger.debug(f"Schema mismatch: {e}")
        logger.debug(
            "existing schema: %s" % maybe_existing_registered_schema.schema
            if maybe_existing_registered_schema is not None
            else None,
        )
        logger.debug("Message data: %s" % msg.data)
        new_schema_candidate = AvroSchemaCandidate(
            provider[msg.subject_name].schema + schema_candidate.schema
        )
        logger.debug("New Schema Candidate: %s" % new_schema_candidate)
        schema_id = provider.register_and_set(msg.subject_name, new_schema_candidate)

        return ser.encode_record_with_schema_id(schema_id, msg.data)


