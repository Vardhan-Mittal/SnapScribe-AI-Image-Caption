"""
SnapScribe — AI Image Caption Generator
A premium Gradio app using BLIP for AI-powered image captioning.
"""

from PIL import Image
import gradio as gr
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


# ─────────────────────────────────────────────
#  Core Captioning Engine
# ─────────────────────────────────────────────
class ImageCaption:
    """Handles BLIP model loading and caption generation."""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "Salesforce/blip-image-captioning-base"
        print(f"⚡ Loading BLIP model on {self.device}...")
        self.processor = BlipProcessor.from_pretrained(self.model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_name).to(
            self.device
        )
        self.model.eval()
        print("✅ Model loaded successfully!")

    def generate_caption(self, img, prompt="", style="Detailed"):
        """
        Generate a caption for the given image.

        Args:
            img: PIL Image or file path
            prompt: Optional text prefix for conditional/guided captioning
            style: 'Concise' or 'Detailed'
        Returns:
            Tuple of (caption_text, status_message)
        """
        if img is None:
            return "", "⚠️ Please upload an image first."

        try:
            # Handle file path input
            if isinstance(img, str):
                img = Image.open(img)

            img = img.convert("RGB")

            # Build inputs based on whether we have a prompt
            if prompt and prompt.strip():
                inputs = self.processor(
                    images=img,
                    text=prompt.strip(),
                    return_tensors="pt",
                ).to(self.device)
            else:
                inputs = self.processor(
                    images=img,
                    return_tensors="pt",
                ).to(self.device)

            # Adjust generation params based on style
            gen_kwargs = {
                "max_new_tokens": 50 if style == "Concise" else 120,
                "num_beams": 3 if style == "Concise" else 5,
                "repetition_penalty": 1.5,
            }

            with torch.no_grad():
                output = self.model.generate(**inputs, **gen_kwargs)

            caption = self.processor.decode(output[0], skip_special_tokens=True)

            # Clean up the caption
            caption = caption.strip()
            if caption and not caption[0].isupper():
                caption = caption[0].upper() + caption[1:]
            if caption and caption[-1] not in ".!?":
                caption += "."

            return caption, "✅ Caption generated successfully!"

        except FileNotFoundError:
            return "", "❌ Error: Image file not found."
        except Exception as e:
            return "", f"❌ Error generating caption: {str(e)}"

    def generate_both(self, img, prompt=""):
        """Generate both concise and detailed captions."""
        if img is None:
            return "", "", "⚠️ Please upload an image first."

        concise, status1 = self.generate_caption(img, prompt, "Concise")
        if "❌" in status1:
            return "", "", status1

        detailed, status2 = self.generate_caption(img, prompt, "Detailed")
        if "❌" in status2:
            return concise, "", status1

        return concise, detailed, "✅ Both captions generated!"


