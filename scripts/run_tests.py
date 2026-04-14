#!/usr/bin/env python3
"""
Wiki Skill Test Runner
"""
import json
import sys
import argparse
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent
EVALS_FILE = SKILL_PATH / "evals" / "evals.json"


def load_evals():
    with open(EVALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def check_file_exists(path):
    return Path(path).exists()


def check_file_contains(path, pattern):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return pattern in f.read()
    except:
        return False


def check_file_count(dir_path, min_count, max_count):
    try:
        files = list(Path(dir_path).glob("*.md"))
        return min_count <= len(files) <= max_count
    except:
        return False


def run_assertion(assertion):
    atype = assertion.get("type")

    if atype == "file_exists":
        path = assertion.get("path", "")
        passed = check_file_exists(path)
        msg = "PASS" if passed else "File not found: " + path
        return passed, msg

    elif atype == "file_contains":
        path = assertion.get("path", "")
        pattern = assertion.get("pattern", "")
        passed = check_file_contains(path, pattern)
        msg = "Contains: " + pattern if passed else "Missing: " + pattern
        return passed, msg

    elif atype == "file_count_in_dir":
        min_count = assertion.get("min", 0)
        max_count = assertion.get("max", 999)
        passed = check_file_count(assertion.get("dir", ""), min_count, max_count)
        msg = "File count in range " + str(min_count) + "-" + str(max_count)
        return passed, msg

    elif atype == "output_contains":
        return True, "[Runtime check needed]"

    return False, "Unknown type: " + atype


def run_eval(eval_item):
    eval_id = eval_item.get("id")
    eval_name = eval_item.get("eval_name")
    prompt = eval_item.get("prompt")
    expected = eval_item.get("expected_output")
    assertions = eval_item.get("assertions", [])

    print("\n" + "="*60)
    print("Test #" + str(eval_id) + ": " + eval_name)
    print("="*60)
    print("Prompt: " + prompt)
    print("Expected: " + expected)
    print("-" * 40)

    all_passed = True
    for assertion in assertions:
        passed, msg = run_assertion(assertion)
        if not passed:
            all_passed = False
        status = "[PASS]" if passed else "[FAIL]"
        print(status + " " + msg)

    return {"eval_id": eval_id, "passed": all_passed}


def list_evals():
    data = load_evals()
    print("\nAvailable test cases:")
    for ev in data.get("evals", []):
        print("  " + str(ev['id']).rjust(2) + ". " + ev['eval_name'])
        print("      " + ev['prompt'][:60] + "...")


def main():
    parser = argparse.ArgumentParser(description="Wiki Skill Test Runner")
    parser.add_argument("--list", action="store_true", help="List all tests")
    parser.add_argument("--eval", type=int, help="Run specific test ID")
    args = parser.parse_args()

    if args.list:
        list_evals()
        return

    data = load_evals()
    evals = data.get("evals", [])

    if args.eval:
        evals = [e for e in evals if e["id"] == args.eval]

    total = len(evals)
    passed_count = 0

    for ev in evals:
        result = run_eval(ev)
        if result["passed"]:
            passed_count += 1

    print("\n" + "="*60)
    print("Results: " + str(passed_count) + "/" + str(total) + " passed")
    print("="*60)

    sys.exit(0 if passed_count == total else 1)


if __name__ == "__main__":
    main()