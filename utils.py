from difflib import SequenceMatcher

user_states = {}

def init_user(user_id):
    if user_id not in user_states:
        user_states[user_id] = {
            "asked": 0,
            "correct": 0,
            "current": 0
        }

def is_similar(a: str, b: str) -> bool:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio() >= 0.6
