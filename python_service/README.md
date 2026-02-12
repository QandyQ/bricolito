# My Python Background Service (Windows)

A minimal Windows service written in Python that runs in the background and logs a heartbeat every 5 seconds. This is a transparent, legitimate way to keep a process running without a visible window.

Note: You cannot make a process unkillable or disguise it as a critical system resource. Windows administrators can always stop services or processes. Use services for legitimate tasks only.

## Prerequisites
- Windows
- Python 3.10+

## Install dependencies
```powershell
pip install -r requirements.txt
```

## Install & manage the service
```powershell
# Install the service
python python_service\my_service.py install

# Start the service
python python_service\my_service.py start

# Check logs (created after start)
Get-Content python_service\logs\heartbeat.log -Wait

# Stop the service
python python_service\my_service.py stop

# Remove the service
python python_service\my_service.py remove
```

## Configure automatic restart on failure (optional)
Use the Services console (`services.msc`) -> find "My Python Background Service" -> Recovery tab -> set First/Second/Subsequent failures to "Restart the Service".

Or via `sc.exe` (requires admin):
```powershell
sc.exe failure MyPythonService reset= 0 actions= restart/60000
```

## Alternative: Invisible scheduled task
If you prefer no service, you can run a script with `pythonw.exe` (no console) using Task Scheduler:
- Create Task -> Run whether user is logged on or not -> Hidden -> Trigger at logon.
- Action: `pythonw.exe` with arguments `-u C:\path\to\your_script.py`.

## Ethics & limitations
- Do not attempt to bypass other apps' restrictions (e.g., exam software). This service is for legitimate automation on your own machine.
- Windows may still terminate services during shutdown or by admin action. There is no supported way to make a process impossible to stop.
