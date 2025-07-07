from fastapi import APIRouter, HTTPException, Request
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image
import logging
from typing import Dict, Any
import json
import os

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("")
async def process_image(data: ImageData, request: Request) -> Dict[str, Any]:
    logger.info(f"Received request from {request.client.host}")
    """
    Process an image containing mathematical expressions and return calculated results.
    
    Args:
        data: ImageData containing:
            - image: Base64 encoded image string
            - dict_of_vars: Dictionary of variables for calculation
            
    Returns:
        Dictionary with:
        - message: Status message
        - data: List of calculation results
        - status: 'success' or 'error'
    """
    try:
        # Validate image format
        if not data.image.startswith('data:image/'):
            logger.error("Invalid image format")
            raise HTTPException(
                status_code=400,
                detail="Image must be in data:image/<format>;base64,<data> format"
            )

        # Decode base64 image
        try:
            _, encoded = data.image.split(",", 1)
            image_data = base64.b64decode(encoded)
        except (ValueError, IndexError, base64.binascii.Error) as e:
            logger.error(f"Image decoding failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid image data"
            ) from e

        # Open and validate image
        try:
            image = Image.open(BytesIO(image_data))
            if image.format not in ['JPEG', 'PNG', 'WEBP']:
                raise ValueError(f"Unsupported format: {image.format}")
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted image"
            ) from e

        # Process image (remove await if analyze_image is synchronous)
        try:
            # Check if analyze_image is async or sync
            responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
            
            # If it's actually async (uncomment if needed):
            # responses = await analyze_image(image, dict_of_vars=data.dict_of_vars)
            
            if isinstance(responses, dict) and 'error' in responses:
                logger.error(f"Image analysis error: {responses['error']}")
                raise HTTPException(status_code=500, detail=responses['error'])
            
            if not responses:
                logger.warning("Empty response from image analysis")
                responses = []

            # Validate and format responses
            processed_data = []
            for item in responses:
                if isinstance(item, dict):
                    processed_data.append(item)
                else:
                    try:
                        processed_data.append(json.loads(str(item)))
                    except json.JSONDecodeError:
                        processed_data.append({"raw": str(item)})

            logger.info(f"Processed response: {processed_data}")
            return {
                "message": "Success",
                "data": processed_data,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to analyze image"
            ) from e

    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) from e

@router.get("/health")
async def health_check():
    return {"status": "ok"}
