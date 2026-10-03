# NYC Airbnb Price & Availability Analyzer — Implementation Plan

## 1. Project Overview

The NYC Airbnb Price & Availability Analyzer is a small Python command-line data-analysis application.

The application will read the included New York City Airbnb Open Data CSV file and provide useful summary analysis of Airbnb listings, including price and availability information.

The project is intentionally limited in scope. It will use:

- Python
- pandas for data processing
- pytest for automated testing
- Docker for containerization and reproducibility

The project will not use:

- Machine learning
- Web scraping
- A database
- A web application
- A visualization framework
- An external API
- Docker Compose
- Multi-stage Docker builds
- An additional CLI framework
- Unnecessary dependency-management or packaging tools

The application will maintain a clear separation between:

1. Data loading and cleaning.
2. Data analysis.
3. Command-line interaction.

This separation allows the analysis functions to be independently tested.

Docker will provide a reproducible environment containing the application, dependencies, tests, and dataset.

---

# 2. Project Requirements

The application must:

- Read the included `data/AB_NYC_2019.csv`.
- Verify that the actual dataset contains the columns required by the application.
- Perform documented data cleaning.
- Provide useful summary analysis through a command-line interface.
- Handle invalid user input gracefully.
- Handle empty or completely invalid analysis data without crashing or displaying misleading `NaN` results.
- Include meaningful automated tests.
- Include the dataset in the repository.
- Include setup and usage documentation.
- Include a Dockerfile.
- Include a `.dockerignore`.
- Provide a containerized way to run the CLI.
- Provide a containerized way to run automated tests.
- Include Docker build and run instructions.
- Verify that the built image actually runs a meaningful part of the project.
- Document the containerization smoke test.
- Document AI-assisted development decisions.
- Document independent verification.

The application will provide four main analyses:

1. Overall summary.
2. Price statistics by neighbourhood group.
3. Price statistics by room type.
4. Availability summary.

The availability summary must include:

- Average availability.
- Median availability.
- Number of listings with zero availability.
- Percentage of listings with zero availability.

The project will not include machine learning, web scraping, databases, visualization frameworks, APIs, web interfaces, Docker Compose, or other unnecessary functionality.

---

# 3. Repository Structure

```text
repository-b/
│
├── data/
│   └── AB_NYC_2019.csv
│
├── src/
│   └── nyc_airbnb/
│       ├── __init__.py
│       ├── cli.py
│       ├── data_loader.py
│       └── analysis.py
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   └── fixtures/
│       └── small_airbnb.csv
│
├── docs/
│   └── plan.md
│
├── README.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .gitignore
```

There will be no `pyproject.toml`.

`requirements.txt` will be the project's dependency specification.

There will be no Docker Compose configuration.

---

# 4. File Responsibilities

## `data/AB_NYC_2019.csv`

Contains the project's supplied copy of the New York City Airbnb Open Data dataset.

The application will read this file but will not modify the source CSV.

The dataset will be copied into the Docker image so the standard containerized application is self-contained.

The Builder must inspect the actual file and verify its structure rather than treating the expected schema as guaranteed.

## `src/nyc_airbnb/data_loader.py`

Responsible for:

- Loading the CSV with pandas.
- Checking that required columns exist.
- Performing the documented data-cleaning operations.
- Returning data suitable for analysis.

The data loader should not contain the application's summary-analysis calculations.

## `src/nyc_airbnb/analysis.py`

Contains independently testable analysis functions.

Expected functionality includes:

- Overall summary.
- Price by neighbourhood group.
- Price by room type.
- Availability summary.

Analysis functions should accept DataFrames or cleaned data and return analysis results.

They should not depend on command-line input.

The analysis layer should explicitly handle situations in which there are no valid observations for a particular calculation.

## `src/nyc_airbnb/cli.py`

Responsible for:

- Starting the application.
- Displaying the menu.
- Reading user choices.
- Calling analysis functions.
- Formatting and displaying results.
- Handling invalid menu choices.
- Returning to the menu.
- Exiting normally.

The CLI should not contain the core statistical calculations.

