# main.py

import json
import sys
from dotenv import load_dotenv

load_dotenv()

from testgpt.analyser import analyse_requirement
from testgpt.generator import generate_selenium_test
from testgpt.file_writer import save_test_file
from testgpt.reviewer import review_and_fix


def run(requirement: str):

    print(f"\nRequirement: {requirement}")
    print("-" * 60)

    # Agent 1
    print("\nAgent 1 — Analysing requirement...")
    analysis = analyse_requirement(requirement)
    analysis["raw_text"] = requirement

    print(f"\n  Actor     : {analysis.get('actor')}")
    print(f"  Action    : {analysis.get('action')}")
    print(f"  Test type : {analysis.get('test_type')}")
    print(f"  Username  : {analysis.get('username') or 'not specified'}")
    print(f"  Password  : {analysis.get('password') or 'not specified'}")
    print(f"  URL       : {analysis.get('url')}")
    print(f"  Steps     : {len(analysis.get('test_steps', []))} found")
    print(f"  Edges     : {len(analysis.get('edge_cases', []))} found")

    # Agent 2
    print("\nAgent 2 — Writing Selenium test...")
    generated = generate_selenium_test(analysis)

    # ── Agent 3 — Review and fix ──────────────────────────────────
    print("\nAgent 3 — Reviewing and fixing code...")
    reviewed = review_and_fix(generated["code"], analysis)

    # Print the review report
    review = reviewed.get("review", {})
    issues = review.get("issues_found", 0)
    severity = review.get("severity", "none")

    print(f"\n  Issues found  : {issues}")
    print(f"  Severity      : {severity}")
    print(f"  Summary       : {review.get('summary', 'No summary')}")

    if review.get("changes"):
        print("\n  Changes made:")
        for i, change in enumerate(review["changes"]):
            print(f"\n    [{i+1}] {change.get('category', '')}")
            print(f"         Issue : {change.get('issue', '')}")
            print(f"         Fix   : {change.get('fix', '')}")

    # ── Save the REVIEWED code (not the raw Agent 2 output) ───────
    final_code = reviewed.get("fixed_code") or generated["code"]
    path = save_test_file(generated["class_name"], final_code)

    print(f"\nSaved: {path}")
    print("\n" + "=" * 60)
    print("Done. Your reviewed test file is in generated_tests/")
    print("=" * 60)


def interactive_mode():
    print("\n" + "=" * 60)
    print("  TestGPT — AI-powered Selenium test generator")
    print("=" * 60)
    print("Describe any web scenario in plain English.")
    print("Example: A user should login to saucedemo.com and add one item to cart.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            requirement = input("Enter your requirement:\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if requirement.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if not requirement:
            print("Please enter a requirement.\n")
            continue

        run(requirement)

        print("\nWant to generate another test? (press Enter or type 'quit')")
        again = input("> ").strip().lower()
        if again in ("quit", "exit", "q"):
            print("Goodbye.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        requirement = " ".join(sys.argv[1:])
        run(requirement)
    else:
        interactive_mode()