import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import io
import rembg
from fpdf import FPDF
import PyPDF2
import os
import fitz
import subprocess
import os
import tempfile


# Function to apply dynamic image adjustments
def process_image(img, contrast, brightness, sharpness, blur_radius, sepia, posterize, emboss, edge_detect, color_balance, noise, invert, grayscale, vignette, solarize, cartoonify, unsharp_mask, background_removal, crop, resize_width, resize_height, rotation, flip_horizontal, flip_vertical):
    # Apply crop if selected
    if crop:
        img = crop_image(img)
    
    # Resize image if selected
    if resize_width > 0 and resize_height > 0:
        img = img.resize((resize_width, resize_height))
    
    # Apply rotation if selected
    if rotation != 0:
        img = img.rotate(rotation, expand=True)
    
    # Apply flip if selected
    if flip_horizontal:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    if flip_vertical:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    # Adjust contrast, brightness, and sharpness
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)
    
    # Apply blur if selected
    if blur_radius > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Apply sepia filter
    if sepia:
        img = apply_sepia(img)
    
    # Apply posterize effect
    if posterize:
        img = ImageOps.posterize(img, 2)
    
    # Apply emboss effect
    if emboss:
        img = img.filter(ImageFilter.EMBOSS)
    
    # Apply edge detection
    if edge_detect:
        img = img.filter(ImageFilter.FIND_EDGES)
    
    # Adjust color balance (hue, saturation, lightness)
    if color_balance:
        img = adjust_color_balance(img)
    
    # Add noise to the image
    if noise:
        img = add_noise(img)
    
    # Apply invert effect
    if invert:
        img = ImageOps.invert(img.convert("RGB"))
    
    # Apply grayscale effect
    if grayscale:
        img = img.convert("L")
    
    # Apply vignette effect
    if vignette:
        img = apply_vignette(img)
    
    # Apply solarize effect
    if solarize:
        img = ImageOps.solarize(img, threshold=128)
    
    # Apply cartoon effect
    if cartoonify:
        img = apply_cartoonify(img)
    
    # Apply unsharp mask
    if unsharp_mask:
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    
    # Background removal
    if background_removal:
        img = remove_background(img)
    
    return img

# Apply sepia filter
def apply_sepia(img):
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return img

# Adjust hue, saturation, and lightness (HSL)
def adjust_color_balance(img):
    img = img.convert("HSV")
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            h, s, v = img.getpixel((px, py))
            # Example: Increase saturation and lightness
            s = int(s * 1.5)  # Increase saturation by 50%
            v = int(v * 1.2)  # Increase brightness by 20%
            img.putpixel((px, py), (h, s, v))

    img = img.convert("RGB")
    return img

# Add noise to the image
def add_noise(img):
    width, height = img.size
    pixels = img.load()
    noise_intensity = 25  # Adjust noise intensity
    
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            r += np.random.randint(-noise_intensity, noise_intensity)
            g += np.random.randint(-noise_intensity, noise_intensity)
            b += np.random.randint(-noise_intensity, noise_intensity)
            
            # Ensure pixel values stay within valid range
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            
            pixels[px, py] = (r, g, b)

    return img

# Apply vignette effect
def apply_vignette(img):
    width, height = img.size
    pixels = img.load()
    center_x, center_y = width // 2, height // 2
    max_distance = np.sqrt(center_x**2 + center_y**2)
    
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            distance = np.sqrt((px - center_x) ** 2 + (py - center_y) ** 2)
            factor = 1 - (distance / max_distance) * 0.5
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            img.putpixel((px, py), (r, g, b))
    
    return img

# Apply cartoonify effect
def apply_cartoonify(img):
    # Convert to edge-detection first
    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.convert("RGB")
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img

# Remove background using rembg
def remove_background(img):
    try:
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        # Use rembg to remove background
        output = rembg.remove(img_bytes)
        output_img = Image.open(io.BytesIO(output))

        return output_img
    except Exception as e:
        st.error(f"Error in background removal: {str(e)}")
        return img

