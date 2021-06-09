import json

def add_user_access():
    u_dict = {"mex-dwh-u1": {"type": "password", "password": "uDswer.n!1fl"},
              "mex-dwh-u2": {"type": "password", "password": "password123"}
              }

    with open('user_details.json', 'w') as json_file:
        json.dump(u_dict, json_file)
