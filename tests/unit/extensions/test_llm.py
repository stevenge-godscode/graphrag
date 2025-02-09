import json
import pytest
import logging
from openai import OpenAI

# 配置 OpenAI 客户端
client = OpenAI(
    api_key="<your api key>",
    base_url="http://127.0.0.1:11434/v1",
)

# 配置 logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 定义基础的系统提示
system_prompt = """你是一个智能助手，需要严格按照 JSON 格式回答问题。需要仔细检查答案，确保没有问题。

示例：
问题：世界最高的山是什么？
JSON 回答：
{
    "answer": "珠穆朗玛峰"
}

现在请回答以下问题：
"""

# 仅包含问题的测试数据
test_questions = [
    "水的沸点?",
    "蒙娜丽莎谁画的?",
    "太阳系有多少颗行星?",
    "黄金的化学符号是什么?",
    "世界上人口最多的国家?",
    "相对论是谁提出的?",
    "世界上最长的河流是?",
    "光速是多少?",
    "二氧化碳的化学式是什么?",
    "第一个登上月球的人是谁?"
]


from graphrag.utils.prompts import *

@pytest.mark.parametrize("question", test_questions)
def test_llm_json_format(question):
    """测试 LLM 返回 JSON 是否符合基本结构"""

    # 合并 system 提示和用户问题
    full_prompt = system_prompt + question

    response = client.chat.completions.create(
        model="deepseek-r1:32b",
        messages=[{"role": "user", "content": full_prompt}],  # 直接传递完整的 prompt
        # response_format={"type": "json_object"},
        temperature=0.0,
    )

    # 解析返回的 JSON
    output_json = remove_md(remove_think_tag(response.choices[0].message.content))
    
    # 记录日志
    logger.debug("Prompt: %s", full_prompt)
    logger.debug("LLM Response: %s", response)
    logger.debug("Parsed JSON: %s", output_json)

    # 断言检查输出格式
    assert "answer" in output_json, f"Invalid JSON format: {output_json}"