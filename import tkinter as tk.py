import csv
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import os


# Load job data from CSV
def load_jobs():
    """Load job data from a CSV file."""
    try:
        with open("jobs.csv", "r") as file:
            reader = csv.reader(file)
            return list(reader)[1:]  # Skip header row
    except FileNotFoundError:
        return []  # Return an empty list if file is not found


# Save job data to CSV
def save_job(job_list):
    """Save job data to a CSV file."""
    with open("jobs.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Latitude", "Longitude"])
        writer.writerows(job_list)


# Search function
def search_jobs(jobs, keyword):
    """Search for jobs by keyword in the title."""
    return [job for job in jobs if keyword.lower() in job[0].lower()]


# Sort jobs by location
def sort_jobs(jobs):
    """Sort jobs alphabetically by location."""
    return sorted(jobs, key=lambda x: x[2])


# Display jobs in the treeview
def display_jobs(jobs):
    """Clear and display jobs in the treeview."""
    tree.delete(*tree.get_children())
    for row in jobs:
        tree.insert("", "end", values=row)


# Generate a map with job locations
def generate_map(jobs):
    job_map = folium.Map(location=[51.5074, -0.1278], zoom_start=2)

    for job in jobs:
        title, company, location, lat, lon = job
        folium.Marker(
            location=[float(lat), float(lon)],
            popup=f"{title} at {company} ({location})",
        ).add_to(job_map)

    map_file = "job_map.html"
    job_map.save(map_file)
    webbrowser.open(f"file://{os.path.abspath(map_file)}")


# Search button functionality
def search():
    keyword = search_entry.get().strip()
    if not keyword:
        messagebox.showwarning("Warning", "Enter a search keyword!")
        return
    results = search_jobs(job_data, keyword)
    if results:
        display_jobs(results)
    else:
        messagebox.showinfo("No Results", "No jobs found for your search.")


# Sort button functionality
def sort():
    sorted_jobs = sort_jobs(job_data)
    display_jobs(sorted_jobs)


# Add new job functionality
def add_job():
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
search_label = tk.Label(frame_top, text="Search by Job Title:")
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

root.mainloop()

