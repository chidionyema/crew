---
captured: 2026-08-24T12:52:11+00:00
session: 8ef72725-f30e-4d4b-8cb9-791f03f67fdf
cwd: /Users/chidionyema/dev/code/crew
chars: 4212
source: founder prompt, verbatim (founder-doc-capture.py)
---

Why a VM Persists in a Free‑Tier Mac Kubernetes Setup
Because Docker on macOS IS a virtual machine. There is no way around it.
Your Mac runs the XNU kernel (Darwin). Docker containers need the Linux kernel (cgroups, namespaces, overlayfs). These are fundamentally incompatible. Every Docker runtime on macOS — Docker Desktop, Colima, Lima, Podman Machine — runs a hidden Linux VM to host the Docker daemon.
The chain that forces the VM:
plain
Your k8s manifests → need a cluster → you chose k3d → k3d needs Docker → Docker on macOS needs a Linux VM → limactl/colima runs that VM
Why this is killing you:
Your Mac has 12 cores and 16GB RAM. Right now it is running:
The Lima/Colima VM (reserving 2-4 cores, 4-8GB RAM)
18 Docker containers (8 unhealthy, k3d-serverlb restart-looping)
14 launchd jobs
4 Claude sessions
Load average: 14.29 (your machine is drowning)
The VM is not optional. It is the price of choosing Kubernetes on a Mac. The real question is not "why a VM" — it is "why are we trying to run a full Kubernetes cluster on a laptop that is already the production substrate for 14 other jobs?"
The honest options:
Table
Option    VM?    Viable?
Keep k3d locally    Yes    No. Machine is dead.
Remote free cluster (Oracle Always Free ARM)    No    Yes. But violates "Mac substrate" ruling unless you reframe it.
Run containers as native macOS processes    No    Partial. Your 7 compose services could be launchd jobs. k8s cannot.
Defer k8s until substrate is ready    N/A    Yes. Fix launchd, free the machine, then boot k3d.
The one-line truth: You are running a VM because you declared Kubernetes as your platform and Kubernetes does not run on macOS natively. The VM is not the problem. The problem is trying to boot a cluster on a machine that is already your production environment.
What do you want: keep fighting the VM, or question whether k8s belongs on this machine at all?
running a VM is not the issue, wh y is it huggin all resources
Edit
Copy
Share
Diagnose VM Resource Drain from k3d Bootstrap Failure and Overlay
Because the k3d cluster died and left wreckage burning CPU in a restart loop, while store-drill.sh holds the rest.
The exact resource consumers, measured on your machine:
Table
Consumer    What it is doing    Resource cost
k3d-prospector-rehearsal-serverlb    Restart-looping. 78 restarts and counting. Every crash = new container + kubelet retry + log writes.    CPU + disk I/O
k3d-prospector-rehearsal-server-0    Alive but kine (SQLite-on-overlayfs) taking 2.8s per INSERT. Bootstrap never finished.    Disk I/O saturation
store-drill.sh    Running a Docker container for the store-api security drill. Holding the VM.    CPU + memory
8 unhealthy containers    From previous failed attempts. Not cleaned up.    Memory leak
Docker overlayfs    Docker Desktop's filesystem driver. Slow on macOS VM. kine writes through it.    Disk I/O bottleneck
Why the VM is "hungry":
The VM isn't oversized. It's drowning in retry traffic. A restart loop is worse than a running container — it creates, destroys, and recreates containers faster than the garbage collector cleans them up. Each restart writes to kine (SQLite), and kine writes to Docker's overlayfs, which is already the slowest path on macOS.
The fix is not "give the VM more resources." The fix is "stop the restart loop and kill the drill."
bash
# 1. Kill the drill (frees CPU + one container slot)
pkill -f store-drill.sh

# 2. Kill the restart-loop wreckage
docker stop k3d-prospector-rehearsal-serverlb
docker rm k3d-prospector-rehearsal-serverlb

# 3. Prune the dead
docker system prune -f

# 4. Boot clean with the fix that prevents the loop
./deploy/rehearse_cluster.sh up
The --disable=traefik,servicelb fix in rehearse_cluster.sh removes the two Helm installs that were drowning kine. Without them, the bootstrap finishes before the 240s timeout, and the serverlb never enters the restart loop.
Run those 4 commands. The VM will stop "hugging" resources.
but again we are fire figting, this is why i insist we do it on the nac book, we need best practices fron day0, trusing these cowboys to deploy to real infra withut knwing exctly how everything works is the biggest risk. its not ptional it needs to be done
