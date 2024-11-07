#!/bin/bash

mode=$1

if [ "$mode" == "eval" ]; then
    mode="--do_evaluate"
else
    mode="--do_generate"
fi

python3.11 src/evaluator.py \
    --model_name_or_path deepseek-ai/deepseek-coder-1.3b-base \
    --samples 1 \
    $mode \
    --batch_size 32
