# Monk spell preparation

## Preemptive healing against lethal melee

Hypothesis: the standard emergency policy waited for one-third maximum HP,
which is too late when a known adjacent monster can kill the Monk in one melee
round.  The evaluation includes a Dlvl:12 death to a mumak; its 60-damage
attack makes this a categorical survival check rather than ordinary potion
optimization.

Rules consulted: NetHack Wiki, [Monk](https://nethackwiki.com/wiki/Monk) and
[Mumak](https://nethackwiki.com/wiki/Mumak), accessed 2026-09-09.  Monks have
poor HP growth but start with three healing potions; a mumak has a 4d12/4d12
attack routine that can do up to 60 damage.  Therefore a carried identified
healing potion is an appropriate planned reserve when that specific lethal
exchange is adjacent.

Implementation: emergency healing now asks the combat threat model whether an
adjacent visible monster makes melee imminently lethal.  It retains the normal
one-third-HP trigger for ordinary fights, but consumes an identified healing,
extra-healing, or full-healing potion before that exceptional exchange.
Observable check: an adjacent mumak at any HP up to 60 produces the quaff
action before fight2 chooses melee or movement.

Hypothesis: the prior monk reached Dlvl 8--14 but had no renewable defensive
resource, even on starts with an identified blessed spellbook of healing.
`Character.parse_spellcast_view` explicitly rejected every role except Healer,
and no code read spellbooks, so healing was unusable.

Rules consulted: NetHack Wiki, [Monk](https://nethackwiki.com/wiki/Monk),
accessed 2026-09-09.  The article lists the Monk's identified blessed starting
spellbook (healing, sleep, or protection), says Monks have Basic healing skill,
and recommends Protection before combat.  It also documents that Monks depend
on unarmored mobility and need supplementary defenses in the midgame.

The implementation treats the identified blessed/uncursed healing book as a
planned reserve: it studies it after the finite identified healing-potion stock
is exhausted, then parses the actual cast menu. It confirms a spell is learned
by its presence in that menu. Healing is cast at low HP before consuming a
potion, with at least 5 energy and <=20% displayed failure.
Protection and sleep are intentionally not studied or cast speculatively: their
turn cost needs a tactical planner, while healing has the direct success condition
of more HP before the next attack. The menu and failure checks recover safely
when healing is forgotten or cannot be cast.
