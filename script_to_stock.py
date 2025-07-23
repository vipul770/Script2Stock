import requests
import os


PEXELS_API_KEY = 'PaWSkHy0bMWRPqLzoV6ejUSNlpgdfJGUD61xsGyT0YpOrMpc9EnX88qv'

PEXELS_VIDEO_API = 'https://api.pexels.com/videos/search'
PEXELS_IMAGE_API = 'https://api.pexels.com/v1/search'

HEADERS = {
    'Authorization': PEXELS_API_KEY
}


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_video(query, save_path='downloads/videos'):
    ensure_folder(save_path)
    params = {'query': query, 'per_page': 1}
    res = requests.get(PEXELS_VIDEO_API, headers=HEADERS, params=params)

    if res.status_code == 200:
        videos = res.json().get('videos', [])
        if videos:
            url = videos[0]['video_files'][0]['link']
            filename = os.path.join(save_path, f"{query.replace(' ', '_')}.mp4")
            with open(filename, 'wb') as f:
                f.write(requests.get(url).content)
            print(f"Video saved: {filename}")
        else:
            print(f"No video found for: {query}")
    else:
        print(f"API error ({res.status_code}) for: {query}")

def download_image(query, save_path='downloads/images'):
    ensure_folder(save_path)
    params = {'query': query, 'per_page': 1}
    res = requests.get(PEXELS_IMAGE_API, headers=HEADERS, params=params)

    if res.status_code == 200:
        photos = res.json().get('photos', [])
        if photos:
            url = photos[0]['src']['original']
            filename = os.path.join(save_path, f"{query.replace(' ', '_')}.jpg")
            with open(filename, 'wb') as f:
                f.write(requests.get(url).content)
            print(f"Image saved: {filename}")
        else:
            print(f"No image found for: {query}")
    else:
        print(f"API error ({res.status_code}) for: {query}")

def process_script(script):
    lines = [line.strip() for line in script.strip().split('\n') if line.strip()]
    for line in lines:
        print(f"\nSearching for: {line}")
        download_video(line)
        download_image(line)

script_text = """
A sunrise over the mountains
People jogging on the beach
A crowded street in New York
Children playing in a park
A campfire at night in the forest
"""

process_script(script_text)
