import json
import requests
from skimage import io, img_as_float
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from skimage.transform import resize

def download_image(url):
    response = requests.get(url)
    image = io.imread(response.content, plugin='imageio')
    return img_as_float(image)

# def compare_images(image1, image2):
#     image2_resized = resize(image2, image1.shape[:2], anti_aliasing=True)        
#     gray_image1 = rgb2gray(image1)
#     gray_image2 = rgb2gray(image2_resized)        
#     similarity_index, _ = ssim(gray_image1, gray_image2, full=True, data_range=1)
#     return similarity_index

def compare_images(image1, image2):
    # Resize both images to a common size
    common_size = (min(image1.shape[0], image2.shape[0]), min(image1.shape[1], image2.shape[1]))
    image1_resized = resize(image1, common_size, anti_aliasing=True)
    image2_resized = resize(image2, common_size, anti_aliasing=True)

    # Convert to grayscale
    gray_image1 = rgb2gray(image1_resized)
    gray_image2 = rgb2gray(image2_resized)

    # Calculate SSIM
    similarity_index, _ = ssim(gray_image1, gray_image2, full=True, data_range=1)
    return similarity_index



def handler(event, context):
    img_url1 = event['url1']
    img_url2 = event['url2']
    image1 = download_image(img_url1)
    image2 = download_image(img_url2)
    similarity = compare_images(image1, image2)
    return {'similarity_score': similarity * 100}

# Testing the function locally
if __name__ == '__main__':
    test_event = {
        "url2": "https://articlebucketgts.s3.ap-south-1.amazonaws.com/88/W4PTDO_13502.jpg",
        "url1": "https://articlebucketgts.s3.ap-south-1.amazonaws.com/seapi/download.jpeg"
    }
    test_context = None  # Context is not used in this example
    result = handler(test_event, test_context)
    print(result)
