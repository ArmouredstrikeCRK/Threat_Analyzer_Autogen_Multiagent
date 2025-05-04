import os
import requests
import json
dir = os.getcwd()
print("Current Directory: ", dir)
INPUT_DIR  = dir+"/Data/Images"
OUTPUT_DIR = dir+"/Data/Responses"

print("Input Directory: ", INPUT_DIR)
print("Output Directory: ", OUTPUT_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)
# URL of the service
URL        = "http://127.0.0.1:8000/analyze_image_agent"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    
    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith(exts):
            continue
        
        in_path  = os.path.join(INPUT_DIR, fname)
        out_name = os.path.splitext(fname)[0] + '.json'
        out_path = os.path.join(OUTPUT_DIR, out_name)
        
        with open(in_path, 'rb') as img_file:
            # service expects the image under "file"
            files = {'file': (fname, img_file, 'application/octet-stream')}
            try:
                resp = requests.post(URL, files=files)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"[ERROR] {fname}: {e}")
                continue
        
        # write JSON (or raw text on parse failure)
        try:
            data = resp.json()
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except ValueError:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(resp.text)
        
        print(f"[OK]   {fname} → {out_name}")

if __name__ == "__main__":
    main()