## `tests/test_data_loader.py`

Tests:

- Successful loading.
- Missing-file behavior.
- Required-column validation.
- Price cleaning.
- Other important data-cleaning behavior.
- Empty/invalid data handling where applicable.

## `tests/test_analysis.py`

Tests:

- Overall statistics.
- Price calculations.
- Neighbourhood-group grouping.
- Room-type grouping.
- Availability calculations.
- Zero-availability counts.
- Zero-availability percentages.
- Extreme valid prices.
- No-valid-data behavior.
- Important edge cases.

## `tests/fixtures/small_airbnb.csv`

A small deterministic CSV used for automated tests.

It should contain enough controlled examples to test:

- Valid prices.
- Non-numeric prices.
- Zero prices.
- Negative prices.
- An unusually large valid positive price.
- Multiple neighbourhood groups.
- Multiple room types.
- Multiple availability values.
- At least one zero-availability listing.
- Missing values where relevant.

The fixture should be small enough that expected results can be calculated manually.

## `README.md`

Documents:

- Project purpose.
- Dataset.
- Features.
- Data-cleaning decisions.
- Installation.
- Local usage.
- Testing.
- Docker prerequisites.
- Docker build instructions.
- Containerized CLI usage.
- Containerized test usage.
- Manual CLI smoke test.
- Docker smoke test.
- AI-assisted workflow.
- Accepted AI recommendation.
- Changed/rejected AI recommendation.
- Independent verification.

## `requirements.txt`

Contains the project's direct Python dependencies.

The required dependencies are:

- pandas
- pytest

The Builder must deliberately select compatible versions after verifying the chosen Python version and dependency compatibility.

The project should not introduce additional dependency-management tools.

## `Dockerfile`

Defines the reproducible runtime environment.

It should:

- Use a deliberately selected Python version.
- Install the deliberately selected compatible pandas and pytest versions.
- Set a predictable working directory.
- Copy the application source.
- Copy the tests.
- Copy the dataset.
- Configure the Python import path.
- Launch the CLI by default.

The Dockerfile should remain straightforward and should not use unnecessary infrastructure.

## `.dockerignore`

Excludes unnecessary local files from the Docker build context.

It should exclude items such as:

```text
.git/
.gitignore
.dockerignore
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
env/
.idea/
.vscode/
.DS_Store
```

It must not exclude:

```text
data/AB_NYC_2019.csv
src/
tests/
requirements.txt
Dockerfile
```

## `.gitignore`

Excludes local development artifacts such as:

- Virtual environments.
- Python cache directories.
- pytest cache.
- IDE-specific files.
- Other generated development files.

---

# 5. Python Package and Import Architecture

The project will use the `src` layout:

```text
src/
└── nyc_airbnb/
```

Application modules must import the package as:

```text
nyc_airbnb
```

and **not** as:

```text
src.nyc_airbnb
```

This keeps the application's imports independent of the repository directory name.

The project must make the package importable consistently in:

1. Local application execution.
2. Local pytest execution.
3. Docker CLI execution.
4. Docker pytest execution.

The implementation should use a simple mechanism for exposing `src/` to Python.

The project should not introduce a packaging framework solely to solve this problem.

The Builder must verify all four execution contexts before considering the import architecture complete.

---

# 6. Data Format and Dataset Verification

The project uses the New York City Airbnb Open Data dataset from 2019.

The expected repository file is:

```text
data/AB_NYC_2019.csv
```

The plan expects approximately 49,000 listings and 16 columns, but these values are **assumptions that must be independently verified against the actual repository file**.

The Builder must inspect the actual dataset before implementation is considered complete.

At minimum, the Builder should verify:

- Actual row count.
- Actual column names.
- Data types of relevant columns.
- Presence of `price`.
- Presence of `availability_365`.
- Presence of `neighbourhood_group`.
- Presence of `room_type`.
- Missing values in relevant fields.
- Minimum and maximum relevant numeric values.
- Whether non-numeric price values actually occur.
- Whether zero or negative prices occur.
- Whether zero availability values occur.
- Actual categorical values in the grouping columns.

