import sys
import os

os.environ.setdefault("XDG_CACHE_HOME", "/tmp/opencode/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/opencode/numba")

import contextlib

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
from nethackers.contracts.models import Objective

from autoascend import agent as autoascend_agent

sys.setrecursionlimit(100000)


class DebugEnv:
    """Wrap a real NLE env, adding debug_log/debug_tiles that print to stderr."""

    def __init__(self, env, verbose=False):
        self._env = env
        self.verbose = verbose
        self._dbg_count = 0

    @contextlib.contextmanager
    def debug_log(self, txt="", color=None):
        self._dbg_count += 1
        if self._dbg_count <= 5 or self._dbg_count % 2000 == 0:
            sys.stderr.write(f"DBG#{self._dbg_count}: {txt}\n")
            sys.stderr.flush()
        yield

    @contextlib.contextmanager
    def debug_tiles(self, *args, **kwargs):
        yield

    def step(self, action):
        return self._env.step(action)

    def reset(self, spec):
        return self._env.reset(spec)

    def __getattr__(self, name):
        return getattr(self._env, name)


def run(trajectory_id, character="mon-hum-neu-mal", max_steps=1_000_000,
        no_progress_timeout=10_000):
    obj = Objective(character=character, max_steps=max_steps,
                    no_progress_timeout=no_progress_timeout)
    env = make_environment(obj.max_steps, obj.no_progress_timeout, obj.character)
    spec = trajectory_spec("public", "local", trajectory_id)
    obs = env.reset(spec)
    sys.stderr.write(f"env type: {type(env).__name__} action_count={env.action_count}\n")
    wrapped = DebugEnv(env, verbose=False)
    ag = autoascend_agent.Agent(wrapped, seed=0, verbose=False, panic_on_errors=False)
    try:
        ag.main()
    except BaseException as e:
        sys.stderr.write(f"AGENT RAISED: {type(e).__name__}: {e}\n")
        raise
    finally:
        sys.stderr.write(f"steps={ag.step_count} turns={ag.blstats.time} "
                         f"depth={ag.blstats.dungeon_number}/{ag.blstats.level_number} "
                         f"hp={ag.blstats.hitpoints}/{ag.blstats.max_hitpoints} "
                         f"xl={ag.blstats.experience_level} "
                         f"dbg_calls={wrapped._dbg_count}\n")
        env.close()


if __name__ == "__main__":
    tid = int(sys.argv[1])
    sys.stderr.write(f"=== running trajectory {tid} ===\n")
    sys.stderr.flush()
    run(tid)
    sys.stderr.write(f"=== done trajectory {tid} ===\n")
