import json
from pathlib import Path
from community_dinners.schema import Family, Person, Config
from community_dinners.loader import load_json_key, load_dict, save_dict

STATE_FILE = Path("community_dinners/state.json")

def check_state_exists():
    """Check if state file exists."""
    if not STATE_FILE.exists():
        raise FileNotFoundError("State file not found")

class Session:
    """Session class for managing application state."""
    
    def __init__(self):
        # Initialize empty collections and config
        self.families = []
        self.persons = []
        self.config = None
        self._cached_state = None  # Cache for file reads
    
    def _load_from_state_file(self, use_cache: bool = True):
        """Load raw data from state file (internal method).
 
        Args:
            use_cache: If True, return cached data if available.
        """
        if use_cache and self._cached_state is not None:
            return self._cached_state
    
        check_state_exists()
        data = load_dict(STATE_FILE)
        self._cached_state = {
            "families": data.get("families", []),
            "persons": data.get("persons", []),
            "config": data.get("config")
        }
        return self._cached_state
        
    
    def _invalidate_cache(self):
        """Invalidate the cached state data."""
        self._cached_state = None
    
    # -- Load Methods --
    def load_families(self):
        """Load only families from state file."""
        data = self._load_from_state_file()
        self.families = Family.from_list(data["families"])
    
    def load_persons(self):
        """Load only persons from state file."""
        data = self._load_from_state_file()
        self.persons = Person.from_list(data["persons"])
    
    def load_config(self):
        """Load only config from state file."""
        data = self._load_from_state_file()
        self.config = Config.from_dict(data["config"]) if data["config"] else None
    
    def load_state(self):
        """Load all data from state file (single file read)."""
        data = self._load_from_state_file()
        self.families = Family.from_list(data["families"])
        self.persons = Person.from_list(data["persons"])
        self.config = Config.from_dict(data["config"]) if data["config"] else None
    
    # -- Save Methods --
    def _save_to_file(self, state: dict):
        """Write state to file and invalidate cache."""
        save_dict(STATE_FILE, state)
        self._invalidate_cache()
    
    def _read_current_state(self) -> dict:
        """Read current state from file."""
        return load_dict(STATE_FILE)
    
    def save_state(self):
        """Save all data to state file."""
        state = {
            "families": [f.model_dump() for f in self.families],
            "persons": [p.model_dump() for p in self.persons],
            "config": self.config.model_dump() if self.config else None
        }
        self._save_to_file(state)
    
    def save_families(self):
        """Save only families to state file."""
        state = self._read_current_state()
        state["families"] = [f.model_dump() for f in self.families]
        self._save_to_file(state)
    
    def save_persons(self):
        """Save only persons to state file."""
        state = self._read_current_state()
        state["persons"] = [p.model_dump() for p in self.persons]
        self._save_to_file(state)
    
    def save_config(self):
        """Save only config to state file."""
        state = self._read_current_state()
        state["config"] = self.config.model_dump() if self.config else None
        self._save_to_file(state)
   
    # -- Update Methods --
    def update_families(self, families):
        """Update families in state file."""
        self.families = families
        self.save_families()
    
    def update_persons(self, persons):
        """Update persons in state file."""
        self.persons = persons
        self.save_persons()
    
    def update_config(self, config):
        """Update config in state file."""
        self.config = config
        self.save_config()
    
    # -- Get Methods --
    def get_host_families(self):
        """Get list of host families."""
        return [f for f in self.families if f.can_host]

    def get_host_family_ids(self):
        """Get list of host family IDs."""
        return [f.family_id for f in self.families if f.can_host]
    
    def get_guest_families(self):
        """Get list of guest families."""
        return [f for f in self.families if not f.can_host]

    def get_guest_family_ids(self):
        """Get list of guest family IDs."""
        return [f.family_id for f in self.families if not f.can_host]

    def get_config_group_size(self):
        """Get config group size."""
        return self.config.group_size

# Self-test
if __name__ == '__main__':
    """Manual test for session functionality."""
    try:
        check_state_exists()
        print("State file exists")
        
        # Test loading
        session = Session()
        session.load_state()
        print(f"Loaded {len(session.families)} families, {len(session.persons)} persons")
        
        # Test saving
        session.save_state()
        print("Save successful!")
        
    except FileNotFoundError as e:
        print(f"State file not found: {e}")
    except Exception as e:
        print(f"Error: {e}")