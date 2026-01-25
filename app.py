import streamlit as st
import re
import difflib
from datetime import datetime
import json
import os
import random
import math



def mandatory_popup():
    """Simple mandatory popup that must be accepted"""
    
    if 'popup_accepted' not in st.session_state:
        st.session_state.popup_accepted = False
    
    if not st.session_state.popup_accepted:
        # Create a warning container
        with st.container():
            st.markdown("---")
            st.error("""
            ⚠️ **IMPORTANT DISCLAIMER - READ BEFORE USING**
            
            **This calculator uses BASE RARITY VALUES ONLY!**

            I HAVE TO SAY THIS AGAIN BUT I NEVER CHANGED VALUE BASED ON RARITY, think about the demand yourself to avoid getting scammed

            According to the owner of mochidex and other mods, this calculator is not recommended to use because rarity could be outdated, the calculation is inaccuate and I could change the rarity

            I admit that if there are rarity changes in mochidex that they didn't announce, I won't be able to realize it and update until someone point it out

            For the inaccuate part: I don't see anywhere in my calculator that have incorrect calculation, there is also the detailed calc button where you can see how it's calculated, if smth is wrong, dm/tell me and I'll change it. plz don't say that it's inaccuate without evidence cuz it's starting to piss me off a bit :p

            I will never change any rarity because there is no point of me doing that, cuz I wanna become friend with everyone and dishonesty will make people dislike me.

            ALSO you can dm me(howo.chernenko) at anytime if you have any question/concern or needs help with the calculator
            
            """)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✅ I Understand & Accept - Let me use the calculator", 
                           use_container_width=True,
                           type="primary"):
                    st.session_state.popup_accepted = True
                    st.rerun()
            
            st.markdown("---")
            st.stop() 



def show_owner_messages():
    """Show popup messages from the owner when the app starts"""
    
    # Initialize session state for messages
    if 'message_index' not in st.session_state:
        st.session_state.message_index = 0
    if 'show_messages' not in st.session_state:
        st.session_state.show_messages = True
    
    # Messages from the owner
    OWNER_MESSAGES = [
        "🌟 Hai Welcome to Mochis Trade Calculator! I just updated it so it shows detailed calculation",
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
mandatory_popup()  # Add this line
show_owner_messages()  # Your existing welcome messages

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
    13: ["nyo lithuania", "china", "nyo england", "serbia"],
    14: ["neko austria", "ancient egypt", "mama egypt", "kemet", "czechoslovakia", "waiter"],
    15: ["sweden", "nyo belarus", "nyo germany"],
    16: ["quebec"],
    17: ["nyo italy"],
    18: ["nyo finland"],
    19: ["neko hungary", "pictonian", "south africa"],
    20: ["nyo portugal", "nyo turkey", "seychelles' mystery friend", "seychelles friend", "mystery friend", "nyo sweden"],
    24: ["nyo hong kong"],
    25: ["benelux", "greenland", "nyo romano", "nyo china", "kitty-chan"],
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
    {"date": "2025-12-26", "changes": "Updated new rarity"},
    {"date": "2025-12-13", "changes": "Added disclaimer part"}, 
    {"date": "2025-11-18", "changes": "Added Kitty-Chan"}, 
    {"date": "2025-11-7", "changes": "Added detailed calculation function which shows how calculation works"}, 
    {"date": "2025-10-31", "changes": "fixed comment section, added some message thingy that appear when you open the calculator"},
    {"date": "2025-10-10", "changes": "Added Neko Spain, Neko China, Neko Canada. Fixed some mochi placements."},
    {"date": "2025-01-10", "changes": "Added Value Converter feature and improved parsing for both '3 russia' and 'russia x3' formats"},
]


mochi_type = "Common" 
current_data = LATVIAVERSE_DATA if mochi_type == "Latviaverse" else MOCHI_DATA

