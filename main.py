import asyncio
import json
from dataclasses import dataclass
from typing import List

from autogen import config_list_from_json
from autogen_core import CancellationToken
from autogen_core.model_context import ChatCompletionContext, BufferedChatCompletionContext
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from agent import (
    BlenderExpertAgent,
    BlenderManagementAgent,
    BlenderModelingAgent,
    BlenderAnimatorAgent,
    BlenderRenderAgent,
    BlenderReviewerAgent,
    BlenderCodeAgent,
)

def load_config():
    config_list = config_list_from_json(
        "OAI_CONFIG_LIST.json",
        file_location="./config/",
    )
    blender_mcp_params = StdioServerParams(
        command="uvx",
        args=["blender-mcp"],
    )
    return config_list, blender_mcp_params

async def main(prompt: str):
    config_list, blender_mcp_params = load_config()
    model_client = OpenAIChatCompletionClient(
        model=config_list[2]['model'],
        api_key=config_list[2]['api_key'],
    )
    workbench = McpWorkbench(blender_mcp_params)
    await workbench.start()
    # blender_agent = BlenderExpertAgent(
    #     name="blender_agent",
    #     model_client=model_client,
    #     workbench=workbench,
    #     model_client_stream=True,
    #     reflect_on_tool_use=True
    # )
    blender_project_manager = BlenderManagementAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    blender_modeling_expert = BlenderModelingAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    blender_render_expert = BlenderRenderAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    blender_animation_expert = BlenderAnimatorAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    blender_code_expert = BlenderExpertAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    blender_reviewer = BlenderReviewerAgent(
        model_client=model_client,
        workbench=workbench,
        model_client_stream=True,
        reflect_on_tool_use=True
    )
    team = RoundRobinGroupChat(
        [blender_project_manager, blender_modeling_expert, blender_render_expert, blender_animation_expert, blender_reviewer, blender_code_expert],
        termination_condition=TextMessageTermination(source="blender_project_manager"),
    )
    await Console(
        team.run_stream(task=prompt, cancellation_token=CancellationToken())
    )
    await model_client.close()
    await workbench.stop()

if __name__ == "__main__":
    prompts = [
        "Create a house with a door and some windows. The roof is red and the walls are white.",
        "A vibrant autumn forest, with trees ablaze in shades of red, orange, and gold, as a gentle breeze rustles the fallen leaves",
        "A misty spring morning, where dewkissed flowers dot a lush meadow, surrounded by budding trees",
        "A serene winter landscape, with snowcovered evergreen trees and a frozen lake reflecting the pale sunlight",
        "The mountains, majestic and snow-capped, stood like sentinels guarding the vast expanse of the valley, their peaks disappearing into the swirling mist that clung to their rugged slopes.",
        "The desert, an endless sea of shifting sands, stretched to the horizon, its rippling dunes catching the golden rays of the setting sun, creating an ever-changing landscape of shadows and light",
        "The lake, serene and glassy, mirrored the cloudless sky above, reflecting the surrounding mountains and the graceful flight of a heron, as lily pads floated like emerald jewels upon its tranquil surface",
    ]
    asyncio.run(main(prompt=prompts[0]))
