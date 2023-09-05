#!/bin/bash

# Archivo de salida para el informe
OUTPUT_FILE="project_diagnosis.txt"

# Función para recopilar recursos
gather_resources() {
    NAMESPACE=$1
    echo "Procesando el namespace: $NAMESPACE..."
    # Verificar si hay recursos en general en el namespace
    if rancher kubectl get all -n $NAMESPACE &>/dev/null; then
        echo "### Namespace: $NAMESPACE" >> $OUTPUT_FILE
        for RESOURCE in $(rancher kubectl api-resources --verbs=list -o name)
        do
            # Si el recurso existe en el namespace, recopila información
            # La salida se redirige a un archivo temporal para evitar mensajes de error innecesarios
            OUTPUT=$(rancher kubectl get $RESOURCE -n $NAMESPACE -o wide 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "Recopilando información de $RESOURCE en $NAMESPACE"
                echo "Resource: $RESOURCE" >> $OUTPUT_FILE
                echo "$OUTPUT" >> $OUTPUT_FILE
                echo "---------------------------" >> $OUTPUT_FILE
            fi
        done
    else
        echo "El namespace $NAMESPACE no tiene recursos."
        echo "### Namespace: $NAMESPACE has no resources" >> $OUTPUT_FILE
    fi
}

# Empezar con el informe
echo "Project Diagnosis Report - $(date)" > $OUTPUT_FILE
echo "===========================" >> $OUTPUT_FILE

# Obtener todos los namespaces asociados al contexto actual
NAMESPACES=$(rancher namespaces ls --format '{{.Namespace.Name}}')

# Iterar sobre los namespaces asociados al proyecto y recopilar recursos
for NAMESPACE in $NAMESPACES
do
    gather_resources $NAMESPACE
done

# Imprimir la ubicación del informe
echo "Report generated at $OUTPUT_FILE"