def normalize_name(name: str) -> str:
    """Normalize input for matching: lower case, remove punctuation, replace dashes."""
    name = name.lower()
    name = re.sub(r"[.'’–—]", "", name)
    name = name.replace("-", " ").replace("!", " ")
    return name.strip()


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


def shiny_2p_simulator():
    st.subheader("✨ Shiny & 2P Trade Simulator")
    
    st.markdown("""
    **Chance Rates:**
    - **Shiny:** 1 in 2,048 chance (×2048 multiplier)
    - **2P:** 1 in 1,000 chance (×1000 multiplier)
    
    **Correct Formula:**
    - Shiny Value = (Base Rarity × 2048) in terms of normal mochi value
    - To get equivalent in another mochi: (Base Rarity × 2048) ÷ Other Rarity
    """)
    
    # Step 1: Base mochi input
    st.markdown("### 🎯 Step 1: Base Mochi & Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        base_input = st.text_input(
            "Base Mochi (name or rarity):",
            placeholder="e.g. 'ukraine' or '90'",
            help="Enter mochi name or rarity number"
        )
    
    with col2:
        special_type = st.radio(
            "Special Type:",
            ["Shiny", "2P"],
            horizontal=True
        )
    
    # Calculate base rarity
    base_rarity = None
    base_name = None
    if base_input:
        if re.match(r"^\d+(\.\d+)?$", base_input):
            base_rarity = float(base_input)
            base_name = f"rarity {base_rarity}"
        else:
            base_rarity = get_rarity_by_name(base_input, mochi_type.lower())
            base_name = base_input
    
    # Step 2: Input mochis with max limits
    st.markdown("### 📝 Step 2: Bundle Mochis & Limits")
    
    st.write("Enter mochis you want in the bundle (one per line):")
    
    mochi_inputs = st.text_area(
        "Format: 'mochi_name [max_amount]'",
        placeholder="e.g.:\nromania\nukraine 50\nbelarus 100",
        help="Leave max amount blank for no limit"
    )
    
    # Parse mochi inputs with max limits
    mochi_items = []
    if mochi_inputs:
        lines = [line.strip() for line in mochi_inputs.split('\n') if line.strip()]
        for line in lines:
            parts = line.split()
            if len(parts) == 1:
                mochi_items.append({
                    'name': parts[0],
                    'max': None  # No limit
                })
            elif len(parts) == 2:
                try:
                    mochi_items.append({
                        'name': parts[0],
                        'max': int(parts[1])
                    })
                except:
                    mochi_items.append({
                        'name': line,
                        'max': None
                    })
            else:
                # Handle "mochi max" format
                try:
                    mochi_items.append({
                        'name': ' '.join(parts[:-1]),
                        'max': int(parts[-1])
                    })
                except:
                    mochi_items.append({
                        'name': line,
                        'max': None
                    })
    
    # Get rarities for all mochis
    mochi_data = []
    if mochi_items and base_rarity:
        for item in mochi_items:
            rarity = get_rarity_by_name(item['name'], mochi_type.lower())
            if rarity:
                mochi_data.append({
                    'name': item['name'],
                    'rarity': rarity,
                    'max': item['max']
                })
            else:
                st.warning(f"Could not find '{item['name']}'")
    
    # Calculate multiplier
    multiplier = 2048 if special_type == "Shiny" else 1000
    
    if st.button("🎯 Generate Optimized Bundles", type="primary") and base_rarity and mochi_data:
        st.markdown("### 📦 Step 3: Generated Bundles")
        
        # Calculate shiny/2P value in terms of normal mochis
        shiny_value = base_rarity * multiplier
        
        if base_name:
            st.success(f"**1 {special_type} {base_name.title()}**")
            st.info(f"Value in normal terms: **{shiny_value:,.1f}** (={base_rarity} × {multiplier})")
        
        # Generate multiple optimized bundles
        for bundle_num in range(3):  # Generate 3 different bundles
            with st.expander(f"📊 Bundle #{bundle_num + 1}", expanded=bundle_num == 0):
                remaining_value = shiny_value
                bundle = {}
                
                # Sort mochis by rarity (most common first for better distribution)
                sorted_mochis = sorted(mochi_data, key=lambda x: x['rarity'])
                
                # Try different strategies for each bundle
                if bundle_num == 0:
                    # Strategy 1: Use most common mochi first
                    available_mochis = sorted_mochis
                elif bundle_num == 1:
                    # Strategy 2: Use rarest mochi first
                    available_mochis = list(reversed(sorted_mochis))
                else:
                    # Strategy 3: Random order
                    available_mochis = mochi_data.copy()
                    random.shuffle(available_mochis)
                
                # Fill bundle with available mochis
                for mochi in available_mochis:
                    if remaining_value <= 0.01:
                        break
                    
                    # Calculate how many of this mochi equals 1 normal mochi value
                    # Since each mochi of rarity R is worth 1/R in normal terms
                    # We need: amount × (1/rarity) = remaining_value
                    # So: amount = remaining_value × rarity
                    
                    possible_amount = math.floor(remaining_value * mochi['rarity'])
                    
                    if possible_amount <= 0:
                        continue
                    
                    # Apply max limit if exists
                    if mochi['max'] is not None:
                        possible_amount = min(possible_amount, mochi['max'])
                    
                    if possible_amount <= 0:
                        continue
                    
                    # Determine actual amount (use significant portion)
                    if bundle_num == 0:
                        # Use most of possible amount
                        amount = possible_amount
                    elif bundle_num == 1:
                        # Use about half
                        amount = max(1, possible_amount // 2)
                    else:
                        # Random amount
                        amount = random.randint(1, possible_amount)
                    
                    # Calculate value contributed
                    value_contributed = amount / mochi['rarity']
                    
                    # Add to bundle
                    if mochi['name'] in bundle:
                        bundle[mochi['name']]['amount'] += amount
                        bundle[mochi['name']]['value'] += value_contributed
                    else:
                        bundle[mochi['name']] = {
                            'amount': amount,
                            'rarity': mochi['rarity'],
                            'value': value_contributed
                        }
                    
                    remaining_value -= value_contributed
                
                # Try to optimize remainder
                if abs(remaining_value) > 0.1:
                    # Try to adjust with the most common mochi
                    common_mochi = sorted_mochis[0]  # Most common (lowest rarity)
                    
                    # Calculate adjustment needed
                    adjustment_needed = remaining_value * common_mochi['rarity']
                    
                    if adjustment_needed > 0:
                        # Need to add more
                        current_amount = bundle.get(common_mochi['name'], {}).get('amount', 0)
                        max_allowed = common_mochi['max'] if common_mochi['max'] else float('inf')
                        can_add = max_allowed - current_amount
                        
                        to_add = min(math.ceil(adjustment_needed), can_add)
                        if to_add > 0:
                            if common_mochi['name'] in bundle:
                                bundle[common_mochi['name']]['amount'] += to_add
                                bundle[common_mochi['name']]['value'] += to_add / common_mochi['rarity']
                            else:
                                bundle[common_mochi['name']] = {
                                    'amount': to_add,
                                    'rarity': common_mochi['rarity'],
                                    'value': to_add / common_mochi['rarity']
                                }
                
                # Calculate final bundle value
                total_bundle_value = sum(item['value'] for item in bundle.values())
                
                # Display bundle
                bundle_items = []
                for name, data in sorted(bundle.items()):
                    bundle_items.append(f"**{int(data['amount'])} {name.title()}** (rarity {data['rarity']})")
                
                st.write("**Bundle Contents:**")
                for item in bundle_items:
                    st.write(f"- {item}")
                
                st.write("")
                st.write(f"**Total Bundle Value:** {total_bundle_value:.2f} normal mochis")
                st.write(f"**Target Value:** {shiny_value:.2f} normal mochis")
                st.write(f"**Difference:** {abs(total_bundle_value - shiny_value):.2f} "
                        f"({abs((total_bundle_value - shiny_value)/shiny_value*100):.1f}% off)")
                
                # Show calculation breakdown
                with st.expander("🧮 Show Calculation"):
                    st.write(f"**Base:** 1 {special_type} {base_name.title()} (rarity {base_rarity})")
                    st.write(f"**Multiplier:** {multiplier}×")
                    st.write(f"**Total value:** {base_rarity} × {multiplier} = {shiny_value:,.1f} normal mochis")
                    st.write("")
                    st.write("**Bundle Calculation:**")
                    for name, data in bundle.items():
                        st.write(f"- {data['amount']} × {name.title()} (1/{data['rarity']} each)")
                        st.write(f"  = {data['amount']} × {1/data['rarity']:.4f} = {data['value']:.2f}")
    
    # Quick Calculator for single mochi
    st.markdown("---")
    st.subheader("🧮 Quick Single Mochi Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calc_base = st.text_input("Special mochi:", placeholder="e.g. 'shiny ukraine'", key="calc_base")
    
    with col2:
        calc_target = st.text_input("Normal mochi:", placeholder="e.g. 'romania'", key="calc_target")
    
    if calc_base and calc_target:
        # Parse special mochi
        special_parts = calc_base.lower().split()
        if len(special_parts) >= 2:
            special_type_calc = special_parts[0]
            base_name_calc = ' '.join(special_parts[1:])
            
            base_rarity_calc = get_rarity_by_name(base_name_calc, mochi_type.lower())
            target_rarity = get_rarity_by_name(calc_target, mochi_type.lower())
            
            if base_rarity_calc and target_rarity:
                if special_type_calc == 'shiny':
                    mult = 2048
                elif special_type_calc == '2p' or special_type_calc == '2p':
                    mult = 1000
                else:
                    mult = 1
                
                # Calculate: (base × multiplier) ÷ target
                amount_needed = (base_rarity_calc * mult) / target_rarity
                
                st.success(f"**1 {special_type_calc.title()} {base_name_calc.title()}**")
                st.success(f"= **{amount_needed:,.0f} {calc_target.title()}**")
                st.write(f"Calculation: ({base_rarity_calc} × {mult}) ÷ {target_rarity} = {amount_needed:,.0f}")
    
    # Examples Section
    st.markdown("---")
    st.subheader("📚 Examples")
    
    examples = [
        ("Shiny Ukraine → Romania", 
         "1 Shiny Ukraine = 2048 Romania\n(Ukraine rarity 90, Romania rarity 90)\n90 × 2048 ÷ 90 = 2048"),
        
        ("Shiny 5 → Ukraine", 
         "1 Shiny 5 = 113.78 Ukraine\n(5 × 2048 ÷ 90 = 113.78)"),
        
        ("2P Russia → Belarus", 
         "1 2P Russia = 150 Belarus\n(Russia rarity 9, Belarus rarity 60)\n9 × 1000 ÷ 60 = 150"),
        
        ("Shiny 100 → 2P 10", 
         "1 Shiny 100 = 20.48 2P 10\n(100 × 2048) ÷ (10 × 1000) = 20.48")
    ]
    
    for title, calc in examples:
        with st.expander(title):
            st.code(calc)
        
    
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

def show_update_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Update History")
    for update in UPDATE_HISTORY:
        with st.sidebar.expander(f"📅 {update['date']}"):
            st.write(update['changes'])
            
# Sidebar features
show_update_history()
comments_section()

mode = st.radio("Choose mode:", ["Name ↔ Rarity Lookup", "Compare two mochis", "Value from Counts", "Value Converter", "Shiny/2P Simulator", "Tag Search"])
        
    
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

elif mode == "Shiny/2P Simulator":
    shiny_2p_simulator()

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
