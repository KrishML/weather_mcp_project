import os
import warnings

# Suppress transformers and tokenizers warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

import subprocess
import json
import time

from transformers.pipelines import pipeline


def call_mcp_tool(location):
    message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_current_weather",
            "arguments": {"location": location}
        }
    }
    proc = subprocess.Popen(
        ["python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(1)
    response = None
    try:
        if proc.stdin and proc.stdout:
            proc.stdin.write(json.dumps(message) + "\n")
            proc.stdin.flush()
            response = proc.stdout.readline()
        else:
            response = "Error: Subprocess pipes are not available. Please run this script in a standard terminal."
    except Exception as e:
        response = f"Error communicating with MCP server: {e}"
    finally:
        proc.terminate()
    return response

if __name__ == "__main__":
    MODEL = "sshleifer/tiny-gpt2"  # Use a tiny model for fast local inference

    generator = pipeline("text-generation", model=MODEL)

    user_location = input("Enter a city or location: ")
    user_question = f"What is the weather in {user_location}?"

    try:
        result = generator(user_question, max_length=60, num_return_sequences=1)
        if result and isinstance(result, list) and "generated_text" in result[0]:
            llm_content = result[0]["generated_text"]
        else:
            llm_content = str(result)
    except Exception as e:
        import traceback
        print("Error details from local transformers pipeline:")
        traceback.print_exc()
        llm_content = f"Error calling local transformers pipeline: {e}"

    print("LLM:", llm_content)

    weather_result = call_mcp_tool(user_location)
    print("Weather Agent Response:", weather_result)
