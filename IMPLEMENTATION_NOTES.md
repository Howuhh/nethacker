# Shop-door safety

Consulted: [NetHack Wiki: Shop](https://nethackwiki.com/wiki/Shop), especially
"Closed shops" (retrieved 2026-09-09).

Rule implemented: a closed shop has a locked door and the "Closed for
inventory" engraving; breaking that door angers its owner unless the player
immediately pays 400 zorkmids.  Generic exploration therefore treats a known
shop-adjacent closed door as unavailable, marks it explored, and leaves
unlocking/purchase decisions to a future explicit shopping plan.  This avoids
both shopkeeper hostility and repeatedly searching an intentionally skipped
doorway.

Diagnostic support: setting `AUTOASCEND_TRACE` writes a bounded action/state
trace outside the solution directory; `AUTOASCEND_TRACE_LIMIT` defaults to
50,000 actions.  It is inactive in normal arena evaluation.