The application should validate required columns at runtime rather than assuming that the expected schema is guaranteed.

The Builder should not add cleaning rules merely because an assumed problem was mentioned in the plan. Cleaning decisions should be based on the documented project requirements and verified dataset behavior.

---

# 7. Data-Cleaning Decisions

Cleaning will be limited to decisions necessary for reliable analysis.

## 7.1 Price cleaning rule

The project explicitly defines:

> Prices that are non-numeric or less than or equal to zero are excluded from price-based calculations.

This is an intentional project decision.

A non-numeric price cannot be used in numeric price calculations.

A price of zero or below is excluded because the analysis is intended to describe positive Airbnb listing prices.

The application must therefore use only valid positive numeric prices for price-based calculations.

This rule must be documented and tested.

## 7.2 Valid extreme prices

Valid positive extreme prices will **not** automatically be removed.

There will be no arbitrary maximum-price cutoff.

There will be no automatic statistical outlier-removal procedure.

If a price is numeric and greater than zero, it remains eligible for price-based calculations regardless of how large it is.

The application will report both:

- Mean price.
- Median price.

This allows the effect of unusually large valid prices to be considered.

This is an explicit project decision rather than an accidental consequence of implementation.

## 7.3 Missing values

Missing values will be handled according to the specific analysis.

The project will not delete every row containing any missing value.

For example:

- Price analysis requires a valid positive numeric price.
- Availability analysis requires usable availability.
- Neighbourhood analysis requires a usable neighbourhood group.
- Room-type analysis requires a usable room type.

Missing values unrelated to the current calculation should not unnecessarily remove otherwise usable observations.

## 7.4 Availability

`availability_365` will be treated as a numeric analysis variable.

The Builder must verify its actual data type and values.

Rows without usable availability values will not be included in availability calculations.

---

# 8. Explicit No-Valid-Data Behavior

The application must explicitly handle cases where an analysis has no usable observations.

It must not:

- Crash because a calculation receives an empty dataset.
- Display misleading `NaN` results to the CLI user.
- Divide by zero when calculating a percentage.

Examples include:

- Every price is invalid.
- Every availability value is missing/invalid.
- A filtered group has no valid price observations.
- An analysis receives an empty DataFrame.

For these situations, the analysis layer should return an identifiable no-data result.

The CLI should convert that result into a clear message, such as:

```text
No valid price data available for this analysis.
```

or:

```text
No valid availability data available for this analysis.
```

The exact wording can be selected during implementation.

For the zero-availability percentage:

```text
zero-availability percentage =
    (number of valid listings with availability == 0 /
     number of listings with valid availability) × 100
```

If there are no valid availability observations, the percentage must not be calculated.

The tests must explicitly verify this behavior.

This requirement should remain simple; the project does not need a general-purpose error-handling framework.

---

# 9. Core Functionality

## 9.1 Overall Summary

Display:

- Number of listings represented by the analysis.
- Average price.
- Median price.
- Average availability.
- Median availability.

Price statistics use only valid positive numeric prices.

Availability statistics use valid availability observations.

If no valid data exists for a statistic, display the project's no-data message instead of `NaN`.

## 9.2 Price by Neighbourhood Group

Group listings by `neighbourhood_group`.

Display:

- Number of listings with valid prices.
- Average price.
- Median price.

The application should use the actual categorical values present in the dataset rather than hard-coding a fixed list of neighbourhood groups.

## 9.3 Price by Room Type

Group listings by `room_type`.

Display:

- Number of listings with valid prices.
- Average price.
- Median price.

The implementation should use actual values found in the dataset.

## 9.4 Availability Summary

Display all four required measures:

1. Average availability.
2. Median availability.
3. Number of listings with zero availability.
4. Percentage of listings with zero availability.

The percentage denominator must be the number of valid availability observations.

---

# 10. CLI Design

The CLI will use a simple menu.

Expected structure:

```text
NYC Airbnb Price & Availability Analyzer

1. Overall summary
2. Price by neighbourhood group
3. Summary by room type
4. Availability summary
5. Exit

Select an option:
```

