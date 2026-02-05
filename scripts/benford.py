import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def get_leading_digit(n):
    """
    Extracts the first significant digit (1-9) from a number.
    Returns None if the number is 0 or invalid.
    """
    try:
        val = abs(float(n))
        if val == 0:
            return None

        s = str(val)
        for char in s:
            if char in '123456789':
                return int(char)
        return None
    except (ValueError, TypeError):
        return None

def calculate_benford_stats(series):
    """
    Calculates observed counts/frequencies and expected Benford frequencies.
    Returns a DataFrame with Digit, Count, Observed_Freq, Expected_Freq.
    """
    # Extract leading digits
    leading_digits = series.apply(get_leading_digit).dropna().astype(int)

    # Filter for valid digits 1-9 (just in case)
    leading_digits = leading_digits[leading_digits.between(1, 9)]

    total_count = len(leading_digits)
    if total_count == 0:
        return None

    # Calculate observed counts
    observed_counts = leading_digits.value_counts().sort_index()

    # Create DataFrame
    stats = pd.DataFrame({'Digit': range(1, 10)})
    stats['Count'] = stats['Digit'].map(observed_counts).fillna(0).astype(int)
    stats['Observed_Freq'] = stats['Count'] / total_count

    # Calculate expected frequencies (Benford's Law)
    # P(d) = log10(1 + 1/d)
    stats['Expected_Freq'] = stats['Digit'].apply(lambda d: math.log10(1 + 1/d))
    stats['Expected_Count'] = stats['Expected_Freq'] * total_count

    return stats

def plot_benford(stats, title, filename):
    """
    Generates a bar chart comparing observed vs. expected frequencies and saves it.
    """
    if stats is None or stats.empty:
        print(f"No data to plot for {title}")
        return

    # Use seaborn style
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 6))

    # Prepare data for plotting (melt or just bar plot)
    # We can use simple bar plot with offset

    bar_width = 0.35
    index = np.arange(len(stats['Digit']))

    plt.bar(index, stats['Observed_Freq'], bar_width, label='Observed', color='skyblue', edgecolor='black')
    plt.bar(index + bar_width, stats['Expected_Freq'], bar_width, label='Expected (Benford)', color='salmon', edgecolor='black')

    plt.xlabel('Leading Digit', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(title, fontsize=14)
    plt.xticks(index + bar_width / 2, stats['Digit'])
    plt.legend()

    # Add summary stats text if needed? Maybe too crowded.

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
