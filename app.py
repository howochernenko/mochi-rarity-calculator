import streamlit as st
import re

# Sample rarity data (simplified)
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

# Flatten and normalize MOCHI_DATA
MOCHI_LOOKUP = {}
for rarity, names in MOCHI_DATA.items():
    for name in names:
        normalized = name.lower().replace("-", " ").replace("!", "").strip()
        MOCHI_LOOKUP[normalized] = rarity

# Normalize name
def normalize_name(name):
    return name.lower().replace("-", " ").replace("!", "").strip()

# Get rarity
def get_rarity(name):
    return MOCHI_LOOKUP.get(normalize_name(name), None)

# Get value (1/rarity)
def get_value(name):
    rarity = get_rarity(name)
    if rarity:
        return 1 / rarity
    return 0

# Parse entry
def parse_entry(entry):
    entry = entry.strip().lower()
    if "x" in entry:
        part, amount_str = map(str.strip, entry.split("x", 1))
        rarity = get_rarity(part) or (float(part) if part.replace(".", "", 1).isdigit() else None)
        amount = float(amount_str) if amount_str.replace(".", "", 1).isdigit() else None
        return amount / rarity if rarity and amount else None
    else:
        try:
            return 1 / float(entry)
        except:
            rarity = get_rarity(entry)
            return 1 / rarity if rarity else None

# --- Streamlit App ---
st.title("🐾 Mochi Trade Calculator")

mode = st.radio("Select mode:", ["Compare two mochis", "Trade multiple mochis", "Calculate how many mochis for a fair trade"])

if mode == "Calculate how many mochis for a fair trade":
    have_input = st.text_input("Your mochis (e.g., '1 pierre, 1 scotland, 5 new zealands'):")
    want_input = st.text_input("Their mochis (e.g., '15 ukraines'):")

    if have_input and want_input:
        try:
            have_entries = [x.strip() for x in have_input.split(",") if x.strip()]
            want_entries = [x.strip() for x in want_input.split(",") if x.strip()]
            have_values = [get_value(e) for e in have_entries]
            want_values = [get_value(e) for e in want_entries]
            total_have_value = sum(have_values)
            total_want_value = sum(want_values)
            difference = total_want_value - total_have_value

            new_zealand_value = get_value("new zealand")
            if difference > 0:
                required = difference / new_zealand_value
                st.success(f"You need **{required:.2f} New Zealands** to balance the trade.")
            else:
                st.success("Your mochis are worth more than their mochis! The trade is already fair.")
        except Exception as e:
            st.warning(f"Error: {e}")

elif mode == "Compare two mochis":
    have = st.text_input("Your mochi (name, rarity, or `mochi x amount`):")
    want = st.text_input("Their mochi (name, rarity, or `mochi x amount`):")

    if have and want:
        val_have = parse_entry(have)
        val_want = parse_entry(want)

        if val_have and val_want:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"You need **{1/ratio:.2f}** of your mochi to match theirs.")
            else:
                st.success(f"They need **{ratio:.2f}** of their mochi to match yours.")
        else:
            st.warning("Could not interpret one or both entries. Try using formats like `ukraine x 20`, `5`, or `russia`.")

elif mode == "Trade multiple mochis":
    input_text = st.text_input("Enter your mochis (comma separated, names or rarities):")

    if input_text:
        try:
            entries = [x.strip() for x in input_text.split(",") if x.strip()]
            rarities = []
            for e in entries:
                if re.match(r"^\d+(\.\d+)?$", e):
                    rarities.append(float(e))
                else:
                    r = get_rarity(e)
                    if r:
                        rarities.append(r)

            if rarities:
                total = sum(1 / r for r in rarities)
                exact = 1 / total
                rounded = round(exact, 1 if exact < 1 else 0.5)
                if rounded >= 1:
                    rounded = round(rounded * 2) / 2  # Nearest .5 for >= 1
                else:
                    rounded = round(rounded, 1)       # Nearest .1 for < 1

                mochis = [mochi for rarity, names in MOCHI_DATA.items() for mochi in names if round(rarity, 2) == round(rounded, 2)]

                if mochis:
                    st.success(f"Your mochis are roughly worth one of rarity **~{exact:.2f}**, rounded to **{rounded}**.\n\nMochis at that rarity: {', '.join(mochis)}")
                else:
                    st.info(f"Closest rarity to your mochis: **~{exact:.2f}**, rounded to **{rounded}**, but no exact match was found.")
            else:
                st.warning("Could not recognize any valid mochi names or rarities.")
        except Exception as e:
            st.warning(f"Error: {e}")
