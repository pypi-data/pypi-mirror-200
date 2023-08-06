from dataclasses import dataclass
from typing import List, Optional, Union
from .content_types import Collection, Photo, Video


@dataclass
class PhotoSearchResponse:
    total_results: int
    page: int
    per_page: int
    photos: List[Photo]
    prev_page: Optional[int] = None
    next_page: Optional[int] = None


@dataclass
class PhotoCuratedResponse(PhotoSearchResponse):
    ...


@dataclass
class VideoSearchResponse:
    videos: List[Video]
    url: str
    page: int
    per_page: int
    total_results: int
    prev_page: Optional[int] = None
    next_page: Optional[int] = None


@dataclass
class PopularVideosResponse(VideoSearchResponse):
    ...


@dataclass
class FeaturedCollectionsResponse:
    collections: List[Collection]
    page: int
    per_page: int
    total_results: int
    prev_page: Optional[int] = None
    next_page: Optional[int] = None


@dataclass
class MyCollectionsResponse(FeaturedCollectionsResponse):
    ...


@dataclass
class CollectionMediaResponse:
    id: str
    media: List[Union[Photo, Video]]
    page: int
    per_page: int
    total_results: int
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