# ─────────────────────────────────────────────
#  Premium Custom CSS
# ─────────────────────────────────────────────
CUSTOM_CSS = """
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0a1a;
    --bg-secondary: #12122a;
    --glass-bg: rgba(255, 255, 255, 0.04);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-hover: rgba(255, 255, 255, 0.08);
    --accent-1: #6c5ce7;
    --accent-2: #00cec9;
    --accent-3: #fd79a8;
    --text-primary: #f0f0ff;
    --text-secondary: rgba(240, 240, 255, 0.6);
    --text-muted: rgba(240, 240, 255, 0.35);
    --success: #00b894;
    --warning: #fdcb6e;
    --error: #d63031;
    --radius: 16px;
    --radius-sm: 10px;
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* ── Global Reset ── */
body, .gradio-container {
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 0 1rem !important;
}

/* ── Animated Background ── */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(108, 92, 231, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 206, 201, 0.10) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(253, 121, 168, 0.08) 0%, transparent 50%);
    animation: bgShift 15s ease-in-out infinite alternate;
    z-index: -1;
    pointer-events: none;
}

@keyframes bgShift {
    0%   { opacity: 0.7; transform: scale(1); }
    50%  { opacity: 1;   transform: scale(1.05); }
    100% { opacity: 0.8; transform: scale(1); }
}

/* ── Hero / Title ── */
#hero-title {
    text-align: center;
    padding: 2.5rem 0 0.5rem;
}

#hero-title h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #6c5ce7, #00cec9, #fd79a8, #6c5ce7);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGradient 6s ease-in-out infinite;
    margin: 0 !important;
    line-height: 1.2 !important;
}

@keyframes titleGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

#hero-subtitle {
    text-align: center;
    padding: 0 0 1.5rem;
}

#hero-subtitle p {
    color: var(--text-secondary) !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    max-width: 600px;
    margin: 0 auto !important;
    line-height: 1.6 !important;
}

/* ── Badge Row ── */
#badge-row {
    text-align: center;
    padding: 0.5rem 0 2rem;
}

#badge-row span {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    margin: 0.25rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Glass Panel ── */
.glass-panel, .gr-group {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    box-shadow: var(--shadow) !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease !important;
}

.glass-panel:hover, .gr-group:hover {
    border-color: rgba(108, 92, 231, 0.3) !important;
    box-shadow: 0 8px 32px rgba(108, 92, 231, 0.1), var(--shadow) !important;
}

/* ── Section Titles ── */
.section-title h3 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 0 0.25rem !important;
    letter-spacing: -0.2px;
}

.section-subtitle p {
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    margin: 0 !important;
}

/* ── Image Upload Area ── */
.gr-image, .gr-image .upload-container {
    border-radius: var(--radius-sm) !important;
    border: 2px dashed rgba(108, 92, 231, 0.3) !important;
    background: rgba(108, 92, 231, 0.03) !important;
    transition: all 0.3s ease !important;
    min-height: 280px !important;
}

.gr-image:hover, .gr-image .upload-container:hover {
    border-color: rgba(108, 92, 231, 0.6) !important;
    background: rgba(108, 92, 231, 0.06) !important;
}

/* ── Input Fields ── */
.gr-textbox textarea, .gr-textbox input, input, textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.3s ease !important;
}

.gr-textbox textarea:focus, .gr-textbox input:focus, input:focus, textarea:focus {
    border-color: var(--accent-1) !important;
    box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.15) !important;
    outline: none !important;
}

/* ── Primary Button ── */
.gr-button-primary, button.primary {
    background: linear-gradient(135deg, var(--accent-1), #8b5cf6) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3) !important;
    text-transform: none !important;
    letter-spacing: 0.3px !important;
    position: relative;
    overflow: hidden;
}

.gr-button-primary:hover, button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(108, 92, 231, 0.45) !important;
    background: linear-gradient(135deg, #7c6cf7, #9b7cf7) !important;
}

.gr-button-primary:active, button.primary:active {
    transform: translateY(0) !important;
}

/* ── Secondary Button ── */
.gr-button-secondary, button.secondary {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.gr-button-secondary:hover, button.secondary:hover {
    background: var(--glass-hover) !important;
    border-color: rgba(108, 92, 231, 0.3) !important;
    color: var(--text-primary) !important;
}

/* ── Output Textboxes ── */
#concise-output textarea, #detailed-output textarea {
    background: rgba(108, 92, 231, 0.05) !important;
    border: 1px solid rgba(108, 92, 231, 0.15) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
}

/* ── Status Bar ── */
#status-bar textarea {
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    text-align: center !important;
    padding: 0.5rem !important;
}

/* ── Radio & Checkbox ── */
.gr-radio label, .gr-checkbox label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}

.gr-radio input:checked + span {
    color: var(--accent-1) !important;
}

/* ── Labels ── */
label, .gr-textbox label, .gr-image label span {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Accordion ── */
.gr-accordion {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
}

.gr-accordion summary {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--glass-border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Footer ── */
#footer-text {
    text-align: center;
    padding: 2rem 0 1rem;
}

#footer-text p {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
}

#footer-text a {
    color: var(--accent-1) !important;
    text-decoration: none !important;
}

/* ── How-It-Works Cards ── */
.step-card {
    padding: 0 !important;
}

.step-card p {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    #hero-title h1 {
        font-size: 2rem !important;
    }

    #hero-subtitle p {
        font-size: 0.95rem !important;
    }

    .gradio-container {
        padding: 0 0.5rem !important;
    }

    .glass-panel {
        padding: 1rem !important;
    }
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: rgba(108, 92, 231, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(108, 92, 231, 0.5);
}

/* ── Hide Gradio Footer ── */
footer {
    display: none !important;
}

/* ── Smooth Transitions on Everything ── */
* {
    transition-property: background-color, border-color, box-shadow, transform, opacity;
    transition-duration: 0.2s;
    transition-timing-function: ease;
}
"""


