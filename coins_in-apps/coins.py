from airtest.core.api import *
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import re
from airtest.core.api import G


# Connect to the Android device (or iOS if applicable)
connect_device("Android:///")  # Adjust as necessary for iOS
mobile_device = True

# Ensure the device is connected
if G.DEVICE:
    # Get screen width and height
    width, height = G.DEVICE.display_info["width"], G.DEVICE.display_info["height"]

    # Set threshold to distinguish between tablet and mobile
    if width >= 1200 and height >= 800:  # Adjust based on typical tablet resolutions
        print("The device is a tablet.")
        mobile_device = False
        print(f"The device is a TABLET & varable is '{mobile_device}'")
        subsequent_crop_box = (600, 345, 1882, 450)  # Crop box for all other screenshots
        print(f"Using crop box of TABLET '{subsequent_crop_box}'")
    else:
        print("The device is a mobile phone.")
        mobile_device = True
        print(f"The device is a MOBILE & varable is '{mobile_device}'")
        subsequent_crop_box = (50, 1345, 1050, 1600)  # Crop box for all other screenshots
        print(f"Using crop box of MOBILE '{subsequent_crop_box}'")
else:
    print("No device connected.")


# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Hamza.Naseer\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Define different crop regions for the initial and subsequent screenshots
initial_crop_box = (1900, 35, 2250, 135)  # Crop box for the first screenshot

# Step 1: Take and process the first screenshot
first_screenshot_path = r'C:\\Users\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\coins_in-apps\\screen_snapshot.png'
snapshot(first_screenshot_path)

# Open and enhance the first screenshot
image = Image.open(first_screenshot_path)
initial_cropped_image = image.crop(initial_crop_box).convert('L')
enhancer = ImageEnhance.Contrast(initial_cropped_image)
enhanced_initial_image = enhancer.enhance(2.0)

# Save the enhanced first screenshot without using the counter
enhanced_first_path = r'C:\\Users\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\coins_in-apps\\enhanced_first_image.png'
enhanced_initial_image.save(enhanced_first_path)

# Extract numbers from the first enhanced screenshot
extracted_text = pytesseract.image_to_string(enhanced_initial_image)
print(f"Extracted Text: '{extracted_text}'")

# Extract digits from the text and convert to an integer, or default to 0 if no digits found
digits = ''.join(filter(str.isdigit, extracted_text))
initial_number = int(digits) if digits else 0

print(f"Initial Number: {initial_number}")

# Global variable for running total of coins
extracted_numbers_int = initial_number
expected_coins = extracted_numbers_int + 6500

# Initialize a counter for subsequent screenshots
screenshot_counter = 1

# Function to convert extracted number to a float for comparison
def convert_to_float(num_str):
    if num_str is None:
        return None  # Return None if the input is None
    try:
        return float(num_str)
    except ValueError:
        return None  # Return None if conversion fails

