import streamlit as st
import re
import difflib

st.title("🌟 Mochis Trade Calculator")

# Data with rarities and aliases
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
    5: ["austria-hungary", "japan", "neko america", "americat"],
    5.5: ["2p italy"],
    6: ["neko germany", "germouser", "tony", "nyo france", "neko france"],
    6.5: ["2p germany"],
    7: ["nyo korea", "korea", "south korea", "neko italy", "itabby", "gino", "sealand"],
    7.2: ["domain and realms of the shadows and the darkness", "drsd"],
    8: ["poland", "neko romano", "romacat", "nyo spain", "nyo russia"],
    8.24: ["portugal"],
    9: ["uncensored china", "nyo canada", "russia", "prussia"],
    10: ["italy", "north italy", "germany", "nyo poland", "spain"],
    11: ["france", "romano", "south italy", "nyo america"],
    12: ["wales", "germania", "germanic tribes", "canada", "nyo prussia"],
    13: ["nyo lithuania", "china", "nyo england"],
    14: ["neko austria", "ancient egypt", "mama egypt", "kemet", "czechoslovakia", "waiter"],
    15: ["sweden", "nyo belarus", "nyo germany"],
    16: ["quebec"],
    17: ["nyo italy", "serbia"],
    18: ["nyo finland"],
    19: ["neko hungary", "pictonian", "south africa"],
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
    95: ["moldova", "luxembourg", "luxemburg", "molossia", "netherlands", "holland"],
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

def normalize_name(name: str) -> str:
    """Normalize input for matching: lower case, remove punctuation, replace dashes."""
    name = name.lower()
    name = re.sub(r"[.'’–—]", "", name)
    name = name.replace("-", " ").replace("!", " ")
    return name.strip()

def get_rarity_by_name(name: str, mochi_type="common"):
    """Return rarity number by mochi alias name, or None if not found."""
    name = normalize_name(name)
    data = LATVIAVERSE_DATA if mochi_type == "latviaverse" else MOCHI_DATA
    for rarity, aliases in data.items():
        normalized_aliases = [normalize_name(alias) for alias in aliases]
        if name in normalized_aliases:
            return rarity
    return None

def suggest_similar_mochis(input_name, data):
    """Suggest similar mochi names when no exact match found"""
    input_name = normalize_name(input_name)
    all_aliases = [normalize_name(alias) for names in data.values() for alias in names]
    matches = difflib.get_close_matches(input_name, all_aliases, n=5, cutoff=0.6)
    return matches

def parse_entry(entry: str, mochi_type="common"):
    """Parse a single entry like 'netherlands x2' or '0.5' and return float value (amount / rarity)."""
    entry = entry.strip().lower()
    if "x" in entry:
        parts = entry.split("x")
        if len(parts) >= 2:
            part = parts[0].strip()
            amount_str = parts[1].strip()
            rarity = get_rarity_by_name(part, mochi_type)
            if rarity is None:
                if re.match(r"^\d+(\.\d+)?$", part):
                    rarity = float(part)
                else:
                    return None
            try:
                amount = float(amount_str)
                return amount / rarity if rarity else None
            except:
                return None
        else:
            return None
    else:
        if re.match(r"^\d+(\.\d+)?$", entry):
            try:
                return 1 / float(entry)
            except:
                return None
        rarity = get_rarity_by_name(entry, mochi_type)
        if rarity:
            return 1 / rarity
    return None

def round_to_nearest_custom(n):
    """Rounds to nearest 0.1 if below 1, else nearest 0.5."""
    if n < 1:
        return round(n, 1)
    else:
        return round(n * 2) / 2

def get_closest_rarity(target, data):
    """Find closest rarity key to target in data dictionary."""
    return min(data.keys(), key=lambda r: abs(r - target))