The user should be able to:

1. Select an analysis.
2. View results.
3. Return to the menu.
4. Exit.

Invalid menu choices should produce a readable error message rather than crash the program.

The CLI should use standard Python functionality.

No external CLI framework is required.

---

# 11. Docker Architecture

## 11.1 Purpose

Docker will provide a reproducible environment containing:

- A deliberately selected Python version.
- pandas.
- pytest.
- Application source.
- Tests.
- The repository's dataset.

The goal is to allow another developer to build the application from the repository and run it without depending on their host Python environment.

## 11.2 Docker Compose decision

Docker Compose is explicitly out of scope.

The application has:

- One Python CLI.
- No database.
- No web server.
- No worker.
- No message queue.
- No second service.

Therefore, Compose would add configuration without providing an architectural benefit.

The project will use one Dockerfile and one application image.

## 11.3 Dataset strategy

The dataset will be **copied into the Docker image**.

The standard containerized application will therefore contain the project's exact repository copy of:

```text
data/AB_NYC_2019.csv
```

The Docker build must not download the dataset from Kaggle.

This provides:

- A self-contained image.
- A reproducible input dataset.
- Simpler Docker commands.
- A simpler grading smoke test.
- No runtime dependency on an external dataset source.

A host volume is **not part of the required workflow**.

An optional development volume could technically be used, but it should not be necessary for building, running, or testing the assignment.

The README's primary Docker instructions should therefore use the self-contained image.

## 11.4 Working directory

The container should use a predictable working directory such as:

```text
/app
```

The expected structure will resemble:

```text
/app/
├── data/
├── src/
└── tests/
```

## 11.5 Python path

The container must make:

```text
/app/src
```

available to Python so that:

```text
nyc_airbnb
```

can be imported.

The same package import convention must work locally.

The project should not use `src.nyc_airbnb` imports.

## 11.6 Default container command

The image should launch the CLI by default.

Conceptually:

```text
docker build -t nyc-airbnb-analyzer .
docker run --rm -it nyc-airbnb-analyzer
```

The exact Python invocation will be selected during implementation.

The important requirement is that a normal container run launches the analyzer rather than opening a shell.

## 11.7 Running tests inside Docker

The image should contain pytest and the test suite.

The test suite should be runnable by overriding the default command:

```text
docker run --rm nyc-airbnb-analyzer pytest
```

This should use the same Python environment and dependencies contained in the application image.

---

# 12. Docker Version and Dependency Strategy

The Builder must deliberately select compatible versions for:

- Python.
- pandas.
- pytest.

The Architect does not prescribe arbitrary versions in advance.

Instead, the Builder must:

1. Select a specific supported Python version.
2. Select compatible pandas and pytest versions.
3. Record those versions in `requirements.txt` and the Dockerfile as appropriate.
4. Verify that the selected versions work together.
5. Run the automated tests using that environment.
6. Run the actual application inside the resulting Docker image.

The project should not add:

- Poetry.
- Pipenv.
- Conda.
- A separate lockfile system.
- A dependency manager beyond `requirements.txt`.

The chosen versions should be documented in the README so another developer knows which environment was verified.

The Builder should avoid using floating `latest` tags where doing so would weaken reproducibility.

---

# 13. Dockerfile Requirements

The Dockerfile should:

1. Use a deliberately selected Python base version.
2. Set the working directory.
3. Copy `requirements.txt`.
4. Install the selected compatible dependencies.
5. Copy `src/`.
6. Copy `tests/`.
7. Copy `data/`.
8. Configure the Python path so `nyc_airbnb` imports correctly.
9. Define the default CLI command.

The Dockerfile should remain straightforward.

It should not contain:

- Multiple application services.
- A database.
- Docker Compose.
- Multi-stage builds.
- Application logic.
- Dataset downloads from Kaggle.
- Unnecessary operating-system packages.

---

# 14. `.dockerignore` Requirements

The `.dockerignore` file should prevent irrelevant files from entering the Docker build context.

It should exclude:

