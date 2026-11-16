import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# ====================================================================================


def normalize_visualizations(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> None:
    """"""

    try:
        nrows, ncols = 2, 2

        _, axes = plt.subplots(
            num="Normalization",
            nrows=nrows, ncols=ncols,
            figsize=(16, 14),
        )
        axes = np.atleast_1d(axes).flatten()

        # --------------------------------------------

        targets = {
            "Sith": 0,
            "Jedi": 1
        }

        features = {
            "Sensitivity": 0,
            "Push": 1
        }

        colors = ["red", "blue"]

        # --------------------------------------------

        for idx, ax in enumerate(axes):
            df = df1 if idx % 2 == 0 else df2

            if idx < 2:
                for target_label in targets:
                    target_id = targets[target_label]
                    target_color = colors[target_id]

                    mask = df.iloc[:, -1] == target_id
                    selected_df = df.loc[mask]

                    label_feature1, label_feature2 = features.keys()
                    id_feature1, id_feature2 = features.values()

                    ax.scatter(
                        selected_df.iloc[:, id_feature1],
                        selected_df.iloc[:, id_feature2],
                        c=target_color,
                        marker="o",
                        edgecolor="white",
                        linewidth=1,
                        zorder=1,
                        label=target_label,
                    )

                    ax.set_xlabel(label_feature1)
                    ax.set_ylabel(label_feature2)

            else:
                for feature_label in features:
                    feature_id = features[feature_label]
                    feature_color = colors[feature_id]

                    selected_df = df.iloc[:, feature_id]

                    ax.hist(
                        selected_df,
                        label=feature_label, color=feature_color,
                        bins=45, density=True, alpha=0.5
                    )

                ax.set_xlabel("Values")
                ax.set_ylabel("Frequency")

                if (idx == 3):
                    plt.axvline(x=0, color="y", linestyle="--", label="Min: 0")
                    plt.axvline(x=1, color="g", linestyle="--", label="Max: 1")

            ax.set_title(
                "Original Data" if idx % 2 == 0
                else "Normalized Data"
            )
            ax.legend()

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error [normalize_visualizations()]: {e}")


def data_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the numerical features
    of a DataFrame using min-max scaling."""

    try:
        scaled = df.copy()

        for column in scaled.columns:
            min_value = scaled[column].min()
            max_value = scaled[column].max()

            if max_value != min_value:
                scaled[column] = (
                    (scaled[column] - min_value) /
                    (max_value - min_value)
                )
            else:
                scaled[column] = 0.0

        print("\n=== Normalized Data ===")
        print(scaled.head())

        return scaled

    except Exception as e:
        print(f"Error [data_normalization()]: {e}")

    return pd.DataFrame()
