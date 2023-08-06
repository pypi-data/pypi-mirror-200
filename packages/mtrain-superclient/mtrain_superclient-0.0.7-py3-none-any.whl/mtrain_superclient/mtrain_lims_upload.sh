#!/bin/bash

conda init bash && source ~/.bashrc
conda activate /pkg/mtrain_lims

conda deactivate
conda activate /pkg/mtrain_lims

export PATH=/opt/conda/envs/py37/bin:$PATH
# python3 -m mtrain_lims
mtrain_lims --input_json=$UPLOAD_INPUT_JSON --output_json=$UPLOAD_OUTPUT_JSON
ERRORCODE=$?

conda deactivate

exit $ERRORCODE