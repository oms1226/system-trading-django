import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os, sys, string, time


class aservice(win32serviceutil.ServiceFramework):
    _svc_name_ = "django"
    _svc_display_name_ = "django"
    _svc_description_ = "django"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        import servicemanager
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.timeout = 640000  # 640 seconds / 10 minutes (value is in milliseconds)  # self.timeout = 120000     #120 seconds / 2 minutes
        # This is how long the service will wait to run / refresh itself (see script below)

        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("SomeShortNameVersion - STOPPED!")  # For Event Log
                break
            else:
                t = time.localtime()
                if t.tm_min == 0 or t.tm_min == 30:
                    # Ok, here's the real money shot right here.
                    # [actual service code between rests]
                    try:
                        file_path = "%py32% %conoha%\system-trading-django\twisted_run.tac"
                        # execfile(file_path)  # Execute the script
                        exec(open(file_path).read())
                    except:
                        pass
                        # [actual service code between rests]
                else:
                    pass


def ctrlHandler(ctrlType):
    return True


if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(aservice)
