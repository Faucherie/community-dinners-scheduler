# User Guide for community_dinners

- [1. Introduction](#1-introduction)
    - [1.1 Purpose](#11-purpose)
    - [1.2 Key Concepts](#12-key-concepts)
    - [1.3 Problem Domain](#13-problem-domain)
      - [1.3.1 Primary Constraint](#131-primary-constraint)
- [2. Project Structure](#2-project-structure)
  - [2.1 Needed Files](#21-needed-files)
      - [Families](#families)
      - [Persons](#persons)
      - [Config](#config)
  - [2.2 Persisted application state](#22-persisted-application-state)
  - [2.3 Generated output](#23-generated-output)
  - [2.4 Example Datasets](#24-example-datasets)
- [3. Setup](#3-setup)
  - [3.1 Activate the virtual environment](#31-activate-the-virtual-environment)
  - [3.2 Run the CLI](#32-run-the-cli)
  - [3.3 Sturcture](#33-sturcture)
- [4. Workflow](#4-workflow)
  - [4.1 Data Commands](#41-data-commands)
      - [4.1.1 Check current state](#411-check-current-state)
      - [4.1.2 Load family and person data](#412-load-family-and-person-data)
  - [4.2 Configuration Commands](#42-configuration-commands)
    - [4.2.1 Load Configuration Setting from a JSON File](#421-load-configuration-setting-from-a-json-file)
    - [4.2.2 Create Congifuartion Setting Interactively](#422-create-congifuartion-setting-interactively)
    - [4.2.3 View Current Configuration](#423-view-current-configuration)
  - [4.3 Assignments Commands](#43-assignments-commands)
    - [4.3.1 Generate Assignments](#431-generate-assignments)
    - [4.3.2. View Assignment Statistics](#432-view-assignment-statistics)
  - [4.4 Recap](#44-recap)
    - [4.4.1 Command Table](#441-command-table)
    - [4.4.2 Example Flow](#442-example-flow)
- [5. Common Issues](#5-common-issues)
  - [5.1 Missing or Incomplete JSON State File](#51-missing-or-incomplete-json-state-file)
  - [5.2 Missing config](#52-missing-config)
  - [5.3 Missing families or persons](#53-missing-families-or-persons)
  - [5.4 Invalid JSON structure](#54-invalid-json-structure)
  - [5.5 Note on filename spelling](#55-note-on-filename-spelling)


## 1. Introduction

#### 1.1 Purpose

Community Dinners is a command-line tool for organizing dinner event assignments between families.

It lets you:

- **Load participant data**
- **Create or load event configuration**
- **Generate dinner assignments for a season**
- **View simple assignment statistics**

#### 1.2 Key Concepts

**Events**: Individual dinner gatherings consisting of:
- One host family
- Multiple guest families
- Dynamic group sizes based on host capacity

**Series**: Collections of events within a specific time period (typically one month)

**Season**: The complete program cycle containing all series for a given period


#### 1.3 Problem Domain

The Community Dinners tool automates the assignment of dinner events for a population of families predefined as hosts and guests. 

##### 1.3.1 Primary Constraint

The application is based on the **Social Golfer Problem**, a combinatorial scheduling challenge where a population of 32 golfers want to play in groups of 4 for 10 weeks without repeating partners. The original verage was, "so no two players should walk abreast." Which means that the groups of 4 are further constrained that no pairwise meeting should repeat, not just the unique quadruples. This applies to the dinner events as well - no two families should meet more than once throughout the season.

In this context:

- Each dinner event features one host family and multiple guest families
- A season consists of multiple series, each containing several events
- Families should not meet more than once throughout the season
- Dinner sizes vary based on each host's capacity

Unlike traditional implementations where event sizes are fixed, this solution takes a host-centric approach. Each family has unique hosting constraints:
- Maximum guest capacity differs by family
- Event sizes dynamically adapt to host capabilities

This design enables realistic dinner assignments that respect the practical limitations and varying capacities of participating families, making it a practical adaptation of the Social Golfer Problem for community dinner events.

**Source:** [Wolfram *Social Golfer Problem*](https://demonstrations.wolfram.com/SocialGolferProblem/)

## 2. Project Structure

The project is a **Python CLI** built with `click` and `pydantic`.

Main files:

- **cli.py**: Command-line interface using Click.

- **session.py**: Stores and loads app state from a json file.

- **assingments.py**: Generates event and series assignments

- **schema/**: Pydantic data models for families, persons, config, events, and series

```
project-root/
├── community_dinners/
│   ├── __init__.py
│   ├── cli.py
│   ├── session.py
│   ├── assingments.py
│   └── schema/
│       ├── __init__.py
│       ├── family.py
│       ├── person.py
│       ├── config.py
│       ├── event.py
│       └── series.py
```

### 2.1 Needed Files 

This application processes JSON files. It takes a directory containing two JSON files: `families.json` and `persons.json`, and then a configuration which can be provided as a JSON file or as command line arguments. Thus here is how the JSON files should be structured prior to running the application.

##### Families

The core data type this project works with is a family. Created as Pydantic models in `schema/family.py`:

- **`family_id`**: positive integer
- **`name`**: non-empty string
- **`address`**: non-empty string
- **`family_members`**: list of person IDs

Optional:

- **`max_guests`**
- **`can_host`**

The families file should contain an array of family objects with the following structure:

```
{
    "families":[
        {
            "family_id": int,
            "name": string,
            "address": string,
            "can_host": bool,
            "max_guests": int,
            "family_members": list[int]
        },
    ]
}
```

Where:

- `family_id`: Unique identifier for the family (required `int`)
- `name`: Family name (required `str`)
- `address`: Family address (required `str`)
- `can_host`: Whether the family can host dinners (required `bool`)
- `max_guests`: Maximum number of guests the family can host (required `Optional[int]`)
- `family_members`: Array of person IDs belonging to this family (required `List[int]`)


##### Persons

Persons while not fully implemented in the codebase, expand on the family data type. Each person is a member of a family and has additional attributes. A person may include:

- **`person_id`**
- **`first_name`**
- **`last_name`**
- **`family_id`**
- **`age`**
- **`kid`**
- **`phone`**
- **`email`**

The persons file should contain an array of person objects with the following structure:

```
{
    "persons": [
        {
            "person_id": int,
            "family_id": int,
            "first_name": string,
            "last_name": string,
            "age": int,
            "kid": bool,
            "phone": string,
            "email": string
        }
    ]
}
```

where:

- `family_id`: Unique identifier for their family (optional `int`)
- `person_id`: Unique identifier for the person (required `int`)
- `first_name`: Person's first name (required `str`)
- `last_name`: Person's last name (required `str`)
- `age`: Person's age (optional `int`)
- `kid`: Whether the person is a kid (optional `bool`)
- `phone`: Person's phone number (optional `str`)
- `email`: Person's email address (optional `str`)

##### Config

The assignment generation process requires configuration of three key parameters:

- **Group size**: The global scope target number of families per dinner event
    - Sets the default group size for each series if not specified otherwise by the host of that event.
- **Events per series**: Number of dinner events within each series (time period)
    
- **Series count**: Number of series that make up the complete season

Each event represents a single dinner assignment. Events are grouped into series (typically monthly periods), and the collection of all series forms the complete season.

The config requires:

- **`group_size`**: greater than 1
- **`events_per_series`**: greater than 0
- **`series_count`**: greater than 0

The config file can be input via command line argument or by loading in a file. The file should contain the following structure:

```
{
    "group_size": int,
    "events_per_series": int,
    "series_count": int
}
```

### 2.2 Persisted application state

As this application is a command-line tool, the state is persisted in a JSON file.

Use the `load` commands in the CLI for both the data (families and persons) and the config. This copies the data into the state file. Which allows for later assignment generation.

- **state.json**: Is where data and config information is stored.

This file is not input by the user like the families and persons files, but is created and managed by the application.

### 2.3 Generated output

After successful assignment generation, the following assingments for the season are save to the assingments file:
- **assingments.json**: Stores assingments for the season

The assingments are broken into events and series.

**Events**: Individual dinner assignments.

```json
"events": [
    {
      "event_id": 1,
      "host_family_id": 4,
      "guest_family_ids": [
        5,
        9,
        6,
        10,
        7
      ]
    }
]
```
Where:
- `event_id`: Unique identifier for the event.
- `host_family_id`: Unique identifier for the host family of the event.
- `guest_family_ids`: List of unique identifiers for the guest families at the event.

**Series**: Groups of events that occur together.

```json
"series": [
    {
      "series_id": 1,
      "event_ids": [
        1,
        2
      ]
    }
  ]
```

Where:
- `series_id`: Unique identifier for the series.
- `event_ids`: List of unique identifiers for the events in the series.

This is the final product of the assignment generation process. It is saved to the `assingments.json` file. 
 
### 2.4 Example Datasets

The application comes with example data files in the `example_data` directory.

```
project-root/
├── community_dinners/
├── example_data/
│   ├── 4f12p/
│   │   ├── families.csv
│   │   ├── persons.csv
│   │   └── config.json
│   ├── 6f12p/
│   │   ├── families.csv
│   │   ├── persons.csv
│   │   └── config.json
│   └── 6f12p-max_guests/
│       ├── families.csv
│       ├── persons.csv
│       └── config.json
```

The datasets contain toy data for testing the application. They are not meant to be used in production. But looking at them will help you understand the structure for your data.

I will use `6f12p-max_guests` as the example dataset for rest of the documentation.

## 3. Setup

This application runs as a Click-based command-line interface (CLI).

The principles of the CLI are:
1. **Arbitrary nesting of commands**: The application can have multiple levels of commands and subcommands. So only the commands relevant to the current context are shown.
2. **Automatic help generation**: For each command their are automated help messages that are generated from the command's docstring. These help if the user needs to know more about the command.

### 3.1 Activate the virtual environment

From the project root, before running the CLI, activate the virtual environment:

```bash
source venv/bin/activate
```

### 3.2 Run the CLI

From the project root, run the CLI through the main entry point:

```bash
python3 -m community_dinners.cli
```

- Output:
    ```
    Usage: python -m community_dinners.cli [OPTIONS] COMMAND [ARGS]...

      Entry point for the CLI.

    Options:
      --help  Show this message and exit.

    Commands:
      assignments  Assignments commands.
      config       Configuration commands.
      data         Data commands.
    ```

### 3.3 Sturcture

The CLI is structured as follows:

- **`data`**: Commands for loading and managing family and person data
- **`config`**: Commands for loading and managing configuration
- **`assignments`**: Commands for generating and managing dinner assignments

```
cli
├── data
├── config
└── assignments
```

By calling the subcommands you can navigate through the CLI and reveals more subcommands where you can perform the desired actions.

## 4. Workflow

Before running assingments commands, you must first load the family and person data and then set the configuration settings you desire for the assignments.

### 4.1 Data Commands

`cli.data`

The first subcommand is `data` which is used to load and manage family and person data. 

There are two main subcommands under `data`:
- `get-state`: Print the state file
- `load`: Load family and person data from a folder
- `summary`: Print a summary of the loaded data (not implemented yet)

##### 4.1.1 Check current state

`cli.data.get-state()`

This cammand gets the current state of the application and prints it to the console. Which allows the user to see what data has been loaded and what the data is.

**Usage:**
  ```bash
  python -m community_dinners.cli data get-state
  ```

**Example:**

The following example shows the output when no data has been loaded:

- Output:
  ```
  Welcome to Community Dinners!
  === Current State ===
  Families: 0
  Persons: 0
  ```

Once you've verified the state contains the correct data, proceed to configure the assignment settings. Alternatively, like in the above output where there are 0 families and 0 persons, you can load data by running the `load` command.

**Note:** The state file is stored in `data/state.json` and is automatically loaded when the CLI starts.

##### 4.1.2 Load family and person data

`cli.data.load()`

Prior to uploading your own data, you should familiarize yourself with the format of the data. The data should be in the form of two json files, `families.json` and `persons.json`. The format of these files is described in the [section 2.1 Needed Files](#21-needed-files).

To load data into the application, use the `load` subcommand in the `data` group:

**Usage:**
```bash
python -m community_dinners.cli data load /path/to/data-folder
```

What it does:

- **Reads** `families.json` and `persons.json`
- **Validates** records with Pydantic models
- **Prints** a summary of loaded families
- **Asks for confirmation**
- **Saves** the data into state.json

You will be prompted:

```text
Do you accept this data?
```

If you select "yes" (`Y`, `y`, or press Enter), the state file is updated. Otherwise, the process is aborted. 

You can verify that the state file was updated by running the `get-state` command as explained in [4.1.1 Check current state](#411-check-current-state).

**Note**: Loading data will overwrite any existing data in the state file.

**Example:**
```bash
python3 -m community_dinners.cli data load example_data/10f36p-max_guests
```

- Output:

```
Welcome to Community Dinners!

=== Dataset Summary ===
Families: 10
Persons:  36

=== Families ===
  [1] Doe [host] - 1 address, example, AA 12345 (members: [1, 2, 3])
  [2] Smith [host] - 2 address, example, BB 12345 (members: [4, 5, 6, 7])
  [3] Price - 3 address, example, CC 12345 (members: [8, 9])
  [4] Bridger [host] - 4 address, example, DD 12345 (members: [10, 11, 12])
  [5] Johnson - 5 address, example, EE 12345 (members: [13, 14, 15, 16, 17])
  [6] Williams - 6 address, example, FF 12345 (members: [18, 19, 20, 21])
  [7] Brown - 7 address, example, GG 12345 (members: [22, 23, 24])
  [8] Davis - 8 address, example, HH 12345 (members: [25, 26, 27, 28, 29])
  [9] Miller - 9 address, example, II 12345 (members: [30, 31, 32, 33])
  [10] Wilson - 10 address, example, JJ 12345 (members: [34, 35, 36])
Do you accept this data? [Y/n]: 

>>> Y

Data loaded and saved to state file.
```

### 4.2 Configuration Commands

`cli.config`

Configuration is the settings for the assingment. How many events do you want to schedule?

$$
\text{Total events in a season} = k_{\text{series}} \times j_{\text{events per series}}
$$

A series could be a month, a quarter, or any other time period that you want to group events by.

Unlike the data, their are two methods for creating a configuration:
1. Load from a file
2. Create interactively

Both methods end in the same result, so choose the one that you find more convenient. I prefer the interactive method because it is more user-friendly. 

**Config command help**:
```
python -m community_dinners.cli config --help
```

- Output:
```
Welcome to Community Dinners!
Usage: python -m community_dinners.cli config [OPTIONS] COMMAND [ARGS]...

  Configuration commands.

Options:
  --help  Show this message and exit.

Commands:
  create      Create config and print summary.
  get-config  Print the config file.
  load        Load config and print summary.
```

#### 4.2.1 Load Configuration Setting from a JSON File

`cli.config.load()`

To load the configuration setting from a premade json file, ensure the file is in the correct format. Refer to [Section 2.1 Needed files](#21-needed-files) for the required format.


**Usage:**

```bash
python -m community_dinners.cli config load /path/to/config.json
```

What it does:

- **Reads** a config JSON file
- **Validates** it
- **Prints** a summary
- **Asks for confirmation**
- **Saves** the config to state.json

After confirmation, the config is saved to `community_dinners/state.json`

**Note**: The config is saved to `community_dinners/state.json`, not to the file you loaded from, and overwrites any existing config settings in the state file.

**Example:**

```bash
python -m community_dinners.cli config load example_data/10f36p-max_guests/config.json
```

- Output:
    ```text
    Welcome to Community Dinners!

    === Configuration Summary ===
    Group size: 4
    Events per series: 3
    Series count: 4
    Do you accept this configuration? [Y/n]: 
    >>> Y
    ```



#### 4.2.2 Create Congifuartion Setting Interactively

`cli.config.create()`

Instead of loading a config file, you can create one interactively by answering prompts.

**Usage:**
```bash
python -m community_dinners.cli config create
```

What it does:

- **Prompts** for group size, events per series, and series count
- **Validates** the input
- **Prints** a summary
- **Asks for confirmation**
- **Saves** it to [community_dinners/state.json](cci:7://file:///home/scott-swanson/projects/Agile_final/community_dinners/state.json:0:0-0:0)

**Note**: The config is saved to `community_dinners/state.json`, overwriting any existing config settings in the state file.

After confirmation, the config is saved to `community_dinners/state.json`.

**Example:**

```bash
python -m community_dinners.cli config create
```

- Output:
```
Welcome to Community Dinners!

=== Configuration Summary ===
Group size: 
>>> 4
Events per series: 
>>> 4
Series count: 
>>> 3
Do you accept this configuration? [Y/n]: 
>>> Y
```

#### 4.2.3 View Current Configuration

`cli.config.get_config()`

To confirm the current configuration, you can view it using the `get-config` command.

**Usage:**

```bash
python -m community_dinners.cli config get-config
```

What it shows:

- **Group size**
- **Events per series**
- **Series count**

**Example:**

```bash
python -m community_dinners.cli config get-config
```

- Output:
```
Welcome to Community Dinners!

=== Configuration Summary ===
Group size: 4
Events per series: 3
Series count: 4
```

### 4.3 Assignments Commands

`cli.assignments`

If you have loaded data and configuration, you can now generate assignments.

#### 4.3.1 Generate Assignments

`cli.assignments.generate()`


The current assignment generation uses a random selection approach with validation to ensure novel dining pairs. The process works as follows:

1. **Host Selection**: Randomly selects a host family from those that have volunteered to host
2. **Guest Selection**: Randomly selects guest families up to either:
   - The group size specified in configuration, or
   - The host's maximum guest capacity (if specified)
3. **Validation**: Checks that all family pairs in the proposed dinner have not dined together before
4. **Retry Logic**: If any pairs have met previously, the algorithm attempts to generate a new valid combination
5. **Fallback**: After multiple failed attempts, the system skips that dinner and moves to the next one

This means some dinners may remain unassigned if valid combinations cannot be found within the attempt limit. Future versions will implement more sophisticated assignment algorithms.

**Usage:**

```bash
python -m community_dinners.cli assignments generate
```

Before generating, the CLI checks that:

- **Config exists**
- **Families exist**
- **Persons exist**

If valid, it shows a summary and asks if you want to proceed.

If confirmed, it generates the series and events, and writes the results to `assignments.json`.

**Example:**
```bash
python -m community_dinners.cli assignments generate
```

- Output:
    ```
    Welcome to Community Dinners!

    === Configuration ===
    Group size: 4 families per event
    Events per series: 3
    Series count: 4
    Total events to generate: 12

    Proceed with generation? [y/N]: 
    >>> Y

    Generating season...
    Generating 4 series with 3 events each...
    Created event 1 using pairs: [(4, 8), (4, 7), (3, 4), (7, 8), (3, 8), (3, 7)]
    Created event 2 using pairs: [(4, 6), (4, 5), (4, 10), (5, 6), (6, 10), (5, 10)]
    Created event 3 using pairs: [(1, 8), (1, 5), (5, 8)]
    Created event 4 using pairs: [(2, 10), (2, 9), (2, 8), (9, 10), (8, 10), (8, 9)]
    Created event 5 using pairs: [(1, 9), (1, 3), (3, 9)]
    Created event 6 using pairs: [(1, 10), (1, 7), (7, 10)]
    Could not create unique event 7
    Failed to create event 7 for series 3
    Could not create unique event 10
    Failed to create event 10 for series 4

    === Generation Complete ===
    Generated 4 series with 6 total events

    Assignments saved to: community_dinners/assingments.json
    ```

Here we can that from the config setting that we need to generate 12 total events. However, the algorithm could only find valid combinations for 6 events, so only 6 events were generated. The remaining events could not be created because the algorithm could not find valid combinations for them.

This failure is due to the algorithm's limitations and the constraints of the problem. Future versions will implement more sophisticated assignment algorithms to handle these edge cases.

#### 4.3.2. View Assignment Statistics

`cli.assignments.stats()`

After generating assignments, you can inspect the statistics about the assignments.

**Usage:**

```bash
python -m community_dinners.cli assignments stats
```

What it shows:

- **Total events**
- **Total series**
- **Events per series**
- **Host frequency by family**

**Example**
- Output:
  
    ```
    Welcome to Community Dinners!

    === Assignment Statistics ===
    Total events: 6
    Total series: 4
    Events per series: [3, 3, 0, 0]

    Host frequency:
      Family 1: 3 times
      Family 2: 1 times
      Family 4: 2 times
    ```

### 4.4 Recap

This is a summary of the assignments commands. With an example flow of generating assignments and viewing statistics.

#### 4.4.1 Command Table

| Command | Description |
| --- | --- |
| `python -m community_dinners.cli` | Show the main CLI entry point and available command groups |
| `python -m community_dinners.cli data load /path/to/data-folder` | Load [families.json](cci:7://file:///home/scott-swanson/projects/Agile_final/example_data/10f36p-max_guests/families.json:0:0-0:0) and `persons.json` into application state |
| `python -m community_dinners.cli data summary` | Reserved for a future data summary command; currently not implemented |
| `python -m community_dinners.cli data get-state` | Show how many families and persons are currently loaded |
| `python -m community_dinners.cli config load /path/to/config.json` | Load configuration from a JSON file |
| `python -m community_dinners.cli config create` | Create configuration interactively |
| `python -m community_dinners.cli config get-config` | Show the current saved configuration |
| `python -m community_dinners.cli assignments generate` | Generate season assignments and save them |
| `python -m community_dinners.cli assignments generate --verbose` | Generate assignments with the optional verbose flag |
| `python -m community_dinners.cli assignments stats` | Show statistics for generated assignments |

#### 4.4.2 Example Flow

 
1. Load data:
   ```bash
   python -m community_dinners.cli data load example_data/10f36p-max_guests
   ```
2. Check state:
   ```bash
   python -m community_dinners.cli data get-state
   ```
3. Create config:
   ```bash
   python -m community_dinners.cli config create
   ```
4. Verify config:
   ```bash
   python -m community_dinners.cli config get-config
   ```
5. Generate assignments:
   ```bash
   python -m community_dinners.cli assignments generate
   ```
6. View stats:
   ```bash
   python -m community_dinners.cli assignments stats
   ```


## 5. Common Issues

### 5.1 Missing or Incomplete JSON State File

If the state.json file is missing, empty, or malformed, commands that read application state may fail.

One common error occurs when the file exists but contains no JSON data at all. In that case, the CLI attempts to read the file and raises a `JSONDecodeError` because an empty file is not valid JSON.

To fix this, ensure that the state.json file contains valid JSON. If you want to start with an empty state file, use:

```json
{

}
```

### 5.2 Missing config

If you try to generate assignments without a config, the CLI prints an error.

```
Welcome to Community Dinners!
Error: No configuration found. Please run 'cli config create' or 'cli config load' first.
```

I have at least handled this error correctly and provided a helpful message to the user. If you arrive at this error, you need to load a config setting via `cli config load` or create a new one with `cli config create`. Then you can proceed with assignment generation.

### 5.3 Missing families or persons

If no participant data has been loaded, assignment generation will not run. Like with missing config, this error is handled gracefully and provides a helpful message to the user.

```
Welcome to Community Dinners!
Error: No families or persons data found. Please run 'cli data load' first.
```

If you encounter this error, you need to load participant data via `cli data load` before generating assignments.

### 5.4 Invalid JSON structure

The `data load` command requires a data directory with both [families.json] and `persons.json`.

Expected directory structure:

```text
input_file_root/
├── families.json
└── persons.json
```

Expected JSON structure:

```json
{
  "families": [...]
}
```

```json
{
  "persons": [...]
}
```

If a file is missing, contains invalid JSON, or does not use the expected top-level key, the data loader will fail. 

This is not handled gracefully and will raise an exception.


### 5.5 Note on filename spelling

The project currently uses:

- **`assingments.py`**
- **`assingments.json`**

This appears to be a misspelling of “assignments,” but the guide should match the code as it exists today. If I fix this I will need to update all references to these files throughout the codebase.
