🩺 RetinaVision-MNet: Eye Disease Detection System (MobileNetV2 + FastAPI + JWT + Grad-CAM)
RetinaVision-MNet is a full-stack AI system for detecting 10 retinal diseases from fundus images. The project integrates a custom-trained MobileNetV2 model, Grad-CAM explainability, a secure FastAPI backend, JWT authentication, and a responsive HTML/CSS/JS frontend. The model is trained on the Mendeley Retinal OCT & Fundus Image Dataset with 10 disease classes.

🖼 Supported Eye Diseases
CSCR (Central Serous Chorioretinopathy)
Diabetic Retinopathy
Disc Edema
Glaucoma
Healthy
Macular Scar
Myopia
Pterygium
Retinal Detachment
Retinitis Pigmentosa
🚀 Key Features
🧠 Deep Learning Model (MobileNetV2)
Custom-trained on Mendeley dataset (10 classes)
Lightweight CNN suitable for deployment
Grad-CAM integrated for visual explanations
Model saved as .h5 (TensorFlow/Keras)
🛡️ Authentication System (Secure)
Login & registration
Password hashing using bcrypt
Protected endpoints using JWT tokens
🌐 Frontend (HTML/CSS/JS)
Clean UI for login, registration, and dashboard
Image upload with prediction display
⚡ FastAPI Backend
Async API for fast predictions
Well-structured modular architecture
Prediction + explainability pipeline
🗄 PostgreSQL-Ready Backend
.env configuration
Optional logging for predictions/users
📂 Dataset — Mendeley Retinal Disease Dataset
The model is trained on the Mendeley Data Fundus Disease Dataset, containing 10 classes of retinal images.

Preprocessing Steps:
Resize to 224 × 224 × 3
Normalization
Data augmentation (rotation, zoom, brightness, flip)
Train/Validation split
📦 Download the Trained Model (MobileNetV2 .h5)
The trained RetinaVision-MNet model is hosted on Hugging Face because GitHub does not allow large model files.

🔗 Download Model (.h5): https://huggingface.co/DrakeBlaze/RetinaVision-MNet/tree/main

After downloading, place the model inside:

📌 Load the Model in FastAPI
from tensorflow.keras.models import load_model

model = load_model("model/mobile_model.h5")
🧠 Model Architecture — RetinaVision-MNet (MobileNetV2-Based)
The model is built using a custom-trained MobileNetV2 backbone optimized for retinal disease detection.

🔍 Layer Overview
Input: 224 × 224 × 3
Convolution + ReLU6
Depthwise Separable Convolutions
7× Inverted Residual Blocks
Bottleneck + Expansion
1×1 Conv layer (feature compression)
Global Average Pooling (1 × 1 × 1280)
Dropout
Dense (512 units)
Softmax Output (10 classes)
📊 Model Performance
Metric	Score
Training Accuracy	89.35%
Validation Accuracy	65.07%
Loss Function	Categorical Cross-Entropy
Optimizer	Adam
🔥 Prediction Pipeline (How It Works)
User logs in → Receives a JWT token
Uploads a retinal fundus image
Backend:
Preprocesses the image
Runs inference using MobileNetV2
Generates Grad-CAM heatmap
Response includes:
Predicted disease
Confidence
Path to Grad-CAM image
Example Response

{
  "disease": "Glaucoma",
  "confidence": 98.42,
  "gradcam_path": "/static/gradcam/gradcam_image.jpg"
}
📁 Project Structure

EyeDisease/
│── app/
│   │── __init__.py
│   │── main.py                     # FastAPI app entry point
│   │
│   ├── auth/                       # Authentication module
│   │   │── __init__.py
│   │   │── auth.py
│   │   │── utils.py
│   │   │── database.py
│   │   └── schemas.py
│   │
│   ├── ml/                         # Model + prediction logic
│   │   │── model_loader.py         # Load MobileNet model
│   │   │── gradcam.py              # Grad-CAM generation
│   │   └── predict.py              # Prediction pipeline
│   │
│   ├── frontend/                   # Frontend UI
│   │   │── index.html
│   │   │── login.html
│   │   │── register.html
│   │   └── dashboard.html
│   │
│   └── static/                     # Static files
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── uploads/                # Uploaded images + GradCAM
│
├── model/                          # Trained models
│   ├── mobile_model.h5
│   └── mobile.h5
│
├── .env
├── requirements.txt
└── README.md
Sample Image From Webiste
image alt

🔧 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/eye-disease-detection.git
cd eye-disease-detection
2️⃣ Create Virtual Environment
python -m venv venv
Activate Windows
    venv\Scripts\activate
Activate (Mac/Linux):
source venv/bin/activate
3️⃣ Install Requirements
pip install fastapi uvicorn tensorflow pillow numpy opencv-python python-multipart python-jose[cryptography] passlib[bcrypt] sqlalchemy asyncpg psycopg2-binary scikit-learn matplotlib

4️⃣ Create .env File
Add the following inside a .env file in the project root:

SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

5️⃣ Run FastAPI App
uvicorn main:app --reload
6️⃣ Open API Docs
http://127.0.0.1:8000/docs
👤 Author
vignesh varma mudunuri AI/ML Developer • CSE Student

GitHub LinkedIn
