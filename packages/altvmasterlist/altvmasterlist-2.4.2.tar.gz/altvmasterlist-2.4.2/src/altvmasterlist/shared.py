#!/usr/bin/env python3
from dataclasses import dataclass
from json import dumps, loads
from io import StringIO
import requests
import logging
import secrets

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


@dataclass
class MasterlistUrls:
    """This class is used for the masterlist submodule. It provides all urls needed."""
    base_link: str = "https://api.alt-mp.com"
    all_server_stats_link: str = f"{base_link}/servers"
    all_servers_link: str = f"{base_link}/servers/list"
    server_link: str = f"{base_link}/server" + "/{}"
    server_average_link: str = f"{base_link}/avg" + "/{}/{}"
    server_max_link: str = f"{base_link}/max" + "/{}/{}"


@dataclass
class AltstatsUrls:
    """This class is used for the altstats submodule. It provides all urls needed."""
    base_link: str = "https://api.altstats.net/api/v1/"
    all_server_stats_link: str = f"{base_link}/master"
    all_servers_link: str = f"{base_link}/server"
    server_link: str = f"{base_link}/server/" + "{}"


@dataclass
class RequestHeaders:
    """These are the common request headers used by the request function.
    They are commonly used to emulate an alt:V client.
    """
    host: str = "",
    user_agent: str = 'AltPublicAgent',
    accept: str = '*/*',
    alt_debug: str = 'false',
    alt_password: str = '17241709254077376921',
    alt_branch: str = "",
    alt_version: str = "",
    alt_player_name: str = secrets.token_urlsafe(10),
    alt_social_id: str = secrets.token_hex(9),
    alt_hardware_id2: str = secrets.token_hex(19),
    alt_hardware_id: str = secrets.token_hex(19)

    def __init__(self, version, debug="false", branch="release"):
        self.alt_branch = branch
        self.alt_version = version
        self.alt_debug = debug

    def __repr__(self):
        return dumps({
            'host': self.host,
            'user-agent': self.user_agent,
            "accept": self.accept,
            'alt-debug': self.alt_debug,
            'alt-password': self.alt_password,
            'alt-branch': self.alt_branch,
            'alt-version': self.alt_version,
            'alt-player-name': self.alt_player_name,
            'alt-social-id': self.alt_social_id,
            'alt-hardware-id2': self.alt_hardware_id2,
            'alt-hardware-id': self.alt_hardware_id
        })


def request(url: str, cdn: bool = False, server: any = None) -> dict | None:
    """This is the common request function to fetch remote data.

    Args:
        url (str): The Url to fetch.
        cdn (bool): Define if the request goes to an alt:V CDN. Then the emulated alt:V Client will be used.
        server (Server): An alt:V masterlist or altstats Server object.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        json: As data
    """
    # Use the User-Agent: AltPublicAgent, because some servers protect their CDN with
    # a simple User-Agent check e.g. https://luckyv.de does that
    if "http://" in url and cdn:
        req_headers = RequestHeaders(server.version, server.branch)
    else:
        req_headers = {
            'User-Agent': 'AltPublicAgent',
            'content-type': 'application/json; charset=utf-8'
        }

    try:
        api_data = requests.get(url, headers=req_headers, timeout=60)

        if api_data.status_code != 200:
            logging.warning(f"the request returned nothing.")
            return None
        else:
            return loads(api_data.content.decode("utf-8", errors='ignore'))
    except Exception as e:
        logging.error(e)
        return None


def get_dtc_url(use_cdn: bool, cdn_url: str, host: str, port: int, locked: bool, password: str = None) -> str | None:
    """This function gets the direct connect protocol url of an alt:V Server.
        (https://docs.altv.mp/articles/connectprotocol.html)

    Args:
        use_cdn (bool): Define if the Server is using a CDN.
        cdn_url (str): The CDN url of the server.
        host (str): The host IP adress of the server.
        port (int): The port of the server.
        locked (bool): Define if the server is locked. Locked servers have a password.
        password (str): The password of the server.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        str: The direct connect protocol url.
    """
    with StringIO() as dtc_url:
        if use_cdn:
            if "http" not in cdn_url:
                dtc_url.write(f"altv://connect/http://{cdn_url}")
            else:
                dtc_url.write(f"altv://connect/{cdn_url}")
        else:
            dtc_url.write(f"altv://connect/{host}:{port}")

        if locked and password is None:
            logging.warning(
                "Your server is password protected but you did not supply a password for the Direct Connect Url.")

        if password is not None:
            dtc_url.write(f"?password={password}")

        return dtc_url.getvalue()


