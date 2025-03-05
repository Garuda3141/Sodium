import argparse
import os
from graph import Graph
import subprocess
import storage
from dotenv import load_dotenv
import analysis
# Load .env variables
load_dotenv()

# Use environment variables
GRAPH_FILE = os.getenv("GRAPH_FILE", os.path.expanduser("~/.sodium/graph.json"))
NOTES_DIR = os.getenv("NOTES_DIR", "/Users/sudarshan/Desktop/gg3141/code/projects/sodium/notes")
DEFAULT_EDITOR = os.getenv("EDITOR", "subl")

# Initialize graph
graph = Graph(GRAPH_FILE, NOTES_DIR)

def main():
    parser = argparse.ArgumentParser(description="Sodium CLI - CLI-based Second-Brain")
    subparsers = parser.add_subparsers(dest="command")

    open_parser = subparsers.add_parser("open", help="Open a note in the editor")
    open_parser.add_argument("title")
    # Create a new note
    new_parser = subparsers.add_parser("new", help="Create a new note")
    new_parser.add_argument("title")

    remove_parser = subparsers.add_parser("remove", help="Remove a note and the associated links and tags")
    remove_parser.add_argument("title")

    # Link two notes
    link_parser = subparsers.add_parser("link", help="Create a bidirectional link")
    link_parser.add_argument("note1")
    link_parser.add_argument("note2")

    # List links in a note
    list_parser = subparsers.add_parser("list", help="List links in a note")
    list_parser.add_argument("note")

    # Show backlinks
    backlinks_parser = subparsers.add_parser("backlinks", help="Find notes linking to a given note")
    backlinks_parser.add_argument("note")

    # Search notes
    search_parser = subparsers.add_parser("search", help="Search for a keyword")
    search_parser.add_argument("query")

    # Tag a note
    tag_parser = subparsers.add_parser("tag", help="Add a tag to a note")
    tag_parser.add_argument("note")
    tag_parser.add_argument("tag")

    # List tags
    subparsers.add_parser("tags", help="List all tags and associated notes")

    # Visualize graph
    graph_parser = subparsers.add_parser("graph", help="Visualize note relationships")
    graph_parser.add_argument(
    "flag", choices=["hmap", "cen", "viz"], help="Choose: 'hmap' for heatmap, 'cen' for centrality, 'viz' for graph visualization"
    )

    subparsers.add_parser("init", help="Scan notes directory and add new notes to the graph")
    log_parser = subparsers.add_parser("log", help="Create mono logs")
    log_parser.add_argument("title", help="Title of the log")
    log_parser.add_argument("log", help="Log text")
    args = parser.parse_args()

    if args.command == "new":
        graph.create_note(args.title)
    elif args.command == "open":
        storage.open_note(args.title)
    elif args.command == "link":
        graph.create_link(args.note1, args.note2)
    elif args.command == "list":
        graph.list_links(args.note)
    elif args.command == "backlinks":
        graph.list_backlinks(args.note)
    elif args.command == "search":
        graph.search_notes(args.query)
    elif args.command == "tag":
        graph.add_tag(args.note, args.tag)
    elif args.command == "tags":
        graph.list_tags()
    elif args.command == "graph":
        analysis.analyse(GRAPH_FILE, args.flag)
    elif args.command == "init":
        graph.init_graph()
    elif args.command == "remove":
        graph.remove_note(args.title)
    elif args.command == "log":
        storage.log_entry(GRAPH_FILE, args.title, args.log)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
