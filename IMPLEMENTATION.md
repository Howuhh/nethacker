# Footrice contact safety

## Evidence and hypothesis

The parent evaluation has two otherwise-progressing monk runs (training seeds
9 and 11) ending in `petrified by a cockatrice`.  `Inventory.get_best_melee_weapon`
unconditionally returns `None` for monks, while the generic combat action still
selects adjacent melee.  Thus the bot attacks with bare hands.

## Rule and implementation

Consulted: [NetHack Wiki: Cockatrice](https://nethackwiki.com/wiki/Cockatrice)
(accessed 2026-09-09).  Its relevant rules are that a cockatrice has a passive
stoning attack on skin contact, ranged attacks are preferred, and unprotected
attack forms must not be used.  The bot therefore treats cockatrices and
chickatrices as lethal while unarmed.  It only permits adjacent melee after
equipping an identified blessed/uncursed weapon; otherwise it leaves movement,
Elbereth, wands, and ranged actions available.  The emergency weapon switch is
recorded as `footrice_safe_weapon` in the normal stats log.

This is intentionally conservative for monks: even gloves do not prove all of
their unarmed attack forms (notably kicks) are protected.
