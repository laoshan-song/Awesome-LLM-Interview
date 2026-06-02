from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="QLoRA SFT template for interview diagnosis data.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--data", default="data/sft_interview_diagnosis.jsonl")
    parser.add_argument("--output", default="outputs/interview-diagnosis-lora")
    parser.add_argument("--max-steps", type=int, default=100)
    args = parser.parse_args()

    try:
        from datasets import load_dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from trl import SFTTrainer
    except ImportError as exc:
        raise SystemExit(
            "Missing training dependencies. Install transformers, datasets, peft, trl, accelerate "
            "and bitsandbytes if you want 4-bit QLoRA."
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, device_map="auto", trust_remote_code=True)
    dataset = load_dataset("json", data_files=args.data, split="train")

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    training_args = TrainingArguments(
        output_dir=args.output,
        max_steps=args.max_steps,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        logging_steps=10,
        save_steps=50,
        fp16=True,
    )
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        peft_config=peft_config,
        args=training_args,
    )
    trainer.train()
    trainer.save_model(args.output)


if __name__ == "__main__":
    main()

