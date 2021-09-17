"""Processes most of the commands the bot receives to provide usable card information for the user"""
from discord import Embed


class BotFunctions:

    def __init__(self):
        self.final_message = []
        self.message = Embed()
        self.card_type = ""

    def get_card_type(self, card: 'json') -> bool:
        """Using the web json information determine what type or error the webpage contains regarding the card search"""
        if card["object"] == 'error':
            print("Card Error")
            self.message.add_field(name="__***Error:***__", value=card["details"], inline=False)
            self.card_type = card["object"]
            return False
        self.card_type = card["layout"]
        return True

    def get_card_image(self, card: 'json') -> None:
        """Using the card json information obtain the image(s) of the cards"""
        if self.card_type == "transform":
            self.message.set_image(url=card['card_faces'][0]["image_uris"]["png"])
            self.final_message.append(Embed().set_image(url=card['card_faces'][1]["image_uris"]["png"]))
        else:
            self.message.set_image(url=card["image_uris"]["png"])

    def create_card_description(self, card: 'json', counter) -> None:
        """Using the card json information, create the description for the searched card"""
        if counter < 1 and self.card_type == "normal":
            self.message.add_field(name="__***Description:***__", value=card["oracle_text"], inline=False)
        else:
            self.message.add_field(name=f"__***Description: {card['card_faces'][counter]['name']}"
                                        f"***__", value=card["card_faces"][counter]["oracle_text"], inline=False)

    def create_card_details(self, card: 'json') -> None:
        """Using the card json, create the embed title, url, set and links/pricing needed to display the card"""
        self.message.title = card["name"]
        self.message.url = card["scryfall_uri"]
        self.message.add_field(name="__***Link(TCG Player):***__", value=card["purchase_uris"]
        ["tcgplayer"], inline=False)
        self.message.add_field(name="__***Prices(TCG Player):***__",
                               value="Usd: ${}\n Usd (Foil): ${}".format(card["prices"]["usd"],
                                                                         card["prices"]["usd_foil"]),
                               inline=True)
        self.message.add_field(name="__***Set:***__", value=card["set_name"], inline=False)

    def create_search_embed(self, card: 'json') -> None:
        """Creates the message embed for discord and fills it using information from the card json provided"""
        self.message = Embed()
        self.get_card_type(card)
        self.final_message.append(self.message)

        if self.card_type != "error":
            self.create_card_details(card)
        else:
            return

        if self.card_type == "normal":
            self.create_card_description(card, 0)

        elif self.card_type == "split" or self.card_type == "transform":
            for face in range(len(card["card_faces"])):
                self.create_card_description(card, face)

        self.get_card_image(card)





