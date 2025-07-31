"""
Local ComfyUI Workflow Client for ElizaOS

This client allows ElizaOS to trigger local ComfyUI workflows without requiring
external API services or authentication tokens.
"""

import json
import requests
from typing import Dict, Any, Optional
from url_mapper import url_mapper, get_browser_accessible_image_urls, get_browser_accessible_audio_urls

class LocalComfyUIClient:
    def __init__(self, comfyui_url="http://localhost:8188"):
        self.comfyui_url = comfyui_url
        
        # Your default workflow template
        self.default_workflow = {
            "6": {
                "inputs": {
                    "text": "A hyperrealistic close-up of an alien being with ethereal, translucent skin and glowing, otherworldly eyes. Its face is adorned with intricate, geometric patterns that resemble ancient runes. The background is a swirling vortex of vibrant colors, reminiscent of a nebula or a cosmic storm.",
                    "clip": ["30", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Positive Prompt)"
                }
            },
            "8": {
                "inputs": {
                    "samples": ["31", 0],
                    "vae": ["30", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            },
            "27": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptySD3LatentImage",
                "_meta": {
                    "title": "EmptySD3LatentImage"
                }
            },
            "30": {
                "inputs": {
                    "ckpt_name": "flux1-dev-fp8.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "31": {
                "inputs": {
                    "seed": 4294967295,
                    "steps": 35,
                    "cfg": 1,
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "denoise": 1,
                    "model": ["30", 0],
                    "positive": ["35", 0],
                    "negative": ["33", 0],
                    "latent_image": ["27", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "33": {
                "inputs": {
                    "text": "",
                    "clip": ["30", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Negative Prompt)"
                }
            },
            "35": {
                "inputs": {
                    "guidance": 3.5,
                    "conditioning": ["6", 0]
                },
                "class_type": "FluxGuidance",
                "_meta": {
                    "title": "FluxGuidance"
                }
            }
        }
        
        # Audio workflow template for Stable Audio Open
        self.default_audio_workflow = {
            "3": {
                "inputs": {
                    "seed": 495250103929212,
                    "steps": 50,
                    "cfg": 4.98,
                    "sampler_name": "dpmpp_3m_sde_gpu",
                    "scheduler": "exponential",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["11", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "4": {
                "inputs": {
                    "ckpt_name": "stable-audio-open-1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "6": {
                "inputs": {
                    "text": "electronic dance music like grimes",
                    "clip": ["10", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "7": {
                "inputs": {
                    "text": "",
                    "clip": ["10", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "10": {
                "inputs": {
                    "clip_name": "t5-base.safetensors",
                    "type": "stable_audio",
                    "device": "default"
                },
                "class_type": "CLIPLoader",
                "_meta": {
                    "title": "Load CLIP"
                }
            },
            "11": {
                "inputs": {
                    "seconds": 47.6,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentAudio",
                "_meta": {
                    "title": "EmptyLatentAudio"
                }
            },
            "12": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecodeAudio",
                "_meta": {
                    "title": "VAEDecodeAudio"
                }
            },
            "13": {
                "inputs": {
                    "filename_prefix": "audio/ComfyUI",
                    "audioUI": "",
                    "audio": ["12", 0]
                },
                "class_type": "SaveAudio",
                "_meta": {
                    "title": "SaveAudio"
                }
            }
        }
    
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                      width: int = 1024, height: int = 1024, 
                      steps: int = 35, seed: int = -1,
                      guidance: float = 3.5) -> Dict[str, Any]:
        """
        Generate an image using the local Flux model workflow.
        
        Args:
            prompt: The positive prompt for image generation
            negative_prompt: The negative prompt (things to avoid)
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            steps: Number of sampling steps (default: 35)
            seed: Random seed (-1 for random)
            guidance: Guidance scale (default: 3.5)
        
        Returns:
            Dict containing the result status and prompt_id
        """
        # Create a copy of the workflow to modify
        workflow = json.loads(json.dumps(self.default_workflow))
        
        # Update the workflow with the provided parameters
        workflow["6"]["inputs"]["text"] = prompt
        workflow["33"]["inputs"]["text"] = negative_prompt
        workflow["27"]["inputs"]["width"] = width
        workflow["27"]["inputs"]["height"] = height
        workflow["31"]["inputs"]["steps"] = steps
        workflow["31"]["inputs"]["seed"] = seed if seed != -1 else 4294967295
        workflow["35"]["inputs"]["guidance"] = guidance
        
        # Update filename prefix to include prompt info
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        workflow["9"]["inputs"]["filename_prefix"] = f"ElizaOS_{safe_prompt}"
        
        result = self._queue_workflow(workflow, "Local Image Generation")
        
        # If successful, add image URL information
        if result.get('status') == 'success' and 'prompt_id' in result:
            result['image_urls'] = f"Check generated images at: http://localhost:8188/view?filename=ElizaOS_{safe_prompt}_*.png&type=output"
            result['note'] = "Images will be available after generation completes"
        
        return result
    
    def generate_image_with_custom_workflow(self, workflow: Dict[str, Any], 
                                          workflow_name: str = "Custom Workflow") -> Dict[str, Any]:
        """
        Generate an image using a custom workflow.
        
        Args:
            workflow: The complete workflow dictionary
            workflow_name: Name for logging purposes
        
        Returns:
            Dict containing the result status and prompt_id
        """
        return self._queue_workflow(workflow, workflow_name)
    
    def generate_audio(self, prompt: str, negative_prompt: str = "", 
                      duration: float = 47.6, steps: int = 50, 
                      seed: int = -1, cfg: float = 4.98,
                      sampler_name: str = "dpmpp_3m_sde_gpu",
                      scheduler: str = "exponential") -> Dict[str, Any]:
        """
        Generate audio using the Stable Audio Open model workflow.
        
        Args:
            prompt: The positive prompt for audio generation
            negative_prompt: The negative prompt (things to avoid)
            duration: Audio duration in seconds (default: 47.6)
            steps: Number of sampling steps (default: 50)
            seed: Random seed (-1 for random)
            cfg: CFG scale (default: 4.98)
            sampler_name: Sampler to use (default: "dpmpp_3m_sde_gpu")
            scheduler: Scheduler to use (default: "exponential")
        
        Returns:
            Dict containing the result status and prompt_id
        """
        # Create a copy of the workflow to modify
        workflow = json.loads(json.dumps(self.default_audio_workflow))
        
        # Update the workflow with the provided parameters
        workflow["6"]["inputs"]["text"] = prompt
        workflow["7"]["inputs"]["text"] = negative_prompt
        workflow["11"]["inputs"]["seconds"] = duration
        workflow["3"]["inputs"]["steps"] = steps
        workflow["3"]["inputs"]["seed"] = seed if seed != -1 else 495250103929212
        workflow["3"]["inputs"]["cfg"] = cfg
        workflow["3"]["inputs"]["sampler_name"] = sampler_name
        workflow["3"]["inputs"]["scheduler"] = scheduler
        
        # Update filename prefix to include prompt info
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        workflow["13"]["inputs"]["filename_prefix"] = f"audio/ElizaOS_{safe_prompt}"
        
        result = self._queue_workflow(workflow, "Local Audio Generation")
        
        # If successful, add audio URL information
        if result.get('status') == 'success' and 'prompt_id' in result:
            result['audio_urls'] = f"Check generated audio at: http://localhost:8188/view?filename=ElizaOS_{safe_prompt}_*.wav&type=output"
            result['note'] = "Audio will be available after generation completes"
        
        return result
    
    def generate_audio_with_custom_workflow(self, workflow: Dict[str, Any], 
                                          workflow_name: str = "Custom Audio Workflow") -> Dict[str, Any]:
        """
        Generate audio using a custom workflow.
        
        Args:
            workflow: The complete workflow dictionary
            workflow_name: Name for logging purposes
        
        Returns:
            Dict containing the result status and prompt_id
        """
        return self._queue_workflow(workflow, workflow_name)
    
    def _queue_workflow(self, workflow: Dict[str, Any], workflow_type: str) -> Dict[str, Any]:
        """
        Queue a workflow for execution.
        """
        payload = {
            "prompt": workflow
        }
        
        try:
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "status": "success",
                "workflow_type": workflow_type,
                "prompt_id": result.get('prompt_id'),
                "message": f"{workflow_type} workflow queued successfully"
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to queue {workflow_type} workflow: {str(e)}"}
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Gets the current queue status.
        """
        try:
            response = requests.get(f"{self.comfyui_url}/queue")
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get queue status: {str(e)}"}
    
    def get_history(self, prompt_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gets the execution history.
        """
        try:
            url = f"{self.comfyui_url}/history"
            if prompt_id:
                url += f"/{prompt_id}"
            
            response = requests.get(url)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get history: {str(e)}"}
    
    def get_image_urls_for_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """
        Get browser-accessible image URLs for a completed prompt.
        
        Args:
            prompt_id: The ComfyUI prompt ID
            
        Returns:
            Dict with image URLs mapped to localhost
        """
        return get_browser_accessible_image_urls(prompt_id, self)
    
    def get_audio_urls_for_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """
        Get browser-accessible audio URLs for a completed prompt.
        
        Args:
            prompt_id: The ComfyUI prompt ID
            
        Returns:
            Dict with audio URLs mapped to localhost
        """
        return get_browser_accessible_audio_urls(prompt_id, self)
    
    def check_comfyui_status(self) -> Dict[str, Any]:
        """
        Checks if ComfyUI is running and accessible.
        """
        try:
            response = requests.get(f"{self.comfyui_url}/queue", timeout=5)
            response.raise_for_status()
            return {
                "status": "success",
                "message": "ComfyUI is running and accessible",
                "comfyui_url": self.comfyui_url
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"ComfyUI is not accessible: {str(e)}",
                "comfyui_url": self.comfyui_url
            }

# Global instance for ElizaOS to use
local_comfyui = LocalComfyUIClient()

# Convenience functions for the LLM to call
def generate_image_with_flux(prompt: str, **kwargs):
    """Generate an image using the Flux model."""
    return local_comfyui.generate_image(prompt, **kwargs)

def get_comfyui_queue():
    """Get the current ComfyUI queue status."""
    return local_comfyui.get_queue_status()

def get_comfyui_history(prompt_id: Optional[str] = None):
    """Get ComfyUI execution history."""
    return local_comfyui.get_history(prompt_id)

def check_comfyui_status():
    """Check if ComfyUI is running."""
    return local_comfyui.check_comfyui_status()

def get_image_urls(prompt_id: str):
    """Get browser-accessible image URLs for a prompt."""
    return local_comfyui.get_image_urls_for_prompt(prompt_id)

# Audio convenience functions
def generate_audio_with_stable_audio(prompt: str, **kwargs):
    """Generate audio using the Stable Audio Open model."""
    return local_comfyui.generate_audio(prompt, **kwargs)

def get_audio_urls(prompt_id: str):
    """Get browser-accessible audio URLs for a prompt."""
    return local_comfyui.get_audio_urls_for_prompt(prompt_id)  # Audio uses same URL structure

# Example usage for testing
if __name__ == "__main__":
    print("Local ComfyUI Workflow Client")
    print("=" * 40)
    
    # Check if ComfyUI is running
    status = check_comfyui_status()
    print(f"ComfyUI Status: {status['status']}")
    print(f"Message: {status['message']}")
    
    if status['status'] == 'success':
        # Test image generation
        print("\n🎨 Testing image generation...")
        result = generate_image_with_flux(
            prompt="A beautiful sunset over mountains, cinematic lighting, hyperrealistic",
            negative_prompt="blurry, low quality, distorted",
            width=1024,
            height=1024
        )
        print(f"Image Result: {json.dumps(result, indent=2)}")
        
        # Test audio generation
        print("\n🎵 Testing audio generation...")
        audio_result = generate_audio_with_stable_audio(
            prompt="electronic dance music like grimes, upbeat tempo, dreamy synths",
            negative_prompt="distorted, low quality, silence",
            duration=30.0,
            steps=40
        )
        print(f"Audio Result: {json.dumps(audio_result, indent=2)}")
        
        # Check queue status
        print("\n📊 Current queue status:")
        queue_status = get_comfyui_queue()
        if queue_status['status'] == 'success':
            print(json.dumps(queue_status['data'], indent=2))
        else:
            print(f"Error: {queue_status['error']}")
    else:
        print("\n❌ ComfyUI is not running. Please start ComfyUI first:")
        print("   ./start_comfyui_api.sh")
        print("   or")
        print("   python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header") 