# kakaotalk channel chat parser

카카오톡 채널에 있는 채팅 데이터를 파싱하는 도구입니다.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

```python
main.py
def main():    
    cookies = """ INPUT YOUR COOKIES """
    parser = KaKaoChannelParser(cookies)
    return_chat_list = parser.get_chat_messages()
    save_to_csv(return_chat_list)
    

if __name__ == "__main__":
    main()

```

### Getting Cookies

1. 브라우저에서 카카오톡 채널 관리자 페이지에 로그인
2. 개발자 도구 열기 (F12)
3. Network 탭에서 페이지 새로고침
4. 첫 번째 요청을 클릭하여 Request Headers에서 Cookie 값 복사
