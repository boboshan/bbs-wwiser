#!/usr/bin/env python3
import re
from waapi import WaapiClient, CannotConnectToWaapiException

def create_folder(name, parent, onNameConflict):

    object_create_args = {
        "parent": parent,
        "type": "Folder",
        "name": name,
        "onNameConflict": onNameConflict,
    }

    return client.call("ak.wwise.core.object.create", object_create_args)["id"]


def create_event(name, parent, child, action):

    object_create_args = {
        "parent": parent,
        "type": "Event",
        "name": name,
            "children": [
                { 
                "name":"",
                "type": "Action", 
                "@ActionType": 1, 
                "@Target": child
                }
            ]
    }

    return client.call("ak.wwise.core.object.create", object_create_args)["id"]

def create_bank(name, parent, onNameConflict):

    object_create_args = {
        "parent": parent,
        "type": "SoundBank",
        "name": name,
        "onNameConflict": onNameConflict,
    }

    return client.call("ak.wwise.core.object.create", object_create_args)["id"]

def set_bank_inclusions(soundbank, inclusion):

    set_args = {
        "soundbank": soundbank,
        "operation": "add",
        "inclusions": [{ 
            "object": inclusion,
            "filter": [
                "events", 
                "structures"
            ]
        }]
    }

    return client.call('ak.wwise.core.soundbank.setInclusions', set_args)

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        client.call("ak.wwise.core.undo.beginGroup")

        selected_object = client.call("ak.wwise.ui.getSelectedObjects", options={"return": ["id", "name", "parent"]})["objects"]

        for obj in selected_object:

            obj_name = obj["name"]
            obj_id = obj["id"]
            parent_id = obj["parent"]["id"]

            new_folder_name = re.match(r'(.+)_(\w+_\w+)', obj_name).group(1)
            new_folder_id = create_folder(new_folder_name, "\\Events\\Default Work Unit", "merge")

            create_event(obj_name, new_folder_id, obj_id, 1)

            new_bank_id = create_bank(new_folder_name, "\\SoundBanks\\Default Work Unit", "merge")

            set_bank_inclusions(new_bank_id, new_folder_id)
            
        client.call("ak.wwise.core.undo.endGroup", {"displayName": "SFX Assembly"})


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")