def tag_based_search():
    st.subheader("🏷️ Tag-Based Mochi Search")
    
    TAG_CATEGORIES = {
        "Neko": ["neko"],
        "Nyo": ["nyo"],
        "2P": ["2p"],
        "Creature": ["whale", "gilbird", "puffin", "flying", "pictonian", "hanatamago", "pochi", "tony", "pierre", "pookie"],
        "Micronations": ["wy", "sealand", "aerican", "niko", "ladonia", "seborga", "drsd", "slowjamastan", "kugelmugel", "stomaria"],
    }
    
    selected_tags = st.multiselect(
        "Search by tags:",
        options=list(TAG_CATEGORIES.keys()),
        default=["Neko"]
    )
    
    if selected_tags:
        results = {}
        search_patterns = []
        
        for tag in selected_tags:
            search_patterns.extend(TAG_CATEGORIES[tag])
        
        for rarity, names in current_data.items():
            for name in names:
                normalized_name = normalize_name(name)
                if any(pattern in normalized_name for pattern in search_patterns):
                    if rarity not in results:
                        results[rarity] = []
                    results[rarity].append(name)
        
        if results:
            st.success(f"Found {sum(len(v) for v in results.values())} matching mochis:")
            
            for rarity in sorted(results.keys()):
                with st.expander(f"Rarity {rarity}: {len(results[rarity])} mochis"):
                    cols = st.columns(3)
                    for i, name in enumerate(sorted(results[rarity])):
                        cols[i%3].write(f"- {name.title()}")
        else:
            st.warning("No mochis found matching these tags")

def mochi_value_converter(current_dict):
    st.subheader("🔁 Mochi Value Converter")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        input_mochis = st.text_input(
            "Your mochis:", 
            placeholder="e.g. '5 russia, 1 ukraine' or 'russia, 3 benelux'"
        )
    with col2:
        target_mochi = st.text_input(
            "Value in:", 
            placeholder="e.g. 'belarus'"
        )
    
    if input_mochis and target_mochi:
        total_value = 0
        invalid_entries = []
        
        # entries = []
        # for part in input_mochis.split(","):
        #     entries.extend([x.strip() for x in part.split("\n") if x.strip()])
        entries = [x.strip() for x in re.split(r'[,\n]', input_mochis) if x.strip()]
        target_val = current_dict[target_mochi]
        for entry in entries:
            entry_split = entry.strip().split()
            if entry_split and entry_split[0].isdigit():
                #st.success(f">>>{entry_split[0]}")
                n = int(entry_split[0])
                real_entry = ' '.join(entry_split[1:]).strip()
                #real_entry = re.sub(r'^\d+\s+', '', entry).strip()
            else:
                n = 1
                real_entry = entry.strip()
            val = current_dict[real_entry] / n
            
            # if "*" in entry:
            #     val = parse_entry(entry, mochi_type.lower())
            # else:
            #     val = current_dict[entry]
                # parts = entry.split()
                # if len(parts) >= 2 and parts[0].replace('.', '', 1).isdigit():
                #     val = parse_entry(f"{' '.join(parts[1:])} x {parts[0]}", mochi_type.lower())
                # else:
                #     val = parse_entry(f"{entry} x 1", mochi_type.lower())

            if val is not None:
                total_value += target_val/val
            else:
                invalid_entries.append(entry)

        # if "x" in target_mochi:
        #     target_val = parse_entry(target_mochi, mochi_type.lower())
        # else:
        #     target_val = parse_entry(f"{target_mochi} x 1", mochi_type.lower())
        
        if invalid_entries:
            st.warning(f"Could not calculate: {', '.join(invalid_entries)} in {current_dict}")

        if total_value and target_val:
            #equivalent_amount =  target_val / total_value 
            equivalent_amount = total_value
            st.success(f"""
                **Equivalent Value:** 
                {input_mochis} ≈ **{equivalent_amount:.2f} {target_mochi}({target_val})**
            """)

            with st.expander("📊 Breakdown"):
                st.write(f"Total value of your mochis: **{total_value:.4f}**")
                st.write(f"Value of 1 {target_mochi}: **{target_val:.4f}**")
                st.write(f"Calculation: {total_value:.4f} ÷ {target_val:.4f} = {equivalent_amount:.2f}")

def convert_to_flat_dict(input_dict):
    flat_dict = {}
    for score, names in input_dict.items():
        for name in names:
            flat_dict[name] = score
    return flat_dict
    
# Main app interface
mochi_type = st.radio("Select mochi type:", ["Common", "Latviaverse"])
current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA
current_data_flat = convert_to_flat_dict(current_data)

mode = st.radio("Choose mode:", ["Name ↔ Rarity Lookup", "Compare two mochis", "Value from Counts", "Value Converter", "Tag Search"])

