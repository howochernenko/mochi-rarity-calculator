import streamlit as st
import re

# -------- Dark Mode Toggle --------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("Toggle Dark Mode", on_click=toggle_dark_mode)

# Use basic theming by setting background/text colors accordingly
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #121212; color: #e0e0e0; }
        .stButton button { background-color: #333; color: #eee; }
        input, textarea { background-color: #222; color: #eee; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #fff; color: #000; }
        .stButton button { background-color: #f0f0f0; color: #000; }
        input, textarea { background-color: #fff; color: #000; }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("🌟 Mochis Trade Calculator")

# ---------------- Mochi Rarity Data ----------------
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
        normalized_aliases = [normalize_name(a) for a in aliases]
        if name in normalized_aliases:
            return rarity
    return None

def round_to_nearest_custom(n):
    if n < 1:
        return round(n, 1)
    else:
        return round(n * 2) / 2

def get_closest_rarity(target):
    return min(MOCHI_DATA.keys(), key=lambda r: abs(r - target))

def get_all_mochis_at_rarity(rarity):
    return [name.title() for r, names in MOCHI_DATA.items() if abs(r - rarity) < 1e-9 for name in names]

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

def copy_to_clipboard_js(text):
    """Return JS snippet to copy text to clipboard"""
    return f"""
    <script>
    navigator.clipboard.writeText(`{text}`).then(function() {{
        alert('Copied to clipboard: {text}');
    }}, function(err) {{
        alert('Failed to copy: ', err);
    }});
    </script>
    """

if mode == "Compare two mochis":
    have = st.text_input("Your mochi (name, rarity, or `mochi x amount`):")
    want = st.text_input("Their mochi (name, rarity, or `mochi x amount`):")

    if have and want:
        val_have = parse_entry(have)
        val_want = parse_entry(want)
        if val_have is None:
            st.error("Could not parse your mochi input.")
        elif val_want is None:
            st.error("Could not parse their mochi input.")
        else:
            ratio = val_have / val_want
            rounded = round_to_nearest_custom(ratio)
            mochis = get_all_mochis_at_rarity(rounded)
            if not mochis:
                closest = get_closest_rarity(rounded)
                mochis = get_all_mochis_at_rarity(closest)
            st.success(f"Trade value ratio: **{ratio:.2f}** (rounded to **{rounded}**)")

            st.markdown("Suggested mochis at that rarity: " + ", ".join(mochis))

            if st.button("Copy result to clipboard"):
                st.markdown(copy_to_clipboard_js(f"{ratio:.2f}"), unsafe_allow_html=True)

elif mode == "Trade multiple mochis":
    your_input = st.text_area("Your mochis (comma or newline separated, e.g. 'ukraine x 20, italy x 3'):")
    their_input = st.text_area("Their mochis (comma or newline separated):")

    def parse_multiple(text):
        total = 0.0
        entries = re.split(r"[,\\n]", text)
        for e in entries:
            if e.strip():
                val = parse_entry(e)
                if val is None:
                    st.warning(f"Could not parse entry: {e}")
                else:
                    total += val
        return total

    if your_input and their_input:
        val_yours = parse_multiple(your_input)
        val_theirs = parse_multiple(their_input)
        ratio = val_yours / val_theirs if val_theirs else None
        if ratio is None:
            st.error("Could not calculate ratio due to invalid input.")
        else:
            rounded = round_to_nearest_custom(ratio)
            mochis = get_all_mochis_at_rarity(rounded)
            if not mochis:
                closest = get_closest_rarity(rounded)
                mochis = get_all_mochis_at_rarity(closest)
            st.success(f"Trade value ratio: **{ratio:.2f}** (rounded to **{rounded}**)")

            st.markdown("Suggested mochis at that rarity: " + ", ".join(mochis))

            if st.button("Copy result to clipboard"):
                st.markdown(copy_to_clipboard_js(f"{ratio:.2f}"), unsafe_allow_html=True)

else:  # Value from Counts
    counts = st.text_input("Enter counts (e.g. '20x5, 3x2'):")

    def parse_counts(text):
        total = 0.0
        parts = re.split(r"[,\\n]", text)
        for part in parts:
            if "x" in part:
                amount_str, rarity_str = map(str.strip, part.split("x"))
                try:
                    amount = float(amount_str)
                    rarity = float(rarity_str)
                    total += amount / rarity
                except:
                    st.warning(f"Invalid count entry: {part}")
            else:
                st.warning(f"Count entry missing 'x': {part}")
        return total

    if counts:
        val = parse_counts(counts)
        rounded = round_to_nearest_custom(val)
        mochis = get_all_mochis_at_rarity(rounded)
        if not mochis:
            closest = get_closest_rarity(rounded)
            mochis = get_all_mochis_at_rarity(closest)
        st.success(f"Total value: **{val:.2f}** (rounded to **{rounded}**)")

        st.markdown("Suggested mochis at that rarity: " + ", ".join(mochis))

        if st.button("Copy result to clipboard"):
            st.markdown(copy_to_clipboard_js(f"{val:.2f}"), unsafe_allow_html=True)
