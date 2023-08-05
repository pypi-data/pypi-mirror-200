import sys
import requests

def download_image(url, output_path):
    """
    Download an image from the specified URL and save it to the output_path.
    
    Args:
        url (str): The URL of the image to download.
        output_path (str): The local file path where the image will be saved.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Image downloaded to {output_path}")

def main():
    """
    The main function of the script. It parses the command-line arguments and calls
    the download_image function with a hardcoded image URL.
    """
    if len(sys.argv) < 2:
        print("Usage: image-downloader <output_path>")
        sys.exit(1)

    url = "https://example.com/image.jpg"  # Replace with the specific image URL
    output_path = sys.argv[1]

    download_image(url, output_path)

if __name__ == "__main__":
    main()
