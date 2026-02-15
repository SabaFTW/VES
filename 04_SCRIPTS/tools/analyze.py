import json
import os
from datetime import datetime, timedelta
from difflib import SequenceMatcher

def analyze_projects(data):
    # Get the current timestamp
    analysis_timestamp = datetime.now().isoformat()

    # Initialize the output structure
    output = {
        "analysis_timestamp": analysis_timestamp,
        "categories": {
            "ACTIVE": [],
            "WIP": [],
            "GRAVEYARD": [],
            "CORE": [],
            "DOCS": []
        },
        "duplicates_detected": [],
        "largest_projects": [],
        "most_recent": []
    }

    # Get the projects from the data
    projects = data.get("projects", [])

    # --- Categorization Logic ---
    six_months_ago = datetime.now() - timedelta(days=180)
    three_months_ago = datetime.now() - timedelta(days=90)

    for project in projects:
        # Ignore files
        if project.get("type") == "file":
            continue

        path = project.get("path")
        name = project.get("name")
        size_kb = project.get("size_kb", 0)
        last_modified_str = project.get("last_modified")
        contains = project.get("contains", [])
        has_readme = project.get("has_readme", False)
        file_types = project.get("file_types", [])

        # Check for None before parsing
        if last_modified_str:
            try:
                last_modified = datetime.fromisoformat(last_modified_str)
            except ValueError:
                continue
        else:
            # Handle cases where last_modified is not available
            # For example, skip this project or use a default date
            continue

        score = 0
        reason = []

        # --- ACTIVE Category ---
        is_active = False
        active_score = 0
        active_reason = []
        if (has_readme or "package.json" in contains or "requirements.txt" in contains):
            active_score += 25
            active_reason.append("Has README/config.")
        if last_modified > six_months_ago:
             active_score+=15
             active_reason.append("Modified in last 6 months.")
        if size_kb > 10:
             active_score+=15
             active_reason.append("Size > 10KB.")
        if any(ft in ["py", "js"] for ft in file_types):
             active_score+=20
             active_reason.append("Contains working code.")
        if any(kw in name.lower() for kw in ["server", "api", "bot", "engine"]):
            active_score += 25
            active_reason.append("Contains active keywords.")

        if active_score > 50:
             output["categories"]["ACTIVE"].append({"path": path, "reason": " ".join(active_reason), "score": min(100, active_score)})
             is_active = True


        # --- WIP Category ---
        is_wip = False
        wip_score = 0
        wip_reason = []
        if not is_active:
            if "TODO.md" in contains or any("WIP" in c for c in contains):
                wip_score += 40
                wip_reason.append("Has TODO/WIP markers.")
            if last_modified > three_months_ago:
                wip_score += 30
                wip_reason.append("Recent activity.")
            if not has_readme and any(ft in ["py", "js"] for ft in file_types):
                wip_score += 20
                wip_reason.append("Missing README but has code.")
            if any(kw in name.lower() for kw in ["test", "draft", "temp"]):
                wip_score += 10
                wip_reason.append("Contains WIP keywords.")

            if wip_score > 0:
                output["categories"]["WIP"].append({"path": path, "reason": " ".join(wip_reason), "score": min(100, wip_score)})
                is_wip = True

        # --- GRAVEYARD Category ---
        is_graveyard = False
        graveyard_score = 0
        graveyard_reason = []
        if not is_active and not is_wip:
            if last_modified < six_months_ago:
                graveyard_score += 50
                graveyard_reason.append("No activity in >6 months.")
            if any(kw in path.lower() for kw in ["old", "backup", "archive"]):
                graveyard_score += 30
                graveyard_reason.append("Contains graveyard keywords in path.")
            if size_kb < 5:
                graveyard_score += 20
                graveyard_reason.append("Very small size (< 5KB).")

            if graveyard_score > 0:
                output["categories"]["GRAVEYARD"].append({"path": path, "reason": " ".join(graveyard_reason), "score": min(100, graveyard_score)})
                is_graveyard = True


        # --- CORE Category ---
        is_core = False
        core_score = 0
        core_reason = []
        if any(kw.upper() in c.upper() for c in contains for kw in ["MANIFEST", "LEGAL", "RESEARCH", "INIT"]):
            core_score += 40
            core_reason.append("Contains core file keywords.")
        if size_kb > 50 and any(c.endswith(".md") for c in contains):
            core_score += 30
            core_reason.append("Contains large markdown files.")
        if any(kw in name.lower() for kw in ["consciousness", "constellation", "treaty"]):
            core_score += 30
            core_reason.append("Contains core keywords in name.")

        if core_score > 0:
            output["categories"]["CORE"].append({"path": path, "reason": " ".join(core_reason), "score": min(100, core_score)})
            is_core = True


        # --- DOCS Category ---
        is_docs = False
        docs_score = 0
        docs_reason = []
        if any(c.endswith(".html") for c in contains):
            docs_score += 30
            docs_reason.append("Contains HTML guides.")
        if any(c.endswith(".md") for c in contains):
            docs_score += 30
            docs_reason.append("Contains markdown tutorials.")
        if any(kw in name.lower() for kw in ["guide", "howto", "readme"]):
            docs_score += 40
            docs_reason.append("Contains docs keywords in name.")

        if docs_score > 0:
             # Avoid double-counting CORE docs
            if not is_core:
                output["categories"]["DOCS"].append({"path": path, "reason": " ".join(docs_reason), "score": min(100, docs_score)})
                is_docs = True

    # --- Duplicates Detection (Simple Name Similarity) ---
    project_paths = [p["path"] for p in projects if p.get("type") == "directory"]
    for i in range(len(project_paths)):
        for j in range(i + 1, len(project_paths)):
            path1 = project_paths[i]
            path2 = project_paths[j]
            name1 = os.path.basename(path1)
            name2 = os.path.basename(path2)
            similarity = SequenceMatcher(None, name1, name2).ratio()
            if similarity > 0.8 and name1 != name2:
                output["duplicates_detected"].append({
                    "group": [path1, path2],
                    "similarity": similarity
                })


    # --- Largest and Most Recent Projects ---
    # Filter out files and sort projects by size and modification date
    dir_projects = [p for p in projects if p.get("type") == "directory" and p.get("last_modified")]

    # Sort by size for largest_projects
    largest = sorted(dir_projects, key=lambda p: p.get("size_kb", 0), reverse=True)[:10]
    output["largest_projects"] = [{"path": p["path"], "size_mb": p.get("size_kb", 0) / 1024} for p in largest]

    # Sort by modification date for most_recent
    recent = sorted(dir_projects, key=lambda p: datetime.fromisoformat(p["last_modified"]), reverse=True)[:10]
    output["most_recent"] = [{"path": p["path"], "last_modified": p["last_modified"]} for p in recent]


    return output

if __name__ == "__main__":
    # Read the input file
    with open("/home/saba/MASTER_NAVIGATOR/raw_scan_data.json", "r") as f:
        data = json.load(f)

    # Analyze the projects
    analyzed_data = analyze_projects(data)

    # Write the output file
    with open("/home/saba/MASTER_NAVIGATOR/analyzed_projects.json", "w") as f:
        json.dump(analyzed_data, f, indent=2)

    print("Analysis complete. Output saved to /home/saba/MASTER_NAVIGATOR/analyzed_projects.json")
