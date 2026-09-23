#!/usr/bin/env python3
"""
make-mage-levels.py - builds every level in Mage Run.

    python3 tools/make-mage-levels.py

Rebuilds the levels and writes them straight into mage-run.html. Nothing is
written unless every level passes the fairness checks below.

To add a world: add a colour theme to WORLDS, pick a boss for BOSSES, and
(optionally) new monsters in ARRIVES. The game has to know how to draw and
move any new monster or boss - that part is in mage-run.html.

The checks, which is why this exists instead of placing things by hand:
  - no pit wider than a double jump
  - no spike or monster where you land after a jump
  - no monster hovering over a pit, in your jump arc
  - every ledge and star can actually be reached
  - every monster type appears somewhere, and gets its "new!" level
"""
import random, sys

SINGLE_GAP, DOUBLE_GAP = 200, 225
LANDING  = 190          # keep spikes and creatures out of where you land
PIT_KEEP = 70           # and keep creatures away from the sides of a pit
MAX_RISE, MAX_SPAN = 220, 230

WORLDS = [
  # colours picked off the reference screenshots
  dict(name='Green Fields', crags=False,
       sky=['#3F8FCC', '#62AADB'], cloud='#EEF3F7', cloudShade='#C6ECF4', cloudBase='#74D4E7',
       far='#2F5A52', meadow='#6DAA5A', meadowDark='#548F47', meadowLight='#88C26E',
       rock='#8C91A6', rockLight='#B5BACB', rockDark='#5F6379',
       grass='#62BC3C', grassLight='#A2E856', grassDark='#3E8B2C',
       dirt='#583C5A', pebble='#6F4F71', pebbleDark='#432D45'),
  dict(name='Ember Reach', crags=True,
       sky=['#E3A96B', '#F0C68F'], cloud='', cloudShade='', cloudBase='',
       far='#C8684A', meadow='#8A4438', meadowDark='#6A3230', meadowLight='#A8573F',
       rock='#9E5A46', rockLight='#C9785A', rockDark='#6A3834',
       grass='#D98A48', grassLight='#F4B86C', grassDark='#A8612E',
       dirt='#4A2C30', pebble='#61393C', pebbleDark='#381F24', lava=True),
  dict(name='Frostfall', crags=True, snow=True,
       sky=['#16204A', '#3E5A9A'], cloud='', cloudShade='', cloudBase='',
       far='#6F86B8', meadow='#51689A', meadowDark='#3E5282', meadowLight='#7F97C7',
       rock='#8FA3C8', rockLight='#F2F7FF', rockDark='#5A6C94',
       grass='#E6F0FA', grassLight='#FFFFFF', grassDark='#A9BFD8',
       dirt='#3B4466', pebble='#4C5780', pebbleDark='#2C3350'),
  dict(name='Crystal Caverns', cave=True,
       sky=['#150C26', '#2E1A4A'], cloud='', cloudShade='', cloudBase='',
       far='#2A1B45', meadow='#34224F', meadowDark='#261840', meadowLight='#4A3270',
       rock='#5A4680', rockLight='#8A74B8', rockDark='#3A2A5A',
       grass='#3FD6C0', grassLight='#A8FFF2', grassDark='#1F8A80',
       dirt='#2A1B3E', pebble='#3C2A58', pebbleDark='#1C1230'),
]
BOSSES = ['skullking', 'magma', 'wraith', 'guardian']

# when each monster first turns up (global level number, 0 = world 1 level 1)
ARRIVES = dict(skull=0, bat=2, hopper=5, charger=10, spitter=13, knight=16,
               ghost=20, golem=23, bird=26, worm=30, shielder=33, turret=36)
GROUND_KINDS = ['skull', 'hopper', 'charger', 'spitter', 'knight', 'golem',
                'worm', 'shielder', 'turret']
AIR_KINDS    = ['bat', 'ghost', 'bird']
AIR_HEIGHT   = dict(bat=None, ghost=-120, bird=-230)
PER_WORLD = 10          # the tenth is the boss

