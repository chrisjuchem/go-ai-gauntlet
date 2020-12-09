import subprocess
import re
from debug import debug, info

CMD = [
    ".\\leela\\leela-zero-0.17-win64\\leelaz.exe",
    "--gtp",
    "--quiet",
    "--noponder",
    "--resignpct", "0", # Never resign
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

    def cmd(self, command, wait=True, print_all=False):
        self.cmdno += 1
        full_cmd = "{} {}\n".format(self.cmdno, command)
        self.process.stdin.write(full_cmd)
        if print_all:
            info(full_cmd)
        while wait:
            if self.process.poll() is not None:
                raise RuntimeError("Leela failed :(")
            ln = self.process.stdout.readline()
            if print_all:
                info(ln)
            match = OUTPUT_RE.match(ln)
            if match and match.group("cmdno") == str(self.cmdno):
                return match.group("output")#, match.group("success") == "="

    # def __del__(self):
    #     self.cmd("quit", wait=False)

LEELA_INST = Leela()