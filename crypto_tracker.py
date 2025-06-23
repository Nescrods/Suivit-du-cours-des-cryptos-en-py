##
## PERSONNAL PROJECT, 2025
## Crypto_tracker
## File description:
## It's just a main ...
##

import streamlit as st
import pandas as pd
import call_api

usr_time_choises: dict[str, int] = {
    "1 day": 1,
    "3 day": 3,
    "1 week": 7,
    "2 weeks": 14,
    "1 month": 30,
    "3 month": 90,
    "6 month": 180,
    "1 year": 365,
}

st.title("💰 Crypto Tracker")
st.text("Voici un mini projet pour traquer des crypto")


@st.cache_data
def ask_api_for(
    usr_crypto: str | None,
    currencies: str | None,
    type_of_demand: tuple[str, int | None],
):
    list_of_possible_demand: list[str] = ["evolution", "price"]
    respond = call_api.make_url(usr_crypto, currencies, type_of_demand)

    if not respond or respond.status_code != 200:
        if not respond:
            return None
        st.warning(f"{respond.reason}\n(lol independant project 🤣)")
        st.stop()
        return None

    if type_of_demand[0] in list_of_possible_demand:
        return respond.json()
    return None


def worked_data(usr_crypto: str | None, usr_convert: str | None) -> None:
    if usr_crypto is None or usr_convert is None:
        return
    currencies: str = usr_convert

    crypto_price_data = ask_api_for(usr_crypto, currencies, ("price", None))
    crypto_evolution_data = True

    if not crypto_price_data or not crypto_evolution_data:
        st.warning("Something wrong")
        return

    data: dict = crypto_price_data

    print(data)
    usr_conversion_choise: float = st.number_input(
        label="Choisissez un nombre à convertir:",
        min_value=1,
    )
    st.metric(
        label=f"Prix de {usr_crypto} en {currencies}",
        value=f"{usr_conversion_choise} ({usr_crypto}) == {data[usr_crypto][currencies] * usr_conversion_choise} ({currencies})",
    )
    st.metric(
        label=f"{currencies} en {usr_crypto}",
        value=f"{usr_conversion_choise} ({currencies}) == {usr_conversion_choise / data[usr_crypto][currencies]} ({usr_crypto})",
    )
    usr_nbr_days_choise: str = st.selectbox(
        label="Choisissez un nombre à convertir:",
        options=usr_time_choises.keys(),
    )
    if st.button(
        label="Graph",
        icon="📈",
    ):
        crypto_evolution_data = ask_api_for(
            usr_crypto,
            currencies,
            ("evolution", usr_time_choises[usr_nbr_days_choise]),
        )
        if crypto_evolution_data:
            df = pd.DataFrame(crypto_evolution_data["prices"], columns=["days", "prices"])
            df["days"] = pd.to_datetime(df["days"], unit="ms")
        st.line_chart(df.set_index("days"))

usr_choises: tuple[str | None, str | None] = call_api.get_usr_choises()
worked_data(usr_choises[0], usr_choises[1])
