from data_access import csv_to_db, query_execution

from standardization import data_standardization, standardize_visualizations
from normalization import data_normalization, normalize_visualizations

# ====================================================================================


def main() -> None:
    """Standardization / Normalization"""

    try:
        if not csv_to_db(
            csv_file="config/data.csv",
            table_name="data"
        ):
            raise TypeError("Failed to load data!")

        # --------------------------------------------

        sql_query = "SELECT * FROM data;"
        if (data := query_execution(sql_query)).empty:
            raise TypeError("Failed to execute SQL query!")

        # Convert target from text to numbers
        data["knight"] = data["knight"].map({
            "Jedi": 1,
            "Sith": 0
        })

        print("\n=== Original Data ===")
        print(data.iloc[:, :-1].head())

        # --------------------------------------------

        standardized_data = data_standardization(data.iloc[:, :-1])
        standardized_data["knight"] = data.iloc[:, -1]

        standardize_visualizations(data, standardized_data)

        # --------------------------------------------

        normalized_data = data_normalization(data.iloc[:, :-1])
        normalized_data["knight"] = data.iloc[:, -1]

        normalize_visualizations(data, normalized_data)

    except Exception as e:
        print(f"Error [main()]: {e}")


if __name__ == "__main__":
    main()
