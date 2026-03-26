# testgpt/reviewer.py

import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def review_and_fix(code: str, analysis: dict) -> dict:
    """
    Agent 3 — Code Reviewer.
    Reads the Java test code from Agent 2.
    Finds bugs and bad practices.
    Returns fixed code + a review report.
    """

    prompt = f"""You are a principal-level Selenium Java automation engineer
and code reviewer with 10+ years of experience.

You have been given a generated Selenium WebDriver test class to review.
Your job is to:
  1. Find all bugs, anti-patterns, and bad practices
  2. Fix every issue you find directly in the code
  3. Return the corrected code AND a structured review report

==== ORIGINAL REQUIREMENT ====
{analysis.get("raw_text", "")}

==== CODE TO REVIEW ====
{code}

==== WHAT TO CHECK AND FIX ====

Category 1 — Selenium best practices:
  - Every findElement must use WebDriverWait — fix any bare driver.findElement() calls
  - No Thread.sleep() allowed — replace with explicit WebDriverWait conditions
  - Locator quality — prefer id > name > cssSelector > xpath
  - If xpath is used, make sure it is not fragile (no absolute xpaths like /html/body/div[3])

Category 2 — Test structure:
  - @BeforeMethod must initialise driver AND navigate to the base URL
  - @AfterMethod must quit driver with a null check: if (driver != null) driver.quit()
  - Every @Test method must have // Arrange // Act // Assert comments
  - Every @Test method must have at least one assertion — fix any empty test bodies
  - testMainScenario() must cover ALL the test steps in the original requirement

Category 3 — Java quality:
  - All imports must be present and correct — add any missing ones
  - No unused imports — remove them
  - No raw types — use proper generics where needed
  - Constants (BASE_URL, USERNAME, PASSWORD) must be private static final

Category 4 — TestGPT specific:
  - Class name must not contain username or password values
  - Package must be com.testgpt.generated
  - Class-level JavaDoc must be present

==== RESPONSE FORMAT ====
Return a JSON object with exactly these two fields:

{{
  "fixed_code": "the complete corrected Java class as a string",
  "review": {{
    "issues_found": <number of issues you found>,
    "severity": "low" | "medium" | "high",
    "changes": [
      {{
        "category": "category name",
        "issue": "what was wrong",
        "fix": "what you changed and why"
      }}
    ],
    "summary": "one sentence overall assessment"
  }}
}}

If the code is already perfect, return it unchanged with issues_found = 0.

Return ONLY the JSON. No explanation. No markdown. No code fences."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )

    raw_text = response.choices[0].message.content.strip()

    # Clean markdown fences if present
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1])

    result = json.loads(raw_text)
    return result