from diffusers import DiffusionPipeline

def initialize_model():
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", force_download=True, low_cpu_mem_usage=True)
    DiffusionPipeline.save_pretrained(self=pipeline, save_directory="./stable-diffusion-v1-5")

if __name__ == '__main__':
    initialize_model()