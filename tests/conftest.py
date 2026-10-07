# tests/conftest.py
import pytest
from community_dinners.schema.person import Person
from community_dinners.schema.family import Family
from community_dinners.schema.config import Config
from community_dinners.schema.event import Event
from community_dinners.session import Session

too_long_id = 2**12 + 1
too_long_name = "n" * (2**8)

# ======================================================================
# Raw Dictionary Fixtures 
# ======================================================================
 
@pytest.fixture
def sample_person_dict():
    """Sample person data as dictionary."""
    return {
        "person_id": 1,
        "family_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "kid": False,
        "phone": "123-456-7890",
        "email": "john.doe@example.com"
    }

@pytest.fixture
def sample_persons_dict_list():
    """Sample person dictionary list."""
    return [
        {"person_id": 1, "first_name": "John", "last_name": "Doe"},
        {"person_id": 2, "first_name": "Jane", "last_name": "Smith"}
    ]
 
@pytest.fixture
def sample_person_dict_minimal():
    """Minimal person data with only required fields."""
    return {
        "person_id": 1,
        "first_name": "John",
        "last_name": "Doe"
    }
 
@pytest.fixture
def sample_family_dict():
    """Sample family data as dictionary."""
    return {
        "family_id": 1,
        "name": "Doe",
        "address": "123 Main St, Anytown, USA 12345",
        "can_host": True,
        "family_members": [1, 2, 3]
    }

@pytest.fixture
def sample_families_10f_36p__dict_list():
    """Sample family dictionary list."""
    return [
        {
            "family_id":1,
            "name": "Doe",
            "address": "1 address, example, AA 12345",
            "can_host": True,
            "family_members": [1,2,3]
        },
        {
            "family_id":2,
            "name": "Smith",
            "address": "2 address, example, BB 12345",
            "can_host": True,
            "family_members": [4,5,6,7]
        },
        {
            "family_id":3,
            "name": "Price",
            "address": "3 address, example, CC 12345",
            "can_host": False,
            "family_members": [8,9]
        },
        {
            "family_id":4,
            "name": "Bridger",
            "address": "4 address, example, DD 12345",
            "can_host": True,
            "family_members": [10,11,12]
        },
        {
            "family_id":5,
            "name": "Johnson",
            "address": "5 address, example, EE 12345",
            "can_host": False,
            "family_members": [13,14,15,16,17]
        },
        {
            "family_id":6,
            "name": "Williams",
            "address": "6 address, example, FF 12345",
            "can_host": False,
            "family_members": [18,19,20,21]
        },
        {
            "family_id":7,
            "name": "Brown",
            "address": "7 address, example, GG 12345",
            "can_host": False,
            "family_members": [22,23,24]
        },
        {
            "family_id":8,
            "name": "Davis",
            "address": "8 address, example, HH 12345",
            "can_host": False,
            "family_members": [25,26,27,28,29]
        },
        {
            "family_id":9,
            "name": "Miller",
            "address": "9 address, example, II 12345",
            "can_host": False,
            "family_members": [30,31,32,33]
        },
        {
            "family_id":10,
            "name": "Wilson",
            "address": "10 address, example, JJ 12345",
            "can_host": False,
            "family_members": [34,35,36]
        }
    ]
 
@pytest.fixture
def sample_config_dict():
    """Sample config data as dictionary."""
    return {
        "group_size": 4,
        "events_per_series": 3,
        "series_count": 4
    }
 
@pytest.fixture
def sample_event_dict():
    """Sample event data as dictionary."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 4]
    }
 
# ======================================================================
# Schema Object Fixtures using raw dictionary fixtures
# ======================================================================
 
@pytest.fixture
def sample_person(sample_person_dict):
    """Sample Person object."""
    return Person.from_dict(sample_person_dict)

@pytest.fixture
def sample_persons(sample_persons_dict_list):
    """Sample Person objects."""
    return [Person.from_dict(p) for p in sample_persons_dict_list]

@pytest.fixture
def sample_family(sample_family_dict):
    """Sample Family object."""
    return Family.from_dict(sample_family_dict)


@pytest.fixture
def sample_config(sample_config_dict):
    """Sample Config object."""
    return Config.from_dict(sample_config_dict)
 
@pytest.fixture
def sample_event(sample_event_dict):
    """Sample Event object."""
    return Event.from_dict(sample_event_dict)

# ======================================================================
# Session Fixtures
# ======================================================================

@pytest.fixture
def sample_config():
    """Sample config object."""
    return Config.from_dict({"group_size": 4, "events_per_series": 3, "series_count": 2})

@pytest.fixture
def sample_families_10f_36p(sample_families_10f_36p__dict_list):
    """Sample Family objects."""
    return [Family.from_dict(f) for f in sample_families_10f_36p__dict_list]

@pytest.fixture
def temp_state_dir():
    """Create a temporary directory for state files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_state_file(temp_state_dir):
    """Create a mock state file path."""
    return temp_state_dir / "state.json"

