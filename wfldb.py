import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import ArrayUnion, ArrayRemove

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_playerid(user,player_id):
    db.collection("users").document(str(user)).set({'player_id':str(player_id)}, merge=True)

def get_playerid(user):
    db.collection("users").document(str(user)).set({'logic':1}, merge=True)
    info = db.collection("users").document(str(user)).get().to_dict()
    if ('player_id' in info):
        player_id = info['player_id']
    else:
        player_id = "Error"
    return player_id

