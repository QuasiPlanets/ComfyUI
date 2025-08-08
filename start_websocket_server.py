#!/usr/bin/env python3
"""
WebSocket Server for Real-time Audio Transcription
This file is referenced by elizaos_management.sh and must be present.
"""

import asyncio
import websockets
import json
import numpy as np
import whisperx
import torch
import threading
import time
from typing import Dict, Any

class WebSocketTranscriptionServer:
    def __init__(self, host="0.0.0.0", port=8189):
        self.host = host
        self.port = port
        self.clients = set()
        self.audio_buffer = []
        self.buffer_duration = 3.0  # seconds
        self.sample_rate = 16000
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if torch.cuda.is_available() else "int8"
        
    async def start_server(self):
        """Start the WebSocket server"""
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        async with websockets.serve(self._handle_client, self.host, self.port):
            await asyncio.Future()  # run forever
            
    async def _handle_client(self, websocket, path):
        """Handle individual client connections"""
        print("Client connected")
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self._process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.clients.discard(websocket)
            
    async def _process_message(self, websocket, message):
        """Process incoming messages from clients"""
        try:
            data = json.loads(message)
            if "audio" in data:
                await self._handle_audio_chunk(data["audio"])
        except json.JSONDecodeError:
            print("Invalid JSON message received")
        except Exception as e:
            print(f"Error processing message: {e}")
            
    async def _handle_audio_chunk(self, audio_data):
        """Handle incoming audio chunks"""
        try:
            # Convert audio data to numpy array
            audio_array = np.array(audio_data, dtype=np.float32)
            self.audio_buffer.append(audio_array)
            
            # Check if we have enough audio to process
            total_duration = len(self.audio_buffer) * (len(audio_array) / self.sample_rate)
            
            if total_duration >= self.buffer_duration:
                await self._process_audio_buffer()
                
        except Exception as e:
            print(f"Error handling audio chunk: {e}")
            
    async def _process_audio_buffer(self):
        """Process the accumulated audio buffer"""
        if not self.audio_buffer:
            return
            
        try:
            # Concatenate audio chunks
            audio = np.concatenate(self.audio_buffer)
            
            # Load model if not loaded
            if self.model is None:
                print("Loading WhisperX model...")
                self.model = whisperx.load_model("base", self.device, compute_type=self.compute_type)
                
            # Transcribe audio
            result = self.model.transcribe(audio)
            
            if result and result["segments"]:
                transcription = result["segments"][0]["text"].strip()
                if transcription:
                    await self._broadcast_transcription(transcription)
                    
            # Clear buffer
            self.audio_buffer = []
            
        except Exception as e:
            print(f"Error processing audio buffer: {e}")
            
    async def _broadcast_transcription(self, transcription):
        """Broadcast transcription to all connected clients"""
        message = json.dumps({
            "type": "transcription",
            "text": transcription,
            "timestamp": time.time()
        })
        
        # Send to all connected clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
                
        # Remove disconnected clients
        self.clients -= disconnected_clients

def main():
    """Main function to start the WebSocket server"""
    server = WebSocketTranscriptionServer()
    print("Starting WebSocket transcription server...")
    asyncio.run(server.start_server())

if __name__ == "__main__":
    main() 