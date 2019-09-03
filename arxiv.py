# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:58:01 2019

@author: Ken
"""

import arxiv
import pandas as pd
import requests

result = arxiv.query(query="all:deep learning")
data = pd.DataFrame(columns = ["title","id",'arxiv_url','published'])

for i in range(len(result)):
  id = result[i]['id'].split("/")[-1].split("v")[0]
  title = result[i]['title']
  arxiv_url = result[i]['arxiv_url']
  published = result[i]['published']
  data_tmp = pd.DataFrame({"title":title,"id":id, "arxiv_url":arxiv_url, "published":published},index=[0])
  data = pd.concat([data,data_tmp]).reset_index(drop=True)

citation_num_list = []
for i in data["id"]:
  try:
    sem = requests.get("https://api.semanticscholar.org/v1/paper/arXiv:"+i).json()
    citation_num = len(sem["citations"])
  except:
    citation_num = 0
  citation_num_list.append(citation_num)

data["citation"] = citation_num_list

data = data.sort_values(by='citation', ascending=False)

data.to_csv("data.csv",index=False)