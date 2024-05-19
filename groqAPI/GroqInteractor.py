from groq import Groq
import os
import json
os.environ["GROQ_API_KEY"] = "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"
from decorators import *

class GroqInteractor:
    def __init__(self, api_key = ""):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    @logLMInfo
    def _getGroqResponse(self, model="llama3-70b-8192", json_mode = True, message_list = [], temperature=0.9, tools=[]):
        assert temperature >=0 and temperature < 2
        _args = {
            "messages":message_list,
            "temperature":temperature,
            "model":model,
        }
        if json_mode == True:
            if (len(tools) == 0):
                _messages = "\n".join([item["content"] for item in message_list])
                assert "json" in _messages.lower(), "The message list should contain the word 'json' for json mode"
                _args["response_format"] = {"type":"json_object"}
        
        if (len(tools) > 0):
            _args["tools"] = tools
            _args["tool_choice"] = "auto"

        completion = self.client.chat.completions.create(
            **_args
        )
        
        return completion