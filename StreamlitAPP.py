import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utlis import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
# from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
