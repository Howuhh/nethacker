import os, sys
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/opencode/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/opencode/numba")

import contextlib

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
from nethackers.contracts.models import Objective

from autoascend import agent as autoascend_agent
from autoascend import exceptions as exc

sys.setrecursionlimit(100000)

STEP_LOG = open("/tmp/step_trace.log", "w")
ORIG_STEP = autoascend_agent.Agent.step


def patched_step(self, action, additional_action_iterator=None):
    if self.step_count % 500 == 0:
        try:
            bl = self.blstats
            STEP_LOG.write(f"step={self.step_count} turn={bl.time} dung={bl.dungeon_number} "
                           f"lvl={bl.level_number} xl={bl.experience_level} "
                           f"hp={bl.hitpoints}/{bl.max_hitpoints} pw={bl.energy}/{bl.max_energy} "
                           f"ac={bl.armor_class} str={bl.strength} dex={bl.dexterity} "
                           f"msg={repr(self.message)[:100]}\n")
            STEP_LOG.flush()
        except Exception as e:
            STEP_LOG.write(f"step={self.step_count} logerr={e}\n")
            STEP_LOG.flush()
    if self.step_count > 40000:
        raise exc.AgentFinished()
    return ORIG_STEP(self, action, additional_action_iterator)


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


def run(trajectory_id, character="mon-hum-neu-mal"):
    obj = Objective(character=character, max_steps=1_000_000,
                    no_progress_timeout=10_000)
    env = make_environment(obj.max_steps, obj.no_progress_timeout, obj.character)
    spec = trajectory_spec("public", "local", trajectory_id)
    env.reset(spec)
    wrapped = TraceEnv(env)
    ag = autoascend_agent.Agent(wrapped, seed=0, verbose=False, panic_on_errors=False)
    STEP_LOG.write(f"START traj={trajectory_id} panic_on_errors=False\n")
    STEP_LOG.flush()
    try:
        ag.main()
        STEP_LOG.write(f"MAIN_RETURNED step={ag.step_count} steps={ag.step_count} "
                       f"hasattr_blstats={hasattr(ag,'blstats')} panics={len(ag.all_panics)}\n")
    except BaseException as e:
        import traceback
        STEP_LOG.write(f"MAIN_RAISED {type(e).__name__}: {e}\n")
        STEP_LOG.write(traceback.format_exc()[-3000:])
    finally:
        try:
            STEP_LOG.write(f"FINAL step={ag.step_count} turns={ag.blstats.time} "
                           f"depth={ag.blstats.dungeon_number}/{ag.blstats.level_number} "
                           f"xl={ag.blstats.experience_level} hp={ag.blstats.hitpoints}/"
                           f"{ag.blstats.max_hitpoints} pw={ag.blstats.energy}/{ag.blstats.max_energy}\n")
        except Exception as fe:
            STEP_LOG.write(f"FINAL_ERR {fe}\n")
        STEP_LOG.flush()
        STEP_LOG.close()
        env.close()


if __name__ == "__main__":
    tid = int(sys.argv[1])
    run(tid)
