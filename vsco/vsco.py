from concurrent.futures import ThreadPoolExecutor, wait
import json

import requests
import logging

from PIL import Image
from io import BytesIO

from typing import Union

from .exceptions import VscoRequestException, InvalidProfileException, VscoImageAlreadyLoadedException

# CONSTANTS:
logger = logging.getLogger("vsco.py")

HOST = "https://vsco.co"


class Requester:
    def __init__(self):
        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0 Safari/537.36"
        }

    def get(self, url, **kwargs):
        headers = kwargs.get("headers") if kwargs.get("headers") else dict()
        headers.update(self.base_headers)
        return requests.get(url, headers=headers, **kwargs)

    def post(self, url, **kwargs):
        headers = kwargs.get("headers") if kwargs.get("headers") else dict()
        headers.update(self.base_headers)
        return requests.post(url, headers=headers, **kwargs)


class VscoImage:
    def __init__(self):
        self.requests = Requester()

        self.im: Union[None, Image.Image] = None

        self.id: str = ''
        self.gridName: str = ''
        self.adaptiveBase: str = ''
        self.siteId: int = -1
        self.description: str = ''
        self.descriptionAnchored: str = ''
        self.copyrightClasses: list[str] = []
        self.captureDate: int = -1
        self.captureDateMs: int = -1
        self.uploadDate: int = -1
        self.lastUpdated: int = -1
        self.locationCoords = None
        self.hasLocation: bool = False
        self.featureLink = None
        self.isFeatured: bool = False
        self.isVideo: bool = False
        self.permaDomain: str = ""
        self.permaSubdomain: str = ""
        self.permalink: str = ""
        self.shareLink: str = ""
        self.responsiveUrl: str = ""
        self.showLocation: int = 0
        self.imageStatus: dict = {}
        self.imageMeta: dict = {}
        self.height: int = -1
        self.width: int = -1

    def from_adaptive_base(self, im_id):
        """
        Sets self.im given an image id.
        :param im_id: The uuid to the image.
        :return: None
        """
        request = self.requests.get(f"{HOST}/i/{im_id}")
        if request.status_code != 200:
            raise VscoRequestException("Image not found.")
        self.im = Image.open(BytesIO(request.content))

    def from_media_data(self, data):
        im_data = data.get("image")

        self.id = im_data.get("_id")
        self.gridName = im_data.get("grid_name")
        self.adaptiveBase = im_data.get("adaptive_base")
        self.siteId = im_data.get("site_id")
        self.description = im_data.get("description")
        self.descriptionAnchored = im_data.get("description_anchored")
        self.copyrightClasses = im_data.get("copyright_classes")
        self.captureDate = im_data.get("capture_date")
        self.captureDateMs = im_data.get("capture_date_ms")
        self.uploadDate = im_data.get("upload_date")
        self.lastUpdated = im_data.get("last_updated")
        self.locationCoords = im_data.get("location_coords")
        self.hasLocation = im_data.get("has_location")
        self.featureLink = im_data.get("feature_link")
        self.isFeatured = im_data.get("is_featured")
        self.isVideo = im_data.get("is_video")
        self.permaDomain = im_data.get("perma_domain")
        self.permaSubdomain = im_data.get("perma_subdomain")
        self.permalink = im_data.get("permalink")
        self.shareLink = im_data.get("share_link")
        self.responsiveUrl = im_data.get("responsive_url")
        self.showLocation = im_data.get("show_location")
        self.imageStatus = im_data.get("image_status")
        self.imageMeta = im_data.get("image_meta")
        self.height = im_data.get("preset")
        self.width = im_data.get("height")

        return self

    def from_preload_data(self, data):
        self.id = data.get("id")
        self.gridName = data.get("gridName")
        self.adaptiveBase = data.get("adaptiveBase")
        self.siteId = data.get("siteId")
        self.description = data.get("description")
        self.descriptionAnchored = data.get("descriptionAnchored")
        self.copyrightClasses = data.get("copyrightClasses")
        self.captureDate = data.get("captureDate")
        self.captureDateMs = data.get("captureDateMs")
        self.uploadDate = data.get("uploadDate")
        self.lastUpdated = data.get("lastUpdated")
        self.locationCoords = data.get("locationCoords")
        self.hasLocation = data.get("hasLocation")
        self.featureLink = data.get("featureLink")
        self.isFeatured = data.get("isFeatured")
        self.isVideo = data.get("isVideo")
        self.permaDomain = data.get("permaDomain")
        self.permaSubdomain = data.get("permaSubdomain")
        self.permalink = data.get("permalink")
        self.shareLink = data.get("shareLink")
        self.responsiveUrl = data.get("responsiveUrl")
        self.showLocation = data.get("showLocation")
        self.imageStatus = data.get("imageStatus")
        self.imageMeta = data.get("imageMeta")
        self.height = data.get("height")
        self.width = data.get("width")

        return self

    def load(self):
        """
        Gets the image data from the vsco servers and saves to self.im.
        :return: None
        """
        if self.im is not None:
            raise VscoImageAlreadyLoadedException("VscoImage.im is not None.")

        logger.debug(f"Getting image from {HOST}/{self.adaptiveBase}")

        request = self.requests.get(f"{HOST}/{self.adaptiveBase}")

        if request.status_code != 200:
            raise VscoRequestException("Error creating image")

        logger.debug(f"Loading image. {self.id}")
        self.im = Image.open(BytesIO(request.content))


