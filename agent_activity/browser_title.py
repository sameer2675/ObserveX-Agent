BROWSER_PROCESSES = {"chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"}
BROWSER_TITLE_SUFFIXES = [
    " - Profile 1 - Google Chrome",
    " - Profile 2 - Google Chrome",
    " - Profile 3 - Google Chrome",
    " - Google Chrome",
    " - Profile 1 - Microsoft Edge",
    " - Microsoft Edge",
    " - Brave",
    " - Mozilla Firefox",
]


def is_browser_process(process_name):
    return (process_name or "").lower() in BROWSER_PROCESSES


def strip_browser_suffix(process_name, window_title):

    if not window_title or not is_browser_process(process_name):
        return window_title
    for suffix in BROWSER_TITLE_SUFFIXES:
        if window_title.endswith(suffix):
            return window_title[: -len(suffix)]
    return window_title