# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0
import argparse
import subprocess
import getpass
import sys
import openai
import re
import httpx
import os


class ChatBot:
    def __init__(self, model, system="", is_verbose=False, api_key_path=None):
        self.system = system
        self.messages = []
        self.model: str = model
        self.is_verbose: bool = is_verbose

        # Precedence of ways to submit the API key:
        # 1. --api-key-path
        # 2. OPENAI_API_KEY environment variable
        # 3. ~/.openai-api-key
        if api_key_path:
            openai.api_key_path = api_key_path
            if self.is_verbose:
                print("Using API key from {}".format(api_key_path))
        elif os.getenv("OPENAI_API_KEY"):
            # Not actually setting the api key here, because OpenAI will itself
            # look for this env var
            if self.is_verbose:
                print("Using API key from OPENAI_API_KEY environment variable")
        elif api_key_path is None:
            default_key_path: str = os.path.join(
                os.path.expanduser("~"), ".openai-api-key"
            )
            if os.path.exists(default_key_path):
                with open(default_key_path) as f:
                    openai.api_key = f.read().strip()
                    if self.is_verbose:
                        print("Using API key from {}".format(default_key_path))
            else:
                raise ValueError(
                    "Please provide an API key path using --api-key-path or set the OPENAI_API_KEY environment variable."
                )

        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        message = message[:4096]
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model=self.model, messages=self.messages
        )
        if self.is_verbose:
            # eg: {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
            print(completion.usage)
        return completion.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

shell:
e.g. shell: ls ~
Performs an action in a POSIX shell using subprocess

Note that when using `shell`, you should use only non-interactive utilities (so, you cannot use vim and nano).
Also, if you run into permissions issues, then you should try again with `sudo`.

Example session:

Question: Can you list the contents of the home directory?
Thought: I should use the shell command to list the contents of the home directory
Action: shell: ls ~
PAUSE

You will be called again with this:

Observation: Directory contents: file1.txt, file2.txt, folder1

You then output:

Answer: The contents of the home directory are: file1.txt, file2.txt, folder1
""".strip()


action_re = re.compile("^Action: (\w+): (.*)$")


def query(question, model, is_verbose):
    bot = ChatBot(model=model, system=prompt, is_verbose=is_verbose)
    next_prompt = question
    while True:
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            input("Press enter to continue")
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


def wikipedia(q):
    return httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": q, "format": "json"},
    ).json()["query"]["search"][0]["snippet"]


def calculate(what):
    return eval(what)


def shell(command):
    # Check if the command requires sudo
    if command.startswith("sudo"):
        # Get the user's password
        password = getpass.getpass(prompt="Enter your sudo password: ")

        # Create a Popen object with the command and PIPEs for stdout and stderr
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            stdin=subprocess.PIPE,
        )

        # Send the password to the process followed by a newline character
        process.stdin.write(password + "\n")
        process.stdin.flush()

        # Collect the output and error streams
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return "Error: " + stderr.strip()

        return stdout.strip()
    else:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        if result.returncode != 0:
            return "Error: " + result.stderr.strip()

        return result.stdout.strip()


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "shell": shell,
}

def main(args=None):
    if args is None:
        args = parse_arguments()
    
    query(args.query, args.model, args.verbose) 
    

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run ChatGPT in a ReAct loop."
    )
    parser.add_argument(
        "-m", "--model", default="gpt-3.5-turbo", help="OpenAI API model to use"
    )
    # parser.add_argument(
    #     "--api-key-path",
    #     help="Tell me where you stored your OpenAI API key. If this isn't provided, I'll look for the OPENAPI_API_KEY env var, and failing that, ~/.openai_api_key.",
    # )
    parser.add_argument(
        "--verbose", action="store_true", help="Print extra information"
    )
    parser.add_argument(
        "query",
        type=str,
        help="The query string you want to send to ChatGPT."
    )
    args = parser.parse_args()
    return args
