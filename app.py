import streamlit as st
import re

st.title("🌟 Mochis Trade Calculator")

# Mochi rarity data (rarity: [aliases])
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
    17: ["nyo italy"],
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

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.’'–—]", "", name)
    name = name.replace("-", " ").replace("!", " ")
    return name.strip()

def get_rarity_by_name(name):
    name = normalize_name(name)
    for rarity, aliases in MOCHI_DATA.items():
        if name in [normalize_name(alias) for alias in aliases]:
            return rarity
    return None

def round_to_nearest_custom(n):
    return round(n, 1) if n < 1 else round(n * 2) / 2

def get_closest_rarity(target):
    return min(MOCHI_DATA.keys(), key=lambda r: abs(r - target))

def get_all_mochis_at_rarity(rarity):
    return [name.title() for r, names in MOCHI_DATA.items() if r == rarity for name in names]

def parse_entry(entry):
    entry = entry.strip().lower()
    if "x" in entry:
        part, amount_str = map(str.strip, entry.split("x", 1))
        rarity = get_rarity_by_name(part) or (float(part) if re.match(r"^\d+(\.\d+)?$", part) else None)
        try:
            amount = float(amount_str)
        except:
            amount = None
        if rarity and amount:
            return amount / rarity
    else:
        if re.match(r"^\d+(\.\d+)?$", entry):
            try:
                rarity = float(entry)
                return 1 / rarity
            except:
                return None
        else:
            rarity = get_rarity_by_name(entry)
            if rarity:
                return 1 / rarity
    return None

mode = st.radio("Choose mode:", ["Compare two mochis", "Trade multiple mochis", "Value from Counts"])

if mode == "Compare two mochis":
    have = st.text_input("Your mochi (name, rarity, or `mochi x amount`):")
    want = st.text_input("Their mochi (name, rarity, or `mochi x amount`):")

    if have and want:
        val_have = parse_entry(have)
        val_want = parse_entry(want)
        if val_have is not None and val_want is not None:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need **{1/ratio:.2f}** times that for a fair trade, for example they entered four iceland and it says 5 so it would be 4 x 5 which is 20 icelands")
            else:
                st.success(f"You need **{ratio:.2f}** times that for a fair trade, for example you entered four iceland and it says 5 so it would be 4 x 5 which is 20 icelands")
        else:
            st.warning("Could not interpret one or both entries. Please check the format (e.g., `ukraine x 20`, `5`, or `russia`).")

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
                    r = get_rarity_by_name(e)
                    if r:
                        rarities.append(r)

            if rarities:
                total = sum(1 / r for r in rarities)
                exact = 1 / total
                rounded = round_to_nearest_custom(exact)
                mochis = get_all_mochis_at_rarity(rounded) or get_all_mochis_at_rarity(get_closest_rarity(rounded))

                st.success(f"These mochis can be traded for one mochi of rarity **~{exact:.2f}**.")
                st.markdown(f"**Rounded to:** `{rounded}`")
                if mochis:
                    st.markdown("**Suggested mochis at that rarity:** " + ", ".join(mochis))
        except Exception as e:
            st.warning(f"Error: {e}")

elif mode == "Value from Counts":
    input_text = st.text_area("Enter your mochis as 'rarity/mochi x amount', comma-separated (e.g. ukraine x 20, 5 x 5):")

    if input_text:
        try:
            entries = [x.strip() for x in input_text.split(",") if x.strip()]
            total = 0
            for entry in entries:
                val = parse_entry(entry)
                if val:
                    total += val
            if total:
                exact = 1 / total
                rounded = round_to_nearest_custom(exact)
                mochis = get_all_mochis_at_rarity(rounded) or get_all_mochis_at_rarity(get_closest_rarity(rounded))

                st.success(f"Your total value is equivalent to a mochi of rarity **~{exact:.2f}**.")
                st.markdown(f"**Rounded to:** `{rounded}`")
                if mochis:
                    st.markdown("**Suggested mochis at that rarity:** " + ", ".join(mochis))
        except Exception as e:
            st.warning(f"Error: {e}")

st.markdown("---")
st.markdown("Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")
