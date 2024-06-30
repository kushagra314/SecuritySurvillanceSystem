# security-surveillance-system-

## Description

This project implements a security surveillance system using machine learning to detect weapons and count the number of people in a video feed. The system alerts the user via SMS when the number of people exceeds a threshold or a weapon is detected.

## Features

- Real-time video processing
- Weapon detection
- Headcount detection
- SMS alerts using Twilio
- Supports webcam and other camera inputs

## Installation

### Prerequisites

- Python 3.12 or higher

### Clone the Repository

git clone https://github.com/Prem-101/security-surveillance-system.git
cd security-surveillance-system


### Install Dependencies

bash
pip install -r requirements.txt


### Download YOLO Model

Make sure you have the YOLOv9 model file (yolov9c.pt) in the project directory.

## Usage

### Run the Application

bash
python main.py


### Application Interface

- Enter a phone number to receive alerts.
- Choose between Camera 1, or Camera 2 for the video feed.

## Project Structure


security-surveillance-system/
├── detectObj.py
├── main.py
├── requirements.txt
├── README.md
├── yolov9c.pt

## Setup Environment Variables

1. Create a '.env' file in the root directory of the project:
   TWILIO_ACCOUNT_SID=your_new_account_sid
   TWILIO_AUTH_TOKEN=your_new_auth_token


- **detectObj.py**: Contains the Prg class for weapon and headcount detection.
- **main.py**: Main application script.
- **requirements.txt**: Python dependencies.
- **README.md**: Project documentation.
- **yolov9c.pt**: YOLOv9 model file (not included, needs to be downloaded).

## How It Works

1. The application uses the YOLOv9 model to process video frames.
2. It detects weapons and counts the number of people in the frame.
3. If the number of people exceeds a specified threshold or a weapon is detected, it sends an SMS alert using Twilio.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
