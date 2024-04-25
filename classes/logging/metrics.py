"""
TODO 4.5. Métriques de journalisation
- Ce fichier est fourni à titre d'exemple. 
- Vous pouvez vous en insipirer pour créer votre visualisation propre à vos métriques.
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#__name__ = "metrics"
__author__ = "CDL & <votre nom>"
__version__ = 1.0

def extract_log_metric(log_file):
    timestamps = []
    severities = []
    with open(log_file, "r") as fichier:
        lines = fichier.readlines()
    for line in lines:
        parts = line.strip().split("-") 
        if len(parts) >= 3:
            timestamps.append(parts[0])
            severities.append(parts[2].strip())
    return timestamps, severities


def plot_method(timestamps, severities):
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(timestamps),
        "severity": severities
    })
    df['count'] = np.ones(len(df), dtype=int)

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="timestamp", y=np.cumsum(df['count']), hue="severity", data=df, marker="o")
    plt.title("Logs Severity Over Time")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ := "_main_":
    log_file = r"C:\Users\yasmin\OneDrive\Bureau\Cours INF1007\pr02-Yamera\rapport_journalisation_2024-04-15_21-00-07.log"
    timestamps, severities = extract_log_metric(log_file)
    plot_method(timestamps, severities)