def fetch_connect_json(use_cdn: bool, locked: bool, active: bool, host: str, port: int, cdn_url: str) -> dict | None:
    """This function fetched the connect.json of an alt:V server.

    Args:
        use_cdn (bool): Define if the Server is using a CDN.
        locked (bool): Define if the server is locked. Locked servers have a password.
        active (bool): Define if the server is active. Active means Online.
        host (str): The host IP adress of the server.
        port (int): The port of the server.
        cdn_url (str): The CDN url of the server.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        str: The direct connect protocol url.
    """
    if not use_cdn and not locked and active:
        # This Server is not using a CDN.
        cdn_request = request(f"http://{host}:{port}/connect.json", True)
        if cdn_request is None:
            # possible server error or blocked by alt:V
            return None
        else:
            return cdn_request
    else:
        # let`s try to get the connect.json
        cdn_request = request(f"{cdn_url}/connect.json")
        if cdn_request is None:
            # maybe the CDN is offline
            return None
        else:
            return cdn_request


class Permissions:
    """This is the Permission class used by get_permissions.

    Returns:
        Required: The required permissions of an alt:V server. Without them, you can not play on the server.
        Optional: The optional permissions of an alt:V server. You can play without them.
    """

    @dataclass
    class Required:
        """Required Permissions of an alt:V server.

        Attributes:
            screen_capture (bool): This allows a screenshot to be taken of the alt:V process (just GTA) and any webview
            webrtc (bool): This allows peer-to-peer RTC inside JS
            clipboard_access (bool): This allows to copy content to users clipboard
        """
        screen_capture: bool = False
        webrtc: bool = False
        clipboard_access: bool = False

    @dataclass
    class Optional:
        """Optional Permissions of an alt:V server.

        Attributes:
            screen_capture (bool): This allows a screenshot to be taken of the alt:V process (just GTA) and any webview
            webrtc (bool): This allows peer-to-peer RTC inside JS
            clipboard_access (bool): This allows to copy content to users clipboard
        """
        screen_capture: bool = False
        webrtc: bool = False
        clipboard_access: bool = False


def get_permissions(connect_json: dict) -> Permissions | None:
    """This function returns the Permissions defined by the server. https://docs.altv.mp/articles/permissions.html

    Args:
        connect_json (json): The connect.json of the server. You can get the connect.json from the Server object
                                e.g. Server(127).connect_json

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        Permissions: The permissions of the server.
    """
    if connect_json is None:
        return None

    optional = connect_json["optional-permissions"]
    required = connect_json["required-permissions"]

    permissions = Permissions()

    if optional is not []:
        try:
            permissions.Optional.screen_capture = optional["Screen Capture"]
        except TypeError:
            pass

        try:
            permissions.Optional.webrtc = optional["WebRTC"]
        except TypeError:
            pass

        try:
            permissions.Optional.clipboard_access = optional["Clipboard Access"]
        except TypeError:
            pass

    if required is not []:
        try:
            permissions.Required.screen_capture = required["Screen Capture"]
        except TypeError:
            pass

        try:
            permissions.Required.webrtc = required["WebRTC"]
        except TypeError:
            pass

        try:
            permissions.Required.clipboard_access = required["Clipboard Access"]
        except TypeError:
            pass

    return permissions


def get_resource_size(use_cdn: bool, cdn_url: str, resource: str, host: str, port: int, decimal: int) -> float | None:
    """This function returns the resource size of a server in MB.

    Args:
        use_cdn (bool): Define if the server is using a CDN.
        cdn_url (str): The CDN url of the server.
        resource (str): The name of the alt:V resource.
        host (str): The IP address of the server.
        port (int): The port of the server.
        decimal (int): The number of decimal point that you need.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        float: The size of the resource.
    """
    if use_cdn:
        resource_url = f"{cdn_url}/{resource}.resource"
    else:
        resource_url = f"http://{host}:{port}/{resource}.resource"

    data = requests.head(resource_url, headers={"User-Agent": "AltPublicAgent"}, timeout=60)

    if data.ok:
        return round((int(data.headers["Content-Length"]) / 1048576), decimal)
    else:
        return None