# ─────────────────────────────────────────────
#  Build the Gradio App
# ─────────────────────────────────────────────
def create_app():
    """Build and return the premium Gradio interface."""

    # Initialize model
    captioner = ImageCaption()

    # Event handlers
    def on_generate(img, prompt, style):
        if style == "Both":
            concise, detailed, status = captioner.generate_both(img, prompt)
            return concise, detailed, status
        else:
            caption, status = captioner.generate_caption(img, prompt, style)
            if style == "Concise":
                return caption, "", status
            else:
                return "", caption, status

    def on_clear():
        return None, "", "", "", ""

    # Build UI
    with gr.Blocks(
        css=CUSTOM_CSS,
        title="SnapScribe — AI Image Caption Generator",
        theme=gr.themes.Base(),
    ) as app:

        # ── Hero Section ──
        gr.Markdown(
            "# ✨ SnapScribe",
            elem_id="hero-title",
        )
        gr.Markdown(
            "AI-powered image captioning that understands your visuals. "
            "Upload any image and get intelligent, context-aware descriptions instantly.",
            elem_id="hero-subtitle",
        )
        gr.HTML(
            """
            <div id="badge-row">
                <span style="background: rgba(108,92,231,0.15); color: #a78bfa;">⚡ BLIP Model</span>
                <span style="background: rgba(0,206,201,0.15); color: #00cec9;">🤗 Hugging Face</span>
                <span style="background: rgba(253,121,168,0.15); color: #fd79a8;">🎨 Gradio UI</span>
                <span style="background: rgba(0,184,148,0.15); color: #00b894;">🔒 Privacy-First</span>
            </div>
            """
        )

        # ── Main Content ──
        with gr.Row(equal_height=False):

            # Left Column — Upload & Settings
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 📸 Upload Image", elem_classes="section-title")
                    gr.Markdown(
                        "Drop an image or click to browse",
                        elem_classes="section-subtitle",
                    )
                    img_input = gr.Image(
                        type="pil",
                        label="Image",
                        show_label=False,
                        height=300,
                    )

                with gr.Group():
                    gr.Markdown("### ⚙️ Options", elem_classes="section-title")

                    with gr.Accordion("Guided Captioning (Optional)", open=False):
                        prompt_input = gr.Textbox(
                            label="Prompt Prefix",
                            placeholder="e.g., 'A photo of' or 'This image shows'",
                            lines=1,
                            info="Guide the AI by providing a starting phrase",
                        )

                    style_radio = gr.Radio(
                        choices=["Concise", "Detailed", "Both"],
                        value="Both",
                        label="Caption Style",
                        info="Choose the level of detail",
                    )

                    with gr.Row():
                        generate_btn = gr.Button(
                            "✨ Generate Caption",
                            variant="primary",
                            size="lg",
                        )
                        clear_btn = gr.Button(
                            "🗑️ Clear",
                            variant="secondary",
                            size="lg",
                        )

            # Right Column — Results
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 📝 Results", elem_classes="section-title")
                    gr.Markdown(
                        "Your AI-generated captions will appear here",
                        elem_classes="section-subtitle",
                    )

                    concise_output = gr.Textbox(
                        label="⚡ Concise Caption",
                        lines=2,
                        interactive=False,
                        elem_id="concise-output",
                        show_copy_button=True,
                    )

                    detailed_output = gr.Textbox(
                        label="📖 Detailed Caption",
                        lines=4,
                        interactive=False,
                        elem_id="detailed-output",
                        show_copy_button=True,
                    )

                    status_output = gr.Textbox(
                        label="",
                        lines=1,
                        interactive=False,
                        elem_id="status-bar",
                        show_label=False,
                    )

        # ── How It Works ──
        gr.Markdown("---")
        gr.Markdown("### 🚀 How It Works", elem_classes="section-title")

        with gr.Row():
            with gr.Column(scale=1, elem_classes="step-card"):
                gr.Markdown(
                    "**① Upload**\n\n"
                    "Drop any image — photos, screenshots, artwork, diagrams. "
                    "Supports JPEG, PNG, WebP, and more."
                )
            with gr.Column(scale=1, elem_classes="step-card"):
                gr.Markdown(
                    "**② Analyze**\n\n"
                    "The BLIP vision-language model processes your image, "
                    "understanding objects, scenes, actions, and context."
                )
            with gr.Column(scale=1, elem_classes="step-card"):
                gr.Markdown(
                    "**③ Caption**\n\n"
                    "Get intelligent captions in concise or detailed style. "
                    "Use guided mode for custom context."
                )

        # ── Sample Images ──
        gr.Markdown("---")
        gr.Markdown("### 🖼️ Try with Sample Images", elem_classes="section-title")

        gr.Examples(
            examples=[
                [
                    "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=400",
                    "",
                    "Both",
                ],
                [
                    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
                    "",
                    "Both",
                ],
                [
                    "https://images.unsplash.com/photo-1474511320723-9a56873571b7?w=400",
                    "A scenic view of",
                    "Detailed",
                ],
            ],
            inputs=[img_input, prompt_input, style_radio],
            label="",
        )

        # ── Footer ──
        gr.Markdown(
            "Built with ❤️ by **Vardhan Mittal** · Powered by "
            "[BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) · "
            "[GitHub](https://github.com/Vardhan-Mittal/SnapScribe-AI-Image-Caption)",
            elem_id="footer-text",
        )

        # ── Event Bindings ──
        generate_btn.click(
            fn=on_generate,
            inputs=[img_input, prompt_input, style_radio],
            outputs=[concise_output, detailed_output, status_output],
        )

        clear_btn.click(
            fn=on_clear,
            inputs=[],
            outputs=[img_input, prompt_input, concise_output, detailed_output, status_output],
        )

    return app


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    app.launch(share=False)
