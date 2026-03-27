# TestGPT

> Turn plain English into Selenium Java test code using a self-correcting 3-agent AI pipeline.

## What it does

You describe what you want to test in plain English.  
TestGPT runs three AI agents in sequence and gives you a reviewed, Java test file.
```
"A user should login to saucedemo.com and add one item to cart"
                        ↓
              Agent 1 — Requirement Analyst
     Extracts actor, steps, credentials, edge cases
                        ↓
              Agent 2 — Selenium Engineer
        Writes complete Java TestNG test class 
                        ↓
              Agent 3 — Code Reviewer
     Finds bugs, fixes them, checks code quality and coding standards explains every change 
                        ↓
        StandardUserLoginAndAddToCartTest.java (saved under generated_tests)
```

---
## Generated output

The saved Java file contains:

- `testMainScenario()` — automates all steps end to end
- One `@Test` method per edge case
- `WebDriverWait` for every element interaction — no `Thread.sleep()`
- `@BeforeMethod` and `@AfterMethod` for setup and teardown
- Full TestNG assertions with meaningful messages
- Class-level JavaDoc summarising the test purpose

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| AI model | Llama 3.3 70B via Groq API |
| Agent framework | Custom multi-agent pipeline |
| Test output | Java + Selenium WebDriver + TestNG |

---

## Setup

### Prerequisites
- Python 3.9+
- A free Groq API key — [get one here](https://console.groq.com) (no credit card needed)

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/Arijit06/TestGPT.git
cd TestGPT
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**
```bash
cp .env.example .env
# Open .env and add your key
```

---

## Usage

**Interactive mode — recommended**
```bash
python3 main.py
```

**Pass requirement directly**
```bash
python3 main.py "A user should login to saucedemo.com and add one item to cart"
```

**Any website, any scenario**
```bash
python3 main.py "An admin should be able to login to opensource-demo.orangehrmlive.com and add a new employee"
```

---

## Project structure
```
TestGPT/
├── testgpt/
│   ├── analyser.py       # Agent 1 — requirement analyst
│   ├── generator.py      # Agent 2 — Selenium code writer
│   ├── reviewer.py       # Agent 3 — code reviewer and fixer
│   └── file_writer.py    # saves generated .java files to disk
├── generated_tests/      # output folder — your .java files appear here
├── .env.example          # copy to .env and add your Groq key
├── requirements.txt
└── main.py               # entry point
```

---

## How the 3-agent pipeline works

**Agent 1 — Requirement Analyst**  
Reads your plain English requirement and extracts a structured specification — actor, action, test steps, credentials, URL, class name, and edge cases. Nothing is hardcoded — it works for any website and any scenario.

**Agent 2 — Selenium Engineer**  
Receives the structured spec from Agent 1 and writes a complete, runnable Java test class. Uses its own Selenium expertise to infer locators, waits, and assertions. Covers the main scenario and every edge case in one file.

**Agent 3 — Code Reviewer**  
Reads Agent 2's output and checks it against real Selenium best practices — missing waits, empty test bodies, fragile locators, unused imports, bad assertions. Fixes every issue it finds and returns a structured report explaining each change.

---

## Example requirements you can try
```
A locked out user should see an error message when trying to login to saucedemo.com

A user with username visual_user and password secret_sauce should login 
and add two items to the cart then checkout

An admin should login to opensource-demo.orangehrmlive.com and navigate to the employee list

A user should search for a product on saucedemo.com and verify the results
```

---

## Running the generated tests

The generated `.java` files are ready to use in any Maven project with Selenium and TestNG dependencies.

---

## Author

**Arijit Singha Roy**

---
