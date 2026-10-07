from community_dinners.session import Session
from community_dinners.schema import Event
from community_dinners.schema import Series

from typing import List, Tuple, Optional

import random 
from pathlib import Path
import json 
from itertools import combinations 
 
ASSIGNMENTS_FILE = Path("community_dinners/assingments.json")
 
def check_assignments_exists():
    """Check if assignments file exists."""
    if not ASSIGNMENTS_FILE.exists():
        raise FileNotFoundError("Assignments file not found")
 
class SeasonManager:
    """Manages the creation of multiple series for a dinner season."""
    
    def __init__(self, session: Session, series_count: int):
        self.session = session
        self.series_count = series_count
        self.used_pairs = []  # Track pairs across the entire season
        self.event_generator = EventGenerationEngine(session, used_pairs=self.used_pairs)
        self.series_list: List['SeriesManager'] = []
        self.events: List[Event] = []
        
    def generate_season(self) -> List['SeriesManager']:
        """Generate all series for the season."""
        events_per_series = self.session.config.events_per_series
        
        print(f"Generating {self.series_count} series with {events_per_series} events each...")
        
        # Use config series count to know how many series to generate
        for series_id in range(1, self.series_count + 1):
            # generate series 
            series = SeriesManager(self.session, series_id, events_per_series, self.event_generator, self.used_pairs)
            
            # get events from series
            series_events = series.generate_series()
            
            # add events to season
            self.events.extend(series_events)
            
            # add series to season
            self.series_list.append(series)
            
        return self.series_list
    
    def save_season(self):
        """Save all events and series to assignments.json."""
        self.event_generator.clear_assignments()
        
        # Save all events
        for event in self.events:
            self.event_generator.save_event(event)
        
        # Update with series information
        self._save_series_to_file()
        
    def _save_series_to_file(self):
        """Save series data to assignments.json."""
        with open(ASSIGNMENTS_FILE, 'r') as f:
            data = json.load(f)
        
        # Add series data
        data["series"] = [series.model_dump() for series in self.series_list]
        
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
 
class SeriesManager:
    """Manages the creation of events for a single series."""
    
    def __init__(self, session: Session, series_id: int, events_per_series: int, event_generator: 'EventGenerationEngine', used_pairs: List[Tuple[int, int]]):
        self.session = session
        self.series_id = series_id
        self.events_per_series = events_per_series
        self.event_generator = event_generator
        self.used_pairs = used_pairs  # Reference to season's used_pairs
        self.event_ids: List[int] = []
        
    def generate_series(self) -> List[Event]:
        """Generate all events for this series."""
        series_events = []
        
        for i in range(self.events_per_series):
            # Calculate global event ID
            event_id = (self.series_id - 1) * self.events_per_series + i + 1
            
            event = self.event_generator.create_event(event_id)
            if event is None:
                print(f"Failed to create event {event_id} for series {self.series_id}")
                break
                
            series_events.append(event)
            self.event_ids.append(event_id)
            
        return series_events
    
    def model_dump(self) -> dict:
        """Return series data as dictionary for writing to JSON file."""
        return {
            "series_id": self.series_id,
            "event_ids": self.event_ids
        }
 
 
# -- Algorithm Strategy Pattern --

class RandomUniqueAlgorithm:
    """Random selection requiring ALL pairs to be unique."""
    
    def __init__(self, max_attempts: int = 500000):
        self.max_attempts = max_attempts
    
    def select_event(
    self,
    host_families: List[int],
    guest_families: List[int],
    group_size: int,              
    used_pairs: List[Tuple[int, int]],
    host_max_guests_dict: dict = None 
    ) -> Optional[Tuple[int, List[int], List[Tuple[int, int]]]]: # host_id, guest_ids, event_pairs
        """Try random combinations until finding one with all unique pairs."""
        
        for attempt in range(self.max_attempts):
            # Select random host
            host = random.choice(host_families)

            # Lookup host's max_guests value
            if host in host_max_guests_dict:
                num_guests = host_max_guests_dict[host]
            else: # use global group_size if not present
                num_guests = group_size - 1
            guests = random.sample(guest_families, num_guests)
            
            # Calculate pairs for this candidate
            event_family_ids = [host] + guests
            event_pairs = [tuple(sorted(pair)) for pair in combinations(event_family_ids, 2)]
            
            # Check if ALL pairs are new
            if all(pair not in used_pairs for pair in event_pairs):
                return (host, guests, event_pairs)
        
        return None

# -- Event Generator --

class EventGenerationEngine:
    """Generates events for a series using a configurable algorithm."""
    
    def __init__(self, session, algorithm = None, used_pairs = None): 
        self.session = session
        self.host_families = session.get_host_family_ids()
        self.guest_families = session.get_guest_family_ids()
        self.group_size = session.get_config_group_size()
        self.used_pairs = used_pairs or []  # Reference to shared used_pairs
        
        # Default to RandomUniqueAlgorithm if none provided
        self.algorithm = algorithm or RandomUniqueAlgorithm()

        # Build host_max_guests dictionary lookup table
        self.host_max_guests_dict = {}
        for f in session.get_host_families():
            if f.max_guests is not None:
                self.host_max_guests_dict[f.family_id] = f.max_guests
    
    def set_algorithm(self, algorithm):
        """Change the event selection algorithm."""
        self.algorithm = algorithm

    def create_event(self, event_id: int) -> Optional[Event]:
        """Create one event using the configured algorithm."""
        result = self.algorithm.select_event(
            self.host_families,
            self.guest_families,
            self.group_size,
            self.used_pairs,
            self.host_max_guests_dict
        )
        
        if result is None:
            print(f"Could not create unique event {event_id}")
            return None
        
        host, guests, event_pairs = result
        self.used_pairs.extend(event_pairs)
        print(f"Created event {event_id} using pairs: {event_pairs}")
        return self._build_event(event_id, host, guests)
    
    def _build_event(self, event_id: int, host_family_id: int, guest_family_ids: List[int]) -> Event:
        return Event(
            event_id=event_id,
            host_family_id=host_family_id,
            guest_family_ids=guest_family_ids
        )
    
    def save_event(self, event: Event):
        """Save the event to assignments.json (append mode)"""
        check_assignments_exists()
        
        # Load existing events
        try:
            with open(ASSIGNMENTS_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"events": []}
        
        # Add the new event
        data["events"].append(event.model_dump())
        
        # Save back to file
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
 
    def clear_assignments(self):
        """Clear the assignments file."""
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump({"events": [], "series": []}, f, indent=2)
 
# Update the main section
if __name__ == '__main__':
    # Create session only when running directly
    session = Session()
    session.load_state()
    
    # Get config values
    series_count = session.config.series_count
    
    # Create season
    season = SeasonManager(session, series_count)
    
    # Generate all series and events
    season.generate_season()
    
    # Save everything
    season.save_season()
    
    print(f"Successfully generated season with {len(season.series_list)} series and {len(season.events)} total events!")