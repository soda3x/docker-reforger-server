import os
import subprocess

STABLE_BRANCH_APPID = "1874900"
EXPERIMENTAL_BRANCH_APPID = "1890870"

def select_branch() -> str:
    """
    If USE_EXPERIMENTAL is set to true, use the Experimental Reforger server branch
    """
    if os.environ["USE_EXPERIMENTAL"] == "true":
        return EXPERIMENTAL_BRANCH_APPID
    return STABLE_BRANCH_APPID

steamcmd = ["/home/reforger/steamcmd/steamcmd.sh"]
steamcmd.extend(["+force_install_dir", "/home/reforger/reforger_bins"])
steamcmd.extend(["+login", "anonymous"])
steamcmd.extend(["+app_update", select_branch()])
steamcmd.extend(["validate", "+quit"])
subprocess.call(steamcmd)

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
print(launch, flush=True)
os.system(launch)
