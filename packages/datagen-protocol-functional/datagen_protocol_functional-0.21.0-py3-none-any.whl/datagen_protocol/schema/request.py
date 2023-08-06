from typing import List

from datagen_protocol.schema.attributes import Generator
from datagen_protocol.schema.base import SchemaBaseModel
from datagen_protocol.schema.hic.sequence import DataSequence
from datagen_protocol.schema.humans import HumanDatapoint


class DataRequest(SchemaBaseModel):
    datapoints: List[HumanDatapoint] = None
    generator: Generator = Generator.IDENTITIES

    def __len__(self):
        return len(self.datapoints)


class SequenceRequest(SchemaBaseModel):
    sequences: List[DataSequence] = None
    generator: Generator = Generator.HIC

    def __len__(self):
        len(self.sequences)
