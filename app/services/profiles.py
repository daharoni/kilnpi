import json
from typing import List, Dict, Any

def load_firing_profiles() -> List[Dict[str, Any]]:
    with open('data/firing_profiles.json') as f:
        return json.load(f)

def get_firing_profiles() -> List[Dict[str, Any]]:
    return load_firing_profiles()

def get_profile_by_id(profile_id: int) -> Dict[str, Any]:
    profiles = load_firing_profiles()
    for profile in profiles:
        if profile['id'] == profile_id:
            return profile
    return None