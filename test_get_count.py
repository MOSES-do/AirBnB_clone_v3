#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State


"""
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
first_state_id = list(storage.all(State).values())[0].id
print(f"test-file{first_state_id}")
print("First state: {}".format(storage.get(State, first_state_id)))"""


print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print(type(first_state_id))
print("First state: {}".format(storage.get(State, '07837f0f-50f9-473c-a0ef-8e17a3a64e59')))
print(type(State), type(first_state_id))

first_state_id = list(storage.all(State).values())[0].id
state = storage.get(State, first_state_id)
if state is None:
    print("None", end="")
else:
    print("Get shouldn't return an object if the ID doesn't exist", end="")




"""
def wrapper_all_type(m_class):
    res = {}
    try:
        res = storage.all(m_class)
    except:
        res = {}
    if res is None or len(res.keys()) == 0:
        try:
            res = storage.all(m_class.__name__)
        except:
            res = {}
    return res

state_ids = []
state_ids_found = []
for state in wrapper_all_type(State).values():
    state_ids.append(state.id)

if len(state_ids) == 0:
    print("empty", end="")
else:
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state is not None and state.id == state_id:
            state_ids_found.append(state_id)
            print(state_ids_found)
    if len(state_ids_found) != len(state_ids):
        # try with `<class_name>.<id>`
        state_ids = wrapper_all_type(State).keys()
        state_ids_found = []
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state is not None and state.id == state_id:
                state_ids_found.append(state_id)
    
    if len(state_ids_found) == len(state_ids):
        print("Get success", end="")
    else:
        print(state_ids_found, state_ids)
        print("Get doesn't retreive all State in storage", end="")
"""
