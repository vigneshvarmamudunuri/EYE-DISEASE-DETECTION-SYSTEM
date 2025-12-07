# main.py (patched)
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import cv2
import os
import traceback


from backend_auth.auth import router as auth_router, get_current_user
from backend_auth.database import init_db

app = FastAPI(title="EyePredict - AI Eye Disease Detection with GradCAM")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
MODEL_PATH = os.path.join(BASE_DIR, "model", "mobile_model.h5")


os.makedirs(os.path.join(STATIC_DIR, "uploads"), exist_ok=True)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


model = None

CLASS_NAMES = [
    "CSCR_Color Fundus", "Diabetic Retinopathy", "Disc Edema", "Glaucoma",
    "Healthy", "Macular Scar", "Myopia", "Pterygium",
    "Retinal Detachment", "Retinitis Pigmentosa"
]

DISEASE_DESCRIPTIONS = {
    "CSCR_Color Fundus": "Fluid accumulation under the retina causes blurred or distorted vision.",
    "Diabetic Retinopathy": "Retinal blood vessels are damaged by prolonged diabetes, leading to vision loss.",
    "Disc Edema": "Swelling of the optic disc due to increased intracranial pressure.",
    "Glaucoma": "Optic nerve damage caused by increased intraocular pressure; can lead to blindness.",
    "Healthy": "No abnormalities detected — retina appears normal and healthy.",
    "Macular Scar": "Scarring in the central retina that reduces clarity and sharpness of vision.",
    "Myopia": "Nearsightedness where distant objects appear blurry due to improper focusing.",
    "Pterygium": "A non-cancerous growth of tissue on the eye that can cause redness or irritation.",
    "Retinal Detachment": "Retina separates from the back of the eye — a vision-threatening emergency.",
    "Retinitis Pigmentosa": "Inherited disorder that causes progressive vision loss and night blindness."
}

def preprocess_img(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    arr = image.img_to_array(img) / 255.0
    return np.expand_dims(arr, axis=0)

def make_gradcam_heatmap(img_array, model, last_conv_layer_name=None, pred_index=None):
    if last_conv_layer_name is None:
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer_name = layer.name
                break

    grad_model = Model([model.inputs],
                       [model.get_layer(last_conv_layer_name).output, model.output])

    with tf.GradientTape() as tape:
        conv_out, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        loss = preds[:, pred_index]

    grads = tape.gradient(loss, conv_out)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_out[0]
    heatmap = conv_out @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = np.maximum(heatmap, 0)
    if np.max(heatmap) != 0:
        heatmap /= np.max(heatmap)
    return heatmap

def save_gradcam_overlay(img_path, heatmap, alpha=0.4):
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img, 0.6, heatmap, alpha, 0)
    root, _ = os.path.splitext(img_path)
    gradcam_path = f"{root}_gradcam.jpg"
    cv2.imwrite(gradcam_path, overlay)
    return gradcam_path

@app.post("/predict")
async def predict(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    """
    Protected predict endpoint: requires valid JWT. current_user provided by dependency.
    """
    global model
    if model is None:
        # model not loaded yet or failed earlier
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Model not available. Try again later.")

    upload_dir = os.path.join(STATIC_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    # Save uploaded image
    with open(file_path, "wb") as f:
        f.write(await file.read())

   
    img_array = preprocess_img(file_path)
    preds = model.predict(img_array)
    pred_index = int(np.argmax(preds))
    pred_class = CLASS_NAMES[pred_index]
    confidence = float(preds[0][pred_index])

    
    heatmap = make_gradcam_heatmap(img_array, model)
    gradcam_path = save_gradcam_overlay(file_path, heatmap)

    gradcam_filename = os.path.basename(gradcam_path)
    gradcam_url = f"/static/uploads/{gradcam_filename}"

    desc = DISEASE_DESCRIPTIONS.get(pred_class, "Retinal anomaly detected. Further medical examination recommended.")

    return {
        "disease": pred_class,
        "confidence": round(confidence * 100, 2),
        "description": desc,
        "gradcam_path": gradcam_url,
        "user": {"email": current_user.email}
    }

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/login.html", response_class=FileResponse)
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/register.html", response_class=FileResponse)
def serve_register():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))

@app.get("/dashboard.html", response_class=FileResponse)
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

@app.on_event("startup")
async def on_startup():
    # DB init (keeps as before)
    await init_db()

    
    try:
        print("🚀 Starting EyePredict app")
        print(f"BASE_DIR = {BASE_DIR}")
        print(f"STATIC_DIR = {STATIC_DIR}")
        print(f"FRONTEND_DIR = {FRONTEND_DIR}")
        print("static exists:", os.path.exists(STATIC_DIR))
        print("frontend exists:", os.path.exists(FRONTEND_DIR))
        print("auth.js exists:", os.path.exists(os.path.join(STATIC_DIR, "js", "auth.js")))
        print("uploads exists:", os.path.exists(os.path.join(STATIC_DIR, "uploads")))
    except Exception:
        print("Error printing debug info:", traceback.format_exc())

    
    global model
    try:
        model = load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    except Exception as e:
        model = None
        print(f"❌ Failed to load model at startup: {e}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
