import autogen

class BlenderProjectManager(autogen.UserProxyAgent):
    """项目管理和协调Agent"""
    
    def __init__(self, name="ProjectManager"):
        super().__init__(
            name=name,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config=False,
            system_message="""
            你是项目管理者，负责协调各个专业Agent完成Blender项目。
            你需要：
            1. 分析用户需求
            2. 制定工作计划
            3. 分配任务给专业Agent
            4. 监控进度和质量
            5. 整合最终结果
            """
        )

class BlenderAgentOrchestrator:
    """Agent编排器"""
    
    def __init__(self):
        self.project_manager = BlenderProjectManager()
        self.modeler = BlenderModelingAgent()
        self.animator = BlenderAnimatorAgent()
        self.renderer = BlenderRenderAgent()
        
        # 创建群聊
        self.group_chat = autogen.GroupChat(
            agents=[
                self.project_manager,
                self.modeler, 
                self.animator,
                self.renderer
            ],
            messages=[],
            max_round=20,
            speaker_selection_method="auto"
        )
        
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=llm_config
        )
    
    async def execute_project(self, user_request: str):
        """执行Blender项目"""
        print(f"开始执行项目: {user_request}")
        
        # 启动群聊协作
        response = await self.project_manager.a_initiate_chat(
            self.manager,
            message=f"用户需求: {user_request}\n\n请分析需求并制定执行计划。"
        )
        
        return response