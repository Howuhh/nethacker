from ..glyph import MON


# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # TOOD: implement properly
    return 'bat' in mon.mname or 'dog' in mon.mname or 'cat' in mon.mname \
           or 'kitten' in mon.mname or 'pony' in mon.mname or 'horse' in mon.mname \
           or 'bee' in mon.mname or 'fox' in mon.mname


def imminent_death_on_melee(agent, monster):
    if is_dangerous_monster(monster):
        return agent.blstats.hitpoints <= 16
    return agent.blstats.hitpoints <= 8


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # hypothesis: treating hostile orcs and elves as dangerous lets the existing retreat,
    # Elbereth, and wand heuristics prevent the repeated hill-orc/Green-elf deaths.
    is_hostile_race = getattr(mon, 'mflags2', 0) & (MON.M2_ORC | MON.M2_ELF)
    # hypothesis: treating experienced, intrinsically strong monsters as dangerous triggers
    # escape tools for high-damage threats without spending them on low-level strong species.
    is_strong = getattr(mon, 'mflags2', 0) & MON.M2_STRONG and getattr(mon, 'mlevel', 0) >= 6
    # hypothesis: treating fast monsters as dangerous makes every Valkyrie start
    # retreating or using ranged options before rats, bats, and spiders get repeated hits.
    is_fast = getattr(mon, 'mmove', 0) > 12
    # hypothesis: treating spiders as dangerous makes Valkyries use their existing
    # defensive combat options before a poisonous or fast arachnid can end an early run.
    is_spider = 'spider' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    return is_pet or mon.mname in INSECTS or bool(is_hostile_race) or bool(is_strong) or is_fast or is_spider


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
