# Combat contact safety

Consulted: [NetHack Wiki — Cockatrice](https://nethackwiki.com/wiki/Cockatrice),
accessed 2026-09-09. The installed NLE exposes `BL_MASK_STONE`, matching the
article's stoning-resistance mechanic.

Rules implemented:

* A bare-handed attack against a cockatrice or chickatrice can invoke its
  passive skin-contact stoning attack. An unpolymorphed hero may melee only
  when wearing gloves, wielding a weapon, or stoning-resistant.
* An unprotected footrice is handled as a ranged/escape target: combat strongly
  prefers leaving adjacency and may engrave Elbereth when cornered.
* The generic UI yes/no handler declines only explicit `Really attack ...?`
  confirmations, preventing accidental shopkeeper hostility while preserving
  existing command-specific confirmation flows.
