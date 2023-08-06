#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:35:38 2021

@author: ross
"""
import json
#import ocrp
from ocrp.aws import trp
from ocrp.aws import paragraph_detector


filen = '.json'

with open(filen,'rt') as handle:
    doc =  json.load(handle)
    if 'ExtractedText' in doc.keys():
        document = trp.Document(doc['ExtractedText'])
    else:
        document = trp.Document(doc)
        

page = document.pages[1]
all_paragraphs = paragraph_detector.extract_paragraphs(page, dist_x=0, dist_y = 0.007, display=True)