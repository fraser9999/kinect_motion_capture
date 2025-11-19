
### **README.md **

````markdown
# Kinect v1 Motion Capture Python Project

**Author:** Hermann Knopp  
**Date:** 17.06.2025  
**Python Version:** 3.10.10  
**Stage:** Early Alpha  

---

## Project Overview

This project allows **recording, visualizing, and converting motion capture data** using a **Kinect v1 depth camera** on Windows. The recorded raw data can be converted into the **BVH format**, which can be used for animations in Blender.

The project is divided into three main modules:

1. **Recording Raw Data** – `Kinect_Recorder.py`  
   Reads Kinect data, tracks the skeleton, and saves the XYZ coordinates of each joint to a text file.

2. **Visualizing & Checking Data** – `Kinect_Anim_plotter.py`  
   Loads the saved raw data and displays it as a **3D line animation** to check the quality of the captured motion.

3. **Converting to BVH** – `BVH_Writer.py`  
   Converts raw data into **Blender-compatible BVH files**, including computation of joint rotations.

---

## Requirements

### Software
- **Kinect SDK 1.8** (for Kinect V1 support)  
- **OpenNI2** (`Openni_x64.exe`)  
- **NiTE2** (`Nite2_x64.exe`)  

### Important Files
- `h.dat` and `s.dat` must be located in the **application folder** or correctly added to the system path.

### System Path
- OpenNI2 and NiTE2 should be registered in the system `PATH`.  
- Optionally, `nite2.dll` and `openni2.dll` can be copied into the Python application folder.

---

## Installation

1. Install Python 3.10.10.  
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
````

3. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Install Kinect SDK, OpenNI2, NiTE2.
5. Make sure the data files (`h.dat`, `s.dat`) are accessible.


Required Download:

"Openni_x64.exe"  
OpenNI-Windows-x64-2.2.0.33.zip (from structure.io or openni.com website)

"Nite2_x64.exe"
NiTE2-Windows-x64(x86)-2.21.zip (from openni.com website)

Kinect SDK 1.7 or 1.8
(from microsoft.com)



---

## Usage

### 1. Record Raw Data

```bash
python Kinect_Recorder.py -o output_file.txt
```

* Starts Kinect skeleton tracking.
* Saves raw joint data to a text file (`output_file.txt`).
* Press `q` to stop recording.

### 2. Visualize the Data

```bash
python Kinect_Anim_plotter.py
```

* Enter the path to the saved raw data file.
* Displays a 3D line animation of the recorded frames.

### 3. Generate BVH File

```bash
python BVH_Writer.py
```

* Enter the path to the raw data file.
* Creates a Blender-compatible `.bvh` file in the project folder.

---

## Project Structure

```
/project_root
│
├─ Kinect_Recorder.py      # Kinect raw data recording
├─ Kinect_Anim_plotter.py  # 3D visualization
├─ BVH_Writer.py           # BVH conversion
├─ requirements.txt        # Python dependencies
└─ README.md
```

---

## Python Dependencies

* `numpy`
* `opencv-python`
* `matplotlib`
* `scipy`
* `openni` (Python bindings for OpenNI2/NiTE2)

---

## Notes

* If the software does not start, check:

  * Are `h.dat` and `s.dat` in the correct folder?
  * Are `openni2.dll` and `nite2.dll` available?
  * Is the system path set correctly?

```



