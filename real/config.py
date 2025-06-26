"""
MCP 서버 설정 파일
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# MCP 서버 설정
MCP_SERVERS = {
    "exa": {
        "command": "cmd",
        "args": [
            "/c",
            "npx",
            "-y",
            "@smithery/cli@latest",
            "run",
            "exa",
            "--key",
            "d52a2502-98a5-452f-9ce7-65f507929073"
        ],
        "transport": "stdio"
    }
}

# API 키 설정 (환경변수에서 가져오거나 직접 설정)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here") 