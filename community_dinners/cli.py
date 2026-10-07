"""
Command-line interface for Community Dinners.
"""

import click
import json
from community_dinners.loader import load_dataset, load_dict
from community_dinners.schema import Family, Person, Config
from community_dinners.session import Session
from community_dinners.assingments import EventGenerationEngine, SeasonManager 

# cli entry point
"""
Structure of CLI
cli
├── data
├── config
└── assignments
"""
@click.group()
def cli():
    """Entry point for the CLI."""
    click.echo("Welcome to Community Dinners!")
    pass

# Subgroup 1: `data` for Data commands

"""
Data commands

Structure of Data commands
cli
├── data
│   ├── load (takes folder path as argument returns families and persons objects)
│   ├── summary (...nothing yet)
│   └── get_state (loads state file and prints it)
"""
@cli.group()
def data():
    """Data commands."""
    pass

"""
Load command for loading toy dataset
- Takes folder path as argument
    - Assumes two files: families.csv and persons.csv
- Loads families and persons from the folder
- Returns families and persons objects
"""
@data.command()
@click.argument('data_path', type=click.Path(exists=True))
def load(data_path):
    """Load toy dataset and print summary."""
    # load raw data from loader
    data_families, data_persons = load_dataset(data_path)
 
    # create objects using schema methods
    families = Family.from_list(data_families)
    persons = Person.from_list(data_persons)
 
    # print summary of loaded data
    click.echo(f"\n=== Dataset Summary ===")
    click.echo(f"Families: {len(families)}")
    click.echo(f"Persons:  {len(persons)}")
    
    click.echo(f"\n=== Families ===")
    for f in families:
        host_tag = " [host]" if f.can_host else ""
        click.echo(f"  [{f.family_id}] {f.name}{host_tag} - {f.address} (members: {f.family_members})")
    
    # check if the user accepts the data
    click.confirm("Do you accept this data?", default=True, abort=True)
    
    # save data to state file
    session = Session()
    session.update_families(families)
    session.update_persons(persons)
    
    click.echo("Data loaded and saved to state file.")

"""
Print summary of data
- Takes families and persons objects as arguments
- Prints summary of data
"""
@data.command()
def summary():
    """Print summary of data from state file."""


@data.command()
def get_state():
    """Print the state file."""
    session = Session()
    session.load_families()
    session.load_persons()

    # Print summary
    click.echo("=== Current State ===")
    click.echo(f"Families: {len(session.families)}")
    click.echo(f"Persons: {len(session.persons)}")


# Subgroup 2: `config` for configuration commands

"""
Configuration commands

Structure of Configuration commands
cli
├── config
│   ├── load (takes folder path as argument returns config object)
│   ├── create (creates a new config object)

"""
@cli.group()
def config():
    """Configuration commands."""
    pass

"""
Load command for loading config
- Takes folder path as argument
    - Assumes file: config.json
- Loads config from the folder
- Returns config object
"""
@config.command()
@click.argument('data_path', type=click.Path(exists=True))
def load(data_path):
    """Load config and print summary."""
    # load raw data from loader
    data_config = load_dict(data_path)
 
    # create objects using schema methods
    config = Config.from_dict(data_config)
 
    # print summary of loaded data
    click.echo(f"\n=== Configuration Summary ===")
    click.echo(f"Group size: {config.group_size}")
    click.echo(f"Events per series: {config.events_per_series}")
    click.echo(f"Series count: {config.series_count}")

    # check if the user accepts the configuration
    click.confirm("Do you accept this configuration?", default=True, abort=True)
     
    session = Session()
    session.update_config(config)

@config.command()
def create():
    """Create config and print summary."""

    # get configuration from user
    group_size = click.prompt("Group size", type=int)
    events_per_series = click.prompt("Events per series", type=int)
    series_count = click.prompt("Series count", type=int)
    
    # print summary of configuration
    click.echo(f"\n=== Configuration Summary ===")
    click.echo(f"Group size: {group_size}")
    click.echo(f"Events per series: {events_per_series}")
    click.echo(f"Series count: {series_count}")
    
    # check if the user accepts the configuration
    click.confirm("Do you accept this configuration?", default=True, abort=True)
 

    try:
        # create config object
        config = Config(
            group_size=group_size,
            events_per_series=events_per_series,
            series_count=series_count
        )
    except Exception as e:
        click.echo(f"Error creating config: {e}", err=True)
        return
    
    
    # save config to session
    session = Session()
    session.update_config(config)
    click.echo("Config saved successfully!")

@config.command()
def get_config():
    """Print the config file."""
    session = Session()
    session.load_state()
 
    if not session.config:
        click.echo("No config found. Run 'config create' or 'config load' first.", err=True)
        return
 
    click.echo("=== Current Config ===")
    click.echo(f"Group size: {session.config.group_size}")
    click.echo(f"Events per series: {session.config.events_per_series}")
    click.echo(f"Series count: {session.config.series_count}")

"""
Assignments commands

Structure of Assignments commands
cli
├── assignments
│   ├── generate (generates assignments)
"""
@cli.group()
def assignments():
    """Assignments commands."""
    pass

# Update the assignments generate command
@assignments.command()
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def generate(verbose):
    """Generate a full season of assignments."""
    # Load session data
    session = Session()
    session.load_state()
    
    # Verify we have the required data
    if not session.config:
        click.echo("Error: No configuration found. Please run 'cli config create' or 'cli config load' first.", err=True)
        return
    
    if not session.families or not session.persons:
        click.echo("Error: No families or persons data found. Please run 'cli data load' first.", err=True)
        return
    
    # Show configuration summary
    click.echo(f"\n=== Configuration ===")
    click.echo(f"Group size: {session.config.group_size} families per event")
    click.echo(f"Events per series: {session.config.events_per_series}")
    click.echo(f"Series count: {session.config.series_count}")
    click.echo(f"Total events to generate: {session.config.series_count * session.config.events_per_series}")
    
    # Confirm before generating
    if not click.confirm("\nProceed with generation?"):
        click.echo("Generation cancelled.")
        return
    
    # Create season and generate
    click.echo(f"\nGenerating season...")
    season = SeasonManager(session, session.config.series_count)
    season.generate_season()
    
    # Save assignments
    season.save_season()
    
    # Show generation complete
    click.echo(f"\n=== Generation Complete ===")
    click.echo(f"Generated {len(season.series_list)} series with {len(season.events)} total events")
    
    click.echo(f"\nAssignments saved to: community_dinners/assingments.json")
 
@assignments.command()
def stats():
    """Show statistics about generated assignments."""
    try:
        with open("community_dinners/assingments.json", 'r') as f:
            data = json.load(f)
        
        events = data.get('events', [])
        series = data.get('series', [])
        
        click.echo(f"\n=== Assignment Statistics ===")
        click.echo(f"Total events: {len(events)}")
        click.echo(f"Total series: {len(series)}")
        
        if series:
            events_per_series = [len(s['event_ids']) for s in series]
            click.echo(f"Events per series: {events_per_series}")
        
        if events:
            # Count host frequency
            host_count = {}
            for event in events:
                host = event['host_family_id']
                host_count[host] = host_count.get(host, 0) + 1
            
            click.echo(f"\nHost frequency:")
            for host_id, count in sorted(host_count.items()):
                click.echo(f"  Family {host_id}: {count} times")
                
    except FileNotFoundError:
        click.echo("No assignments file found. Run 'assignments generate' first.", err=True)
    except json.JSONDecodeError:
        click.echo("Error reading assignments file.", err=True)

if __name__ == '__main__':
    cli()