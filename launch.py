import os
import subprocess

STABLE_BRANCH_APPID = "1874900"
EXPERIMENTAL_BRANCH_APPID = "1890870"

def select_branch() -> str:
    """
    If USE_EXPERIMENTAL is set to true, use the Experimental Reforger server branch
    """
    if os.environ["USE_EXPERIMENTAL"].lower() == "true":
        return EXPERIMENTAL_BRANCH_APPID
    return STABLE_BRANCH_APPID

def update_server():
    steamcmd = ["/home/reforger/steamcmd/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/home/reforger/reforger_bins"])
    steamcmd.extend(["+login", "anonymous"])
    steamcmd.extend(["+app_update", select_branch()])
    steamcmd.extend(["validate", "+quit"])
    subprocess.call(steamcmd)

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

def main():
    update_server()
    launch = build_launch_command()

    print(launch, flush=True)
    os.system(launch)

if __name__ == "__main__":
    main()
