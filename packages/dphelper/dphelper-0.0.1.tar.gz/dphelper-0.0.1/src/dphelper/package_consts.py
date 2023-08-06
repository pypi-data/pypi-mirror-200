# Constants used by package

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