```text
.git/
.gitignore
.dockerignore
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
env/
.idea/
.vscode/
.DS_Store
```

The following must remain available to the Docker build:

```text
data/AB_NYC_2019.csv
src/
tests/
requirements.txt
Dockerfile
```

---

# 15. Testing Strategy

The project will use four distinct verification layers.

These layers have different purposes and should not duplicate one another unnecessarily.

## Layer 1 — Automated Unit Tests

Use pytest and the small fixture dataset.

Test:

- Data loading.
- Required-column validation.
- Price cleaning.
- Mean price.
- Median price.
- Grouped price calculations.
- Availability calculations.
- Zero-availability count.
- Zero-availability percentage.
- Extreme valid prices.
- No-valid-data behavior.
- Important edge cases.

The tests should verify calculations with known expected values.

## Layer 2 — Local CLI Smoke Test

Use the actual `AB_NYC_2019.csv`.

Verify:

- Application launches.
- Menu appears.
- Each analysis can be selected.
- Results are displayed.
- Availability output includes all four required measures.
- Invalid menu input does not crash the application.
- Exit works normally.

This verifies integration and user-facing behavior.

## Layer 3 — Docker Smoke Test

Build the image and launch the container.

Verify:

- Image builds successfully.
- CLI launches.
- Dataset is available inside the image.
- A meaningful analysis runs successfully.

The Docker smoke test must demonstrate actual application functionality, not merely that the container starts.

## Layer 4 — Automated Tests Inside Docker

Run:

```text
docker run --rm nyc-airbnb-analyzer pytest
```

Verify that the full automated test suite executes successfully inside the container.

This verifies that the reproducible environment can run both the application and its tests.

---

# 16. Automated Test Cases

The fixture should allow deterministic tests for the following.

## Normal price calculation

Verify expected mean and median for known valid positive prices.

## Non-numeric price

Verify that a non-numeric price does not enter price-based calculations.

## Zero price

Verify that a price of `0` is excluded.

## Negative price

Verify that a negative price is excluded.

## Extreme valid price

Include an unusually large positive price.

Verify that:

- It remains included.
- It affects the mean.
- It remains represented in the median calculation according to normal statistical rules.

This confirms that valid extreme values are not silently treated as invalid.

## Missing price

Verify that a missing price does not cause the application to crash and is not used as a valid price observation.

## Availability

Verify:

- Mean availability.
- Median availability.
- Zero-availability count.
- Zero-availability percentage.

## No valid price data

Provide data in which every price is invalid.

Verify that the analysis produces a no-data result rather than `NaN` output or an exception.

## No valid availability data

Provide data with no usable availability observations.

Verify that:

- No availability statistic is misleadingly displayed.
- No division-by-zero occurs.
- The CLI can report that availability data is unavailable.

## Empty data

Verify that an empty DataFrame does not cause an unexpected crash.

## Group with no valid price observations

Verify that one group lacking usable prices is handled without crashing the entire analysis.

## CLI invalid input

Verify that an invalid menu choice results in a readable error and allows the application to continue.

---

# 17. Potential Risks and Design Concerns

## 17.1 Import-path mistakes

The `src/` structure can cause local/Docker differences if the Python path is configured inconsistently.

The Builder must verify:

- Local CLI imports.
- Local pytest imports.
- Docker CLI imports.
- Docker pytest imports.

Application imports must use `nyc_airbnb`, not `src.nyc_airbnb`.

## 17.2 Dependency compatibility

The selected Python, pandas, and pytest versions must be tested together.

Versions should not be selected arbitrarily.

The Builder must document the verified combination.

## 17.3 Dataset assumptions

The expected dataset schema, row count, and value distributions are assumptions until verified.

The Builder must inspect the actual repository CSV.

## 17.4 Empty data

Pandas operations on empty data can produce `NaN`, empty results, warnings, or division-by-zero behavior.

The application must explicitly handle these situations.

## 17.5 Extreme prices

Valid extreme prices can substantially affect the mean.

The project intentionally keeps them.

Reporting both mean and median gives the user information with which to consider their effect.

## 17.6 Scope creep

