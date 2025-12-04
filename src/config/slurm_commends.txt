### Interactive Jupyter Notebook ###
conda activate backbone_env
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###
cd /home/amitner/Backbone-Graph
sbatch "/home/amitner/Backbone-Graph/src/config/run_notebook.sbatch" Ecuador_part_3.gzip.parquet