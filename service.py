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

if getattr(sys, "frozen", False):
    _LOG_DIR = os.path.dirname(sys.executable)
else:
    _LOG_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(_LOG_DIR, "observex_service.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        self.process = None
    def SvcStop(self):
        logging.info("Stopping ObserveX Service")
        self.ReportServiceStatus(
            win32service.SERVICE_STOP_PENDING
        )

        if self.process:
            try:
                self.process.terminate()
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
        self.main()

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

                    if self.process is None:

                        logging.info(f"Starting: {agent}")
                        agent_log.write(f"\n--- Launch at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                        agent_log.flush()

                       
                        agent_env = os.environ.copy()
                        agent_env["PYTHONUNBUFFERED"] = "1"

                        self.process = subprocess.Popen(
                            [agent],
                            cwd=os.path.dirname(agent),
                            stdout=agent_log,
                            stderr=subprocess.STDOUT,
                            env=agent_env
                        )
                    else:
                        rc = self.process.poll()
                        if rc is not None:
                            logging.error(f"Process exited with code {rc}")
                            self.process = None

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