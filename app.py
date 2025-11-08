import streamlit as st
import re
import difflib
from datetime import datetime
import json
import os

def show_owner_messages():
    """Show popup messages from the owner when the app starts"""
    
    # Initialize session state for messages
    if 'message_index' not in st.session_state:
        st.session_state.message_index = 0
    if 'show_messages' not in st.session_state:
        st.session_state.show_messages = True
    
    # Messages from the owner
    OWNER_MESSAGES = [
        "🌟 Hai Welcome to Mochis Trade Calculator!",
        "This calculator helps you calculate fair trades between different mochis.",
        "Remember about demand and stuff, some mochis like russia/Japan are worth more due to popularity BUT I DON'T CHANGE THE RARITY BASED ON DEMAND plz stop spreadng misinformation ty......don't get scammed",
        "Found a bug? Use the comments section or tell me on discord",
        "Make sure to scroll down and check the disclaimer and tutorial part.....it's important oaky?",
        "u can also suggest new features and stuff okay??okay???...plz leave some comment if u like this calculator i need motive",
        "bro i'm lowkey crashing out ugh if u have any problem with this calculator tell me in comment section or just tell in on discord plz don't hate me...",
        "🎉 ok that's all ty -Howo (me the awesome owner of this site)"
    ]
    
    if st.session_state.show_messages and st.session_state.message_index < len(OWNER_MESSAGES):
        # Create a popup-like container
        with st.container():
            st.markdown("""
                <style>
                .owner-message {
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid #ff4b4b;
                    margin: 10px 0px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .owner-header {
                    color: #ff4b4b;
                    font-weight: bold;
                    font-size: 1.2em;
                    margin-bottom: 10px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Message content
            st.markdown(f"""
                <div class="owner-message">
                    <div class="owner-header">💌 Message from Howo (me the awesome owner)</div>
                    {OWNER_MESSAGES[st.session_state.message_index]}
                </div>
            """, unsafe_allow_html=True)
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.session_state.message_index > 0:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state.message_index -= 1
                        st.rerun()
            
            with col2:
                if st.session_state.message_index < len(OWNER_MESSAGES) - 1:
                    if st.button("Next ➡️", use_container_width=True):
                        st.session_state.message_index += 1
                        st.rerun()
                else:
                    if st.button("🎉 Got it!", use_container_width=True):
                        st.session_state.show_messages = False
                        st.rerun()
            
            with col3:
                if st.button("❌ Close", use_container_width=True):
                    st.session_state.show_messages = False
                    st.rerun()
            
            # Progress indicator
            progress = (st.session_state.message_index + 1) / len(OWNER_MESSAGES)
            st.progress(progress)
            st.caption(f"Message {st.session_state.message_index + 1} of {len(OWNER_MESSAGES)}")

st.title("🌟 Mochis Trade Calculator")
show_owner_messages() 

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
    5: ["austria-hungary", "japan", "neko america", "americat", "Neko Spain"],
    5.5: ["2p italy"],
    6: ["neko germany", "germouser", "tony", "nyo france", "neko france"],
    6.5: ["2p germany"],
    7: ["nyo korea", "korea", "south korea", "neko italy", "itabby", "gino", "sealand", "Neko China"],
    7.2: ["domain and realms of the shadows and the darkness", "drsd"],
    8: [ "neko romano", "romacat", "nyo spain", "nyo russia", "Neko Canada"],
    8.24: ["portugal"],
    9: ["uncensored china", "poland","russia", "prussia"],
    10: ["italy", "north italy", "germany", "nyo canada", "spain"],
    11: ["france", "romano", "south italy", "nyo poland", "nyo america"],
    12: ["wales", "germania", "germanic tribes", "canada", "nyo prussia"],
    13: ["nyo lithuania", "china", "nyo england"],
    14: ["neko austria", "ancient egypt", "mama egypt", "kemet", "czechoslovakia", "waiter"],
    15: ["sweden", "nyo belarus", "nyo germany"],
    16: ["quebec"],
    17: ["nyo italy", "serbia"],
    18: ["nyo finland"],
    19: ["neko hungary", "pictonian", "south africa"],
    20: ["nyo portugal", "nyo turkey", "seychelles' mystery friend", "seychelles friend", "mystery friend", "nyo sweden"],
    24: ["nyo hong kong"],
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

UPDATE_HISTORY = [
    {"date": "2025-10-31", "changes": "fixed comment section, added some message thingy that appear when you open the calculator"},
    {"date": "2025-10-10", "changes": "Added Neko Spain, Neko China, Neko Canada. Fixed some mochi placements."},
    {"date": "2025-01-10", "changes": "Added Value Converter feature and improved parsing for both '3 russia' and 'russia x3' formats"},
]


mochi_type = "Common" 
current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA

def convert_to_flat_dict(input_dict):
    flat_dict = {}
    for score, names in input_dict.items():
        for name in names:
            flat_dict[normalize_name(name)] = score
    return flat_dict

current_data_flat = convert_to_flat_dict(current_data)

COMMENTS_FILE = "mochi_comments.json"
MODERATOR_PASSWORD = "ukrowocanon"  
def load_comments():
    """Load comments from JSON file"""
    try:
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.sidebar.error(f"Error loading comments: {e}")
    return []

def save_comments(comments):
    """Save comments to JSON file"""
    try:
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.sidebar.error(f"Error saving comments: {e}")
        return False

def comments_section():
    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Comments & Feedback")
    
    # Load comments from file
    comments = load_comments()
    
    # Comment input form
    with st.sidebar.form("comment_form", clear_on_submit=True):
        name = st.text_input("Your name:", placeholder="Anonymous")
        comment = st.text_area("Your comment:", placeholder="Share your thoughts, bug reports, or suggestions...", height=100)
        submitted = st.form_submit_button("💬 Post Comment")
        
        if submitted:
            if comment.strip():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                comment_data = {
                    "name": name.strip() or "Anonymous",
                    "comment": comment.strip(),
                    "timestamp": timestamp
                }
                comments.append(comment_data)
                if save_comments(comments):
                    st.sidebar.success("✅ Comment posted successfully!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Failed to save comment")
            else:
                st.sidebar.warning("⚠️ Please write a comment before posting")
    
    # Display comments
    if comments:
        st.sidebar.markdown(f"### 📝 Recent Comments ({len(comments)} total)")
        
        # Show last 10 comments (newest first)
        recent_comments = list(reversed(comments[-10:]))
        
        for i, comment in enumerate(recent_comments):
            st.sidebar.markdown(f"**{comment['name']}** *({comment['timestamp']})*")
            st.sidebar.write(comment['comment'])
            
            # Add separator between comments (but not after the last one)
            if i < len(recent_comments) - 1:
                st.sidebar.markdown("---")
    else:
        st.sidebar.info("💡 No comments yet. Be the first to share your thoughts!")
    
    # Clear comments button with password protection
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔒 Moderator Tools")
    
    # Initialize session state for password
    if 'show_password_field' not in st.session_state:
        st.session_state.show_password_field = False
    
    if not st.session_state.show_password_field:
        if st.sidebar.button("🗑️ Clear All Comments"):
            st.session_state.show_password_field = True
            st.rerun()
    else:
        st.sidebar.warning("⚠️ This will permanently delete all comments!")
        password = st.sidebar.text_input("Enter moderator password:", type="password")
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("✅ Confirm Clear"):
                if password == MODERATOR_PASSWORD:
                    if save_comments([]):
                        st.session_state.show_password_field = False
                        st.sidebar.success("✅ All comments cleared!")
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Failed to clear comments")
                else:
                    st.sidebar.error("❌ Incorrect password")
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_password_field = False
                st.rerun()


def normalize_name(name: str) -> str:
    """Normalize input for matching: lower case, remove punctuation, replace dashes."""
    name = name.lower()
    name = re.sub(r"[.''–—]", "", name)
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
    """Parse a single entry like '3 russia' and return float value (amount / rarity)."""
    entry = entry.strip().lower()
    
    # Only handle format: "3 russia"
    if re.match(r"^\d+", entry):
        parts = re.split(r"\s+", entry, 1)
        if len(parts) == 2:
            try:
                amount = float(parts[0])
                name_part = parts[1]
                rarity = get_rarity_by_name(name_part, mochi_type)
                if rarity is None:
                    if re.match(r"^\d+(\.\d+)?$", name_part):
                        rarity = float(name_part)
                    else:
                        return None, None, None
                value = amount / rarity if rarity else None
                return value, amount, rarity
            except:
                return None, None, None
    
    # Handle single number or name without amount
    if re.match(r"^\d+(\.\d+)?$", entry):
        try:
            rarity = float(entry)
            return 1 / rarity, 1, rarity
        except:
            return None, None, None
    
    # Handle just mochi name (default amount = 1)
    rarity = get_rarity_by_name(entry, mochi_type)
    if rarity:
        return 1 / rarity, 1, rarity
    
    return None, None, None

def show_detailed_calculation(entries, target_mochi, target_rarity, mochi_type="common"):
    """Show detailed calculation breakdown"""
    st.subheader("🧮 Detailed Calculation")
    
    total_value = 0
    calculation_steps = []
    
    for entry in entries:
        val, amount, rarity = parse_entry(entry, mochi_type)
        if val is not None:
            total_value += val
            mochi_name = entry.split(' ', 1)[1] if ' ' in entry else entry
            calculation_steps.append(f"{amount} {mochi_name.title()}({rarity}) = {amount}/{rarity} = {val:.4f}")
    
    if calculation_steps:
        st.write("**Step 1: Calculate total value**")
        for step in calculation_steps:
            st.write(f"• {step}")
        
        st.write(f"**Total Value = {total_value:.4f}**")
        st.write("")
        
        st.write("**Step 2: Convert to target mochi**")
        st.write(f"Target: 1 {target_mochi.title()}({target_rarity}) = 1/{target_rarity} = {1/target_rarity:.4f}")
        st.write("")
        st.write(f"**Step 3: Final calculation**")
        st.write(f"{total_value:.4f} ÷ {1/target_rarity:.4f} = {total_value * target_rarity:.2f}")
        st.write("")
        st.success(f"**Result: {total_value * target_rarity:.2f} {target_mochi.title()}**")


def round_to_nearest_custom(n):
    """Rounds to nearest 0.1 if below 1, else nearest 0.5."""
    if n < 1:
        return round(n, 1)
    else:
        return round(n * 2) / 2

def get_closest_rarity(target, data):
    """Find closest rarity key to target in data dictionary."""
    return min(data.keys(), key=lambda r: abs(r - target))

def tag_based_search(data):
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
        
        for rarity, names in data.items():
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

def mochi_value_converter(current_data_flat):
    st.subheader("🔁 Mochi Value Converter")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        input_mochis = st.text_input(
            "Your mochis:", 
            placeholder="e.g. '4 ukraine, 3 belarus' or '5 russia'"
        )
    with col2:
        target_mochi = st.text_input(
            "Value in:", 
            placeholder="e.g. 'belarus'"
        )
    
    if input_mochis and target_mochi:
        # Get target mochi value
        target_norm = normalize_name(target_mochi)
        if target_norm not in current_data_flat:
            st.error(f"Target mochi '{target_mochi}' not found in database")
            return
        
        target_rarity = current_data_flat[target_norm]
        
        # Parse input mochis
        entries = [x.strip() for x in re.split(r'[,\n]', input_mochis) if x.strip()]
        total_value = 0
        invalid_entries = []
        
        for entry in entries:
            val, amount, rarity = parse_entry(entry, mochi_type.lower())
            if val is not None:
                total_value += val
            else:
                invalid_entries.append(entry)
        
        if invalid_entries:
            st.warning(f"Could not calculate: {', '.join(invalid_entries)}")
            for entry in invalid_entries:
                suggestions = suggest_similar_mochis(entry.split()[0] if ' ' in entry else entry, 
                                                    LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA)
                if suggestions:
                    st.info(f"Suggestions for '{entry}': {', '.join(suggestions)}")
        
        if total_value > 0:
            equivalent_amount = total_value * target_rarity
            
            st.success(f"""
                **Equivalent Value:** 
                {input_mochis} ≈ **{equivalent_amount:.2f} {target_mochi.title()}**
            """)

            # Show detailed calculation
            with st.expander("📊 Show Detailed Calculation"):
                show_detailed_calculation(entries, target_mochi, target_rarity, mochi_type.lower())

def compare_two_mochis_detailed(have_entry, want_entry, mochi_type="common"):
    """Show detailed comparison between two mochis"""
    val_have, amount_have, rarity_have = parse_entry(have_entry, mochi_type)
    val_want, amount_want, rarity_want = parse_entry(want_entry, mochi_type)
    
    if val_have is not None and val_want is not None and val_have != 0:
        ratio = val_want / val_have
        
        st.subheader("🧮 Detailed Comparison")
        st.write("**Step 1: Calculate values**")
        
        have_name = have_entry.split(' ', 1)[1] if ' ' in have_entry else have_entry
        want_name = want_entry.split(' ', 1)[1] if ' ' in want_entry else want_entry
        
        st.write(f"Your {have_entry}: {amount_have}/{rarity_have} = {val_have:.4f}")
        st.write(f"Their {want_entry}: {amount_want}/{rarity_want} = {val_want:.4f}")
        st.write("")
        
        st.write("**Step 2: Calculate ratio**")
        st.write(f"{val_want:.4f} ÷ {val_have:.4f} = {ratio:.4f}")
        st.write("")
        
        st.write("**Step 3: Fair trade calculation**")
        if ratio < 1:
            needed = 1/ratio
            st.write(f"Since {ratio:.4f} < 1, they need more of theirs:")
            st.write(f"1 ÷ {ratio:.4f} = {needed:.2f}×")
            st.success(f"**They need {needed:.2f}× of their {want_name.title()} for a fair trade**")
        else:
            st.write(f"Since {ratio:.4f} ≥ 1, you need more of yours:")
            st.success(f"**You need {ratio:.2f}× of your {have_name.title()} for a fair trade**")

mochi_type = st.radio("Select mochi type:", ["Common", "Latviaverse"])
current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA
current_data_flat = convert_to_flat_dict(current_data)

# Sidebar features
show_update_history()
comments_section()

mode = st.radio("Choose mode:", ["Name ↔ Rarity Lookup", "Compare two mochis", "Value from Counts", "Value Converter", "Tag Search"])

# Update the Compare two mochis section
if mode == "Compare two mochis":
    col1, col2 = st.columns(2)
    with col1:
        have = st.text_input("Your mochi:", placeholder="e.g. '3 russia'")
    with col2:
        want = st.text_input("Their mochi:", placeholder="e.g. '5 ukraine'")

    if have and want:
        val_have, amount_have, rarity_have = parse_entry(have, mochi_type.lower())
        val_want, amount_want, rarity_want = parse_entry(want, mochi_type.lower())

        if val_have is None:
            name_part = have.split(' ', 1)[1] if ' ' in have else have
            suggestions = suggest_similar_mochis(name_part, current_data)
            if suggestions:
                st.warning(f"Couldn't find '{have}'. Did you mean: {', '.join(suggestions)}?")
        
        if val_want is None:
            name_part = want.split(' ', 1)[1] if ' ' in want else want
            suggestions = suggest_similar_mochis(name_part, current_data)
            if suggestions:
                st.warning(f"Couldn't find '{want}'. Did you mean: {', '.join(suggestions)}?")

        if val_have is not None and val_want is not None and val_have != 0:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need {1/ratio:.2f}× of theirs for a fair trade")
            else:
                st.success(f"You need {ratio:.2f}× of yours for a fair trade")
            
            # Show detailed comparison
            with st.expander("📊 Show Detailed Calculation"):
                compare_two_mochis_detailed(have, want, mochi_type.lower())

# Update the Value from Counts section to show detailed calculation
elif mode == "Value from Counts":
    input_text = st.text_area(f"Enter {mochi_type} mochis (one per line or comma-separated):",
                             help="Format: 'amount mochi'\nExample: '20 ukraine' or '3 russia, 5 ukraine'",
                             placeholder="e.g. '3 russia, 5 ukraine'")

    if input_text:
        entries = [x.strip() for x in re.split(r'[,\n]', input_text) if x.strip()]

        total_value = 0
        invalid_entries = []
        calculation_steps = []

        for entry in entries:
            val, amount, rarity = parse_entry(entry, mochi_type.lower())
            if val is not None:
                total_value += val
                mochi_name = entry.split(' ', 1)[1] if ' ' in entry else entry
                calculation_steps.append(f"{amount} {mochi_name.title()}({rarity}) = {amount}/{rarity} = {val:.4f}")
            else:
                invalid_entries.append(entry)

        if invalid_entries:
            st.warning(f"Could not parse: {', '.join(invalid_entries)}")
            for entry in invalid_entries:
                name_part = entry.split(' ', 1)[1] if ' ' in entry else entry
                suggestions = suggest_similar_mochis(name_part, current_data)
                if suggestions:
                    st.info(f"Suggestions for '{entry}': {', '.join(suggestions)}")

        if total_value > 0:
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)

            st.success(f"Total value: {total_value:.2f} (1 mochi of rarity ~{exact_rarity:.2f})")
            st.markdown(f"Rounded to: {rounded_rarity}")

            # Show detailed calculation
            with st.expander("📊 Show Detailed Calculation"):
                st.write("**Step-by-step calculation:**")
                for step in calculation_steps:
                    st.write(f"• {step}")
                st.write("")
                st.write(f"**Total Value = {total_value:.4f}**")
                st.write("")
                st.write(f"**Equivalent rarity:** 1 ÷ {total_value:.4f} = {exact_rarity:.4f}")
                st.write(f"**Rounded to nearest standard: {rounded_rarity}**")

            suggestions = [name.title() for r, names in current_data.items()
                           if r == rounded_rarity for name in names]
            if not suggestions:
                closest = get_closest_rarity(rounded_rarity, current_data)
                suggestions = [name.title() for r, names in current_data.items()
                               if r == closest for name in names]

            if suggestions:
                st.markdown(f"Suggested {mochi_type} mochis: {', '.join(suggestions)}")
                
            
            # Look up mochi value
            name_norm = normalize_name(name)
            if name_norm in current_data_flat:
                mochi_value = current_data_flat[name_norm]
                total_value += amount * (1 / mochi_value)  # Convert to base value
            else:
                invalid_entries.append(entry)
        
        if invalid_entries:
            st.warning(f"Could not calculate: {', '.join(invalid_entries)}")
            for entry in invalid_entries:
                suggestions = suggest_similar_mochis(entry.split('x')[0].strip() if 'x' in entry else entry.split()[0], 
                                                    LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA)
                if suggestions:
                    st.info(f"Suggestions for '{entry}': {', '.join(suggestions)}")
        
        if total_value > 0:
            # Calculate how many target mochis this is worth
            equivalent_amount = total_value * target_value  # Convert from base value to target
            st.success(f"""
                **Equivalent Value:** 
                {input_mochis} ≈ **{equivalent_amount:.2f} {target_mochi}**
            """)

            with st.expander("📊 Breakdown"):
                st.write(f"Total base value: {total_value:.4f}")
                st.write(f"Value of 1 {target_mochi}: {1/target_value:.4f}")
                st.write(f"Calculation: {total_value:.4f} × {target_value:.4f} = {equivalent_amount:.2f}")
                

def show_update_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Update History")
    for update in UPDATE_HISTORY:
        with st.sidebar.expander(f"📅 {update['date']}"):
            st.write(update['changes'])

    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔒 Moderator Tools")
    
    if 'moderator_authenticated' not in st.session_state:
        st.session_state.moderator_authenticated = False
    
    if not st.session_state.moderator_authenticated:
        with st.sidebar.form("moderator_login"):
            st.write("Moderator Login")
            password = st.text_input("Password:", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                if password == "ukrowocanon":  
                    st.session_state.moderator_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password!")
    else:
        st.sidebar.success("🔓 Moderator Mode Active")
        if st.sidebar.button("🗑️ Clear All Comments"):
            if save_comments([]):
                st.sidebar.success("✅ All comments cleared!")
                st.rerun()
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.moderator_authenticated = False
            st.rerun()



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
        have = st.text_input("Your mochi:", placeholder="e.g. '3 russia'")
    with col2:
        want = st.text_input("Their mochi:", placeholder="e.g. '5 ukraine'")

    if have and want:
        val_have, amount_have, rarity_have = parse_entry(have, mochi_type.lower())
        val_want, amount_want, rarity_want = parse_entry(want, mochi_type.lower())

        if val_have is None:
            name_part = have.split(' ', 1)[1] if ' ' in have else have
            suggestions = suggest_similar_mochis(name_part, current_data)
            if suggestions:
                st.warning(f"Couldn't find '{have}'. Did you mean: {', '.join(suggestions)}?")
        
        if val_want is None:
            name_part = want.split(' ', 1)[1] if ' ' in want else want
            suggestions = suggest_similar_mochis(name_part, current_data)
            if suggestions:
                st.warning(f"Couldn't find '{want}'. Did you mean: {', '.join(suggestions)}?")

        if val_have is not None and val_want is not None and val_have != 0:
            ratio = val_want / val_have
            if ratio < 1:
                st.success(f"They need {1/ratio:.2f}× of theirs for a fair trade")
            else:
                st.success(f"You need {ratio:.2f}× of yours for a fair trade")
            
            # Show detailed comparison
            with st.expander("📊 Show Detailed Calculation"):
                compare_two_mochis_detailed(have, want, mochi_type.lower())

elif mode == "Value from Counts":
    input_text = st.text_area(f"Enter {mochi_type} mochis (one per line or comma-separated):",
                             help="Format: 'amount mochi'\nExample: '20 ukraine' or '3 russia, 5 ukraine'",
                             placeholder="e.g. '3 russia, 5 ukraine'")

    if input_text:
        entries = [x.strip() for x in re.split(r'[,\n]', input_text) if x.strip()]

        total_value = 0
        invalid_entries = []
        calculation_steps = []

        for entry in entries:
            val, amount, rarity = parse_entry(entry, mochi_type.lower())
            if val is not None:
                total_value += val
                mochi_name = entry.split(' ', 1)[1] if ' ' in entry else entry
                calculation_steps.append(f"{amount} {mochi_name.title()}({rarity}) = {amount}/{rarity} = {val:.4f}")
            else:
                invalid_entries.append(entry)

        if invalid_entries:
            st.warning(f"Could not parse: {', '.join(invalid_entries)}")
            for entry in invalid_entries:
                name_part = entry.split(' ', 1)[1] if ' ' in entry else entry
                suggestions = suggest_similar_mochis(name_part, current_data)
                if suggestions:
                    st.info(f"Suggestions for '{entry}': {', '.join(suggestions)}")

        if total_value > 0:
            exact_rarity = 1 / total_value
            rounded_rarity = round_to_nearest_custom(exact_rarity)

            st.success(f"Total value: {total_value:.2f} (1 mochi of rarity ~{exact_rarity:.2f})")
            st.markdown(f"Rounded to: {rounded_rarity}")

            # Show detailed calculation
            with st.expander("📊 Show Detailed Calculation"):
                st.write("**Step-by-step calculation:**")
                for step in calculation_steps:
                    st.write(f"• {step}")
                st.write("")
                st.write(f"**Total Value = {total_value:.4f}**")
                st.write("")
                st.write(f"**Equivalent rarity:** 1 ÷ {total_value:.4f} = {exact_rarity:.4f}")
                st.write(f"**Rounded to nearest standard: {rounded_rarity}**")

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
    tag_based_search(current_data)
    

st.markdown("---")
st.markdown("Disclaimer: Calculator could be outdated if I didn't notice any rarity change so don't use if you don't trust it :p")
st.markdown("If you noticed any bug ping howo.chernenko on discord")
st.markdown("Also some mochi worth more due to demand for example russia/neko england.etc I DIDN'T CHANGE ANY RARITY IN THE CALCULATOR U HAVE TO THINK ABOUT DEMAND URSELF WHEN TRADING SORRY")
st.markdown("---")
st.markdown("Tutorial:")
st.markdown("Name-Rarity look up is to check rarity or check mochis ") 
st.markdown("Compare two mochis is u compare two values, u put a value on both side e.g.: russia and  ukraine, and it will tell u the amount u need")
st.markdown("Value from counts is you type what you have and it will tell u what it worth")
st.markdown("Value converter is you put a bunch of stuff e.g. 2 ukraine, 4 prussia, and you put another mochi on the other side  for exampple belarus so you know how many belarus 2 ukraine and 4 prussia worth")
st.markdown("Tag search is is using tag to search a mochi")
