from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json

from stable_diffusion import get_image_from_text
from upload_blob import upload_blob
import random
import os

import firebase_admin
from firebase_admin import db
from time import sleep


INFERENCE_STEPS = 25
IMAGE_SIZE = 64


app = FastAPI()

@app.get('/hello')
def hello_world():
    print(os.listdir())
    return JSONResponse(content={'message': "Hello world!"})

@app.post('/predict')
async def predict(request: Request):
    
    # save request.__dict__ to storage bucket testing
    random_number = random.randint(0, 100000)
    print('Saving request to storage bucket')
    path_to_request = f'request_{random_number}.txt'
    with open(path_to_request, 'w') as f:
        f.write(str(request.__dict__))
    bucket_id = 'saving-to-storage-bucket-test'
    upload_blob(bucket_id, path_to_request, path_to_request)
    
    # get value for key 'ce-ref' in request headers: tasks/somerandomuuid/sometimestamp/task
    source_path = request.headers.get('ce-ref')
    print(f'Found source path in headers "ce-ref": {source_path}')
    if len(source_path.split("/")) == 4:
        output_path = f'images/tasks/{source_path.split("/")[1]}/{source_path.split("/")[2]}.jpg'
    else:
        output_path = f'images/{source_path}.jpg'
    print(f'Found output path: {output_path}')

    # get value for key 'delta' in request body: "find a pigeon"
    task_text = await request.body()
    task_text = json.loads(task_text)['delta']
    print(f'Found task text in request body: {task_text}')

    # check if image is already generated
    ref = db.reference(f'/{"/".join(source_path.split("/")[:-1])}', url='https://ai-todo-list.firebaseio.com/')
    
    if ref.get() is not None and 'hasImage' in ref.get() and ref.get()['hasImage'].startswith('processing'):
        print('Image is already processing. Waiting 10minutes.')
        for _ in range(10):
            sleep(60)
            if ref.get()['hasImage'] == 'true':
                return JSONResponse(content={'message': "New image generated successfully."})
        return JSONResponse(content={'message': "Image has not been generated in the last 10 minutes by other process. Proceeding..."})
    
    if ref.get() is None or not 'hasImage' in ref.get() or ref.get()['hasImage'] == 'false':
        ref = db.reference(f'/{"/".join(source_path.split("/")[:-1])}', url='https://ai-todo-list.firebaseio.com/')
        ref.update({
            'hasImage' : f'processing'
        })

    if ref.get() is not None and 'hasImage' in ref.get() and ref.get()['hasImage'] == 'true':
        print('Image already generated. Skipping.')
        return JSONResponse(content={'message': "Image already generated. Skipping."})

    # generating image from text
    print(f'Prompt: {task_text}')
    image = get_image_from_text([task_text], inference_steps=INFERENCE_STEPS, image_size=IMAGE_SIZE)
    print('Image generated. Saiving to storage bucket.')

    # saveing image to storage bucket
    random_number = random.randint(0, 100000)
    image=image[0]
    tmp_image_saved_path = f'filename_{random_number}.png'
    image.save(tmp_image_saved_path)

    bucket_id = 'ai-todo-list.appspot.com'

    upload_blob(bucket_id, tmp_image_saved_path, output_path)

    # add information about image to firebase realtime database
    sleep(5) # make sure new image is saved to storage bucket
    ref = db.reference(f'/{"/".join(source_path.split("/")[:-1])}', url='https://ai-todo-list.firebaseio.com/')
    ref.update({
        'hasImage' : 'true'
    })
    return JSONResponse(content={'message': "New image generated successfully."})

if __name__ == '__main__':
    default_app = firebase_admin.initialize_app() 
    uvicorn.run(app, host="0.0.0.0", port=8080)
