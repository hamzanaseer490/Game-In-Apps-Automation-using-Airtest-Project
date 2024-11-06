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
        print(f"The device is a TABLET & variable is '{mobile_device}'")
        subsequent_crop_box = (600, 345, 1882, 450)  # Crop box for all other screenshots
        print(f"Using crop box of TABLET '{subsequent_crop_box}'")
    else:
        print("The device is a mobile phone.")
        mobile_device = True
        print(f"The device is a MOBILE & variable is '{mobile_device}'")
        subsequent_crop_box = (50, 1435, 1050, 1670)  # Crop box for all other screenshots
        print(f"Using crop box of MOBILE '{subsequent_crop_box}'")
else:
    print("No device connected.")

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Hamza.Naseer\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Define different crop regions for the initial and subsequent screenshots
initial_crop_box = (1400, 35, 1950, 135)  # Crop box for the first screenshot

# Step 1: Take and process the first screenshot
first_screenshot_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\stars_in-apps\\screen_snapshot.png'
snapshot(first_screenshot_path)

# Open and enhance the first screenshot
image = Image.open(first_screenshot_path)
initial_cropped_image = image.crop(initial_crop_box).convert('L')
enhancer = ImageEnhance.Contrast(initial_cropped_image)
enhanced_initial_image = enhancer.enhance(2.0)

# Save the enhanced first screenshot without using the counter
enhanced_first_path = r'C:\\Users\\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\stars_in-apps\\enhanced_first_image.png'
enhanced_initial_image.save(enhanced_first_path)

# Extract numbers from the first enhanced screenshot
extracted_text = pytesseract.image_to_string(enhanced_initial_image)
print(f"Extracted Text: '{extracted_text}'")

# Extract digits from the text and convert to an integer, or default to 0 if no digits found
digits = ''.join(filter(str.isdigit, extracted_text))
initial_number = int(digits) if digits else 0

print(f"Initial Number: {initial_number}")

# Global variable for running total of stars
extracted_numbers_int = initial_number
expected_stars = extracted_numbers_int + 345

# Initialize a counter for subsequent screenshots
screenshot_counter = 1

# Initialize a list to hold results of comparisons
results = []

# Function to convert extracted number to a float for comparison
def convert_to_float(num_str):
    if num_str is None:
        return None  # Return None if the input is None
    try:
        return float(num_str)
    except ValueError:
        return None  # Return None if conversion fails

# Define a function to perform touch actions, take screenshots, crop, enhance, save, and compare extracted numbers

def perform_touch_and_update_stars(template_path, coin_increment, variable_to_match):
    global extracted_numbers_int, screenshot_counter

    # Take and save a screenshot before each touch action
    screenshot_name = f"in-app{screenshot_counter}.png"
    screenshot_full_path = os.path.join(r'C:\\Users\\Hamza.Naseer\\Downloads\\Game In-Apps Automation using Airtest Project\\stars_in-apps\\In Apps Images\\', screenshot_name)
    snapshot(screenshot_full_path)

    # Open and enhance the new screenshot with subsequent_crop_box
    image = Image.open(screenshot_full_path)
    cropped_image = image.crop(subsequent_crop_box).convert('L')  # Convert to grayscale
    contrast_enhancer = ImageEnhance.Contrast(cropped_image)
    enhanced_image = contrast_enhancer.enhance(2.5).filter(ImageFilter.SHARPEN)

    # Save the enhanced cropped screenshot
    enhanced_screenshot_path = os.path.join(r'C:\\Users\Hamza.Naseer\\Downloads\Game In-Apps Automation using Airtest Project\\stars_in-apps\Ehanced Images\\', f"enhanced_image_{screenshot_counter}.png")
    enhanced_image.save(enhanced_screenshot_path)
    screenshot_counter += 1

    # Use pytesseract to extract the text from the enhanced cropped image
    custom_config = r'--psm 6 -c tessedit_char_whitelist="0123456789,."'
    extracted_text = pytesseract.image_to_string(enhanced_image, config=custom_config)

    print(f"Extracted Text: '{extracted_text}'")

    # Initialize quantity and price as None
    quantity = None
    price = None

    # Extract quantity and price from the text
    numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', extracted_text)  # Matches numbers with commas and decimals

    # Ensure we have at least two numbers for quantity and price
    if len(numbers) >= 2:
        # Remove commas and convert the first number to integer for quantity
        quantity = int(numbers[0].replace(',', ''))
        
        # Remove commas and convert the second number to float for price
        price = float(numbers[1].replace(',', ''))

        # Check if price might be missing decimal by evaluating its range
        if price >= 1000 and not '.' in numbers[1]:  # If price seems unusually high and lacks a decimal
            price /= 100

        print(f"Extracted Quantity: {quantity}")
        print(f"Extracted Price: {price:,.2f}")
    else:
        print("Insufficient numbers extracted. Quantity and price could not be determined.")
        return  # Exit if values aren't sufficient

    # Compare extracted values with expected values
    extracted_quantity = quantity
    extracted_price = price

    compare_extracted_values(screenshot_counter, extracted_quantity, extracted_price, variable_to_match[0], variable_to_match[1])

    # Perform touch action and increment stars
    touch(Template(template_path, resolution=(2560, 1600)))
    sleep(5)  # Wait for the action to complete
    extracted_numbers_int += coin_increment


