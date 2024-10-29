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
snapshot(screenshot_path)

# Check if the file exists
if not os.path.exists(screenshot_path):
    print(f"Screenshot not found at {screenshot_path}")
else:
    # Step 2: Open the screenshot using PIL
    image = Image.open(screenshot_path)

    # Step 3: Crop the image to the specified region (left, upper, right, lower)
    left = 2000  # Decrease this value to widen the crop towards the left
    upper = 35
    right = 2250
    lower = 135
    crop_box = (left, upper, right, lower)  # Define the crop box
    cropped_image = image.crop(crop_box)

    # Save the cropped image for debugging (optional)
    cropped_image_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\cropped_image.png'  # Update this path as needed
    cropped_image.save(cropped_image_path)

    # Step 4: Improve the image quality (convert to grayscale and enhance contrast)
    cropped_image = cropped_image.convert('L')  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(cropped_image)
    enhanced_image = enhancer.enhance(2.0)  # Increase contrast

    # Save the enhanced cropped image for debugging (optional)
    enhanced_image_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\stars_func\\enhanced_cropped_image.png'  # Update this path as needed
    enhanced_image.save(enhanced_image_path)

    # Step 5: Use pytesseract to extract the text from the enhanced cropped image
    extracted_text = pytesseract.image_to_string(enhanced_image)

    # Debug: Print the raw extracted text
    print(f"Extracted Text: '{extracted_text}'")

    # Step 6: Optionally, process the extracted text (e.g., find specific values)
    numbers = ''.join(filter(str.isdigit, extracted_text))
    extracted_numbers = numbers  # Save extracted numbers in a variable

    if extracted_numbers:
        print(f"Extracted Numbers: {extracted_numbers}")
        
        # Convert the extracted numbers to an integer
        try:
            extracted_numbers_int = int(extracted_numbers)  # Convert to int
            expected_coins = extracted_numbers_int + 6500  # Perform addition
        except ValueError:
            print("Error: The extracted number is not a valid integer.")
            expected_coins = 0  # Set to a default or handle error
    else:
        print("No numbers were extracted from the image.")
        expected_coins = 6500  # Default if no numbers are extracted

    # Define a function to perform touch actions and update coins
    def perform_touch_and_update_coins(template_path, coin_increment):
        global extracted_numbers_int  # Use the integer version
        touch(Template(template_path, resolution=(2560, 1600)))
        sleep(5)  # Wait for the action to complete
        extracted_numbers_int += coin_increment  # Update the integer variable

    # Start performing actions
    touch(Template(r"tpl1729768161494.png", record_pos=(0.468, -0.201), resolution=(2340, 1080)))

    if not exists(Template(r"tpl1729682994210.png", record_pos=(-0.0, -0.003), resolution=(2560, 1600))):
        # Alternative actions if the first condition is not met
        print("Coins VGP detected. Performing it.")
        touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
        sleep(5)
        perform_touch_and_update_coins(r"tpl1729599241291.png", 2500)
        sleep(4)

        touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729599986214.png", 150)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729600704210.png", 350)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729600810661.png", 550)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729601355758.png", 950)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729601472369.png", 2000)
    else:
        touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729599986214.png", 150)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729600704210.png", 350)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729600810661.png", 550)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729601355758.png", 950)

        # Next section
        sleep(4)
        touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
        sleep(4)
        perform_touch_and_update_coins(r"tpl1729601472369.png", 2000)

        # Touch actions at the end
        touch(Template(r"tpl1729600096931.png", resolution=(2560, 1600)))
        sleep(4)

        touch(Template(r"tpl1729768161494.png", record_pos=(0.468, -0.201), resolution=(2340, 1080)))
        sleep(5)
        touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
        sleep(5)
        perform_touch_and_update_coins(r"tpl1729599241291.png", 2500)

# Print results
print("\n\n===================================================================================\n")
print("Total Number of Coins:", extracted_numbers_int)  # Print the updated integer
assert_equal(expected_coins, extracted_numbers_int, "Please fill in the test point.")
print("\n\n===================================================================================\n")
