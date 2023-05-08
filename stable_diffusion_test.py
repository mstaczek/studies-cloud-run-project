from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("./stable-diffusion-v1-5", low_cpu_mem_usage=True)
results = pipeline(['cloud'], num_inference_steps=2, height=64, width=64)
