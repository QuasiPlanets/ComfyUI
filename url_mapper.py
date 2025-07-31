"""
URL Mapper for ComfyUI Media Access

This module provides utilities to map internal Docker network URLs to localhost URLs
that are accessible from the browser, supporting both images and audio files.
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
    
    def map_media_url(self, internal_url: str) -> str:
        """
        Map an internal Docker network URL to an external localhost URL.
        Works for both images and audio files.
        
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
    
    # Alias for backward compatibility
    def map_image_url(self, internal_url: str) -> str:
        """Alias for map_media_url for backward compatibility."""
        return self.map_media_url(internal_url)
    
    def map_audio_url(self, internal_url: str) -> str:
        """Map audio URLs (alias for map_media_url)."""
        return self.map_media_url(internal_url)
    
    def map_urls_in_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively map all URLs in a response dictionary.
        Works for both images and audio files.
        
        Args:
            response: The response dictionary that may contain URLs
            
        Returns:
            Updated response with mapped URLs
        """
        if isinstance(response, dict):
            mapped_response = {}
            for key, value in response.items():
                if isinstance(value, str) and self.internal_url_pattern.search(value):
                    mapped_response[key] = self.map_media_url(value)
                elif isinstance(value, (dict, list)):
                    mapped_response[key] = self.map_urls_in_response(value)
                else:
                    mapped_response[key] = value
            return mapped_response
        elif isinstance(response, list):
            return [self.map_urls_in_response(item) for item in response]
        elif isinstance(response, str) and self.internal_url_pattern.search(response):
            return self.map_media_url(response)
        else:
            return response
    
    def get_media_info_with_mapped_urls(self, prompt_id: str, comfyui_client, media_type: str = "auto") -> Dict[str, Any]:
        """
        Get media information for a prompt and map all URLs to be browser-accessible.
        Works for both images and audio files.
        
        Args:
            prompt_id: The ComfyUI prompt ID
            comfyui_client: The ComfyUI client instance
            media_type: Type of media ("image", "audio", or "auto" to detect)
            
        Returns:
            Media info with mapped URLs
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
            
            # Extract media information
            media_files = []
            for node_id, output in outputs.items():
                # Check for images
                if 'images' in output:
                    for media_info in output['images']:
                        # Construct the internal URL
                        filename = media_info.get('filename', '')
                        subfolder = media_info.get('subfolder', '')
                        type_param = media_info.get('type', 'output')
                        
                        internal_url = f"http://172.19.0.4:8188/view?filename={filename}&subfolder={subfolder}&type={type_param}"
                        external_url = self.map_media_url(internal_url)
                        
                        media_files.append({
                            'filename': filename,
                            'subfolder': subfolder,
                            'type': type_param,
                            'media_type': 'image',
                            'internal_url': internal_url,
                            'external_url': external_url,
                            'browser_url': external_url,  # This is what the browser can access
                            'direct_url': external_url,   # For compatibility
                            'url': external_url           # For compatibility
                        })
                
                # Check for audio files (ComfyUI stores audio files in separate "audio" field)
                if 'audio' in output:
                    for media_info in output['audio']:
                        filename = media_info.get('filename', '')
                        subfolder = media_info.get('subfolder', '')
                        type_param = media_info.get('type', 'output')
                        
                        internal_url = f"http://172.19.0.4:8188/view?filename={filename}&subfolder={subfolder}&type={type_param}"
                        external_url = self.map_media_url(internal_url)
                        
                        media_files.append({
                            'filename': filename,
                            'subfolder': subfolder,
                            'type': type_param,
                            'media_type': 'audio',
                            'internal_url': internal_url,
                            'external_url': external_url,
                            'browser_url': external_url,
                            'direct_url': external_url,
                            'url': external_url
                        })
                
                # Also check for audio files that might be in the images field (legacy support)
                # Audio files typically have extensions like .wav, .mp3, .flac
                if 'images' in output:
                    for media_info in output['images']:
                        filename = media_info.get('filename', '')
                        if any(filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.flac', '.ogg', '.m4a']):
                            subfolder = media_info.get('subfolder', '')
                            type_param = media_info.get('type', 'output')
                            
                            internal_url = f"http://172.19.0.4:8188/view?filename={filename}&subfolder={subfolder}&type={type_param}"
                            external_url = self.map_media_url(internal_url)
                            
                            # Only add if we haven't already added this file from the audio field
                            duplicate_found = False
                            for existing_file in media_files:
                                if existing_file['filename'] == filename and existing_file['subfolder'] == subfolder:
                                    duplicate_found = True
                                    break
                            
                            if not duplicate_found:
                                media_files.append({
                                    'filename': filename,
                                    'subfolder': subfolder,
                                    'type': type_param,
                                    'media_type': 'audio',
                                    'internal_url': internal_url,
                                    'external_url': external_url,
                                    'browser_url': external_url,
                                    'direct_url': external_url,
                                    'url': external_url
                                })
            
            # Separate by media type
            images = [f for f in media_files if f['media_type'] == 'image']
            audio_files = [f for f in media_files if f['media_type'] == 'audio']
            
            return {
                "status": "success",
                "prompt_id": prompt_id,
                "media_files": media_files,
                "images": images,
                "audio_files": audio_files,
                "total_files": len(media_files),
                "total_images": len(images),
                "total_audio": len(audio_files),
                "image_urls": [img['browser_url'] for img in images],  # For compatibility
                "audio_urls": [audio['browser_url'] for audio in audio_files],
                "media_urls": [f['browser_url'] for f in media_files],
                "urls": [f['browser_url'] for f in media_files]         # For compatibility
            }
            
        except Exception as e:
            return {"error": "Exception occurred", "details": str(e)}
    
    # Backward compatibility methods
    def get_image_info_with_mapped_urls(self, prompt_id: str, comfyui_client) -> Dict[str, Any]:
        """
        Get image information for a prompt and map all URLs to be browser-accessible.
        (Backward compatibility wrapper)
        """
        result = self.get_media_info_with_mapped_urls(prompt_id, comfyui_client, "image")
        # Remove audio-specific fields for backward compatibility
        if 'audio_files' in result:
            del result['audio_files']
        if 'audio_urls' in result:
            del result['audio_urls']
        if 'total_audio' in result:
            del result['total_audio']
        return result
    
    def get_audio_info_with_mapped_urls(self, prompt_id: str, comfyui_client) -> Dict[str, Any]:
        """
        Get audio information for a prompt and map all URLs to be browser-accessible.
        """
        result = self.get_media_info_with_mapped_urls(prompt_id, comfyui_client, "audio")
        # Focus on audio files
        if result.get('status') == 'success':
            result['files'] = result.get('audio_files', [])
            result['file_urls'] = result.get('audio_urls', [])
        return result

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

def get_browser_accessible_audio_urls(prompt_id: str, comfyui_client) -> Dict[str, Any]:
    """
    Get browser-accessible URLs for audio files generated by a prompt.
    """
    return url_mapper.get_audio_info_with_mapped_urls(prompt_id, comfyui_client)

def get_browser_accessible_media_urls(prompt_id: str, comfyui_client) -> Dict[str, Any]:
    """
    Get browser-accessible URLs for all media files (images and audio) generated by a prompt.
    """
    return url_mapper.get_media_info_with_mapped_urls(prompt_id, comfyui_client)

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
        mapped = mapper.map_media_url(url) # Changed to map_media_url
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