@pytest.fixture
def sample_state_data(sample_families_10f_36p, sample_persons, sample_config):
    """Complete state data as dict."""
    return {
        "families": [f.model_dump() for f in sample_families_10f_36p],
        "persons": [p.model_dump() for p in sample_persons],
        "config": sample_config.model_dump()
    }

@pytest.fixture
def sample_state_data_missing_families():
    """State data missing 'families' key."""
    return {"persons": [], "config": None}

# ======================================================================
# List Fixtures
# ======================================================================
 
@pytest.fixture
def sample_persons_dict_list():
    """List of sample person dictionaries."""
    return [
        {
            "person_id": 1,
            "family_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "kid": False
        },
        {
            "person_id": 2,
            "family_id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 28,
            "kid": False
        },
        {
            "person_id": 3,
            "family_id": 1,
            "first_name": "Jimmy",
            "last_name": "Doe",
            "age": 8,
            "kid": True
        }
    ]
 
@pytest.fixture
def sample_families_dict_list():
    """List of sample family dictionaries."""
    return [
        {
            "family_id": 1,
            "name": "Doe",
            "address": "123 Main St, Anytown, USA 12345",
            "can_host": True,
            "family_members": [1, 2, 3]
        },
        {
            "family_id": 2,
            "name": "Smith",
            "address": "456 Oak Ave, Anytown, USA 12345",
            "can_host": False,
            "family_members": [4, 5]
        }
    ]
 
# ======================================================================
# Combined Valid Dataset
# ======================================================================
 
@pytest.fixture
def valid_dataset():
    """Complete valid dataset with consistent family/person relationships."""
    persons = [
        {"person_id": 1, "family_id": 1, "first_name": "John", "last_name": "Doe", "age": 30},
        {"person_id": 2, "family_id": 1, "first_name": "Jane", "last_name": "Doe", "age": 28},
        {"person_id": 3, "family_id": 1, "first_name": "Jimmy", "last_name": "Doe", "age": 8},
        {"person_id": 4, "family_id": 2, "first_name": "Bob", "last_name": "Smith", "age": 35},
        {"person_id": 5, "family_id": 2, "first_name": "Mary", "last_name": "Smith", "age": 32}
    ]
    
    families = [
        {"family_id": 1, "name": "Doe", "address": "123 Main St", "can_host": True, "family_members": [1, 2, 3]},
        {"family_id": 2, "name": "Smith", "address": "456 Oak Ave", "can_host": False, "family_members": [4, 5]}
    ]
    
    return {
        "persons": persons,
        "families": families,
        "config": {"group_size": 4, "events_per_series": 3, "series_count": 4}
    }

 
# ======================================================================
# Invalid Data Fixtures
# ======================================================================
 
#-------------------
# Person Invalid Data
#-------------------
@pytest.fixture
def invalid_person_missing_required():
    """Person data missing required fields."""
    return {
        "person_id": 1
        # Missing first_name and last_name
    }
 
@pytest.fixture
def invalid_person_wrong_types():
    """Person data with wrong types."""
    return {
        "person_id": "not_an_int",
        "family_id": 1,
        "first_name": 123,
        "last_name": 4.5,
        "age": "thirty"
    }

@pytest.fixture
def invalid_person_id_zero():
    """Person data with person_id = 0."""
    return {
        "person_id": 0,
        "family_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "age": 30
    }

@pytest.fixture
def invalid_person_id_negative():
    """Person data with person_id = -1."""
    return {
        "person_id": -1,
        "family_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "age": 30
    }

@pytest.fixture
def invalid_person_id_too_large():
    """Person data with person_id over the limit."""
    return {
        "person_id": too_long_id,
        "family_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "age": 30
    }

@pytest.fixture
def invalid_person_first_name_too_long():
    """Person data with first_name too long."""
    return {
        "person_id": 1,
        "family_id": 1,
        "first_name": too_long_name,
        "last_name": "Doe",
        "age": 30
    }

@pytest.fixture
def invalid_person_last_name_too_long():
    """Person data with last_name too long."""
    return {
        "person_id": 1,
        "family_id": 1,
        "first_name": "John",
        "last_name": too_long_name,
        "age": 30
    }

