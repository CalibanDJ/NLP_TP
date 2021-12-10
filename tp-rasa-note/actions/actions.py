# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# API : https://www.coinlore.com/cryptocurrency-data-api

# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

import requests as requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset


class InteracteWithUserHello(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]


class ActionGetIdCrypto(Action):

    def name(self) -> Text:
        return "action_crypto_get_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        r = requests.get("https://api.coinlore.net/api/tickers/")
        crypto_list = r.json()["data"]
        id = -1
        crypto = str(tracker.get_slot("crypto")).lower()
        for i in range(100):
            if (str(crypto_list[i]["symbol"]).lower() == crypto or \
                    str(crypto_list[i]["name"]).lower() == crypto):
                id = int(crypto_list[i]["id"])
                break
        if id == -1:
            dispatcher.utter_message(
                text="I did not find any coin named \"" + crypto + "\" in the Top 100 cryptocurrency."
                                                                   "\n Please retry !")
            return [AllSlotsReset()]
        else:
            dispatcher.utter_message(text="What do you want to know about it ? [Price/Rank/Change]")
            return [SlotSet("id", id)]


class ActionGetPriceCrypto(Action):

    def name(self) -> Text:
        return "action_crypto_price_usd"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        crypto_id = str(tracker.get_slot("id")).lower()
        crypto = str(tracker.get_slot("crypto")).lower()
        r = requests.get("https://api.coinlore.net/api/ticker/?id=" + crypto_id)
        price = crypto + " price is : " + str(r.json()[0]["price_usd"]) + " USD$."
        dispatcher.utter_message(text=price)
        return []


class ActionGetRankCrypto(Action):

    def name(self) -> Text:
        return "action_crypto_rank"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        crypto_id = str(tracker.get_slot("id")).lower()
        crypto = str(tracker.get_slot("crypto")).lower()
        r = requests.get("https://api.coinlore.net/api/ticker/?id=" + crypto_id)
        rank = crypto + " rank is : " + str(r.json()[0]["rank"]) + "."
        dispatcher.utter_message(text=rank)
        return []


class ActionGetChangeCrypto(Action):

    def name(self) -> Text:
        return "action_crypto_change"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        crypto = str(tracker.get_slot("crypto")).lower()
        dispatcher.utter_message(text="Which change do you want to now about " + crypto + " ? [1hour/24hours/7days]")
        return []


class ActionGetChange2Crypto(Action):

    def name(self) -> Text:
        return "action_crypto_change_with_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        crypto_id = str(tracker.get_slot("id")).lower()
        crypto = str(tracker.get_slot("crypto")).lower()
        crypto_change_asked = str(tracker.get_slot("change")).lower()
        changes_type = ["percent_change_24h", "percent_change_1h", "percent_change_7d"]
        changes_type_string = ["24hours", "1hour", "7days"]
        if (crypto_change_asked == "1" or crypto_change_asked == "one"):
            change_selected = 1
        elif (
                crypto_change_asked == "24" or crypto_change_asked == "twenty-four" or crypto_change_asked == "twenty four"):
            change_selected = 0
        elif (crypto_change_asked == "7" or crypto_change_asked == "seven"):
            change_selected = 2
        r = requests.get("https://api.coinlore.net/api/ticker/?id=" + crypto_id)
        change = crypto + " change in the last " + changes_type_string[change_selected] + " is : " + str(
            r.json()[0][changes_type[change_selected]]) + "."
        dispatcher.utter_message(text=change)
        return []
