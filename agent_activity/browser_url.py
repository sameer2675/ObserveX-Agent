import sqlite3
import os
import shutil
import uuid
import re
 
try:
    import uiautomation as auto
    UIAUTOMATION_AVAILABLE = True
except ImportError:
    UIAUTOMATION_AVAILABLE = False
    print("Warning: 'uiautomation' package not installed. "
          "Run 'pip install uiautomation' for live tab detection. "
          "Falling back to history-based detection only.")

BROWSER_PATHS = {
    "chrome.exe": [
        r"~\AppData\Local\Google\Chrome\User Data\Default\History",
        r"~\AppData\Local\Google\Chrome\User Data\Profile 1\History",
        r"~\AppData\Local\Google\Chrome\User Data\Profile 2\History",
        r"~\AppData\Local\Google\Chrome\User Data\Profile 3\History",
    ],
    "msedge.exe": [
        r"~\AppData\Local\Microsoft\Edge\User Data\Default\History",
        r"~\AppData\Local\Microsoft\Edge\User Data\Profile 1\History",
    ],
    "brave.exe": [
        r"~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History",
    ],
}
BROWSER_SUFFIXES = [
    " - Google Chrome",
    " - Profile 1 - Google Chrome",
    " - Microsoft Edge",
    " - Brave",
] 
def _clean_title(title):
    if not title:
        return ""
    for suffix in BROWSER_SUFFIXES:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
            break
    return title.strip().lower()

def _normalize(text):
    return re.sub(r"\s+", " ", (text or "")).strip().lower()
  
def _looks_like_url(text):
  
    if not text:
        return False
    text = text.strip()
    if " " in text and "://" not in text:       
        return False
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", text)) or bool(
        re.match(r"^[\w.-]+\.[a-zA-Z]{2,}(/.*)?$", text)
    )

def get_current_tab_url_live(hwnd):
    try:
        window = auto.ControlFromHandle(hwnd)
        if not window:
            return None
        edits = window.GetChildren()
        for control in edits:
            try:
                if control.ControlTypeName == "EditControl":
                    value = control.GetValuePattern().Value
                    if value.startswith("http"):
                        return value
            except:
                pass
        for control, depth in auto.WalkControl(window):
            try:
                if control.ControlTypeName == "EditControl":
                    value = control.GetValuePattern().Value
                    if value.startswith("http"):
                        return value
            except:
                pass
    except Exception as e:
        print(e)
    return None

def _get_url_from_history(browser_name, window_title):
    paths = BROWSER_PATHS.get(browser_name, [])
    target_title = _normalize(_clean_title(window_title))
    for path in paths:
        history_path = os.path.expanduser(path)
        if not os.path.exists(history_path):
            continue
        temp = f"history_temp_{uuid.uuid4().hex}.db"
        temp_wal = f"{temp}-wal"
        temp_shm = f"{temp}-shm"
        wal_source = history_path + "-wal"
        shm_source = history_path + "-shm"
        copied_files = []
        try:
            shutil.copy2(history_path, temp)
            copied_files.append(temp)
            if os.path.exists(wal_source):
                shutil.copy2(wal_source, temp_wal)
                copied_files.append(temp_wal)
            if os.path.exists(shm_source):
                shutil.copy2(shm_source, temp_shm)
                copied_files.append(temp_shm)
            conn = sqlite3.connect(temp)
            cursor = conn.cursor()
            if target_title:
                cursor.execute(
                    """
                    SELECT url, title
                    FROM urls
                    WHERE title LIKE ?
                    ORDER BY last_visit_time DESC
                    LIMIT 20
                    """,
                    (f"%{window_title.strip()}%",),
                )
                rows = cursor.fetchall()

                for url, title in rows:
                    if not url or not url.startswith("http"):
                        continue
                    norm_title = _normalize(title)
                    if (
                        norm_title == target_title
                        or target_title in norm_title
                        or norm_title in target_title
                    ):
                        conn.close()
                        return {"url": url, "title": title}
 
            
            cursor.execute(
                """
                SELECT url, title
                FROM urls
                WHERE url LIKE 'http%'
                ORDER BY last_visit_time DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return {"url": row[0], "title": row[1]}
        except Exception as e:
            print("Browser Error:", e)
        finally:
            for f in copied_files:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception:
                        pass
 
    return None
 
def get_url_browsers(browser_name=None, window_title=None, hwnd=None):
  
    if browser_name is None:
        return None
    browser_name = browser_name.lower()
    if hwnd is not None:
        live_url = get_current_tab_url_live(hwnd)
        if live_url:
            return {"url": live_url, "title": window_title} 
    return _get_url_from_history(browser_name, window_title)
 