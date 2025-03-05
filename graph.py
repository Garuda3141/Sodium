import os
import json
import re

class Graph:
    def __init__(self, storage_file, notes_dir):
        self.storage_file = storage_file
        self.notes_dir = notes_dir
        os.makedirs(self.notes_dir, exist_ok=True)
        self.graph = self.load_graph()

    def load_graph(self):
        """Load graph from storage file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):  # ✅ Ensure it's a dictionary
                    data = {"notes": {}, "links": {}, "tags": {}}
                return data
        return {"notes": {}, "links": {}, "tags": {}}


    def save_graph(self):
        """Save graph to file."""
        with open(self.storage_file, "w") as f:
            json.dump(self.graph, f, indent=4)

    def create_note(self, title):
        """Create a new note."""
        note_path = os.path.join(self.notes_dir, f"{title}.na.md")
        if os.path.exists(note_path):
            print(f"Note {title} already exists.")
            return

        with open(note_path, "w") as f:
            f.write(f"# {title}\n\n")
        self.graph["notes"][title] = note_path
        self.save_graph()
        print(f"Note '{title}' created.")

    def create_link(self, note1, note2):
        """Create a bidirectional link between two notes."""
        if note1 not in self.graph["notes"] or note2 not in self.graph["notes"]:
            print("One or both notes do not exist.")
            return

        # Insert [[note2]] into note1
        self._insert_link(note1, note2)
        self._insert_link(note2, note1)

        # Update graph structure
        self.graph["links"].setdefault(note1, []).append(note2)
        self.graph["links"].setdefault(note2, []).append(note1)
        self.save_graph()
        print(f"Linked {note1} <-> {note2}")

    def _insert_link(self, note, target):
        """Insert a wiki-style link [[target]] into note."""
        path = self.graph["notes"][note]
        with open(path, "a") as f:
            f.write(f"\n[[{target}]]\n")

    def list_links(self, note):
        """List all links inside a note."""
        links = self.graph["links"].get(note, [])
        if links:
            print(f"Links in {note}: {', '.join(links)}")
        else:
            print(f"No links in {note}.")

    def list_backlinks(self, note):
        """List all notes linking to a given note."""
        backlinks = [n for n, links in self.graph["links"].items() if note in links]
        if backlinks:
            print(f"Backlinks to {note}: {', '.join(backlinks)}")
        else:
            print(f"No backlinks to {note}.")

    def search_notes(self, query):

        note_results = []
        log_results = []

        # --- Search in notes ---
        for note, path in self.graph.get("notes", {}).items():
            try:
                with open(path, "r") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        note_results.append(note)
            except FileNotFoundError:
                print(f"Warning: Note file '{path}' not found.")

        # --- Search in logs (titles & content) ---
        if "logs" in self.graph and isinstance(self.graph["logs"], dict):
            for title, log_data in self.graph["logs"].items():
                # Check if query matches the log title
                if query.lower() in title.lower():
                    log_results.append((title, "[TITLE MATCH] " + str(log_data)))

                # Handle logs stored as a **single string**
                if isinstance(log_data, str):
                    if query.lower() in log_data.lower():
                        log_results.append((title, log_data))

                # Handle logs stored as a **list of strings**
                elif isinstance(log_data, list):
                    for log in log_data:
                        if isinstance(log, str) and query.lower() in log.lower():
                            log_results.append((title, log))

        # --- Print Results ---
        if note_results:
            print(f"\nNotes containing '{query}': {', '.join(note_results)}")

        if log_results:
            print("\nLogs matching the query:")
            for title, log in log_results:
                print(f"- {title}: {log}")

        if not note_results and not log_results:
            print(f"No matches found.")



    def add_tag(self, note, tag):
        """Add a tag to a note."""
        self.graph["tags"].setdefault(tag, []).append(note)
        self.save_graph()
        print(f"Added tag #{tag} to {note}")

    def list_tags(self):
        """List all tags and associated notes."""
        for tag, notes in self.graph["tags"].items():
            print(f"#{tag}: {', '.join(notes)}")

    def init_graph(self):
        for filename in os.listdir(self.notes_dir):
            if filename.endswith(".na.md"):
                title = filename[:-6]
                if title not in self.graph["notes"]:
                    note_path = os.path.join(self.notes_dir, filename)
                    self.graph["notes"][title] = note_path
                    print(f"Found and added note: {title}")
        self.save_graph()

    def remove_note(self, title):
        """
        Remove a note from the graph, delete its file, and clean up associated links and tags.
        """
        if title not in self.graph["notes"]:
            print(f"Note '{title}' does not exist.")
            return
        
        # Handle case where graph["notes"][title] is either a path string or a dictionary
        note_data = self.graph["notes"].pop(title)
        
        # Extract the actual path
        note_path = note_data if isinstance(note_data, str) else note_data.get("path", "")

        # Remove this note from all links
        if title in self.graph["links"]:
            del self.graph["links"][title]  # Remove direct links

        # Remove backlinks pointing to this note
        for note, links in self.graph["links"].items():
            if title in links:
                links.remove(title)

        # Remove the note from all tags
        for tag in list(self.graph["tags"]):
            if title in self.graph["tags"][tag]:
                self.graph["tags"][tag].remove(title)
                if not self.graph["tags"][tag]:  # Remove empty tag lists
                    del self.graph["tags"][tag]

        # Delete the actual note file
        if note_path and os.path.exists(note_path):
            os.remove(note_path)
            print(f"Deleted file: {note_path}")

        # Save changes to graph.json
        self.save_graph()
        print(f"Note '{title}' removed successfully.")



