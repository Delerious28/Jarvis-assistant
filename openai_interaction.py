import os
import openai

openai.api_key = "#OPenAI_API_KEY"

conversation_history = [
    {"role": "system", "content": "You are my assistant Named Jarvis. You are a helpfull assistant that gives short but usefull awnsers Respond to all queries in this style."}
]

def ask_openai(question, session_id=None):
    global conversation_history

    try:
        conversation_history.append({"role": "user", "content": question})

        params = {
            "model": "gpt-4o",
            "messages": conversation_history
        }

        if session_id:
            params["session_id"] = session_id

        response = openai.ChatCompletion.create(**params)

        answer = response.choices[0].message['content']
        conversation_history.append({"role": "assistant", "content": answer})

        return answer

    except Exception as e:
        return f"Error from OpenAI: {str(e)}"

