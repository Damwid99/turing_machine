# Turing Machine Simulator


## Overview

  

This project is a Turing Machine simulator implemented in Python with a graphical user interface (GUI) using PyQt5.

  

## Table of Contents

  

- [Features](#features)

- [Getting Started](#getting-started)

- [Dependencies](#dependencies)

- [Installation](#installation)

- [Usage](#usage) 
	- [Graphical User Interface](#graphical-user-interface) 
	- [As a Python Library](#as-a-python-library)

- [File Format](#file-format)

- [Screenshots](#screenshots)

- [License](#license)

  

## Features

  

- Simulates Turing Machines with a user-friendly GUI.

- Supports step-by-step and continuous execution modes.

- Allows uploading Turing Machine configurations from text files.

- Displays the current state, tape content, and executed transitions.

- Provides a message box for additional information.

  

## Getting Started

  

To get started with the Turing Machine simulator, follow these steps:

  


### Prerequisites

- Python 3.x
- PyQt5 library and its dependencies:

 
### Installation

  

1. Clone the repository:

  

```bash

git clone https://github.com/Damwid99/turing_machine.git

```

  

2. Install dependencies:

  

```bash

pip install -r requirements.txt

```

 

### Usage

    
Certainly! Here's an updated section in the README.md file to include information about running the Turing Machine simulator through the console and using it as a Python library:

markdownCopy code

`# Turing Machine Simulator

## Overview

This project is a Turing Machine simulator implemented in Python with a graphical user interface (GUI) using PyQt5.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
 - [Graphical User Interface](#graphical-user-interface)
 - [Console](#console)
 - [As a Python Library](#as-a-python-library)
- [File Format](#file-format)
- [Screenshots](#screenshots)
- [License](#license)

## Features

- Simulates Turing Machines with a user-friendly GUI.
- Supports step-by-step and continuous execution modes.
- Allows uploading Turing Machine configurations from text files.
- Displays the current state, tape content, and executed transitions.
- Provides a message box for additional information.

## Getting Started

To get started with the Turing Machine simulator, follow these steps:

### Prerequisites

- Python 3.x
- PyQt5 library

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/turing-machine-simulator.git
   ``` 

2.  Install dependencies:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    

### Usage

#### Graphical User Interface

1. Run the application:

  

```bash
python .\turing-machine-simulator\main.py
```
2. Upload a Turing Machine configuration file using the "Upload file" button.

3. Start, pause, or step through the execution using the corresponding buttons.

4. View the tape content, current state, and transition details in the GUI.

#### As a Python Library

The Turing Machine simulator can also be used as a Python library. Import the `TuringMachine` class and use it programmatically in your Python scripts.
```python
from modules.turingMachine import TuringMachine
from utils.utils import render_txt

# Load Turing Machine configuration from a file
initial_word, states, final_states, initial_state, relations, tape_alphabet = render_txt('<path_to_configuration_file>')
turing_machine = TuringMachine(relations=relations, initial_state=initial_state, final_state=final_states, states=states, initial_word=initial_word)

# Perform custom operations or run the Turing Machine programmatically
turing_machine.run()
```

## File Format

  

The Turing Machine configuration file should follow a specific format:

  

```plaintext

slowo wejsciowe: <initial_word>

alfabet tasmowy: <tape_alphabet>

stany: <state_1> <state_2> ...

stany akceptujace: <accepting_state_1> <accepting_state_2> ...

stan poczatkowy: <initial_state>

relacja przejscia:

<state_1> <symbol_1> <next_state_1> <write_symbol_1> <direction_1>

<state_2> <symbol_2> <next_state_2> <write_symbol_2> <direction_2>

...

```
For example:
```
alfabet tasmowy:
abc#
alfabet wejsciowy:
a
slowo wejsciowe:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
stany:
1 2 3 4
stan poczatkowy:
1
stany akceptujace:
4
relacja przejscia:
1 a 2 b P
1 c 4 c L
2 a 2 a P
2 c 2 c P
2 # 3 c L
3 a 3 a L
3 c 3 c L
3 b 1 b P
```

  

## Screenshots

  

https://github.com/Damwid99/turing_machine/assets/119733924/cffabe00-4827-45e2-b07a-a078d9ec5f70


