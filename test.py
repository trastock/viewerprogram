import csv
row = [';1000;Emil Alakulju;;;Herr;0;0;Nyköping;;1;1;18:30;0;1;0;0']
with open('test.csv', "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(row)