# Crop image function
def crop_image(img):
    width, height = img.size
    left = st.slider("Left", 0, width, 0)
    right = st.slider("Right", 0, width, width)
    top = st.slider("Top", 0, height, 0)
    bottom = st.slider("Bottom", 0, height, height)
    
    return img.crop((left, top, right, bottom))

# Sidebar with navigation
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose an option", ["Image Editor", "Image to PDF", "YouTube Downloader"])

    if app_mode == "Image Editor":
        image_editor()
    elif app_mode == "Image to PDF":
        pdf_app()
    elif app_mode == "YouTube Downloader":
        youtube_downloader()

# Image editor page
def image_editor():
    st.title("Image Editor")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Image", use_column_width=True)

        # Image adjustments controls
        st.sidebar.header("Adjust Image Settings")
        
        contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
        brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
        sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)

        blur_radius = st.sidebar.slider("Blur Radius", 0, 5, 0)

        crop = st.sidebar.checkbox("Crop Image")
        resize_width = st.sidebar.slider("Resize Width", 50, 2000, img.width)
        resize_height = st.sidebar.slider("Resize Height", 50, 2000, img.height)
        rotation = st.sidebar.slider("Rotate Image (degrees)", -180, 180, 0)
        flip_horizontal = st.sidebar.checkbox("Flip Horizontal")
        flip_vertical = st.sidebar.checkbox("Flip Vertical")
        
        sepia = st.sidebar.checkbox("Apply Sepia Filter")
        posterize = st.sidebar.checkbox("Apply Posterize Effect")
        emboss = st.sidebar.checkbox("Apply Emboss Effect")
        edge_detect = st.sidebar.checkbox("Apply Edge Detection")
        color_balance = st.sidebar.checkbox("Adjust Color Balance (Saturation/Lightness)")
        noise = st.sidebar.checkbox("Add Noise to Image")
        invert = st.sidebar.checkbox("Invert Colors")
        grayscale = st.sidebar.checkbox("Apply Grayscale Effect")
        vignette = st.sidebar.checkbox("Apply Vignette Effect")
        solarize = st.sidebar.checkbox("Apply Solarize Effect")
        cartoonify = st.sidebar.checkbox("Apply Cartoonify Effect")
        unsharp_mask = st.sidebar.checkbox("Apply Unsharp Mask")
        background_removal = st.sidebar.checkbox("Remove Image Background")

        # Process image with selected adjustments
        edited_img = process_image(img, contrast, brightness, sharpness, blur_radius, sepia, posterize, emboss, edge_detect, color_balance, noise, invert, grayscale, vignette, solarize, cartoonify, unsharp_mask, background_removal, crop, resize_width, resize_height, rotation, flip_horizontal, flip_vertical)
        
        # Convert the image to RGB before saving as JPEG
        if edited_img.mode == 'RGBA':
            edited_img = edited_img.convert('RGB')

        st.image(edited_img, caption="Edited Image", use_column_width=True)

        # Download option
        with io.BytesIO() as buffer:
            edited_img.save(buffer, format="JPEG")
            buffer.seek(0)
            st.download_button(
                label="Download Edited Image",
                data=buffer,
                file_name="edited_image.jpg",
                mime="image/jpeg"
            )

