import hashlib
import time
from win10toast import ToastNotifier

"""
This checks a csv file for changes every .5 seconds and when there is a change it will print "CSV file has been modified." to the console
If you uncomment the two lines with the send_windows_notification function it will also send a windows notification to the user
Those are a little annoying so I commented them out since you have to close them manually and dont refresh automatically

"""

# Define the path to the CSV file you want to monitor
csv_file_path = 'C:/Users/pando/.vscode/PythonCode/FunScripts/RobotSim/dataName.csv'

# Function to calculate the MD5 checksum of a file
def calculate_checksum(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        checksum = hashlib.md5(data).hexdigest()
    return checksum

def send_windows_notification(title, message):      ##this adds popup and notification sound
    try:
        # Initialize the notification object
        toaster = ToastNotifier()

        # Display the notification with a sound
        toaster.show_toast(title, message, duration=10, threaded=True)
    except Exception as e:
        print(f"Error sending Windows notification: {e}")


# Initial checksum of the CSV file
initial_checksum = calculate_checksum(csv_file_path)

while True:
    time.sleep(.5)  # Adjust the interval as needed (optimal time)

    # Calculate the current checksum of the CSV file
    current_checksum = calculate_checksum(csv_file_path)

    # Compare the initial checksum with the current checksum
    if current_checksum != initial_checksum:            ##this is where the data has been updated so i can read it and graph it
        print("CSV file has been modified.")
        #send_windows_notification("CSV Update", "The CSV file has been updated!") ##remove this to drop the notification sonud
        # You can add code here to perform actions when the CSV file is updated
        initial_checksum = current_checksum  # Update the initial checksum

# Press Ctrl+C to stop the script