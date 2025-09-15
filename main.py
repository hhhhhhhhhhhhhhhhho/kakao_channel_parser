from kakao_channel_parser import KaKaoChannelParser
from kakao_channel_parser import save_to_csv

def main():    
    cookies = """"""
    parser = KaKaoChannelParser(cookies)
    return_chat_list = parser.get_chat_messages()
    save_to_csv(return_chat_list)
    

if __name__ == "__main__":
    main()