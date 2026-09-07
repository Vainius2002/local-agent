from openai import OpenAI
from app.services.search import search_files
from app.services.read import read_file
from app.services.activate import start_app
from app.services.taskkill import kill_task
from app.services.find_pid import find_pid
from app.services.write import write_file
from app.config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

chat_history = []
chat_mode = False

def invoke_question(question):
    global chat_history, chat_mode


    input_items = [{"role": "user", "content": question}] #openai expects role of a user to be assigned and obv. content. this is for tools logic below



# /convo logic ===

    if question == "/convo":
        chat_mode = True
        chat_history.clear()
        input_items.clear()
        return "Entered /convo mode."

    if question == "/stop":
        chat_mode = False
        chat_history.clear()
        input_items.clear()
        return "Stopped /convo mode."

    if chat_mode:
        chat_history.extend(input_items)


        response = client.responses.create(
        model="gpt-5-mini",
        input=chat_history,
        )

        chat_history.append({"role": "assistant", "content": response.output_text})
        return response.output_text
    


# end of /convo logic ===



#if not in chat mode:
    while True:
        response = client.responses.create(
            model="gpt-5-mini",
            input=input_items,
            tools= [
        {
            "type": "function",
            "name": "search_files",
            "description": "Search the workspace for files or directories matching a filename, function, class, error message, or other text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for in file or directory names."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "type": "function",
            "name": "read_file",
            "description": "Read the contents of a specific file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read."}
                },
                "required": ["path"]
            }
        },
        {
            "type": "function",
            "name": "start_app",
            "description": "Start a FastAPI application with Uvicorn. Determine the correct Uvicorn target such as 'app.main:app' using search_files or read_file before calling this tool; do not guess it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project directory containing the application and virtual environment."},
                    "file_name": {"type": "string", "description": "Complete Uvicorn target in the format 'module_path:application_object', such as 'app.main:app'. Determine it with search_files or read_file; do not guess."},
                    "port": {"type": "string", "description": "Port to run the application on."}
                },
                "required": ["path", "file_name", "port"]
            }
        },
        {
            "type": "function",
            "name": "find_pid",
            "description": "Find the PID of the processes using the specified port.",
            "parameters": {
                "type": "object",
                "properties": {
                    "port": {"type": "string", "description": "Port whose running process PID should be found."}
                },
                "required": ["port"]
            }
        },
        {
            "type": "function",
            "name": "kill_task",
            "description": "Terminate a running process by PID. If you only know the port, use find_pid first. If multiple PIDs are returned for the port, call this tool once for each PID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pid": {"type": "string", "description": "PID of the process to terminate."}
                },
                "required": ["pid"]
            }
        },
        {
            "type": "function",
            "name": "write_file",
            "description": "Write the provided content to a file, replacing its existing contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write."},
                    "content": {"type": "string", "description": "Complete new content to write to the file."}
                },
                "required": ["path", "content"]
            }
        }
    ]
        )



        # give ai its own response return, so it remembers whats happening
        input_items.extend(response.output)


#OpenAIs API is built like so that when you pass a tools list, response.output can contain either plain text items or function_call items — the model itself decides which, based on my prompt:
#  so response.output_text gives us the text of ai; for x in response.output: if x.type == "function_call" = means it gave us sign its gonna use a func.
        # print(response.model_dump_json(indent=2))    *if i want to see response json elements*
 
        found_function_call = False

        for x in response.output:
            if x.type == "function_call":
                found_function_call = True

                args = json.loads(x.arguments) #.arguments is deliberately left as json whereas other dicts are auto converted to python understanding syntax, like x.type f.e.;

                if x.name == "search_files":
                    result = search_files(**args)
                elif x.name == "read_file":
                    result = read_file(**args)
                elif x.name == "start_app":
                    result = start_app(**args)
                elif x.name == "find_pid":
                    result = find_pid(**args)
                elif x.name == "kill_task":
                    result = kill_task(**args)
                elif x.name == "write_file":
                    result = write_file(**args)
                
                #also give ai the understanding of what it chose to do (func call or not)
                input_items.append({ #these values are required for openai to understand what it received from those functions and from whom.
                    "type": "function_call_output",
                    "call_id": x.call_id,
                    "output": str(result)
                })
            
        if not found_function_call:
            return response.output_text

    return f"I couldn't solve the problem in 30 iterations..."

