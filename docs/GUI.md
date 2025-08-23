# Manimations

## Overview
**Manimations** is an automated video tutorial generator for programming topics. It uses Manim to create engaging, narrated videos from structured JSON scripts, supporting code explanations, quizzes, and real-world examples.

---

## Features
- **Script-driven video generation** using JSON
- **Code, quiz, and real-world sections** with voiceover
- **Animated transitions** and code highlighting
- **Automatic voiceover** using TTS
- **Shorts generator** with NASA APOD backgrounds

---

## Getting Started

### 1. Install Requirements

```sh
pip install -r requirements.txt
```

### 2. Prepare Your Script

- Write a JSON script as described in `main.py`'s docstring.
- Place it in your project directory (e.g., `test.json`).

### 3. Generate a Video

```sh
python run_mcp.py
```

- This will process your JSON and create a video using Manim.

### 4. Generate Shorts

- Place your quotes in `generated_shorts/quotes.json`.
- Run:

```sh
python shorts.py
```

- The script will fetch NASA images and create short videos.

---

## Customization

- **Edit `main.py`** to change video style or add new section types.
- **Edit `generate_voice.py`** to change TTS voice or language.

---

## Tips

- For best results, use concise explanations and quiz questions.
- You can add your own images, voices, or code styles.

---

## License

MIT License

---

*If you have questions or want to contribute, open an issue or pull request!*

---

# GUI Design Plan for Manimations

After reviewing your wrapper script and the overall project, here's my proposed GUI design:

## **Main Window Layout**

### **Top Menu Bar**
- **File**: New Script, Open Script, Save Script, Exit
- **Tools**: Generate Video, Batch Process, Generate Shorts, Cleanup Logs
- **Help**: About, Documentation, JSON Format Guide

### **Left Panel - Script Management**
- **Script Explorer**
  - Tree view showing `scripts/` folder contents
  - Icons for `.json` files (✅ processed, ⏳ pending)
  - Right-click context menu: Edit, Delete, Duplicate, Process Single

### **Center Panel - Script Editor**
- **Tabbed Interface**
  - **JSON Editor Tab**: Code editor with syntax highlighting
  - **Visual Builder Tab**: Form-based script creation
  - **Preview Tab**: Formatted preview of the tutorial structure

### **Right Panel - Controls & Status**
- **Quick Actions**
  - "Generate Single Video" button
  - "Process All Scripts" button  
  - "Generate Shorts" button
- **Progress Section**
  - Current operation status
  - Progress bar for batch operations
  - Live log output (scrollable)
- **Settings**
  - Output quality dropdown (low/medium/high)
  - Voice settings
  - NASA API key input

### **Bottom Panel - Log & Output**
- **Tabs**: Current Log, All Logs, Generated Videos
- **Generated Videos**: Thumbnail view with play buttons

## **Additional Windows**

### **Visual Script Builder**
- Drag-and-drop interface for creating tutorials
- Add sections: Code Block, Quiz, Real-world Example
- Live preview of JSON structure

### **Shorts Generator**
- Upload/select quotes JSON
- NASA API settings
- Preview thumbnails of generated shorts

### **Batch Processing Dashboard**
- Queue management
- Parallel processing options
- Error handling and retry mechanisms

## **Key Features**
1. **Real-time validation** of JSON scripts
2. **Live preview** of tutorial structure
3. **Integrated video player** for generated content
4. **Drag-and-drop** file management
5. **Progress tracking** with estimated time remaining
6. **Error highlighting** in JSON editor
7. **Template library** for common tutorial types

## **Technology Stack Suggestion**
- **Python + Tkinter** (simple, built-in)
- **Python + PyQt/PySide** (more professional)
- **Python + CustomTkinter** (modern look)
- **Web-based (Flask + HTML/CSS/JS)** (cross-platform)

## **Integration with Existing Scripts**
- Wrapper script integration for batch processing
- Real-time monitoring of `scripts/done.txt`
- Live log streaming from individual operations
- Video thumbnail generation and preview

What aspects would you like me to refine or change in this design?