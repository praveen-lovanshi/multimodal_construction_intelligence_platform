# Multimodal Construction Intelligence Platform

The Multimodal Construction Intelligence Platform is a Streamlit application for turning construction-site images and project details into practical planning and safety insights. It combines Google Gemini multimodal analysis with transparent rule-based calculations, so the application can still be demonstrated without an API key.

This project was created as a Skill Wallet capstone project.

## What the application does

### 1. Site safety and PPE review

Upload a construction-site photograph to review visible PPE and hazards. The report includes:

- Safety score and overall status
- Helmet, high-visibility vest, safety footwear, harness, glove, and eye-protection checks
- Hazards grouped by severity
- Corrective actions and referenced standards
- Downloadable JSON output

### 2. Crack and defect diagnosis

Upload a concrete or masonry defect image to receive an engineering-oriented assessment, including:

- Probable defect classification
- Estimated crack width and visual pattern
- Likely causes
- Structural-integrity risk
- Recommended repair methods and priorities
- Monitoring guidance
- Downloadable JSON output

### 3. Planning and real-estate valuation

The planning tab accepts project parameters such as structure type, built-up area, location tier, floors, parking, and completion percentage. It calculates:

- Estimated construction budget
- CapEx incurred so far
- Indicative market valuation
- Projected ROI
- Approximate steel and cement quantities
- Current construction milestone

It can also request a conceptual architectural image through Pollinations AI.

### 4. Site assistant

The assistant provides selectable weather-condition advisories for normal conditions, high wind, heavy rain, and extreme heat. It also includes a multi-turn construction chatbot for questions about concrete, reinforcement, safety standards, and site operations.

## Technology used

- Python 3.12
- Streamlit
- Google Gemini API through `google-generativeai`
- Pillow for image handling
- Requests for HTTP support
- Pollinations AI for optional conceptual renders
- Custom CSS styling

## Project layout

```text
.
├── app.py                         # Streamlit entry point and page layout
├── gemini_client.py               # Gemini wrapper and demo-mode responses
├── prompts.py                     # Image-analysis and chatbot prompts
├── styles.py                      # Custom visual theme and reusable CSS
├── requirements.txt               # Python dependencies
├── .streamlit/config.toml         # Streamlit configuration
└── README.md                      # Project documentation
```

## Setup on Windows

Python 3.12 is recommended because the application uses Pillow's compiled image-processing library.

```powershell
cd "C:\Users\Guest1\Desktop\Multimodal-Construction-Intelligence-Platform-main"

py -3.12 -m venv .venv312
.\.venv312\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit normally opens the application at:

```text
http://localhost:8501
```

If that port is already in use, Streamlit automatically selects another port, such as `8502`.

## Gemini configuration

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Start the application.
3. Enter the key in the sidebar field labelled **Google Gemini API Key**.
4. Use the safety, crack, and chatbot features with live model responses.

When no key is entered, the application runs in **Demo Mode**. Demo Mode uses built-in sample reports and responses, making it useful for testing the interface and demonstrating the workflow without exposing credentials.

Never commit an API key to GitHub. Store secrets outside the repository and keep `.env` files ignored.

## How to use the application

1. Open the application in a browser.
2. Choose one of the four tabs.
3. Upload an image where requested, or enter planning values.
4. Run the relevant analysis or calculation.
5. Review the result and download the JSON report when available.

For a first demonstration, use Demo Mode and test each tab before adding a Gemini key.

## Deploying with Streamlit Community Cloud

1. Push the repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select the repository and branch.
4. Set the main file to `app.py`.
5. Add `GEMINI_API_KEY` through the deployment secrets if live Gemini analysis is required.
6. Deploy and test all four tabs using the public URL.

## Important limitations

- Image analysis is an AI-assisted visual estimate and is not a substitute for an inspection by a qualified safety professional or structural engineer.
- Crack width, material quantities, cost rates, market values, and ROI are indicative calculations and should be replaced with project-specific data before real decisions are made.
- The weather panel currently uses manually selected conditions; it is not connected to a live weather service.
- Pollinations rendering requires network access and may be unavailable or slow.
- Gemini responses depend on the configured model, prompt quality, image quality, and API availability.
- The current application is a Streamlit monolith; it does not include a separate FastAPI backend or React frontend.

## Responsible use

Use the generated results as decision-support information only. Confirm safety findings, structural diagnoses, costs, and regulatory requirements with the appropriate qualified professionals and current local codes.
