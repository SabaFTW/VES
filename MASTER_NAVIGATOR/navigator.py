#!/usr/bin/env python3
"""
MASTER NAVIGATOR - Šabad's Project Navigation Tool
"""
import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ANSI colors
class Color:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    END = "\033[0m"


BASE_DIR = Path(__file__).resolve().parent
RAW_PATH = BASE_DIR / "raw_scan_data.json"
ANALYZED_PATH = BASE_DIR / "analyzed_projects.json"


def color_text(text: str, color: str) -> str:
    return f"{color}{text}{Color.END}"


def format_size_kb(size_kb: float) -> str:
    """Format size from kilobytes to a readable string."""
    size_bytes = size_kb * 1024
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size_bytes < 1024 or unit == units[-1]:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_time(iso_ts: Optional[str]) -> str:
    if not iso_ts:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(iso_ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return str(iso_ts)


def ensure_data_files() -> None:
    for path in (RAW_PATH, ANALYZED_PATH):
        if not path.exists():
            print(color_text(f"Missing data file: {path}", Color.RED))
            sys.exit(1)


@lru_cache(maxsize=1)
def load_data() -> Dict[str, object]:
    """Load scan & analysis data with basic caching."""
    ensure_data_files()
    try:
        with RAW_PATH.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
        with ANALYZED_PATH.open("r", encoding="utf-8") as fh:
            analyzed = json.load(fh)
    except json.JSONDecodeError as exc:
        print(color_text(f"Failed to parse JSON: {exc}", Color.RED))
        sys.exit(1)

    categories = build_category_lookup(analyzed)
    project_index = build_project_index(raw)
    return {
        "raw": raw,
        "analyzed": analyzed,
        "categories": categories,
        "project_index": project_index,
    }


def build_category_lookup(analyzed: Dict[str, object]) -> Dict[str, str]:
    lookup: Dict[str, str] = {}
    for cat, entries in analyzed.get("categories", {}).items():
        for entry in entries:
            path = entry.get("path")
            if path:
                lookup[path] = cat
    return lookup


def build_project_index(raw: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    index: Dict[str, Dict[str, object]] = {}
    for project in raw.get("projects", []):
        path = project.get("path")
        if path:
            index[path] = project
    return index


def get_category_for_path(path: str) -> Optional[str]:
    return load_data()["categories"].get(path)


def category_color(category: Optional[str]) -> str:
    cat = (category or "").upper()
    if cat == "ACTIVE":
        return Color.GREEN
    if cat == "WIP":
        return Color.YELLOW
    if cat == "GRAVEYARD":
        return Color.RED
    if cat == "CORE":
        return Color.BLUE
    if cat == "DOCS":
        return Color.CYAN
    return Color.CYAN


def list_projects(category: Optional[str] = None) -> None:
    data = load_data()
    projects = data["raw"].get("projects", [])
    cat_lookup = data["categories"]
    target_cat = category.upper() if category else None
    filtered = (
        [p for p in projects if cat_lookup.get(p.get("path")) == target_cat]
        if target_cat
        else projects
    )
    if not filtered:
        msg = f"No projects found for category '{category}'" if category else "No projects found."
        print(color_text(msg, Color.RED))
        return

    for project in sorted(filtered, key=lambda p: p.get("name", "").lower()):
        path = project.get("path", "")
        cat = cat_lookup.get(path, "UNCATEGORIZED")
        color = category_color(cat)
        size = format_size_kb(project.get("size_kb", 0))
        last = format_time(project.get("last_modified"))
        print(
            f"{color_text(project.get('name', 'unknown'), color)} "
            f"[{cat}] {path} (size: {size}, last: {last})"
        )


def search(keyword: str) -> None:
    data = load_data()
    kw = keyword.lower()
    results: List[Dict[str, object]] = []
    for project in data["raw"].get("projects", []):
        fields: List[str] = [
            project.get("name", ""),
            project.get("path", ""),
        ]
        contains = project.get("contains") or []
        file_types = project.get("file_types") or []
        fields.extend(contains)
        fields.extend(file_types)
        if any(kw in str(field).lower() for field in fields):
            results.append(project)

    if not results:
        print(color_text(f"No matches for '{keyword}'.", Color.RED))
        return

    print(color_text(f"Found {len(results)} matches for '{keyword}':", Color.GREEN))
    cat_lookup = data["categories"]
    for project in sorted(results, key=lambda p: p.get("name", "").lower()):
        path = project.get("path", "")
        cat = cat_lookup.get(path, "UNCATEGORIZED")
        color = category_color(cat)
        print(f"- {color_text(project.get('name', 'unknown'), color)} [{cat}] {path}")


def find_project_by_name(name: str) -> Tuple[Optional[Dict[str, object]], List[Dict[str, object]]]:
    data = load_data()
    projects = data["raw"].get("projects", [])
    name_lower = name.lower()
    exact = [p for p in projects if p.get("name", "").lower() == name_lower]
    if exact:
        return exact[0], exact
    partial = [p for p in projects if name_lower in p.get("name", "").lower() or name_lower in p.get("path", "").lower()]
    if partial:
        return partial[0], partial
    return None, []


def show_status() -> None:
    list_projects(category="ACTIVE")


def build_tree(paths: List[str]) -> Dict[str, dict]:
    tree: Dict[str, dict] = {}
    home = Path.home()
    for raw_path in paths:
        p = Path(raw_path)
        try:
            rel = p.relative_to(home)
            parts = rel.parts
        except ValueError:
            parts = p.parts
        node = tree
        for part in parts:
            node = node.setdefault(part, {})
    return tree


def print_tree(tree: Dict[str, dict], prefix: str = "") -> None:
    items = sorted(tree.items(), key=lambda kv: kv[0].lower())
    for idx, (name, subtree) in enumerate(items):
        connector = "`-- " if idx == len(items) - 1 else "|-- "
        print(f"{prefix}{connector}{name}")
        if subtree:
            extension = "    " if idx == len(items) - 1 else "|   "
            print_tree(subtree, prefix + extension)


def show_tree(category: Optional[str] = None) -> None:
    data = load_data()
    cat_lookup = data["categories"]
    target_cat = category.upper() if category else None
    paths = []
    for project in data["raw"].get("projects", []):
        path = project.get("path")
        if not path:
            continue
        if target_cat and cat_lookup.get(path) != target_cat:
            continue
        paths.append(path)

    if not paths:
        msg = f"No paths found for category '{category}'" if category else "No paths to display."
        print(color_text(msg, Color.RED))
        return

    tree = build_tree(paths)
    print(color_text("Project Tree:", Color.BLUE))
    print_tree(tree)


def open_project(name: str) -> None:
    project, matches = find_project_by_name(name)
    if not project:
        print(color_text(f"Project '{name}' not found.", Color.RED))
        return
    if len(matches) > 1 and project.get("name", "").lower() != name.lower():
        print(color_text(f"Multiple matches found, opening first: {project.get('name')}", Color.YELLOW))

    path = project.get("path")
    if not path or not Path(path).exists():
        print(color_text(f"Path not found: {path}", Color.RED))
        return

    try:
        subprocess.run(["xdg-open", path], check=False)
        print(color_text(f"Opened {path}", Color.GREEN))
    except FileNotFoundError:
        print(color_text("xdg-open is not available on this system.", Color.RED))


def get_category_detail(path: str) -> Tuple[Optional[str], Optional[Dict[str, object]]]:
    data = load_data()
    cat_lookup = data["categories"]
    cat = cat_lookup.get(path)
    if not cat:
        return None, None
    for entry in data["analyzed"].get("categories", {}).get(cat, []):
        if entry.get("path") == path:
            return cat, entry
    return cat, None


def show_info(name: str) -> None:
    project, matches = find_project_by_name(name)
    if not project:
        print(color_text(f"Project '{name}' not found.", Color.RED))
        return
    if len(matches) > 1 and project.get("name", "").lower() != name.lower():
        print(color_text(f"Multiple matches found, showing first: {project.get('name')}", Color.YELLOW))

    path = project.get("path", "")
    cat, cat_entry = get_category_detail(path)
    color = category_color(cat)
    size = format_size_kb(project.get("size_kb", 0))
    last = format_time(project.get("last_modified"))
    contains = project.get("contains") or []
    file_types = project.get("file_types") or []

    print(color_text(f"Info for {project.get('name', 'unknown')}", color))
    print(f"Path         : {path}")
    print(f"Category     : {cat or 'UNCATEGORIZED'}")
    if cat_entry:
        reason = cat_entry.get("reason")
        score = cat_entry.get("score")
        if reason:
            print(f"Reason       : {reason}")
        if score is not None:
            print(f"Score        : {score}")
    print(f"Size         : {size}")
    print(f"Last modified: {last}")
    print(f"Files        : {len(contains)} listed")
    if file_types:
        print(f"File types   : {', '.join(file_types)}")

    path_obj = Path(path)
    if path_obj.exists():
        try:
            stat = path_obj.stat()
            print(f"FS modified  : {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        except OSError:
            pass

    if contains:
        preview = ", ".join(contains[:5])
        if len(contains) > 5:
            preview += ", ..."
        print(f"Contains     : {preview}")


def print_prompt_help() -> None:
    print(
        "Commands:\n"
        "  list [CATEGORY]   - List projects (optionally by category)\n"
        "  status            - Show ACTIVE projects\n"
        "  search <keyword>  - Search by name/path/content\n"
        "  tree [CATEGORY]   - Show path tree\n"
        "  info <project>    - Show detailed info\n"
        "  open <project>    - Open project directory\n"
        "  help              - Show this help\n"
        "  quit/exit         - Leave prompt"
    )


def interactive_prompt() -> None:
    ensure_data_files()
    print(color_text("MASTER NAVIGATOR interactive prompt (type 'help' for commands, 'quit' to exit)", Color.BLUE))
    while True:
        try:
            line = input(color_text("nav> ", Color.CYAN))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = shlex.split(line)
        if not parts:
            continue
        cmd, *args = parts
        cmd_lower = cmd.lower()
        if cmd_lower in {"quit", "exit", "q"}:
            break
        if cmd_lower in {"help", "?"}:
            print_prompt_help()
            continue
        if cmd_lower in {"list", "ls"}:
            list_projects(category=args[0] if args else None)
            continue
        if cmd_lower == "status":
            show_status()
            continue
        if cmd_lower == "search":
            if not args:
                print(color_text("Usage: search <keyword>", Color.YELLOW))
                continue
            search(" ".join(args))
            continue
        if cmd_lower == "tree":
            show_tree(category=args[0] if args else None)
            continue
        if cmd_lower == "info":
            if not args:
                print(color_text("Usage: info <project_name>", Color.YELLOW))
                continue
            show_info(" ".join(args))
            continue
        if cmd_lower == "open":
            if not args:
                print(color_text("Usage: open <project_name>", Color.YELLOW))
                continue
            open_project(" ".join(args))
            continue
        print(color_text(f"Unknown command: {cmd}", Color.RED))
        print(color_text("Type 'help' for available commands.", Color.YELLOW))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Navigate projects scanned in raw_scan_data.json and analyzed_projects.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python navigator.py --list\n"
            "  python navigator.py --search api\n"
            "  python navigator.py --status\n"
            "  python navigator.py --tree\n"
            "  python navigator.py --category ACTIVE\n"
            "  python navigator.py --open cloud_constellation\n"
            "  python navigator.py --info cloud_constellation\n"
            "  python navigator.py --prompt\n"
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="List all projects (optionally filtered by --category).")
    group.add_argument("--search", metavar="KEYWORD", help="Search projects by name/path/content.")
    group.add_argument("--status", action="store_true", help="Show ACTIVE projects only.")
    group.add_argument("--tree", action="store_true", help="Show ASCII tree of project paths.")
    group.add_argument("--open", metavar="PROJECT", help="Open a project directory in the file manager.")
    group.add_argument("--info", metavar="PROJECT", help="Show detailed info for a project.")
    group.add_argument("--prompt", action="store_true", help="Start interactive prompt mode.")
    parser.add_argument("--category", metavar="CATEGORY", help="Filter by category (e.g., ACTIVE, WIP, GRAVEYARD).")
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_data_files()

    if args.list:
        list_projects(category=args.category)
    elif args.status:
        show_status()
    elif args.search:
        search(args.search)
    elif args.tree:
        show_tree(category=args.category)
    elif args.open:
        open_project(args.open)
    elif args.info:
        show_info(args.info)
    elif args.prompt:
        interactive_prompt()
    elif args.category:
        list_projects(category=args.category)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
