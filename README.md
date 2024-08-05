## How to Compile

### Step 1: Install Requirements

First, install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```
###  Step 2: Install dlib

Second, install the specific version of `dlib` using the provided wheel file (`dlib-19.22.99-cp39-cp39-win_amd64.whl`):
```bash
pip install dlib-19.22.99-cp39-cp39-win_amd64.whl
```

### Step 3: Compile to Executable

Finally, compile the Python script (`Login.py`) into a standalone executable. Run the following command:

```bash
python -m PyInstaller .\Login.py -w -F --collect-all face_recognition_models --icon logo.ico
```

