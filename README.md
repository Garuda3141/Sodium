# Sodium
A Graph-Based Note Taker
# Sodium CLI

Sodium is a command-line tool designed to function as a **CLI-based Second Brain**. It enables users to create, manage, and analyze bidirectional note relationships within the command line. The tool allows note linking, searching, tagging, visualization, and graph-based analysis.

## Features
- **Note Management**: Create, open, and remove notes.
- **Graph Structure**: Link notes and view relationships.
- **Backlinking**: Find notes that reference a given note.
- **Search & Tagging**: Search notes and organize them with tags.
- **Graph Visualization**: Heatmaps, centrality analysis, and interactive visualization.
- **Persistent Storage**: Stores relationships in a designated home directory.

## Installation
```sh
git clone https://github.com/Garuda3141/sodium.git
cd sodium
pip install -r requirements.txt
```

## Usage
Run the CLI tool:
```sh
python main.py --help
```

### Example Commands
```sh
python main.py new "MyNote"   # Create a new note
python main.py open "MyNote"  # Open a note
python main.py link "Note1" "Note2"  # Create a bidirectional link
python main.py list "MyNote"  # List links in a note
python main.py backlinks "MyNote"  # Find backlinks
python main.py search "keyword"  # Search notes
python main.py tag "MyNote" "Project"  # Add a tag
python main.py tags  # List all tags
python main.py graph viz  # Visualize graph
python main.py init  # Scan and initialize notes directory
python main.py log "Meeting" "Discussed Sodium improvements"  # Create a log entry
```

## Configuration
Sodium uses environment variables stored in a `.env` file:
```sh
GRAPH_FILE=~/.sodium/graph.json
NOTES_DIR=/Users/sudarshan/Desktop/gg3141/code/projects/sodium/notes
EDITOR=subl
```

## File Structure
```
├── sodium_home/        # Persistent storage
├── notes/              # Graph-based note storage
├── main.py             # CLI entry point
├── graph.py            # Graph processing logic
├── analysis.py         # Markov analysis module
├── storage.py          # File storage management
├── .env                # Environment variable configuration
└── README.md           # Project documentation
```

## License
MIT License

