# Petrification-safe combat

Consulted: [NetHack Wiki: Cockatrice](https://nethackwiki.com/wiki/Cockatrice)
(retrieved 2026-09-09).

Rule derived: touching a cockatrice without protection from petrification is
instantly fatal; a monk's unarmed attack is therefore not a valid combat action.
The combat controller must retreat or use a ranged attack until it has a
separately verified safe-contact capability.

Diagnostic evidence: the parent evaluation has two petrification deaths
(seeds 9 and 11).  Seed 9 reaches XP 10 and then dies specifically to a
cockatrice, showing that the existing generic melee action remains available
at the obstacle.  The combat action generator now removes contact attacks for
cockatrices and Medusa, while the movement layer classifies them as threats to
keep at range.
