# ParkEase BDD – Automated Software Testing, Assignment 2

**Student:** Waleed Abdulah  **Reg. No.:** BSE223145  **Tool:** Python 3 + behave (Gherkin)

An in-memory `ParkEase` model (rules R1–R8) tested with behave scenarios for the
"automatic parking fee on exit" user story.

## Run all tests (one command)

```bash
pip install -r requirements.txt && behave
```

(After the first install, the single command `behave` is enough.)

## Useful variants

```bash
behave --tags=@smoke        # EV happy path only (this is what CI runs)
behave --tags=@boundary     # grace / rounding / cap boundaries
behave --tags=@negative     # wallet Rs. 1 short
behave -f progress3         # compact one-line-per-scenario output
behave --tags=@smoke -f behave_html_formatter:HTMLFormatter -o reports/smoke-report.html
```

## Layout

```
parkease/parkease.py              ParkEase + ExitResult (business rules R1–R8)
features/exit_payment.feature     C1 @smoke, C2 @boundary, C3 @negative (+ extra R5 cap-order @boundary)
features/environment.py           hook: fresh ParkEase before every scenario
features/steps/parameter_types.py custom types: Amount ("Rs. 1,000" -> 1000), Duration, ...
features/steps/parkease_steps.py  thin step definitions (no fee arithmetic)
.github/workflows/smoke.yml       bonus: runs @smoke on every push, uploads HTML report
```
