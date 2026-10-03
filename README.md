# NYC Airbnb Price & Availability Analyzer

A Python command-line application that analyzes the supplied New York City (NYC) Airbnb Open Data dataset. The purpose of this project is to report overall NYC Airbnb price and availability summaries, price statistics by neighbourhood group, price statistics by room type, and the required availability measures. 

## Project structure

```text
data/AB_NYC_2019.csv
src/nyc_airbnb/
tests/
docs/plan.md
Dockerfile
requirements.txt
```

The implementation follows `docs/plan.md` and intentionally does not add a database, web application, API, visualization framework, machine learning, Docker Compose, multi-stage Docker builds, or an external CLI framework.

## Dataset

The project uses the 2019 New York City Airbnb Open Data dataset, stored in `data/AB_NYC_2019.csv`. The exact repository CSV was inspected before implementation.

Verified characteristics:

- **48,895 rows and 16 columns**.
- Required columns include `price`, `availability_365`, `neighbourhood_group`, and `room_type`.
- `price` ranges from **0 to 10,000**; 11 listings have price 0 and no negative prices occur.
- `availability_365` ranges from **0 to 365** with no missing values.
- The five neighbourhood groups are Brooklyn, Manhattan, Queens, Staten Island, and Bronx.
- The three room types are Private room, Entire home/apt, and Shared room.
- `last_review` and `reviews_per_month` each have 10,052 missing values. These fields are not required by the application, so rows are not globally dropped because of those missing values.
- There are no duplicate listing IDs and no duplicate complete rows.

## Data cleaning

For price-based calculations, prices are converted to numeric values and only values greater than zero are included. Non-numeric, zero, and negative prices are excluded. Valid positive extreme prices are retained; there is no arbitrary price cap or statistical outlier-removal rule. Both mean and median are reported.

Availability is converted to numeric and missing/invalid values are excluded only from availability calculations. Other missing fields do not cause blanket row deletion.

The application validates the required analysis columns at runtime.

If an analysis has no valid observations, the analysis layer returns an explicit no-data result rather than exposing `NaN` or dividing by zero.

## Local installation

The verified environment uses **Python 3.12**, **pandas 2.2.3**, and **pytest 8.3.5**.

Create a virtual environment and install the dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Local usage

From the repository root:

```bash
PYTHONPATH=src python -m nyc_airbnb.cli
```

The menu provides:

1. Overall summary
2. Price by neighbourhood group
3. Summary by room type
4. Availability summary
5. Exit

Invalid menu choices are reported without terminating the program.

## Testing

From the repository root:

```bash
PYTHONPATH=src pytest
```

**Verified result:** 11 tests passed.

The deterministic fixture covers:

- valid prices
- non-numeric prices
- zero prices
- negative prices
- a large valid positive price
- missing price
- multiple neighbourhood groups
- multiple room types
- multiple availability values
- zero availability
- missing availability
- no-valid-data cases
- missing required columns
- missing dataset file

## Manual smoke test

The project was manually tested locally against the actual 48,895-row dataset on 2026-10-03.

The documented local setup instructions were followed successfully:

- python3.12 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt

The automated test suite was then run using the documented command: 

```bash
PYTHONPATH=src pytest
```

Result:

```text
11 passed in 0.42s
```

The CLI was then run using the documented command: 

```bash
PYTHONPATH=src python -m nyc_airbnb.cli
```

The following workflow was tested: 

```text
1 -> Overall summary
2 -> Price by neighbourhood group
3 -> Summary by room type
4 -> Availability summary
abc -> Invalid menu choice
5 -> Exit
```

The project started successfully. All four required analyses produced results, the invalid input was rejected without crashing, and the application exited normally.

Verified overall results from the supplied dataset:

- Listings: **48,895**
- Average price: **152.76**
- Median price: **106.00**
- Average availability: **112.78**
- Median availability: **45.00**

Verified availability results:

- Zero-availability listings: **17,533**
- Zero-availability percentage: **35.86%**

