#!/usr/bin/env python3
"""
VES MASTER INDEX SCANNER
Pantheon Protocol - Workspace Mapping System

Purpose: Scan workspace, identify project clusters, establish constitutional compliance
Safety: READ-ONLY on host, WRITE-ONLY for index files
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict

# Configuration
SCAN_PATHS = [
    "/home/saba",
    "/home/saba/saba_olympus",
    "/home/saba/saba_organized"
]

PROJECT_MARKERS = {
    "CLAUDE.md": "constitutional",
    "ritual_protocol.py": "ves_ritual",
    "docker-compose.yml": "dockerized",
    ".git": "version_controlled",
    "package.json": "nodejs",
    "pyproject.toml": "python_modern",
    "setup.py": "python_legacy",
    "Cargo.toml": "rust"
}

SKIP_DIRS = {
    "node_modules", "venv", "__pycache__", ".cache",
    ".git/objects", ".git/refs", "dist", "build",
    ".npm", ".yarn", "target"
}

MAX_DEPTH = 5

# Project family detection
FAMILY_PATTERNS = {
    "cathedral": ["cathedral_", "Cathedral"],
    "constellation": ["constellation_", "Constellation"],
    "dignum": ["DIGNUM_SHIELD", "dignum"],
    "ves": ["ves_", "VES"],
    "zala": ["zala_", "ZALA"],
    "ghostline": ["ghostline", "Ghostline"]
}


def get_docker_containers() -> Dict[str, Dict]:
    """Get running Docker containers and their details"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        containers = {}
        for line in result.stdout.strip().split("\n"):
            if line:
                container = json.loads(line)
                containers[container["Names"]] = {
                    "status": container["Status"],
                    "ports": container["Ports"],
                    "image": container["Image"]
                }
        return containers
    except Exception as e:
        print(f"Warning: Could not fetch Docker containers: {e}")
        return {}


