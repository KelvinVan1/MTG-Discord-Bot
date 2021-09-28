"""Contains functions for all of the possible API calls needed"""
import requests
from thefuzz import fuzz


class ScryfallLogic:

    def __init__(self):
        self.SCRYFALL_API = "https://api.scryfall.com/"
        self.card_search = "cards/named"
        self.set_search = "sets"
        self.card = None
        self.set_names = {}

    def create_set_dictionary(self) -> None:
        """Using set data from scryfall's site create a dictionary with set codes as the keys and names as the values"""
        data = self.open_link(self.set_search, {})
        for magic_set in data["data"]:
            self.set_names[magic_set["code"].upper()] = magic_set["name"].upper()
        print("Creation of set dictionary has been completed")

    def fuzzy_search_sets(self, user_set: str) -> str:
        """Using a user inputted set name/code utilize fuzzy search in order to return the proper set code"""
        best_set_match = ""
        current_best_percentage = 0
        for key, value in self.set_names.items():
            if max(fuzz.ratio(user_set, value), fuzz.ratio(user_set, key)) > current_best_percentage:
                best_set_match = key
                current_best_percentage = max(fuzz.ratio(user_set, value), fuzz.ratio(user_set, key))

        return best_set_match

    def open_link(self, search_type: str, payload: dict) -> 'json':
        """Get a webpage's url by utilizing an API, searchtype, and payload in order to return a json of the contents"""
        data = requests.get(self.SCRYFALL_API + search_type, payload)
        print(data.url)
        return data.json()

    def quick_search_card(self, card_name: str) -> 'json':
        """Search for a card using the card_name and set self.card to a json containing the cards information"""
        payload = {'fuzzy': card_name}
        self.card = self.open_link(self.card_search, payload)

    def set_search_card(self, card_name: str, set_name: str) -> 'json':
        """Search for a card using card_name and set_name to set self.card to a json containing the cards information"""
        payload = {'fuzzy': card_name, 'set': set_name}
        self.card = self.open_link(self.card_search, payload)


