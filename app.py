import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io

st.title("Image Editor")

image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if image_file is not None:
    original_image = Image.open(image_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    # Sidebar for image editing options
    st.sidebar.header("Image Editing Options")

    contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
    rotation = st.sidebar.slider("Rotation", -180, 180, 0)
    width = st.sidebar.number_input("Width", value=original_image.width, min_value=1)
    height = st.sidebar.number_input("Height", value=original_image.height, min_value=1)

    # Image enhancement - contrast, rotation, and resizing
    enhanced_image = ImageEnhance.Contrast(original_image).enhance(contrast)
    rotated_image = enhanced_image.rotate(rotation)
    resized_image = rotated_image.resize((width, height))

    # Flip options
    flip_direction = st.sidebar.radio("Flip Direction", ("None", "Horizontal", "Vertical"))

    # Apply flipping based on user selection
    if flip_direction == "Horizontal":
        flipped_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_direction == "Vertical":
        flipped_image = resized_image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        flipped_image = resized_image

    # Filter options
    filter_type = st.sidebar.radio("Filter", ("Original", "Blur", "Sharpen", "Grayscale"))

    # Apply selected filter
    if filter_type == "Blur":
        filtered_image = flipped_image.filter(ImageFilter.BLUR)
    elif filter_type == "Sharpen":
        filtered_image = flipped_image.filter(ImageFilter.SHARPEN)
    elif filter_type == "Grayscale":
        filtered_image = flipped_image.convert("L")
    else:
        filtered_image = flipped_image

    st.image(filtered_image, caption="Final Image", use_column_width=True)

    # Download final image
    if st.sidebar.button("Download Final Image"):
        final_img_bytes = io.BytesIO()
        filtered_image.save(final_img_bytes, format="PNG")
        st.sidebar.download_button(
            label="Download Final Image",
            data=final_img_bytes.getvalue(),
            file_name="final_image.png",
            mime="image/png"
        )
