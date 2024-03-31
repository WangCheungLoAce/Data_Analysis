import pandas as pd

def convert_to_csv(data):
    df = pd.DataFrame(data)

    # Clean 'Number_of_Ratings' column
    df['Number_of_Ratings'] = df['Number_of_Ratings'].str.replace(', with\n\(', 'Total ').str.replace('\)', '')

    # Save DataFrame to CSV
    df.to_csv('data.csv', index=False)

    # Return the CSV data as a string
    return df.to_csv(index=False)
