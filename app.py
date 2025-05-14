import streamlit as st

# Rarity Data
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

# Helper: normalize mochi name
def normalize_name(name):
    return name.lower().replace("-", " ").replace("!", "").strip()

# Helper: get rarity from name
def get_rarity(mochi_name):
    return MOCHI_LOOKUP.get(normalize_name(mochi_name), None)

# Helper: calculate the value of a mochi (1/rareness)
def get_value(mochi_name):
    rarity = get_rarity(mochi_name)
    if rarity:
        return 1 / rarity
    return 0  # If rarity is not found

# Main app
st.title("🐾 Mochi Trade Calculator")

mode = st.radio("Select mode:", ["Compare Mochis", "Calculate Fair Trade Value"])

if mode == "Compare Mochis":
    have = st.text_input("I have (e.g., trnc, god):")
    want = st.text_input("I want (e.g., fkm, rare):")

    if have and want:
        rarity_have = get_rarity(have)
        rarity_want = get_rarity(want)

        if rarity_have and rarity_want:
            val_have = get_value(have)
            val_want = get_value(want)

            if val_have and val_want:
                ratio = val_have / val_want
                st.success(f"**1 {have}** ≈ **{round(ratio)} {want}**")
            else:
                st.error("One of the mochis has invalid rarity (0 or missing).")
        else:
            st.error("Could not find one or both mochis in the rarity list.")

elif mode == "Calculate Fair Trade Value":
    # Input the mochis and their counts (you have and they want)
    have_input = st.text_input("I have (e.g., 1 pierre, 2 scotland, 5 new zealand):")
    want_input = st.text_input("They want (e.g., 15 ukraine):")

    def parse_input(input_str):
        """Parse input like '1 pierre' into count and mochi name."""
        parsed = []
        for part in input_str.split(","):
            parts = part.strip().split(" ")
            count = int(parts[0])
            mochi = " ".join(parts[1:])
            parsed.append((count, mochi))
        return parsed

    # Parse inputs
    have_mochis = parse_input(have_input)
    want_mochis = parse_input(want_input)

    if have_mochis and want_mochis:
        # Calculate total value of what you have
        total_value_have = sum(count * get_value(mochi) for count, mochi in have_mochis)
        
        # Calculate total value of what they want
        total_value_want = sum(count * get_value(mochi) for count, mochi in want_mochis)

        if total_value_want > total_value_have:
            # Calculate how much more of the mochis you need
            remaining_value = total_value_want - total_value_have
            needed_mochis = []

            # Look at the mochis you have to fill the value gap
            for count, mochi in have_mochis:
                mochi_value = get_value(mochi)
                if mochi_value > 0:
                    needed_count = remaining_value / mochi_value
                    needed_mochis.append(f"{mochi}: {round(needed_count)} more")

            st.success(f"You need more mochis to match the trade value: {', '.join(needed_mochis)}")
        else:
            st.success(f"Your mochis are enough! You have {round(total_value_have)} value, and they want {round(total_value_want)}.")
    else:
        st.error("Invalid input format. Please use format like '1 pierre, 2 scotland, 5 new zealand'.")

        st.markdown(f"**Closest Rarity: {closest_r}** ({rarity_label(closest_r)}):")
        st.write(", ".join(sorted(set(MOCHI_DATA[closest_r]))))

