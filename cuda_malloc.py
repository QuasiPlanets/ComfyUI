#!/usr/bin/env python3
"""
CUDA Memory Allocation Utility
This file is required by main.py and must be present.
"""

import torch
import gc
import psutil
import os

def cuda_malloc_supported():
    """Check if CUDA malloc is supported"""
    return torch.cuda.is_available()

def clear_cuda_memory():
    """Clear CUDA memory and garbage collect"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    gc.collect()

def get_memory_info():
    """Get current memory usage information"""
    if torch.cuda.is_available():
        cuda_memory = torch.cuda.memory_allocated() / 1024**3  # GB
        cuda_reserved = torch.cuda.memory_reserved() / 1024**3  # GB
        return {
            'cuda_allocated': cuda_memory,
            'cuda_reserved': cuda_reserved,
            'system_ram': psutil.virtual_memory().percent
        }
    else:
        return {
            'cuda_allocated': 0,
            'cuda_reserved': 0,
            'system_ram': psutil.virtual_memory().percent
        }

def optimize_memory():
    """Optimize memory usage"""
    clear_cuda_memory()
    return get_memory_info()

if __name__ == "__main__":
    print("CUDA Memory Utility")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"CUDA Malloc Supported: {cuda_malloc_supported()}")
    if torch.cuda.is_available():
        print(f"CUDA Device: {torch.cuda.get_device_name()}")
        print(f"Memory Info: {get_memory_info()}") 