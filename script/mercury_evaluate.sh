#!/bin/bash

mode=$1

if [ "$mode" == "eval" ]; then
    mode="--do_evaluate"
else
    mode="--do_generate"
fi

#python3.11 src/evaluator.py \
#    --model_name_or_path kimhan0515/deepseek-coder-1.3b-orpo-original \
#    --samples 1 \
#    $mode \
#    --batch_size 16

python3.11 src/evaluator.py \
    --model_name_or_path kimhan0515/deepseek-coder-1.3b-dpo-200-original-shuffle \
    --samples 1 \
    $mode \
    --batch_size 16

#python3.11 src/evaluator.py \
#    --model_name_or_path kimhan0515/deepseek-coder-1.3b-cpo-500 \
#    --samples 1 \
#    $mode \
#    --batch_size 16

#python3.11 src/evaluator.py \
#    --model_name_or_path deepseek-ai/deepseek-coder-1.3b-base \
#    --samples 1 \
#    $mode \
#    --batch_size 16
