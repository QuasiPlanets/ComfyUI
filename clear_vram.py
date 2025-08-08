#!/usr/bin/env python3
"""
VRAM Clearing Utility
This file provides VRAM management functions.
"""

import torch
import gc
import psutil
import os

def clear_vram():
    """Clear VRAM and free up GPU memory"""
    if torch.cuda.is_available():
        # Clear CUDA cache
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        
        # Force garbage collection
        gc.collect()
        
        print(f"VRAM cleared. Available: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
    else:
        print("CUDA not available, clearing system memory only")
        gc.collect()

def get_vram_info():
    """Get current VRAM usage information"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3  # GB
        reserved = torch.cuda.memory_reserved() / 1024**3  # GB
        total = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
        
        return {
            'allocated_gb': allocated,
            'reserved_gb': reserved,
            'total_gb': total,
            'free_gb': total - reserved
        }
    else:
        return {
            'allocated_gb': 0,
            'reserved_gb': 0,
            'total_gb': 0,
            'free_gb': 0
        }

def optimize_vram():
    """Optimize VRAM usage"""
    clear_vram()
    return get_vram_info()

if __name__ == "__main__":
    print("VRAM Clearing Utility")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"VRAM Info: {get_vram_info()}")
        clear_vram()
        print(f"After clearing: {get_vram_info()}") 