import datetime
import re 

import requests 
import csv

from nltk.corpus import stopwords
from textblob import TextBlob

# Cleans Text
def cleantext(paragraph):
    text = paragraph.lower()
    text = str(text).replace('\n\t', '')
    stop = stopwords.words('english')
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", text)
    text = ' '.join([word for word in text.split() if word not in (stop)])
    text = ''.join([word for word in text if not word.isdigit()])
    return TextBlob(text)

# Performs Analysis on text
def analysis(row): 
    # First subset is n row 
    # Second subset is [0]: outlet, [1]: heading, [2]: date, [3]: url, [4]: paragraph

    outlet         = row[0]
    month          = datetime.datetime.strptime(row[2].replace("Sept", "Sep"), "%d-%b-%y").month
    year           = datetime.datetime.strptime(row[2].replace("Sept", "Sep"), "%d-%b-%y").year
    text_polarity  = (cleantext(row[4]).sentiment)[0]
    text_bias      = (cleantext(row[4]).sentiment)[1]
    head_polarity  = (cleantext(row[1]).sentiment)[0]
    head_bias      = (cleantext(row[1]).sentiment)[1]
    return [outlet, 
            month, 
            year, 
            round(text_polarity, 4), 
            round(text_bias, 4),
            round(head_polarity, 4),
            round(head_bias, 4)
            ]

# Helper Functions above here
# ------------------------------------------------------------------------------------------------------------ #
# Main function here 

# Opens data and sends analysis into a csv file
# Takes in the file with data and empty csv file
def analysistocsv(input_file, output_file):
    with open(input_file, encoding = "ISO-8859-1" ) as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        rows = list(csv_reader)

        header = ["outlet", "month", "year", "text_polarity", "text_bias", "head_polarity", "head_bias"]
        
        with open(output_file, "a") as output_file: 
            writer = csv.writer(output_file)
            writer.writerow(header)
            for index, row in enumerate(rows):
                if index != 0:
                    writer.writerow(analysis(row))
                    

    return "Done!"








