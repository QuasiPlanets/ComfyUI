import os
import torch
import numpy as np
import folder_paths
import torchaudio
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

class ParlerTTSNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "Hello, how are you today? What is your name? I hope you're having a wonderful day.",
                    "multiline": True
                }),
                "description": ("STRING", {
                    "default": "A female speaker with a clear, natural voice speaking at a moderate pace.",
                    "multiline": True
                }),
                "model_name": (["parler-tts/parler-tts-mini-v1", "parler-tts/parler-tts-large-v1", "auto"], {
                    "default": "auto",
                    "description": "Auto: Choose best model based on GPU memory"
                }),
                "aggressive_generation": ("BOOLEAN", {
                    "default": True,
                    "description": "Use aggressive parameters to force complete generation"
                }),
                "max_tokens": ("INT", {
                    "default": 500,
                    "min": 100,
                    "max": 1000,
                    "step": 50,
                    "description": "Maximum tokens to generate (higher = longer audio)"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.6,  # Lower for more stable audio
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1
                }),
                "top_p": ("FLOAT", {
                    "default": 0.85,  # Conservative for better quality
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05
                }),
                "top_k": ("INT", {
                    "default": 30,  # Conservative for focused generation
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIOPATH",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "generate_speech"
    CATEGORY = "audio/tts"
    DESCRIPTION = "Generate complete speech using Parler-TTS with aggressive parameters"
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.use_cuda = torch.cuda.is_available()
        
        # Clear GPU memory on initialization
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def _save_audio(self, audio_data, prefix="fallback"):
        """Helper to save audio data"""
        output_dir = folder_paths.get_output_directory()
        os.makedirs(output_dir, exist_ok=True)
        import time
        timestamp = time.time()
        filename = f"{prefix}_{timestamp}.wav"
        filepath = os.path.join(output_dir, filename)
        
        torchaudio.save(
            filepath,
            torch.tensor(audio_data).unsqueeze(0),
            44100
        )
        
        print(f"Audio saved to: {filepath}")
        return filepath
    
    def generate_speech(self, text, description, model_name, aggressive_generation, max_tokens, temperature, top_p, top_k):
        try:
            # Auto-select best model based on GPU memory
            if model_name == "auto":
                if torch.cuda.is_available():
                    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                    print(f"Available GPU memory: {gpu_memory:.1f}GB")
                    
                    # Use large model if we have enough VRAM (>6GB)
                    if gpu_memory > 6.0:
                        model_name = "parler-tts/parler-tts-large-v1"
                        print(f"Auto-selected large model (GPU memory: {gpu_memory:.1f}GB)")
                    else:
                        model_name = "parler-tts/parler-tts-mini-v1"
                        print(f"Auto-selected mini model (GPU memory: {gpu_memory:.1f}GB)")
                else:
                    model_name = "parler-tts/parler-tts-mini-v1"
                    print("Auto-selected mini model (CPU only)")
            
            # Load model if not already loaded
            if self.model is None or self.tokenizer is None:
                print(f"Loading Parler-TTS model: {model_name}")
                
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    
                    # Clear GPU memory before loading
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    
                    # Load model with aggressive memory settings
                    if torch.cuda.is_available():
                        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
                            model_name,
                            torch_dtype=torch.float16,
                            low_cpu_mem_usage=True,
                            device_map=None  # Load directly to GPU
                        ).to("cuda")
                        print(f"Parler-TTS {model_name} loaded successfully on GPU")
                        self.device = "cuda"
                        self.use_cuda = True
                    else:
                        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
                            model_name,
                            torch_dtype=torch.float32,
                            low_cpu_mem_usage=True
                        ).to("cpu")
                        print(f"Parler-TTS {model_name} loaded successfully on CPU")
                        self.device = "cpu"
                        self.use_cuda = False
                        
                except Exception as e:
                    print(f"Model loading failed: {e}")
                    raise e
            
            # Tokenize inputs
            input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
            prompt_input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
            input_attention_mask = torch.ones_like(input_ids)
            
            print(f"Generating speech for: '{text}'")
            print(f"Voice description: '{description}'")
            print(f"Text length: {len(text)} characters")
            
            # Calculate aggressive token limits based on text length
            text_length = len(text)
            if aggressive_generation:
                # AGGRESSIVE: Use much higher token limits
                if text_length < 50:
                    target_tokens = max(200, text_length * 8)  # 8 tokens per char
                elif text_length < 200:
                    target_tokens = max(400, text_length * 10)  # 10 tokens per char
                else:
                    target_tokens = max(600, text_length * 12)  # 12 tokens per char
                
                # Cap at max_tokens but be aggressive
                final_tokens = min(target_tokens, max_tokens)
                print(f"[AGGRESSIVE] Target tokens: {target_tokens}, Final tokens: {final_tokens}")
            else:
                # Conservative approach
                final_tokens = min(max(100, text_length * 4), max_tokens)
                print(f"[CONSERVATIVE] Final tokens: {final_tokens}")
            
            # Generate audio with aggressive parameters
            with torch.no_grad():
                try:
                    # AGGRESSIVE GENERATION PARAMETERS
                    generation_params = {
                        "input_ids": input_ids,
                        "prompt_input_ids": prompt_input_ids,
                        "attention_mask": input_attention_mask,
                        "max_new_tokens": final_tokens,  # Much higher token limit
                        "temperature": temperature,
                        "top_p": top_p,
                        "top_k": top_k,
                        "do_sample": True,
                        "pad_token_id": self.tokenizer.eos_token_id,
                        "eos_token_id": self.tokenizer.eos_token_id,
                        "early_stopping": False,  # CRITICAL: Never stop early
                        "repetition_penalty": 1.0,  # No penalty to allow completion
                        "no_repeat_ngram_size": 1,  # Minimal restriction
                        "num_beams": 1,  # Single beam for speed
                        "use_cache": True,
                        "min_new_tokens": final_tokens // 2,  # Force minimum generation
                        "length_penalty": 0.5,  # Prefer longer sequences
                        "no_eos_token": True,  # Don't stop at EOS token
                    }
                    
                    print(f"[DEBUG] Generation parameters: {generation_params}")
                    print(f"[DEBUG] Model device: {next(self.model.parameters()).device}")
                    print(f"[DEBUG] Input device: {input_ids.device}")
                    
                    # Ensure all tensors are on the same device
                    if input_ids.device != next(self.model.parameters()).device:
                        input_ids = input_ids.to(next(self.model.parameters()).device)
                    if prompt_input_ids.device != next(self.model.parameters()).device:
                        prompt_input_ids = prompt_input_ids.to(next(self.model.parameters()).device)
                    if input_attention_mask.device != next(self.model.parameters()).device:
                        input_attention_mask = input_attention_mask.to(next(self.model.parameters()).device)
                    
                    # AGGRESSIVE MULTI-PASS GENERATION
                    print("[AGGRESSIVE] Starting streaming generation...")
                    all_audio_segments = []
                    total_samples = 0
                    target_samples = max(176400, text_length * 4000)  # At least 4 seconds, or 4000 samples per character
                    
                    # Break text into smaller chunks for streaming generation
                    text_chunks = []
                    sentences = text.split('.')
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if sentence:
                            # Break long sentences into smaller parts
                            if len(sentence) > 30:
                                words = sentence.split()
                                mid = len(words) // 2
                                text_chunks.append(' '.join(words[:mid]))
                                text_chunks.append(' '.join(words[mid:]))
                            else:
                                text_chunks.append(sentence)
                    
                    if not text_chunks:
                        text_chunks = [text]
                    
                    print(f"[AGGRESSIVE] Split text into {len(text_chunks)} chunks for streaming")
                    
                    # Generate audio for each chunk
                    for chunk_idx, chunk_text in enumerate(text_chunks):
                        print(f"[AGGRESSIVE] Generating chunk {chunk_idx + 1}/{len(text_chunks)}: '{chunk_text[:30]}...'")
                        
                        # Tokenize this chunk
                        chunk_input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
                        chunk_prompt_ids = self.tokenizer(chunk_text, return_tensors="pt").input_ids.to(self.device)
                        chunk_attention_mask = torch.ones_like(chunk_input_ids)
                        
                        # Generate with aggressive parameters for this chunk
                        chunk_params = {
                            "input_ids": chunk_input_ids,
                            "prompt_input_ids": chunk_prompt_ids,
                            "attention_mask": chunk_attention_mask,
                            "max_new_tokens": 200,  # High token limit per chunk
                            "temperature": temperature,
                            "top_p": top_p,
                            "top_k": top_k,
                            "do_sample": True,
                            "pad_token_id": self.tokenizer.eos_token_id,
                            "eos_token_id": self.tokenizer.eos_token_id,
                            "early_stopping": False,  # Never stop early
                            "repetition_penalty": 1.0,  # No penalty
                            "no_repeat_ngram_size": 1,  # Minimal restriction
                            "num_beams": 1,  # Single beam for speed
                            "use_cache": True,
                            "min_new_tokens": 100,  # Force minimum generation
                            "length_penalty": 0.5,  # Prefer longer sequences
                            "no_eos_token": True,  # Don't stop at EOS token
                        }
                        
                        try:
                            # Generate this chunk
                            chunk_generation = self.model.generate(**chunk_params)
                            chunk_audio = chunk_generation.cpu().float().numpy().squeeze()
                            
                            all_audio_segments.append(chunk_audio)
                            total_samples += len(chunk_audio)
                            
                            print(f"[AGGRESSIVE] Chunk {chunk_idx + 1} generated: {len(chunk_audio)} samples")
                            print(f"[AGGRESSIVE] Total samples so far: {total_samples} ({total_samples/44100:.1f}s)")
                            
                            # Check if we have enough audio
                            if total_samples >= target_samples:
                                print(f"[AGGRESSIVE] Target reached: {total_samples} samples ({total_samples/44100:.1f}s)")
                                break
                            
                        except Exception as chunk_error:
                            print(f"[ERROR] Chunk {chunk_idx + 1} failed: {chunk_error}")
                            break
                    
                    # Concatenate all audio segments
                    if all_audio_segments:
                        generation = np.concatenate(all_audio_segments)
                        print(f"[AGGRESSIVE] Final audio: {len(generation)} samples ({len(generation)/44100:.1f}s)")
                    else:
                        # Fallback to single generation
                        generation = self.model.generate(**generation_params)
                        generation = generation.cpu().float().numpy().squeeze()
                        print(f"[FALLBACK] Single generation: {len(generation)} samples")
                    
                except Exception as e:
                    print(f"Error in Parler-TTS generation: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    # Generate fallback audio
                    fallback_audio = np.zeros(44100, dtype=np.float32)  # 1 second of silence
                    return (self._save_audio(fallback_audio, "fallback"),)
            
            # Convert to audio (ensure it's a numpy array)
            if isinstance(generation, torch.Tensor):
                audio_arr = generation.cpu().float().numpy().squeeze()
            else:
                audio_arr = generation  # Already numpy array
            
            # Save audio file
            output_dir = folder_paths.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            import time
            timestamp = time.time()
            filename = f"parler_tts_{timestamp}.wav"
            filepath = os.path.join(output_dir, filename)
            
            # Save as WAV file
            torchaudio.save(
                filepath,
                torch.tensor(audio_arr).unsqueeze(0),
                self.model.config.sampling_rate
            )
            
            print(f"Audio saved to: {filepath}")
            print(f"Audio shape: {audio_arr.shape}")
            print(f"Sample rate: {self.model.config.sampling_rate}")
            print(f"Duration: {len(audio_arr)/44100:.1f} seconds")
            
            return (filepath,)
            
        except Exception as e:
            print(f"Error in Parler-TTS generation: {e}")
            import traceback
            traceback.print_exc()
            
            # Clean up GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Try to provide a fallback
            try:
                print("[DEBUG] Attempting fallback generation...")
                fallback_audio = np.zeros(44100, dtype=np.float32)  # 1 second of silence
                return (self._save_audio(fallback_audio, "fallback"),)
                
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                raise e

class PreViewAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"audio": ("AUDIOPATH",),}
                }

    CATEGORY = "audio/tts"
    DESCRIPTION = "Preview audio files in the ComfyUI interface"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_name = os.path.basename(audio)
        tmp_path = os.path.dirname(audio)
        audio_root = os.path.basename(tmp_path)
        return {"ui": {"audio":[audio_name,audio_root]}}

# Node registration
NODE_CLASS_MAPPINGS = {
    "ParlerTTSNode": ParlerTTSNode,
    "PreViewAudio": PreViewAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ParlerTTSNode": "Parler-TTS Generator",
    "PreViewAudio": "Preview Audio",
} 