# import pytesseract
# from PIL import Image, ImageEnhance
# import os

# # Set the path to the Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Hamza.Naseer\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# # Step 1: Specify the path to the existing screenshot
# screenshot_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\screen_snapshot.png'  # Update this path to your screenshot location

# # Check if the file exists
# if not os.path.exists(screenshot_path):
#     print(f"Screenshot not found at {screenshot_path}")
# else:
#     # Step 2: Open the screenshot using PIL
#     image = Image.open(screenshot_path)

#     # Step 3: Crop the image to the specified region (left, upper, right, lower)
#     left = 2000  # Decrease this value to widen the crop towards the left
#     upper = 45
#     right = 2382
#     lower = 135
#     crop_box = (left, upper, right, lower)  # Define the crop box
#     cropped_image = image.crop(crop_box)

#     # Save the cropped image for debugging (optional)
#     cropped_image_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\cropped_image.png'  # Update this path as needed
#     cropped_image.save(cropped_image_path)

#     # Step 4: Improve the image quality (convert to grayscale and enhance contrast)
#     cropped_image = cropped_image.convert('L')  # Convert to grayscale
#     enhancer = ImageEnhance.Contrast(cropped_image)
#     enhanced_image = enhancer.enhance(2.0)  # Increase contrast

#     # Save the enhanced cropped image for debugging (optional)
#     enhanced_image_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\enhanced_cropped_image.png'  # Update this path as needed
#     enhanced_image.save(enhanced_image_path)

#     # Step 5: Use pytesseract to extract the text from the enhanced cropped image
#     extracted_text = pytesseract.image_to_string(enhanced_image)

#     # Debug: Print the raw extracted text
#     print(f"Extracted Text: '{extracted_text}'")

#     # Step 6: Optionally, process the extracted text (e.g., find specific values)
#     numbers = ''.join(filter(str.isdigit, extracted_text))
#     if numbers:
#         print(f"Extracted Numbers: {numbers}")
#     else:
#         print("No numbers were extracted from the image.")


from airtest.core.api import *
import pytesseract
from PIL import Image, ImageEnhance
import os

# Connect to the Android device (or iOS if applicable)
connect_device("Android:///")  # Adjust as necessary for iOS

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Hamza.Naseer\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Step 1: Take a screenshot using Airtest
screenshot_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\screen_snapshot.png'
snapshot(screenshot_path)  # This will take a screenshot

# Continue with your existing processing...
