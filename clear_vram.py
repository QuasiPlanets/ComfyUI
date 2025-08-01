#!/usr/bin/env python3
"""
GPU VRAM Clearing Script for ComfyUI
Multiple methods to clear GPU memory
"""

import gc
import sys
import subprocess
import os

def check_gpu_info():
    """Check GPU information and memory usage"""
    try:
        import torch
        if torch.cuda.is_available():
            print("🔍 GPU Information:")
            print(f"   CUDA Available: {torch.cuda.is_available()}")
            print(f"   Device Count: {torch.cuda.device_count()}")
            print(f"   Current Device: {torch.cuda.current_device()}")
            print(f"   Device Name: {torch.cuda.get_device_name()}")
            print(f"   Memory Allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
            print(f"   Memory Reserved: {torch.cuda.memory_reserved() / 1024**3:.2f} GB")
            print(f"   Max Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
            return True
        else:
            print("❌ CUDA not available")
            return False
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def clear_vram_method1():
    """Method 1: Basic garbage collection"""
    print("\n🧹 Method 1: Basic Garbage Collection")
    try:
        import torch
        if torch.cuda.is_available():
            # Clear PyTorch cache
            torch.cuda.empty_cache()
            print("   ✅ PyTorch cache cleared")
        else:
            print("   ❌ CUDA not available")
    except ImportError:
        print("   ❌ PyTorch not installed")
    
    # Python garbage collection
    collected = gc.collect()
    print(f"   ✅ Python garbage collection: {collected} objects collected")

def clear_vram_method2():
    """Method 2: Aggressive memory clearing"""
    print("\n🧹 Method 2: Aggressive Memory Clearing")
    try:
        import torch
        if torch.cuda.is_available():
            # Clear all PyTorch caches
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
            # Force garbage collection multiple times
            for i in range(3):
                gc.collect()
            
            print("   ✅ Aggressive cache clearing completed")
        else:
            print("   ❌ CUDA not available")
    except ImportError:
        print("   ❌ PyTorch not installed")

def clear_vram_method3():
    """Method 3: Reset CUDA device"""
    print("\n🧹 Method 3: Reset CUDA Device")
    try:
        import torch
        if torch.cuda.is_available():
            # Reset the current CUDA device
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
            print("   ✅ CUDA device reset completed")
        else:
            print("   ❌ CUDA not available")
    except ImportError:
        print("   ❌ PyTorch not installed")

def clear_vram_method4():
    """Method 4: Kill ComfyUI processes and restart"""
    print("\n🧹 Method 4: Process Management")
    
    # Find ComfyUI processes
    try:
        result = subprocess.run(['pgrep', '-f', 'main.py'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"   📋 Found {len(pids)} ComfyUI processes")
            
            # Ask for confirmation
            response = input("   ❓ Do you want to kill ComfyUI processes? (y/N): ")
            if response.lower() == 'y':
                for pid in pids:
                    try:
                        subprocess.run(['kill', '-9', pid])
                        print(f"   ✅ Killed process {pid}")
                    except:
                        print(f"   ❌ Failed to kill process {pid}")
            else:
                print("   ⏭️  Skipped process killing")
        else:
            print("   ℹ️  No ComfyUI processes found")
    except Exception as e:
        print(f"   ❌ Error checking processes: {e}")

def main():
    """Main function to clear VRAM"""
    print("🚀 ComfyUI GPU VRAM Clearing Tool")
    print("=" * 40)
    
    # Check GPU info first
    gpu_available = check_gpu_info()
    
    if not gpu_available:
        print("\n⚠️  GPU not available or PyTorch not installed")
        print("   Try installing PyTorch: pip install torch torchvision torchaudio")
        return
    
    # Show memory usage before clearing
    print("\n📊 Memory Usage Before Clearing:")
    check_gpu_info()
    
    # Run all clearing methods
    clear_vram_method1()
    clear_vram_method2()
    clear_vram_method3()
    clear_vram_method4()
    
    # Show memory usage after clearing
    print("\n📊 Memory Usage After Clearing:")
    check_gpu_info()
    
    print("\n✅ VRAM clearing completed!")
    print("\n💡 Tips:")
    print("   - Use --lowvram flag when starting ComfyUI")
    print("   - Use --novram flag for minimal VRAM usage")
    print("   - Restart ComfyUI server for complete memory reset")

if __name__ == "__main__":
    main() 