import streamlit as st

st.title("🌟 Mochi Trade Calculator")

mode = st.radio("Choose mode:", ["Compare two mochis", "Trade multiple mochis", "Event Mochi Section"])

if mode == "Compare two mochis":
    rarity_have = st.number_input("Your mochi's rarity", min_value=1.0)
    rarity_want = st.number_input("Their mochi's rarity", min_value=1.0)

    if rarity_have and rarity_want:
        ratio = rarity_want / rarity_have
        if ratio < 1:
            st.success(f"You need **{1/ratio:.2f}** mochis for a fair trade..")
        else:
            st.success(f"They need **{ratio:.2f}** mochis for a fair trade.")

elif mode == "Trade multiple mochis":
    input_text = st.text_input("Enter your mochi rarities (e.g. 35, 20):")

    if input_text:
        try:
            rarities = [float(x.strip()) for x in input_text.split(",") if float(x.strip()) > 0]
            total_value = sum(1 / r for r in rarities)
            result = 1 / total_value
            st.success(f"With mochis {rarities}, you can trade for one of rarity **~{result:.2f}**")
        except:
            st.error("Please enter valid numbers only.")

elif mode == "Event Mochi Section":
    event_mochi_value = st.number_input("Enter the rarity of your event mochi", min_value=1.0)
    if event_mochi_value:
        adjusted_value = event_mochi_value / 2  # Event mochi rarity is doubled
        st.success(f"An event mochi with rarity {event_mochi_value} is worth the equivalent of a regular mochi with rarity ~{adjusted_value:.2f}.")
