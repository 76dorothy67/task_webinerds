import os
import argparse
from dotenv import load_dotenv
from helpers import *
from Storage import Storage
from MyChatBot import MyChatBot

if __name__ == "__main__":
    # Load api-key from .env file
    load_dotenv()

    # Command-line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--verbose', action='store_true')
    arg_parser.add_argument('-k', '--api-key', action='store')
    arg_parser.add_argument('-t', '--temperature', type=float, default=0.1)
    args = arg_parser.parse_args()

    # Setup verbosity
    verbosity(args.verbose)
    if verbose():
        print(bold('Verbosity: True'))
    else:
        print(bold('Verbosity: False'), '\n Use --verbose option to see debug information')

    # Provide OpenAI API KEY
    if 'OPENAI_API_KEY' in os.environ:
        api_key = os.environ['OPENAI_API_KEY']
        print(bold('API Key is taken from ENV'))
    else:
        if not args.api_key:
            print(red(
                "Provide OpenAI API key as environment variable 'OPENAI_API_KEY'"
                "or put it to .env file (see .env.example) or pass as --api-key argument"
            ))
            exit()
        api_key = args.api_key

    # Main app. loop
    chat = MyChatBot(api_key, Storage('program_data'), temperature=args.temperature)
    print(f'If you want to clear chat-bot memory, delete {bold("program_data")} folder')
    while True:
        try:
            user_input = input(f'{bold(chat.u_msg_begin)} {yellow("type q to exit or message to AI")}: ').strip()
        except KeyboardInterrupt:
            user_input = 'q'
        if user_input == 'q':
            print(red("Terminating program. Summaries from your dialogue is saved in 'program_data' folder..."))
            verbosity(False)
            print(blue(chat.finalize()))
            break
        elif user_input == '':
            continue
        else:
            print(blue(chat.replay_to(user_input)))
