import csv
import tkinter as tk
from tkinter import ttk, messagebox
import folium
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

# File handling
def save_job(job_list):
    """Save job data to a CSV file."""
    with open("jobslist.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Latitude", "Longitude"])
        writer.writerows(job_list)

def load_jobs():
    """Load job data from a CSV file."""
    try:
        with open("jobslist.csv", "r") as file:
            reader = csv.reader(file)
            return list(reader)[1:]  # Skip header
    except FileNotFoundError:
        return []

# Search and sort functions
def search_jobs(jobs, keyword):
    """Search for jobs by keyword in the title or location."""
    return [job for job in jobs if keyword.lower() in job[0].lower() or keyword.lower() in job[2].lower()]

def sort_jobs(jobs):
    """Sort jobs alphabetically by location."""
    return sorted(jobs, key=lambda x: x[2].strip().lower())  # Location is in the 3rd column (index 2)

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
    latitude = lat_entry.get().strip()
    longitude = lon_entry.get().strip()

    if not (title and company and location and latitude and longitude):
        messagebox.showerror("Error", "All fields are required!")
        return

    job_data.append([title, company, location, latitude, longitude])
    save_job(job_data)
    display_jobs(job_data)
    title_entry.delete(0, tk.END)
    company_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    lat_entry.delete(0, tk.END)
    lon_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Job added successfully!")

# Load job data
job_data = load_jobs()

# GUI setup
root = tk.Tk()
root.title("Job Search Application")

# Frames
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

# Search bar
search_label = tk.Label(frame_top, text="Search by Job Title or Location:")
search_label.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(frame_top)
search_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(frame_top, text="Search", command=search)
search_button.grid(row=0, column=2, padx=5)

sort_button = tk.Button(frame_top, text="Sort by Location", command=sort)
sort_button.grid(row=0, column=3, padx=5)

# Job list display
columns = ("Job Title", "Company", "Location", "Latitude", "Longitude")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(pady=10)

# Add job form
title_label = tk.Label(frame_bottom, text="Job Title:")
title_label.grid(row=0, column=0, padx=5, pady=5)

title_entry = tk.Entry(frame_bottom)
title_entry.grid(row=0, column=1, padx=5, pady=5)

company_label = tk.Label(frame_bottom, text="Company:")
company_label.grid(row=1, column=0, padx=5, pady=5)

company_entry = tk.Entry(frame_bottom)
company_entry.grid(row=1, column=1, padx=5, pady=5)

location_label = tk.Label(frame_bottom, text="Location:")
location_label.grid(row=2, column=0, padx=5, pady=5)

location_entry = tk.Entry(frame_bottom)
location_entry.grid(row=2, column=1, padx=5, pady=5)

lat_label = tk.Label(frame_bottom, text="Latitude:")
lat_label.grid(row=3, column=0, padx=5, pady=5)

lat_entry = tk.Entry(frame_bottom)
lat_entry.grid(row=3, column=1, padx=5, pady=5)

lon_label = tk.Label(frame_bottom, text="Longitude:")
lon_label.grid(row=4, column=0, padx=5, pady=5)

lon_entry = tk.Entry(frame_bottom)
lon_entry.grid(row=4, column=1, padx=5, pady=5)

add_button = tk.Button(frame_bottom, text="Add Job", command=add_job)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

# Display initial jobs
display_jobs(job_data)

# Run the map generation
generate_map(job_data)

root.mainloop()