import os
import sys
import time
import subprocess
import logging
import win32timezone
import win32event
import win32service
import win32serviceutil
import servicemanager
import win32ts
import win32security
import win32process
import win32profile
import win32con
import pywintypes

if getattr(sys, "frozen", False):
    LOG_DIR = os.path.dirname(sys.executable)
else:
    LOG_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "observex_service.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s")

def launch_in_user_session(exe_path, cwd):
    session_id = win32ts.WTSGetActiveConsoleSessionId()
    if session_id in (0xFFFFFFFF, None):
        return None
    try:
        user_token = win32ts.WTSQueryUserToken(session_id)
    except pywintypes.error:
        return None

    try:
        env = win32profile.CreateEnvironmentBlock(user_token, False)
        startup = win32process.STARTUPINFO()
        startup.dwFlags = win32process.STARTF_USESHOWWINDOW
        startup.wShowWindow = win32con.SW_HIDE

        priv_token = win32security.DuplicateTokenEx(
            user_token,
            win32security.SecurityImpersonation,
            win32con.MAXIMUM_ALLOWED,
            win32security.TokenPrimary,
            win32security.SECURITY_ATTRIBUTES()
        )

        proc_info = win32process.CreateProcessAsUser(
            priv_token,
            exe_path,
            None,
            None,
            None,
            False,
            win32process.CREATE_NEW_CONSOLE | win32process.NORMAL_PRIORITY_CLASS,
            env,
            cwd,
            startup
        )
        return proc_info  # (hProcess, hThread, pid, tid)
    finally:
        user_token.Close()


class ObserveXService(win32serviceutil.ServiceFramework):

    _svc_name_ = "ObserveXAgent"
    _svc_display_name_ = "ObserveX Agent Service"
    _svc_description_ = "We reduce Human Error"
    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(
            None,
            0,
            0,
            None
        )
        self.process_handle = None
        self.process_pid = None
    def SvcStop(self):
        logging.info("Stopping ObserveX Service")
        self.ReportServiceStatus(
            win32service.SERVICE_STOP_PENDING
        )

        if self.process_handle:
            try:
                win32process.TerminateProcess(self.process_handle, 0)
                self.process_handle.Close()
                logging.info("Main agent terminated")
            except Exception:
                logging.exception(
                    "Failed terminating agent"
                )
        win32event.SetEvent(
            self.stop_event
        )
    def SvcDoRun(self):
        servicemanager.LogInfoMsg(
            "ObserveX Service Started"
        )

        self.ReportServiceStatus(
            win32service.SERVICE_RUNNING
        )
        try:
            self.main()
        finally:
            
            self.ReportServiceStatus(
                win32service.SERVICE_STOPPED)
    def main(self):
        try:
            if getattr(sys, "frozen", False):
                SERVICE_DIR = os.path.dirname(
                    sys.executable
                )
            else:
                SERVICE_DIR = os.path.dirname(
                    os.path.abspath(__file__)
                )
            INSTALL_ROOT = os.path.dirname(SERVICE_DIR)

            agent = os.path.join(
                INSTALL_ROOT,
                "main",
                "main.exe"
            )
            BASE_DIR = INSTALL_ROOT
            logging.info(
                f"Agent path: {agent}"
            )
            if not os.path.exists(agent):

                logging.error(
                    "main.exe not found"
                )
                return
            agent_log_path = os.path.join(BASE_DIR, "main_agent_output.log")
            agent_log = open(agent_log_path, "a", encoding="utf-8")
            
            while True:
                try:

                    if self.process_handle is None:

                        logging.info(f"Starting: {agent}")
                        agent_log.write(f"\n--- Launch at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                        agent_log.flush()

                        proc_info = launch_in_user_session(agent, os.path.dirname(agent))
                        if proc_info is None:
                            logging.info("No interactive user session yet; will retry.")
                        else:
                            hProcess, hThread, pid, tid = proc_info
                            hThread.Close()
                            self.process_handle = hProcess
                            self.process_pid = pid
                            logging.info(f"Agent started in user session, pid={pid}")
                    else:
                        rc = win32process.GetExitCodeProcess(self.process_handle)
                        if rc != win32con.STILL_ACTIVE:
                            logging.error(f"Process exited with code {rc}")
                            self.process_handle.Close()
                            self.process_handle = None
                            self.process_pid = None

                    result = win32event.WaitForSingleObject(
                        self.stop_event,
                        5000
                    )
                    if result == win32event.WAIT_OBJECT_0:
                        logging.info(
                            "Stop signal received"
                        )
                        break
                except Exception:
                    logging.exception(
                        "Agent execution error"
                    )
                    time.sleep(5)

        except Exception:
            logging.exception(
                "Fatal Service Error"
            )
        finally:
         try:
           agent_log.close()
         except:
            pass

if __name__ == "__main__":
    if len(sys.argv) == 1:

        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ObserveXService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(
            ObserveXService
        )