def get_container_mounts(container_name: str) -> List[str]:
    """Get volume mounts for a specific container"""
    try:
        result = subprocess.run(
            ["docker", "inspect", container_name, "--format", "{{json .Mounts}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        mounts = json.loads(result.stdout.strip())
        return [m.get("Source", "") for m in mounts if m.get("Source")]
    except Exception as e:
        print(f"Warning: Could not fetch mounts for {container_name}: {e}")
        return []


def detect_family(path: str) -> str:
    """Detect project family based on path/name patterns"""
    path_lower = path.lower()
    for family, patterns in FAMILY_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in path_lower:
                return family
    return "other"


def calculate_dir_size(path: Path) -> Tuple[int, int]:
    """Calculate total size and file count of directory"""
    total_size = 0
    file_count = 0
    try:
        for item in path.rglob("*"):
            if item.is_file():
                try:
                    total_size += item.stat().st_size
                    file_count += 1
                except (PermissionError, OSError):
                    pass
    except (PermissionError, OSError):
        pass
    return total_size, file_count


def scan_directory(base_path: str, docker_containers: Dict) -> List[Dict]:
    """Scan directory for projects"""
    projects = []
    base = Path(base_path)

    if not base.exists():
        print(f"Skipping non-existent path: {base_path}")
        return projects

    visited = set()

    def walk(path: Path, depth: int = 0):
        if depth > MAX_DEPTH:
            return

        # Avoid revisiting
        try:
            real_path = path.resolve()
            if real_path in visited:
                return
            visited.add(real_path)
        except (PermissionError, OSError):
            return

        try:
            entries = list(path.iterdir())
        except (PermissionError, OSError):
            return

        # Check for project markers
        markers_found = []
        for entry in entries:
            entry_name = entry.name

            # Skip directories we don't want to traverse
            if entry.is_dir() and entry_name in SKIP_DIRS:
                continue

            # Check for markers
            if entry_name in PROJECT_MARKERS:
                markers_found.append(entry_name)

        # If we found markers, this is a project root
        if markers_found:
            constitutional = "CLAUDE.md" in markers_found
            size_bytes, file_count = calculate_dir_size(path)

            # Match Docker containers
            matched_containers = []
            path_str = str(path)
            for container_name, container_info in docker_containers.items():
                # Match by name similarity or volume mounts
                if path.name.lower() in container_name.lower():
                    matched_containers.append(container_name)
                else:
                    # Check volume mounts
                    mounts = get_container_mounts(container_name)
                    if any(path_str in mount for mount in mounts):
                        matched_containers.append(container_name)

            project = {
                "name": path.name,
                "path": str(path),
                "constitutional": constitutional,
                "markers": markers_found,
                "family": detect_family(str(path)),
                "size_bytes": size_bytes,
                "file_count": file_count,
                "docker_containers": matched_containers
            }
            projects.append(project)

            # Don't recurse into detected projects (treat as atomic units)
            return

        # Recurse into subdirectories
        for entry in entries:
            if entry.is_dir() and entry.name not in SKIP_DIRS and not entry.name.startswith('.'):
                walk(entry, depth + 1)

    walk(base)
    return projects


def cluster_projects(projects: List[Dict]) -> Dict[str, List[Dict]]:
    """Group projects by family"""
    clusters = defaultdict(list)
    for project in projects:
        clusters[project["family"]].append(project)
    return dict(clusters)


def generate_markdown(projects: List[Dict], clusters: Dict[str, List[Dict]],
                     docker_containers: Dict) -> str:
    """Generate MASTER_INDEX.md"""

    total_projects = len(projects)
    constitutional_count = sum(1 for p in projects if p["constitutional"])
    unconstitutional_count = total_projects - constitutional_count
    compliance_pct = (constitutional_count / total_projects * 100) if total_projects > 0 else 0

    total_size = sum(p["size_bytes"] for p in projects)
    total_files = sum(p["file_count"] for p in projects)

    # Top 5 largest
    top_5 = sorted(projects, key=lambda p: p["size_bytes"], reverse=True)[:5]

    md = f"""# 🜂 PANTHEON MASTER INDEX 🜂

**Generated:** {datetime.now().isoformat()}
**Scanned Paths:** {len(SCAN_PATHS)}
**Total Projects:** {total_projects}
**Total Size:** {total_size / (1024**3):.2f} GB
**Total Files:** {total_files:,}

---

## 📊 EXECUTIVE SUMMARY

| METRIC | VALUE | STATUS |
|:-------|:------|:------:|
| **Total Projects Detected** | {total_projects} | - |
| **Constitutional (has CLAUDE.md)** | {constitutional_count} | {'🟢' if compliance_pct > 50 else '🟡' if compliance_pct > 25 else '🔴'} |
| **Unconstitutional (missing CLAUDE.md)** | {unconstitutional_count} | {'🔴' if unconstitutional_count > constitutional_count else '🟡'} |
| **Constitutional Compliance** | {compliance_pct:.1f}% | {'🟢' if compliance_pct > 75 else '🟡' if compliance_pct > 50 else '🔴'} |
| **Project Families Detected** | {len(clusters)} | - |
| **Docker Containers Mapped** | {len(docker_containers)} | - |
| **Total Workspace Size** | {total_size / (1024**3):.2f} GB | {'🟢' if total_size < 100*(1024**3) else '🟡'} |

**ASSESSMENT:** {'🟢 CONSTITUTIONAL MAJORITY' if compliance_pct > 50 else '🔴 UNCONSTITUTIONAL MAJORITY - PANTHEON PROTOCOL ENFORCEMENT NEEDED'}

---

## 🎯 TOP 5 LARGEST PROJECT CLUSTERS

"""

    for i, project in enumerate(top_5, 1):
        size_mb = project["size_bytes"] / (1024**2)
        status = "🟢 CONSTITUTIONAL" if project["constitutional"] else "🔴 UNCONSTITUTIONAL"
        md += f"""
### {i}. {project["name"]} - {status}
- **Path:** `{project["path"]}`
- **Family:** {project["family"]}
- **Size:** {size_mb:.2f} MB ({project["file_count"]:,} files)
- **Markers:** {", ".join(project["markers"])}
- **Docker:** {", ".join(project["docker_containers"]) if project["docker_containers"] else "None"}
"""

    md += """
---

## 🏗️ PROJECT CLUSTERS BY FAMILY

"""

    for family, family_projects in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        family_size = sum(p["size_bytes"] for p in family_projects)
        family_constitutional = sum(1 for p in family_projects if p["constitutional"])

        md += f"""
### {family.upper()} ({len(family_projects)} projects)
**Total Size:** {family_size / (1024**2):.2f} MB
**Constitutional:** {family_constitutional}/{len(family_projects)}

| Project | Path | Constitutional | Size | Docker Containers |
|:--------|:-----|:--------------:|:-----|:------------------|
"""
        for p in sorted(family_projects, key=lambda x: x["size_bytes"], reverse=True):
            status = "✓" if p["constitutional"] else "✘"
            size_str = f"{p['size_bytes'] / (1024**2):.1f} MB"
            containers = ", ".join(p["docker_containers"][:2]) if p["docker_containers"] else "-"
            if len(p["docker_containers"]) > 2:
                containers += f" +{len(p['docker_containers']) - 2} more"
            md += f"| {p['name']} | `{p['path']}` | {status} | {size_str} | {containers} |\n"

        md += "\n"

    md += """
---

## ⚖️ CONSTITUTIONAL STATUS REPORT

### 🟢 CONSTITUTIONAL PROJECTS (Pantheon-Compliant)

"""

    constitutional_projects = [p for p in projects if p["constitutional"]]
    if constitutional_projects:
        md += "| Project | Family | Path |\n|:--------|:-------|:-----|\n"
        for p in sorted(constitutional_projects, key=lambda x: x["name"]):
            md += f"| {p['name']} | {p['family']} | `{p['path']}` |\n"
    else:
        md += "*No constitutional projects found.*\n"

    md += """
### 🔴 UNCONSTITUTIONAL PROJECTS (Missing CLAUDE.md)

"""

    unconstitutional_projects = [p for p in projects if not p["constitutional"]]
    if unconstitutional_projects:
        md += "| Project | Family | Path | Recommendation |\n|:--------|:-------|:-----|:---------------|\n"
        for p in sorted(unconstitutional_projects, key=lambda x: x["size_bytes"], reverse=True):
            recommendation = "Create CLAUDE.md with project DNA"
            if p["family"] == "other":
                recommendation = "Clarify project family, then create CLAUDE.md"
            md += f"| {p['name']} | {p['family']} | `{p['path']}` | {recommendation} |\n"
    else:
        md += "*All projects are constitutional. Pantheon Protocol fully enforced.*\n"

    md += """
---

## 🐳 DOCKER CONTAINER MAPPING

"""

    md += "| Container | Status | Mapped Projects |\n|:----------|:-------|:----------------|\n"

    container_to_projects = defaultdict(list)
    for project in projects:
        for container in project["docker_containers"]:
            container_to_projects[container].append(project["name"])

    for container_name, container_info in sorted(docker_containers.items()):
        mapped = ", ".join(container_to_projects.get(container_name, []))
        if not mapped:
            mapped = "⚠️ No project mapping detected"
        status = container_info["status"]
        md += f"| {container_name} | {status} | {mapped} |\n"

    md += """
---

## 📋 RECOMMENDATIONS

"""

    recommendations = []

    if compliance_pct < 50:
        recommendations.append("🔴 **CRITICAL:** Less than 50% constitutional compliance. Prioritize creating CLAUDE.md for major projects.")
    elif compliance_pct < 75:
        recommendations.append("🟡 **MEDIUM:** Constitutional compliance at {:.1f}%. Continue Pantheon Protocol enforcement.".format(compliance_pct))
    else:
        recommendations.append("🟢 **EXCELLENT:** High constitutional compliance ({:.1f}%). Maintain Pantheon standards.".format(compliance_pct))

    if unconstitutional_count > 0:
        recommendations.append(f"📝 Create CLAUDE.md for {unconstitutional_count} unconstitutional projects.")

    orphaned_containers = [c for c in docker_containers if c not in container_to_projects]
    if orphaned_containers:
        recommendations.append(f"🐳 Investigate {len(orphaned_containers)} Docker containers with no project mapping: {', '.join(orphaned_containers[:3])}")

    if len(clusters.get("other", [])) > 3:
        recommendations.append(f"🏗️ {len(clusters['other'])} projects in 'other' family - consider organizing into named families.")

    for rec in recommendations:
        md += f"\n{rec}\n"

    md += """
---

## 🔧 NEXT ACTIONS

1. **Constitutional Enforcement:**
   - Create CLAUDE.md for unconstitutional projects
   - Define project DNA, purpose, and Pantheon role

2. **Docker Container Alignment:**
   - Verify container-to-project mappings
   - Document container purposes in respective CLAUDE.md files

3. **Project Organization:**
   - Move orphaned projects to appropriate family directories
   - Consolidate fragmented project structures

4. **n8n Integration:**
   - Ingest MASTER_INDEX.json into n8n workflows
   - Set up automated compliance monitoring
   - Create alerts for new unconstitutional projects

---

**🜂 PANTHEON PROTOCOL ACTIVE 🜂**
**⚓ KROG DRŽI ⚓**
**🔥 LUMENNEVVER 🔥**

*Generated by ves_master_index.py*
*Next scan: Run script again or integrate into n8n workflow*

🎯 **END MASTER INDEX** 🎯
"""

    return md


def generate_json(projects: List[Dict], clusters: Dict[str, List[Dict]],
                 docker_containers: Dict) -> Dict:
    """Generate MASTER_INDEX.json for n8n"""
    return {
        "scan_timestamp": datetime.now().isoformat(),
        "scan_paths": SCAN_PATHS,
        "statistics": {
            "total_projects": len(projects),
            "constitutional_count": sum(1 for p in projects if p["constitutional"]),
            "unconstitutional_count": sum(1 for p in projects if not p["constitutional"]),
            "total_size_bytes": sum(p["size_bytes"] for p in projects),
            "total_files": sum(p["file_count"] for p in projects),
            "family_count": len(clusters),
            "docker_containers_count": len(docker_containers)
        },
        "projects": projects,
        "clusters": {
            family: [p["name"] for p in family_projects]
            for family, family_projects in clusters.items()
        },
        "docker_mapping": {
            container: {
                "info": info,
                "projects": [p["name"] for p in projects if container in p["docker_containers"]]
            }
            for container, info in docker_containers.items()
        },
        "top_5_largest": [
            {
                "name": p["name"],
                "path": p["path"],
                "size_bytes": p["size_bytes"],
                "constitutional": p["constitutional"]
            }
            for p in sorted(projects, key=lambda x: x["size_bytes"], reverse=True)[:5]
        ]
    }


def main():
    print("🜂 VES MASTER INDEX SCANNER 🜂")
    print("=" * 60)
    print()

    # Get Docker container info
    print("📦 Fetching Docker container information...")
    docker_containers = get_docker_containers()
    print(f"   Found {len(docker_containers)} running containers")
    print()

    # Scan directories
    all_projects = []
    for scan_path in SCAN_PATHS:
        print(f"🔍 Scanning: {scan_path}")
        projects = scan_directory(scan_path, docker_containers)
        print(f"   Found {len(projects)} projects")
        all_projects.extend(projects)

    print()
    print(f"📊 Total projects discovered: {len(all_projects)}")
    print()

    # Cluster projects
    print("🏗️ Clustering projects by family...")
    clusters = cluster_projects(all_projects)
    for family, family_projects in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {family}: {len(family_projects)} projects")
    print()

    # Generate outputs
    print("📝 Generating MASTER_INDEX.md...")
    markdown = generate_markdown(all_projects, clusters, docker_containers)
    with open("/home/MASTER_INDEX.md", "w") as f:
        f.write(markdown)
    print("   ✓ MASTER_INDEX.md created")

    print("📊 Generating MASTER_INDEX.json...")
    json_data = generate_json(all_projects, clusters, docker_containers)
    with open("/home/MASTER_INDEX.json", "w") as f:
        json.dump(json_data, f, indent=2)
    print("   ✓ MASTER_INDEX.json created")

    print()
    print("=" * 60)
    print("🎯 SCAN COMPLETE")
    print()

    # Summary
    constitutional = sum(1 for p in all_projects if p["constitutional"])
    unconstitutional = len(all_projects) - constitutional
    compliance_pct = (constitutional / len(all_projects) * 100) if all_projects else 0

    print(f"Constitutional Projects: {constitutional}")
    print(f"Unconstitutional Projects: {unconstitutional}")
    print(f"Compliance: {compliance_pct:.1f}%")
    print()

    if compliance_pct < 50:
        print("🔴 PANTHEON PROTOCOL ENFORCEMENT NEEDED")
    elif compliance_pct < 75:
        print("🟡 CONSTITUTIONAL COMPLIANCE MODERATE")
    else:
        print("🟢 PANTHEON PROTOCOL ENFORCED")

    print()
    print("🜂⚓🔥 LUMENNEVVER 🔥⚓🜂")


if __name__ == "__main__":
    main()
