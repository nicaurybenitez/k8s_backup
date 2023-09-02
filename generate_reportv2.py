import os
from collections import defaultdict, Counter

def parse_cluster_file(file_path):
    # Data structure to store the parsed data
    resource_statuses = defaultdict(Counter)

    # Helper variables
    current_resource = None

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
            data = line.split()
            status = data[1]  # Assuming the status is always the second column
            resource_statuses[current_resource][status] += 1

    return resource_statuses

def generate_html(resource_statuses, output_path="cluster_report.html"):
    html_content = """
    <html>
        <head>
            <title>Cluster Diagnosis Report</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Cluster Diagnosis Report</h1>
    """

    for resource, statuses in resource_statuses.items():
        html_content += f"<h2>{resource}</h2>"
        html_content += f"<canvas id='{resource}_chart'></canvas>"
        html_content += """
            <script>
                var ctx = document.getElementById('%s_chart').getContext('2d');
                var chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: %s,
                        datasets: [{
                            label: 'Status Count',
                            data: %s,
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.2)',  // You can add more colors here
                                'rgba(255, 99, 132, 0.2)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 99, 132, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            </script>
        """ % (resource, list(statuses.keys()), list(statuses.values()))

    html_content += """
        </body>
    </html>
    """

    with open(output_path, "w") as html_file:
        html_file.write(html_content)

    print(f"HTML report generated at {output_path}")

if __name__ == "__main__":
    file_path = "cluster_diagnosis.txt"  # Path to your file
    resource_statuses = parse_cluster_file(file_path)
    generate_html(resource_statuses)

