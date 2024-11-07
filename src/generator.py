# coding: utf-8

# Strik on the assigned GPU.
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0,1,2,3'
os.environ["TOKENIZERS_PARALLELISM"] = 'true'
os.environ['HF_HOME'] = '/home/s4/hanbyeol/.cache/huggingface/hub'

