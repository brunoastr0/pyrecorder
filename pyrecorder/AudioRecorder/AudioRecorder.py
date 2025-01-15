import sounddevice as sd
import numpy as np

class AudioRecorder:
    def __init__(self, device_name, sample_rate=16000):
        self.device_name = device_name
        self.sample_rate = sample_rate
        self.device_index = self.find_device()

    def find_device(self):
        """
        Find the audio device index by name.
        """
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if self.device_name.lower() in device['name'].lower():
                return idx
        raise ValueError(f"Device '{self.device_name}' not found. Available devices: {[d['name'] for d in devices]}")

    def record_audio(self, duration):
        """
        Record audio for a specified duration.
        """
        print("Recording...")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,  # Mono input
            dtype="float32",
            device=self.device_index
        )
        sd.wait()  # Wait for the recording to finish
        print("Recording complete.")
        return np.squeeze(audio_data)  # Convert 2D array to 1D

    def record_audio_indefinitely(self):
        """
        Record audio indefinitely until stopped (Ctrl+C).
        """
        print("Recording... Press Ctrl+C to stop.")
        audio_chunks = []  # List to store audio chunks
        samplerate=self.sample_rate
        device_index=self.device_index
        try:
            while True:
                # Record in 5-second chunks to avoid memory overload
                chunk = sd.rec(
                    int(5 * samplerate),
                    samplerate=samplerate,
                    channels=1,  # Mono input
                    dtype="float32",
                    device=device_index
                )
                sd.wait()  # Wait for the chunk to finish
                audio_chunks.append(chunk)
        except KeyboardInterrupt:
            print("\nRecording stopped.")
        
        if audio_chunks:
            return np.concatenate(audio_chunks, axis=0)  # Combine all chunks into one array
        else:
            return None  
