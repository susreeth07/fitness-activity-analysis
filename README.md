# TEAM 6 – FITNESS ACTIVITY DATA ANALYSIS
**College Practicum: Git & GitHub Data Analysis Project**

---

## 1. Project Title
**Fitness Activity Data Analysis**

## 2. Project Objective
The objective of this practicum project is to develop an end-to-end data analysis workflow to study daily physical activity habits and health metrics recorded by personal fitness trackers. The project focuses on:
- Exploring daily physical activity indicators including total steps, distance traveled, activity intensities (very active, fairly active, lightly active, sedentary minutes), and calories burned.
- Analyzing sleep duration patterns (total minutes asleep and total time in bed).
- Applying data quality inspection (missing-value handling and duplicate detection).
- Computing key descriptive statistics (mean steps, mean calories burned, and distribution metrics).
- Applying a defensible statistical threshold to detect low-activity days.
- Studying the relationship between sleep duration and physical activity.
- Producing clean, presentation-ready visualizations.

---

## 3. Dataset Description
This project utilizes the Fitbit Fitness Tracker datasets provided for the practicum:
1. **`data/dailyActivity_merged.csv`**:
   - **Records**: 940 rows, 15 columns
   - **Participants**: 33 unique user IDs
   - **Date Range**: April 12, 2016 – May 12, 2016
   - **Key Columns**: `Id`, `ActivityDate`, `TotalSteps`, `TotalDistance`, `TrackerDistance`, `LoggedActivitiesDistance`, `VeryActiveDistance`, `ModeratelyActiveDistance`, `LightActiveDistance`, `SedentaryActiveDistance`, `VeryActiveMinutes`, `FairlyActiveMinutes`, `LightlyActiveMinutes`, `SedentaryMinutes`, `Calories`
2. **`data/sleepDay_merged.csv`**:
   - **Records**: 413 rows (raw), 5 columns
   - **Participants**: 24 unique user IDs
   - **Key Columns**: `Id`, `SleepDay`, `TotalSleepRecords`, `TotalMinutesAsleep`, `TotalTimeInBed`

---

## 4. Tools and Libraries Used
- **Python 3**: Core language used for data manipulation, cleaning, and computation.
- **pandas**: Used for data loading, data wrangling, date formatting, and statistical aggregation.
- **numpy**: Used for numerical computations.
- **matplotlib**: Used for plotting and exporting figures.
- **seaborn**: Used for enhanced statistical visualizations and regression scatter plots.
- **Jupyter Notebook**: Used for interactive, reproducible step-by-step reporting (`notebooks/analysis.ipynb`).
- **Git & GitHub**: Used for version control, repository organization, and practicum submission.

---

## 5. Analysis Performed
1. **Data Inspection & Quality Checks**:
   - Examined shapes, column schemas, and data types.
   - Evaluated missing values: both datasets contained **0 missing values** across all columns; thus, no imputation or artificial value replacement was needed.
   - Evaluated duplicates: `dailyActivity_merged.csv` had **0 duplicate rows**; `sleepDay_merged.csv` contained **3 exact duplicate records**, which were removed to retain 410 unique sleep observations.
2. **Data Preprocessing**:
   - Formatted `ActivityDate` (`%m/%d/%Y`) and `SleepDay` (`%m/%d/%Y %I:%M:%S %p`) into standard `datetime` objects (`Date`).
3. **Daily Activity Statistics**:
   - Computed mean, median, standard deviation, quartiles, and maximums for steps, calories, distances, and activity minutes.
4. **Low-Activity Days Identification**:
   - Rather than choosing an arbitrary number, a statistically sound threshold was chosen: the **First Quartile ($Q_1$, 25th percentile)** of `TotalSteps` ($3,789.75$ steps).
   - Filtered and characterized all days falling below this threshold.
5. **Sleep & Activity Integration**:
   - Merged activity and sleep records on participant `Id` and `Date` using an inner join, producing 410 matched daily records.
   - Evaluated the correlation between sleep duration (`TotalMinutesAsleep`) and step count (`TotalSteps`).

---

## 6. Visualizations Generated
All plots were generated with clear titles, labeled axes, visual legends, and exported to `results/`:
1. **`results/steps_per_day.png`**:
   - Line chart depicting average daily steps over time with an overall mean benchmark line ($7,638$ steps).
2. **`results/calories_burned.png`**:
   - Line chart depicting average daily caloric expenditure over time with an overall mean benchmark line ($2,304$ kcal).
3. **`results/sleep_vs_activity.png`**:
   - Scatter plot with a linear regression trend line analyzing the relationship between sleep duration (`TotalMinutesAsleep`) and physical activity (`TotalSteps`).

---

## 7. Observed Outputs & Results

| Metric / Analysis | Observed Value |
| :--- | :--- |
| **Total Activity Days Analyzed** | 940 records |
| **Cleaned Sleep Records** | 410 records (3 duplicates removed) |
| **Matched Activity-Sleep Days** | 410 records |
| **Average Daily Steps** | **7,637.91 steps** |
| **Median Daily Steps** | 7,405.50 steps |
| **Average Daily Calories Burned** | **2,303.61 kcal** |
| **Median Daily Calories Burned** | 2,134.00 kcal |
| **Low-Activity Threshold ($Q_1$)** | **3,789.75 steps** |
| **Low-Activity Days Count** | **235 days (25.0% of total)** |
| **Average Sedentary Time** | 991.21 minutes (~16.5 hours/day) |
| **Sleep vs. Steps Correlation ($r$)** | **-0.19** (slight negative correlation) |

---

## 8. Git Features Demonstrated (Practicum Assessment Guide)
During the manual Git/GitHub practicum assessment, the following Git features and workflows can be demonstrated:
1. **Repository Setup**: Initializing with `git init` and configuring user name and email.
2. **Ignoring Untracked Files**: Using `.gitignore` to omit virtual environment folders (`.env`), Python bytecode (`__pycache__/`, `*.pyc`), and Jupyter checkpoint artifacts (`.ipynb_checkpoints/`).
3. **Staging & Commit History**: Using `git add` and `git commit -m "<descriptive message>"` to document incremental progress (e.g., initial structure, data ingestion, analysis script, notebook outputs).
4. **Branching & Merging**: Creating feature branches (`git checkout -b feature/analysis`) to develop modules safely and merging them into `main`.
5. **Remote Collaboration**: Adding GitHub remote repositories (`git remote add origin <url>`), pushing commits (`git push -u origin main`), and handling pull requests / code reviews.

---

## Project Structure
```text
fitness-activity-analysis/
│
├── data/
│   ├── dailyActivity_merged.csv
│   └── sleepDay_merged.csv
│
├── docs/
│
├── notebooks/
│   └── analysis.ipynb
│
├── results/
│   ├── calories_burned.png
│   ├── sleep_vs_activity.png
│   └── steps_per_day.png
│
├── src/
│   └── analysis.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## How to Run the Analysis
From the project root directory:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Analysis Script**:
   ```bash
   python src/analysis.py
   ```

3. **Open Jupyter Notebook**:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```
