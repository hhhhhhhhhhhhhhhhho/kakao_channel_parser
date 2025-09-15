"""
최종 개선된 API 파서 - 모든 채팅방의 실제 대화 내용 수집
"""

from email import message
from os import name
import requests
import json
import time
import csv
from datetime import datetime
from typing import List, Dict, Optional

def save_to_csv(return_chat_list):
    with open('chat_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'nickname', 'message'])
        for item in return_chat_list:
            writer.writerow([item['time'], item['nickname'], item['message']])

def timeconvert(unix_time):
    return datetime.fromtimestamp(unix_time/1000)  # UTC 기준

class KaKaoChannelParser:
    
    def __init__(self, cookies: str):
        self.cookies = cookies
        self.session = requests.Session()
        self.base_url = "https://center-pf.kakao.com"
        
        # API 엔드포인트들
        self.api_endpoints = {
            'chat_list': '/api/profiles/_Ihxlbj/chats',
            'chat_messages': '/api/profiles/_Ihxlbj/chats/{chat_id}/chatlogs'
        }
        
        self._setup_session()
    
    def _setup_session(self):
        """세션 설정 및 쿠키 적용"""
        try:
            # 쿠키 파싱 및 설정
            cookie_dict = {}
            for cookie in self.cookies.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookie_dict[key] = value
            
            self.session.cookies.update(cookie_dict)
            
            # 헤더 설정
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            print("✅ 세션 설정 완료")
            
        except Exception as e:
            print(f"❌ 세션 설정 오류: {e}")
    
    def get_all_chats(self):
        """모든 채팅방 목록 조회"""
        try:
            print("📡 API로 모든 채팅방 목록 조회 중...")
            
            endpoint = f"{self.base_url}{self.api_endpoints['chat_list']}"
            print(f"  엔드포인트: {endpoint}")
            
            response = self.session.get(endpoint, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 채팅방 목록 조회 성공")
                print(f"📊 응답 데이터 크기: {len(str(data))} 문자")
                
                if 'items' in data:
                    chats = data['items']
                    print(f"📋 총 {len(chats)}개의 채팅방 발견")

                return data

            else:
                print(f"❌ API 호출 실패: {response.status_code}")

                
        except Exception as e:
            print(f"❌ 채팅방 목록 조회 오류: {e}")

    
    def get_chat_messages(self):
        chats = self.get_all_chats()['items']
        #print(chats)
        # 각 채팅방의 메시지 수집
        chat_contents = {}
        return_chat_list = []
        """채팅방 메시지 조회"""
        for i,chat in enumerate(chats):
            chat_id = chat["talk_user"]['chat_id']
            
            print(f"   {i+1}/{len(chats)}: {chat['name']} 대화방 처리 중...")

            try:
                print(f"📡 API로 채팅방 메시지 조회 중... (ID: {chat_id})")            
                endpoint = f"{self.base_url}{self.api_endpoints['chat_messages'].format(chat_id=chat_id)}/"
                print(f"  엔드포인트: {endpoint}")
                response = self.session.get(endpoint, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 채팅방 메시지 조회 성공")
                    print(f"📊 응답 데이터 크기: {len(str(data))} 문자")
                    print(f"  🔍 API 응답 구조: {list(data.keys())}")
                    if 'items' in data:
                        print(f"  📊 items 개수: {len(data['items']) if data['items'] else 0}")
                        #print(f"########## items INFO MATION #############")
                        for item in data['items']:
                            #print(f"time:{timeconvert(item['send_at'])}")
                            #print(f"nickname:{item['author']['nickname']}\nmessage:{item['message']}")
                            #print("--------------------------------")
                            return_chat_list.append({
                                'time': timeconvert(item['send_at']),
                                'nickname': item['author']['nickname'],
                                'message': item['message']
                            })
                    
                else:
                    print(f"❌ API 호출 실패: {response.status_code}")
            
            except Exception as e:
                print(f"❌ 채팅방 메시지 조회 오류: {e}")
        return return_chat_list

if __name__ == "__main__":
    
    cookies = """"""
    parser = KaKaoChannelParser(cookies)
    
    return_chat_list = parser.get_chat_messages()
    print(return_chat_list)
    save_to_csv(return_chat_list)