from enum import Enum, IntEnum

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.d3 import Point, Rotation
from pydantic import BaseModel, Field


class CameraProjection(str, Enum):
    PERSPECTIVE = "perspective"


class SequenceCameraProjection(str, Enum):
    PERSPECTIVE = "perspective"
    PANORAMIC = "panoramic"
    ORTHOGRAPHIC = "orthographic"


class Wavelength(str, Enum):
    VISIBLE = "visible"
    NIR = "nir"


class FramesPerSecond(IntEnum):
    FPS_0 = 0
    FPS_1 = 1
    FPS_5 = 5
    FPS_10 = 10
    FPS_15 = 15
    FPS_30 = 30
    FPS_60 = 60


class CameraIntrinsicParams(BaseModel):
    projection: CameraProjection = fields.enum(CameraProjection, conf["camera"]["projection"])
    wavelength: Wavelength = fields.enum(Wavelength, conf["camera"]["wavelength"])
    resolution_height: int = fields.numeric(conf["camera"]["res"]["height"])
    resolution_width: int = fields.numeric(conf["camera"]["res"]["width"])
    fov_horizontal: int = fields.numeric(conf["camera"]["fov"]["horizontal"])
    fov_vertical: int = fields.numeric(conf["camera"]["fov"]["vertical"])
    sensor_width: float = fields.numeric(conf["camera"]["sensor"]["width"])

    def dict(self, exclude_none=True, **kwargs):
        return super().dict(exclude_none=exclude_none, **kwargs)


class CameraExtrinsicParams(BaseModel):
    location: Point = fields.point(conf["camera"]["location"])
    rotation: Rotation = fields.rotation(conf["camera"]["rotation"])


class Camera(BaseModel):
    name: str = conf["camera"]["name"]
    extrinsic_params: CameraExtrinsicParams = Field(default_factory=CameraExtrinsicParams)
    intrinsic_params: CameraIntrinsicParams = Field(default_factory=CameraIntrinsicParams)

    @property
    def extrinsics(self) -> CameraExtrinsicParams:
        return self.extrinsic_params

    @extrinsics.setter
    def extrinsics(self, extrinsic_params: CameraExtrinsicParams) -> None:
        self.extrinsic_params = extrinsic_params

    @property
    def intrinsics(self) -> CameraIntrinsicParams:
        return self.intrinsic_params

    @intrinsics.setter
    def intrinsics(self, intrinsic_params: CameraIntrinsicParams) -> None:
        self.intrinsic_params = intrinsic_params


class SequenceIntrinsicParams(CameraIntrinsicParams):
    projection: SequenceCameraProjection = fields.enum(SequenceCameraProjection, conf["camera"]["projection"])
    fps: FramesPerSecond = fields.enum(FramesPerSecond, conf["camera"]["fps"])


class SequenceCamera(Camera):
    intrinsic_params: SequenceIntrinsicParams = Field(default_factory=SequenceIntrinsicParams)
