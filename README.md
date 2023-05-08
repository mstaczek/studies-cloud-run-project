# Stable Diffusion API on Cloud Run

Source: [cloud-run-fastapi](https://github.com/alexsantos/cloud-run-fastapi)

Dockerfile installs py packages and copies the [Stable Diffusion 1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5) using [diffusers](https://github.com/huggingface/diffusers) library.

## app.py 

1. save `request` for debugging to `Cloud Storage`,
2. extract path and new task content from `request`,
3. check `Firebase Realtime Database` if the image for this task is already present or being generated,
4. if not, generate the image and save it to `Firebase Storage`,
5. update `Firebase Realtime Database` to mark that the image is ready.


