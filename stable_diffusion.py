from diffusers import DiffusionPipeline
import requests
from PIL import Image
import os

def get_image_from_text(prompts_list, inference_steps=25, image_size=320):
    ## Get images from text prompts
    ## In: list of prompts ['cloud in the sky','cat on a bike']
    ## Out: list of PIL images, one per prompt: [PIL.Image, PIL.Image]

    def replace_nsfw_images_with_rainbow(results, image_size):
        # download rainbow image, once
        rainbow_filename = "rainbow_replaces_nsfw_black_image.jpg"
        if not os.path.exists(rainbow_filename):
            url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.shopify.com%2Fs%2Ffiles%2F1%2F2804%2F8054%2Fproducts%2Fil_fullxfull.1042262096_cpey_1024x.jpg%3Fv%3D1571726677&f=1&nofb=1&ipt=f7ed85da3c76764eb6e810708013263c103acbdc8a9d3b7e85c47fff23541c47&ipo=images"
            img_data = requests.get(url).content
            with open(rainbow_filename, 'wb') as handler:
                handler.write(img_data)

        # replace nsfw images with rainbow. Loop through all generated images
        for i in range(len(results['nsfw_content_detected'])):
            if results['nsfw_content_detected'][i]:
                img = Image.open(rainbow_filename)
                img = img.resize((image_size, image_size))
                results['images'][i] = img
        return results

    try:
        pipeline = DiffusionPipeline.from_pretrained("./stable-diffusion-v1-5", low_cpu_mem_usage=True)
        results = pipeline(prompts_list, num_inference_steps=inference_steps, height=image_size, width=image_size)
    except:
        print('An error has been caught.')
        print('Replacing with NSFW image.')
        results = {'nsfw_content_detected': [True], 'images': ['NSFW content detected, please try again with a different prompt']}

    results = replace_nsfw_images_with_rainbow(results, image_size)
    return results['images'][0], results['nsfw_content_detected'][0]

# example
#images_list = get_image_from_text(["paint a picture of a cloud in the sky"])
#for i, image in enumerate(images_list):
#    image.save(f"test_{i}.jpg")

# for reference i5-10210u, sorted by time, for prompt "paint a picture of a cloud in the sky":
# size,   iter,   ram,    cpu,    time,   result
# 64,     50,     6gb,    50%,    84s,    nsfw
# 128,    50,     6gb,    50%,    104s,   poor
# 64,     100,    6gb,    50%,    130s,   poor
# 192,    50,     6gb,    50%,    153s,   nsfw
# 320,    25,     6gb,    50%,    173s,   good <- selected
# 128,    100,    6gb,    50%,    192s,   nsfw
# 256,    50,     6gb,    50%,    201s,   so-so
# 320,    50,     6gb,    50%,    327s,   good