def pdf_app():
    # Title for the app
    st.title("PDF Processing App")
    st.write("This is where you can convert images to PDFs")

    # Upload images to convert to PDF
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Function to create PDF from images
    def images_to_pdf(images):
        pdf = FPDF()
        for img in images:
            im = Image.open(img)
            im = im.convert("RGB")
            temp_path = "temp_image.jpg"
            im.save(temp_path, quality=85)  # Save image with reduced quality
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=180)
            os.remove(temp_path)  # Clean up the temporary image file
        return pdf

    # Function to compress the PDF using PyMuPDF
 
    # Function to rename the PDF file


    # If files are uploaded, proceed
    if uploaded_files:
        # Save the uploaded images temporarily
        image_paths = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_path = f"temp_{uploaded_file.name}"
            image.save(image_path)
            image_paths.append(image_path)

        # Convert images to PDF
        if st.button("Convert Images to PDF"):
            try:
                pdf = images_to_pdf(image_paths)
                pdf_output = "output.pdf"
                pdf.output(pdf_output)

                st.success(f"PDF created successfully: {pdf_output}")

                # Provide download link for the generated PDF
                with open(pdf_output, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=pdf_output,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error converting images to PDF: {e}")

        # Option to compress the generated PDF

st.set_page_config(page_title="YouTube Downloader", layout="centered")
def youtube_downloader():
    # Streamlit UI Code Inside the youtube_downloader Function
    st.title("YouTube Video Downloader")

    # Input fields for video URL and type (Single Video/Playlist)
    with st.container():
        st.markdown("### Input Video Details")
        url = st.text_input("Enter YouTube URL", key="url_input")
        option = st.selectbox("Download Type", ("Single Video", "Playlist"), key="download_type")
        is_playlist = option == "Playlist"

    # Options for video quality and subtitles
    with st.container():
        st.markdown("### Options")
        quality = st.selectbox(
            "Select Video Quality",
            ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "Best Available"],
            index=4,
            key="quality_select"
        )
        subtitles = st.checkbox("Add Subtitles", key="subtitles_checkbox")

    # Download button
    with st.container():
        download_button = st.button("Download", key="download_button")

    # Handle the download when the button is clicked
    if download_button:
        if not url:
            st.error("Please provide a valid YouTube URL.")
        else:
            try:
                with st.spinner("Downloading... Please wait."):
                    # Call the function to download the video
                    temp_dir = tempfile.mkdtemp()

                    # Base command for yt-dlp
                    cmd = ["yt-dlp", "-o", os.path.join(temp_dir, "%(title)s.%(ext)s")]

                    # Add format options for video and audio based on selected quality
                    if quality == "144p":
                        cmd += ["-f", "bv*[height<=144][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "240p":
                        cmd += ["-f", "bv*[height<=240][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "360p":
                        cmd += ["-f", "bv*[height<=360][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "480p":
                        cmd += ["-f", "bv*[height<=480][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "720p":
                        cmd += ["-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "1080p":
                        cmd += ["-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "1440p":
                        cmd += ["-f", "bv*[height<=1440][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    elif quality == "2160p":
                        cmd += ["-f", "bv*[height<=2160][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
                    else:
                        cmd += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"]

                    # Set output format to mp4
                    cmd += ["--merge-output-format", "mp4"]

                    # Subtitles options
                    if subtitles:
                        cmd += ["--write-sub", "--sub-lang", "en", "--embed-subs"]

                    # Playlist or single video
                    if is_playlist:
                        cmd += ["-o", os.path.join(temp_dir, "%(playlist_index)s. %(title)s.%(ext)s")]
                    else:
                        cmd += ["-o", os.path.join(temp_dir, "%(title)s.%(ext)s")]

                    # Add the URL
                    cmd.append(url)

                    # Execute the command
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Check for errors
                    if result.returncode != 0:
                        st.error(f"Error occurred: {result.stderr}")
                        return None

                    # Return the path to the downloaded file
                    downloaded_file = [f for f in os.listdir(temp_dir) if f.endswith('.mp4') or f.endswith('.mkv') or f.endswith('.webm')][0]
                    file_path = os.path.join(temp_dir, downloaded_file)

                    # Provide a download link/button for the user to download the video
                    if file_path:
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download Video",
                                data=file,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4"
                            )

                st.success("Download completed successfully!")

            except subprocess.CalledProcessError:
                st.error("An error occurred during the download. Please check the URL and try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()