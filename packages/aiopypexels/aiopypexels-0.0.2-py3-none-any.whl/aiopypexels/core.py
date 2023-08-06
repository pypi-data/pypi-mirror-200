from pathlib import Path
from aiohttp import ClientSession
from aiocfscrape import CloudflareScraper
from .types.response_types import *
from .types.content_types import Photo, Video
from .types.arg_types import ORIENTATION_TYPE, SIZE_TYPE, LOCALE_TYPE, QUALITY_TYPE
from dacite import from_dict
from typing import Literal, Optional, get_args
from .exceptions import EXCEPTIONS_ENUM


class AioPexels:
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.__BASE_URL = "https://api.pexels.com/"

    # --------------------------------- PHOTOS --------------------------------- #

    # --- Search photo by query --- #

    async def get_photos_by_query(
        self,
        query: str,
        orientation: ORIENTATION_TYPE = None,
        size: SIZE_TYPE = None,
        color: str = None,
        locale: LOCALE_TYPE = None,
        page: int = 1,
        per_page: int = 15,
    ) -> PhotoSearchResponse:
        """Enables you to search Pexels for any topic that you would like. For example your query could be something broad like Nature, Tigers, People. Or it could be something specific like Group of people working."""

        response = await self.__request_json(
            endpoint="v1/search",
            query=query,
            orientation=orientation,
            size=size,
            color=color,
            locale=locale,
            page=page,
            per_page=per_page,
        )
        return from_dict(PhotoSearchResponse, response)

    # --- Get curated photos --- #

    async def get_curated_photos(
        self, page: int = 1, per_page: int = 15
    ) -> PhotoCuratedResponse:
        """Enables you to receive real-time photos curated by the Pexels team."""

        response = await self.__request_json(
            endpoint="v1/curated", page=page, per_page=per_page
        )
        return from_dict(PhotoCuratedResponse, response)

    # --- Get single photo by ID --- #

    async def get_photo_by_id(self, photo_id: int) -> Photo:
        """Retrieve a specific Photo from its id."""

        response = await self.__request_json(endpoint=f"v1/photos/{photo_id}")
        return from_dict(Photo, response)

    # --- Download photo by ID --- #

    async def download_photo_by_id(
        self, photo_id: int, destination: str, quality: QUALITY_TYPE = "original"
    ):
        """Unofficial feature to download a photo in one of avaliable resolutions in the selected destination"""

        listed_qualities = list(get_args(QUALITY_TYPE))
        if not quality in listed_qualities:
            raise ValueError(
                f"Quality must be one of the following: {', '.join(listed_qualities)}"
            )

        photo = await self.get_photo_by_id(photo_id)
        path = Path(destination)

        self.__check_and_create_path(path)

        if path.is_dir():
            file_name = f"{photo_id}_{quality}.{photo.extension}"
            path = path.joinpath(file_name)

        async with CloudflareScraper() as session:
            async with session.get(url=photo.src.__getattribute__(quality)) as response:
                photo_bytes = await response.read()

        with open(path, "wb") as f:
            f.write(photo_bytes)

    # --------------------------------- VIDEOS --------------------------------- #

    # --- Search video by query --- #

    async def get_video_by_query(
        self,
        query: str,
        orientation: ORIENTATION_TYPE = None,
        size: SIZE_TYPE = None,
        locale: LOCALE_TYPE = None,
        page: int = 1,
        per_page: int = 15,
    ) -> VideoSearchResponse:
        """Enables you to search Pexels for any topic that you would like. For example your query could be something broad like Nature, Tigers, People. Or it could be something specific like Group of people working."""

        response = await self.__request_json(
            endpoint="videos/search",
            query=query,
            orientation=orientation,
            size=size,
            locale=locale,
            page=page,
            per_page=per_page,
        )
        return from_dict(VideoSearchResponse, response)

    # --- Get popular videos --- #

    async def get_popular_videos(
        self,
        min_width: Optional[int],
        min_height: Optional[int],
        min_duration: Optional[int],
        max_duration: Optional[int],
        page: int = 1,
        per_page: int = 15,
    ) -> PopularVideosResponse:
        """Receive the current popular Pexels videos."""

        response = await self.__request_json(
            endpoint="videos/popular",
            min_width=min_width,
            min_height=min_height,
            min_duration=min_duration,
            max_duration=max_duration,
            page=page,
            per_page=per_page,
        )
        return from_dict(PopularVideosResponse, response)

    # --- Get single video by ID --- #

    async def get_video_by_id(self, video_id: int) -> Video:
        """Retrieve a specific Video from its id."""

        response = await self.__request_json(endpoint=f"videos/videos/{video_id}")
        return from_dict(Video, response)

    # --------------------------------- COLLECTIONS --------------------------------- #

    # --- Get featured collections --- #

    async def get_featured_collections(
        self, page: int = 1, per_page: int = 15
    ) -> FeaturedCollectionsResponse:
        """Returns all featured collections on Pexels."""

        response = await self.__request_json(
            endpoint="v1/collections/featured", page=page, per_page=per_page
        )
        return from_dict(FeaturedCollectionsResponse, response)

    # --- Get featured collections --- #

    async def get_my_collections(self, page: int = 1, per_page: int = 15):
        """Returns all of your collections."""

        response = await self.__request_json(
            endpoint="v1/collections", page=page, per_page=per_page
        )
        return from_dict(MyCollectionsResponse, response)

    # --- Get featured collections --- #
    async def get_collection_by_id(
        self,
        collection_id: int,
        type: Optional[Literal["photos", "videos"]],
        page: int = 1,
        per_page: int = 15,
    ) -> CollectionMediaResponse:
        """Returns all the media (photos and videos) within a single collection. You can filter to only receive photos or videos using the type parameter."""

        response = await self.__request_json(
            endpoint=f"v1/collections/{collection_id}",
            type=type,
            page=page,
            per_page=per_page,
        )
        return from_dict(CollectionMediaResponse, response)

    # --------------------------------- PRIVATE METHODS --------------------------------- #
    def __build_params(self, **params):
        valued_params = {}

        for key, value in params.items():
            if value is not None:
                valued_params[key] = value
        return valued_params

    def __check_and_create_path(self, path: Path):
        path_way = path.parent if path.is_file() else path

        path_way.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()

    async def __request_json(self, endpoint: str, **params):
        async with ClientSession() as session:
            params = self.__build_params(**params)
            async with session.get(
                url=self.__BASE_URL + endpoint,
                params=params,
                headers={"Authorization": self.API_KEY},
            ) as response:
                json_data = await response.json()
                self.__handle_exceptions(json_data)
                return json_data

    def __handle_exceptions(self, response_data: dict):
        status_code = response_data.get("status")
        if status_code:
            exception = EXCEPTIONS_ENUM.get(status_code)
            message = response_data.get("error") or response_data.get("code")
            if exception:
                raise exception(code=status_code, message=message)
            else:
                raise Exception(
                    f"Unhandled exception in pexels API. Code: {status_code}, message: {message}"
                )
