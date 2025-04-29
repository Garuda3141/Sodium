# Sodium  
A Graph-Based Knowledge Management System by Sudharshan K.

Sodium is a command-line and web-based note-taking system designed to function as a **Second Brain**. It enables users to create, manage, and analyze bidirectional note relationships. Notes are stored as Markdown files, with backlinks, tags, and graph-based visualizations to help connect and resurface knowledge.

---

## 🔧 Features

- **Note Management**: Create, view, edit, and delete notes.
- **Graph Structure**: Link notes together to form a connected knowledge web.
- **Backlinking**: Identify notes that reference the current one.
- **Search & Tagging**: Organize and retrieve notes via keyword search and tags.
- **Logs**: Quickly store short, timestamp-free entries (like scratch notes).
- **Graph Visualization**: Visualize structure via heatmaps, centrality maps, and node graphs.
- **Persistent JSON Graph**: All note metadata is stored in a single graph file.
- **Web Interface**: Fast, clean interface for browsing, editing, linking, tagging, and logging notes.

---

## 📦 Installation

```bash
git clone https://github.com/Garuda3141/sodium.git
cd sodium
pip install -r requirements.txt
```

Ensure you have a `.env` file for configuration (see below).

---

## 🖥️ CLI Usage

Run the CLI tool from the root directory:

```bash
python main.py --help
```

### Example Commands

```bash
python main.py new "MyNote"                 # Create a new note
python main.py open "MyNote"               # Open note in editor
python main.py link "Note1" "Note2"        # Link two notes
python main.py list "MyNote"               # List links in a note
python main.py backlinks "MyNote"          # Find notes that link to this note
python main.py search "keyword"            # Search all notes
python main.py tag "MyNote" "Philosophy"   # Add a tag
python main.py tags                        # List all tags
python main.py graph viz                   # Visualize graph
python main.py init                        # Initialize graph from `notes/`
python main.py log "Title" "Content"       # Add a log entry
```

---

## 🌐 Web Interface

You can also launch a lightweight Flask-powered web UI:

```bash
python server.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Web Features

- **Dashboard**: View all notes, tags, and recent logs.
- **Note Viewer**: Render content, backlinks, and tags.
- **Edit Notes**: Update contents in the browser.
- **Create/Delete Notes**: Fully CRUD enabled.
- **Linker**: Link notes via dropdowns.
- **Tag Manager**: Add and view tags.
- **Log Console**: Record small notes/logs separately from full notes.
- **Search Bar**: Instant search through note content.
- **Graph Modes**: Explore visualizations via `/graph/viz`, `/graph/cen`, `/graph/hmap`.

---

## ⚙️ Configuration

Sodium uses a `.env` file for basic settings:

```env
GRAPH_FILE=~/.sodium/graph.json
NOTES_DIR=/Users/sudarshan/Desktop/gg3141/code/projects/sodium/notes
EDITOR=subl  # or code, vim, nano, etc.
```

---

## 📁 File Structure

```
├── notes/              # Folder containing all .na.md notes
├── templates/          # HTML templates for the web UI
├── static/             # CSS and JS assets
├── main.py             # CLI entry point
├── server.py           # Web interface (Flask app)
├── graph.py            # Graph data structure and operations
├── analysis.py         # Graph analysis & visualization
├── storage.py          # File & note handling
├── .env                # Configuration file
└── README.md           # Project documentation
```

---

## 📜 License

MIT License — Use freely, attribute fairly.
