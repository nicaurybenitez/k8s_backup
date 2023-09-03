import os
from collections import defaultdict, Counter
from datetime import datetime

def parse_cluster_file_v2(file_path):
        # Data structure to store the parsed data
        resource_statuses = defaultdict(Counter)
        resource_details = defaultdict(list)

        # Helper variables
        current_resource = None
        headers = None

        # Read the file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Parse the file
        for line in lines:
            line = line.strip()
            if line.startswith("Resource:"):
                current_resource = line.split(":")[1].strip()
            elif line.startswith("NAME") or current_resource is None:
                headers = line.split()
            elif current_resource and not line:
                current_resource = None
                headers = None
            elif current_resource and "----" not in line:
                data = dict(zip(headers, line.split()))
                resource_details[current_resource].append(data)
                status = data.get("STATUS", None)
                if status:
                    resource_statuses[current_resource][status] += 1

        return resource_statuses, resource_details

def generate_html_v3(resource_statuses, resource_details, output_path="cluster_report.html"):
        # Base HTML content with added styles for table and chart
        html_content = """
        <html>
            <head>
                <title>Cluster Diagnosis Report</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 20px;
                    }
                    th, td {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    tr:hover {background-color: #f5f5f5;}
                </style>
            </head>
            <body>
                <h1>Cluster Diagnosis Report</h1>
        """

        # Generate content for each resource
        for resource, statuses in resource_statuses.items():
            html_content += f"<h2>{resource}</h2>"
            html_content += f"<canvas id='{resource}_chart'></canvas>"

            # Add enhanced chart with tooltips
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
                                    'rgba(75, 192, 192, 0.6)',
                                    'rgba(255, 99, 132, 0.6)'
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
                            },
                            tooltips: {
                                callbacks: {
                                    label: function(tooltipItem, data) {
                                        return data.labels[tooltipItem.index] + ': ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                    }
                                }
                            }
                        }
                    });
                </script>
            """ % (resource, list(statuses.keys()), list(statuses.values()))

            # Add details table with added styles
            if resource_details.get(resource):
                details = resource_details[resource]
                headers = details[0].keys()
                html_content += "<table><tr>"
                for header in headers:
                    html_content += f"<th>{header}</th>"
                html_content += "</tr>"
                for detail in details:
                    html_content += "<tr>"
                    for header in headers:
                        html_content += f"<td>{detail[header]}</td>"
                    html_content += "</tr>"
                html_content += "</table>"

        # Closing tags
        html_content += """
            </body>
        </html>
        """

        # Save the HTML content to the specified output path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as html_file:
            html_file.write(html_content)

        print(f"HTML report generated at {output_path}")


if __name__ == "__main__":
        file_path = "cluster_diagnosis.txt"  # Path to your file
        current_date = datetime.now().strftime('%Y%m%d')
        output_folder = f"reports_" + current_date
        output_path = os.path.join(output_folder, "cluster_report.html")
        resource_statuses, resource_details = parse_cluster_file_v2(file_path)
        generate_html_v3(resource_statuses, resource_details, output_path)
import subprocess

def create_readme(output_base_dir):
 def export_k8s_resources_to_yaml(output_base_dir):


    if __name__ == "__main__":
        file_path = "cluster_diagnosis.txt"
        current_date = datetime.now().strftime('%Y%m%d')
        report_folder = f"reports_" + current_date
        output_path = os.path.join(report_folder, "cluster_report.html")
        resource_statuses, resource_details = parse_cluster_file_v2(file_path)
        generate_html_v3(resource_statuses, resource_details, output_path)
        export_k8s_resources_to_yaml(os.path.join(report_folder, "k8s_resources"))
