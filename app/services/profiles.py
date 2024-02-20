import json
from typing import List, Dict, Any
from app.utils.global_state import get_temperature
from app.models.firing_model import TemperatureProfilePoint

firing_profiles = []
def load_firing_profiles() -> List[Dict[str, Any]]:
    """
    Load firing profiles from a JSON file and return them as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing firing profiles.
    """
    with open('data/firing_profiles.json') as f:
        return json.load(f)


def get_firing_profiles() -> List[Dict[str, Any]]:
    global firing_profiles
    if not firing_profiles:
        firing_profiles = load_firing_profiles()
    return firing_profiles

def get_profile_by_id(profile_id: int) -> Dict[str, Any]:
    """
    Retrieve a firing profile by its ID.

    Args:
        profile_id (int): The ID of the firing profile to retrieve.

    Returns:
        dict: A dictionary representing the firing profile with the given profile_id. If no matching profile is found, None is returned.
    """
    global firing_profiles
    if not firing_profiles:
        firing_profiles = load_firing_profiles()
    for profile in firing_profiles:
        if profile['id'] == profile_id:
            return profile
    return None

async def updateProfile(profile_id: int, isDry: bool, isSoak: bool):
    global firing_profiles
    
    if not firing_profiles:
        load_firing_profiles()

    baseTemp = get_temperature()
    print(baseTemp)
    start_point = TemperatureProfilePoint(time= 0.0, temperature= baseTemp.temperature)
    low_ramp_point = TemperatureProfilePoint(time= 0.33, temperature= baseTemp.temperature + 4.0)
    for profile in firing_profiles:
        if profile['id'] == profile_id:
            
            profile['temperature_profile'].insert(0, low_ramp_point)
            profile['temperature_profile'].insert(0, start_point)
            if isDry:
                pass
            return profile
    return None