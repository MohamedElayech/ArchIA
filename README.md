# ArchIA : Design and Developement Project

This project is a toolset for modeling, processing, and visualizing architectural concepts from natural language inputs. It converts user-provided architecture-related descriptions into structured models and generates Draw.io and Archimate diagrams automatically.

The system uses:

- **Flask** to expose an API
- **OpenAI** for semantic understanding
- **NetworkX** for internal graph modeling
- **Graphviz** to generate Draw.io-compatible visuals

---

## Purpose

The project allows users to input architectural ideas in plain text, and get back structured diagrams showing Stakeholders, Goals, Principles, Constraints, and more, automatically laid out in Draw.io or archimate.

---

## Setup Instructions

Please follow these steps to install and run the project.

#### Environment Variables

To run the project, you must set your OpenAI API key as an environment variable

#### Install Dependencies

This project requires both **Python** and **Java** to be installed.

##### Install Python

Download and install Python 3.8 or later from the [official Python website](https://www.python.org/downloads/).

Verify installation:

```bash
python --version
```

##### Install Java

Java is required for Graphviz to work correctly with Draw.io exports.

Download and install the Java JDK from the Oracle website

### Running the Back-end

#### Create and Activate Python Virtual Environment

To isolate dependencies, create a Python virtual environment inside the `flask` folder.

1. Navigate to the `flask` directory:

```bash
cd flask
```

2. Create a virtual environment:

```bash
python -m venv env
```

3. Activate the virtual envirement :

```bash
env\Scripts\activate
```

#### Install Python Dependencies

Once the virtual environment is active, run:

```
pip install flask
pip install openai
pip install networkx graphviz
```

### Install Graphviz (Required)
Graphviz is needed to generate the Draw.io-compatible diagrams.

▶️ Windows
Download the installer from:
--> https://graphviz.org/download/

Install it using the default settings.
Make sure "Add Graphviz to the system PATH" is checked.

After installation, open Command Prompt and run:

dot -V
You should see something like:
dot - graphviz version 2.49.0

If not recognized, add this path to your system's environment variables:
C:\Program Files\Graphviz\bin

Then restart your terminal.

▶️ macOS

brew install graphviz

▶️ Linux (Ubuntu/Debian)

sudo apt update  
sudo apt install graphviz

Verify installation:

dot -V


#### Run flask code

```bash
python app.py
```
#### Navigate to the `drawio` directory:

```bash
cd drawio
```

#### Run flask code

```bash
python app.py
```

### Running the user interface

#### Navigate to the `interface` directory:

```bash
cd interface
```


#### install npm

```bash
npm install
```

#### Running the front-end code

```bash
npm run dev
```
