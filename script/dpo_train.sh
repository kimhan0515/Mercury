#!/bin/bash

# deepseek-ai/deepseek-coder-1.3b-base
python ./src/dpo_train.py    \
    --model_name    deepseek-ai/deepseek-coder-1.3b-base   \
    --beta          0.1  \
    --learning_rate 2e-4    \
    --max_prompt_length 1024    \
    --max_length    2048    \
    --warmup_steps  100     \
    --max_steps     200     \
    --per_device_train_batch_size   1   \
    --gradient_accumulation_steps   4
