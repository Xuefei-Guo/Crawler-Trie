from flask import Flask, render_template, request, jsonify
from .crawler import build_index
import os
import threading

app = Flask(__name__)

# Global storage
search_trie = None
is_building = False
build_status = "Ready"

# Configuration
current_config = {
    "url": os.getenv("URL", "https://example.com"),
    "depth": int(os.getenv("DEPTH", 2))
}

def run_build_index(url, depth):
    """Background task to build index."""
    global search_trie, is_building, build_status
    is_building = True
    build_status = f"Crawling {url} (Depth {depth})..."
    print(build_status)
    
    try:
        new_trie = build_index(url, depth)
        search_trie = new_trie
        build_status = "Index built successfully."
    except Exception as e:
        build_status = f"Error: {str(e)}"
        print(build_status)
    finally:
        is_building = False

@app.before_request
def initialize_app():
    """
    Builds the index when the application starts.
    """
    global search_trie
    # only build the index once
    if search_trie is not None:
        return  

    # If no index, build it
    if not is_building:
        thread = threading.Thread(target=run_build_index, args=(current_config["url"], current_config["depth"]))
        thread.start()


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the main search page.
    """
    return render_template("index.html")


@app.route("/api/config", methods=["GET", "POST"])
def config():
    """
    Get or update configuration.
    """
    global current_config
    
    if request.method == "POST":
        if is_building:
            return jsonify({"error": "Index is currently building"}), 409
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        new_url = data.get("url")
        new_depth = int(data.get("depth", 2))
        
        if new_url:
            current_config["url"] = new_url
            current_config["depth"] = new_depth
            
            # Start rebuild in background
            thread = threading.Thread(target=run_build_index, args=(new_url, new_depth))
            thread.start()
            
            return jsonify({"message": "Rebuild started", "config": current_config})
            
    return jsonify({
        "config": current_config,
        "is_building": is_building,
        "status": build_status
    })


@app.route("/search")
def search():
    """
    Accepts query and returns JSON data.
    """
    query = request.args.get("query", "")
    
    if not query or not search_trie:
        return jsonify([])
    
    # get wildcard search results
    results = list(search_trie.wildcard_search(query))
    # sort by word
    results.sort(key=lambda x: x[0])
    
    # convert to JSON-friendly format
    json_data = []
    for word, urls in results:
        json_data.append({
            "word": word,
            "urls": sorted(urls) # Sort URLs
        })
        
    return jsonify(json_data)

@app.route("/autocomplete")
def autocomplete():
    """
    Accepts prefix and returns list of matching words.
    """
    prefix = request.args.get("q", "")
    
    if not prefix or not search_trie:
        return jsonify([])
    
    # get autocomplete results
    results = search_trie.autocomplete(prefix)
    # sort alphabetically and limit to 10
    results.sort()
    return jsonify(results[:10])