from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

extra_site = os.environ.get("EXTRA_SITE")
if extra_site and extra_site not in sys.path:
    sys.path.insert(0, extra_site)

import torch
from peft import LoraConfig, get_peft_model
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


class JsonlChatDataset(Dataset):
    def __init__(self, path: Path, tokenizer, max_length: int) -> None:
        self.examples = []
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                row = json.loads(line)
                messages = row["messages"]
                if hasattr(tokenizer, "apply_chat_template"):
                    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
                else:
                    text = "\n".join(f"{item['role']}: {item['content']}" for item in messages)
                encoded = tokenizer(text, truncation=True, max_length=max_length, add_special_tokens=False)
                if encoded["input_ids"]:
                    self.examples.append(encoded)

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict:
        return self.examples[index]


class CausalCollator:
    def __init__(self, tokenizer, pad_to_multiple_of: int = 8) -> None:
        self.tokenizer = tokenizer
        self.pad_to_multiple_of = pad_to_multiple_of

    def __call__(self, features: list[dict]) -> dict:
        batch = self.tokenizer.pad(
            features,
            padding=True,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )
        labels = batch["input_ids"].clone()
        labels[batch["attention_mask"] == 0] = -100
        batch["labels"] = labels
        return batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal LoRA SFT without datasets/trl dependency.")
    parser.add_argument("--model", default="/data1/ml-1-1/models/Qwen2.5-3B-Instruct")
    parser.add_argument("--data", default="data/sft_interview_diagnosis.remote.jsonl")
    parser.add_argument("--output", default="/data1/ml-1-1/outputs/interview-diagnosis-lora")
    parser.add_argument("--max-steps", type=int, default=100)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--gradient-checkpointing", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.float16 if args.fp16 else torch.bfloat16 if args.bf16 else None
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        trust_remote_code=True,
        local_files_only=True,
        torch_dtype=dtype,
    )
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    dataset = JsonlChatDataset(Path(args.data), tokenizer, args.max_length)
    if len(dataset) == 0:
        raise SystemExit(f"No training examples loaded from {args.data}")

    training_args = TrainingArguments(
        output_dir=args.output,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.learning_rate,
        logging_steps=5,
        save_steps=max(20, args.max_steps),
        save_total_limit=2,
        fp16=args.fp16,
        bf16=args.bf16,
        report_to=[],
        remove_unused_columns=False,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=CausalCollator(tokenizer),
    )
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)


if __name__ == "__main__":
    main()
