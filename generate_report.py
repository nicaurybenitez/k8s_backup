import os
from collections import defaultdict

def parse_cluster_file(file_path):
    # Data structure to store the parsed data
    cluster_data = defaultdict(list)

    # Helper variables
    current_resource = None
    columns = []

    # Read the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Parse the file
    for line in lines:
        line = line.strip()
        if line.startswith("Resource:"):
            current_resource = line.split(":")[1].strip()
        elif line.startswith("NAME") or current_resource is None:
            continue
        elif current_resource and not line:
            current_resource = None
        elif current_resource and "----" not in line:
            cluster_data[current_resource].append(line.split())

    return cluster_data

def generate_html(cluster_data, output_path="cluster_report.html"):
    html_content = """
    <html>
        <head>
            <title>Cluster Diagnosis Report</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Cluster Diagnosis Report</h1>
    """

    for resource, data in cluster_data.items():
        html_content += f"<h2>{resource}</h2>"
        html_content += "<table>"
        # Headers
        html_content += "<tr>"
        for header in data[0]:
            html_content += f"<th>{header}</th>"
        html_content += "</tr>"
        # Data
        for row in data[1:]:
            html_content += "<tr>"
            for item in row:
                html_content += f"<td>{item}</td>"
            html_content += "</tr>"
        html_content += "</table>"

    html_content += """
        </body>
    </html>
    """

    with open(output_path, "w") as html_file:
        html_file.write(html_content)

    print(f"HTML report generated at {output_path}")

if __name__ == "__main__":
    file_path = "cluster_diagnosis.txt"  # Path to your file
    cluster_data = parse_cluster_file(file_path)
    generate_html(cluster_data)
