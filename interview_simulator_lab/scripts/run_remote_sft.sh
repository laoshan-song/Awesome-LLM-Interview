#!/usr/bin/env bash
set -euo pipefail

GPU_ID="${GPU_ID:-0}"
PYTHON_BIN="${PYTHON_BIN:-/data1/ml-1-1/venv/bin/python}"
EXTRA_SITE="${EXTRA_SITE:-/data1/ml-1-1/envs/interview-prefix/local/lib/python3.10/dist-packages}"
MODEL_PATH="${MODEL_PATH:-/data1/ml-1-1/models/Qwen2.5-3B-Instruct}"
DATA_PATH="${DATA_PATH:-data/sft_interview_diagnosis.remote.jsonl}"
OUTPUT_DIR="${OUTPUT_DIR:-/data1/ml-1-1/outputs/interview-diagnosis-lora}"
MAX_STEPS="${MAX_STEPS:-100}"

export CUDA_VISIBLE_DEVICES="${GPU_ID}"
export PYTHONNOUSERSITE=1
export EXTRA_SITE="${EXTRA_SITE}"
export PYTHONPATH="${EXTRA_SITE}${PYTHONPATH:+:${PYTHONPATH}}"
export HF_HOME="${HF_HOME:-/data1/ml-1-1/hf_cache}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-/data1/ml-1-1/hf_cache}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/data1/ml-1-1/cache}"

"${PYTHON_BIN}" scripts/simple_lora_sft.py \
  --model "${MODEL_PATH}" \
  --data "${DATA_PATH}" \
  --output "${OUTPUT_DIR}" \
  --max-steps "${MAX_STEPS}" \
  --fp16 \
  --gradient-checkpointing
