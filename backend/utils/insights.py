import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for PNG generation
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_charts(df, output_dir="static"):
    """
    Generate charts for visualizing transaction data (Bar and Line Charts Only).
    """
    try:
        # Ensure output directory exists
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Bar Chart: Total Spending per Category
        category_totals = df.groupby("Category")["Amount"].sum()
        plt.figure(figsize=(10, 6))  # Improved figure size
        category_totals.plot(kind="bar", color="skyblue")
        plt.title("Total Spending by Category", fontsize=14)
        plt.xlabel("Category", fontsize=12)
        plt.ylabel("Amount", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()  # Prevent layout overlaps
        plt.savefig(f"{output_dir}/bar_chart.png", dpi=300)  # High-resolution
        plt.close()

        # Line Chart: Spending Over Time
        df.sort_values("Date", inplace=True)
        plt.figure(figsize=(12, 6))  # Larger figure size for clarity
        df.groupby("Date")["Amount"].sum().plot(kind="line", marker="o", color="green")
        plt.title("Spending Over Time", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Total Amount", fontsize=12)
        plt.grid(alpha=0.5)  # Add grid for better readability
        plt.tight_layout()
        plt.savefig(f"{output_dir}/line_chart.png", dpi=300)  # High-resolution
        plt.close()

        logging.info("Charts generated successfully and saved in the static directory.")
    except Exception as e:
        logging.error(f"Error generating charts: {e}")


def spending_analysis(df):
    """
    Generate insights on spending data.
    """
    try:
        insights = {
            "total_spending": round(df["Amount"].sum(), 2),
            "average_spending": round(df["Amount"].mean(), 2) if not df.empty else 0,
            "highest_category": df.groupby("Category")["Amount"].sum().idxmax() if not df.empty else None,
            "highest_transaction": df.loc[df["Amount"].idxmax()].to_dict() if not df.empty else None,
            "category_totals": {
                k: round(v, 2) for k, v in df.groupby("Category")["Amount"].sum().to_dict().items()
            } if not df.empty else {},
            "monthly_breakdown": {
                str(period): round(total, 2) for period, total in df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().items()
            } if not df.empty else {}
        }
        return insights
    except Exception as e:
        logging.error(f"Error generating spending insights: {e}")
        return {}


def optimal_clusters(df):
    """
    Determine the optimal number of clusters using Silhouette Score.
    """
    try:
        scores = {}
        for k in range(2, min(len(df), 10)):  # Prevent issues with small data
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(df[["Amount"]])
            scores[k] = silhouette_score(df[["Amount"]], labels)
        optimal_k = max(scores, key=scores.get)
        logging.info(f"Optimal number of clusters determined: {optimal_k}")
        return optimal_k
    except ValueError as e:
        logging.warning("Insufficient data for clustering.")
        return 2  # Default to 2 clusters
    except Exception as e:
        logging.error(f"Error determining optimal clusters: {e}")
        return 2  # Default to 2 clusters


def spending_clusters(df):
    """
    Perform clustering on spending data.
    """
    try:
        optimal_k = optimal_clusters(df)
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(df[["Amount"]])
        return df["Cluster"].tolist()
    except Exception as e:
        logging.error(f"Error performing clustering: {e}")
        return []