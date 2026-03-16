"""
Pre-built teams for each training format.

5 teams per format in Showdown export format.
Used by RotatingTeambuilder to cycle through diverse teams during RL training.

Formats covered:
  gen9ou           — standard OU, 5 teams (various archetypes)
  gen9nationaldex  — NatDex OU, 5 teams (older Pokemon available)
  gen9monotype     — Monotype, 5 teams (one per common type)
  gen9anythinggoes — Anything Goes, 5 teams (legendaries legal)
  gen9doublesou    — Doubles OU, 5 teams (doubles-oriented)
"""

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 OU
# ─────────────────────────────────────────────────────────────────────────────

GEN9OU = [

    # Team 1 — Bulky Offense (Tusk + Ghold core)
    """\
Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Swords Dance

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Great Tusk @ Heavy-Duty Boots
Ability: Protosynthesis
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Ice Spinner
- Rapid Spin
- Stealth Rock

Dragapult @ Choice Scarf
Ability: Infiltrator
Tera Type: Dragon
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Dragon Pulse
- Shadow Ball
- Flamethrower
- U-turn

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower""",

    # Team 2 — Stall
    """\
Dondozo @ Leftovers
Ability: Unaware
Tera Type: Water
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Waterfall
- Rest
- Sleep Talk
- Wave Crash

Clodsire @ Black Sludge
Ability: Unaware
Tera Type: Poison
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Earthquake
- Toxic
- Recover
- Stealth Rock

Blissey @ Leftovers
Ability: Natural Cure
Tera Type: Normal
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Soft-Boiled
- Heal Bell
- Protect
- Thunder Wave

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 252 Def / 4 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Gliscor @ Toxic Orb
Ability: Poison Heal
Tera Type: Ground
EVs: 252 HP / 184 Def / 72 Spe
Impish Nature
- Earthquake
- U-turn
- Protect
- Knock Off

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Protect
- Flamethrower""",

    # Team 3 — Rain Offense
    """\
Pelipper @ Leftovers
Ability: Drizzle
Tera Type: Water
EVs: 248 HP / 8 SpA / 252 SpD
Calm Nature
- Surf
- Hurricane
- Roost
- U-turn

Barraskewda @ Life Orb
Ability: Swift Swim
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Liquidation
- Close Combat
- Flip Turn
- Psychic Fangs

Zapdos @ Heavy-Duty Boots
Ability: Static
Tera Type: Flying
EVs: 248 HP / 8 SpA / 252 Def
Bold Nature
- Thunderbolt
- Hurricane
- Roost
- Volt Switch

Iron Treads @ Heavy-Duty Boots
Ability: Quark Drive
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Iron Head
- Rapid Spin
- Stealth Rock

Swampert @ Leftovers
Ability: Torrent
Tera Type: Ground
EVs: 240 HP / 16 Atk / 252 Def
Relaxed Nature
- Waterfall
- Earthquake
- Stealth Rock
- Flip Turn

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Swords Dance""",

    # Team 4 — Trick Room
    """\
Hatterene @ Misty Seed
Ability: Magic Bounce
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Mystical Fire
- Trick Room
- Healing Wish

Ursaluna @ Flame Orb
Ability: Guts
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Facade
- Headlong Rush
- Crunch
- Swords Dance

Porygon2 @ Eviolite
Ability: Download
Tera Type: Normal
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Tri Attack
- Shadow Ball
- Thunderbolt
- Trick Room

Armarouge @ Choice Scarf
Ability: Flash Fire
Tera Type: Fire
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Armor Cannon
- Psychic
- Energy Ball
- Focus Blast

Mimikyu @ Life Orb
Ability: Disguise
Tera Type: Ghost
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Play Rough
- Shadow Sneak
- Swords Dance
- Shadow Claw

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower""",

    # Team 5 — Sand
    """\
Tyranitar @ Smooth Rock
Ability: Sand Stream
Tera Type: Rock
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Stone Edge
- Crunch
- Stealth Rock
- Dragon Dance

Excadrill @ Life Orb
Ability: Sand Rush
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Earthquake
- Iron Head
- Rock Slide
- Rapid Spin

Garchomp @ Rocky Helmet
Ability: Rough Skin
Tera Type: Ground
EVs: 252 HP / 164 Def / 92 Spe
Impish Nature
- Earthquake
- Stealth Rock
- Dragon Tail
- Fire Fang

Scizor @ Choice Band
Ability: Technician
Tera Type: Steel
EVs: 248 HP / 252 Atk / 8 SpD
Adamant Nature
- U-turn
- Bullet Punch
- Iron Head
- Knock Off

Rotom-Wash @ Leftovers
Ability: Levitate
Tera Type: Water
EVs: 248 HP / 252 SpA / 8 Spe
Modest Nature
- Volt Switch
- Hydro Pump
- Will-O-Wisp
- Pain Split

Blissey @ Leftovers
Ability: Natural Cure
Tera Type: Normal
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Soft-Boiled
- Heal Bell
- Protect
- Thunder Wave""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 National Dex
# ─────────────────────────────────────────────────────────────────────────────

GEN9NATIONALDEX = [

    # Team 1 — Classic Balance
    """\
Landorus-Therian @ Rocky Helmet
Ability: Intimidate
Tera Type: Ground
EVs: 252 HP / 240 Def / 16 Spe
Impish Nature
- Earthquake
- U-turn
- Stealth Rock
- Rock Slide

Rotom-Wash @ Leftovers
Ability: Levitate
Tera Type: Water
EVs: 248 HP / 252 SpA / 8 Spe
Modest Nature
- Volt Switch
- Hydro Pump
- Will-O-Wisp
- Pain Split

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower

Scizor @ Choice Band
Ability: Technician
Tera Type: Steel
EVs: 248 HP / 252 Atk / 8 SpD
Adamant Nature
- U-turn
- Bullet Punch
- Superpower
- Knock Off

Heatran @ Leftovers
Ability: Flash Fire
Tera Type: Steel
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Magma Storm
- Earth Power
- Stealth Rock
- Taunt

Latios @ Choice Specs
Ability: Levitate
Tera Type: Dragon
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Draco Meteor
- Psyshock
- Thunderbolt
- Trick""",

    # Team 2 — Fairy Offense
    """\
Iron Valiant @ Choice Scarf
Ability: Quark Drive
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Dazzling Gleam
- Shadow Ball
- Trick

Gardevoir @ Choice Specs
Ability: Trace
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Psyshock
- Focus Blast
- Trick

Tyranitar @ Choice Band
Ability: Sand Stream
Tera Type: Rock
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Stone Edge
- Crunch
- Pursuit
- Earthquake

Iron Treads @ Heavy-Duty Boots
Ability: Quark Drive
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Iron Head
- Rapid Spin
- Stealth Rock

Garchomp @ Rocky Helmet
Ability: Rough Skin
Tera Type: Ground
EVs: 252 HP / 164 Def / 92 Spe
Impish Nature
- Earthquake
- Stealth Rock
- Dragon Tail
- Fire Fang

Great Tusk @ Heavy-Duty Boots
Ability: Protosynthesis
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Ice Spinner
- Rapid Spin
- Stealth Rock""",

    # Team 3 — Hazard Stack
    """\
Garchomp @ Rocky Helmet
Ability: Rough Skin
Tera Type: Ground
EVs: 252 HP / 164 Def / 92 Spe
Impish Nature
- Earthquake
- Stealth Rock
- Dragon Tail
- Fire Fang

Iron Treads @ Heavy-Duty Boots
Ability: Quark Drive
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Iron Head
- Rapid Spin
- Stealth Rock

Toxapex @ Black Sludge
Ability: Regenerator
Tera Type: Poison
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Surf
- Recover
- Toxic Spikes
- Haze

Zapdos @ Heavy-Duty Boots
Ability: Static
Tera Type: Flying
EVs: 248 HP / 8 SpA / 252 Def
Bold Nature
- Thunderbolt
- Hurricane
- Roost
- Volt Switch

Blissey @ Leftovers
Ability: Natural Cure
Tera Type: Normal
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Soft-Boiled
- Wish
- Protect
- Toxic

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick""",

    # Team 4 — Sun offense
    """\
Ninetales @ Heat Rock
Ability: Drought
Tera Type: Fire
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Fire Blast
- Solar Beam
- Hypnosis
- Nasty Plot

Venusaur @ Life Orb
Ability: Chlorophyll
Tera Type: Grass
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Solar Beam
- Sludge Bomb
- Sleep Powder
- Earth Power

Heatran @ Choice Scarf
Ability: Flash Fire
Tera Type: Fire
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Magma Storm
- Earth Power
- Flash Cannon
- Ancient Power

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Swords Dance

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Great Tusk @ Heavy-Duty Boots
Ability: Protosynthesis
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Ice Spinner
- Rapid Spin
- Stealth Rock""",

    # Team 5 — Volt-Turn
    """\
Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- U-turn
- Stone Edge
- Rock Slide

Rotom-Wash @ Leftovers
Ability: Levitate
Tera Type: Water
EVs: 248 HP / 252 SpA / 8 Spe
Modest Nature
- Volt Switch
- Hydro Pump
- Will-O-Wisp
- Pain Split

Scizor @ Choice Band
Ability: Technician
Tera Type: Steel
EVs: 248 HP / 252 Atk / 8 SpD
Adamant Nature
- U-turn
- Bullet Punch
- Superpower
- Knock Off

Zapdos @ Heavy-Duty Boots
Ability: Static
Tera Type: Flying
EVs: 248 HP / 8 SpA / 252 Def
Bold Nature
- Thunderbolt
- Hurricane
- Roost
- Volt Switch

Tyranitar @ Choice Band
Ability: Sand Stream
Tera Type: Rock
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Stone Edge
- Crunch
- Earthquake
- Ice Punch

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 Monotype (all 6 Pokemon share the listed type)
# ─────────────────────────────────────────────────────────────────────────────

GEN9MONOTYPE = [

    # Team 1 — Water
    """\
Toxapex @ Black Sludge
Ability: Regenerator
Tera Type: Water
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Surf
- Recover
- Toxic
- Haze

Dondozo @ Leftovers
Ability: Unaware
Tera Type: Water
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Waterfall
- Rest
- Sleep Talk
- Wave Crash

Rotom-Wash @ Leftovers
Ability: Levitate
Tera Type: Water
EVs: 248 HP / 252 SpA / 8 Spe
Modest Nature
- Volt Switch
- Hydro Pump
- Will-O-Wisp
- Pain Split

Barraskewda @ Choice Band
Ability: Swift Swim
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Liquidation
- Close Combat
- Flip Turn
- Psychic Fangs

Pelipper @ Leftovers
Ability: Drizzle
Tera Type: Water
EVs: 248 HP / 8 SpA / 252 SpD
Calm Nature
- Surf
- Hurricane
- Roost
- U-turn

Greninja @ Life Orb
Ability: Protean
Tera Type: Water
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Hydro Pump
- Dark Pulse
- Ice Beam
- U-turn""",

    # Team 2 — Steel
    """\
Scizor @ Choice Band
Ability: Technician
Tera Type: Steel
EVs: 248 HP / 252 Atk / 8 SpD
Adamant Nature
- U-turn
- Bullet Punch
- Iron Head
- Knock Off

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Steel
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Heatran @ Leftovers
Ability: Flash Fire
Tera Type: Steel
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Magma Storm
- Earth Power
- Stealth Rock
- Taunt

Iron Treads @ Choice Scarf
Ability: Quark Drive
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Iron Head
- Rapid Spin
- Ice Spinner

Magnezone @ Choice Scarf
Ability: Analytic
Tera Type: Steel
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Thunderbolt
- Flash Cannon
- Volt Switch
- Body Press""",

    # Team 3 — Dragon
    """\
Dragapult @ Choice Scarf
Ability: Infiltrator
Tera Type: Dragon
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Dragon Pulse
- Shadow Ball
- Flamethrower
- U-turn

Roaring Moon @ Life Orb
Ability: Protosynthesis
Tera Type: Dragon
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Acrobatics
- Knock Off
- Dragon Dance
- Earthquake

Garchomp @ Rocky Helmet
Ability: Rough Skin
Tera Type: Dragon
EVs: 252 HP / 164 Def / 92 Spe
Impish Nature
- Earthquake
- Stealth Rock
- Dragon Tail
- Fire Fang

Dragonite @ Heavy-Duty Boots
Ability: Multiscale
Tera Type: Dragon
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Dragon Dance
- Extreme Speed
- Earthquake
- Fire Punch

Hydreigon @ Choice Specs
Ability: Levitate
Tera Type: Dragon
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Draco Meteor
- Dark Pulse
- Flash Cannon
- U-turn

Noivern @ Choice Scarf
Ability: Infiltrator
Tera Type: Dragon
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Hurricane
- Dragon Pulse
- U-turn
- Flamethrower""",

    # Team 4 — Fairy
    """\
Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower

Flutter Mane @ Choice Scarf
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Psyshock
- Dazzling Gleam

Gardevoir @ Choice Specs
Ability: Trace
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Psyshock
- Focus Blast
- Trick

Azumarill @ Choice Band
Ability: Huge Power
Tera Type: Water
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Aqua Jet
- Play Rough
- Knock Off
- Ice Punch

Sylveon @ Leftovers
Ability: Pixilate
Tera Type: Fairy
EVs: 252 HP / 252 SpA / 4 SpD
Modest Nature
- Hyper Voice
- Shadow Ball
- Calm Mind
- Protect

Mimikyu @ Life Orb
Ability: Disguise
Tera Type: Ghost
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Play Rough
- Shadow Sneak
- Swords Dance
- Shadow Claw""",

    # Team 5 — Ground
    """\
Garchomp @ Rocky Helmet
Ability: Rough Skin
Tera Type: Ground
EVs: 252 HP / 164 Def / 92 Spe
Impish Nature
- Earthquake
- Stealth Rock
- Dragon Tail
- Fire Fang

Great Tusk @ Heavy-Duty Boots
Ability: Protosynthesis
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Ice Spinner
- Rapid Spin
- Knock Off

Gliscor @ Toxic Orb
Ability: Poison Heal
Tera Type: Ground
EVs: 252 HP / 184 Def / 72 Spe
Impish Nature
- Earthquake
- U-turn
- Protect
- Knock Off

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- U-turn
- Stone Edge
- Rock Slide

Clodsire @ Black Sludge
Ability: Unaware
Tera Type: Poison
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Earthquake
- Toxic
- Recover
- Stealth Rock

Iron Treads @ Booster Energy
Ability: Quark Drive
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Iron Head
- Rapid Spin
- Ice Spinner""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 Anything Goes
# ─────────────────────────────────────────────────────────────────────────────

GEN9ANYTHINGGOES = [

    # Team 1 — Restricted Offense
    """\
Zacian-Crowned @ Rusted Sword
Ability: Intrepid Sword
Tera Type: Fairy
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Behemoth Blade
- Play Rough
- Wild Charge
- Close Combat

Kyogre @ Choice Specs
Ability: Drizzle
Tera Type: Water
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Water Spout
- Origin Pulse
- Ice Beam
- Thunder

Landorus-Therian @ Rocky Helmet
Ability: Intimidate
Tera Type: Ground
EVs: 252 HP / 240 Def / 16 Spe
Impish Nature
- Earthquake
- U-turn
- Stealth Rock
- Rock Slide

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Swords Dance""",

    # Team 2 — Sun Legendaries
    """\
Groudon @ Earth Plate
Ability: Drought
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Precipice Blades
- Fire Punch
- Stealth Rock
- Rock Slide

Rayquaza @ Life Orb
Ability: Air Lock
Tera Type: Dragon
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Dragon Ascent
- Extreme Speed
- Earthquake
- Dragon Dance

Ho-Oh @ Life Orb
Ability: Regenerator
Tera Type: Fire
EVs: 252 Atk / 4 SpD / 252 Spe
Adamant Nature
- Sacred Fire
- Brave Bird
- Earthquake
- Recover

Flutter Mane @ Choice Specs
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Mystical Fire
- Dazzling Gleam

Necrozma-Dusk-Mane @ Life Orb
Ability: Prism Armor
Tera Type: Steel
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Sunsteel Strike
- Earthquake
- Dragon Dance
- Knock Off

Great Tusk @ Heavy-Duty Boots
Ability: Protosynthesis
Tera Type: Ground
EVs: 252 HP / 4 Atk / 252 Def
Impish Nature
- Earthquake
- Ice Spinner
- Rapid Spin
- Stealth Rock""",

    # Team 3 — Rain Legendaries
    """\
Kyogre @ Choice Specs
Ability: Drizzle
Tera Type: Water
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Water Spout
- Origin Pulse
- Ice Beam
- Thunder

Palkia @ Choice Specs
Ability: Pressure
Tera Type: Water
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Spacial Rend
- Hydro Pump
- Fire Blast
- Thunder

Zamazenta-Crowned @ Rusted Shield
Ability: Dauntless Shield
Tera Type: Steel
EVs: 252 HP / 252 Def / 4 SpD
Impish Nature
- Body Press
- Iron Defense
- Crunch
- Protect

Eternatus @ Leftovers
Ability: Pressure
Tera Type: Poison
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Flamethrower
- Sludge Bomb
- Recover
- Dragon Pulse

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick""",

    # Team 4 — Trick Room Legendaries
    """\
Calyrex-Ice @ Weakness Policy
Ability: As One (Glastrier)
Tera Type: Ice
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Glacial Lance
- High Horsepower
- Protect
- Trick Room

Hatterene @ Misty Seed
Ability: Magic Bounce
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Mystical Fire
- Trick Room
- Healing Wish

Ursaluna @ Flame Orb
Ability: Guts
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Facade
- Headlong Rush
- Crunch
- Swords Dance

Necrozma @ Power Herb
Ability: Prism Armor
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Photon Geyser
- Moonblast
- Power Gem
- Trick Room

Zacian-Crowned @ Rusted Sword
Ability: Intrepid Sword
Tera Type: Fairy
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Behemoth Blade
- Play Rough
- Wild Charge
- Close Combat

Clefable @ Leftovers
Ability: Magic Guard
Tera Type: Fairy
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Moonblast
- Calm Mind
- Moonlight
- Flamethrower""",

    # Team 5 — Balanced Restricted
    """\
Lugia @ Leftovers
Ability: Multiscale
Tera Type: Psychic
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Aeroblast
- Roost
- Recover
- Toxic

Zekrom @ Choice Band
Ability: Teravolt
Tera Type: Dragon
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Bolt Strike
- Dragon Claw
- Outrage
- Zen Headbutt

Miraidon @ Choice Specs
Ability: Hadron Engine
Tera Type: Electric
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Electro Drift
- Draco Meteor
- Focus Blast
- Volt Switch

Landorus-Therian @ Rocky Helmet
Ability: Intimidate
Tera Type: Ground
EVs: 252 HP / 240 Def / 16 Spe
Impish Nature
- Earthquake
- U-turn
- Stealth Rock
- Rock Slide

Corviknight @ Leftovers
Ability: Pressure
Tera Type: Steel
EVs: 252 HP / 4 Def / 252 SpD
Careful Nature
- Body Press
- Roost
- Defog
- U-turn

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 Doubles OU
# ─────────────────────────────────────────────────────────────────────────────

GEN9DOUBLESOU = [

    # Team 1 — Urshifu + Rillaboom
    """\
Ogerpon-Wellspring @ Wellspring Mask
Ability: Water Absorb
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Ivy Cudgel
- Horn Leech
- Follow Me
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Iron Valiant @ Booster Energy
Ability: Quark Drive
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Dazzling Gleam
- Shadow Ball
- Protect

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect

Heatran @ Safety Goggles
Ability: Flash Fire
Tera Type: Steel
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Heat Wave
- Flash Cannon
- Earth Power
- Protect""",

    # Team 2 — Ogerpon + Kingambit
    """\
Ogerpon-Wellspring @ Wellspring Mask
Ability: Water Absorb
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Ivy Cudgel
- Horn Leech
- Follow Me
- Spiky Shield

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Iron Bundle @ Choice Scarf
Ability: Quark Drive
Tera Type: Ice
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Hydro Pump
- Freeze-Dry
- U-turn
- Icy Wind

Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane""",

    # Team 3 — Trick Room
    """\
Hatterene @ Misty Seed
Ability: Magic Bounce
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Mystical Fire
- Trick Room
- Healing Wish

Ursaluna @ Flame Orb
Ability: Guts
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Facade
- Headlong Rush
- Crunch
- Protect

Porygon2 @ Eviolite
Ability: Download
Tera Type: Normal
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Tri Attack
- Shadow Ball
- Trick Room
- Protect

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Iron Hands @ Assault Vest
Ability: Quark Drive
Tera Type: Electric
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Wild Charge
- Close Combat
- Fake Out
- Drain Punch

Indeedee-F @ Psychic Seed
Ability: Psychic Surge
Tera Type: Psychic
EVs: 252 HP / 4 SpA / 252 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Follow Me
- Trick Room
- Helping Hand""",

    # Team 4 — Tailwind
    """\
Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane

Sylveon @ Choice Specs
Ability: Pixilate
Tera Type: Fairy
EVs: 252 HP / 252 SpA / 4 Spe
Modest Nature
- Hyper Voice
- Psychic
- Shadow Ball
- Protect

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Protect

Garchomp @ Life Orb
Ability: Rough Skin
Tera Type: Dragon
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Dragon Claw
- Scale Shot
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick""",

    # Team 5 — Sun + Chlorophyll
    """\
Torkoal @ Heat Rock
Ability: Drought
Tera Type: Fire
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Heat Wave
- Earth Power
- Stealth Rock
- Protect

Venusaur @ Life Orb
Ability: Chlorophyll
Tera Type: Grass
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Solar Beam
- Sludge Bomb
- Sleep Powder
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 VGC 2026 Reg I  (one restricted legendary allowed, level 50 flat rules)
# ─────────────────────────────────────────────────────────────────────────────

GEN9VGC2026REGI = [

    # Team 1 — Zacian restricted + Flutter Mane
    """\
Zacian-Crowned @ Rusted Sword
Ability: Intrepid Sword
Tera Type: Fairy
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Behemoth Blade
- Play Rough
- Wild Charge
- Protect

Flutter Mane @ Life Orb
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Protect
- Dazzling Gleam

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect""",

    # Team 2 — Kyogre restricted + Tailwind
    """\
Kyogre @ Choice Specs
Ability: Drizzle
Tera Type: Water
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Water Spout
- Origin Pulse
- Ice Beam
- Protect

Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane

Urshifu-Rapid-Strike @ Choice Band
Ability: Unseen Fist
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Surging Strikes
- Close Combat
- U-turn
- Aqua Jet

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect""",

    # Team 3 — Calyrex-Ice restricted + Trick Room
    """\
Calyrex-Ice @ Weakness Policy
Ability: As One (Glastrier)
Tera Type: Ice
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Glacial Lance
- High Horsepower
- Close Combat
- Protect

Hatterene @ Misty Seed
Ability: Magic Bounce
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Mystical Fire
- Trick Room
- Healing Wish

Ursaluna @ Flame Orb
Ability: Guts
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Facade
- Headlong Rush
- Crunch
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Flutter Mane @ Life Orb
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Protect
- Dazzling Gleam""",

    # Team 4 — Groudon restricted + Sun
    """\
Groudon @ Earth Plate
Ability: Drought
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Adamant Nature
- Precipice Blades
- Fire Punch
- Rock Slide
- Protect

Venusaur @ Life Orb
Ability: Chlorophyll
Tera Type: Grass
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Solar Beam
- Sludge Bomb
- Sleep Powder
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Flutter Mane @ Life Orb
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Protect
- Dazzling Gleam

Urshifu-Rapid-Strike @ Choice Band
Ability: Unseen Fist
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Surging Strikes
- Close Combat
- U-turn
- Aqua Jet

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect""",

    # Team 5 — Calyrex-Shadow restricted + Tailwind Offense
    """\
Calyrex-Shadow @ Life Orb
Ability: As One (Spectrier)
Tera Type: Psychic
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Astral Barrage
- Psyshock
- Shadow Ball
- Protect

Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane

Urshifu-Rapid-Strike @ Choice Band
Ability: Unseen Fist
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Surging Strikes
- Close Combat
- U-turn
- Aqua Jet

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Flutter Mane @ Life Orb
Ability: Protosynthesis
Tera Type: Fairy
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Moonblast
- Shadow Ball
- Protect
- Dazzling Gleam""",

]


# ─────────────────────────────────────────────────────────────────────────────
# Gen 9 VGC 2026 Reg F  (Flat Rules — no restricted legendaries allowed)
# ─────────────────────────────────────────────────────────────────────────────

GEN9VGC2026REGF = [

    # Team 1 — Tailwind offense
    """Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect""",

    # Team 2 — Trick Room
    """Hatterene @ Misty Seed
Ability: Magic Bounce
Tera Type: Psychic
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Mystical Fire
- Trick Room
- Healing Wish

Ursaluna @ Flame Orb
Ability: Guts
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Facade
- Headlong Rush
- Crunch
- Protect

Porygon2 @ Eviolite
Ability: Download
Tera Type: Normal
EVs: 252 HP / 252 SpA / 4 SpD
Quiet Nature
IVs: 0 Spe
- Tri Attack
- Shadow Ball
- Trick Room
- Protect

Iron Hands @ Assault Vest
Ability: Quark Drive
Tera Type: Electric
EVs: 252 HP / 252 Atk / 4 Def
Brave Nature
IVs: 0 Spe
- Wild Charge
- Close Combat
- Fake Out
- Drain Punch

Indeedee-F @ Psychic Seed
Ability: Psychic Surge
Tera Type: Psychic
EVs: 252 HP / 4 SpA / 252 SpD
Quiet Nature
IVs: 0 Spe
- Psychic
- Follow Me
- Trick Room
- Helping Hand

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect""",

    # Team 3 — Rain offense
    """Pelipper @ Leftovers
Ability: Drizzle
Tera Type: Water
EVs: 248 HP / 8 SpA / 252 SpD
Calm Nature
- Surf
- Hurricane
- Protect
- U-turn

Urshifu-Rapid-Strike @ Choice Band
Ability: Unseen Fist
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Surging Strikes
- Close Combat
- U-turn
- Aqua Jet

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect""",

    # Team 4 — Sun + Chlorophyll
    """Torkoal @ Heat Rock
Ability: Drought
Tera Type: Fire
EVs: 252 HP / 4 SpA / 252 SpD
Calm Nature
- Heat Wave
- Earth Power
- Stealth Rock
- Protect

Venusaur @ Life Orb
Ability: Chlorophyll
Tera Type: Grass
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Solar Beam
- Sludge Bomb
- Sleep Powder
- Protect

Landorus-Therian @ Choice Scarf
Ability: Intimidate
Tera Type: Ground
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Earthquake
- Rock Slide
- U-turn
- Protect

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect

Gholdengo @ Choice Specs
Ability: Good as Gold
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Make It Rain
- Shadow Ball
- Focus Blast
- Trick

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect""",

    # Team 5 — Balanced
    """Ogerpon-Wellspring @ Wellspring Mask
Ability: Water Absorb
Tera Type: Water
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Ivy Cudgel
- Horn Leech
- Follow Me
- Protect

Kingambit @ Black Glasses
Ability: Supreme Overlord
Tera Type: Flying
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Fire
EVs: 252 HP / 4 Atk / 252 SpD
Careful Nature
- Fake Out
- Flare Blitz
- Knock Off
- Protect

Rillaboom @ Assault Vest
Ability: Grassy Surge
Tera Type: Grass
EVs: 252 HP / 252 Atk / 4 Spe
Adamant Nature
- Grassy Glide
- U-turn
- Wood Hammer
- Fake Out

Tornadus @ Focus Sash
Ability: Prankster
Tera Type: Flying
EVs: 252 HP / 4 SpA / 252 Spe
Timid Nature
- Tailwind
- Rain Dance
- Taunt
- Hurricane

Amoonguss @ Rocky Helmet
Ability: Regenerator
Tera Type: Grass
EVs: 252 HP / 4 Def / 252 SpD
Calm Nature
- Spore
- Pollen Puff
- Rage Powder
- Protect""",

]

# ─────────────────────────────────────────────────────────────────────────────
# Format → team list mapping
# ─────────────────────────────────────────────────────────────────────────────

FORMAT_TEAMS: dict[str, list[str]] = {
    "gen9ou"           : GEN9OU,
    "gen9nationaldex"  : GEN9NATIONALDEX,
    "gen9monotype"     : GEN9MONOTYPE,
    "gen9anythinggoes" : GEN9ANYTHINGGOES,
    "gen9doublesou"    : GEN9DOUBLESOU,
    "gen9vgc2026regi"  : GEN9VGC2026REGI,
    "gen9vgc2026regf"  : GEN9VGC2026REGF,
}
