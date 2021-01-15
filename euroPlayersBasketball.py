from bs4 import BeautifulSoup
import csv
html = open("euroPlayersTable.html").read()
soup = BeautifulSoup(html, 'lxml')
table = soup.find("table")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)
    
with open('internationalBasketballTeams.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
print('Task complete')
