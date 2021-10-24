# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


import requests
import json
import re



API_TOKEN = "NORDIGEN_API_TOKEN"
CHAT_WEBSITE_URL = "https://localhost:4000"
countries = [
            {"code": "AT", "name": "AUSTRIA"},
            {"code": "BE", "name": "BELGIUM"},
            {"code": "BG", "name": "BULGARIA"},
            {"code": "HR", "name": "CROATIA"},
            {"code": "CY", "name": "CYPRUS"},
            {"code": "CZ", "name": "CZECH REPUBLIC"},
            {"code": "DK", "name": "DENMARK"},
            {"code": "EE", "name": "ESTONIA"},
            {"code": "FI", "name": "FINLAND"},
            {"code": "FR", "name": "FRANCE"},
            {"code": "DE", "name": "GERMANY"},
            {"code": "GR", "name": "GREECE"},
            {"code": "HU", "name": "HUNGARY"},
            {"code": "IS", "name": "ICELAND"},
            {"code": "IE", "name": "IRELAND"},
            {"code": "IT", "name": "ITALY"},
            {"code": "LV", "name": "LATVIA"},
            {"code": "LI", "name": "LIECHTENSTEIN"},
            {"code": "LT", "name": "LITHUANIA"},
            {"code": "LU", "name": "LUXEMBOURG"},
            {"code": "MT", "name": "MALTA"},
            {"code": "NL", "name": "NETHERLANDS"},
            {"code": "NO", "name": "NORWAY"},
            {"code": "PL", "name": "POLAND"},
            {"code": "PT", "name": "PORTUGAL"},
            {"code": "RO", "name": "ROMANIA"},
            {"code": "SK", "name": "SLOVAKIA"},
            {"code": "SI", "name": "SLOVENIA"},
            {"code": "ES", "name": "SPAIN"},
            {"code": "SE", "name": "SWEDEN"},
            {"code": "CH", "name": "SWITZERLAND"},
            {"code": "GB", "name": "UNITED KINGDOM"},
            {"code": "US", "name": "UNITED STATES"}
        ]



class ActionGetCountries(Action):
    def name(self):
        return "action_get_countries"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(text="You can connect to bank APIs in more than 30 countries:")
        description = "\n".join([country['name'] for country in countries])
        dispatcher.utter_message(text=f"{description}")

        return []


class ActionSelectCountry(Action):
    def name(self):
        return "action_select_country"

    def run(self, dispatcher, tracker, domain):

        message = tracker.latest_message['text']
        country_result = [country for country in countries if (re.search(country['code'], message, re.IGNORECASE) or re.search(country['name'], message, re.IGNORECASE))]

        if not country_result:
            dispatcher.utter_message(text="Country " + tracker.get_latest_entity_values("name") + " is currently not available.")
            return []

        return [SlotSet("country", country_result[0])]


class ActionGetAvailableBanks(Action):
    def name(self):
        return "action_get_available_banks"

    def run(self, dispatcher, tracker, domain):

        selected_country = tracker.get_slot("country")

        api_url = "https://ob.nordigen.com/api/aspsps/?country=" + selected_country['code']
        headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.get(api_url, headers=headers)
        available_banks = response.json()

        if not available_banks:
            dispatcher.utter_message(text="The are currently no available banks in " + selected_country['name'] + ".")
            return []

        dispatcher.utter_message(text="The available banks in " + selected_country['name'] + " are:")
        description = "\n".join([bank['name'] + " [" + bank['bic'] + "]" for bank in available_banks])
        dispatcher.utter_message(text=f"{description}")

        return []


