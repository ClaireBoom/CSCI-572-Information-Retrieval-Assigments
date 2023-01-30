from bs4 import BeautifulSoup
import time 
import requests
from random import randint
from html.parser import HTMLParser
import json
import re
import csv

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: # Prevents loading too many pages too soon
            delay = randint(2, 7)
            time.sleep(delay)
        temp_url = '+'.join(query.split()) #for adding + between words for the query
        url = 'https://www.duckduckgo.com/html/?q=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all('a', attrs = {'class' : 'result__a'})
        results = []
        #implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            link = result.get('href')
            url = re.compile(r'https?://(www\.)?')
            link = url.sub('', link).strip().strip('/')

            if link not in results and len(results) < 10:
                results.append(link)
        return results

with open("C:/Users/clair/OneDrive/Documents/USC/CSCI 572 Search Engines/100QueriesSet4.txt") as f:
    queries = f.readlines()

jsonFile = open("hw1.json", "w")
results_dictionary = {}

index = len(queries)
for query in queries:
    print('remaining queries: ', index)
    query_results = SearchEngine.search(query)
    query_pretty = query.strip(" \n")
    results_dictionary.update({query_pretty : query_results})
    index = index-1

formatted_results = json.dump(results_dictionary, jsonFile)

jsonFile.close()

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
    overlap_percentage_average = overlap_average * 100 

    csvwriter.writerow(['Averages'] + [str(overlap_average)] + [str(overlap_percentage_average)] + [str(spearman_average)])

    print('program complete.')