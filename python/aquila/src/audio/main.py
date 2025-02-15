import pandas as pd
def read_csv_analyse(file_name):
    df = pd.read_csv(file_name)

    # Get the column names (titles)
    titles = df.columns.tolist()

    # Get the count of all rows
    row_count = df.shape[0]

    # Print the titles and row count
    print(f"Titles: {titles}")
    print(f"Row count: {row_count}")
def main():
    file_name = 'data/Data.csv'

if __name__ == "__main__":
    main()