@pytest.fixture
def invalid_person_age_too_old():
    """Person data with age over the limit."""
    return {
        "person_id": 1,
        "family_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "age": 151
    }

#-------------------
# Family Invalid Data
#-------------------

# Required Fields
@pytest.fixture
def invalid_family_missing_required():
    """Family data missing required fields."""
    return {
        "family_id": 1,
        "name": "Doe"
        # Missing address and family_members
    }

# ID
@pytest.fixture
def invalid_family_id_zero():
    """Family data with family_id = 0."""
    return {
        "family_id": 0,
        "name": "Doe",
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }
 


@pytest.fixture
def invalid_family_id_negative():
    """Family data with family_id = -1."""
    return {
        "family_id": -1,
        "name": "Doe",
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }

@pytest.fixture
def invalid_family_id_too_large():
    """Family data with family_id that exceeds the limit."""
    return {
        "family_id": too_long_id, 
        "name": "Doe",
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }

# Name
@pytest.fixture
def invalid_family_name_empty():
    """Family data with empty name."""
    return {
        "family_id": 1,
        "name": "",
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }

@pytest.fixture
def invalid_family_name_whitespace():
    """Family data with whitespace-only name."""
    return {
        "family_id": 1,
        "name": "   ",
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }

@pytest.fixture
def invalid_family_name_too_long():
    """Family data with very long name."""
    return {
        "family_id": 1,
        "name": too_long_name,
        "address": "123 Main St",
        "family_members": [1, 2, 3]
    }

# Address
@pytest.fixture
def invalid_family_address_empty():
    """Family data with empty address."""
    return {
        "family_id": 1,
        "name": "Doe",
        "address": "",
        "family_members": [1, 2, 3]
    }
 
@pytest.fixture
def invalid_family_address_too_long():
    """Family data with very long address."""
    return {
        "family_id": 1,
        "name": "Doe",
        "address": "A" * 1000,
        "family_members": [1, 2, 3]
    }
#-------------------
# Config Invalid Data
#-------------------

# Size

@pytest.fixture
def invalid_config_group_size_zero():
    """Config data with group_size = 0."""
    return {
        "group_size": 0,
        "events_per_series": 3,
        "series_count": 4
    }
 
@pytest.fixture
def invalid_config_group_size_too_large():
    """Config data with very large group_size."""
    return {
        "group_size": 21,
        "events_per_series": 3,
        "series_count": 4
    }

# Events per Series


@pytest.fixture
def invalid_config_events_per_series_zero():
    """Config data with events_per_series = 0."""
    return {
        "group_size": 4,
        "events_per_series": 0,
        "series_count": 4
    }
 
@pytest.fixture
def valid_config_events_per_series_one():
    """Config data with events_per_series = 1 (minimal)."""
    return {
        "group_size": 4,
        "events_per_series": 1,
        "series_count": 4
    }

# Series count

@pytest.fixture
def invalid_config_series_count_zero():
    """Config data with series_count = 0."""
    return {
        "group_size": 4,
        "events_per_series": 3,
        "series_count": 0
    }

#-------------------
# Event Invalid Data
#-------------------

# Event ID

@pytest.fixture
def invalid_event_id_string():
    """Event data with event_id as string."""
    return {
        "event_id": "one",  # Should be int
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 4]
    }
    
@pytest.fixture
def invalid_event_id_zero():
    """Event data with event_id = 0."""
    return {
        "event_id": 0,
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 4]
    }
 
@pytest.fixture
def invalid_event_id_negative():
    """Event data with event_id = -1."""
    return {
        "event_id": -1,
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 4]
    }

@pytest.fixture
def invalid_event_id_too_large():
    """Event data with event_id that exceeds the limit."""
    return {
        "event_id": too_long_id, 
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 4]
    }

# Host FamilyID


@pytest.fixture
def invalid_event_host_family_id_zero():
    """Event data with host_family_id = 0."""
    return {
        "event_id": 1,
        "host_family_id": 0,
        "guest_family_ids": [2, 3, 4]
    }
 
@pytest.fixture
def invalid_event_host_family_id_negative():
    """Event data with host_family_id = -1."""
    return {
        "event_id": 1,
        "host_family_id": -1,
        "guest_family_ids": [2, 3, 4]
    }

@pytest.fixture
def invalid_event_host_family_id_too_large():
    """Event data with host_family_id that exceeds the limit."""
    return {
        "event_id": 1,
        "host_family_id": too_long_id,
        "guest_family_ids": [2, 3, 4]
    }

