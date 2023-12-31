#!/bin/bash

# Archivo de salida para el informe
OUTPUT_FILE="cluster_diagnosis.txt"

# Función para recopilar recursos
gather_resources() {
    NAMESPACE=$1
    echo "### Namespace: $NAMESPACE" >> $OUTPUT_FILE
    for RESOURCE in $(kubectl api-resources --verbs=list -o name)
    do
        # Verificar si el recurso existe en el namespace
        if kubectl get $RESOURCE -n $NAMESPACE &>/dev/null; then
            echo "Resource: $RESOURCE" >> $OUTPUT_FILE
            kubectl get $RESOURCE -n $NAMESPACE -o wide >> $OUTPUT_FILE
            echo "---------------------------" >> $OUTPUT_FILE
        fi
    done
}

# Empezar con el informe
echo "Cluster Diagnosis Report - $(date)" > $OUTPUT_FILE
echo "===========================" >> $OUTPUT_FILE

# Iterar sobre todos los namespaces y recopilar recursos
for NAMESPACE in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}')
do
    gather_resources $NAMESPACE
done

# Imprimir la ubicación del informe
echo "Report generated at $OUTPUT_FILE"

