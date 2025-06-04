# model_optimization.py
import tensorflow as tf
import tensorflow_model_optimization as tfmot
import onnx
from onnxruntime.quantization import quantize_dynamic
import psutil
import gc
import logging
import os

logger = logging.getLogger(__name__)

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / 1024 / 1024
    logger.info(f"Memory usage: {memory:.2f} MB")
    
    if memory > 400:  # 400MB threshold
        logger.warning("High memory usage detected!")
        gc.collect()
    return memory

def optimize_and_quantize_model(model_path):
    """Optimize and quantize the model"""
    try:
        # 1. Convert to TFLite with quantization
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
        quantized_model = converter.convert()

        # Save quantized model
        with open('quantized_model.tflite', 'wb') as f:
            f.write(quantized_model)

        return quantized_model

    except Exception as e:
        logger.error(f"Error in model optimization: {str(e)}")
        raise

def load_model_efficiently(model_path):
    """Load model with memory optimization"""
    model = None
    try:
        model = tf.keras.models.load_model(
            model_path,
            compile=False
        )
        
        # Set memory growth
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise
        
    return model