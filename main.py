# Import necessary modules
import io
import pathlib
import tkinter as tk
import requests
from bs4 import BeautifulSoup
from PIL import Image
import validators

# Define function to scrape images and convert to PDF
def get_pdf():
    # Get URL from entry field
    url = url_entry.get()

    # Check if URL is valid
    if not validators.url(url):
        info_label_2.configure(text="Please enter a valid URL.")
        return

    # Make request to URL and parse HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all image tags with class "slide-image" and get the source URLs
    img_tags = soup.find_all("img", class_="slide-image")
    img_srcs = [img_tag.get("srcset").split(",")[-1].strip().split(" ")[0].split("?")[0] for img_tag in img_tags]

    # Download images and create list of Image objects
    images = []
    for src in img_srcs:
        try:
            response = requests.get(src)
            image_bytes = io.BytesIO(response.content)
            image = Image.open(image_bytes)
            images.append(image)
        except:
            info_label_2.configure(text="Error: Could not download image from URL.")
            return

    # Create PDF file from images
    try:
        file_name = f"{soup.title.string}.pdf"
        images[0].save(file_name, save_all=True, append_images=images[1:])
        info_label_2.configure(text=f"PDF downloaded to {pathlib.Path().resolve() / file_name}.")
    except:
        info_label_2.configure(text="Error: Could not create PDF from images.")

# Create GUI window
window = tk.Tk()
window.geometry("300x300")
window.title("Slideshare to PDF")
window.resizable(False, False)
window.configure(background="aliceblue")

# Add input field and button to window
url_var = tk.StringVar()
url_entry = tk.Entry(window, textvariable=url_var, width="30")
url_entry.place(x=50, y=50)
pdf_button = tk.Button(window, text="Get PDF", command=get_pdf, width="25", height="2", bg="grey")
pdf_button.place(x=50, y=100)

# Add info label to window
info_label = tk.Label(window, text="Enter the presentation link\nMake sure you have a good internet connection.")
info_label.place(x=35, y=200)
info_label_2 = tk.Label(window, text="")
info_label_2.place(x=50, y=250)

# Start event loop
window.mainloop()