The Builder should not add infrastructure or features simply because they are technically possible.

Do not add:

- Web UI.
- Database.
- Machine learning.
- API.
- Visualization framework.
- Docker Compose.
- Multi-stage Docker build.
- External CLI framework.
- Additional dependency manager.

---

# 18. Manual CLI Smoke Test

After implementation, perform the following test against the actual dataset.

## Step 1 — Launch

Start the application using the documented local command.

Verify that the menu appears.

## Step 2 — Overall summary

Select the overall summary.

Verify that it displays:

- Listing count.
- Average price.
- Median price.
- Average availability.
- Median availability.

## Step 3 — Neighbourhood analysis

Select price by neighbourhood group.

Verify that groups are displayed with:

- Valid listing count.
- Average price.
- Median price.

## Step 4 — Room-type analysis

Select the room-type analysis.

Verify that actual room types from the dataset are represented and that price statistics appear.

## Step 5 — Availability analysis

Verify all four required measures:

- Average availability.
- Median availability.
- Number of zero-availability listings.
- Percentage of zero-availability listings.

## Step 6 — Invalid input

Enter an invalid menu choice.

Verify that the application does not crash.

## Step 7 — Exit

Exit normally.

The README should document the actual smoke-test outcome after implementation.

---

# 19. Docker Smoke Test

After the local application has been verified:

## Step 1 — Build

Run:

```text
docker build -t nyc-airbnb-analyzer .
```

Verify that the image builds successfully.

## Step 2 — Launch

Run:

```text
docker run --rm -it nyc-airbnb-analyzer
```

Verify that the CLI menu appears.

## Step 3 — Meaningful analysis

Select the overall summary.

Verify that the application successfully reads the dataset **from inside the image** and produces meaningful results.

No host dataset volume should be required.

## Step 4 — Test inside container

Run:

```text
docker run --rm nyc-airbnb-analyzer pytest
```

Verify that the automated test suite executes successfully.

## Step 5 — Verify import consistency

Confirm that the same `nyc_airbnb` package imports work inside Docker as they do locally.

The README should document the actual results rather than claiming successful verification before it occurs.

---

# 20. Reproducibility Requirements

The project should be reproducible without introducing unnecessary tooling.

Reproducibility will be supported by:

- A specific Python version.
- Explicitly selected compatible pandas and pytest versions.
- `requirements.txt`.
- A Dockerfile.
- The repository-contained dataset.
- No runtime dataset download.
- A predictable Docker working directory.
- A consistent `nyc_airbnb` import path.
- Containerized automated tests.

The exact Python and dependency versions must be selected and verified by the Builder.

The dataset version is represented by the CSV committed to the repository.

The Docker image must use that repository copy rather than downloading a potentially different dataset.

---

# 21. Documentation Requirements

The README must contain the following sections or equivalent information.

## Project overview

Explain:

- What the application does.
- Why the project exists.
- What data it uses.

## Dataset

Identify:

- New York City Airbnb Open Data.
- The Kaggle source.
- The repository location of the CSV.

The README should clearly state that the application uses the dataset included in the repository.

## Data-cleaning decisions

Document:

- Non-numeric prices are excluded.
- Zero and negative prices are excluded.
- Valid positive extreme prices are retained.
- Mean and median are both reported.
- Missing values are handled according to the specific analysis.

## Installation

Explain local Python setup using:

```text
requirements.txt
```

No additional package-management system should be required.

## Usage

Document the local CLI command.

## Testing

Document the local pytest command.

## Docker

Document:

- Docker prerequisite.
- Build command.
- Containerized CLI command.
- Containerized test command.
- Dataset inclusion strategy.
- The fact that a volume is not required.

## Manual smoke test

Document the local smoke-test procedure and actual verification result.

## Containerization smoke test

Document:

- Docker build.
- Container launch.
- Meaningful analysis.
- Tests inside Docker.
- Verification that the dataset is available inside the image.

## AI-assisted workflow

Document:

- How AI was used during planning/development.
- An AI recommendation that was accepted.
- An AI recommendation that was changed or rejected.
- Why the decision was made.
- How the resulting implementation was independently verified.

