import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(transcript):
    prompt = f"""
You are an expert meeting analyst. Your task is to analyze the provided meeting transcript and extract key insights, summarize the discussions, and identify actionable tasks.

CRITICAL: Do not just repeat or transcribe the input. You must distill the information into key points and actionable items. Focus on extracting the actual meaning and outcomes of the conversation.

You must return a valid JSON object ONLY. Do not include any markdown formatting (like ```json), no explanations, and no text outside the JSON object.

The JSON object must have exactly these keys:
1. 'summary': A concise distillation of the meeting's key discussions, decisions, and insights. It should be 2-4 paragraphs long. You may use markdown formatting (like bolding or bullet points) within the text to highlight key insights.
2. 'action_items': An array of objects representing specific tasks identified during the meeting. Each object must have:
   - 'task': A clear, actionable description of what needs to be done.
   - 'assigned_to': The name of the person responsible. If no owner is mentioned, set it to 'Unassigned'.
   - 'deadline': The deadline for the task. If no deadline is mentioned, set it to null (actual JSON null, not a string).

Transcript:
{transcript}
"""
    
    backend = os.getenv("LLM_BACKEND", "ollama").lower()
    
    if backend == "ollama":
        return call_ollama(prompt)
    elif backend == "openrouter":
        return call_openrouter(prompt)
    else:
        raise ValueError("Unsupported LLM Backend")

def call_ollama(prompt):
    model = os.getenv("OLLAMA_MODEL", "llama3")
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return json.loads(data.get("response", "{}"))
    except Exception as e:
        print(f"Ollama Error: {e}")
        return {"summary": "Error generating summary.", "action_items": []}

def call_openrouter(prompt):
    key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    model = "qwen/qwen-2.5-coder-32b-instruct"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if "choices" not in data:
            print(f"OpenRouter Error Response: {data}")
            error_msg = data.get("error", {}).get("message", "Unknown OpenRouter API error")
            return {"summary": f"Error: {error_msg}", "action_items": []}

        text = data["choices"][0]["message"]["content"].strip()
        
        # Clean up potential markdown formatting from the response
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            text = match.group(1)
        else:
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                text = match.group(1)
                
        # Fix common JSON error where model leaves trailing empty values (e.g., "deadline": \n })
        text = re.sub(r':\s*(?=[,}])', ': null', text)
            
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e} - Response Text: {text}")
        return {"summary": "Error: LLM did not return valid JSON.", "action_items": []}
    except Exception as e:
        print(f"OpenRouter Exception: {e}")
        return {"summary": f"Error communicating with OpenRouter: {e}", "action_items": []}