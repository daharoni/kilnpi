import json
import copy
from typing import List, Dict, Any
from app.utils.global_state import get_temperature
from app.models.app_state_model import AppState

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

async def updateProfile(state: AppState):
    global firing_profiles
    
    profile_id = state.profileID
    isDry = state.isDry
    isSoak = state.isSoak
    isHold = state.isHold
    
    
    baseTemp = get_temperature()
    if not profile_id:
        return []
    
    if not firing_profiles:
        load_firing_profiles()

    for profile in firing_profiles:
        if profile['id'] == profile_id:
            modified_profile = copy.deepcopy(profile)
            if state.isFiring:
                firingStartTemperature = state.startFiringTemperatureData.temperature
                modified_profile['temperature_profile'].insert(0, dict(time= 0.0, temperature= firingStartTemperature))
                modified_profile['temperature_profile'].insert(1, dict(time= 0.33, temperature= firingStartTemperature + 4.0))
            else:
                modified_profile['temperature_profile'].insert(0, dict(time= 0.0, temperature= baseTemp.temperature))
                modified_profile['temperature_profile'].insert(1, dict(time= 0.33, temperature= baseTemp.temperature + 4.0))
            if isDry:
                # add in a 15 minute dry period at 100 C
                dry_temp = 100
                dry_length = 0.25
                count = 2
                time1 = 0
                temp1 = 0
                for temp in modified_profile['temperature_profile'][2:]:
                    if (temp['temperature'] > dry_temp):
                        # Find where curve would have hit 100
                        # y = mx+b
                        time2 = temp['time']
                        temp2 = temp['temperature']
                        m = (temp2 - temp1) / (time2 - time1)
                        b = temp2 - m * time2
                        dry_time_start = (dry_temp - b) / m
                        
                        modified_profile['temperature_profile'].insert(count, dict(time= dry_time_start, temperature= dry_temp))
                        modified_profile['temperature_profile'].insert(count + 1, dict(time= dry_time_start + dry_length, temperature= dry_temp))
                        # push back time of remaining points
                        for i in range(count+2, len(modified_profile['temperature_profile'])):
                            modified_profile['temperature_profile'][i]['time'] = modified_profile['temperature_profile'][i]['time'] + dry_length
                        break
                    
                    count = count + 1
                    time1 = temp['time']
                    temp1 = temp['temperature']
            if isSoak:
                # add in a 15 minute soak period at 700 C to burn stuff off
                soak_temp = 700
                soak_length = 0.25
                count = 0
                time1 = 0
                temp1 = 0
                for temp in modified_profile['temperature_profile']:
                    if (temp['temperature'] > soak_temp):
                        # Find where curve would have hit 100
                        # y = mx+b
                        time2 = temp['time']
                        temp2 = temp['temperature']
                        m = (temp2 - temp1) / (time2 - time1)
                        b = temp2 - m * time2
                        dry_time_start = (soak_temp - b) / m
                        
                        modified_profile['temperature_profile'].insert(count, dict(time= dry_time_start, temperature= soak_temp))
                        modified_profile['temperature_profile'].insert(count + 1, dict(time= dry_time_start + soak_length, temperature= soak_temp))
                        # push back time of remaining points
                        for i in range(count+2, len(modified_profile['temperature_profile'])):
                            modified_profile['temperature_profile'][i]['time'] = modified_profile['temperature_profile'][i]['time'] + soak_length
                        break
                    count = count + 1
                    time1 = temp['time']
                    temp1 = temp['temperature']
            if isHold:
                # add in a 15 minute soak period at 700 C to burn stuff off
                last_profile_temp_info = modified_profile['temperature_profile'][-1]
                hold_length = 0.25                  
                modified_profile['temperature_profile'].append(dict(time= last_profile_temp_info['time'] + hold_length, temperature= last_profile_temp_info['temperature']))
                       
            print(modified_profile)
            return modified_profile
    return None