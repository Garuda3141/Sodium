from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from storage import graph, open_note, log_entry
import analysis
import os
import json

app = Flask(__name__)
app.secret_key = "supersecret"  # for flash messages
GRAPH_FILE = os.getenv("GRAPH_FILE", os.path.expanduser("~/.sodium/graph.json"))

@app.route("/", methods=["GET", "POST"])
def index():
    notes = sorted(graph.graph["notes"].keys())
    
    if request.method == "POST":
        log_title = request.form.get("log_title")
        log_text = request.form.get("log_text")
        
        if log_title and log_text:
            log_entry(GRAPH_FILE, log_title, log_text)
            flash(f"Added log for '{log_title}'.", "success")
    
    return render_template("index.html", notes=notes)


@app.route("/note/<title>")
def view_note(title):
    if title not in graph.graph["notes"]:
        return f"Note '{title}' not found", 404
    path = graph.graph["notes"][title]
    with open(path, "r") as f:
        content = f.read()
    links = graph.graph["links"].get(title, [])
    tags = [tag for tag, notes in graph.graph["tags"].items() if title in notes]
    return render_template("note.html", title=title, content=content, links=links,tags=tags)

@app.route("/new", methods=["POST"])
def new_note():
    title = request.form.get("title")
    if title:
        graph.create_note(title)
    return redirect(url_for("index"))

@app.route("/edit/<title>", methods=["GET", "POST"])
def edit_note(title):
    path = graph.graph["notes"].get(title)
    if not path:
        return "Note not found", 404
    if request.method == "POST":
        with open(path, "w") as f:
            f.write(request.form.get("content", ""))
        return redirect(url_for("view_note", title=title))
    else:
        with open(path, "r") as f:
            content = f.read()
        return render_template("edit.html", title=title, content=content)

@app.route("/delete/<title>", methods=["POST"])
def delete_note(title):
    graph.remove_note(title)
    flash(f"Deleted note '{title}'.", "warning")
    return redirect(url_for("index"))

@app.route("/link", methods=["POST"])
def link_notes():
    note1 = request.form.get("note1")
    note2 = request.form.get("note2")
    graph.create_link(note1, note2)
    flash(f"Linked '{note1}' ↔ '{note2}'.", "info")
    return redirect(url_for("view_note", title=note1))

@app.route("/tag", methods=["POST"])
def tag_note():
    note = request.form.get("note")
    tag = request.form.get("tag")
    graph.add_tag(note, tag)
    flash(f"Added tag #{tag} to '{note}'.", "success")
    return redirect(url_for("view_note", title=note))

@app.route("/tags")
def list_tags():
    return render_template("tags.html", tags=graph.graph["tags"])

@app.route("/search")
def search():
    query = request.args.get("q", "")
    found = []
    if query:
        for note in graph.graph["notes"]:
            path = graph.graph["notes"][note]
            try:
                with open(path, "r") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        found.append(note)
            except FileNotFoundError:
                pass
    return render_template("search.html", query=query, results=found)

@app.route("/graph/<mode>")
def visualize(mode):
    if mode not in {"viz", "hmap", "cen"}:
        return "Invalid mode", 400
    result = analysis.analyse(graph.graph_path, mode)
    return render_template("graph.html", mode=mode, result=result)

@app.route("/init")
def init_graph():
    graph.init_graph()
    flash("Graph initialized from notes directory.", "info")
    return redirect(url_for("index"))

@app.route("/open/<title>")
def open_in_editor(title):
    open_note(title)
    flash(f"Opened '{title}' in editor.", "info")
    return redirect(url_for("view_note", title=title))

@app.route("/log", methods=["POST"])
def add_log():
    title = request.form.get("title")
    log_text = request.form.get("log")
    log_entry(GRAPH_FILE, title, log_text)
    flash(f"Added log to '{title}'.", "success")
    return redirect(url_for("view_note", title=title))

@app.route("/logs")
def view_logs():
    # Load logs from the graph file
    logs = {}
    if os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE, "r") as f:
            try:
                data = json.load(f)
                logs = data.get("logs", {})
            except json.JSONDecodeError:
                logs = {}

    return render_template("logs.html", logs=logs)


if __name__ == "__main__":
    app.run(debug=True)
