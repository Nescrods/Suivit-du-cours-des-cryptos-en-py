##
## PERSONNAL PROJECT, 2025
## Crypto_tracker
## File description:
## api_call
##

import streamlit as st
import requests

URL_API: str = "https://api.coingecko.com/api/v3/"

currencies_dict: dict[str, list[str]] = {}
coins_dict: dict[str, list[str]] = {}


@st.cache_data
def get_list_of_currencies() -> dict[str, list[str]]:
    url_of_currencies = f"{URL_API}simple/supported_vs_currencies"
    respond = requests.get(url=url_of_currencies)

    dict_of_currencies: dict[str, list[str]] = {"currencies": respond.json()}
    return dict_of_currencies


@st.cache_data
def get_list_of_coins() -> dict[str, list[str]]:
    url_to_list_of_coins = f"{URL_API}coins/list"
    respond = requests.get(url=url_to_list_of_coins)
    dict_of_coins = respond.json()

    rearenged_respond: dict[str, list[str]] = {
        coin["name"]: [coin["id"], coin["symbol"]] for coin in dict_of_coins
    }
    return rearenged_respond


currencies_dict = get_list_of_currencies()
coins_dict = get_list_of_coins()


def make_url(
    usr_crypto: str | None,
    usr_convert: str | None,
    type_of_demand: tuple[str, int | None],
):
    if not usr_crypto or not usr_convert:
        st.warning("Veuillez sélectionner une crypto et une devise.")
        st.stop()

    if type_of_demand[0] == "price":
        rep = requests.get(
            url=f"{URL_API}simple/price",
            params={
                "ids": usr_crypto,
                "vs_currencies": (
                    usr_convert
                    if usr_convert in currencies_dict["currencies"]
                    else "usd"
                ),
            },
        )
        return rep
    if type_of_demand[0] == "evolution" and type_of_demand[1]:
        # print("calling evolution")
        print(
            f"here the api: {URL_API}coins/{usr_crypto}/market_chart?vs_currency=usd&days=30&interval=daily"
        )
        rep = requests.get(
            url=f"{URL_API}coins/{usr_crypto}/market_chart",
            params={
                "vs_currency": (
                    usr_convert if usr_convert in currencies_dict else "usd"
                ),
                "days": type_of_demand[1],
                "interval": "daily",
            },
        )
        return rep
    return


if not coins_dict or not currencies_dict:
    st.error("Something wrong !")
    st.stop()


def get_usr_choises() -> tuple[str | None, str | None]:
    usr_coins_choise_from_key: str | None = st.selectbox(
        label="Choisissez vos crypto à comparer:",
        options=coins_dict.keys(),
        index=None,
        placeholder="Bitcoin",
    )

    if usr_coins_choise_from_key:
        usr_coins_choise: str | None = coins_dict[usr_coins_choise_from_key][0]
    else:
        usr_coins_choise = None
    usr_currencies_choise: str | None = st.selectbox(
        label="Choisissez votre monnaie vers laquelle sera converti la crypto:",
        options=currencies_dict["currencies"],
        index=None,
        placeholder="usd",
    )
    if not usr_coins_choise or not usr_currencies_choise:
        st.warning("Please choose a coin and a currencie")
        st.stop()
    return (usr_coins_choise, usr_currencies_choise)
