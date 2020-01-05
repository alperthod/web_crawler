BASE_PASTEBIN_URL = "https://pastebin.com"
RECENT_PASTES_URL = "%s/archive" % BASE_PASTEBIN_URL
PASTE_CONTENT_URL = "%s/raw{paste_id}" % BASE_PASTEBIN_URL

TABLE_CLASS_NAME = "maintable"
PASTE_INFO_CLASS = "paste_box_info"
PASTE_BOX_SECOND_LINE = "paste_box_line2"

TITLES_TO_NORMALIZE = {"Untitled"}

TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"

NUM_OF_THREADS = 1
TIME_TO_SLEEP = 60 * 2
