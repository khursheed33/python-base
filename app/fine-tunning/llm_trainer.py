import torch
import torch.cuda
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer
)
from peft import (
    LoraConfig,
    get_peft_model,
    PeftModel,
    PeftConfig,
    prepare_model_for_kbit_training
)
from datasets import load_dataset
import os
import logging
from torch.utils.data import Dataset
import gc
from tqdm.auto import tqdm
import wandb

@dataclass
class PeftModelConfig:
    lora_r: int = 64
    lora_alpha: int = 16
    lora_dropout: float = 0.1
    bias: str = "none"
    task_type: str = "CAUSAL_LM"
    target_modules: Optional[List[str]] = None
    modules_to_save: Optional[List[str]] = None

@dataclass
class ModelConfig:
    model_name: str
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_compute_dtype: str = "float16"  # Changed from torch.dtype to str
    use_nested_quant: bool = False

@dataclass
class TrainerConfig:
    output_dir: str
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 1
    optim: str = "paged_adamw_32bit"
    learning_rate: float = 2e-4
    max_grad_norm: float = 0.3
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100

@dataclass
class DeviceConfig:
    device: str = "auto"
    mixed_precision: Optional[str] = "fp16"
    gradient_checkpointing: bool = True
    enable_cuda_graph: bool = True
    torch_compile: bool = True

@dataclass
class HubConfig:
    hub_model_id: Optional[str] = None
    push_to_hub: bool = False
    token: Optional[str] = None
    private: bool = False

