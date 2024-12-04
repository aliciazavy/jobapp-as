import csv
import for tkinter as tk
from tkinter import ttk, messagebox
import folium
import csv
import webbrowser
import os

def load_job_data(filename):
    job_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            job_data.append(row)
    return job_data