def normal(wi, li, rnd):
    gi = wi * 10 + li
    hard = min(1.0, gi / 29.0)                       # ramps over the first three worlds
    maxgap = int(SINGLE_GAP + (DOUBLE_GAP - SINGLE_GAP) * hard)
    target = 3200 + li * 260 + wi * 900

    ground, x = [], 0
    while x < target:
        w = rnd.randrange(540, 1000, 20)
        ground.append([x, w])
        x += w + rnd.randrange(150, maxgap + 1, 10)
    goal = ground[-1][0] + ground[-1][1] - 200

    pits = [(g[0] + g[1], ground[i+1][0]) for i, g in enumerate(ground[:-1])]
    def near_pit(a, b):
        return any(a < pe + PIT_KEEP and b > ps - PIT_KEEP for ps, pe in pits)

    plats, stars, magic, spikes, foes = [], [], [], [], []
    ground_ok = [k for k in GROUND_KINDS if ARRIVES[k] <= gi]
    air_ok    = [k for k in AIR_KINDS    if ARRIVES[k] <= gi]
    newest    = max(ARRIVES, key=lambda k: ARRIVES[k] if ARRIVES[k] <= gi else -1)
    brand_new = newest if ARRIVES[newest] == gi else None
    def pick(options):
        # the newest kinds turn up more, the old ones still appear
        weights = [1 + 2 * (ARRIVES[k] / max(1, gi)) for k in options]
        return rnd.choices(options, weights)[0]
    placed_new = [False]
    for n, (gx, gw) in enumerate(ground):
        safe = gx + LANDING

        if gw > 620:
            lowX, lowY = gx + 150, -rnd.randrange(130, 161, 10)
            plats.append([lowX, lowY, 160])
            highX, highY = lowX + 220, lowY - rnd.randrange(100, 121, 10)
            plats.append([highX, highY, 140])
            magic.append([lowX + 80, lowY - 28])
            if len(stars) < 3 and n % 2 == 1:
                stars.append([highX + 70, highY - 105])
            # a bat guarding the way up to the high ledge — never over a pit
            # start the guard just past the landing zone. (It used to start at
            # lowX - 40, which is always inside the landing zone, so the
            # "ba > safe" test never passed and no flyer was ever placed.)
            ba = safe + 10
            bb = ba + 240
            if not near_pit(ba, bb) and bb < gx + gw - 60 and air_ok:
                kind = brand_new if brand_new in AIR_KINDS and not placed_new[0] else pick(air_ok)
                if kind == brand_new: placed_new[0] = True
                y = lowY + 55 if AIR_HEIGHT[kind] is None else AIR_HEIGHT[kind]
                foes.append([ba, bb, y, kind])

        if n < len(ground) - 1:
            plats.append([gx + gw + 40, -rnd.randrange(150, 191, 10), 120])

        for k in range(3 + min(wi, 2)):
            magic.append([gx + 120 + k * 60 + rnd.randrange(0, 30, 10), -28])

        if gw > 700 and n > 0:
            sx = rnd.randrange(safe + 120, gx + gw - 160, 20)
            if not near_pit(sx, sx + 80):
                spikes.append([sx, rnd.choice([60, 70, 80])])
        if n > 0:
            a = safe + 60
            b = min(gx + gw - 140, a + rnd.randrange(220, 400, 20))
            if b > a + 140 and not near_pit(a, b):
                kind = brand_new if brand_new in GROUND_KINDS and not placed_new[0] else pick(ground_ok)
                if kind == brand_new: placed_new[0] = True
                foes.append([a, b, 0, kind])
                # later worlds: a second creature on long stretches of grass
                if wi >= 1 and gw > 820:   # worlds 2 onwards
                    a2 = b + 60
                    b2 = min(gx + gw - 140, a2 + 220)
                    if b2 > a2 + 120 and not near_pit(a2, b2):
                        foes.append([a2, b2, 0, pick(ground_ok)])

    highs = sorted([p for p in plats if p[1] <= -230], key=lambda p: p[0])
    while len(stars) < 3 and highs:
        p = highs.pop(len(highs)//2)
        c = [p[0] + p[2]//2, p[1] - 105]
        if all(abs(c[0] - s[0]) > 300 for s in stars): stars.append(c)
    while len(stars) < 3:
        p = plats[len(plats)//2]; stars.append([p[0] + p[2]//2, p[1] - 105])

    return dict(name=f'{wi+1}-{li+1}', ground=ground, plats=plats, magic=magic,
                stars=stars, spikes=spikes, foes=foes, goal=goal, boss=False,
                newFoe=brand_new if placed_new[0] else '')

def boss(wi, rnd):
    # one long arena, no pits to fall down, plenty of magic and places to dodge
    ground = [[0, 2200]]
    plats  = [[320, -150, 150], [700, -230, 140], [1180, -150, 150], [1560, -230, 140]]
    magic  = [[x, -28] for x in range(200, 2100, 130)] + \
             [[390, -178], [1250, -178]]
    stars  = [[770, -335], [1630, -335], [1100, -70]]
    return dict(name=f'{wi+1}-10', ground=ground, plats=plats, magic=magic,
                stars=stars, spikes=[], foes=[[520, 1700, 0, 'boss']],
                goal=2060, boss=True, bossKind=BOSSES[wi], newFoe='')

def surfaces(lv):
    return [dict(x=x, w=w, top=0) for x, w in lv['ground']] + \
           [dict(x=x, w=w, top=y) for x, y, w in lv['plats']]
def span(s, x):
    return s['x'] - x if x < s['x'] else (x - (s['x'] + s['w']) if x > s['x'] + s['w'] else 0)

def check(lv):
    bad = []
    pits = []
    for i in range(len(lv['ground']) - 1):
        end = lv['ground'][i][0] + lv['ground'][i][1]
        nxt = lv['ground'][i+1][0]
        pits.append((end, nxt))
        if nxt - end > DOUBLE_GAP: bad.append(f"pit {nxt-end}px")
        land = (nxt, nxt + LANDING)
        for sx, sw in lv['spikes']:
            if sx < land[1] and sx + sw > land[0]: bad.append(f"spike {sx} where you land")
        for a, b, y, k in lv['foes']:
            if a < land[1] and b > land[0]: bad.append(f"{k} {a} where you land")
    for a, b, y, k in lv['foes']:
        for ps, pe in pits:
            if a < pe + PIT_KEEP and b > ps - PIT_KEEP:
                bad.append(f"{k} {a}-{b} hovering over a pit")
    surf = surfaces(lv)
    for x, y, w in lv['plats']:
        me = next(s for s in surf if s['x'] == x and s['top'] == y)
        if not any(any(s is not me and s['top'] > y and (s['top'] - y) <= MAX_RISE
                       and span(s, px) <= MAX_SPAN for s in surf) for px in (x, x+w/2, x+w)):
            bad.append(f"ledge {x},{y} unreachable")
    for x, y in lv['stars']:
        if not any(s['top'] > y and (s['top'] - y) <= MAX_RISE and span(s, x) <= MAX_SPAN for s in surf):
            bad.append(f"star {x},{y} unreachable")
    if len(lv['stars']) != 3: bad.append(f"{len(lv['stars'])} stars")
    return bad

worlds, total, problems = [], 0, 0
for wi, w in enumerate(WORLDS):
    levels = []
    for li in range(PER_WORLD):
        rnd = random.Random(5000 + wi * 137 + li * 31)
        lv = boss(wi, rnd) if li == PER_WORLD - 1 else normal(wi, li, rnd)
        bad = check(lv)
        if bad:
            problems += 1
            print(f"  {w['name']} {lv['name']}  PROBLEM: {'; '.join(bad)}")
        levels.append(lv); total += 1
    worlds.append(dict(**w, levels=levels))
    pits = [len(l['ground']) - 1 for l in levels]
    print(f"  {w['name']:<13} {len(levels)} levels (last is the boss), "
          f"{sum(len(l['foes']) for l in levels)} creatures, "
          f"{sum(len(l['magic']) for l in levels)} magic orbs")
if problems: sys.exit(f"{problems} levels have problems")
seen = {f[3] for w in worlds for l in w['levels'] for f in l['foes']}
missing = [k for k in ARRIVES if k not in seen]
if missing: sys.exit(f"these monsters never appear in any level: {missing}")
news = [l['newFoe'] for w in worlds for l in w['levels'] if l.get('newFoe')]
unannounced = [k for k in ARRIVES if k not in news]
if unannounced: sys.exit(f"these monsters never get their 'new!' level: {unannounced}")

def arr(a):  return '[' + ','.join('[' + ','.join(str(int(v)) for v in p) + ']' for p in a) + ']'
def foes(a): return '[' + ','.join('[%d,%d,%d,%r]' % (x[0], x[1], x[2], x[3]) for x in a) + ']'
def lvjs(l):
    return ("    { name:%r, boss:%s, goal:%d, bossKind:%r, newFoe:%r,\n"
            "      ground:%s,\n      plats:%s,\n      magic:%s,\n"
            "      stars:%s,\n      spikes:%s,\n      foes:%s }") % (
        l['name'], 'true' if l['boss'] else 'false', l['goal'], l.get('bossKind', ''), l.get('newFoe', ''),
        arr(l['ground']), arr(l['plats']), arr(l['magic']),
        arr(l['stars']), arr(l['spikes']), foes(l['foes']))

out = "const WORLDS = [\n"
for w in worlds:
    out += "  {\n"
    for k, v in w.items():
        if k == 'levels':
            continue
        val = ('true' if v else 'false') if isinstance(v, bool) else repr(v)
        out += "    %s: %s,\n" % (k, val)
    out += "    levels: [\n"
    out += ",\n".join(lvjs(l) for l in w['levels'])
    out += "\n    ]\n  },\n"
out += "];\n"
import argparse, pathlib as _pl, re as _re
ap = argparse.ArgumentParser(description="Rebuild Mage Run's levels")
ap.add_argument("--js-only", help="write just the WORLDS block to this file instead of updating mage-run.html")
args = ap.parse_args()
if args.js_only:
    open(args.js_only, "w").write(out)
    print(f"\nwrote {args.js_only}")
else:
    game = _pl.Path(__file__).resolve().parent.parent / "mage-run.html"
    html = game.read_text(encoding="utf-8")
    block = _re.compile(r"const WORLDS = \[\n.*?\n\];\n", _re.S)
    if len(block.findall(html)) != 1:
        sys.exit("could not find exactly one WORLDS block in mage-run.html - nothing changed")
    game.write_text(block.sub(lambda m: out, html, count=1), encoding="utf-8")
    print(f"\nupdated {game.name}: {total} levels across {len(worlds)} worlds")
