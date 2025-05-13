import streamlit as st
import re

st.title("🌟 Mochis Trade Calculator")

MOCHI_DATA = {
    0.1: ["god", "fairy king of the mochi", "fairy king", "fkm"],
    0.5: ["soviet union", "ussr"],
    0.6: ["allied powers", "allies", "allie"],
    0.7: ["bad friends trio", "bad friend trio", "bad friends trios", "bft"],
    0.8: ["axis powers", "axis"],
    0.9: ["franco-british union","fbu"],
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
    for rarity, names in MOCHI_DATA.items():
        if name in [normalize_name(n) for n in names]:
            return rarity
    return None

mode = st.radio("Choose mode:", ["Compare two mochis", "Trade multiple mochis", "Event Mochi Section", "Value from Counts"])

if mode == "Compare two mochis":
    name_or_rarity_have = st.text_input("Your mochi (name or rarity):")
    name_or_rarity_want = st.text_input("Their mochi (name or rarity):")

    def parse_input(val):
        try:
            return float(val)
        except:
            return get_rarity_by_name(val)

    rarity_have = parse_input(name_or_rarity_have)
    rarity_want = parse_input(name_or_rarity_want)

    if rarity_have and rarity_want:
        ratio = rarity_want / rarity_have
        if ratio < 1:
            st.success(f"You need **{1/ratio:.2f}** mochis for a fair trade.")
        else:
            st.success(f"They need **{ratio:.2f}** mochis for a fair trade.")
    else:
        if name_or_rarity_have or name_or_rarity_want:
            st.warning("Could not identify mochi name or rarity. Please double-check spelling.")

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
                    rarity = get_rarity_by_name(e)
                    if rarity and rarity > 0:
                        rarities.append(rarity)

            if rarities:
                total_value = sum(1 / r for r in rarities)
                exact_result = 1 / total_value
                rounded_result = math.ceil(exact_result * 100) / 100  # Round up to nearest 0.01

                # Suggest closest mochis
                exact_suggestion = min(
                    mochi_rarities.items(), key=lambda x: abs(x[1] - exact_result)
                )
                rounded_suggestion = min(
                    mochi_rarities.items(), key=lambda x: abs(x[1] - rounded_result)
                )

                formatted_entries = ", ".join([e.title() for e in entries])

                st.success(
                    f"**Your mochis**: {formatted_entries}\n\n"
                    f"- **Exact trade value**: `{exact_result:.2f}` → Suggested mochi: **{exact_suggestion[0].title()}** (rarity {exact_suggestion[1]})\n"
                    f"- **Rounded-up value**: `{rounded_result:.2f}` → Suggested mochi: **{rounded_suggestion[0].title()}** (rarity {rounded_suggestion[1]})"
                )
            else:
                st.warning("No valid rarities or mochi names were recognized.")
        except Exception as e:
            st.error(f"Error: {e}\n\nPlease enter valid mochi names or rarity numbers.")


elif mode == "Event Mochi Section":
    mochi_input = st.text_input("Enter your event mochi's name or rarity:")

    if mochi_input:
        rarity = get_rarity_by_name(mochi_input)
        try:
            if rarity is None:
                rarity = float(mochi_input)
            adjusted = rarity / 2
            st.success(f"An event mochi with base rarity {rarity} is worth the equivalent of **~{adjusted:.2f}**.")
        except:
            st.error("Could not process the input. Please enter a number or known mochi name.")


elif mode == "Value from Counts":
    input_text = st.text_area("Enter your mochis as 'rarityOrName x amount', comma-separated (e.g. japan x 20, 5 x 5):")

    if input_text:
        try:
            items = input_text.split(",")
            total_value = 0
            invalids = []
            for item in items:
                item = item.strip().lower()
                if "x" in item:
                    part, amount_str = map(str.strip, item.split("x", 1))
                    try:
                        rarity = float(part)
                    except ValueError:
                        rarity = get_rarity_by_name(part)
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        amount = None
                    if rarity and amount:
                        total_value += amount / rarity
                    else:
                        invalids.append(item)
            if total_value > 0:
                result = 1 / total_value
                st.success(f"These mochis can be traded for one mochi of rarity **~{result:.2f}**.")
                if invalids:
                    st.warning(f"Some items couldn't be processed: {', '.join(invalids)}")
            else:
                st.warning("No valid values found.")
        except:
            st.error("Invalid format. Please use 'mochi x amount' like 'japan x 20, 5 x 5'.")


# Footer
st.markdown("---")
st.markdown("Calculator created by **Howo Chernenko**")
