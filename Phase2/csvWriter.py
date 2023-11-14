
import csv




def csv_writer(soup,fileName,m):
    tables = soup.find_all("table")

    if tables:
        for table in tables:
            # Initialize lists to store the table data
            data=[]
            headers = [header.text for header in table.find('tr').find_all('th')]
            data.append(headers)
            rows = table.find_all('tr')[1:] 
            for row in rows:
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