class ActionSelectBank(Action):
    def name(self):
        return "action_select_bank"

    def run(self, dispatcher, tracker, domain):

        message = tracker.latest_message['text']

        chat_reference = "Chatbot"
        chat_user_id = tracker.sender_id
        selected_country = tracker.get_slot("country")

        api_url = "https://ob.nordigen.com/api/aspsps/?country=" + selected_country['code']
        headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.get(api_url, headers=headers)
        available_banks = response.json()

        bank_array = [bank for bank in available_banks if re.search(bank['name'], message, re.IGNORECASE)]

        if not bank_array:
            dispatcher.utter_message(text="Bank " + tracker.get_latest_entity_values("name") + " is currently not available.")
            return []

        bank_result = bank_array[0]

        dispatcher.utter_message(text="Bank -> " + bank_result['name'])

        login_text = "Do you want to connect to " + bank_result['name'] + " [BIC " + bank_result['bic'] + "] and get information about your accounts?"
        
        requisition_data = "{\"redirect\":\"%s\", \"reference\":\"%s\", \"enduser_id\":\"%s\", \"agreements\": [], \"user_language\": \"EN\"}" % (CHAT_WEBSITE_URL, chat_reference, chat_user_id)

        api_url = "https://ob.nordigen.com/api/requisitions/"
        headers =  {"Accept":"application/json", "Content-Type":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.post(api_url, data=json.dumps(requisition_data), headers=headers)
        requisition_result = response.json()
        
        link_data = "{\"aspsp_id\":\"%s\"}" % ("SANDBOXFINANCE_SFIN0000")
        
        api_url = "https://ob.nordigen.com/api/requisitions/" + requisition_result['id'] + "/links/"
        headers =  {"Accept":"application/json", "Content-Type":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.post(api_url, data=json.dumps(link_data), headers=headers)
        link_result = response.json()
        
        dispatcher.utter_message(text=login_text, buttons =[{"payload": login_result['initiate'], "title": "Open Bank Login Dialog"}])
        
        return [SlotSet("bank", bank_result)]


class ActionGetAccounts(Action):
    def name(self):
        return "action_get_accounts"

    def run(self, dispatcher, tracker, domain):

        bank = tracker.get_slot("bank")
        selected_country = tracker.get_slot("country")


        api_url = "https://ob.nordigen.com/api/requisitions/" + selected_country['code'] + "/"
        headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.get(api_url, headers=headers)
        accounts_result = response.json()   

        accounts = []
        description = "" 

        for account_id in accounts_result['accounts']:
            api_url = "https://ob.nordigen.com/api/accounts/" + account_id + "/details/"
            headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
            response = requests.get(api_url, headers=headers)
            account_result = response.json()
            accounts.append(account_result['account'])
            description += account_result['account']['iban'] + " " + account_result['name'] + "\n" 

        dispatcher.utter_message(text="Your accounts at " + bank['name'] + "are:")
        dispatcher.utter_message(text=f"{description}")

        accounts_slot_data = {}
        account_ids_slot_data = []
        for account in accounts:
            account_slot_data[account['id']] = account
            account_ids_slot_data.append(account['id'])

        return [SlotSet("accounts", accounts_slot_data)]


class ActionGetAccountBalance(Action):
    def name(self):
        return "action_get_account_balance"

    def run(self, dispatcher, tracker, domain):

        message = tracker.latest_message['text']
        accounts = tracker.get_slot("accounts")

        account_result = [account for account in accounts if (re.search(account['iban'], message, re.IGNORECASE) or re.search(account['name'], message, re.IGNORECASE))]

        if not account_result:
            dispatcher.utter_message(text="Account not found.")
            return []

        account = account_result[0]

        api_url = "https://ob.nordigen.com/api/accounts/" + account['id'] + "/balances/"
        headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.get(api_url, headers=headers)
        balances_result = response.json()

        description = [balance['balanceAmount']['amount'] + " " + balance['balanceAmount']['currency'] + "  [" + balance['referenceDate'] + "]\n" for balance in balances_result['balances']]


        dispatcher.utter_message(text="Your account balance for " + account['name'] + ":")
        dispatcher.utter_message(text=f"{description}")

        return []


class ActionGetAccountTransactions(Action):
    def name(self):
        return "action_get_account_transactions"

    def run(self, dispatcher, tracker, domain):

        message = tracker.latest_message['text']
        accounts = tracker.get_slot("accounts")

        account_result = [account for account in accounts if (re.search(account['iban'], message, re.IGNORECASE) or re.search(account['name'], message, re.IGNORECASE))]

        if not account_result:
            dispatcher.utter_message(text="Account not found.")
            return []

        account = account_result[0]

        api_url = "https://ob.nordigen.com/api/accounts/" + account['id'] + "/transactions/"
        headers =  {"Accept":"application/json", "Authorization":"Token " + API_TOKEN}
        response = requests.get(api_url, headers=headers)
        transactions_result = response.json()

        description = [transaction['valueDate'][:10] + " " + transaction['debtorName'] + "  " + transaction['transactionAmount']['amount'] + " " + transaction['transactionAmount']['currency'] + "\n" for transaction in transactions_result['transactions']['booked']]


        dispatcher.utter_message(text="Your account transactions for " + account['name'] + ":")
        dispatcher.utter_message(text=f"{description}")

        return []


class ActionHandoff(Action):
    def name(self):
        return "action_handoff"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(text="I've assigned the conversation to one of our customer service specialists. This might take a minute or two.")
        dispatcher.utter_message(text="CUSTOMER_SERVICE_HANDOFF")

        return []