import streamlit as st

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

# Build alias-to-rarity dictionary
NAME_TO_RARITY = {}
for rarity, names in MOCHI_DATA.items():
    for name in names:
        NAME_TO_RARITY[name.lower()] = rarity

def normalize(name):
    return name.lower().replace("-", " ").replace("!", "").strip()

def get_rarity(name, is_event=False):
    name = normalize(name)
    rarity = NAME_TO_RARITY.get(name)
    if rarity is not None:
        return rarity * (2 if is_event else 1)
    return None

def value_from_count_input(count_input: str):
    total = 0
    for part in count_input.split(','):
        if 'x' in part:
            qty, val = part.lower().split('x')
            total += int(qty.strip()) * float(val.strip())
        else:
            total += float(part.strip())
    return total

def find_closest_mochis(target_rarity):
    closest_diff = float('inf')
    closest_rarity = None
    for rarity in MOCHI_DATA:
        diff = abs(rarity - target_rarity)
        if diff < closest_diff:
            closest_diff = diff
            closest_rarity = rarity
    return closest_rarity, MOCHI_DATA[closest_rarity]

# Streamlit UI
st.title("🌸 Mochi Rarity & Trade Calculator")

option = st.radio("Choose a feature:", [
    "Find rarity of a mochi",
    "Compare two mochis",
    "Compare two mochi groups",
    "Find total value from counts (e.g., 20x5, 3x2)",
])

if option == "Find rarity of a mochi":
    name = st.text_input("Enter mochi name:")
    is_event = st.checkbox("Is this an event mochi?", value=False)
    if name:
        rarity = get_rarity(name, is_event)
        if rarity is not None:
            st.success(f"'{name}' has a rarity of {rarity}")
        else:
            st.error("Mochi not found.")

elif option == "Compare two mochis":
    m1 = st.text_input("Mochi 1:")
    m2 = st.text_input("Mochi 2:")
    if m1 and m2:
        r1, r2 = get_rarity(m1), get_rarity(m2)
        if r1 is not None and r2 is not None:
            if r1 < r2:
                st.write(f"**{m1}** is rarer than **{m2}**")
            elif r1 > r2:
                st.write(f"**{m2}** is rarer than **{m1}**")
            else:
                st.write("They are equally rare.")
        else:
            st.error("One or both mochis not found.")

elif option == "Compare two mochi groups":
    g1 = st.text_area("Group 1 mochis (comma-separated):")
    g2 = st.text_area("Group 2 mochis (comma-separated):")
    if g1 and g2:
        group1 = g1.split(',')
        group2 = g2.split(',')
        total1 = sum(get_rarity(m.strip()) or 0 for m in group1)
        total2 = sum(get_rarity(m.strip()) or 0 for m in group2)
        st.write(f"Group 1 total rarity: {total1}")
        st.write(f"Group 2 total rarity: {total2}")
        if total1 < total2:
            st.success("Group 1 is rarer overall.")
        elif total1 > total2:
            st.success("Group 2 is rarer overall.")
        else:
            st.info("Both groups are equally rare.")

elif option == "Find total value from counts (e.g., 20x5, 3x2)":
    count_input = st.text_input("Enter counts (e.g., 20x5, 3x2):")
    if count_input:
        try:
            result = value_from_count_input(count_input)
            st.write(f"Total value: {result}")
            rounded = round(result * 2) / 2 if result >= 1 else round(result, 1)
            st.write(f"Rounded: {rounded}")
            matching = MOCHI_DATA.get(rounded)
            if matching:
                st.write(f"Mochis with rarity {rounded}: {', '.join(matching)}")
            else:
                closest_rarity, names = find_closest_mochis(rounded)
                st.write(f"No exact match. Closest rarity: {closest_rarity}")
                st.write(f"Mochis: {', '.join(names)}")
        except:
            st.error("Invalid input format.")
