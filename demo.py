import subprocess
import os

currentDir = os.path.dirname(os.path.realpath(__file__))
with open("{}/platforms.cfg".format(currentDir), "r") as f:
    fileTypes = f.read()

def gameList():
    games = []
    for root, dirs, files in os.walk("/home/pi/RetroPie/roms/"):
        for name in files:
            if name.split(".")[-1] in fileTypes:
                games.append(os.path.join(root, name))
    return games

def playGame(rom):
    name = rom.split("/")[-1]
    core = subprocess.Popen(["{}/search.sh".format(currentDir), name.split(".")[-1]],
                            stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    core = core.replace("Binary file ", "").replace(" matches", "").strip()
    p = subprocess.Popen(["{}/run.sh".format(currentDir), core, rom])
    try:
        p.wait(60)
        print(p.returncode)
        if p.returncode != 139:
            import sys
            sys.exit()
    except subprocess.TimeoutExpired:
        subprocess.call(["killall", "retroarch"])

if __name__ == "__main__":
    games = gameList()
    import random
    random.shuffle(games)
    for i in games:
        playGame(i)

