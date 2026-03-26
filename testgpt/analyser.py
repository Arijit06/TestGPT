# testgpt/analyser.py

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyse_requirement(requirement_text: str) -> dict:
    """
    Agent 1 — Requirement Analyst.
    Reads ANY plain English requirement.
    Extracts full structured spec for Agent 2.
    """

    prompt = f"""You are a senior software test analyst.

A user will give you a plain English test requirement.
It may be messy, informal, contain credentials, URLs, or multiple actions.

Read it carefully and return ONLY a JSON object with exactly these fields:

- actor: who is performing the actions (string)
  Example: "standard user", "admin", "visual user"

- action: short summary of what is being tested (string)
  Example: "login and order one item"

- condition: the preconditions or circumstances (string)
  Example: "user is logged in with valid credentials"

- outcome: what the test should ultimately verify (string)
  Example: "one item is successfully ordered and confirmation is shown"

- test_steps: every single step to perform, in order (list of strings)
  Be specific and complete. Include every action: navigate, login, click,
  handle popup, add to cart, checkout, confirm etc.
  Example: [
    "Navigate to https://www.saucedemo.com",
    "Enter username in the username field",
    "Enter password in the password field",
    "Click the login button",
    "Wait for inventory page to load",
    "Click Add to cart on the first product",
    "Click the shopping cart icon",
    "Click Checkout",
    "Fill in First Name Last Name and Zip Code",
    "Click Continue",
    "Click Finish",
    "Verify order confirmation message is displayed"
  ]

- username: extract if mentioned, otherwise use null (string or null)

- password: extract if mentioned, otherwise use null (string or null)

- url: extract if mentioned, otherwise use "https://www.saucedemo.com" (string)

- class_name: generate a clean PascalCase Java class name (string)
  Combine actor + action, no spaces, ends with "Test"
  Example: "StandardUserOrderOneItemTest"

- edge_cases: 3 realistic boundary scenarios not mentioned (list of strings)
  Make them specific to the steps involved.
  Example: [
    "What if the cart already has items before starting?",
    "What if the checkout form is submitted with empty fields?",
    "What if the first product is out of stock?"
  ]

- test_type: classify what kind of test this is (string)
  One of: "login", "e2e_purchase", "navigation", "form_submission", "search", "mixed"

Return ONLY valid JSON. No explanation. No markdown. No code fences.

Requirement: {requirement_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.choices[0].message.content.strip()

    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1])

    return json.loads(raw_text)