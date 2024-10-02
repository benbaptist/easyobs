# EasyOBS

EasyOBS is a Python package that provides a simple interface to interact with the OBS (Open Broadcaster Software) remote protocol. It aims to streamline the process of controlling OBS from Python scripts.

## Features
- Access current scenes and their properties.
- Control video settings.
- Take screenshots of scenes.

## Installation
To install EasyOBS, you can use pip:

```bash
pip install -r requirements.txt
```

## Usage
Here is a basic example of how to use EasyOBS:

```python
from easyobs import EasyOBS

# Create an instance of EasyOBS
obs = EasyOBS(host="localhost", port=4455, password="your_password")

# Check connection
if obs.connected:
    print("Connected to OBS.")

    # Get the current program scene
    current_scene = obs.program_scene
    print(f"Current Scene: {current_scene}")
else:
    print("Failed to connect to OBS.")
```

## Contributing
If you'd like to contribute to EasyOBS, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.