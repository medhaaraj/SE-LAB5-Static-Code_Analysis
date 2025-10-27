REFLECTION QUESTIONS
1. Which issues were the easiest to fix, and which were the hardest? Why?
Easiest: Style and formatting issues flagged by Flake8 were the simplest to fix. Problems like long lines (E501), missing blank lines, and string formatting were straightforward because the feedback was explicit and the corrections had no effect on logic.
Hardest: Logic-related or design-related fixes, such as adding input validation, replacing the bare except: with specific exception types, and configuring logging correctly were more challenging. These required understanding how the program worked and ensuring that changes didn’t break functionality.


2. Did the static analysis tools report any false positives? If so, describe one example.
There were minor Pylint warnings (e.g., suggesting to remove “global variables” or to rename constants) that didn’t represent real errors for this small lab program.In this context, those were false positives because the global dictionary STOCK_DATA was intentionally kept simple for the exercise, and changing it to a class would have added unnecessary complexity.


3. How would you integrate static analysis tools into your actual software development workflow?
Integrate Pylint, Flake8, and Bandit into a pre-commit hook so code is automatically checked before each commit.Add these tools to a Continuous Integration (CI) pipeline (e.g., GitHub Actions) so that every pull request runs the checks automatically.Use VS Code extensions for Pylint or Flake8 to get 
real-time linting feedback during local development, catching problems before pushing code.


4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
The code is now cleaner, safer, and more maintainable:
- Replacing eval() and bare except: improved security and reliability.
- Adding input validation prevents invalid data from corrupting the inventory.
- Using logging instead of print() improved traceability and debugging.
- Refactoring long lines and adding docstrings improved readability and made the code PEP 8 compliant.
Overall, the program feels more professional and production-ready, with clear error messages, safer operations, and consistent style.
