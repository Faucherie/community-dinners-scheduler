from community_dinners.schema.person import Person
from community_dinners.schema.family import Family
from community_dinners.schema.config import Config
from community_dinners.schema.event import Event
from pydantic import ValidationError
import pytest

# ==============================================================================
# Person Tests
# ==============================================================================

# ------------------------------------------------------------------
# Person.from_dict() Tests
# ------------------------------------------------------------------
def test_create_person_valid_from_dict(sample_person_dict):
    """Test creating a Person from a valid dictionary."""
    person = Person.from_dict(sample_person_dict)
    
    assert person.person_id == 1
    assert person.family_id == 1
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.age == 30
    assert person.kid is False
    assert person.phone == "123-456-7890"
    assert person.email == "john.doe@example.com"

def test_create_person_missing_required_fields(invalid_person_missing_required):
    """Test creating a Person with missing required fields."""
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_missing_required)
    assert "first_name" in str(exc_info.value)
    assert "last_name" in str(exc_info.value)

def test_create_person_from_dict_returns_object(sample_person_dict):
    """Test that from_dict returns a Person object."""
    result = Person.from_dict(sample_person_dict)
    assert isinstance(result, Person)

def test_create_person_optional_fields_default_values(sample_person_dict_minimal):
    """Test that optional fields get correct default values when omitted."""
    person = Person.from_dict(sample_person_dict_minimal)
    
    # Verify default values
    assert person.family_id is None
    assert person.age is None
    assert person.kid is False
    assert person.phone == ""
    assert person.email == ""

def test_create_person_invalid_data_types(invalid_person_wrong_types):
    """Test creating a Person with invalid data types."""
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_wrong_types)
    
    # expects string but input is int and float
    assert "first_name" in str(exc_info.value)
    assert "last_name" in str(exc_info.value)
    
    # expects int but input is string
    assert "person_id" in str(exc_info.value)
    assert "age" in str(exc_info.value)

# -- Class Validation Tests --

# ID
def test_person_id_zero(invalid_person_id_zero):
    """Test person_id = 0 (should fail if IDs start at 1)."""
    
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_id_zero)
    
    assert "person_id" in str(exc_info.value)
            
def test_person_id_negative(invalid_person_id_negative):
    """Test person_id = -1 (should fail if IDs start at 1)."""
        
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_id_negative)

    assert "person_id" in str(exc_info.value)
            

def test_person_id_too_large(invalid_person_id_too_large):
    """Test person_id too large."""
    
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_id_too_large)

    assert "person_id" in str(exc_info.value)

# First Name
def test_person_first_name_too_long(invalid_person_first_name_too_long):
    """Test first_name too long."""
    
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_first_name_too_long)

    assert "first_name" in str(exc_info.value)

# Last Name
def test_person_last_name_too_long(invalid_person_last_name_too_long):
    """Test last_name too long."""
    
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_last_name_too_long)

    assert "last_name" in str(exc_info.value)

# Age
def test_person_age_too_large(invalid_person_age_too_old):
    """Test age too large."""
    
    with pytest.raises(ValidationError) as exc_info:
        Person.from_dict(invalid_person_age_too_old)

    assert "age" in str(exc_info.value)

# ------------------------------------------------------------------
# Person.from_list() Tests
# ------------------------------------------------------------------
def test_create_person_valid_from_list(sample_persons_dict_list):
    """Test creating Persons from a valid list."""
    persons = Person.from_list(sample_persons_dict_list)
    
    assert len(persons) == 3
    assert persons[0].first_name == "John"
    assert persons[1].first_name == "Jane"
    assert persons[2].first_name == "Jimmy"

def test_create_person_from_list_returns_list(sample_person_dict):
    """Test that from_list returns a list, not a single Person."""
    data = [sample_person_dict]
    
    result = Person.from_list(data)
    assert isinstance(result, list)
    assert len(result) == 1

def test_create_person_from_empty_list():
    """Test creating Persons from an empty list."""
    persons = Person.from_list([])
    assert persons == []
    assert isinstance(persons, list)

# ======================================================================
# Family Tests
# ======================================================================

# ------------------------------------------------------------------
# Family.from_dict() Tests
# ------------------------------------------------------------------
def test_create_family_valid_from_dict(sample_family_dict):
    """Test creating a Family from a valid dictionary."""
    family = Family.from_dict(sample_family_dict)
    
    assert family.family_id == 1
    assert family.name == "Doe"
    assert family.address == "123 Main St, Anytown, USA 12345"
    assert family.can_host is True
    assert family.family_members == [1, 2, 3]

