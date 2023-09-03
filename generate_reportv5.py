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

import subprocess
import os

def create_readme(output_base_dir):
    readme_content = """# Kubernetes Resources Backup

Este directorio contiene copias de seguridad de los recursos de Kubernetes, organizados por namespace.

## Orden de Restauración

Cuando restaures los recursos desde estos archivos YAML, sigue el siguiente orden:

1. Persistent Volumes (PVs) - `pv.yaml`
2. Persistent Volume Claims (PVCs) - `pvc.yaml`
3. Secrets - `secrets.yaml`
4. ConfigMaps - `configmaps.yaml`
5. Deployments - `deployments.yaml`
6. StatefulSets - `statefulsets.yaml`
7. DaemonSets - `daemonsets.yaml`
8. ReplicaSets - `replicasets.yaml`
9. Pods - `pods.yaml`
10. Services - `services.yaml`
11. Ingresses - `ingress.yaml`

## Consideraciones Especiales

### Volúmenes Persistentes (PVs y PVCs)

Si estás utilizando almacenamiento estático, asegúrate de que los volúmenes físicos asociados con los PVs estén disponibles y contengan los datos esperados. Si estás utilizando almacenamiento dinámico, los volúmenes físicos se crean automáticamente cuando se crea el PVC, pero debes asegurarte de que el almacenamiento dinámico esté configurado y funcionando correctamente.

### Secretos

Los secretos se exportan en su forma codificada (base64). Si necesitas acceder al contenido real del secreto después de la restauración, tendrás que decodificarlo.

### Pruebas

Antes de realizar cualquier restauración en un entorno de producción, siempre es una buena práctica restaurar primero en un entorno de prueba o desarrollo para asegurarte de que todo funcione según lo esperado.
    """

    # Save the README content to each namespace directory
    namespaces = [dir for dir in os.listdir(output_base_dir) if os.path.isdir(os.path.join(output_base_dir, dir))]
    for ns in namespaces:
        with open(os.path.join(output_base_dir, ns, "README.md"), "w") as file:
            file.write(readme_content)

def export_k8s_resources_to_yaml(output_base_dir):
    os.makedirs(output_base_dir, exist_ok=True)
    namespaces = subprocess.getoutput("kubectl get namespaces -o custom-columns=NAME:.metadata.name --no-headers").split()
    resources = ["pods", "services", "deployments", "configmaps", "secrets", "pv", "pvc", "ingress", "daemonsets", "replicasets", "statefulsets"]

    for ns in namespaces:
        ns_dir = os.path.join(output_base_dir, ns)
        os.makedirs(ns_dir, exist_ok=True)

        for res in resources:
            output_path = os.path.join(ns_dir, f"{res}.yaml")
            subprocess.run(["kubectl", "get", res, "-n", ns, "-o", "yaml"], stdout=open(output_path, "w"))

    # Create the README
    create_readme(output_base_dir)

if __name__ == "__main__":
    file_path = "cluster_diagnosis.txt"
    current_date = datetime.now().strftime('%Y%m%d')
    report_folder = f"reports_" + current_date
    output_path = os.path.join(report_folder, "cluster_report.html")
    resource_statuses, resource_details = parse_cluster_file_v2(file_path)
    generate_html_v3(resource_statuses, resource_details, output_path)
    export_k8s_resources_to_yaml(os.path.join(report_folder, "k8s_resources"))

