import csv
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import os
import webbrowser


def load_job_data(filename):
    """Load job data from a CSV file."""
    job_data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                job_data.append(row)
    except FileNotFoundError:
        pass
    return job_data


def save_job(job_list):
    """Save job data to a CSV file."""
    with open("jobs.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Latitude", "Longitude"])
        writer.writerows(job_list)


def search_jobs(jobs, keyword):
    """Search for jobs by keyword in the title."""
    return [job for job in jobs if keyword.lower() in job[0].lower()]


def sort_jobs(jobs):
    """Sort jobs alphabetically by location."""
    return sorted(jobs, key=lambda x: x[2])


def generate_map(jobs):
    """Generate a map displaying all job locations."""
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


def display_jobs(jobs):
    """Clear and display jobs in the Treeview."""
    tree.delete(*tree.get_children())
    for row in jobs:
        tree.insert("", "end", values=row)


def search():
    """Search for jobs by title."""
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
    """Sort jobs alphabetically by location."""
    sorted_jobs = sort_jobs(job_data)
    display_jobs(sorted_jobs)


def add_job():
    """Add a new job to the list."""
    title = title_entry.get().strip()
    company = company_entry.get().strip()
    location = location_entry.get().strip()
    lat = latitude_entry.get().strip()
    lon = longitude_entry.get().strip()

    if not (title and company and location and lat and lon):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        messagebox.showerror("Error", "Latitude and Longitude must be numeric!")
        return

    job_data.append([title, company, location, lat, lon])
    save_job(job_data)
    display_jobs(job_data)
    title_entry.delete(0, tk.END)
    company_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    latitude_entry.delete(0, tk.END)
    longitude_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Job added successfully!")


# Load initial job data
job_data = load_job_data("jobs.csv")

# GUI Setup
root = tk.Tk()
root.title("Job Search Application")

# Top Frame (Search and Sort)
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

search_label = tk.Label(frame_top, text="Search by Job Title:")
search_label.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(frame_top)
search_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(frame_top, text="Search", command=search)
search_button.grid(row=0, column=2, padx=5)

sort_button = tk.Button(frame_top, text="Sort by Location", command=sort)
sort_button.grid(row=0, column=3, padx=5)

# Treeview for Job Display
columns = ("Job Title", "Company", "Location", "Latitude", "Longitude")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(pady=10)

# Bottom Frame (Add Job)
frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

labels = ["Job Title", "Company", "Location", "Latitude", "Longitude"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame_bottom, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(frame_bottom)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

title_entry, company_entry, location_entry, latitude_entry, longitude_entry = entries

add_button = tk.Button(frame_bottom, text="Add Job", command=add_job)
add_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

map_button = tk.Button(frame_bottom, text="Generate Map", command=lambda: generate_map(job_data))
map_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

# Display Initial Jobs
display_jobs(job_data)

root.mainloop()
