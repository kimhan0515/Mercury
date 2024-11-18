#!/bin/bash

mode=$1

if [ "$mode" == "eval" ]; then
    mode="--do_evaluate"
else
    mode="--do_generate"
fi

python3.11 src/evaluator.py \
    --model_name_or_path kimhan0515/deepseek-coder-1.3b-dpo-original \
    --samples 1 \
    $mode \
    --batch_size 16
