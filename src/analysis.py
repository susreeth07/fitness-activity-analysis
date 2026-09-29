"""
TEAM 6 – FITNESS ACTIVITY DATA ANALYSIS
College Practicum: Git & GitHub Data Analysis Project

This script performs the complete data analysis pipeline:
1. Loads daily activity and sleep datasets.
2. Explores and cleans the data (date conversion, missing value verification, duplicate removal).
3. Computes summary statistics, average steps, and average calories burned.
4. Identifies low-activity days using a statistical threshold (lower quartile, Q1).
5. Merges activity data with sleep duration data.
6. Generates and saves the three required visualization plots into the results/ folder.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(activity_path="data/dailyActivity_merged.csv", sleep_path="data/sleepDay_merged.csv"):
    """
    Loads the activity and sleep datasets from relative CSV paths.
    """
    print(f"Loading activity dataset from: {activity_path}")
    activity_df = pd.read_csv(activity_path)

    print(f"Loading sleep dataset from: {sleep_path}")
    sleep_df = pd.read_csv(sleep_path)

    return activity_df, sleep_df


def inspect_data(activity_df, sleep_df):
    """
    Prints key inspection metrics: shapes, column names, missing values, duplicates.
    """
    print("\n" + "=" * 50)
    print("DATASET INSPECTION")
    print("=" * 50)

    print(f"\nActivity Dataset Shape: {activity_df.shape[0]} rows, {activity_df.shape[1]} columns")
    print(f"Sleep Dataset Shape: {sleep_df.shape[0]} rows, {sleep_df.shape[1]} columns")

    print("\nActivity Dataset Missing Values:")
    print(activity_df.isnull().sum())

    print("\nSleep Dataset Missing Values:")
    print(sleep_df.isnull().sum())

    print(f"\nActivity Dataset Duplicates: {activity_df.duplicated().sum()}")
    print(f"Sleep Dataset Duplicates: {sleep_df.duplicated().sum()}")


def clean_data(activity_df, sleep_df):
    """
    Cleans datasets:
    - Converts date strings to datetime objects using exact date formats.
    - Handles missing values (none found in raw data).
    - Removes duplicate rows in sleep data.
    """
    print("\n" + "=" * 50)
    print("DATA CLEANING & PREPROCESSING")
    print("=" * 50)

    # Convert date columns to datetime
    activity_cleaned = activity_df.copy()
    sleep_cleaned = sleep_df.copy()

    activity_cleaned["Date"] = pd.to_datetime(activity_cleaned["ActivityDate"], format="%m/%d/%Y")
    sleep_cleaned["Date"] = pd.to_datetime(sleep_cleaned["SleepDay"], format="%m/%d/%Y %I:%M:%S %p")

    # Missing value handling
    # The dataset contains 0 missing values; we log this explicitly
    print("Missing value check: No missing values found in either dataset.")

    # Duplicate removal
    sleep_duplicates = sleep_cleaned.duplicated().sum()
    if sleep_duplicates > 0:
        print(f"Found {sleep_duplicates} duplicate records in sleep dataset. Removing duplicates...")
        sleep_cleaned = sleep_cleaned.drop_duplicates().reset_index(drop=True)
    else:
        print("No duplicate records found in sleep dataset.")

    print(f"Cleaned Activity records: {len(activity_cleaned)}")
    print(f"Cleaned Sleep records: {len(sleep_cleaned)}")

    return activity_cleaned, sleep_cleaned


def calculate_statistics(activity_df):
    """
    Calculates summary statistics:
    - Average daily steps
    - Average daily calories burned
    - Summary distribution of key activity metrics
    """
    print("\n" + "=" * 50)
    print("ACTIVITY STATISTICS")
    print("=" * 50)

    avg_steps = activity_df["TotalSteps"].mean()
    avg_calories = activity_df["Calories"].mean()

    print(f"Average Daily Steps: {avg_steps:.2f}")
    print(f"Average Daily Calories Burned: {avg_calories:.2f} kcal")

    key_columns = ["TotalSteps", "Calories", "TotalDistance", "VeryActiveMinutes", "SedentaryMinutes"]
    summary_stats = activity_df[key_columns].describe()
    print("\nKey Activity Metrics Summary:")
    print(summary_stats.round(2))

    return avg_steps, avg_calories, summary_stats


def identify_low_activity_days(activity_df):
    """
    Identifies low-activity days using a defensible statistical threshold:
    The lower quartile (25th percentile, Q1) of TotalSteps.
    Days with step counts strictly below Q1 are classified as low-activity days.
    """
    print("\n" + "=" * 50)
    print("LOW-ACTIVITY DAYS IDENTIFICATION")
    print("=" * 50)

    q1_threshold = activity_df["TotalSteps"].quantile(0.25)
    low_activity_df = activity_df[activity_df["TotalSteps"] < q1_threshold]

    pct_low = (len(low_activity_df) / len(activity_df)) * 100

    print(f"Statistical Threshold (Q1 / 25th Percentile): {q1_threshold:.2f} steps")
    print(f"Total Observations: {len(activity_df)}")
    print(f"Low-Activity Days Count: {len(low_activity_df)} ({pct_low:.1f}% of total recorded days)")

    return q1_threshold, low_activity_df


def merge_activity_sleep(activity_df, sleep_df):
    """
    Merges activity and sleep datasets on participant 'Id' and normalized 'Date'.
    """
    print("\n" + "=" * 50)
    print("MERGING ACTIVITY & SLEEP DATA")
    print("=" * 50)

    merged_df = pd.merge(activity_df, sleep_df, on=["Id", "Date"], how="inner")
    print(f"Successfully merged {len(merged_df)} daily activity-sleep records.")

    return merged_df


def generate_visualizations(activity_df, merged_df, output_dir="results"):
    """
    Generates and saves the three required visualizations:
    1. Steps per day plot (results/steps_per_day.png)
    2. Calories burned plot (results/calories_burned.png)
    3. Sleep duration vs activity plot (results/sleep_vs_activity.png)
    """
    print("\n" + "=" * 50)
    print("GENERATING VISUALIZATIONS")
    print("=" * 50)

    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Aggregate daily averages across participants for time-series trend
    daily_trend = activity_df.groupby("Date")[["TotalSteps", "Calories"]].mean().reset_index()
    overall_avg_steps = activity_df["TotalSteps"].mean()
    overall_avg_calories = activity_df["Calories"].mean()

    # 1. Steps per Day Plot
    plt.figure(figsize=(12, 6))
    plt.plot(
        daily_trend["Date"],
        daily_trend["TotalSteps"],
        marker="o",
        color="#1f77b4",
        linewidth=2,
        label="Daily Average Steps"
    )
    plt.axhline(
        overall_avg_steps,
        color="#d62728",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Average ({overall_avg_steps:.0f} steps)"
    )
    plt.title("Daily Steps per Day Over Time", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Steps", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(frameon=True)
    plt.tight_layout()
    steps_path = os.path.join(output_dir, "steps_per_day.png")
    plt.savefig(steps_path, dpi=300)
    plt.close()
    print(f"Saved: {steps_path}")

    # 2. Calories Burned Plot
    plt.figure(figsize=(12, 6))
    plt.plot(
        daily_trend["Date"],
        daily_trend["Calories"],
        marker="s",
        color="#ff7f0e",
        linewidth=2,
        label="Daily Average Calories Burned"
    )
    plt.axhline(
        overall_avg_calories,
        color="#2ca02c",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Average ({overall_avg_calories:.0f} kcal)"
    )
    plt.title("Daily Calories Burned Over Time", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Calories Burned (kcal)", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(frameon=True)
    plt.tight_layout()
    calories_path = os.path.join(output_dir, "calories_burned.png")
    plt.savefig(calories_path, dpi=300)
    plt.close()
    print(f"Saved: {calories_path}")

    # 3. Sleep Duration vs Activity Plot
    plt.figure(figsize=(9, 6))
    sns.regplot(
        data=merged_df,
        x="TotalMinutesAsleep",
        y="TotalSteps",
        scatter_kws={"alpha": 0.6, "color": "#9467bd"},
        line_kws={"color": "#d62728", "linewidth": 2, "label": "Trend Line"}
    )
    plt.title("Sleep Duration vs. Daily Activity (Total Steps)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Sleep Duration (Total Minutes Asleep)", fontsize=12)
    plt.ylabel("Daily Activity (Total Steps)", fontsize=12)
    plt.legend(frameon=True)
    plt.tight_layout()
    sleep_path = os.path.join(output_dir, "sleep_vs_activity.png")
    plt.savefig(sleep_path, dpi=300)
    plt.close()
    print(f"Saved: {sleep_path}")


def main():
    """
    Main execution pipeline.
    """
    # 1. Load data
    activity_df, sleep_df = load_data()

    # 2. Inspect data
    inspect_data(activity_df, sleep_df)

    # 3. Clean data
    activity_cleaned, sleep_cleaned = clean_data(activity_df, sleep_df)

    # 4. Compute statistics
    calculate_statistics(activity_cleaned)

    # 5. Identify low-activity days
    identify_low_activity_days(activity_cleaned)

    # 6. Merge datasets for sleep vs activity analysis
    merged_df = merge_activity_sleep(activity_cleaned, sleep_cleaned)

    # 7. Generate visualizations
    generate_visualizations(activity_cleaned, merged_df)

    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE! All outputs and plots successfully generated.")
    print("=" * 50)


if __name__ == "__main__":
    main()