class VscoProfile:
    def __init__(self):
        self.images: list[VscoImage] = []
        self.tkn = None
        self.cursor = ""
        self.siteId = None
        self.requests = Requester()

    def from_preload_data(self, data):
        images = data.get("entities", dict()).get("images")

        user_data = data.get('users', dict())
        current_user = user_data.get("currentUser")
        self.tkn = current_user.get("tkn")

        self.requests.base_headers.update({"Authorization": f"Bearer {self.tkn}"})

        self.cursor = list(data.get("medias", dict()).get("bySiteId", dict()).values())[0].get("nextCursor")
        self.siteId = list(data.get("medias", dict()).get("bySiteId", dict()).keys())[0]
        media = self._load_more(cursor=self.cursor, site_id=self.siteId)

        for media_im in media:
            im = VscoImage().from_media_data(media_im)
            self.images.append(im)

        for key, value in images.items():
            im = VscoImage().from_preload_data(value)
            self.images.append(im)
        return self

    def _load_more(self, cursor, site_id, media=None):
        """
        Recursive function to get all images from a given user's profile.
        """
        url = f"{HOST}/api/3.0/medias/profile?site_id={site_id}&limit=9999&cursor={cursor}"
        request = self.requests.get(url)

        if request.status_code != 200:
            raise VscoRequestException("Error making request to /api/3.0/medias/profile")

        data = request.json()
        next_cursor = data.get("next_cursor")

        if media:
            media += data.get("media")
        else:
            media = data.get("media")

        if next_cursor is not None and next_cursor != cursor:
            return self._load_more(cursor=next_cursor, site_id=site_id, media=media)

        return media

    def get_profile_images(self) -> list[VscoImage]:
        return self.images

    def load_all_images(self, threads: int = None):
        """
        Loads all images.
        :param threads: The number of threads used to load the images, set to None to not use multithreading
        :return: None
        """
        def load_im(img):
            try:
                img.load()
            except VscoImageAlreadyLoadedException:
                logger.debug("Image already loaded.")

        if threads is not None:
            futures = []
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for im in self.images:
                    futures.append(executor.submit(load_im, im))
                wait(futures)
        else:
            for im in self.images:
                load_im(im)


class VscoLoader:
    def __init__(self):
        self.authorization = None
        self.requester = Requester()

    def get_profile(self, key) -> VscoProfile:
        if isinstance(key, str):
            return self._get_profile_from_username(key)

    def _get_profile_from_username(self, username: str):
        request = self.requester.get(f"https://vsco.co/{username}/gallery")
        if request.status_code == 404:
            raise InvalidProfileException(f"No profile found with username \"{username}\"")

        preload_data = request.text.split("<script>window.__PRELOADED_STATE__ = ")[1].split("\n")[0].strip("</script>")
        loaded_preload_data = json.loads(preload_data)

        return VscoProfile().from_preload_data(loaded_preload_data)
