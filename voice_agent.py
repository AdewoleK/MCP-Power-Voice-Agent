import sounddevice as sd
import scipy.io.wavfile as wavfile
import assemblyai as aai
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
import requests
import os
from TTS.api import TTS


# Configuration
ASSEMBLYAI_API_KEY = "66bf7dfc4a264729a63571ec5376ecf5"  # Replace with your AssemblyAI API key
MCP_SERVER_PORT = 8000
TTS_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"

# Initialize services
aai.settings.api_key = ASSEMBLYAI_API_KEY
llm = Ollama(model="qwen3")
tts = TTS(model_name=TTS_MODEL, progress_bar=False)

# MCP server call helper
def mcp_call(tool_name: str, params: dict, port: int) -> str:
    try:
        response = requests.post(f"http://localhost:{port}/tools/{tool_name}", json=params)
        return response.json().get("result", "Error: No result from MCP server")
    except Exception as e:
        return f"Error: {str(e)}"

# Define MCP tool (example: weather lookup)
weather_tool = Tool(
    name="GetWeather",
    func=lambda q: mcp_call("get_weather", {"city": q}, MCP_SERVER_PORT),
    description="Get current weather for a city"
)

# Initialize agent
agent = initialize_agent([weather_tool], llm, verbose=True)

# Step 1: Record audio
def record_audio(duration=10, fs=44100):
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio_file = "input.wav"
    wavfile.write(audio_file, fs, recording)
    print("Recording complete.")
    return audio_file

# Step 2: Transcribe audio to text
def transcribe_audio(audio_file):
    print("Transcribing audio...")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    text = transcript.text
    print(f"Transcribed text: {text}")
    return text

# Step 3-4: Process query with LLM and MCP tool
def process_query(query):
    print("Processing query with LLM and MCP...")
    response = agent.run(query)
    print(f"LLM response: {response}")
    return response

# Step 5-6: Convert response to speech and play
def speak_text(text):
    print("Generating speech...")
    output_path = "output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    print("Playing audio response...")
    os.system(f"afplay {output_path}")  # Use 'aplay' on Linux or adjust for your OS
    return "Spoken."

# Main workflow
def main():
    try:
        # Step 1: Record user voice input
        audio_file = record_audio()
        
        # Step 2: Transcribe to text
        query = transcribe_audio(audio_file)
        if not query:
            raise ValueError("No text transcribed from audio.")
        
        # Step 3-4: Process query and fetch data via MCP
        response = process_query(query)
        
        # Step 5-6: Convert response to speech and play
        speak_text(response)
        
        print("Workflow completed successfully.")
    except Exception as e:
        print(f"Error in workflow: {str(e)}")

if __name__ == "__main__":
    main()