#!/usr/bin/env python3


import config
import openai
from datetime import datetime


def get_cost(tokens):
    # returns cost in cents.
    return (.002/10) * tokens


def main():

    # initialize openai

    openai.api_key = config.API_KEY

    # initialize messages

    messages = [
        {
        "role": "system",
        "content": f"You are champ, a large language model trained by OpenAI. Answer as concisely as possible. \
            Knowledge cutoff: 2021. Current date: {datetime.now():%d %B %Y}."
            }
            ]

    # initialize total cost:

    conversation_cost = 0
    
    # chat loop

    user_input = ''

    while True:

        # user input block

        user_input = input('>>> ')
        if (user_input == 'quit') or (user_input == 'exit'):
            break

        # processing block

        messages.append({"role": "user", "content": user_input})

        start = datetime.now()
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        end = datetime.now()

        # aggregation block

        response_time = end - start
        question_cost = get_cost(response['usage']['total_tokens'])
        conversation_cost += question_cost

        # display block

        print(f"<<< {response['choices'][0]['message']['content']}")
        print()
        print(f"response time: {response_time}")
        print(f"total tokens: {response['usage']['total_tokens']}")
        print(f"cost of this interaction: {question_cost:.4f} cents")
        print(f"total cost of conversation: {conversation_cost:.4f} cents")

    return 0


if __name__ == '__main__':
    main()