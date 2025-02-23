import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataProcessor:
    """
    A class to handle the merging and filtering of two CSV datasets based on lead information.

    Attributes:
        df1 (pd.DataFrame): DataFrame loaded from the first CSV file.
        df2 (pd.DataFrame): DataFrame loaded from the second CSV file.
    """

    def __init__(self, df1_path: str, df2_path: str):
        """
        Initializes the DataProcessor by loading two CSV files into DataFrames.

        Args:
            df1_path (str): Path to the first CSV file.
            df2_path (str): Path to the second CSV file.
        """
        try:
            self.df1 = pd.read_csv(df1_path)
            logging.info(f"Successfully loaded first CSV from {df1_path}")
            self.df2 = pd.read_csv(df2_path, encoding="ISO-8859-1")
            logging.info(f"Successfully loaded second CSV from {df2_path}")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except pd.errors.ParserError as e:
            logging.error(f"Error parsing CSV: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during initialization: {e}")
            raise

    def _merge_dataframes(self, merge_on_column: str) -> pd.DataFrame:
        """
        Merges two DataFrames on a specified column, avoiding duplication on common columns.

        Args:
            merge_on_column (str): The column name on which to merge the DataFrames.

        Returns:
            pd.DataFrame: A merged DataFrame.
        """
        try:
            common_columns = set(self.df1.columns).intersection(
                set(self.df2.columns))
            common_columns.remove(merge_on_column)
            merged_df = pd.merge(
                self.df1,
                self.df2.drop(columns=list(common_columns)),
                on=merge_on_column,
                how='outer'
            )
            logging.info(
                f"DataFrames merged successfully on '{merge_on_column}' column.")
            return merged_df
        except KeyError as e:
            logging.error(f"Column not found for merging: {e}")
            raise
        except Exception as e:
            logging.error(f"Error while merging DataFrames: {e}")
            raise

    def get_filter_data(self) -> pd.DataFrame:
        """
        Filters the merged DataFrame to include only leads from 'Landing Page Submission' 
        with a non-empty 'Company' field.

        Returns:
            pd.DataFrame: A filtered DataFrame with relevant leads.
        """
        try:
            merged_df = self._merge_dataframes(merge_on_column="Lead Number")
            filtered_df = merged_df[
                (merged_df['Lead Origin'] == 'Landing Page Submission') &
                (merged_df['Company'].notna())
            ]
            logging.info(f"Filtered data contains {len(filtered_df)} leads.")
            return filtered_df
        except KeyError as e:
            logging.error(f"Required column missing during filtering: {e}")
            raise
        except Exception as e:
            logging.error(f"Error during data filtering: {e}")
            raise

    def save_filtered_dataframe(self, filtered_dataframe: pd.DataFrame, path: str, index: bool = False) -> str:
        """
        Saves a DataFrame to a CSV file.

        Args:
            filtered_dataframe (pd.DataFrame): The DataFrame to save.
            path (str): The file path where the CSV will be saved.
            index (bool): Whether to write row names (index). Default is False.

        Returns:
            None
        """
        try:
            filtered_dataframe.to_csv(path, index=index)
            print(f"DataFrame successfully saved to {path}")
        except Exception as e:
            print(f"Failed to save DataFrame: {e}")
