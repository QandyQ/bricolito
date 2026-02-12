import os
import time
import win32serviceutil
import win32service
import win32event
import servicemanager


class MyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyPythonService"
    _svc_display_name_ = "My Python Background Service"
    _svc_description_ = (
        "Simple background service that stays running and logs heartbeats."
    )

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.main()

    def main(self):
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "heartbeat.log")

        while self.running:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - running\n")
            # Wait up to 5 seconds, exit loop if stop event signaled
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break


if __name__ == "__main__":
    # Handle: install/start/stop/remove, e.g.:
    #   python my_service.py install
    #   python my_service.py start
    #   python my_service.py stop
    #   python my_service.py remove
    win32serviceutil.HandleCommandLine(MyPythonService)