if mode == "Name ↔ Rarity Lookup":
    st.subheader("🔍 Mochi Name ⇄ Rarity")
    lookup_input = st.text_input(f"Enter a mochi name or rarity number:", placeholder="e.g. neko england OR 5")

    if lookup_input:
        norm = normalize_name(lookup_input)

        if re.match(r"^\d+(\.\d+)?$", norm):
            rarity_num = float(norm)
            matched_mochis = [name.title() for r, names in current_data.items() if r == rarity_num for name in names]

            if matched_mochis:
                st.success(f"Mochis at rarity **{rarity_num}**: {', '.join(matched_mochis)}")
            else:
                st.warning(f"No mochis found at rarity {rarity_num} in {mochi_type} data.")
                closest = get_closest_rarity(rarity_num, current_data)
                st.info(f"Closest rarity is {closest}")

        else:
            rarity = get_rarity_by_name(norm, mochi_type.lower())
            if rarity is not None:
                st.success(f"**{lookup_input.title()}** has rarity: **{rarity}**")
            else:
                st.warning(f"No match found for '{lookup_input}' in {mochi_type} mochis.")
                suggestions = suggest_similar_mochis(norm, current_data)
                if suggestions:
                    st.info(f"Did you mean: {', '.join(suggestions)}?")

elif mode == "Compare two mochis":
    col1, col2 = st.columns(2)
    with col1:
        have = st.text_input("Your mochi:", placeholder=f"e.g., 'ukraine x 20' ({mochi_type} only)")
    with col2:
        want = st.text_input("Their mochi:", placeholder=f"e.g., 'russia x 3' ({mochi_type} only)")

    if have and want:
        val_have = parse_entry(have, mochi_type.lower())
        val_want = parse_entry(want, mochi_type.lower())

        if val_have is None:
            suggestions = suggest_similar_mochis(have.split('x')[0].strip(), current_data)
            if suggestions:
                st.warning(f"Couldn't find '{have}'. Did you mean: {', '.join(suggestions)}?")
        
        if val_want is None:
            suggestions = suggest_similar_mochis(want.split('x')[0].strip(), current_data)
            if suggestions:
                st.warning(f"Couldn't find '{want}'. Did you mean: {', '.join(suggestions)}?")

        if val_have is not None and val_want is not None and val_have != 0:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need {1/ratio:.2f}× of theirs for a fair trade")
            else:
                st.success(f"You need {ratio:.2f}× of yours for a fair trade")

elif mode == "Value from Counts":
    input_text = st.text_area(f"Enter {mochi_type} mochis (one per line or comma-separated), mochi/rarity x amount:",
                             help=f"Format: 'mochi x amount' or 'rarity x amount'\nExample: 'ukraine x20' ({mochi_type} only)")

    if input_text:
        entries = []
        for line in input_text.split("\n"):
            entries.extend([x.strip() for x in line.split(",") if x.strip()])

        total_value = 0
        invalid_entries = []

        for entry in entries:
            val = parse_entry(entry, mochi_type.lower())
            if val is not None:
                total_value += val
            else:
                invalid_entries.append(entry)

        if invalid_entries:
            st.warning(f"Could not parse: {', '.join(invalid_entries)}")
            for entry in invalid_entries:
                suggestions = suggest_similar_mochis(entry.split('x')[0].strip(), current_data)
                if suggestions:
                    st.info(f"Suggestions for '{entry}': {', '.join(suggestions)}")

        if total_value > 0:
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)

            st.success(f"Total value: {total_value:.2f} (1 mochi of rarity ~{exact_rarity:.2f})")
            st.markdown(f"Rounded to: {rounded_rarity}")

            suggestions = [name.title() for r, names in current_data.items()
                           if r == rounded_rarity for name in names]
            if not suggestions:
                closest = get_closest_rarity(rounded_rarity, current_data)
                suggestions = [name.title() for r, names in current_data.items()
                               if r == closest for name in names]

            if suggestions:
                st.markdown(f"Suggested {mochi_type} mochis: {', '.join(suggestions)}")

elif mode == "Value Converter":
    mochi_value_converter(current_data_flat)

elif mode == "Tag Search":
    tag_based_search()
    
st.markdown("---")
st.markdown("Disclaimer: Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")
st.markdown("If you noticed any bug ping howo.chernenko on discord")
st.markdown("Also some mochi worth more due to demand for example russia/neko england.etc")
