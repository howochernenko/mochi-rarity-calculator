import streamlit as st

# Sample rarity data
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
    17: ["nyo italy", "Serbia"],
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
    130: ["davie", "empire of stomaria", "stomaria", "cyprus", "turkish republic of northern cyprus", "trnc", "northern cyprus"]
}
}

# Flatten and normalize MOCHI_DATA
MOCHI_LOOKUP = {}
for rarity, names in MOCHI_DATA.items():
    for name in names:
        normalized = name.lower().replace("-", " ").replace("!", "").strip()
        MOCHI_LOOKUP[normalized] = rarity

# Helper: normalize mochi name
def normalize_name(name):
    return name.lower().replace("-", " ").replace("!", "").strip()

# Helper: get rarity from name
def get_rarity(mochi_name):
    return MOCHI_LOOKUP.get(normalize_name(mochi_name), None)

# Helper: label rarity
def rarity_label(rarity):
    if rarity <= 1:
        return "Ultra Rare"
    elif rarity <= 10:
        return "Rare"
    elif rarity <= 50:
        return "Uncommon"
    else:
        return "Common"

# Helper: round for output
def round_value(value, rarity=None):
    if rarity is not None and rarity < 1:
        return round(value, 1)
    return round(value * 2) / 2

# Main app
st.title("🐾 Mochi Trade Calculator")

mode = st.radio("Select mode:", ["Compare Mochis", "Value from Counts", "List by Rarity"])

if mode == "Compare Mochis":
    have = st.text_input("I have (e.g., trnc, god):")
    want = st.text_input("I want (e.g., fkm, rare):")

    if have and want:
        rarity_have = get_rarity(have)
        rarity_want = get_rarity(want)

        if rarity_have and rarity_want:
            val_have = 1 / rarity_have if rarity_have > 0 else None
            val_want = 1 / rarity_want if rarity_want > 0 else None

            if val_have is not None and val_want is not None:
                ratio = val_have / val_want
                st.success(f"**1 {have}** ≈ **{round_value(ratio)} {want}**")
            else:
                st.error("One of the mochis has invalid rarity (0 or missing).")
        else:
            st.error("Could not find one or both mochis in the rarity list.")

elif mode == "Value from Counts":
    count_input = st.text_input("Enter counts (e.g., 20x5, 3x2):")
    total_value = 0
    error = False

    if count_input:
        try:
            for part in count_input.split(","):
                amt_str, rarity_str = part.strip().lower().split("x")
                amt = float(amt_str.strip())
                rarity = float(rarity_str.strip())
                if rarity <= 0:
                    st.warning(f"Skipping invalid rarity: {rarity}")
                    continue
                value = amt / rarity
                total_value += value
        except Exception as e:
            error = True

    if not error and total_value > 0:
        st.success(f"Total trade value: **{round_value(total_value)}**")
    elif error:
        st.error("Invalid input format. Please use format like `20x5, 3x2`.")

elif mode == "List by Rarity":
    input_rarity = st.number_input("Enter desired rarity to search:", min_value=0.01, step=0.1)

    def get_all_mochis_at_rarity(r, tolerance=0.01):
        return [mochi for rar, names in MOCHI_DATA.items() if abs(rar - r) <= tolerance for mochi in names]

    rounded = round_value(input_rarity, input_rarity)
    mochis = get_all_mochis_at_rarity(rounded)

    if mochis:
        st.markdown(f"**Rarity {rounded}** ({rarity_label(rounded)}):")
        st.write(", ".join(sorted(set(mochis))))
    else:
        st.warning("No exact match found. Showing closest available:")
        closest_r = min(MOCHI_DATA.keys(), key=lambda x: abs(x - input_rarity))
        st.markdown(f"**Closest Rarity: {closest_r}** ({rarity_label(closest_r)}):")
        st.write(", ".join(sorted(set(MOCHI_DATA[closest_r]))))

