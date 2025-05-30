import streamlit as st
import re

st.title("🌟 Mochis Trade Calculator")

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

LATVIAVERSE_DATA = {
    0.5: ["rainbow latvia"],
    1.0: ["latvian empire", "kingdom of latvia", "main character latvia"],
    2.0: ["magical girl latvia", "spring god latvia", "mother ocean latvia"],
    3.0: ["roman latvia", "pirate latvia", "latvialoid"],
    4.0: ["muscular latvia", "british latvia", "robot latvia", "l4t-v14"],
    5.0: ["neko latvia", "latvian soviet socialist republic", "flow latvia", "award-winning latvia"],
    6.0: ["polish-lithuanian latvia", "cuirassier latvia", "yugoslatvia"],
    7.0: ["nova letônia", "zombie latvia", "alien latvia"],
    8.0: ["8-bit latvia"],
    9.0: ["viking latvia", "german latvia", "vampire latvia"],
    10.0: ["livonian order", "jibaro latvia", "apocalyptic latvia"],
    11.0: ["guerrilla latvia", "decora latvia", "goth latvia"],
    12.0: ["ladybug latvia", "grape latvia", "drunken latvia"],
    13.0: ["minimum wage latvia"],
    14.0: ["green latvia", "red latvia", "blue latvia", "orange latvia", "yellow latvia", "purple latvia", "pink latvia"],
    15.0: ["gray latvia"]
}

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.'’'–—]", "", name)
    name = name.replace("-", " ").replace("!", " ")
    return name.strip()

def round_to_nearest_custom(n):
    """Your original rounding function"""
    return round(n, 1) if n < 1 else round(n * 2) / 2

def get_closest_rarity(target, data):
    """Get closest rarity from specified dataset"""
    return min(data.keys(), key=lambda r: abs(r - target))

def get_rarity_by_name(name, mochi_type="common"):
    """Get rarity for specific mochi type"""
    name = normalize_name(name)
    data = LATVIAVERSE_DATA if mochi_type.lower() == "latviaverse" else MOCHI_DATA
    for rarity, aliases in data.items():
        if name in [normalize_name(alias) for alias in aliases]:
            return rarity
    return None

def parse_entry(entry, mochi_type):
    """Your original parse_entry with type checking"""
    entry = entry.strip().lower()
    if "x" in entry:
        part, amount_str = map(str.strip, entry.split("x", 1))
        rarity = get_rarity_by_name(part, mochi_type) or (float(part) if re.match(r"^\d+(\.\d+)?$", part) else None)
        try:
            amount = float(amount_str)
            return amount / rarity if rarity else None
        except:
            return None
    else:
        if re.match(r"^\d+(\.\d+)?$", entry):
            try:
                return 1 / float(entry)
            except:
                return None
        else:
            rarity = get_rarity_by_name(entry, mochi_type)
            return 1 / rarity if rarity else None

# Main App
def main():
    st.title("🌟 Mochis Trade Calculator")
    
    mochi_type = st.radio("Select mochi type:", ["Common", "Latviaverse"])
    mode = st.radio("Choose mode:", ["Compare two mochis", "Trade multiple mochis", "Value from Counts"])
    
    current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA

    if mode == "Value from Counts":
        input_text = st.text_area(
            "Enter your mochis as 'rarity/mochi x amount', comma-separated:",
            help="Example: 'ukraine x 20, 5 x 5' for Common or 'rainbow latvia x 2' for Latviaverse"
        )

        if input_text:
            entries = [x.strip() for x in input_text.split(",") if x.strip()]
            total = 0
            invalid_entries = []
            
            for entry in entries:
                val = parse_entry(entry, mochi_type.lower())
                if val:
                    total += val
                else:
                    invalid_entries.append(entry)
            
            if invalid_entries:
                st.warning(f"Could not interpret: {', '.join(invalid_entries)}")
            
            if total > 0:
                exact = 1 / total
                rounded = round_to_nearest_custom(exact)
                
                suggestions = []
                for r, names in current_data.items():
                    if r == rounded:
                        suggestions.extend(names)
                
                if not suggestions:
                    closest = get_closest_rarity(rounded, current_data)
                    for r, names in current_data.items():
                        if r == closest:
                            suggestions.extend(names)
                
                st.success(f"Your total value is equivalent to a mochi of rarity **~{exact:.2f}**.")
                st.markdown(f"**Rounded to:** `{rounded}`")
                
                if suggestions:
                    st.markdown("**Suggested mochis at that rarity:** " + ", ".join([name.title() for name in suggestions]))

    st.markdown("---")
    st.markdown("Disclaimer: Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")

if __name__ == "__main__":
    main()
