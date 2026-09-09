# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
# Threats whose melee damage can kill a weakened early-game character in one
# exchange, even though they are not fast or insects.
HIGH_DAMAGE_MONSTERS = ['ape', 'gargoyle', 'owlbear', 'rope golem',
                        'tiger', 'winter wolf']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']
# A footrice is not merely a high-damage monster.  A weaponless attack can
# invoke its passive stoning attack, and its own touch attack can start the
# delayed-stoning countdown.  Keep this separate from the ordinary damage
# classifications so all combat action selection can enforce the hard rule.
PETRIFYING_MONSTERS = ['cockatrice', 'chickatrice']


def is_petrifying_monster(monster):
    return monster[3].mname in PETRIFYING_MONSTERS


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # hypothesis: using the monster's actual movement speed prevents low-HP
    # monks from trying to outrun fast threats such as ants and underestimating Elbereth.
    return mon.mmove > 12


def imminent_death_on_melee(agent, monster):
    if is_petrifying_monster(monster):
        return True
    if monster[3].mname == 'mumak':
        return agent.blstats.hitpoints <= 60
    if is_dangerous_monster(monster):
        # hypothesis: scaling the danger cutoff with max HP keeps a monk from
        # entering lethal melee after gaining levels, when 16 HP is no longer
        # a meaningful fraction of the damage an adjacent threat can deal.
        return agent.blstats.hitpoints <= max(16, 0.55 * agent.blstats.max_hitpoints)
    return agent.blstats.hitpoints <= 8


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # hypothesis: treating a mumak's full 60-damage attack round as imminently
    # lethal makes monks kite this slow monster instead of entering fatal melee.
    is_mumak = mon.mname == 'mumak'
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    # hypothesis: classifying high-damage mid-dungeon monsters as dangerous
    # makes low-HP combat kite or engrave instead of committing to melee.
    return is_pet or is_mumak or mon.mname in INSECTS or mon.mname in HIGH_DAMAGE_MONSTERS or \
           is_petrifying_monster(monster)


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
