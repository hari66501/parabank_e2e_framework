import csv

# CSV file path
csv_file = "config/test_data.csv"

# Data to write
data = [
    {"username": "hari", "password": "demo"},
]

# Write CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "password"])
    writer.writeheader()      # write header
    writer.writerows(data)    # write data rows

print(f"CSV created at {csv_file}")
