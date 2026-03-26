# testgpt/generator.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_selenium_test(analysis: dict) -> dict:
    """
    Agent 2 — Selenium Code Writer.
    Dynamically generates a complete Java test for a given scenario.
    """

    class_name   = analysis.get("class_name", "GeneratedTest")
    username     = analysis.get("username") or "standard_user"
    password     = analysis.get("password") or "secret_sauce"
    url          = analysis.get("url") or "https://www.saucedemo.com"
    test_type    = analysis.get("test_type", "mixed")

    # Format test steps
    steps_text = "\n".join(
        f"  Step {i+1}: {step}"
        for i, step in enumerate(analysis.get("test_steps", []))
    )

    # Format edge cases
    edges_text = "\n".join(
        f"  Edge {i+1}: {edge}"
        for i, edge in enumerate(analysis.get("edge_cases", []))
    )

    prompt = f"""You are a senior Selenium WebDriver automation engineer
with deep expertise in Java, TestNG, and Page Object patterns.

Generate a complete, runnable Java test class for the following specification.

==== TEST SPECIFICATION ====
Test type   : {test_type}
Actor       : {analysis["actor"]}
Action      : {analysis["action"]}
Condition   : {analysis["condition"]}
Expected    : {analysis["outcome"]}

Test steps to automate:
{steps_text}

Edge cases to cover:
{edges_text}

==== CONFIGURATION ====
Base URL    : {url}
Username    : {username}
Password    : {password}
Class name  : {class_name}
Package     : com.testgpt.generated

==== INSTRUCTIONS ====
1.  Write the complete Java class from package declaration to closing brace.
2.  Use Explicit Wait for ALL element interactions.
    Never use Thread.sleep().     
3.  Write one @Test method named testMainScenario() that automates
    ALL test steps above in exact order.
4.  Write one @Test method per edge case with a descriptive name.
5.  Use @BeforeMethod setUp() — create ChromeDriver, maximize window, navigate to base URL.
6.  Use @AfterMethod tearDown() — quit driver safely with null check.
7.  Use your own Selenium knowledge to infer the best locators for {url}.
    Prefer id > name >  xpath > cssSelector in that order.
8.  Handle any popup or overlay with a try/catch block using a 2 second wait.
    Do not fail the test if popup is absent.
9.  Add clear comments: // Arrange  // Act  // Assert in every test method.
10. Use assertTrue() and assertEquals() from TestNG for all assertions.
11. Add a meaningful assertion at the end of testMainScenario() that
    verifies the final expected outcome: {analysis["outcome"]}
12. Add imports for everything you use.
13. Add a class-level JavaDoc comment summarising the test purpose.
14. Never use any Username and Password in the ClassName  or Test Methods names. 

Return ONLY the Java code. No explanation. No markdown. No code fences.
Start directly with: package com.testgpt.generated;"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )

    code = response.choices[0].message.content.strip()

    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1])

    return {
        "class_name": class_name,
        "code": code
    }