def test_create_family_missing_required_fields(invalid_family_missing_required):
    """Test creating a Family with missing required fields."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_missing_required)
    assert "address" in str(exc_info.value)
    assert "family_members" in str(exc_info.value)

def test_create_family_from_dict_returns_object(sample_family_dict):
    """Test that from_dict returns a Family object."""
    result = Family.from_dict(sample_family_dict)
    assert isinstance(result, Family)

def test_create_family_optional_field_default():
    """Test that can_host gets default value when omitted."""
    minimal_data = {
        "family_id": 1,
        "name": "Doe",
        "address": "123 Main St, Anytown, USA 12345",
        "family_members": [1, 2, 3]
    }
    
    family = Family.from_dict(minimal_data)
    assert family.can_host is False  # Default value

# ------------------------------------------------------------------
# Validation Tests
# ------------------------------------------------------------------

# ID
def test_family_id_zero(invalid_family_id_zero):
    """Test family_id = 0 ."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_id_zero)
    assert "family_id" in str(exc_info.value)

def test_family_id_negative(invalid_family_id_negative):
    """Test family_id = -1 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_id_negative)
    assert "family_id" in str(exc_info.value)

def test_family_id_too_large(invalid_family_id_too_large):
    """Test family_id = 2^12 + 1 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_id_too_large)
    assert "family_id" in str(exc_info.value)

# Name
def test_family_name_empty(invalid_family_name_empty):
    """Test name = '' (empty string)."""
    # Pydantic allows empty strings by default
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_name_empty)
    assert "name" in str(exc_info.value)
   
 
def test_family_name_whitespace(invalid_family_name_whitespace):
    """Test name = '   ' (whitespace only)."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_name_whitespace)
    assert "name" in str(exc_info.value)

def test_family_name_too_long(invalid_family_name_too_long):
    """Test name with too many characters than my arbitrary limit of 255."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_name_too_long)
    assert "name" in str(exc_info.value)

# Address
def test_family_address_empty(invalid_family_address_empty):
    """Test address = '' (empty string)."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_address_empty)
    assert "address" in str(exc_info.value)
 
def test_family_address_too_long(invalid_family_address_too_long):
    """Test address with 1000 characters."""
    with pytest.raises(ValidationError) as exc_info:
        Family.from_dict(invalid_family_address_too_long)
    assert "address" in str(exc_info.value)


# ------------------------------------------------------------------
# Family.from_list() Tests
# ------------------------------------------------------------------
def test_create_family_valid_from_list(sample_families_dict_list):
    """Test creating Families from a valid list."""
    families = Family.from_list(sample_families_dict_list)
    
    assert len(families) == 2
    assert families[0].name == "Doe"
    assert families[1].name == "Smith"

def test_create_family_from_list_returns_list(sample_family_dict):
    """Test that from_list returns a list, not a single Family."""
    data = [sample_family_dict]
    
    result = Family.from_list(data)
    assert isinstance(result, list)
    assert len(result) == 1

def test_create_family_from_empty_list():
    """Test creating Families from an empty list."""
    families = Family.from_list([])
    assert families == []
    assert isinstance(families, list)

# ======================================================================
# Config Tests
# ======================================================================

# ------------------------------------------------------------------
# Config.from_dict() Tests
# ------------------------------------------------------------------
def test_create_config_valid_from_dict(sample_config_dict):
    """Test creating a Config from a valid dictionary."""
    config = Config.from_dict(sample_config_dict)
    
    assert config.group_size == 4
    assert config.events_per_series == 3
    assert config.series_count == 4

def test_create_config_missing_required_fields():
    """Test creating a Config with missing required fields."""
    invalid_data = {
        "group_size": 4
        # Missing events_per_series and series_count
    }
    
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_data)
    assert "events_per_series" in str(exc_info.value)
    assert "series_count" in str(exc_info.value)

def test_create_config_from_dict_returns_object(sample_config_dict):
    """Test that from_dict returns a Config object."""
    result = Config.from_dict(sample_config_dict)
    assert isinstance(result, Config)

def test_create_config_invalid_data_types():
    """Test creating a Config with invalid data types."""
    invalid_data = {
        "group_size": "four",  # Should be int
        "events_per_series": 3,
        "series_count": 4
    }
    
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_data)
    assert "group_size" in str(exc_info.value)

# ------------------------------------------------------------------
# Config Validation Tests
# ------------------------------------------------------------------

# Size
def test_config_group_size_zero(invalid_config_group_size_zero):
    """Test group_size = 0 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_config_group_size_zero)
    assert "group_size" in str(exc_info.value)
 
def test_config_group_size_too_large(invalid_config_group_size_too_large):
    """Test group_size = 21 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_config_group_size_too_large)
    assert "group_size" in str(exc_info.value)

# Events per series

def test_config_events_per_series_zero(invalid_config_events_per_series_zero):
    """Test events_per_series = 0 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_config_events_per_series_zero)
    assert "events_per_series" in str(exc_info.value)

