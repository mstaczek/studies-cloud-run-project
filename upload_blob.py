from google.cloud import storage
import io
import matplotlib.pyplot as plt


def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    print('Trying to upload file to bucket')
    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )



def upload_blob_old(bucket_name, image, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    #
    # Image
    # Image object 
    #
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    buf = io.BytesIO()

    plt.imshow(image)
    plt.axis('off')
    plt.savefig(buf, format='png')

    blob.upload_from_string(
        buf.getvalue(),
        content_type='image/png')

    buf.close()