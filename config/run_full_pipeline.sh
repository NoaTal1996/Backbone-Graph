#!/bin/bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <country>"
    echo "Example: $0 Ecuador_Test"
    exit 1
fi

user="$USER"
country="$1"
project_root="/home/${user}/Backbone-Graph"

min_cluster_sizes=(10 128 256 512)

cd "${project_root}/src" || exit 1

echo "Launch pipeline from working directory: $(pwd)"

step_1_input="../data/Labeled_Datasets/${country}/${country}_part_all.gzip.parquet"

step_1_output="../results/Labeled_Datasets/${country}/${country}_part_all/step_1_translate_topics_entities/${country}_part_all_step_1.gzip.parquet"

step_2_output="../results/Labeled_Datasets/${country}/${country}_part_all/step_2_BERTopic_clustering/${country}_part_all_step_2.gzip.parquet"

echo "========================================"
echo "Submitting pipeline for: ${country}"
echo "========================================"

if [[ ! -f "${step_1_input}" ]]; then
    echo "ERROR: Input file does not exist:"
    echo "${step_1_input}"
    exit 1
fi

# ------------------------------------------------------------
# Step 1
# ------------------------------------------------------------
step_1_job_id=$(
    sbatch --parsable \
        "../config/run_1_translate_topics_entities.sbatch" \
        "${step_1_input}"
)

step_1_job_id="${step_1_job_id%%;*}"

echo "Step 1 submitted:"
echo "  job_id=${step_1_job_id}"

# ------------------------------------------------------------
# Step 2
# Four BERTopic jobs run in parallel after Step 1 succeeds.
# ------------------------------------------------------------
step_2_job_ids=()

for min_cluster_size in "${min_cluster_sizes[@]}"; do
    step_2_job_id=$(
        sbatch --parsable \
            --dependency="afterok:${step_1_job_id}" \
            "../config/run_2_BERTopic_clustering.sbatch" \
            "${step_1_output}" \
            "${min_cluster_size}"
    )

    step_2_job_id="${step_2_job_id%%;*}"
    step_2_job_ids+=("${step_2_job_id}")

    echo "Step 2 submitted:"
    echo "  min_cluster_size=${min_cluster_size}"
    echo "  job_id=${step_2_job_id}"
done

step_2_dependencies=$(IFS=:; echo "${step_2_job_ids[*]}")

# ------------------------------------------------------------
# Step 3
# Starts only after all Step 2 jobs succeed.
# ------------------------------------------------------------
step_3_job_id=$(
    sbatch --parsable \
        --dependency="afterok:${step_2_dependencies}" \
        "../config/run_3_key_authors_graph.sbatch" \
        "${step_2_output}"
)

step_3_job_id="${step_3_job_id%%;*}"

echo
echo "Step 3 submitted:"
echo "  job_id=${step_3_job_id}"
echo "  waits_for=${step_2_dependencies}"

echo
echo "Pipeline submitted successfully."
echo
echo "Execution order:"
echo "  Step 1: ${step_1_job_id}"
echo "  Step 2: ${step_2_job_ids[*]}"
echo "  Step 3: ${step_3_job_id}"
echo
echo "Jobs status:"
squeue --me
