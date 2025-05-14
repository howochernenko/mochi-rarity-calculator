import streamlit as st
import re
from collections import defaultdict

# Mochi rarity database
MOCHI_DATA = {MOCHI\_DATA = {
0.1: \["god", "fairy king of the mochi", "fairy king", "fkm"],
0.5: \["soviet union", "ussr"],
0.6: \["allied powers", "allies", "allie"],
0.7: \["bad friends trio", "bad friend trio", "bad friends trios", "bft"],
0.8: \["axis powers", "axis"],
0.9: \["franco-british union", "fbu"],
1: \["america", "holy roman empire", "holy rome", "ottoman empire", "america's daddy", "daddy", "hre"],
2: \["ancient rome", "rome", "grandpa rome", "roman empire", "england", "polish-lithuanian commonwealth", "plc", "tibet"],
2.5: \["2p japan"],
3: \["nyo japan", "knights templar", "house of habsburg", "habsburg", "hapsburg", "neko england"],
3.14: \["ancient greece", "mama greece", "hellas"],
4: \["neko japan", "tama", "neko prussia", "pictonian princess", "neko russia"],
5: \["nyo poland", "austria-hungary", "japan", "neko america", "americat"],
5.5: \["2p italy"],
6: \["neko germany", "germouser", "tony", "nyo france", "neko france"],
6.5: \["2p germany"],
7: \["nyo korea", "korea", "south korea", "neko italy", "itabby", "gino", "sealand"],
7.2: \["domain and realms of the shadows and the darkness", "drsd"],
8: \["poland", "neko romano", "romacat", "nyo spain", "nyo russia"],
8.24: \["portugal"],
9: \["uncensored china", "nyo canada", "russia", "prussia"],
10: \["italy", "north italy", "germany", "spain"],
11: \["france", "romano", "south italy", "nyo america"],
12: \["wales", "germania", "germanic tribes", "canada"],
13: \["nyo lithuania", "china", "nyo england"],
14: \["neko austria", "ancient egypt", "mama egypt", "kemet", "czechoslovakia", "waiter"],
15: \["sweden", "nyo belarus", "nyo germany"],
16: \["neko hungary", "nyo finland", "quebec"],
17: \["nyo italy"],
18: \["south africa", "pictonian"],
19: \["nyo prussia"],
20: \["nyo portugal", "nyo turkey", "seychelles' mystery friend", "seychelles friend", "mystery friend", "nyo sweden"],
25: \["benelux", "greenland", "nyo romano", "nyo china"],
30: \["aerican empire", "aerica", "flying mint bunny", "nyo switzerland", "nyo norway"],
35: \["hanatamago", "kyoto", "teutonic knights", "ecuador", "osaka"],
40: \["pochi", "mongolia", "persia", "kingdom of pontus", "pontus", "mr. puffin"],
45: \["pookie", "finland", "tonga", "america's whale", "whale", "chibitalia"],
50: \["genoa", "mr. newspapers", "hesse", "baltic states", "baltics", "baltic trio"],
55: \["gilbird", "belgium", "hong kong", "norway"],
60: \["philippines", "belarus", "nyo latvia", "iceland"],
65: \["pierre", "mr. un", "united nations", "malaysia", "seychelles"],
70: \["lithuania", "estonia", "chibiromano", "czechia", "czech republic"],
75: \["latvia", "scotland", "singapore", "greece"],
80: \["liechtenstein", "taiwan", "nyo austria", "ireland"],
85: \["croatia", "slowjamastan", "austria", "hungary"],
90: \["switzerland", "ukraine", "romania", "seborga"],
95: \["moldova", "luxembourg", "molossia", "netherlands", "holland"],
100: \["indonesia", "slovakia", "northern ireland", "wy"],
105: \["picardy", "shujinko", "denmark", "new zealand", "aotearoa", "turkey"],
110: \["niko niko jr", "niko jr", "nyo hungary", "australia", "ladonia"],
115: \["niko niko republic", "niko niko", "bulgaria", "macau", "vietnam"],
120: \["kugelmugel", "india", "monaco", "egypt"],
125: \["thailand", "hutt river", "cuba", "cameroon"],
130: \["davie", "empire of stomaria", "stomaria", "cyprus", "turkish republic of northern cyprus", "trnc", "northern cyprus"]
} 

# Build reverse index: name/alias -> rarity
NAME_TO_RARITY = {}
for rarity, names in MOCHI_DATA.items():
    for name in names:
        NAME_TO_RARITY[name.lower()] = rarity

def normalize_name(name):
    return re.sub(r'[-!]', ' ', re.sub(r'[^\w\s]', '', name.lower())).strip()

def calculate_total_value(entry):
    parts = re.findall(r'(\d+)x([\w\s-!]+)', entry)
    total = 0
    unknown = []
    for count_str, name in parts:
        count = int(count_str)
        norm = normalize_name(name)
        rarity = NAME_TO_RARITY.get(norm)
        if rarity is None:
            unknown.append(name)
        else:
            # Event mochi bonus (if needed): count *= 2
            total += rarity * count
    return total, unknown

def get_mochis_for_rarity(target):
    return MOCHI_DATA.get(target, [])

# Streamlit UI
st.title("🧮 Mochi Trade Calculator")

left = st.text_input("Enter Left Side (e.g. 20xamerica, 3xgod):")
right = st.text_input("Enter Right Side (optional for comparison):")

left_value, left_unknown = calculate_total_value(left)
st.write(f"🔹 Left Value: **{left_value}**")
if left_unknown:
    st.warning(f"Unrecognized mochis: {', '.join(left_unknown)}")

if right:
    right_value, right_unknown = calculate_total_value(right)
    st.write(f"🔸 Right Value: **{right_value}**")
    if right_unknown:
        st.warning(f"Unrecognized mochis: {', '.join(right_unknown)}")

    # Value comparison
    diff = abs(left_value - right_value)
    if diff < 0.1:
        st.success("✅ Trade is approximately fair!")
    else:
        st.info(f"Difference: **{diff}**")

# Suggest mochis at or near value
rounded = round(left_value * 2) / 2 if left_value >= 1 else round(left_value, 1)
match = get_mochis_for_rarity(rounded)

st.subheader("🎯 Mochis at Target Rarity")
st.write(f"Rounded Value: **{rounded}**")
if match:
    st.write(", ".join(match))
else:
    # Suggest closest if none found
    closest = min(MOCHI_DATA.keys(), key=lambda r: abs(r - rounded))
    st.info(f"No exact match. Closest rarity: {closest}")
    st.write(", ".join(MOCHI_DATA[closest]))

