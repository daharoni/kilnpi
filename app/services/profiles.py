import json
from typing import List, Dict, Any

def load_firing_profiles() -> List[Dict[str, Any]]:
    """
    Load firing profiles from a JSON file and return them as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing firing profiles.
    """
    with open('data/firing_profiles.json') as f:
        firing_profiles = json.load(f)
    return firing_profiles


def get_firing_profiles() -> List[Dict[str, Any]]:
    return load_firing_profiles()

def get_profile_by_id(profile_id: int) -> Dict[str, Any]:
    """
    Retrieve a firing profile by its ID.

    Args:
        profile_id (int): The ID of the firing profile to retrieve.

    Returns:
        dict: A dictionary representing the firing profile with the given profile_id. If no matching profile is found, None is returned.
    """
    profiles = load_firing_profiles()
    for profile in profiles:
        if profile['id'] == profile_id:
            return profile
    return None