# Monk spell preparation

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
