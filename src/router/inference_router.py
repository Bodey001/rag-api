from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from src.controllers.inference_controller import infer_query

router = APIRouter()

router.post("/infer", response_class=PlainTextResponse)(infer_query)
