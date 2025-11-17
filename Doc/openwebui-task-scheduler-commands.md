# OpenWebUI — Task Scheduler CLI Reference

This document collects the commands, run script, logging tips, and debugging steps we used to run OpenWebUI via Windows Task Scheduler (run at startup). Paste or save this file for future reference.

---

## Overview

We run OpenWebUI from a simple batch script (no `start` or detached launches) and use Task Scheduler to launch that script at system startup under the SYSTEM account. The batch sets the required environment variable, sets the working directory, and redirects stdout/stderr to a log so failures are visible.

Paths and values used in examples below:
- Install / script directory: `D:\Misc\Python311\Scripts`
- Run script: `D:\Misc\run_openwebui.bat`
- Log file: `D:\Misc\openwebui-task.log`
- Executable: `D:\Misc\Python311\Scripts\open-webui.exe`
- Port: `8080`
- Env var used in the examples: `OLLAMA_HOST=http://localhost:11434`
  - Note: your app may expect `OLLAMA_BASE_URL` — use whichever variable your OpenWebUI build expects.

---

## run_openwebui.bat (create this file)

Save as `D:\Misc\run_openwebui.bat` and test manually first.

```batch
@echo off
REM run_openwebui.bat - drop in D:\Misc\run_openwebui.bat
set WORKDIR=D:\Misc\Python311\Scripts
set EXE=%WORKDIR%\open-webui.exe
set LOG=D:\Misc\openwebui-task.log

REM Use the environment variable your app expects
set OLLAMA_HOST=http://localhost:11434

cd /d "%WORKDIR%"
echo =================================================>> "%LOG%"
echo [%date% %time%] Starting OpenWebUI (task) >> "%LOG%"
echo Command: "%EXE% serve --host 0.0.0.0 --port 8080" >> "%LOG%"
REM Run the server in foreground and append both stdout and stderr to the log
"%EXE%" serve --host 0.0.0.0 --port 8080 >> "%LOG%" 2>>&1
echo [%date% %time%] Process exited with errorlevel %ERRORLEVEL% >> "%LOG%"
```

How to test the batch manually (do this before creating the scheduled task)
- Open an elevated command prompt, then:
  cd /d D:\Misc
  D:\Misc\run_openwebui.bat
- Check the log:
  powershell -Command "Get-Content 'D:\Misc\openwebui-task.log' -Tail 200"

---

## Create the scheduled task (run at system startup as SYSTEM)

Create (or recreate) the scheduled task to run the above batch on system startup as the SYSTEM account:

- Delete old task (if present)
  schtasks /delete /tn "OpenWebUI" /f

- Create the task
  schtasks /create /tn "OpenWebUI" /tr "D:\Misc\run_openwebui.bat" /sc onstart /ru "SYSTEM" /rl HIGHEST /f

- Start it now (for testing)
  schtasks /run /tn "OpenWebUI"

---

## Restart / Stop / Delete task

- End the running task (graceful attempt)
  schtasks /end /tn "OpenWebUI"

- Start the task
  schtasks /run /tn "OpenWebUI"

- Delete the task
  schtasks /delete /tn "OpenWebUI" /f

If `/end` does not stop everything (child process may have exited), kill the process directly:
- List processes:
  tasklist /FI "IMAGENAME eq open-webui.exe" /V
- Kill by PID:
  taskkill /PID <pid> /T /F

---

## Inspect task status and last result

- Verbose task info (includes "Last Result"):
  schtasks /query /tn "OpenWebUI" /v /fo LIST

- Basic query:
  schtasks /query /tn "OpenWebUI"

Important: If a task shows "Running" but the server isn't reachable, check the "Last Result" and the log written by the batch — the task host can be running while the child process exits immediately.

---

## Confirm the server and networking

- Is the process running?
  tasklist /FI "IMAGENAME eq open-webui.exe" /V

- Or check for python if your server runs under `python.exe`:
  tasklist /FI "IMAGENAME eq python.exe" /V

- Is anything listening on port 8080?
  netstat -ano | findstr /R /C:":8080 .*LISTEN" || echo NOT LISTENING

- PowerShell alternative:
  Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Format-Table -AutoSize

If the server binds to `127.0.0.1:8080` instead of `0.0.0.0:8080`, it will be reachable locally but not from other machines.

---

## Firewall rule (allow external access to port 8080)

Allow port 8080 through Windows Firewall (run elevated):

- Add rule
  netsh advfirewall firewall add rule name="OpenWebUI 8080" dir=in action=allow protocol=TCP localport=8080

- Show rules with 8080:
  netsh advfirewall firewall show rule name=all | findstr /I "8080" || echo "no rule"

---

## Logs

- Tail the run script log:
  powershell -Command "Get-Content 'D:\Misc\openwebui-task.log' -Tail 200"

The batch writes both stdout and stderr to the log so you can diagnose immediate failures (missing dependency, binding error, etc.). Check the timestamped headers the batch writes to see when attempts happened.

If logs grow large, consider simple rotation (example: move old log to `.yyyy-mm-dd.log` and start a new one daily, or copy last N lines into a new file). I can provide a rotation script if you want.

---

## Common troubleshooting notes

- Wrong env var: ensure the run script sets the env variable the app expects — we used `OLLAMA_HOST` in the batch because it matched your manual CLI, but some builds expect `OLLAMA_BASE_URL`.
- Working directory: ensure the batch does `cd /d "%WORKDIR%"` so OpenWebUI finds its resources.
- Detached launchers: do not use `start` in the script — `start` detaches and will make Task Scheduler/NSSM lose track of the real server process.
- Task shows "Running" but server not reachable: check the log for immediate error output; the task host can remain "running" while the child process exits quickly.
- For interactive debugging, create the task to run under your user with "Run only when user is logged on" so you can see the console window.
- If you need auto-restart on failure, in Task Scheduler GUI go to Task Properties → Settings:
  - Check "If the task fails, restart every" and configure interval & attempts.
  - Choose "If the task is already running, do not start a new instance" to avoid collisions.

---

## Variant: Create task to run as a specific user (for debugging)

If you want to run the task under your user so you can see the window:

- Create (you will be prompted for password):
  schtasks /create /tn "OpenWebUI-User" /tr "D:\Misc\run_openwebui.bat" /sc onstart /ru "dennyrgood" /rl HIGHEST /f

Or use Task Scheduler GUI and set "Run only when user is logged on" for interactive troubleshooting.

---

## Quick checklist to perform if the website is not reachable

1. Confirm scheduled task status:
   schtasks /query /tn "OpenWebUI" /v /fo LIST

2. Check the run script log (`D:\Misc\openwebui-task.log`) for errors:
   powershell -Command "Get-Content 'D:\Misc\openwebui-task.log' -Tail 200"

3. Verify process is running:
   tasklist /FI "IMAGENAME eq open-webui.exe" /V

4. Verify listener:
   netstat -ano | findstr /R /C:":8080 .*LISTEN" || echo NOT LISTENING

5. Check firewall:
   netsh advfirewall firewall show rule name=all | findstr /I "8080"

6. If no process, re-run the task manually:
   schtasks /run /tn "OpenWebUI"

---

## Notes & next ideas

- Task Scheduler is a reliable, low-friction solution and works well for this setup. If you later want a proper "service wrapper" with native SCM behavior (stop/start mapped to process signals, built-in log rotation and restart policies), I can produce a WinSW XML or a small pywin32-based Windows Service that launches the same run command and handles graceful stops.
- If you want log rotation or an automated cleanup, I can add a PowerShell script and schedule it daily.

---

End of reference.