from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import petl as etl

from . import Repo

class ActionAskName(Action):

    def name(self) -> Text:
        return "action_ask_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_ask_name")

        return []


class ActionAskEmpCode(Action):

    def name(self) -> Text:
        return "action_ask_cid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_ask_cid")

        return []


class ActionAskEmail(Action):

    def name(self) -> Text:
        return "action_ask_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_ask_email")

        return []


class ActionSaveDetails(Action):

    def name(self) -> Text:
        return "action_save"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        print(tracker.get_slot('name'))
        Repo.insert(tracker.get_slot('name'), tracker.get_slot('cid'), tracker.get_slot('email'))

        dispatcher.utter_message(text="done")

        return []


class ActionSelectAll(Action):

    def name(self) -> Text:
        return "action_select"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        rows = Repo.select()

        dispatcher.utter_message(text=rows)

        return []


class ActionDeleteCandidate(Action):

    def name(self) -> Text:
        return "action_delete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #value = tracker.get_slot('cid')
        print(tracker.get_slot('cid'))
        Repo.delete(tracker.get_slot('cid'))

        dispatcher.utter_message(text="Deleted successfully")

        return []

class ActionShowData(Action):

    def name(self) -> Text:
        return "action_show_petl"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        connection=sqlite3.connect('rasa.db')
        table= etl.fromdb(connection, 'select * from demo')
        table=str(table)
        dispatcher.utter_message(text=table)

        return []

class ActionChangeName(Action):

    def name(self) -> Text:
        return "action_change_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        connection=sqlite3.connect('rasa.db')
        table= etl.fromdb(connection, 'select * from demo')
        table2=etl.rename(table, 'NAME', tracker.get_slot('change_name'))
        table2=str(table2)
        dispatcher.utter_message(text=table2)

        return []

class ActionRemoveCol(Action):

    def name(self) -> Text:
        return "action_remove_col"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        connection=sqlite3.connect('rasa.db')
        table= etl.fromdb(connection, 'select * from demo')
        table2=etl.cutout(table, 'EMPLOYEE_CODE')
        table2=str(table2)
        dispatcher.utter_message(text=table2)

        return []

class ValidateName(Action):

    def name(self) -> Text:
        return "validate_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.get_slot('name_list'))

        return []
    

