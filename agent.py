import autogen
from mcp import BlenderMCPInterface, config_list, llm_config

class BlenderModelingAgent(autogen.AssistantAgent):
    """3D建模专家Agent"""
    
    def __init__(self, name="BlenderModeler"):
        system_message = """
        你是一个3D建模专家，擅长使用Blender进行建模操作。
        你的职责包括：
        1. 创建和修改3D几何体
        2. 应用材质和纹理
        3. 设置模型的基础属性
        4. 优化网格结构
        
        当收到建模任务时，你需要：
        - 分析需求并规划建模步骤
        - 调用相应的Blender命令
        - 确保模型质量和性能
        
        你可以使用以下Blender操作：
        - bpy.ops.mesh.primitive_cube_add()
        - bpy.ops.mesh.primitive_sphere_add()
        - bpy.ops.mesh.extrude_region_move()
        - bpy.ops.transform.resize()
        等等...
        """
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config
        )
        self.mcp_interface = BlenderMCPInterface()

class BlenderAnimatorAgent(autogen.AssistantAgent):
    """动画制作专家Agent"""
    
    def __init__(self, name="BlenderAnimator"):
        system_message = """
        你是一个动画制作专家，专门负责Blender中的动画相关任务。
        你的职责包括：
        1. 设置关键帧动画
        2. 创建路径动画
        3. 设置约束和控制器
        4. 管理时间轴和动画序列
        
        你需要理解动画原理，包括：
        - 缓入缓出
        - 时间节奏
        - 物理运动规律
        - 角色表演
        """
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config
        )
        self.mcp_interface = BlenderMCPInterface()

class BlenderRenderAgent(autogen.AssistantAgent):
    """渲染专家Agent"""
    
    def __init__(self, name="BlenderRenderer"):
        system_message = """
        你是一个渲染专家，负责Blender的渲染管道配置和优化。
        你的职责包括：
        1. 设置渲染引擎参数
        2. 配置灯光和环境
        3. 优化渲染性能
        4. 管理输出格式和质量
        
        你熟悉各种渲染引擎：
        - Cycles渲染器
        - Eevee实时渲染
        - Workbench渲染器
        """
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config
        )
        self.mcp_interface = BlenderMCPInterface()