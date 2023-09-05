#!/bin/bash

# Archivo de salida para el informe
OUTPUT_FILE="project_diagnosis.txt"

# Nombre del proyecto (puedes cambiar esto según tus necesidades)
PROJECT_NAME="my_project"

# Función para recopilar recursos
gather_resources() {
    NAMESPACE=$1
    echo "### Namespace: $NAMESPACE" >> $OUTPUT_FILE
    for RESOURCE in $(rancher kubectl api-resources --verbs=list -o name)
    do
        # Verificar si el recurso existe en el namespace
        if rancher kubectl get $RESOURCE -n $NAMESPACE &>/dev/null; then
            echo "Resource: $RESOURCE" >> $OUTPUT_FILE
            rancher kubectl get $RESOURCE -n $NAMESPACE -o wide >> $OUTPUT_FILE
            echo "---------------------------" >> $OUTPUT_FILE
        fi
    done
}

# Empezar con el informe
echo "Project Diagnosis Report - $(date)" > $OUTPUT_FILE
echo "===========================" >> $OUTPUT_FILE

# Obtener todos los namespaces asociados al proyecto
NAMESPACES=$(rancher namespaces ls --format '{{.Namespace.Name}}' --project $PROJECT_NAME)

# Iterar sobre los namespaces asociados al proyecto y recopilar recursos
for NAMESPACE in $NAMESPACES
do
    gather_resources $NAMESPACE
done

# Imprimir la ubicación del informe
echo "Report generated at $OUTPUT_FILE"