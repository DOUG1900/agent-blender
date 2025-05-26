# autogen_blender_agents.py
import autogen
import asyncio
import websockets
import json
from typing import Dict, List, Any
import openai

class BlenderMCPInterface:
    """Blender MCP协议接口"""
    
    def __init__(self, server_uri: str = "ws://localhost:8765"):
        self.server_uri = server_uri
        self.websocket = None
    
    async def connect(self):
        """连接到Blender MCP服务器"""
        try:
            self.websocket = await websockets.connect(self.server_uri)
            print("已连接到Blender MCP服务器")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    async def execute_command(self, method: str, params: Dict = None) -> Dict:
        """执行Blender命令"""
        if not self.websocket:
            await self.connect()
        
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }
        
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def close(self):
        """关闭连接"""
        if self.websocket:
            await self.websocket.close()

# AutoGen配置
config_list = [
    {
        "model": "gpt-4-turbo-preview",
        "api_key": "your-openai-api-key"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
}