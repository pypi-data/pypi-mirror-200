# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0
import argparse
import subprocess
import getpass
import re
import httpx
from .chatbot import ChatBot


prompt = """
Your task is to answer questions about a system, or to take actions in a system
to achieve a human's goal. To do this, you should run in a loop of Thought, Action, PAUSE, Observation.

Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your output should be at most 1 or 2 lines long.

Your available actions are:
shell:
e.g. shell: ls ~
Performs an action in a POSIX shell using subprocess

Note that when using `shell`, you should use only non-interactive utilities (so, you cannot us
e vim and nano).
Also, if you run into permissions issues, then you should try again with `sudo`.

If one way fails, be creative and try different approaches, and be sure
to gather information you need about various systems.

Example:
Question: Can you list the contents of the home directory?
Thought: I should use the shell command to list the contents of the home directory
Action: shell: ls ~
PAUSE

You will be called again with this:

Observation: Directory contents: file1.txt, file2.txt, folder1
(continue the loop)
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
            result = bot(next_prompt)
            if is_verbose:
                print("no action to run")


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
