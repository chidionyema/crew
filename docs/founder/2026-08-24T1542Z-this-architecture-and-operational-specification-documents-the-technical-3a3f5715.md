---
captured: 2026-08-24T15:42:39+00:00
session: a6b4167c-c8f2-43e2-9d31-d26e66f642c9
cwd: /Users/chidionyema/Library/LaunchAgents
chars: 3446
source: founder prompt, verbatim (founder-doc-capture.py)
---

This architecture and operational specification documents the technical solutions for containing, monitoring, and limiting autonomous AI agent subprocesses across host, workstation, and enterprise container layers.Tier 1: Immediate Host Remediation RunbookPurposeForce-terminate orphaned Chrome Helper, Playwright, and Node.js child processes without affecting primary user desktop applications.Remediation ScriptsOperating SystemDetection CommandTermination CommandmacOS / Linux`pgrep -fl "ChromechromiumWindows (PowerShell)Get-Process | Where-Object { $_.ProcessName -match "chrome" }Stop-Process -Name "chrome" -ForceTier 2: Workstation Guardrails (Host OS Layer)1. Global Binary Interceptor (PATH Injection)Applies parameter enforcement to command-line tools executed by any AI agent framework.Create interceptor binary at /usr/local/agent-guard/bin/find:Bash#!/bin/bash
# Enforces safe traversal depth while preserving parameter spaces
if [[ ! " $@ " =~ " -maxdepth " ]]; then
    /usr/bin/find . -maxdepth 3 "$@"
else
    /usr/bin/find "$@"
fi
Deployment:Bashsudo chmod +x /usr/local/agent-guard/bin/find
echo 'export PATH="/usr/local/agent-guard/bin:$PATH"' | sudo tee -a /etc/zshenv
2. Native macOS Watchdog Service (launchd)Monitors overall CPU and RAM thresholds and terminates headless agent sub-processes that exceed limits.Daemon Script (/usr/local/bin/agent_watchdog.sh):Bash#!/bin/bash
MAX_CPU=80
MAX_MEM=70

while true; do
    PIDS=$(ps -eo pid,%cpu,%mem,command | awk -v cpu=$MAX_CPU -v mem=$MAX_MEM \
    '$2 > cpu || $3 > mem {
        if ($4 ~ /node|python|qemu/ || ($0 ~ /chrome/ && $0 ~ /headless/)) 
        print $1
    }')

    for PID in $PIDS; do
        if [ -n "$PID" ]; then
            echo "$(date): Terminated runaway process PID $PID" >> /var/log/agent_watchdog.log
            kill -9 "$PID"
        fi
    done
    sleep 10
done
Service Configuration (/Library/LaunchDaemons/com.enterprise.agentwatchdog.plist):XML<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.plist">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.enterprise.agentwatchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/agent_watchdog.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
Tier 3: Enterprise Container Sandbox Specification1. Hardened OCI DevContainer SpecificationEnforces kernel-level execution boundaries, cgroup limits, and cap dropping.Configuration (.devcontainer/devcontainer.json):JSON{
  "name": "Sandboxed Agent Workspace",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "runArgs": [
    "--memory=6g",
    "--cpus=4.0",
    "--pids-limit=100",
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges:true",
    "--read-only",
    "--tmpfs=/tmp:rw,noexec,nosuid"
  ],
  "remoteUser": "vscode"
}
2. Linux Transient Scope Control (systemd)For native Linux environments, executes agents inside isolated cgroup scopes without container overhead.Bashsystemd-run --scope --user \
  --unit=agent-execution-scope \
  -p MemoryMax=6G \
  -p CPUQuota=400% \
  -p TasksMax=100 \
  claude-code
3. Hypervisor Hard Pinning (Colima)Constrains total hardware consumption for Kubernetes/Docker agent workloads on macOS.Bashcolima start --kubernetes --cpus 4 --memory 8
 review and inpleent needs separate repo
