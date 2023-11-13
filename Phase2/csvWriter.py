
import csv




def csv_writer(soup,fileName,m):
    table = soup.find('table')

    if table:
        # Initialize lists to store the table data
        data = []
        for row in table.find_all('tr'):
            row_data = [cell.get_text() for cell in row.find_all(['th', 'td'])]
            data.append(row_data)

        # Define the CSV file name
        

        # Write the data to the CSV file
        with open(fileName, m, newline='') as file:
            writer = csv.writer(file)
            for row_data in data:
                writer.writerow(row_data)

        print(f"Table data has been saved to {fileName}")
    else:
        print("Desired table not found.")