import streamlit as st
import re
import math
import pyperclip

# Dark mode toggle
dark_mode = st.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #111; color: #eee; }
        .stApp { background-color: #111; color: #eee; }
        .stTextInput > div > div > input { background-color: #222; color: #eee; }
        .stTextArea textarea { background-color: #222; color: #eee; }
        </style>
        """,
        unsafe_allow_html=True,
    )

MOCHI_DATA = {
    0.1: ["god", "fairy king of the mochi", "fairy king", "fkm"],
    0.5: ["soviet union", "ussr"],
    0.6: ["allied powers", "allies", "allie"],
    0.7: ["bad friends trio", "bad friend trio", "bad friends trios", "bft"],
    0.8: ["axis powers", "axis"],
    0.9: ["franco-british union", "fbu"],
    1: ["america", "holy roman empire", "holy rome", "ottoman empire", "america's daddy", "daddy", "hre"],
    2: ["ancient rome", "rome", "grandpa rome", "roman empire", "england", "polish-lithuanian commonwealth", "plc", "tibet"],
    2.5: ["2p japan"],
    3: ["nyo japan", "knights templar", "house of habsburg", "habsburg", "hapsburg", "neko england"],
    3.14: ["ancient greece", "mama greece", "hellas"],
    4: ["neko japan", "tama", "neko prussia", "pictonian princess", "neko russia"],
    5: ["nyo poland", "austria-hungary", "japan", "neko america", "americat"],
    5.5: ["2p italy"],
    6: ["neko germany", "germouser", "tony", "nyo france", "neko france"],
    6.5: ["2p germany"],
    7: ["nyo korea", "korea", "south korea", "neko italy", "itabby", "gino", "sealand"],
    7.2: ["domain and realms of the shadows and the darkness", "drsd"],
    8: ["poland", "neko romano", "romacat", "nyo spain", "nyo russia"],
    8.24: ["portugal"],
    9: ["uncensored china", "nyo canada", "russia", "prussia"],
    10: ["italy", "north italy", "germany", "spain"],
    11: ["france", "romano", "south italy", "nyo america"],
    12: ["wales", "germania", "germanic tribes", "canada"],
    13: ["nyo lithuania", "china", "nyo england"],
    14: ["neko austria", "ancient egypt", "mama egypt", "kemet", "czechoslovakia", "waiter"],
    15: ["sweden", "nyo belarus", "nyo germany"],
    16: ["neko hungary", "nyo finland", "quebec"],
    17: ["nyo italy", "serbia"],
    18: ["south africa", "pictonian"],
    19: ["nyo prussia"],
    20: ["nyo portugal", "nyo turkey", "seychelles' mystery friend", "seychelles friend", "mystery friend", "nyo sweden"],
    25: ["benelux", "greenland", "nyo romano", "nyo china"],
    30: ["aerican empire", "aerica", "flying mint bunny", "nyo switzerland", "nyo norway"],
    35: ["hanatamago", "kyoto", "teutonic knights", "ecuador", "osaka"],
    40: ["pochi", "mongolia", "persia", "kingdom of pontus", "pontus", "mr. puffin"],
    45: ["pookie", "finland", "tonga", "america's whale", "whale", "chibitalia"],
    50: ["genoa", "mr. newspapers", "hesse", "baltic states", "baltics", "baltic trio"],
    55: ["gilbird", "belgium", "hong kong", "norway"],
    60: ["philippines", "belarus", "nyo latvia", "iceland"],
    65: ["pierre", "mr. un", "united nations", "malaysia", "seychelles"],
    70: ["lithuania", "estonia", "chibiromano", "czechia", "czech republic"],
    75: ["latvia", "scotland", "singapore", "greece"],
    80: ["liechtenstein", "taiwan", "nyo austria", "ireland"],
    85: ["croatia", "slowjamastan", "austria", "hungary"],
    90: ["switzerland", "ukraine", "romania", "seborga"],
    95: ["moldova", "luxembourg", "molossia", "netherlands", "holland"],
    100: ["indonesia", "slovakia", "northern ireland", "wy"],
    105: ["picardy", "shujinko", "denmark", "new zealand", "aotearoa", "turkey"],
    110: ["niko niko jr", "niko jr", "nyo hungary", "australia", "ladonia"],
    115: ["niko niko republic", "niko niko", "bulgaria", "macau", "vietnam"],
    120: ["kugelmugel", "india", "monaco", "egypt"],
    125: ["thailand", "hutt river", "cuba", "cameroon"],
    130: ["davie", "empire of stomaria", "stomaria", "cyprus", "turkish republic of northern cyprus", "trnc", "northern cyprus"],
}

# Build alias to rarity map
alias_map = {}
for rarity, names in MOCHI_DATA.items():
    for name in names:
        alias_map[name.lower()] = rarity

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[-!]", " ", name)
    name = re.sub(r"[^\w\s']", "", name)
    return name.strip()

def calculate_trade_value(input_text):
    entries = re.findall(r'(\d+)x(.+?)(?:,|$)', input_text.lower())
    total = 0
    for count_str, name in entries:
        count = int(count_str)
        name = normalize_name(name)
        rarity = alias_map.get(name)
        if rarity is not None:
            multiplier = 2 if 'event' in name else 1
            total += count * rarity * multiplier
    return total

def round_value(value):
    if value < 1:
        return round(value, 1)
    return round(value * 2) / 2

def get_mochis_by_rarity(rarity):
    if rarity in MOCHI_DATA:
        return MOCHI_DATA[rarity]
    closest = min(MOCHI_DATA.keys(), key=lambda x: abs(x - rarity))
    return MOCHI_DATA[closest]

st.title("Mochi Trade Calculator")

input_text = st.text_input("Enter mochis (e.g. `20x5, 3xamerica`):")

if input_text:
    total_value = calculate_trade_value(input_text)
    rounded = round_value(total_value)
    st.markdown(f"**Raw Value**: `{total_value}`  \n**Rounded Value**: `{rounded}`")

    mochis = get_mochis_by_rarity(rounded)
    mochi_list = ", ".join(mochis)
    st.markdown(f"**Matching Mochis**: {mochi_list}")

    if st.button("📋 Copy Mochi List"):
        pyperclip.copy(mochi_list)
        st.success("Copied to clipboard!")
