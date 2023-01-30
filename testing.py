import json
import csv

google_results = open("C:/Users/clair/OneDrive/Documents/USC/CSCI 572 Search Engines/Google_Result4.json")
google_data = json.load(google_results)
google_results.close()

my_results = open("C:/Users/clair/OneDrive/Documents/USC/CSCI 572 Search Engines/hw1.json")
my_data = json.load(my_results)
my_results.close()

with open('hw1.csv', 'w', newline='') as csvfile:

    spearman_total = 0 
    overlap_total = 0

    key_list = sorted(google_data.keys())

    for i in range(len(google_data)):
        google_search = google_data[key_list[i]]
        my_search = my_data[key_list[i]]

        overlap = 0 
        di_2_sum = 0

        for j in range(len(my_search)):
            for k in range(len(google_search)):
                if my_search[j] == google_search[k]:
                    overlap = overlap + 1 
                    my_position = j
                    google_position = k
                    di = my_position - google_position
                    di_2_sum = di_2_sum + (di * di) 
        
        if overlap == 1:
            if my_position == google_position:
                spearman_coefficient = 1 
            else:
                spearman_coefficient = 0
        elif overlap == 0:
            spearman_coefficient = 0 
        else:
            numerator = 6 * di_2_sum
            denominator = overlap * ((overlap * overlap)-1)
            spearman_coefficient = 1 - numerator / denominator 
        
        spearman_total = spearman_total + spearman_coefficient
        overlap_total = overlap_total + overlap

        csvwriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Query ' + str(i)] + [str(overlap)] + [str(overlap/len(google_search)*100)] + [str(spearman_coefficient)])

    spearman_average = spearman_total / len(google_data)
    overlap_average = overlap_total / len(google_data)
    print(overlap_total)
    overlap_percentage_average = overlap_average * 100 

    csvwriter.writerow(['Averages'] + [str(overlap_average)] + [str(overlap_percentage_average)] + [str(spearman_average)])