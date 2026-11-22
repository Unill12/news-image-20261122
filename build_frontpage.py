#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 world-news front page (1024x1024 PNG).

One broadsheet page: masthead, a COP31 lead with a drawn Antalya
illustration, two second leads, a labelled world map, nine short
columns and 24 numbered briefs -- 36 stories in all, every one first
reported on Sunday 22 November 2026. Pure PIL, no network, no clock:
the same input always writes the same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

INK = (18, 18, 20)
PAPER = (250, 247, 238)
NAVY = (16, 34, 64)
CRIMSON = (178, 34, 34)
MUTED = (90, 88, 82)
DIVIDER = (150, 146, 136)
OCEAN = (214, 228, 238)
SHORE = (196, 205, 178)
GOLD = (255, 214, 90)
PALE_BLUE = (180, 200, 230)


def load_font(weight, size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-%s.ttf" % weight,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_F = load_font("Bold", 40)
DAY_F = load_font("Bold", 18)
TAG_F = load_font("Bold", 14)
HEAD_F = load_font("Bold", 38)
DEK_F = load_font("", 18)
SECOND_F = load_font("Bold", 20)
SECOND_DEK_F = load_font("", 15)
COL_HEAD_F = load_font("Bold", 15)
COL_BODY_F = load_font("", 13)
BRIEF_F = load_font("", 12)
MAP_NUM_F = load_font("Bold", 12)
CAPTION_F = load_font("", 12)


def flow_text(canvas, origin, text, typeface, width, colour=INK, gap=3):
    """Greedy word wrap; returns the y just below the last line."""
    x, y = origin
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if canvas.textlength(trial, font=typeface) <= width:
            line = trial
        else:
            if line:
                canvas.text((x, y), line, font=typeface, fill=colour)
                y += typeface.size + gap
            line = word
    if line:
        canvas.text((x, y), line, font=typeface, fill=colour)
        y += typeface.size + gap
    return y


def hline(canvas, x0, y, x1, thick=1, colour=DIVIDER):
    canvas.line([(x0, y), (x1, y)], fill=colour, width=thick)


# ---------------------------------------------------------------- data

LEAD_KICKER = "LEAD  •  ANTALYA"
LEAD_LINES = ["CLIMATE TALKS NEAR DEAL", "AS NEW TEXT TABLED", "AT COP31"]
LEAD_DEK = (
    "COP31 presidents table a new package in Antalya and call a "
    "Sunday-morning session to approve it, after talks ran past their "
    "Friday deadline in a split over fossil fuels."
)
LEAD_CAPTION = "ANTALYA  •  APPROVAL SESSION 06:00 GMT"

SECOND_STORIES = [
    (
        "BAHRAIN  •  IRAN",
        "Iran strikes Bahrain plant; US radars 'hit'",
        "An Iranian attack sets fire to a Bahrain industrial facility; "
        "the IRGC claims a missile-and-drone strike on two US Patriot "
        "radars.",
    ),
    (
        "HONG KONG  •  VOTE",
        "Hong Kong votes for its Election Committee",
        "Polls open for 723 contested seats on the 1,500-member body "
        "that picks the chief executive; 856 candidates, 5,700 voters.",
    ),
]

# (lon, lat) of the ten numbered map pins, in legend order.
PINS = [
    (30.7, 36.9),    # 1 Antalya
    (50.6, 26.2),    # 2 Bahrain
    (114.2, 22.3),   # 3 Hong Kong
    (24.0, 49.8),    # 4 Lviv
    (24.9, 60.2),    # 5 Helsinki
    (34.8, 32.1),    # 6 Tel Aviv
    (34.5, 31.5),    # 7 Gaza
    (51.4, 35.7),    # 8 Tehran
    (39.5, 13.5),    # 9 Mekelle
    (15.3, -4.3),    # 10 Kinshasa
]
LEGEND = (
    "1 ANTALYA   2 BAHRAIN   3 HONG KONG   4 LVIV   5 HELSINKI   "
    "6 TEL AVIV   7 GAZA   8 TEHRAN   9 MEKELLE   10 KINSHASA"
)

COLUMNS = [
    ("LVIV", "Russian strike hits Lviv; 2 killed, 10 hurt. Kyiv says "
     "air defences downed drones overnight."),
    ("FINLAND", "Orpo: the war is spilling over after a drone strike on "
     "a Russian merchant ship off Finland."),
    ("ISRAEL", "Eisenkot invites Netanyahu's Likud to coalition talks "
     "as the deadline nears."),
    ("GAZA", "Recovery teams pull 129 bodies from rubble in central "
     "Gaza, medics say."),
    ("IRAN", "Tehran calls the US blockade a hostile act, its deputy "
     "foreign minister says."),
    ("SAHEL", "Sahel states restart dialogue with the West Africa bloc "
     "after years apart."),
    ("TIGRAY", "New Tigray mayor vows elections within six months "
     "after Ethiopia clashes."),
    ("CONGO", "Tshisekedi enacts a constitutional reform law amid high "
     "tensions in Kinshasa."),
    ("CRICKET", "Smith ruled out of the South Africa Test decider "
     "with a neck injury."),
]

BRIEFS = [
    "Myanmar hit by a magnitude 4.1 quake in the early hours of Sunday.",
    "Nigeria: 24 bodies recovered after a boat capsizes.",
    "Peru quake leaves 152 homes uninhabitable, officials say.",
    "Croatia rally over a patient's death draws crowds.",
    "Paolo Bulgari, of the jewellery dynasty, has died.",
    "UAE president receives US homeland security chief Mullin.",
    "ATP Finals decider today: Alcaraz meets Zverev in Turin.",
    "France reach the Nations Championship final against South Africa.",
    "Trump aide pushes a federal film tax credit for January 2027.",
    "ICE agents smash a car window and detain a man in Santa Clarita.",
    "Belgium's Greens accept nuclear power as a transition source.",
    "Australia end England's seven-match T20 winning streak.",
    "Kenya secures 293,600 job openings in Saudi Arabia.",
    "Nigeria starts building naval ships at home.",
    "EU hunts a new ECB chief as Lagarde resigns.",
    "Awar Odhiang, refugee-born model, named model of the year.",
    "Tyla, Tems and Kidjo lead Africa's Grammy hopes.",
    "Sudan group accuses RSF of killing civilians, three of them children.",
    "Three Salvadorans killed handling explosives in Haiti.",
    "Protest outside a South African court over barred anti-migrant rallies.",
    "Power chaos tests South Africa's ANC: 'no electricity, no vote'.",
    "Lagos Fashion Week tied to stronger US commercial links.",
    "Bangladesh envoy hails India's role in the 1971 liberation war.",
    "Zelenskyy: NATO membership is Ukraine's clearest security guarantee.",
]

# Schematic land outlines (lon, lat), world window: lon -180..180, lat -90..90.
MAP_LON0, MAP_LON1 = -180.0, 180.0
MAP_LAT0, MAP_LAT1 = -90.0, 90.0
SHAPES = [
    [(-168, 66), (-135, 70), (-110, 69), (-90, 68), (-75, 60),
     (-65, 58), (-60, 46), (-70, 42), (-76, 35), (-81, 26),
     (-87, 30), (-94, 22), (-104, 20), (-112, 25), (-118, 33),
     (-124, 42), (-126, 50), (-138, 59), (-156, 58), (-166, 61)],
    [(-79, 9), (-72, 11), (-60, 8), (-51, 4), (-44, -3),
     (-36, -8), (-41, -22), (-49, -29), (-58, -38), (-66, -46),
     (-70, -53), (-73, -42), (-72, -30), (-71, -18), (-78, -10),
     (-81, -4), (-80, 3)],
    [(-17, 15), (-14, 28), (-8, 32), (0, 36), (10, 37),
     (20, 32), (31, 31), (36, 27), (43, 12), (51, 11),
     (46, 0), (40, -11), (35, -19), (30, -28), (25, -34),
     (17, -34), (12, -17), (9, 0), (8, 4), (-9, 5), (-14, 9)],
    [(-10, 37), (-8, 43), (-2, 48), (1, 51), (6, 54),
     (9, 57), (13, 58), (19, 56), (24, 59), (29, 62),
     (33, 69), (42, 68), (39, 60), (36, 52), (30, 46),
     (25, 41), (19, 42), (12, 44), (3, 43)],
    [(42, 68), (55, 69), (68, 72), (80, 73), (95, 76),
     (110, 74), (125, 73), (140, 72), (152, 70), (160, 64),
     (157, 56), (148, 59), (141, 48), (136, 35), (128, 33),
     (122, 37), (119, 27), (110, 20), (106, 9), (100, 7),
     (96, 15), (90, 22), (84, 19), (79, 10), (76, 20),
     (71, 21), (64, 25), (58, 25), (52, 27), (48, 30),
     (44, 29), (42, 16), (45, 24), (52, 28), (58, 26),
     (60, 30), (56, 38), (50, 40), (44, 42), (40, 47),
     (37, 50), (41, 56)],
    [(114, -22), (115, -32), (120, -34), (127, -32), (134, -33),
     (140, -38), (147, -39), (150, -37), (153, -28), (148, -20),
     (143, -12), (136, -12), (131, -12), (125, -14), (120, -18)],
]
# Display nudges (d_lon, d_lat) for pins that would otherwise collide;
# a thin leader joins the shown pin to its true spot.
PIN_NUDGE = {1: (0, 10), 2: (8, -8), 4: (-12, -2), 5: (-10, 8),
             6: (6, -6), 7: (-2, -12), 8: (10, 8), 9: (0, -10)}


def draw_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    ink = ImageDraw.Draw(page)

    # ---- masthead --------------------------------------------------
    ink.rectangle([0, 0, PAGE_W, 76], fill=NAVY)
    ink.text((18, 8), "THE WORLD TODAY", font=TITLE_F, fill=(255, 255, 255))
    ink.text((18, 54), "ONE DAY  •  EVERY STORY THAT MATTERED", font=TAG_F,
             fill=PALE_BLUE)
    ink.text((PAGE_W - 18, 10), "SUNDAY", font=DAY_F,
             fill=(255, 255, 255), anchor="ra")
    ink.text((PAGE_W - 18, 33), "22 NOVEMBER 2026", font=DAY_F,
             fill=GOLD, anchor="ra")
    ink.text((PAGE_W - 18, 56), "36 STORIES  •  ONE FRONT PAGE", font=TAG_F,
             fill=PALE_BLUE, anchor="ra")

    # ---- lead ------------------------------------------------------
    ink.text((18, 86), LEAD_KICKER, font=TAG_F, fill=CRIMSON)
    y = 106
    for line in LEAD_LINES:
        ink.text((18, y), line, font=HEAD_F, fill=INK)
        y += 43
    flow_text(ink, (18, y + 4), LEAD_DEK, DEK_F, 620, colour=MUTED)

    # lead picture: Antalya coast at dusk -- sea, mountains, hall
    px, py, pw, ph = 656, 86, 350, 214
    ink.rectangle([px, py, px + pw, py + ph], fill=(58, 74, 102))
    for i in range(ph):
        shade = int(58 + (102 - 58) * i / ph)
        ink.line([(px, py + i), (px + pw, py + i)],
                 fill=(shade, shade + 16, shade + 36))
    ink.ellipse([px + 268, py + 14, px + 306, py + 52],
                fill=(240, 220, 170))
    ink.polygon([(px, py + ph), (px, py + 150), (px + 92, py + 118),
                 (px + 172, py + 152), (px + 252, py + 122),
                 (px + pw, py + 148), (px + pw, py + ph)],
                fill=(40, 54, 76))
    ink.polygon([(px, py + ph), (px, py + 178), (px + 122, py + 158),
                 (px + 232, py + 182), (px + pw, py + 164),
                 (px + pw, py + ph)], fill=(26, 36, 54))
    ink.rectangle([px + 96, py + 128, px + 254, py + 178],
                  fill=(214, 196, 150))
    ink.rectangle([px + 96, py + 128, px + 254, py + 140],
                  fill=(150, 60, 60))
    for bx in range(px + 106, px + 250, 18):
        ink.rectangle([bx, py + 148, bx + 9, py + 164], fill=(40, 54, 76))
    ink.text((px + 8, py + ph - 22), LEAD_CAPTION, font=TAG_F,
             fill=(255, 255, 255))
    hline(ink, 18, 310, PAGE_W - 18, 2, NAVY)

    # ---- second leads ----------------------------------------------
    for si, (kicker, head, dek) in enumerate(SECOND_STORIES):
        col_x = 18 if si == 0 else 522
        ink.text((col_x, 320), kicker, font=TAG_F, fill=CRIMSON)
        y = flow_text(ink, (col_x, 339), head, SECOND_F, 484)
        flow_text(ink, (col_x, y + 2), dek, SECOND_DEK_F, 484,
                  colour=MUTED)
    ink.line([(512, 320), (512, 424)], fill=DIVIDER, width=1)
    hline(ink, 18, 434, PAGE_W - 18, 2, NAVY)

    # ---- world map ---------------------------------------------------
    ink.text((18, 444), "WHERE IT HAPPENED  •  22 NOVEMBER 2026",
             font=TAG_F, fill=NAVY)
    map_x, map_y, map_w, map_h = 18, 462, 988, 110
    ink.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN)
    ink.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                  outline=DIVIDER, width=1)

    def project(lon, lat):
        return (map_x + (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0) * map_w,
                map_y + (MAP_LAT1 - lat) / (MAP_LAT1 - MAP_LAT0) * map_h)

    for shape in SHAPES:
        ink.polygon([project(lon, lat) for lon, lat in shape],
                    fill=SHORE, outline=(120, 130, 110))
    for idx, (lon, lat) in enumerate(PINS, 1):
        x, y = project(lon, lat)
        nudge = PIN_NUDGE.get(idx)
        if nudge is not None:
            dx, dy = project(lon + nudge[0], lat + nudge[1])
            ink.line([(x, y), (dx, dy)], fill=CRIMSON, width=1)
            ink.ellipse([x - 2, y - 2, x + 2, y + 2], fill=CRIMSON)
            x, y = dx, dy
        ink.ellipse([x - 5, y - 5, x + 5, y + 5], fill=CRIMSON,
                    outline=(255, 255, 255))
        ink.text((x, y), str(idx), font=MAP_NUM_F,
                 fill=(255, 255, 255), anchor="mm")
    ink.text((18, map_y + map_h + 5), LEGEND, font=CAPTION_F, fill=INK)

    # ---- columns -----------------------------------------------------
    top = 600
    ink.text((18, top), "THE DAY IN BRIEF", font=TAG_F, fill=NAVY)
    hline(ink, 18, top + 18, PAGE_W - 18, 1, NAVY)
    col_w, col_gap = 318, 17
    for ci, (head, body) in enumerate(COLUMNS):
        cx = 18 + (ci % 3) * (col_w + col_gap)
        cy = top + 26 + (ci // 3) * 58
        ink.text((cx, cy), head, font=COL_HEAD_F, fill=CRIMSON)
        flow_text(ink, (cx, cy + 17), body, COL_BODY_F, col_w, gap=1)
    hline(ink, 18, top + 26 + 3 * 58 - 6, PAGE_W - 18, 1, NAVY)

    # ---- numbered briefs ---------------------------------------------
    brief_top = top + 26 + 3 * 58 + 2
    ink.text((18, brief_top), "24 MORE STORIES", font=TAG_F, fill=NAVY)
    hline(ink, 18, brief_top + 18, PAGE_W - 18, 1, NAVY)
    half = 488
    for bi, text in enumerate(BRIEFS):
        col = bi // 12
        row = bi % 12
        bx = 18 + col * (half + 12)
        by = brief_top + 24 + row * 13
        ink.text((bx, by), "%d." % (bi + 1), font=COL_HEAD_F, fill=CRIMSON)
        ink.text((bx + 26, by), text, font=BRIEF_F, fill=INK)

    # ---- footer --------------------------------------------------------
    hline(ink, 18, 992, PAGE_W - 18, 1, NAVY)
    ink.text((18, 998),
             "All stories first reported Sunday 22 November 2026  •  "
             "Compiled from wire and press reports  •  THE WORLD TODAY",
             font=CAPTION_F, fill=MUTED)

    page.save(OUT_PATH, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT_PATH, os.path.getsize(OUT_PATH)))


if __name__ == "__main__":
    draw_page()
