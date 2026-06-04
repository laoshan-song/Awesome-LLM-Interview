from __future__ import annotations

import argparse
from inspect import signature


def main() -> None:
    parser = argparse.ArgumentParser(description="QLoRA SFT template for interview diagnosis data.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--data", default="data/sft_interview_diagnosis.jsonl")
    parser.add_argument("--output", default="outputs/interview-diagnosis-lora")
    parser.add_argument("--max-steps", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--max-seq-length", type=int, default=1024)
    parser.add_argument("--load-in-4bit", action="store_true", help="Enable bitsandbytes 4-bit QLoRA loading.")
    parser.add_argument("--fp16", action="store_true", help="Use fp16 training.")
    parser.add_argument("--bf16", action="store_true", help="Use bf16 training. Requires supported GPU.")
    args = parser.parse_args()

    try:
        from datasets import load_dataset
        from peft import prepare_model_for_kbit_training
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from trl import SFTTrainer
    except ImportError as exc:
        raise SystemExit(
            "Missing training dependencies. Install transformers, datasets, peft, trl, accelerate "
            "and bitsandbytes if you want 4-bit QLoRA."
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs = {"device_map": "auto", "trust_remote_code": True}
    if args.load_in_4bit:
        try:
            import torch
            from transformers import BitsAndBytesConfig
        except ImportError as exc:
            raise SystemExit(
                "4-bit training requires torch, bitsandbytes, and a transformers build with BitsAndBytesConfig."
            ) from exc
        model_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    model = AutoModelForCausalLM.from_pretrained(args.model, **model_kwargs)
    if args.load_in_4bit:
        model = prepare_model_for_kbit_training(model)
    dataset = load_dataset("json", data_files=args.data, split="train")

    def formatting_func(example: dict) -> str:
        messages = example["messages"]
        if hasattr(tokenizer, "apply_chat_template"):
            return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        return "\n".join(f"{item['role']}: {item['content']}" for item in messages)

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
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.learning_rate,
        logging_steps=10,
        save_steps=50,
        fp16=args.fp16,
        bf16=args.bf16,
        report_to=[],
    )
    trainer_kwargs = {
        "model": model,
        "train_dataset": dataset,
        "peft_config": peft_config,
        "args": training_args,
        "formatting_func": formatting_func,
    }
    trainer_params = signature(SFTTrainer.__init__).parameters
    if "tokenizer" in trainer_params:
        trainer_kwargs["tokenizer"] = tokenizer
    if "processing_class" in trainer_params:
        trainer_kwargs["processing_class"] = tokenizer
    if "max_seq_length" in trainer_params:
        trainer_kwargs["max_seq_length"] = args.max_seq_length
    trainer = SFTTrainer(**trainer_kwargs)
    trainer.train()
    trainer.save_model(args.output)


if __name__ == "__main__":
    main()
