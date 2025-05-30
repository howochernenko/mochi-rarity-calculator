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

def is_latviaverse(name):
    """Check if a mochi name belongs to Latviaverse"""
    name = normalize_name(name)
    for aliases in LATVIAVERSE_DATA.values():
        if name in [normalize_name(alias) for alias in aliases]:
            return True
    return False

def get_rarity_by_name(name, force_type=None):
    """Get rarity with optional type enforcement"""
    name = normalize_name(name)
    if force_type == "regular":
        data = MOCHI_DATA
    elif force_type == "latviaverse":
        data = LATVIAVERSE_DATA
    else:
        data = {**MOCHI_DATA, **LATVIAVERSE_DATA}
    
    for rarity, aliases in data.items():
        if name in [normalize_name(alias) for alias in aliases]:
            return rarity
    return None

# ... (keep normalize_name, round_to_nearest_custom, get_closest_rarity functions)

def parse_entry(entry, force_type=None):
    entry = entry.strip().lower()
    if "x" in entry:
        part, amount_str = map(str.strip, entry.split("x", 1))
        rarity = get_rarity_by_name(part, force_type) or (float(part) if re.match(r"^\d+(\.\d+)?$", part) else None)
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
            rarity = get_rarity_by_name(entry, force_type)
            if rarity:
                return 1 / rarity
    return None

# ... (rest of your code until the mode selection)

if mode == "Compare two mochis":
    col1, col2 = st.columns(2)
    with col1:
        have = st.text_input("Your mochi:", placeholder="e.g., 'ukraine x 20', '5', or 'russia'")
    with col2:
        want = st.text_input("Their mochi:", placeholder="e.g., 'rainbow latvia', '0.5', or 'magical girl latvia x 3'")

    if have and want:
        # Detect mochi types
        have_is_lv = is_latviaverse(have.split("x")[0].strip() if "x" in have else have)
        want_is_lv = is_latviaverse(want.split("x")[0].strip() if "x" in want else want)
        
        if have_is_lv and want_is_lv:
            # Both are Latviaverse
            val_have = parse_entry(have, "latviaverse")
            val_want = parse_entry(want, "latviaverse")
            note = " (Latviaverse trade)"
        elif not have_is_lv and not want_is_lv:
            # Both are regular
            val_have = parse_entry(have, "regular")
            val_want = parse_entry(want, "regular")
            note = ""
        else:
            # Mixed types
            st.error("❌ Cannot compare Latviaverse mochis with regular mochis!")
            st.stop()
        
        if val_have is not None and val_want is not None:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need {1/ratio:.2f}× yours for a fair trade{note}")
            else:
                st.success(f"You need {ratio:.2f}× theirs for a fair trade{note}")
        else:
            st.warning("Could not interpret one or both entries. Please check the format.")

elif mode == "Trade multiple mochis":
    input_text = st.text_input("Enter mochis (comma-separated):", 
                             help="All mochis must be either regular OR Latviaverse")
    
    if input_text:
        entries = [x.strip() for x in input_text.split(",") if x.strip()]
        if not entries:
            st.warning("No valid entries found")
            st.stop()
        
        # Detect mochi type from first entry
        first_entry = entries[0].split("x")[0].strip() if "x" in entries[0] else entries[0]
        is_lv_group = is_latviaverse(first_entry)
        
        # Verify all mochis are same type
        for entry in entries:
            mochi_name = entry.split("x")[0].strip() if "x" in entry else entry
            if is_latviaverse(mochi_name) != is_lv_group:
                st.error(f"❌ Cannot mix Latviaverse and regular mochis! Found both '{first_entry}' and '{mochi_name}'")
                st.stop()
        
        # Process entries
        rarities = []
        for e in entries:
            val = parse_entry(e, "latviaverse" if is_lv_group else "regular")
            if val is None:
                st.warning(f"Could not parse: {e}")
                continue
            rarities.append(1/val)  # Store rarities instead of values
        
        if rarities:
            total_value = sum(1/r for r in rarities)
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)
            
            st.success(f"**Total value:** 1 mochi of rarity **~{exact_rarity:.2f}**")
            st.markdown(f"**Rounded to:** `{rounded_rarity}`")
            
            # Get suggestions from correct dataset
            dataset = LATVIAVERSE_DATA if is_lv_group else MOCHI_DATA
            suggestions = []
            for r, names in dataset.items():
                if r == rounded_rarity:
                    suggestions.extend(names)
            if not suggestions:
                closest = get_closest_rarity(rounded_rarity)
                for r, names in dataset.items():
                    if r == closest:
                        suggestions.extend(names)
            
            if suggestions:
                st.markdown("**Suggested mochis:** " + ", ".join([name.title() for name in suggestions]))

elif mode == "Value from Counts":
    input_text = st.text_area("Enter mochis (one per line or comma-separated):",
                            help="Format: 'mochi x amount' or 'rarity x amount'\nAll mochis must be same type (regular or Latviaverse)")
    
    if input_text:
        entries = []
        for line in input_text.split("\n"):
            entries.extend([x.strip() for x in line.split(",") if x.strip()])
        
        if not entries:
            st.warning("No valid entries found")
            st.stop()
        
        # Detect mochi type from first entry
        first_entry = entries[0].split("x")[0].strip() if "x" in entries[0] else entries[0]
        is_lv_group = is_latviaverse(first_entry)
        
        # Verify all mochis are same type
        for entry in entries:
            mochi_name = entry.split("x")[0].strip() if "x" in entry else entry
            if is_latviaverse(mochi_name) != is_lv_group:
                st.error(f"❌ Cannot mix Latviaverse and regular mochis! Found both '{first_entry}' and '{mochi_name}'")
                st.stop()
        
        # Process entries
        total_value = 0
        for entry in entries:
            val = parse_entry(entry, "latviaverse" if is_lv_group else "regular")
            if val is None:
                st.warning(f"Could not parse: {entry}")
                continue
            total_value += val

        if total_value > 0:
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)
            
            st.success(f"**Total value:** {total_value:.2f} (1 mochi of rarity ~{exact_rarity:.2f})")
            st.markdown(f"**Rounded to:** `{rounded_rarity}`")
            
            # Get suggestions from correct dataset
            dataset = LATVIAVERSE_DATA if is_lv_group else MOCHI_DATA
            suggestions = []
            for r, names in dataset.items():
                if r == rounded_rarity:
                    suggestions.extend(names)
            if not suggestions:
                closest = get_closest_rarity(rounded_rarity)
                for r, names in dataset.items():
                    if r == closest:
                        suggestions.extend(names)
            
            if suggestions:
                st.markdown("**Suggested mochis:** " + ", ".join([name.title() for name in suggestions]))

st.markdown("---")
st.markdown("Disclaimer: Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")
