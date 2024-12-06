#!/bin/bash

# python src/evaluator.py \
#     --model_name_or_path deepseek-ai/deepseek-coder-1.3b-instruct \
#     --samples 1 \
#     --do_evaluate \
#     # --do_generate 

for i in {1..10}; 
do
    python src/evaluator.py \
        --model_name_or_path deepseek-ai/deepseek-coder-1.3b-instruct \
        --samples 1 \
        --do_evaluate \
        # --do_generate
done
