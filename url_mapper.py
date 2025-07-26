"""
URL Mapper for ComfyUI Image Access

This module provides utilities to map internal Docker network URLs to localhost URLs
that are accessible from the browser.
"""

import re
import json
from typing import Dict, Any, Optional

class ComfyUIURLMapper:
    def __init__(self, external_host="localhost", external_port=8188):
        """
        Initialize the URL mapper.
        
        Args:
            external_host: The external host (usually 'localhost')
            external_port: The external port that forwards to ComfyUI
        """
        self.external_host = external_host
        self.external_port = external_port
        
        # Pattern to match ComfyUI internal network URLs
        self.internal_url_pattern = re.compile(
            r'http://(?:172\.\d+\.\d+\.\d+|comfyui|[\w\-]+):8188/view\?'
        )
    
    def map_image_url(self, internal_url: str) -> str:
        """
        Map an internal Docker network URL to an external localhost URL.
        
        Args:
            internal_url: The internal URL (e.g., http://172.19.0.4:8188/view?filename=...)
            
        Returns:
            External URL accessible from browser (e.g., http://localhost:8188/view?filename=...)
        """
        if not internal_url:
            return internal_url
        
        # Replace internal network address with external host:port
        external_url = self.internal_url_pattern.sub(
            f'http://{self.external_host}:{self.external_port}/view?',
            internal_url
        )
        
        return external_url
    
    def map_urls_in_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively map all URLs in a response dictionary.
        
        Args:
            response: The response dictionary that may contain URLs
            
        Returns:
            Updated response with mapped URLs
        """
        if isinstance(response, dict):
            mapped_response = {}
            for key, value in response.items():
                if isinstance(value, str) and self.internal_url_pattern.search(value):
                    mapped_response[key] = self.map_image_url(value)
                elif isinstance(value, (dict, list)):
                    mapped_response[key] = self.map_urls_in_response(value)
                else:
                    mapped_response[key] = value
            return mapped_response
        elif isinstance(response, list):
            return [self.map_urls_in_response(item) for item in response]
        elif isinstance(response, str) and self.internal_url_pattern.search(response):
            return self.map_image_url(response)
        else:
            return response
    
    def get_image_info_with_mapped_urls(self, prompt_id: str, comfyui_client) -> Dict[str, Any]:
        """
        Get image information for a prompt and map all URLs to be browser-accessible.
        
        Args:
            prompt_id: The ComfyUI prompt ID
            comfyui_client: The ComfyUI client instance
            
        Returns:
            Image info with mapped URLs
        """
        try:
            # Get history for this prompt
            history_response = comfyui_client.get_history(prompt_id)
            
            if history_response.get('status') != 'success':
                return {"error": "Failed to get history", "details": history_response}
            
            history_data = history_response.get('data', {})
            
            if prompt_id not in history_data:
                return {"error": "Prompt not found in history", "prompt_id": prompt_id}
            
            prompt_history = history_data[prompt_id]
            outputs = prompt_history.get('outputs', {})
            
            # Extract image information
            images = []
            for node_id, output in outputs.items():
                if 'images' in output:
                    for image_info in output['images']:
                        # Construct the internal URL
                        filename = image_info.get('filename', '')
                        subfolder = image_info.get('subfolder', '')
                        type_param = image_info.get('type', 'output')
                        
                        internal_url = f"http://172.19.0.4:8188/view?filename={filename}&subfolder={subfolder}&type={type_param}"
                        external_url = self.map_image_url(internal_url)
                        
                        images.append({
                            'filename': filename,
                            'subfolder': subfolder,
                            'type': type_param,
                            'internal_url': internal_url,
                            'external_url': external_url,
                            'browser_url': external_url,  # This is what the browser can access
                            'direct_url': external_url,   # For compatibility
                            'url': external_url           # For compatibility
                        })
            
            return {
                "status": "success",
                "prompt_id": prompt_id,
                "images": images,
                "total_images": len(images),
                "image_urls": [img['browser_url'] for img in images],  # For compatibility
                "urls": [img['browser_url'] for img in images]         # For compatibility
            }
            
        except Exception as e:
            return {"error": "Exception occurred", "details": str(e)}

# Global instance
url_mapper = ComfyUIURLMapper()

def map_comfyui_urls(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to map URLs in any ComfyUI response.
    """
    return url_mapper.map_urls_in_response(response)

def get_browser_accessible_image_urls(prompt_id: str, comfyui_client) -> Dict[str, Any]:
    """
    Get browser-accessible URLs for images generated by a prompt.
    """
    return url_mapper.get_image_info_with_mapped_urls(prompt_id, comfyui_client)

# Example usage
if __name__ == "__main__":
    # Test URL mapping
    mapper = ComfyUIURLMapper()
    
    test_urls = [
        "http://172.19.0.4:8188/view?filename=ElizaOS_00023_.png&subfolder=&type=output",
        "http://172.20.0.5:8188/view?filename=test.png&subfolder=folder&type=output",
        "http://comfyui:8188/view?filename=another.png&subfolder=&type=output"
    ]
    
    print("URL Mapping Test:")
    print("=" * 50)
    
    for url in test_urls:
        mapped = mapper.map_image_url(url)
        print(f"Internal:  {url}")
        print(f"External:  {mapped}")
        print("-" * 50)
    
    # Test response mapping
    test_response = {
        "status": "success",
        "images": [
            {
                "url": "http://172.19.0.4:8188/view?filename=test.png&subfolder=&type=output",
                "filename": "test.png"
            }
        ]
    }
    
    mapped_response = mapper.map_urls_in_response(test_response)
    print(f"Original response: {json.dumps(test_response, indent=2)}")
    print(f"Mapped response: {json.dumps(mapped_response, indent=2)}") 