# Define a function to perform touch actions, take screenshots, crop, enhance, save, and compare extracted numbers
def perform_touch_and_update_coins(template_path, coin_increment, variable_to_match):
    global extracted_numbers_int, screenshot_counter

    # Take and save a screenshot before each touch action
    screenshot_name = f"in-app{screenshot_counter}.png"
    screenshot_full_path = os.path.join(r'C:\\Users\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\coins_in-apps\\In Apps Images\\', screenshot_name)
    snapshot(screenshot_full_path)

    # Open and enhance the new screenshot with subsequent_crop_box
    image = Image.open(screenshot_full_path)
    cropped_image = image.crop(subsequent_crop_box).convert('L')  # Convert to grayscale
    contrast_enhancer = ImageEnhance.Contrast(cropped_image)
    cropped_image = contrast_enhancer.enhance(2.5)
    enhanced_image = cropped_image.filter(ImageFilter.SHARPEN)

    # Save the enhanced cropped screenshot
    enhanced_screenshot_path = f'C:\\Users\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\coins_in-apps\\Ehanced Images\\enhanced_image_{screenshot_counter}.png'
    enhanced_image.save(enhanced_screenshot_path)
    screenshot_counter += 1

    # Step 5: Use pytesseract to extract the text from the enhanced cropped image
    custom_config = r'--psm 6 -c tessedit_char_whitelist="0123456789,."'
    extracted_text = pytesseract.image_to_string(enhanced_image, config=custom_config)

    print(f"Extracted Text: '{extracted_text}'")
    
    # Initialize quantity and price as None
    quantity = None
    price = None

    # Extract quantity and price from the text
    numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', extracted_text)  # Matches numbers with commas and decimals

    # Format the output for readability
    # Step 6: Updated regex pattern to match numbers with or without commas or decimals
    numbers = re.findall(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', extracted_text)
        
    # Ensure we have at least two numbers
    if len(numbers) >= 2:
        quantity = numbers[0].replace(',', '')  # Remove commas
        price = numbers[1].replace(',', '')     # Remove commas for float conversion
        print(f"Extracted Quantity: {int(quantity)}")
        print(f"Extracted Price: {float(price):,.2f}")
    else:
        print("Insufficient numbers extracted.")

    # Proceed to compare values
    extracted_quantity = quantity
    extracted_price = price

    # Compare extracted values
    compare_extracted_values(screenshot_counter, extracted_quantity, extracted_price, variable_to_match[0], variable_to_match[1])
    
    touch(Template(template_path, resolution=(2560, 1600)))
    sleep(5)  # Wait for the action to complete
    extracted_numbers_int += coin_increment 

# Function to compare extracted values with expected values
def compare_extracted_values(screenshot_counter, extracted_quantity, extracted_price, variable_quantity, variable_price):
    if screenshot_counter > 0:  # Skip comparison for the very first call
        extracted_quantity_float = convert_to_float(extracted_quantity)
        extracted_price_float = convert_to_float(extracted_price)
        variable_quantity_float = convert_to_float(variable_quantity)
        variable_price_float = convert_to_float(variable_price)

        # Compare Quantity
        if extracted_quantity_float is not None and variable_quantity_float is not None:
            if extracted_quantity_float == variable_quantity_float:
                print(f"Quantity match found for screenshot {screenshot_counter - 1}: Extracted = {extracted_quantity_float}, Expected = {variable_quantity_float}")
            else:
                print(f"Quantity mismatch for screenshot {screenshot_counter - 1}: Extracted = {extracted_quantity_float}, Expected = {variable_quantity_float}")

        # Compare Price only if variable_price is not None
        if variable_price_float is not None:
            if extracted_price_float is not None:
                if extracted_price_float == variable_price_float:
                    print(f"Price match found for screenshot {screenshot_counter - 1}: Extracted = {extracted_price_float}, Expected = {variable_price_float}")
                else:
                    print(f"Price mismatch for screenshot {screenshot_counter - 1}: Extracted = {extracted_price_float}, Expected = {variable_price_float}")
            else:
                print(f"No price extracted for screenshot {screenshot_counter - 1}, expected price was {variable_price_float}")
    else:
        print(f"Skipping comparison for the first screenshot: Quantity = {extracted_quantity}, Price = {extracted_price}")
        
        

# Start performing actions with screenshots, cropping, and number extraction/comparisons
touch(Template(r"tpl1729768161494.png", record_pos=(0.468, -0.201), resolution=(2340, 1080)))
sleep(2)

if not exists(Template(r"tpl1729682994210.png", record_pos=(-0.0, -0.003), resolution=(2560, 1600))):
    # Alternative actions if the first condition is not met
    print("Coins VGP detected. Performing it.")
    touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729599241291.png", 2500, (2500, 2300.00))
    sleep(6)

    touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729599986214.png", 150, (150, 280.00))

    sleep(6)
    touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729600704210.png", 350, (350, 550.00))

    sleep(6)
    touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729600810661.png", 550, (550, 1100.00))

    sleep(6)
    touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729601355758.png", 950, (950, 1700.00))

    sleep(6)
    touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729601472369.png", 2000, (2000, 2800.00))
else:
    touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729599986214.png", 150, (150, 280.00))
    sleep(6)
    touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729600704210.png", 350, (350, 550.00))
    sleep(6)
    touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729600810661.png", 550, (550, 1100.00))
    sleep(6)
    touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729601355758.png", 950, (950, 1700.00))
    sleep(6)
    touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729601472369.png", 2000, (2000, 2800.00))



    touch(Template(r"tpl1729600096931.png", resolution=(2560, 1600)))
    sleep(6)

    touch(Template(r"tpl1729768161494.png", record_pos=(0.468, -0.201), resolution=(2340, 1080)))
    sleep(6)
    touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_coins(r"tpl1729599241291.png", 2500, (2500, 2300.00))
    

# Print results
print("\n\n===================================================================================\n")
print("Total Number of Coins:", extracted_numbers_int)
assert_equal(expected_coins, extracted_numbers_int, "Please fill in the test point.")
print("\n\n===================================================================================\n")


