import csv
import tkinter as tk
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

# Generate a map with job locations
def generate_map(jobs):
    # Create a base map centered at an average location (London)
    job_map = folium.Map(location=[51.5074, -0.1278], zoom_start=2)

    # Loop through the jobs and add markers with job details
    for job in jobs:
        title, company, location, lat, lon = job
        # Add marker with popup showing job title and company
        folium.Marker(
            location=[float(lat), float(lon)],
            popup=f"{title} at {company} ({location})",
        ).add_to(job_map)

    # Save the map as an HTML file
    map_file = "job_map.html"
    job_map.save(map_file)

    # Get the absolute path of the map file
    map_path = os.path.abspath(map_file)
    print(f"Map saved to: {map_path}")

    # Open the map in the default web browser
    webbrowser.open(f"file://{map_path}")
    
    # Main function
if __name__ == "__main__":
    # Load job data from CSV file
    job_data = load_job_data("jobs.csv")

    # Generate and display the map
    generate_map(job_data)
    
# File handling
def save_job(job_list):
    """Save job data to a CSV file."""
    with open("jobs.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location"])
        writer.writerows(job_list)