class LLMFinetuner:
    def __init__(
        self,
        model_config: ModelConfig,
        trainer_config: TrainerConfig,
        peft_config: Optional[PeftModelConfig] = None,
        device_config: Optional[DeviceConfig] = None,
        hub_config: Optional[HubConfig] = None
    ):
        self.model_config = model_config
        self.trainer_config = trainer_config
        self.peft_config = peft_config
        self.device_config = device_config or DeviceConfig()
        self.hub_config = hub_config or HubConfig()
        self.model = None
        self.tokenizer = None
        self.trainer = None
        self._setup_device()
        
    def _setup_device(self):
        """Configure device and memory settings for GTX 1050 Ti"""
        if torch.cuda.is_available():
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
            logging.info(f"GPU Memory Available: {gpu_mem:.2f} GB")
            
            if gpu_mem < 4:  # GTX 1050 Ti has 4GB VRAM
                logging.warning("Limited VRAM detected, enabling memory optimizations")
                torch.cuda.empty_cache()
                torch.backends.cudnn.benchmark = False
                self.device = torch.device("cuda")
            else:
                self.device = torch.device("cuda")
                torch.backends.cudnn.benchmark = True
        else:
            self.device = torch.device("cpu")
            logging.warning("CUDA not available. Using CPU.")

    def setup_model(self):
        """Initialize model with optimized settings for GTX 1050 Ti"""
        # Convert string dtype to torch.dtype
        dtype_map = {
            "float16": torch.float16,
            "float32": torch.float32,
            "bfloat16": torch.bfloat16
        }
        compute_dtype = dtype_map[self.model_config.bnb_4bit_compute_dtype]
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=self.model_config.load_in_4bit,
            bnb_4bit_quant_type=self.model_config.bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=self.model_config.use_nested_quant
        )
        
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_config.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=compute_dtype,
                max_memory={0: "3GB", "cpu": "8GB"}  # Optimize for GTX 1050 Ti
            )
            
            if self.device_config.gradient_checkpointing:
                self.model.gradient_checkpointing_enable()
            
            self.model = prepare_model_for_kbit_training(self.model)
            
            return self
            
        except Exception as e:
            logging.error(f"Model initialization failed: {str(e)}")
            raise

    def setup_peft(self):
        """Configure and apply LoRA adapters"""
        if not self.peft_config:
            return self
            
        peft_config = LoraConfig(
            r=self.peft_config.lora_r,
            lora_alpha=self.peft_config.lora_alpha,
            lora_dropout=self.peft_config.lora_dropout,
            bias=self.peft_config.bias,
            task_type=self.peft_config.task_type,
            target_modules=self.peft_config.target_modules,
            modules_to_save=self.peft_config.modules_to_save
        )
        
        self.model = get_peft_model(self.model, peft_config)
        self.model.print_trainable_parameters()
        return self

    def prepare_dataset(
        self,
        dataset_source: str,
        is_local: bool = False,
        format: str = "json",
        split: str = "train",
        **kwargs
    ) -> Dataset:
        """Load dataset from local file or HuggingFace Hub"""
        try:
            if is_local:
                if not os.path.exists(dataset_source):
                    raise FileNotFoundError(f"Local dataset not found: {dataset_source}")
                dataset = load_dataset(format, data_files=dataset_source, split=split, **kwargs)
            else:
                dataset = load_dataset(dataset_source, split=split, **kwargs)
            logging.info(f"Successfully loaded dataset from {'local file' if is_local else 'HuggingFace Hub'}")
            return dataset
        except Exception as e:
            logging.error(f"Failed to load dataset: {str(e)}")
            raise

    def tokenize_dataset(
        self,
        dataset: Dataset,
        prompt_template: str,
        max_length: int = 1024
    ) -> Dataset:
        """Tokenize the dataset with proper formatting"""
        def tokenize_function(examples):
            formatted_prompts = [
                prompt_template.format(**example) for example in examples
            ]
            return self.tokenizer(
                formatted_prompts,
                truncation=True,
                max_length=max_length,
                padding="max_length"
            )
            
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        return tokenized_dataset

    def train(self, dataset, eval_dataset=None, **additional_training_args):
        """Enhanced training with optimizations"""
        training_args = TrainingArguments(
            output_dir=self.trainer_config.output_dir,
            num_train_epochs=self.trainer_config.num_train_epochs,
            per_device_train_batch_size=self.trainer_config.per_device_train_batch_size,
            gradient_accumulation_steps=self.trainer_config.gradient_accumulation_steps,
            optim=self.trainer_config.optim,
            learning_rate=self.trainer_config.learning_rate,
            max_grad_norm=self.trainer_config.max_grad_norm,
            warmup_ratio=self.trainer_config.warmup_ratio,
            lr_scheduler_type=self.trainer_config.lr_scheduler_type,
            logging_steps=self.trainer_config.logging_steps,
            save_steps=self.trainer_config.save_steps,
            eval_steps=self.trainer_config.eval_steps,
            fp16=self.device_config.mixed_precision == "fp16",
            bf16=self.device_config.mixed_precision == "bf16",
            gradient_checkpointing=self.device_config.gradient_checkpointing,
            report_to="wandb" if wandb.run else "none",
            **additional_training_args
        )
        
        self.trainer = Trainer(
            model=self.model,
            train_dataset=dataset,
            eval_dataset=eval_dataset,
            args=training_args,
            data_collator=lambda data: {
                'input_ids': torch.stack([f['input_ids'] for f in data]).to(self.device),
                'attention_mask': torch.stack([f['attention_mask'] for f in data]).to(self.device)
            }
        )
        
        try:
            self.trainer.train()
        except Exception as e:
            logging.error(f"Training failed: {str(e)}")
            raise
        finally:
            # Cleanup
            torch.cuda.empty_cache()
            gc.collect()
        
        return self

    def load_peft_model(self, peft_model_path: str):
        """Load a pretrained PEFT model
        
        Args:
            peft_model_path (str): Path to the saved PEFT model
            
        Returns:
            self: The trainer instance
            
        Raises:
            ValueError: If model is not initialized or path doesn't exist
        """
        if not self.model:
            raise ValueError("Base model must be initialized first")
        
        if not os.path.exists(peft_model_path):
            raise ValueError(f"PEFT model path not found: {peft_model_path}")
            
        try:
            config = PeftConfig.from_pretrained(peft_model_path)
            logging.info(f"Loading PEFT model with config: {config}")
            
            self.model = PeftModel.from_pretrained(
                self.model,
                peft_model_path,
                config=config,
                device_map=self.device_config.device if hasattr(self, 'device_config') else "auto"
            )
            print(f"Model type: {type(self.model)}")
            return self
        except Exception as e:
            logging.error(f"Failed to load PEFT model: {str(e)}")
            raise

    def merge_and_save(self, output_path: str):
        """Merge LoRA weights and save the full model
        
        Args:
            output_path (str): Path to save the merged model
            
        Returns:
            self: The trainer instance
            
        Raises:
            ValueError: If model is not a PeftModel
        """
        if not isinstance(self.model, PeftModel):
            raise ValueError("Model must be a PeftModel to merge weights")
            
        try:
            # Clear CUDA cache before merging
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            logging.info("Merging LoRA weights with base model...")
            self.model = self.model.merge_and_unload()
            
            # Save the merged model
            self.save_model(output_path)
            
            # Cleanup
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            logging.info(f"Successfully saved merged model to: {output_path}")
            return self
        except Exception as e:
            logging.error(f"Failed to merge and save model: {str(e)}")
            raise

    def save_model(self, output_path: str):
        """Save the model and tokenizer"""
        os.makedirs(output_path, exist_ok=True)
        self.model.save_pretrained(output_path)
        self.tokenizer.save_pretrained(output_path)
        return self

    def load_model(self, model_path: str):
        """Load a saved model"""
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        return self

    def push_to_hub(self, new_model_name: str):
        """Push model to HuggingFace Hub
        
        Args:
            new_model_name: Format should be 'username/model_name'
        """
        if not self.hub_config.push_to_hub:
            logging.warning("Push to hub is disabled in config")
            return self

        if '/' not in new_model_name:
            raise ValueError("new_model_name should be in format 'username/model_name'")

        try:
            from huggingface_hub import HfApi
            api = HfApi()

            # Login if token provided
            if self.hub_config.token:
                api.set_access_token(self.hub_config.token)

            # Push model
            self.model.push_to_hub(
                new_model_name,
                private=self.hub_config.private,
                use_auth_token=self.hub_config.token
            )

            # Push tokenizer
            self.tokenizer.push_to_hub(
                new_model_name,
                private=self.hub_config.private,
                use_auth_token=self.hub_config.token
            )

            logging.info(f"Successfully pushed model to hub: {new_model_name}")
            return self

        except Exception as e:
            logging.error(f"Failed to push to hub: {str(e)}")
            raise

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('.env')
    token = os.getenv("HF_TOKEN")
    # Example usage
    model_config = ModelConfig(
        model_name="Qwen/Qwen2-0.5B-Instruct",
        bnb_4bit_compute_dtype="float16"  # Use string instead of torch.dtype
    )
    
    trainer_config = TrainerConfig(
        output_dir="./Qwen2-fine-tuned",
        per_device_train_batch_size=1  # Reduced for GTX 1050 Ti
    )
    
    peft_config = PeftModelConfig(
        target_modules=["q_proj", "v_proj"]
    )
    
    device_config = DeviceConfig(
        gradient_checkpointing=True,
        mixed_precision="fp16"
    )
    
    hub_config = HubConfig(
        push_to_hub=True,
        token=token,  # or use huggingface-cli login
        private=False
    )
    
    finetuner = LLMFinetuner(
        model_config=model_config,
        trainer_config=trainer_config,
        peft_config=peft_config,
        device_config=device_config,
        hub_config=hub_config
    )
    
    # Setup and training pipeline
    finetuner.setup_model()\
             .setup_peft()
    
    # Load dataset (local or hub)
    # From Hub
    dataset = finetuner.prepare_dataset("khursheed33/openwho")
    print("Dataset loaded", dataset)
    # Or from local
    # dataset = finetuner.prepare_dataset("path/to/local/data.csv", is_local=True, format="csv")
    
    # Define prompt template
    prompt_template = """### Input: {input}
    ### Output: {output}"""
    
    # Tokenize dataset
    tokenized_dataset = finetuner.tokenize_dataset(dataset, prompt_template)
    print("Tokenized dataset", tokenized_dataset)
    # Train
    # finetuner.train(tokenized_dataset)\
    #          .merge_and_save("./final_model")
    
    # Push to hub after training
    # finetuner.push_to_hub("khursheed33/Qwen2-0.5B-Finetuned")