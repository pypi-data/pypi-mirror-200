from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.environment import CameraExtrinsicParams
from datagen_protocol.schema.base import Asset, AssetAttributes, PresetAsset, SchemaBaseModel
from datagen_protocol.schema.attributes import (
    HICDomain,
    HICSubDomain,
    HumanBehaviour,
    Ethnicity,
    Age,
    Gender,
)
from datagen_protocol.schema.environment import Background, SequenceCamera, Light


class SequenceAttributes(AssetAttributes):
    domain: HICDomain
    sub_domain: HICSubDomain
    behaviour: HumanBehaviour
    ethnicity: Ethnicity
    gender: Gender
    age: Age


class SequencePresets(SchemaBaseModel):
    cameras: Dict[str, CameraExtrinsicParams]
    clutter_areas: List[str]


class ClutterLevel(str, Enum):
    NONE = "none"  # 0
    LOW = "low"  # 8
    MEDIUM = "medium"  # 16
    HIGH = "high"  # 32


class DataSequence(PresetAsset[SequenceAttributes, SequencePresets]):
    camera: SequenceCamera = Field(default_factory=SequenceCamera)
    background: Optional[Background] = None
    lights: Optional[List[Light]] = Field(default_factory=list)
    clutter_areas: Dict[str, ClutterLevel] = Field(default_factory=dict)
