import os
import requests
from duckduckgo_search import ddg_images

# 🔑 Pexels API key for videos
PEXELS_API_KEY = "PaWSkHy0bMWRPqLzoV6ejUSNlpgdfJGUD61xsGyT0YpOrMpc9EnX88qv"
PEXELS_VIDEO_API = 'https://api.pexels.com/videos/search'

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Downloaded: {save_path}")
        else:
            print(f"❌ Failed: {url}")
    except Exception as e:
        print(f"⚠️ Error downloading: {e}")

def search_image(query, folder='downloads/images'):
    ensure_folder(folder)
    print(f"🔍 Searching image for: {query}")
    try:
        results = ddg_images(query, max_results=1)
        if results:
            img_url = results[0]['image']
            filename = os.path.join(folder, f"{query.replace(' ', '_')}.jpg")
            download_file(img_url, filename)
        else:
            print("❌ No image found.")
    except Exception as e:
        print(f"⚠️ DuckDuckGo error: {e}")

def search_video_pexels(query, folder='downloads/videos'):
    ensure_folder(folder)
    print(f"🎞️ Searching video for: {query}")
    try:
        headers = {'Authorization': PEXELS_API_KEY}
        params = {'query': query, 'per_page': 1}
        response = requests.get(PEXELS_VIDEO_API, headers=headers, params=params)
        if response.status_code == 200:
            videos = response.json().get('videos', [])
            if videos:
                video_url = videos[0]['video_files'][0]['link']
                filename = os.path.join(folder, f"{query.replace(' ', '_')}.mp4")
                download_file(video_url, filename)
            else:
                print("❌ No video found on Pexels.")
        else:
            print(f"❌ Pexels API error: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Pexels error: {e}")

def process_script(script):
    lines = [line.strip() for line in script.strip().split('\n') if line.strip()]
    for line in lines:
        print(f"\n📘 Processing: {line}")
        search_image(line)
        search_video_pexels(line)

# ✏️ Your input script
script_text = """
A sunrise over the ocean
A forest waterfall
Kids flying kites
Busy traffic at night
Birds flying over mountains
"""

process_script(script_text)
