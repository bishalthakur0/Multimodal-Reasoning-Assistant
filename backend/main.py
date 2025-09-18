from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from PIL import Image
import io
from models.clip_model import CLIPEncoder
from models.llm_reasoning import LLMReasoningEngine
from models.agentic_safety import AgenticSafetyLayer
from data.data_storage import DataStorage
from models.evaluation import EvaluationMetrics
import time

app = FastAPI()

clip_encoder = CLIPEncoder()
llm_reasoning_engine = LLMReasoningEngine()
agentic_safety_layer = AgenticSafetyLayer()
data_storage = DataStorage()
evaluation_metrics = EvaluationMetrics()

@app.get("/")
async def root():
    return {"message": "Multimodal Reasoning Assistant Backend"}

@app.post("/encode/")
async def encode_multimodal_input(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    start_time = time.time()
    image_embedding = None
    text_embedding = None

    if image:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        image_embedding = clip_encoder.encode_image(pil_image).tolist()

    if text:
        text_embedding = clip_encoder.encode_text(text).tolist()

    raw_response = llm_reasoning_engine.generate_response(image_embedding, text_embedding)
    final_response = agentic_safety_layer.apply_safety_checks(raw_response)

    data_storage.log_query(text_query=text, image_present=bool(image), response=final_response)

    end_time = time.time()
    latency = evaluation_metrics.track_latency(start_time, end_time)

    return {"image_embedding": image_embedding, "text_embedding": text_embedding, "response": final_response, "latency": latency}