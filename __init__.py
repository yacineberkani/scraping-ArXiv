import pandas as pd
import arxiv
import requests
import os
from langdetect import detect
from tqdm import tqdm
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
