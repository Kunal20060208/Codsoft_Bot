import onnxruntime as ort
import numpy as np
import cv2
import os
import urllib.request

class ArcFaceRecognizer:
    def __init__(self, model_path="models/arcface.onnx"):
        self.model_path = model_path
        self._ensure_model_exists()
        self.session = self._load_model()
        self.input_name = self.session.get_inputs()[0].name

    def _ensure_model_exists(self):
        """Download model if not found locally to avoid deployment/storage issues."""
        if not os.path.exists(self.model_path):
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            print("[Downloading] ArcFace model...")

            try:
                url = "https://huggingface.co/onnx/models/resolve/main/arcface.onnx"
                urllib.request.urlretrieve(url, self.model_path)
                print("[Downloaded] ArcFace model successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to download ArcFace model: {e}")

    def _load_model(self):
        try:
            session = ort.InferenceSession(self.model_path)
            return session
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def preprocess(self, face_img):
        """Resize and normalize the face image."""
        if face_img.shape[0] == 0 or face_img.shape[1] == 0:
            raise ValueError("Invalid face image for preprocessing.")
        resized = cv2.resize(face_img, (112, 112))
        normalized = (resized / 127.5 - 1.0).astype(np.float32)
        transposed = np.transpose(normalized, (2, 0, 1))
        return np.expand_dims(transposed, axis=0)

    def get_embedding(self, face_img):
        """Generate the 512-D ArcFace embedding."""
        blob = self.preprocess(face_img)
        embedding = self.session.run(None, {self.input_name: blob})[0]
        return embedding[0]

    def cosine_similarity(self, emb1, emb2):
        """Compute cosine similarity between two embeddings."""
        emb1 = emb1 / np.linalg.norm(emb1)
        emb2 = emb2 / np.linalg.norm(emb2)
        return float(np.dot(emb1, emb2))
