import requests
import json
import uuid
from typing import Dict, List, Optional
from app.config import settings
from app.models import ChatMessage

class HyperCLOVAService:
    def __init__(self):
        self.api_key = settings.hyperclova_api_key
        self.base_url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
        }
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 256,
        temperature: float = 0.5
    ) -> Dict:
        payload = {
            "messages": messages,
            "topP": 0.8,
            "topK": 0,
            "maxTokens": max_tokens,
            "temperature": temperature,
            "repeatPenalty": 1.1,
            "stop": [],
            "seed": 0,
            "includeAiFilters": True
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            return self._parse_streaming_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API 요청 실패: {str(e)}"}
    
    def _parse_streaming_response(self, response) -> Dict:
        full_content = ""
        
        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        if data == '[DONE]':
                            break
                        
                        try:
                            json_data = json.loads(data)
                            if 'message' in json_data and 'content' in json_data['message']:
                                full_content += json_data['message']['content']
                        except json.JSONDecodeError:
                            continue
            
            return {
                "success": True,
                "content": full_content,
                "tokens_used": len(full_content.split())  # 간단한 토큰 추정
            }
            
        except Exception as e:
            return {"success": False, "error": f"응답 파싱 실패: {str(e)}"}