The documentation must describe actual development decisions rather than inventing a workflow that did not occur.

---

# 22. Final Verification Checklist

## Dataset

- [ ] Actual CSV structure inspected.
- [ ] Actual row count verified.
- [ ] Actual column names verified.
- [ ] Relevant data types inspected.
- [ ] Relevant missing values inspected.
- [ ] Price range inspected.
- [ ] Availability values inspected.
- [ ] Actual categorical values inspected.
- [ ] Required columns validated by application code.

## Data cleaning

- [ ] Non-numeric prices excluded.
- [ ] Zero prices excluded.
- [ ] Negative prices excluded.
- [ ] Valid positive extreme prices retained.
- [ ] Mean and median both reported.
- [ ] Missing values handled appropriately.

## Empty-data behavior

- [ ] Empty DataFrame handled.
- [ ] No-valid-price case handled.
- [ ] No-valid-availability case handled.
- [ ] No division by zero.
- [ ] CLI does not display misleading `NaN` for no-data cases.

## Package/import architecture

- [ ] `src/nyc_airbnb` structure used.
- [ ] Application imports use `nyc_airbnb`.
- [ ] No `src.nyc_airbnb` application imports.
- [ ] Local imports verified.
- [ ] Docker imports verified.
- [ ] Local pytest imports verified.
- [ ] Docker pytest imports verified.

## Dependencies

- [ ] Specific Python version selected.
- [ ] Compatible pandas version selected.
- [ ] Compatible pytest version selected.
- [ ] Compatibility verified.
- [ ] Versions documented.
- [ ] No unnecessary dependency-management tools added.

## Tests

- [ ] Unit tests pass locally.
- [ ] Price-cleaning rules tested.
- [ ] Extreme valid prices tested.
- [ ] Availability measures tested.
- [ ] No-data behavior tested.
- [ ] Important edge cases tested.
- [ ] CLI invalid input tested.

## Docker

- [ ] Dockerfile present.
- [ ] `.dockerignore` present.
- [ ] Image builds successfully.
- [ ] Dataset copied into image.
- [ ] No dataset volume required.
- [ ] CLI launches from container.
- [ ] Meaningful analysis runs from container.
- [ ] pytest runs inside container.
- [ ] Docker Compose not added.
- [ ] Multi-stage build not added.
- [ ] Unnecessary infrastructure not added.

## Documentation

- [ ] README explains project.
- [ ] README explains dataset.
- [ ] README explains cleaning decisions.
- [ ] README explains local installation.
- [ ] README explains local usage.
- [ ] README explains local testing.
- [ ] README explains Docker.
- [ ] README explains Docker smoke test.
- [ ] README explains AI-assisted workflow.
- [ ] README documents accepted AI recommendation.
- [ ] README documents changed/rejected AI recommendation.
- [ ] README documents independent verification.
- [ ] `docs/plan.md` matches final architecture.

---

# 23. Suggested Development Sequence

## Phase 1 — Inspect the actual repository and dataset

1. Confirm the repository structure.
2. Inspect `AB_NYC_2019.csv`.
3. Verify actual columns.
4. Verify actual row count.
5. Inspect relevant data types.
6. Inspect relevant missing values.
7. Inspect price values.
8. Inspect availability values.
9. Inspect neighbourhood-group and room-type values.

The Builder must perform these checks before treating dataset assumptions as facts.

## Phase 2 — Establish the Python environment

10. Select a specific Python version.
11. Select compatible pandas and pytest versions.
12. Verify compatibility.
13. Record the selected versions in `requirements.txt`.
14. Document the selected environment.

## Phase 3 — Repository foundation

15. Create the `src/nyc_airbnb` package.
16. Create the tests directory.
17. Create the deterministic test fixture.
18. Create `.gitignore`.

## Phase 4 — Data loading

19. Implement CSV loading.
20. Validate required columns.
21. Implement the explicit price-cleaning rule.
22. Implement appropriate missing-value handling.
23. Add data-loader tests.

## Phase 5 — Analysis

