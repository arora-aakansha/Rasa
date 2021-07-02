from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import petl as etl
from rasa_sdk.types import DomainDict

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

class ActionAddNominee(Action):

    def name(self) -> Text:
        return "action_add_nominee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        n=[]
        name_list=tracker.get_slot('name_list')
        print("slot")
        print(tracker.get_slot('name_list'))
        print(name_list)
        for i in name_list:
            n.append(i)
        dispatcher.utter_message(text="are added to list")
        print("new list")
        print(n)

        return []

class ValidateName(FormValidationAction):

    def name(self) -> Text:
        return "validate_Nomination_name_form"
    
    def validate_name_list(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name_list array"""
        name_list=[]
        print(slot_value)

        connection=sqlite3.connect('rasa.db')
        table= etl.fromdb(connection, 'select * from demo')
        flag=0
        if len(slot_value)==0:
            dispatcher.utter_message(text="No name mentioned")
            return{'name_list':None}
    
        for i in slot_value:
            print(slot_value)
            check=Repo.check(i)
            print("check value")
            print(check)
            if check==True:
                dispatcher.utter_message(text="does not belong to database")
                return{"name_list":None}
                
        return{"name_list":slot_value}
                

              
    


    

