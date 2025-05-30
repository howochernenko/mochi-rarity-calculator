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

def get_rarity_by_name(name, mochi_type="common"):
    name = normalize_name(name)
    data = LATVIAVERSE_DATA if mochi_type == "latviaverse" else MOCHI_DATA
    for rarity, aliases in data.items():
        if name in [normalize_name(alias) for alias in aliases]:
            return rarity
    return None

def is_latviaverse(name):
    name = normalize_name(name)
    for aliases in LATVIAVERSE_DATA.values():
        if name in [normalize_name(alias) for alias in aliases]:
            return True
    return False

def round_to_nearest_custom(n):
    return round(n, 1) if n < 1 else round(n * 2) / 2

def get_closest_rarity(target, data):
    return min(data.keys(), key=lambda r: abs(r - target))

def parse_entry(entry, mochi_type):
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

mochi_type = st.radio("Select mochi type:", ["Common", "Latviaverse"])
current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA
mode = st.radio("Choose mode:", ["Compare two mochis", "Trade multiple mochis", "Value from Counts", "Value Converter"])

if mode == "Compare two mochis":
    col1, col2 = st.columns(2)
    with col1:
        have = st.text_input("Your mochi:", placeholder=f"e.g., 'ukraine x 20' ({mochi_type} only)")
    with col2:
        want = st.text_input("Their mochi:", placeholder=f"e.g., 'russia x 3' ({mochi_type} only)")

    if have and want:
        val_have = parse_entry(have, mochi_type.lower())
        val_want = parse_entry(want, mochi_type.lower())
        
        if val_have is not None and val_want is not None:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need {1/ratio:.2f}× of theirs for a fair trade")
            else:
                st.success(f"You need {ratio:.2f}× of yours for a fair trade")
        else:
            st.warning("Could not interpret entries. Check format and mochi type.")

elif mode == "Trade multiple mochis":
    input_text = st.text_input(f"Enter {mochi_type} mochis (comma separated):",
                             help=f"Example: 'ukraine x2, poland' ({mochi_type} only)")
    
    if input_text:
        entries = [x.strip() for x in input_text.split(",") if x.strip()]
        rarities = []
        
        for e in entries:
            val = parse_entry(e, mochi_type.lower())
            if val is not None:
                rarities.append(1/val)
            else:
                st.warning(f"Could not parse: {e}")
        
        if rarities:
            total_value = sum(1/r for r in rarities)
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)
            
            st.success(f"Total value: 1 mochi of rarity ~{exact_rarity:.2f}")
            st.markdown(f"Rounded to: {rounded_rarity}")
            
            suggestions = [name.title() for r, names in current_data.items() 
                         if r == rounded_rarity for name in names]
            if not suggestions:
                closest = get_closest_rarity(rounded_rarity, current_data)
                suggestions = [name.title() for r, names in current_data.items() 
                             if r == closest for name in names]
            
            if suggestions:
                st.markdown(f"Suggested {mochi_type} mochis: {', '.join(suggestions)}")

elif mode == "Value from Counts":
    input_text = st.text_area(f"Enter {mochi_type} mochis (one per line or comma-separated):",
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
    mochi_value_converter()

def mochi_value_converter():
    st.subheader("🔁 Mochi Value Converter")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    with col1:
        input_mochis = st.text_input(
            "Your mochis:", 
            placeholder="e.g. '5 russia, 1 ukraine' or 'russia x5, ukraine x1'"
        )
    with col2:
        target_mochi = st.text_input(
            "Value in:", 
            placeholder="e.g. 'belarus'"
        )
    
    if input_mochis and target_mochi:
        # Parse input mochis
        total_value = 0
        invalid_entries = []
        
        # Handle both comma and newline separation
        entries = []
        for line in input_mochis.split(","):
            entries.extend([x.strip() for x in line.split("\n") if x.strip()])
        
        for entry in entries:
            # Support both "5 russia" and "russia x5" formats
            if "x" in entry:
                val = parse_entry(entry, mochi_type.lower())
            else:
                # Handle "5 russia" format
                parts = entry.split()
                if len(parts) >= 2 and parts[0].isdigit():
                    val = parse_entry(f"{' '.join(parts[1:])} x {parts[0]}", mochi_type.lower())
                else:
                    val = None
            
            if val:
                total_value += val
            else:
                invalid_entries.append(entry)
        
        # Parse target mochi
        if "x" in target_mochi:
            target_val = parse_entry(target_mochi, mochi_type.lower())
        else:
            target_val = parse_entry(f"{target_mochi} x 1", mochi_type.lower())
        
        # Display results
        if invalid_entries:
            st.warning(f"Could not calculate: {', '.join(invalid_entries)}")
        
        if total_value and target_val:
            equivalent_amount = total_value / target_val
            st.success(f"""
                **Equivalent Value:**  
                {input_mochis} ≈ **{equivalent_amount:.2f} {target_mochi}**
            """)
            
            # Show breakdown
            with st.expander("📊 Breakdown"):
                st.write(f"Total value of your mochis: **{total_value:.4f}**")
                st.write(f"Value of 1 {target_mochi}: **{target_val:.4f}**")
                st.write(f"Calculation: {total_value:.4f} ÷ {target_val:.4f} = {equivalent_amount:.2f}")

st.markdown("---")
st.markdown("Disclaimer: Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")
st.markdown("If you noticed any bug ping howo.chernenko on discord, the current bug i noticed is that luxembourg and benelux does not work and i'm trying to fix it rn......")
st.markdown("Also some mochi worth more due to demand for example russia/neko england.etc")
