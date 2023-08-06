from dataclasses import dataclass
from typing import List, Literal

# --------------------------------- PHOTO TYPES --------------------------------- #


@dataclass
class Src:
    original: str
    large2x: str
    large: str
    medium: str
    small: str
    portrait: str
    landscape: str
    tiny: str


@dataclass
class Photo:
    id: int
    width: int
    height: int
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: str
    src: Src
    liked: bool
    alt: str

    @property
    def extension(self):
        return self.src.original.split(".")[-1]


# --------------------------------- VIDEO TYPES --------------------------------- #


@dataclass
class User:
    id: int
    name: str
    url: str


@dataclass
class VideoFile:
    id: int
    quality: Literal["hd", "sd"]
    file_type: str
    width: int
    height: int
    fps: int
    link: str


@dataclass
class VideoPicture:
    id: int
    picture: str
    nr: int


@dataclass
class Video:
    id: int
    width: int
    height: int
    url: str
    image: str
    duration: int
    user: User
    video_files: List[VideoFile]
    video_pictures: List[VideoPicture]


# --------------------------------- COLLECTION TYPES --------------------------------- #


@dataclass
class Collection:
    id: str
    title: str
    description: str
    private: bool
    media_count: int
    photos_count: int
    videos_count: int
