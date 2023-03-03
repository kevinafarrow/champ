#!/usr/bin/env python3


import config
import openai
import output
from datetime import datetime


def get_cost(tokens):
    # returns cost in cents.
    return (.002/10) * tokens

def show_help():
    help_message = """
    welcome to champ, your personal openai assistant. here's your options:

        help        show these options
        history     show the conversation so far
        exit|quit   quit the interactive session

    """
    print(help_message)


def main():

    # initialize openai

    openai.api_key = config.API_KEY
    max_tokens = 4096

    # initialize messages

    messages = [
        {
        "role": "system",
        "content": f"You are champ, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: 2021. Current date: {datetime.now():%d %B %Y}."
            }
            ]

    # initialize total cost:

    conversation_cost = 0
    
    # chat loop

    user_input = ''

    show_help()

    while True:

        # user input block

        user_input = input('>>> ')

        # options

        if (user_input) == 'help':
            show_help()
            continue
        if (user_input == 'quit') or (user_input == 'exit'):
            break
        if user_input == 'history':
            output.message(messages)
            continue

        # processing block

        messages.append({"role": "user", "content": user_input})

        start = datetime.now()
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        except openai.error.InvalidRequestError as e:
            print(f"<<< Something went wrong: {e}")
        end = datetime.now()

        response_message = response['choices'][0]['message']['content']
        messages.append(response['choices'][0]['message'])

        # metrics block

        response_time = end - start
        question_tokens = response['usage']['total_tokens']
        percent_max_tokens = question_tokens / max_tokens
        question_cost = get_cost(question_tokens)
        conversation_cost += question_cost

        # display block

        print(f"<<< {response_message}")
        print()
        print(f"    response time: {response_time}")
        print(f"    question tokens: {question_tokens} ({percent_max_tokens:%}% of the {max_tokens} token limit)")
        print(f"    question cost: {question_cost:.4f} cents")
        print(f"    total cost of conversation: {conversation_cost:.4f} cents")
        print()

    return 0


if __name__ == '__main__':
    main()