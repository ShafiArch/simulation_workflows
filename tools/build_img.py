# Web copies for the simulation page: python3 tools/build_img.py (needs Pillow and python-pptx).
# Originals in Handloom/ are never changed; everything is written to img/ as name.webp (shown
# on the page) and name-l.webp (opened when a picture is clicked). Legends and histograms come
# out of the presentation in Handloom/Existing.
import os, glob, io
from pptx import Presentation
from PIL import Image, ImageDraw
SRC = "Handloom"; OUT = "img"
PPTX = {}
for slide in Presentation(f"{SRC}/Existing/Handloom Simulation Existing Compilation.pptx").slides:
    for sh in slide.shapes:
        if sh.shape_type == 13: PPTX[__import__("hashlib").md5(sh.image.blob).hexdigest()[:6]] = sh.image.blob
def pp(name): return io.BytesIO(PPTX[name.split("_")[-1].split(".")[0]])
os.makedirs(OUT, exist_ok=True)
def save(im, name, s=720, l=1600, q=80):
    for tag, w in (("", s), ("-l", l)):
        if w is None: continue
        c = im.copy()
        if c.width > w: c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(f"{OUT}/{name}{tag}.webp", "WEBP", quality=q, method=6)
def crop(path, box): return Image.open(path).convert("RGBA").crop(box)
def keyed_white(im, t=244):
    # white paper to transparent, soft edge, so figures sit on any theme without a box
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            if m >= t: px[x, y] = (r, g, b, 0)
    return im
M = ["march", "june", "september", "december"]
MF = {"march": "March", "june": "June", "september": "September", "december": "December"}
# wind: one box for every case so the iterations line up
WB = (1080, 1000, 2210, 1790)
for i in range(1, 7):
    save(crop(f"{SRC}/Wind Analysis/Case{i} vector.jpg", WB), f"wind-vector-{i}", s=560, l=1130)
    save(crop(f"{SRC}/Wind Analysis/Case{i}map.jpg", WB), f"wind-pressure-{i}", s=560, l=1130)
# daylight, existing, point in time
for m in M:
    save(crop(f"{SRC}/Existing/Illuminance/{MF[m]} 21st Illuminance lx.png", (868, 931, 2243, 1519)), f"illum-{m}", s=520, l=1375)
    lum = "Exisiting Lumnance 21st 12PM False Color.png" if m == "june" else f"Exisiting Lumnance {MF[m]} 21st 12PM False Color.png"
    save(Image.open(f"{SRC}/Existing/{lum}").convert("RGBA"), f"lum-{m}", s=420, l=1200)
    for op in ("Reinhart", "Ward"):
        fn = glob.glob(f"{SRC}/Tone Mapping/Existing_{MF[m]}_21*_{op}.jpg")[0]
        im = Image.open(fn).convert("RGBA")
        mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse((4, 4, im.width - 5, im.height - 5), fill=255)
        im.putalpha(mask)
        save(im, f"tone-{op.lower()}-{m}", s=420, l=1200)
# annual metrics, existing and optimized
EB = (553, 748, 2685, 1652)
for a, b in (("avg_UDI", "udi"), ("sDA_map", "sda"), ("ASE_map", "ase"), ("avg_lux", "lux")):
    save(crop(f"{SRC}/Existing/{a}.png", EB), f"exist-{b}", s=560, l=1600)
OB = (790, 574, 2292, 1225)
for a, b in (("UDIa", "udi"), ("sDA", "sda"), ("ASE", "ase"), ("avg Lux", "lux"), ("sDG", "sdg")):
    save(keyed_white(crop(f"{SRC}/Optimized/{a}.png", OB)), f"opt-{b}", s=560, l=1500)
for a, b in (("UDI", "udi"), ("sDA", "sda"), ("ASE", "ase"), ("Avg lux", "lux")):
    save(Image.open(f"{SRC}/Existing/{a}.png").convert("RGBA"), f"dash-{b}", s=420, l=None)
# search
save(Image.open(f"{SRC}/Design Explorar View.png").convert("RGBA"), "design-explorer", s=1400, l=2683)
save(Image.open(f"{SRC}/Pareto front configuration.png").convert("RGBA"), "pareto-octopus", s=900, l=2082)
save(crop(f"{SRC}/Pareto front.png", (20, 100, 1210, 680)), "pareto-front", s=640, l=1190)
save(Image.open(f"{SRC}/Plottes options.png").convert("RGBA"), "plotted-options", s=420, l=856)
# building, assembly
for i in range(1, 5):
    save(crop(f"{SRC}/exploaded 0{i}.png", (8, 46, 1598, 846)), f"assembly-{i}", s=900, l=1590)
# the Butterfly script sheet
save(Image.open("Handloom Script Final.jpg").convert("RGB"), "butterfly-script", s=1800, l=4000, q=82)
# legends and histograms from the presentation
for f, n in (("pp1_40_29_942ecd.png", "legend-cdm2"), ("pp2_18_26_822c5b.png", "legend-lux"), ("pp3_10_23_b843e1.png", "legend-udi"),
             ("pp3_34_23_744d7e.png", "legend-sda"), ("pp3_57_23_8d572a.png", "legend-ase"), ("pp3_81_23_a54171.png", "legend-avglux")):
    save(Image.open(pp(f)).convert("RGBA"), n, s=720, l=None, q=88)
for f, m in (("pp1_36_35_b96dde.png", "march"), ("pp1_53_35_8d87a0.png", "june"), ("pp1_69_36_eea99a.png", "september"), ("pp1_84_36_c9312c.png", "december")):
    im = Image.open(pp(f)).convert("RGBA"); save(im.crop((0, 0, im.width, int(im.height * 0.62))), f"hist-{m}", s=420, l=None, q=85)
