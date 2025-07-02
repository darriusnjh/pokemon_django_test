# pokemaker/services/diffusion_service.py
import torch
from diffusers import DiffusionPipeline
import os
 
class DiffusionService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize_pipeline()
        return cls._instance
    
    def initialize_pipeline(self):
        print("Initializing Stable Diffusion pipeline...")
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to("cuda")
        self.pipe.enable_model_cpu_offload()
        self.pipe.load_lora_weights("darriusnjh/pokemon_test3")
        print("Pipeline initialized successfully!")
    
    def generate_image(self, prompt, pokemon_name):
        image = self.pipe(
            prompt=prompt,
            num_inference_steps=80,
            height=512,
            width=512,
            guidance_scale=7.0,
        ).images[0]
        
        output_folder = os.path.join('media', 'generated_poke')
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f'{pokemon_name}.png')
        
        image.save(output_path)
        return output_path.replace('media/','')
