#!/usr/bin/env python3
import re
from waapi import WaapiClient, CannotConnectToWaapiException

def create_random_container(name, parent, onNameConflict):

    object_create_args = {
        "name": name,
        "parent": parent,
        "type": "RandomSequenceContainer",
        "@RandomOrSequence": 1,
        "onNameConflict": onNameConflict,
    }

    return client.call("ak.wwise.core.object.create", object_create_args)["id"]


def move_object(object_id, parent_id):
    return client.call("ak.wwise.core.object.move", {"parent": parent_id, "object": object_id})

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        client.call("ak.wwise.core.undo.beginGroup")

        selected_object = client.call("ak.wwise.ui.getSelectedObjects", options={"return": ["id", "name", "parent"]})["objects"]

        for obj in selected_object:

            obj_name = obj["name"]
            obj_id = obj["id"]
            parent_id = obj["parent"]["id"]

            new_container_name = re.match(r'(.+)_\w+', obj_name).group(1)
            new_container_id = create_random_container(new_container_name, parent_id, "merge")
            
            move_object(obj_id, new_container_id)
            
        client.call("ak.wwise.core.undo.endGroup", {"displayName": "Create random containers for selected objects."})


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")