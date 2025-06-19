##
## PERSONNAL PROJECT, 2025
## Crypto_tracker
## File description:
## It's just a main ...
##

import streamlit as slt
import requests as rqt
import pandas as pd

URL_API: str = "https://api.coingecko.com/api/v3/"

slt.title("💰 Crypto Tracker")
slt.text("Voici un mini projet pour traquer des crypto")


currencies_list: list[str] = []
coins_dict = {}


@slt.cache_data
def get_list_of_currencies() -> list[str]:
    file_content = None

    try:
        file_content = pd.read_json("currencies.json")
        return file_content["currencies"].to_list()
    except FileNotFoundError:
        print(
            "File currencies.json not existing...\n" "Creating a json with currencies."
        )

    url_of_currencies = f"{URL_API}simple/supported_vs_currencies"
    respond = rqt.get(url=url_of_currencies)
    dict_of_currencies = {"currencies": respond.json()}
    file_to_export = pd.DataFrame(dict_of_currencies)

    pd.DataFrame.to_json(file_to_export, "currencies.json")
    return dict_of_currencies["currencies"]


@slt.cache_data
def get_list_of_coins() -> dict[str, str]:
    coins_dict: dict[str, str] = {}
    file_content = None

    try:
        print("Reading the json...")
        file_content = pd.read_json("crypto.json")
        len_of_df: int = len(file_content)

        for i in range(0, len_of_df):
            coins_dict[file_content["coins"][i]["id"]] = file_content["coins"][i][
                "name"
            ]
        return coins_dict
    except FileNotFoundError:
        print("File crypto.json not existing" "Creating a json with crypto")

    url_to_list_of_coins = f"{URL_API}coins/list"
    respond = rqt.get(url=url_to_list_of_coins)
    dict_of_coins = {"coins": respond.json()}
    file_to_export = pd.DataFrame(dict_of_coins)

    pd.DataFrame.to_json(file_to_export, "crypto.json")
    print(list(dict_of_coins.values()))
    return dict_of_coins


coins_dict = get_list_of_coins() if coins_dict == {} else coins_dict
currencies_list = get_list_of_currencies() if currencies_list == [] else currencies_list


if coins_dict == {} or currencies_list == []:
    slt.error("Something wrong !")
    slt.stop()


def get_usr_choises() -> tuple[str | None, str | None]:
    usr_coins_choise: str | None = slt.selectbox(
        label="Choisissez vos crypto à comparer:",
        options=list(coins_dict.values()),
        index=None,
    )
    usr_currencies_choise: str | None = slt.selectbox(
        label="Choisissez votre monnaie vers laquelle sera converti la crypto:",
        options=currencies_list,
        index=None,
        placeholder="usd"
    )
    return (usr_coins_choise, usr_currencies_choise)


def make_url(usr_crypto: str | None, usr_convert: str | None, type_of_demand: tuple[str, int | None]):
    if not usr_crypto or not usr_convert:
        slt.warning("Veuillez sélectionner une crypto et une devise.")
        slt.stop()

    if (type_of_demand[0] == "price"):
        rep = rqt.get(
            url=f"{URL_API}simple/price",
            params={
                "ids": usr_crypto,
                "vs_currencies": usr_convert if usr_convert in currencies_list else "usd",
            },
        )
        return rep
    if (type_of_demand[0] == "evolution"):
        print("calling evolution")
        rep = rqt.get(
            url=f"{URL_API}coins/{usr_crypto}/market_chart",
            params={
                "vs_currency": usr_convert if usr_convert in currencies_list else "usd",
                "days": type_of_demand[1],
                "interval": "daily",
            },
        )
        print("returning")
        return rep
    return


@slt.cache_data
def call_api(usr_crypto: str | None, currencies: str | None, type_of_demand: tuple[str, int | None]):
    respond = make_url(usr_crypto, currencies, type_of_demand)

    if not respond or respond.status_code != 200:
        slt.stop()
        slt.warning(
            "API is fully used, retry after a minute"
            "(lol this project is not professional just independant :) )"
        )
        return None
    if (type_of_demand[0] == "evolution"):
        print(respond)
        print(respond.json())
        prices = respond.json()["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "prices"])
        print(df)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        print(df)
        return df
    return respond.json()


def load_data(usr_crypto: str | None, usr_convert: str | None) -> None:
    if usr_crypto is None:
        return
    currencies: str = usr_convert if usr_convert is not None else "usd"
    if currencies not in currencies_list:
        currencies = "usd"
        slt.warning(f"changing currency to usd because of not finding: {usr_convert}")

    data = call_api(usr_crypto, currencies, ("price", None))
    if data is None:
        slt.warning("Something wrong")
        return
    coin = list(data.keys())[0]

    usr_conversion_choise: float = slt.number_input(
        label="Choisissez un nombre:",
        min_value=1,
    )

    slt.metric(
        label=f"Prix de {usr_crypto} en {currencies}",
        value=f"{usr_conversion_choise} ({usr_crypto}) == {data[coin][currencies] * usr_conversion_choise} ({currencies})",
    )

    slt.metric(
        label=f"{currencies} en {usr_crypto}",
        value=f"{usr_conversion_choise} ({currencies}) == {usr_conversion_choise / data[coin][currencies]} ({usr_crypto})",
    )

usr_choises: tuple[str | None, str | None] = get_usr_choises()
load_data(usr_choises[0], usr_choises[1])
