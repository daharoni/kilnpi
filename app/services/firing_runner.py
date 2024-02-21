from app.utils.pid_controller import PIDController
import json
import logging
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.kiln_model import KilnParameters




logger = logging.getLogger("logger")

def load_kiln_parameters() -> List[Dict[str, Any]]:
    """
    Load firing profiles from a JSON file and return them as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing firing profiles.
    """
    global logger
    
    try:
        with open('data/kiln_parameters.json') as f:
            data = json.load(f)
        
            # Parse the JSON data into a Pydantic model
            kiln_params = KilnParameters.model_validate(data)
            logger.info(f"Read kiln parameters file: {kiln_params}")
    except IOError as e:
        logger.error(f"Error opening or reading the kiln parameter file: {e}")

    
async def run_kiln() -> None:
    global logger
    
    kiln_params = load_kiln_parameters()
    pid_controller = PIDController(kiln_params)

    while True:
       
        await asyncio.sleep(3)