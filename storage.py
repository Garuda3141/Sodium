from graph import Graph
from dotenv import load_dotenv
import os
import subprocess
import json

# Load .env variables
load_dotenv()

# Use environment variables
GRAPH_FILE = os.getenv("GRAPH_FILE", os.path.expanduser("~/.sodium/graph.json"))
NOTES_DIR = os.getenv("NOTES_DIR", "notes/")
DEFAULT_EDITOR = os.getenv("EDITOR", "nvim")

graph = Graph(GRAPH_FILE, NOTES_DIR)

def open_note(title):
    """Opens the note in the default editor."""
    if title not in graph.graph["notes"]:
        print(f"Note '{title}' does not exist.")
        return

    note_path = graph.graph["notes"][title]
    subprocess.run([DEFAULT_EDITOR, note_path])

def log_entry(graph_file, title, log_text):
    """Save a log entry in graph.json."""
    
    # Load existing data
    if os.path.exists(graph_file):
        with open(graph_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    
    # Ensure logs section exists
    if "logs" not in data:
        data["logs"] = {}
    
    # Save the log entry
    data["logs"][title] = log_text
    
    # Write back to the JSON file
    with open(graph_file, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Log saved: {title}")
