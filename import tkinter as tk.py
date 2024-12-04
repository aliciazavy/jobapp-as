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

def load_jobs():
    """Load job data from a CSV file."""
    try:
        with open("jobs.csv", "r") as file:
            reader = csv.reader(file)
            return list(reader)[1:]  # Skip header
    except FileNotFoundError:
        return []

# Search and sort functions
def search_jobs(jobs, keyword):
    """Search for jobs by keyword in the title."""
    return [job for job in jobs if keyword.lower() in job[0].lower()]

def sort_jobs(jobs):
    """Sort jobs alphabetically by location."""
    return sorted(jobs, key=lambda x: x[2])

# GUI functionality
def display_jobs(jobs):
    """Clear and display jobs in the treeview."""
    tree.delete(*tree.get_children())
    for row in jobs:
        tree.insert("", "end", values=row)

def search():
    """Search for jobs by the given keyword."""
    keyword = search_entry.get().strip()
    if not keyword:
        messagebox.showwarning("Warning", "Enter a search keyword!")
        return
    results = search_jobs(job_data, keyword)
    if results:
        display_jobs(results)
    else:
        messagebox.showinfo("No Results", "No jobs found for your search.")

def sort():
    """Sort jobs by location and display them."""
    sorted_jobs = sort_jobs(job_data)
    display_jobs(sorted_jobs)

def add_job():
    """Add a new job to the list."""
    title = title_entry.get().strip()
    company = company_entry.get().strip()
    location = location_entry.get().strip()

    if not (title and company and location):
        messagebox.showerror("Error", "All fields are required!")
        return
