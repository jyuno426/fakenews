# -*- coding:utf-8 -*-

import os
import csv

with open('summary.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')

    for detect in os.listdir("detects/"):
        with open("detects/" + detect, "r") as f:
            lines = f.readlines()
            title = lines[0].split("@@@@")[0]
            similarity, sentence = lines[1].split("@@@@")[:2]

            writer.writerow(
                [title.strip(),
                 sentence.strip(),
                 float(similarity.strip())])
