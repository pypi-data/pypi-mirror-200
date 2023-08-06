# Constants used by package

PACKAGE_NAME = "dphelper"
"Update this name after changing name in pyproject.toml"

REQUEST_DROP_ON_FAILURE_COUNT = 4
"How many `didnt connect` / `status >= 500` should occur sequentially before giving-up-on-request"

REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S = 3
"How many seconds to sleep after first request failure"

REQUEST_SLEEP_INCREASE_POWER = 2
"sleep time will be increased by this power. time ^ power"

BACKEND_URL = "https://data-platform-backend-4ddpl.ondigitalocean.app"
"url of server that stores snapshots, challenges, code runs. do not include ending slash"

BACKEND_SNAPSHOT_URL = f"{BACKEND_URL}/snapshots"
"backend url root for snapshots. it might be prepended in actual usage"

BACKEND_UTILS_URL = f"{BACKEND_URL}/v1/utils"
"backend url root for utils. it might be appended in actual usage"

HEADERS_AUTHORITY = {
    "authority": "www.something.lt",  # will be set by key `authority`
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,lt;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

HEADERS_ORIGIN_REFERER = {
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://www.something.lt",  # will be set by key `Origin`
    "Referer": "http://www.something.lt/things/",  # will be set by key `Referer`
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,pt;q=0.7,tr;q=0.6",
}
