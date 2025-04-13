import os
import subprocess
import signal
import sys
from datetime import datetime

STABLE_BRANCH_APPID = "1874900"
EXPERIMENTAL_BRANCH_APPID = "1890870"

# Global process reference to kill server process later if needed
server_process = None

def handle_shutdown(signum, frame):
    signals = {
        signal.SIGTERM: "SIGTERM", # Dockers sig for terminating container
        signal.SIGINT: "SIGINT" # CTRL + C Exit
    }
    signal_name = signals.get(signum, f"Signal {signum}")
    print(f"\n[!] Received {signal_name}. Exiting gracefully...\n", flush=True)

    if server_process and server_process.poll() is None:
        print("[!] Terminating server subprocess...", flush=True)
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)

    server_process.wait()
    sys.exit(0)

# Handling graceful exits
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

# Retrieve the maximum amount of acceptable restarts before calling the time of death (None will allow infinite restarts, 0 disables auto-restart function)
def get_max_restarts():
    val = os.environ.get("MAX_RESTARTS", "")
    if val and val.strip():
        val = val.strip()
        if val.isdigit():
            print(f"MAX_RESTARTS Set to: {int(val)}")
            return int(val)
        elif val.lower() == "none":
            print(f"MAX_RESTARTS Set to: infinite restarts")
            return None
    print(f"MAX_RESTARTS Set to: disabled")
    return 0

def select_branch() -> str:
    """
    If USE_EXPERIMENTAL is set to true, use the Experimental Reforger server branch
    """
    if os.environ["USE_EXPERIMENTAL"].lower() == "true":
        return EXPERIMENTAL_BRANCH_APPID
    return STABLE_BRANCH_APPID

# Verifies build for updates or missing installation and retrieves it
def update_server():
    steamcmd = ["/home/reforger/steamcmd/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/home/reforger/reforger_bins"])
    steamcmd.extend(["+login", "anonymous"])
    steamcmd.extend(["+app_update", select_branch()])
    steamcmd.extend(["validate", "+quit"])
    subprocess.run(steamcmd)

# Builds full launch command with mandatory parameters and checks for optional parameters
def build_launch_command() -> list:
    launch = [
        "/home/reforger/reforger_bins/ArmaReforgerServer",
        f"-config", f"/home/reforger/configs/{os.environ['CONFIG']}.json",
        "-createDB",
        "-nothrow",
        f"-maxFPS", os.environ["MAX_FPS"],
        "-profile", "/home/reforger/profile",
        "-addonDownloadDir", "/home/reforger/workshop",
        "-addonsDir", "/home/reforger/workshop",
        "-freezeCheck", os.environ["FREEZE_CHECK"],
        "-freezeCheckMode", "crash"
    ]

    startup_parameters = os.environ.get("STARTUP_PARAMETERS", "")
    if startup_parameters and startup_parameters.strip():
        launch.extend(startup_parameters.strip().split())

    return launch

# Main launch.py loop with auto-restart
def main():
    update_server()

    max_restarts = get_max_restarts()
    restart_count = 0

    while True:
        launch = build_launch_command()
        print(f"Launching server:\n{' '.join(launch)}\n", flush=True)

        server_process = subprocess.Popen(
            launch,
            preexec_fn=os.setsid
        )

        exit_code = server_process.wait()

        if exit_code == 0:
            print("Server exited gracefully. Exiting launch.py loop.", flush=True)
            break
        else:
            restart_count += 1
            print(f"Server crashed (exit code {exit_code}).", flush=True)
            if max_restarts is not None and restart_count >= max_restarts:
                death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Reached max restart attempts ({max_restarts}). Giving up.\nTime of death: [{death_time}]")
                break

if __name__ == "__main__":
    main()