24. Implement overall summary.
25. Implement neighbourhood-group price analysis.
26. Implement room-type price analysis.
27. Implement availability analysis.
28. Implement explicit no-valid-data behavior.
29. Add analysis tests.
30. Add edge-case tests.
31. Verify extreme valid prices remain included.

## Phase 6 — CLI

32. Implement the simple menu.
33. Connect menu options to analysis functions.
34. Handle invalid input.
35. Implement normal exit.
36. Verify CLI behavior locally.

## Phase 7 — Local verification

37. Run all pytest tests.
38. Fix implementation issues.
39. Re-run pytest.
40. Perform the complete local CLI smoke test.

## Phase 8 — Docker

41. Select and document the final Python base image/version.
42. Create the Dockerfile.
43. Configure `/app` as the working directory.
44. Make `/app/src` available to Python.
45. Copy source, tests, and dataset into the image.
46. Install the selected dependency versions.
47. Configure the CLI as the default command.
48. Create `.dockerignore`.

## Phase 9 — Docker verification

49. Build the image.
50. Launch the CLI inside the container.
51. Run a meaningful analysis using the bundled dataset.
52. Run pytest inside the container.
53. Verify imports work in Docker.
54. Record the actual results.

## Phase 10 — Documentation

55. Complete README installation instructions.
56. Complete local usage instructions.
57. Complete testing instructions.
58. Complete Docker instructions.
59. Document data-cleaning decisions.
60. Document the local smoke test.
61. Document the Docker smoke test.
62. Document the AI-assisted workflow.
63. Document accepted and changed/rejected AI recommendations.
64. Document independent verification.

## Phase 11 — Final review

65. Compare implementation against `docs/plan.md`.
66. Verify all tests pass locally.
67. Verify all tests pass in Docker.
68. Verify local smoke test.
69. Verify Docker smoke test.
70. Verify no unnecessary infrastructure was introduced.
71. Verify repository cleanliness.
72. Verify documentation accurately describes what was actually done.

---

# 24. Final Architectural Decisions

The final architecture is intentionally small:

```text
                 AB_NYC_2019.csv
                        │
                        ▼
               ┌─────────────────┐
               │ Data Loader     │
               │ + Cleaning      │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ Analysis        │
               │ Functions       │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ CLI             │
               │ User Interface  │
               └─────────────────┘
```

The application is contained within:

```text
Docker Image
├── Selected Python version
├── Selected pandas version
├── Selected pytest version
├── src/nyc_airbnb/
├── tests/
└── data/AB_NYC_2019.csv
```

The final decisions are:

1. **Use `src/nyc_airbnb` as the Python package structure.**
2. **Application imports use `nyc_airbnb`, never `src.nyc_airbnb`.**
3. **Verify imports in local CLI, local pytest, Docker CLI, and Docker pytest environments.**
4. **Use only `requirements.txt` for dependency specification.**
5. **Select and verify compatible Python, pandas, and pytest versions rather than choosing arbitrary versions in advance.**
6. **Copy the repository's CSV into the Docker image.**
7. **Do not require a dataset volume.**
8. **Do not download the dataset during the Docker build.**
9. **Use one straightforward Dockerfile.**
10. **Do not use Docker Compose.**
11. **Do not use multi-stage builds.**
12. **Do not add an external CLI framework.**
13. **Exclude non-numeric, zero, and negative prices from price calculations.**
14. **Retain valid positive extreme prices.**
15. **Report both mean and median price.**
16. **Report all four required availability measures.**
17. **Explicitly handle empty and no-valid-data cases without misleading `NaN` output or division by zero.**
18. **Verify actual dataset characteristics before relying on dataset assumptions.**
19. **Use four distinct verification layers:**
    - Automated unit tests.
    - Local CLI smoke test.
    - Docker smoke test.
    - Automated tests inside Docker.
20. **Keep the implementation and infrastructure proportional to a small college command-line project.**

The Builder should treat this document as the architectural contract while still independently verifying factual assumptions about the actual dataset, Python environment, dependency compatibility, and resulting implementation.
