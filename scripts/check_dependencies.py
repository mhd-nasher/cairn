# check_dependencies.py

"""
A simple script to check for circular dependencies between Python modules or packages.
This is a Cairn helper tool for enforcing the Acyclic Dependencies Principle (ADP, rule R-005).

Usage:
    python check_dependencies.py <package_directory>

The script scans all .py files in the directory, extracts import statements,
builds a dependency graph, and reports any cycles.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def extract_imports(file_path: Path) -> List[str]:
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                imports.append(module)
    except SyntaxError:
        pass
    return imports


def build_dependency_graph(package_dir: Path) -> Dict[str, Set[str]]:
    """Build a dependency graph for a Python package."""
    graph = {}
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                relative_path = file_path.relative_to(package_dir)
                module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
                imports = extract_imports(file_path)
                graph[module_name] = set()
                for imp in imports:
                    # Only consider imports within the package
                    if imp.startswith(str(package_dir.name)):
                        graph[module_name].add(imp)
    return graph


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find all cycles in the dependency graph using DFS."""
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: str):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
        path.pop()
        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node)
    return cycles


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_dependencies.py <package_directory>")
        sys.exit(1)

    package_dir = Path(sys.argv[1])
    if not package_dir.is_dir():
        print(f"Error: {package_dir} is not a directory")
        sys.exit(1)

    print(f"Analyzing dependencies in {package_dir}...")
    graph = build_dependency_graph(package_dir)
    cycles = find_cycles(graph)

    if cycles:
        print(f"\n❌ Found {len(cycles)} cycle(s) in the dependency graph:")
        for i, cycle in enumerate(cycles, 1):
            print(f"  Cycle {i}: {' -> '.join(cycle)}")
        print("\nThese cycles violate the Acyclic Dependencies Principle (ADP, rule R-005).")
        print("Remediation: Apply the Dependency Inversion Principle or extract a new component.")
        sys.exit(1)
    else:
        print("\n✅ No cycles found. The dependency graph is acyclic.")
        print("The Acyclic Dependencies Principle (ADP) is satisfied.")
        sys.exit(0)


if __name__ == '__main__':
    main()
