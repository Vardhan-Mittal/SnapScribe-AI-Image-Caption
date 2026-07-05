# ✨ SnapScribe — AI Image Caption Generator

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-F97316?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![HuggingFace](https://img.shields.io/badge/🤗_Hugging_Face-Spaces-blue?style=for-the-badge)](https://huggingface.co/spaces)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **AI-powered image captioning** that understands your visuals. Upload any image and get intelligent, context-aware descriptions instantly.

---

## 🌟 About

**SnapScribe** is a premium AI-powered web application that generates descriptive captions for uploaded images. Built with the **BLIP (Bootstrapped Language-Image Pretraining)** model from Salesforce, it produces intelligent, context-aware captions useful for:

- 🦮 **Accessibility** — Describing images for visually impaired users
- 📷 **Content Creation** — Auto-generating social media captions
- 🔎 **SEO** — Improving image search visibility
- 🏛️ **Digital Archiving** — Cataloging image collections
- 🛍️ **E-commerce** — Auto-generating product descriptions

## 🔥 Features

| Feature | Description |
|---------|-------------|
| 📸 **Image Upload** | Drag & drop or click to upload any image (JPEG, PNG, WebP) |
| ⚡ **Dual Captions** | Get both concise and detailed captions |
| 🎯 **Guided Captioning** | Provide a prompt prefix to guide the AI |
| 📋 **Copy to Clipboard** | One-click copy for generated captions |
| 🎨 **Premium UI** | Dark glassmorphism design with smooth animations |
| 🖼️ **Sample Images** | Try the app instantly with built-in examples |
| 📱 **Responsive** | Works beautifully on desktop and mobile |

## 🛠️ Tech Stack

- **[Python](https://python.org)** — Core language
- **[BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base)** — Vision-language model by Salesforce
- **[Transformers](https://huggingface.co/transformers)** — Hugging Face model library
- **[PyTorch](https://pytorch.org)** — Deep learning framework
- **[Gradio](https://gradio.app)** — Web UI framework
- **[Pillow](https://pillow.readthedocs.io)** — Image processing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Vardhan-Mittal/SnapScribe-AI-Image-Caption.git
cd SnapScribe-AI-Image-Caption

# Install dependencies
pip install -r requirements.txt

# Run the app
python caption_app.py
```

The app will launch at `http://localhost:7860`. The BLIP model will be downloaded automatically on first run (~1GB).

## 🚀 How It Works

1. **Upload** — Drop any image into the upload area
2. **Configure** — Choose caption style (Concise, Detailed, or Both) and optionally add a prompt prefix
3. **Generate** — Click "Generate Caption" and the BLIP model analyzes your image
4. **Use** — Copy the generated captions with one click

## 📁 Project Structure

```
SnapScribe-AI-Image-Caption/
├── caption_app.py      # Main application (model + UI)
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## 📜 License

This project is open-source and available under the **MIT License**.

---

✨ Created with ❤️ by **[Vardhan Mittal](https://github.com/Vardhan-Mittal)**
