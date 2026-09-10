import os, sys
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/opencode/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/opencode/numba")

import contextlib
import traceback

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
from nethackers.contracts.models import Objective

from autoascend import agent as autoascend_agent

sys.setrecursionlimit(100000)

LOG = open("/tmp/step_trace.log", "w")
ORIG_STEP = autoascend_agent.Agent.step
_count = {"i": 0}


def patched_step(self, action, additional_action_iterator=None):
    _count["i"] += 1
    i = _count["i"]
    if i <= 60:
        LOG.write(f"--- STEP {i} ---\n")
        LOG.flush()
    try:
        if i <= 60:
            LOG.write(f"  calling orig step action={action} has_blstats={hasattr(self,'blstats')}\n")
            LOG.write(f"  message={repr(getattr(self,'message',''))[:120]}\n")
            LOG.flush()
        rv = ORIG_STEP(self, action, additional_action_iterator)
        if i <= 60:
            LOG.write(f"  orig returned rv_type={type(rv).__name__} has_blstats={hasattr(self,'blstats')}\n")
            if hasattr(self, "blstats"):
                LOG.write(f"  bl hp={self.blstats.hitpoints}/{self.blstats.max_hitpoints} xl={self.blstats.experience_level}\n")
            LOG.flush()
        return rv
    except BaseException as e:
        LOG.write(f"  ORIG_STEP RAISED {type(e).__name__}: {e}\n")
        LOG.write(traceback.format_exc()[-2000:])
        LOG.flush()
        if i > 5:
            raise
        # keep going for the first few to see the pattern
        return 0


autoascend_agent.Agent.step = patched_step


class TraceEnv:
    def __init__(self, env):
        self._env = env

    @contextlib.contextmanager
    def debug_log(self, txt="", color=None):
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


def run(trajectory_id, character="mon-hum-neu-mal", cap=200):
    obj = Objective(character=character, max_steps=1_000_000,
                    no_progress_timeout=10_000)
    env = make_environment(obj.max_steps, obj.no_progress_timeout, obj.character)
    spec = trajectory_spec("public", "local", trajectory_id)
    env.reset(spec)
    wrapped = TraceEnv(env)
    ag = autoascend_agent.Agent(wrapped, seed=0, verbose=False, panic_on_errors=False)
    LOG.write(f"START traj={trajectory_id}\n")
    LOG.flush()
    # raise AgentFinished after cap steps via monkeypatch of main not needed; patch step
    global _count
    _count["i"] = 0
    orig_step_ref = autoascend_agent.Agent.step

    def capped_step(self, action, additional_action_iterator=None):
        if _count["i"] > cap:
            raise autoascend_agent.AgentFinished()
        return patched_step(self, action, additional_action_iterator)

    autoascend_agent.Agent.step = capped_step
    try:
        ag.main()
        LOG.write(f"MAIN_RETURNED step={ag.step_count}\n")
    except BaseException as e:
        LOG.write(f"MAIN_RAISED {type(e).__name__}: {e}\n")
        LOG.write(traceback.format_exc()[-2000:])
    finally:
        autoascend_agent.Agent.step = orig_step_ref
        LOG.write(f"FINAL step={ag.step_count} has_blstats={hasattr(ag,'blstats')} panics={len(ag.all_panics)}\n")
        LOG.flush()
        LOG.close()
        env.close()


if __name__ == "__main__":
    run(int(sys.argv[1]))