# Function to compare extracted values with expected values
def compare_extracted_values(screenshot_counter, extracted_quantity, extracted_price, variable_quantity, variable_price):
    global results  # Reference the results list
    result_entry = {
        'screenshot_counter': screenshot_counter,
        'extracted_quantity': extracted_quantity,
        'extracted_price': extracted_price,
        'expected_quantity': variable_quantity,
        'expected_price': variable_price,
        'quantity_match': False,
        'price_match': False,
        'status': 'Fail'  # Default status as 'Fail'
    }

    if screenshot_counter > 0:  # Skip comparison for the very first call
        extracted_quantity_float = convert_to_float(extracted_quantity)
        extracted_price_float = convert_to_float(extracted_price)
        variable_quantity_float = convert_to_float(variable_quantity)
        variable_price_float = convert_to_float(variable_price)

        # Compare Quantity
        if extracted_quantity_float is not None and variable_quantity_float is not None:
            if extracted_quantity_float == variable_quantity_float:
                print(f"Quantity match found for screenshot {screenshot_counter - 1}: Extracted = {extracted_quantity_float}, Expected = {variable_quantity_float}")
                result_entry['quantity_match'] = True  # Update the result entry
            else:
                print(f"Quantity mismatch for screenshot {screenshot_counter - 1}: Extracted = {extracted_quantity_float}, Expected = {variable_quantity_float}")

        # Compare Price only if variable_price is not None
        if variable_price_float is not None:
            if extracted_price_float is not None:
                if extracted_price_float == variable_price_float:
                    print(f"Price match found for screenshot {screenshot_counter - 1}: Extracted = {extracted_price_float}, Expected = {variable_price_float}")
                    result_entry['price_match'] = True  # Update the result entry
                else:
                    print(f"Price mismatch for screenshot {screenshot_counter - 1}: Extracted = {extracted_price_float}, Expected = {variable_price_float}")
            else:
                print(f"No price extracted for screenshot {screenshot_counter - 1}, expected price was {variable_price_float}")

        # Set status to 'Pass' if both quantity and price match
        if result_entry['quantity_match'] and result_entry['price_match']:
            result_entry['status'] = 'Pass'

    else:
        print(f"Skipping comparison for the first screenshot: Quantity = {extracted_quantity}, Price = {extracted_price}")

    # Append the result entry to the results list
    results.append(result_entry)

# Start performing actions with screenshots, cropping, and number extraction/comparisons

touch(Template(r"tpl1730784065379.png", record_pos=(0.258, -0.202), resolution=(2340, 1080)))

sleep(2)

if not exists(Template(r"tpl1730784087753.png", record_pos=(-0.024, 0.032), resolution=(2340, 1080))):
    # Alternative actions if the first condition is not met
    print("Coins VGP detected. Performing it.")
    touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1730883540360.png", 150, (150, 2300.00))
    sleep(6)

    touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729599986214.png", 5, (5, 280.00))

    sleep(6)
    touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729600704210.png", 15, (15, 550.00))

    sleep(6)
    touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729600810661.png", 30, (30, 1100.00))

    sleep(6)
    touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729601355758.png", 45, (45, 1700.00))

    sleep(6)
    touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729601472369.png", 100, (100, 2800.00))
else:
    touch(Template(r"tpl1729599963378.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729599986214.png", 5, (5, 280.00))
    sleep(6)
    touch(Template(r"tpl1729600787446.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729600704210.png", 15, (15, 550.00))
    sleep(6)
    touch(Template(r"tpl1729600775153.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729600810661.png", 30, (30, 1100.00))
    sleep(6)
    touch(Template(r"tpl1729601324576.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729601355758.png", 45, (45, 1700.00))
    sleep(6)
    touch(Template(r"tpl1729601468555.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1729601472369.png", 100, (100, 2800.00))



    touch(Template(r"tpl1729600096931.png", resolution=(2560, 1600)))
    sleep(6)

    touch(Template(r"tpl1730784065379.png", record_pos=(0.258, -0.202), resolution=(2340, 1080)))
    sleep(6)
    touch(Template(r"tpl1729599219507.png", resolution=(2560, 1600)))
    sleep(6)
    perform_touch_and_update_stars(r"tpl1730883540360.png", 150, (150, 2300.00))
    

# Print results
print("\n\n===================================================================================\n")
print("Total Number of Coins:", extracted_numbers_int)
assert_equal(expected_stars, extracted_numbers_int, "Please fill in the test point.")
print("\n\n===================================================================================\n")


def print_report():
    total_entries = len(results)
    passed_count = sum(1 for result in results if result['status'] == 'Pass')
    failed_count = total_entries - passed_count

    print("\nIn-App Purchase Comparison Report")
    print("=" * 30)
    print(f"Total comparisons: {total_entries}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}\n")
    print("Detailed Results:")
    print("-" * 30)
    
    for result in results:
        print(f"Screenshot {result['screenshot_counter']}:")
        print(f"  Extracted Quantity: {result['extracted_quantity']} | Expected Quantity: {result['expected_quantity']} | Match: {result['quantity_match']}")
        print(f"  Extracted Price: {result['extracted_price']} | Expected Price: {result['expected_price']} | Match: {result['price_match']}")
        print(f"  Status: {result['status']}")
        print("-" * 30)

# After all comparisons, call the report function
print_report()