# Series count

def test_config_series_count_zero(invalid_config_series_count_zero):
    """Test series_count = 0 (should fail or allow?)."""
    with pytest.raises(ValidationError) as exc_info:
        Config.from_dict(invalid_config_series_count_zero)
    assert "series_count" in str(exc_info.value)

# ======================================================================
# Event Tests
# ======================================================================

# ------------------------------------------------------------------
# Event.from_dict() Tests
# ------------------------------------------------------------------
def test_create_event_valid_from_dict(sample_event_dict):
    """Test creating an Event from a valid dictionary."""
    event = Event.from_dict(sample_event_dict)
    
    assert event.event_id == 1
    assert event.host_family_id == 1
    assert event.guest_family_ids == [2, 3, 4]

def test_create_event_missing_required_fields():
    """Test creating an Event with missing required fields."""
    invalid_data = {
        "event_id": 1
        # Missing host_family_id and guest_family_ids
    }
    
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_data)
    assert "host_family_id" in str(exc_info.value)
    assert "guest_family_ids" in str(exc_info.value)

def test_create_event_from_dict_returns_object(sample_event_dict):
    """Test that from_dict returns an Event object."""
    result = Event.from_dict(sample_event_dict)
    assert isinstance(result, Event)

def test_create_event_empty_guest_list():
    """Test creating an Event with empty guest list."""
    data = {
        "event_id": 1,
        "host_family_id": 1,
        "guest_family_ids": []
    }
    
    event = Event.from_dict(data)
    assert event.guest_family_ids == []

#--------------------------
# Event Validation Tests
#--------------------------

# Event ID
def test_create_event_invalid_data_types(invalid_event_id_string):
    """Test creating an Event with invalid data types."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_id_string)
    assert "event_id" in str(exc_info.value)

def test_event_id_zero(invalid_event_id_zero):
    """Test event_id = 0 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_id_zero)
    assert "event_id" in str(exc_info.value)
 
def test_event_id_negative(invalid_event_id_negative):
    """Test event_id = -1 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_id_negative)
    assert "event_id" in str(exc_info.value)

def test_event_id_too_large(invalid_event_id_too_large):
    """Test event_id that exceeds the limit (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_id_too_large)
    assert "event_id" in str(exc_info.value)

# Host Family ID

def test_event_host_family_id_zero(invalid_event_host_family_id_zero):
    """Test host_family_id = 0 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_host_family_id_zero)
    assert "host_family_id" in str(exc_info.value)
 
def test_event_host_family_id_negative(invalid_event_host_family_id_negative):
    """Test host_family_id = -1 (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_host_family_id_negative)
    assert "host_family_id" in str(exc_info.value)

def test_event_host_family_id_too_large(invalid_event_host_family_id_too_large):
    """Test host_family_id that exceeds the limit (should fail)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_host_family_id_too_large)
    assert "host_family_id" in str(exc_info.value)

# Guest List Family IDs
def test_create_event_invalid_guest_list_type(invalid_event_guest_list_type):
    """Test creating an Event with invalid guest list type."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_guest_list_type)
    assert "guest_family_ids" in str(exc_info.value)

def test_create_event_invalid_guest_list_items(invalid_event_guest_list_string_items):
    """Test creating an Event with non-int items in guest list."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_guest_list_string_items)
    assert "guest_family_ids" in str(exc_info.value)

def test_create_event_empty_guest_list(invalid_event_empty_guest_list):
    """Test creating an Event with empty guest list (should fail)."""   
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_empty_guest_list)
    assert "guest_family_ids" in str(exc_info.value)
 
def test_event_too_many_guests(invalid_event_too_many_guests):
    """Test guest_family_ids with 51 items (exceeds limit)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_too_many_guests)
    assert "guest_family_ids" in str(exc_info.value)

def test_event_host_in_guest_list(invalid_event_host_in_guest_list):
    """Test host_family_id in guest_family_ids (logical error)."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_host_in_guest_list)
    assert "Host family cannot be in the guest list" in str(exc_info.value)
 
def test_event_duplicate_guests(valid_event_duplicate_guests):
    """Test guest_family_ids with duplicates [2,3,2,4]."""
    event = Event.from_dict(valid_event_duplicate_guests)
    assert event.guest_family_ids == [2, 3, 2, 4]
    # Consider adding deduplication if needed
 
def test_event_negative_guest_ids(invalid_event_negative_guest_ids):
    """Test guest_family_ids with negative IDs [2, -1, 4]."""
    with pytest.raises(ValidationError) as exc_info:
        Event.from_dict(invalid_event_negative_guest_ids)
    assert "Guest family IDs must be positive" in str(exc_info.value)