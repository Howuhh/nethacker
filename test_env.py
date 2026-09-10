import os, sys
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/opencode/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/opencode/numba")

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh
from nle.nethack import actions as A

env = make_environment(1_000_000, 10_000, "mon-hum-neu-mal")
spec = trajectory_spec("public", "local", 11)
obs = env.reset(spec)
print("reset ok, blstats[0] (x,y):", obs["blstats"][0], obs["blstats"][1])

esc = int(A.Command.ESC)
print("ESC action int:", esc)
rv = env.step(esc)
print("step returned", len(rv), "values")
print("types:", type(rv[0]).__name__, type(rv[1]).__name__, type(rv[2]).__name__, type(rv[3]).__name__, type(rv[4]).__name__ if len(rv)>4 else "N/A")
print("terminated:", rv[2], "truncated:", rv[3])
print("msg:", bytes(rv[0]["message"]).decode().replace(chr(0),' ')[-80:])
env.close()
print("DONE")