# Guest List Family IDs

@pytest.fixture
def invalid_event_guest_list_type():
    """Event data with guest_family_ids as string instead of list."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": "not a list"  # Should be List[int]
    }

@pytest.fixture
def invalid_event_guest_list_string_items():
    """Event data with non-int items in guest list."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": [2, "three", 4]  # "three" should be int
    }
 
@pytest.fixture
def invalid_event_empty_guest_list():
    """Event data with 0 guests (empty list)."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": []
    }
 
@pytest.fixture
def invalid_event_too_many_guests():
    """Event data with 51 guests (exceeds limit)."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": list(range(2, 53))  # 51 guests
    }

@pytest.fixture
def invalid_event_host_in_guest_list():
    """Event data with host_family_id in guest_family_ids."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": [1, 2, 3]  # Host (1) is in guest list
    }
 
@pytest.fixture
def valid_event_duplicate_guests():
    """Event data with duplicate guest IDs."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": [2, 3, 2, 4]  # Duplicate 2
    }
 
@pytest.fixture
def invalid_event_negative_guest_ids():
    """Event data with negative guest IDs."""
    return {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": [2, -1, 4]  # Negative ID
    }

#-------------------
# Dataset Invalid Data
#-------------------

@pytest.fixture
def invalid_dataset_person_in_family_doesnt_exist():
    """Family points to person that doesn't exist."""
    persons = [
        {"person_id": 2, "family_id": 1, "first_name": "Jane", "last_name": "Doe", "age": 28},
        {"person_id": 3, "family_id": 1, "first_name": "Jimmy", "last_name": "Doe", "age": 8},
        {"person_id": 4, "family_id": 2, "first_name": "Bob", "last_name": "Smith", "age": 35},
        {"person_id": 5, "family_id": 2, "first_name": "Mary", "last_name": "Smith", "age": 32}
    ]
    
    families = [
        {"family_id": 1, "name": "Doe", "address": "123 Main St", "can_host": True, "family_members": [1, 2, 3]},
        {"family_id": 2, "name": "Smith", "address": "456 Oak Ave", "can_host": False, "family_members": [4, 5]}
    ]
    
    return {
        "persons": persons,
        "families": families,
        "config": {"group_size": 4, "events_per_series": 3, "series_count": 4}
    }

@pytest.fixture
def invalid_dataset_family_person_points_to_doesnt_exist():
    """Person points to family that doesn't exist."""
    persons = [
        {"person_id": 2, "family_id": 1, "first_name": "Jane", "last_name": "Doe", "age": 28},
        {"person_id": 3, "family_id": 1, "first_name": "Jimmy", "last_name": "Doe", "age": 8},
        {"person_id": 4, "family_id": 2, "first_name": "Bob", "last_name": "Smith", "age": 35},
        {"person_id": 5, "family_id": 2, "first_name": "Mary", "last_name": "Smith", "age": 32}
    ]
    
    families = [
        {"family_id": 1, "name": "Doe", "address": "123 Main St", "can_host": True, "family_members": [1, 2, 3]},
        {"family_id": 2, "name": "Smith", "address": "456 Oak Ave", "can_host": False, "family_members": [4, 5]}
    ]
    
    return {
        "persons": persons,
        "families": families,
        "config": {"group_size": 4, "events_per_series": 3, "series_count": 4}
    }

@pytest.fixture
def invalid_dataset_person_in_wrong_family():
    """Person points to family that doesn't point to them."""
    persons = [
        {"person_id": 1, "family_id": 2, "first_name": "John", "last_name": "Doe", "age": 30},
        {"person_id": 2, "family_id": 1, "first_name": "Jane", "last_name": "Doe", "age": 28},
        {"person_id": 3, "family_id": 1, "first_name": "Jimmy", "last_name": "Doe", "age": 8},
        {"person_id": 4, "family_id": 2, "first_name": "Bob", "last_name": "Smith", "age": 35},
        {"person_id": 5, "family_id": 2, "first_name": "Mary", "last_name": "Smith", "age": 32}
    ]
    
    families = [
        {"family_id": 1, "name": "Doe", "address": "123 Main St", "can_host": True, "family_members": [1, 2, 3]},
        {"family_id": 2, "name": "Smith", "address": "456 Oak Ave", "can_host": False, "family_members": [4, 5]}
    ]
    
    return {
        "persons": persons,
        "families": families,
        "config": {"group_size": 4, "events_per_series": 3, "series_count": 4}
    }