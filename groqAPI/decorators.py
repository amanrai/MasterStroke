from functools import wraps
import json

def logLMInfo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        chat_completion = func(*args, **kwargs)
        extracted_info = {
            "id": chat_completion.id,
            "created": chat_completion.created,
            "model": chat_completion.model,
            "completion_time": chat_completion.usage.completion_time,
            "completion_tokens": chat_completion.usage.completion_tokens,
            "prompt_time": chat_completion.usage.prompt_time,
            "prompt_tokens": chat_completion.usage.prompt_tokens,
            "queue_time": chat_completion.usage.queue_time,
            "total_time": chat_completion.usage.total_time,
            "total_tokens": chat_completion.usage.total_tokens
        }
        #print the extracted info in a dark gray color
        print("\033[90m", json.dumps(extracted_info, indent=4), "\033[0m")
        return chat_completion

    return wrapper