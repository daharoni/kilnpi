# Import your function to load profiles
from your_project.database import load_firing_profiles, get_profile_by_id

def test_load_firing_profiles():
    profiles = load_firing_profiles()
    assert profiles is not None  # Ensure something is returned
    assert len(profiles) > 0  # Ensure at least one profile is loaded

def test_get_profile_by_id():
    profile_id = 1  # Assuming you know this ID exists
    profile = get_profile_by_id(profile_id)
    assert profile is not None  # Ensure the profile is found
    assert profile['id'] == profile_id  # Ensure the correct profile is returned
