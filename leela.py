import subprocess
import re
from debug import debug

CMD = [
    ".\\leela\\leela-zero-0.17-win64\\leelaz.exe",
    "--gtp",
    "--quiet",
    "--noponder",
    "--playouts", "1000",
    "--visits", "100",
    # LZ278 from https://zero.sjeng.org/network-profiles
    "--weights", "leela\\leelaz-model-swa-24-192000_quantized.txt",
]

OUTPUT_RE = re.compile("(?P<success>[=?])(?P<cmdno>\d*) (?P<output>.*)\n")

class Leela:
    def __init__(self):
        self.process = subprocess.Popen(
            CMD, 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=0,
        )
        self.cmdno=0
        self.cmd("known_command")
        debug("initialized")
        

    def cmd(self, command, wait=True):
        self.cmdno += 1
        self.process.stdin.write("{} {}\n".format(self.cmdno, command))
        while wait:
            ln = self.process.stdout.readline()
            match = OUTPUT_RE.match(ln)
            if match and match.group("cmdno") == str(self.cmdno):
                return match.group("output")#, match.group("success") == "="

    # def __del__(self):
    #     self.cmd("quit", wait=False)