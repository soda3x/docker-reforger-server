import os
import subprocess
from datetime import datetime

STABLE_BRANCH_APPID = "1874900"
EXPERIMENTAL_BRANCH_APPID = "1890870"

# Retrieve the maximum amount of acceptable restarts before calling the time of death (None will allow infinite restarts, 0 disables auto-restart function)
def get_max_restarts():
    val = os.environ.get("MAX_RESTARTS", "")
    if val and val.strip():
        val = val.strip()
        if val.isdigit():
            return int(val)
        elif val.lower() == "none":
            return None
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
def build_launch_command() -> str:
    launch = " ".join(
        [
            "/home/reforger/reforger_bins/ArmaReforgerServer",
            f"-config /home/reforger/configs/{os.environ['CONFIG']}.json",
            "-createDB",
            "-nothrow",
            f"-maxFPS {os.environ['MAX_FPS']}",
            f"-profile /home/reforger/profile",
            f"-addonDownloadDir /home/reforger/workshop",
            f"-addonsDir /home/reforger/workshop"
        ]
    )

    # Check for additional Startup parameters and append them
    startup_parameters = os.environ.get("STARTUP_PARAMETERS", "")
    if startup_parameters and startup_parameters.strip():
        launch += " " + startup_parameters.strip()

    return launch

# Main auto-restart loop
def main():
    update_server()

    max_restarts = get_max_restarts()
    restart_count = 0

    while True:
        launch = build_launch_command()
        print(f"Launching server:\n{launch}\n", flush=True)

        result = subprocess.run(launch, shell=True)

        if result.returncode == 0:
            print("Server exited cleanly. Stopping exiting launch.py auto-restart loop.", flush=True)
            break
        else:
            print(f"Server crashed (exit code {result.returncode}).", flush=True)
            if max_restarts is not None and restart_count >= max_restarts:
                death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Reached max restart attempts ({max_restarts}). Giving up.\nTime of death: [{death_time}]")
                break

if __name__ == "__main__":
    main()
