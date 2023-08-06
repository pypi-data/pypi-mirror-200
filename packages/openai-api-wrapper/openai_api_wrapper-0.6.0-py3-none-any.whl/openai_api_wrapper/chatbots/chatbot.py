from rich import print

from chatgptbot import ChatGPTBot
from chatglmbot import ChatGLMBot

class ChatBot(ChatGPTBot):
    pass

def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("--llm", type=str, default="chatglm", choices=["chatgpt", "chatglm"], help="The language model to use. (chatgpt, chatglm)")
    parser.add_argument("--model_name", type=str, default=None, help="The model name to use. (default: None).") 
    parser.add_argument("--temperature", type=float, default=0.95, help="The temperature to use. (default: 0.95).")
    parser.add_argument("--top_p", type=float, default=0.7, help="The top_p to use. (default: 0.7).")
    parser.add_argument("--proxy", type=str, default=None, help="The proxy to use. (default: None). You can set the environment variable OPENAI_PROXY to set the proxy.")
    parser.add_argument("--human", type=str, default=None, help="The human's name. (default: None)")
    parser.add_argument("--assistant", type=str, default=None, help="The assistant's name. (default: None)")
    parser.add_argument("--company", type=str, default=None, help="The company's name. (default: None)")

    args, unk_args = parser.parse_known_args()

    return args, unk_args

def main():
    args, _ = get_args()
    if args.llm == 'chatglm':
        chatbot = ChatGLMBot(human=args.human, assistant=args.assistant, company=args.company, \
            model_name=args.model_name,
            temperature=args.temperature,
            top_p=args.top_p,
            )
    elif args.llm == 'chatgpt':
        chatbot = ChatGPTBot( human=args.human, assistant=args.assistant, company=args.company, \
            proxy=args.proxy,
            model_name=args.model_name,
            temperature=args.temperature,
            top_p=args.top_p,
            )
    else:
        raise ValueError(f"Unknown language model: {args.llm}")


    response = chatbot.ask("你是谁？")
    print(f"{chatbot.assistant}: " + response)
    while True:
        prompt = input(f"{chatbot.human}: ")
        response = chatbot.ask(prompt)
        print(f"{chatbot.assistant}: " + response)

if __name__ == "__main__":
    main()