## Docker

Docker is required for the containerized workflow. The image is designed to contain the application, tests, dependencies, and the repository's exact CSV. No host volume and no runtime dataset download are required.

Build:

```bash
docker build -t nyc-airbnb-analyzer .
```

Run the CLI:

```bash
docker run --rm -it nyc-airbnb-analyzer
```

Run the automated tests inside the image:

```bash
docker run --rm nyc-airbnb-analyzer pytest
```

The Dockerfile uses `python:3.12-slim`, installs pandas 2.2.3 and pytest 8.3.5, uses `/app` as the working directory, copies `src/`, `tests/`, and `data/`, sets `PYTHONPATH=/app/src`, and launches the CLI by default.

### Docker verification status 

Docker was independently tested locally after the Builder phase.

The image was successfully built with: 

```bash
docker build -t nyc-airbnb-analyzer .
```

The build completed successfully and created the `nyc-airbnb-analyzer:latest` image.

The containerized CLI was then started with: 

```bash
docker run --rm -it nyc-airbnb-analyzer
```

The application started successfully, loaded the bundled dataset, produced the overall summary, and exited normally.

The Dockerized test suite was run with: 

```bash
docker run --rm nyc-airbnb-analyzer pytest
```

Result:

```text
11 passed in 0.17s
```

Therefore, the manual smoke test independently verified:

- Local installation and dependency setup
- Local automated tests
- Local CLI startup and required analyses
- Invalid CLI input handling
- Local clean exit
- Docker image build
- Docker CLI startup and analysis
- Docker automated tests
- Docker clean exit


### Smoke-test result

The manual smoke test successfully verified the documented setup, project startup, required analyses and outputs, invalid-input handling, normal exit, Docker image build, Dockerized application startup, and Dockerized automated tests.

## Import architecture

The application uses the `src/nyc_airbnb` package layout. Application imports use `nyc_airbnb`, never `src.nyc_airbnb`.

Locally, `PYTHONPATH=src` exposes the package. In Docker, `PYTHONPATH=/app/src` provides the same import convention.

## AI-assisted workflow and independent verification

AI was used in the Architect/Builder/Tester workflow to structure and review the implementation.

An accepted architectural recommendation was to keep the `src/nyc_airbnb` package and use `nyc_airbnb` as the import name rather than `src.nyc_airbnb`. This keeps application imports independent of the repository directory name.

The decision to avoid Docker Compose and other additional infrastructure was retained rather than expanded since this is a single CLI with no database, server, or second service.

Furthermore, during builder implementation, two issues were observed: one incorrect expected value in a test fixture and one robustness issue in the analysis layer. The fixture expectation was recalculated and corrected, and the analysis layer was changed to explicitly convert raw price values with pd.to_numeric(..., errors="coerce") before applying the positive-price rule. The complete test suite was then rerun successfully.

The tester independently compared the implementation with docs/plan.md, inspected the dataset and source files, evaluated the tests and edge cases, reviewed the CLI and Docker configuration, and checked the README.

No implementation defects requiring correction were identified. The tester reported the inability to perform a literal GitHub clone and Docker execution in its own environment as environmental limitations rather than project failures. The Tester independently verified the available source and test suite and reported 11/11 tests passing.

Independent verification included direct inspection of the exact supplied CSV before implementation, calculation of dataset characteristics from that file, deterministic unit tests with manually checkable fixture values, a local CLI smoke test using the real dataset, and review of the Docker configuration. Docker execution was independently tested locally after the Builder phase and rerun after the Tester review, including the image build, containerized CLI, and Dockerized test suite. 

## Scope

The project remains intentionally small and follows `docs/plan.md`:

- Python
- pandas
- pytest
- one Dockerfile
- one CLI
- repository-contained dataset
- no database
- no web application
- no API
- no machine learning
- no visualization framework
- no Docker Compose
- no multi-stage Docker build
- no external CLI framework
- no additional dependency-management system
