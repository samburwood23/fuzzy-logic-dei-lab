# Women's Workplace Stress & DEI Analysis — Dataset Validation Notebook
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data_path = "../data/stress_dataset.csv"
df = pd.read_csv(data_path)

print("Dataset Shape:", df.shape)
df.head()

# Cleaning
df = df.dropna()
df = df.rename(columns=lambda x: x.strip().replace(" ", "_").lower())

print("Columns:", df.columns.tolist())

# Exploratory Analysis
sns.pairplot(df, diag_kind='kde')
plt.suptitle("Workplace Stress Dataset Overview", y=1.02)
plt.show()

sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# Fuzzy Simulation (placeholder)
df['fuzzy_stress_pred'] = (
    0.4 * df['workload'] +
    0.3 * (10 - df['support']) +
    0.3 * (10 - df['work_life_balance'])
)
df['fuzzy_stress_pred'] = (df['fuzzy_stress_pred'] / df['fuzzy_stress_pred'].max()) * 100

# Compare with ground truth
if 'stress_level' in df.columns:
    mse = mean_squared_error(df['stress_level'], df['fuzzy_stress_pred'])
    r2 = r2_score(df['stress_level'], df['fuzzy_stress_pred'])
    print(f"Fuzzy Model vs Dataset Stress Ratings → MSE: {mse:.2f}, R²: {r2:.2f}")

    sns.scatterplot(x=df['stress_level'], y=df['fuzzy_stress_pred'])
    plt.xlabel("Actual Stress Level")
    plt.ylabel("Fuzzy Predicted Stress")
    plt.title("Fuzzy System Validation Scatter Plot")
    plt.show()

# Save results
df.to_csv("../data/stress_validation_results.csv", index=False)
print("Validation results saved to data/stress_validation_results.csv")
