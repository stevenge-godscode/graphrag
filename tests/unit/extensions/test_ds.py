import json
import pytest
import logging
from openai import OpenAI
from pathlib import Path  # 用于处理文件路径

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
output_file = Path("test_results.json")

# 配置 OpenAI 客户端
client = OpenAI(
    api_key="<your-api-key>",  
    base_url="http://127.0.0.1:11434/v1",
)

# 定义 System Prompt
system_prompt = """
你需要严格按照以下 JSON 格式返回答案，不得缺少任何字段：
{
    "response": "<你的答案>"
}
请确保：
1. 你返回的 JSON 结构必须包含 `response` 这个 key，不可缺失。
2. 你的回答必须是 JSON 格式，**不能添加额外的 Markdown 代码块**（如```json）。
3. 不允许额外的解释或思考过程，直接返回 JSON。
4. 若无法回答，请返回：
   {
       "response": "**UNKNOWN**"
   }
5. 确保 JSON 语法正确，没有多余的逗号或引号错误。
"""

# 仅包含问题的测试数据
test_prompts = [
    # 物理
    "水的沸点?",
    "光速是多少?",
    "牛顿第一定律的内容是什么?",
    "引力常数的值是多少?",
    "谁发现了电磁感应定律?",
    "波粒二象性是什么?",
    "红移和蓝移的含义是什么?",
    "能量的单位是什么?",
    "谁提出了量子力学的不确定性原理?",
    "热力学第二定律的核心内容是什么?",

    # 化学
    "黄金的化学符号是什么?",
    "二氧化碳的化学式?",
    "氢气的分子式是什么?",
    "水的化学式是什么?",
    "氧气的化学式是什么?",
    "最轻的元素是什么?",
    "稀有气体有哪些?",
    "酸碱中和反应的产物是什么?",
    "谁提出了元素周期表?",
    "最硬的天然矿物是什么?",

    # 生物
    "DNA 的全称是什么?",
    "人类的染色体数目是多少?",
    "地球上最大的哺乳动物是什么?",
    "光合作用的主要产物是什么?",
    "血液中的氧气是由什么运输的?",
    "人类的体温正常范围是多少?",
    "最早的生物出现在地球上的哪个时代?",
    "细胞的基本结构有哪些?",
    "RNA 和 DNA 的主要区别是什么?",
    "人体内最大的器官是什么?",

    # 天文
    "太阳系有多少颗行星?",
    "太阳的主要成分是什么?",
    "银河系属于什么类型的星系?",
    "黑洞是什么?",
    "最接近地球的行星是什么?",
    "宇宙膨胀理论是谁提出的?",
    "太阳的寿命大约是多少年?",
    "月球为什么会有潮汐?",
    "宇宙中最冷的地方是哪里?",
    "中子星是什么?",

    # 地理
    "世界上人口最多的国家?",
    "世界上面积最大的国家?",
    "世界上最高的山峰是什么?",
    "世界上最长的河流是?",
    "撒哈拉沙漠位于哪个大陆?",
    "地球的赤道周长是多少?",
    "地球表面的海洋占比是多少?",
    "最深的海洋沟是哪里?",
    "北极属于哪个国家?",
    "长城位于哪个国家?",

    # 历史
    "蒙娜丽莎谁画的?",
    "埃及金字塔是哪个古代文明建造的?",
    "第二次世界大战持续了多少年?",
    "谁是第一位美国总统?",
    "中国的四大发明是什么?",
    "文艺复兴时期的代表人物有哪些?",
    "甲骨文是哪种古代文字?",
    "长城的修建始于哪个朝代?",
    "法国大革命发生在哪一年?",
    "第一次工业革命的标志性发明是什么?",

    # 文学
    "《哈姆雷特》的作者是谁?",
    "《红楼梦》的作者是谁?",
    "莎士比亚的四大悲剧是什么?",
    "《百年孤独》的作者是谁?",
    "《西游记》的主人公是谁?",
    "《1984》是谁写的?",
    "《傲慢与偏见》的作者是谁?",
    "《悲惨世界》的作者是谁?",
    "《老人与海》的作者是谁?",
    "《资本论》的作者是谁?",

    # 计算机
    "第一台计算机是什么时候诞生的?",
    "比特和字节的关系是什么?",
    "Python 的主要应用领域是什么?",
    "谁发明了万维网?",
    "人工智能的三大流派是什么?",
    "什么是机器学习?",
    "计算机的基本组成部分有哪些?",
    "5G 技术的主要特点是什么?",
    "存储器和内存的区别是什么?",
    "Linux 操作系统的创始人是谁?",

    # 数学
    "圆周率的近似值是多少?",
    "毕达哥拉斯定理的数学表达式是什么?",
    "对数的底数一般是多少?",
    "谁提出了微积分?",
    "0 是偶数还是奇数?",
    "最小的素数是多少?",
    "黄金分割的值是多少?",
    "斐波那契数列的前五项是什么?",
    "勾股定理适用于什么类型的三角形?",
    "欧几里得几何的基本公理是什么?",

    # 经济
    "GDP 的全称是什么?",
    "供求关系如何影响价格?",
    "股票市场的基本作用是什么?",
    "凯恩斯经济学的核心观点是什么?",
    "市场经济和计划经济的区别是什么?",
    "通货膨胀的定义是什么?",
    "什么是外汇储备?",
    "中央银行的主要职能是什么?",
    "全球最大的证券交易所是哪个?",
    "什么是区块链?",

    # 体育
    "奥运会每几年举办一次?",
    "世界杯足球赛多久举办一次?",
    "NBA 的全称是什么?",
    "第一届奥运会在哪里举办?",
    "网球四大满贯是什么?",
    "国际象棋的基本规则是什么?",
    "马拉松比赛的标准距离是多少?",
    "棒球比赛的基本规则是什么?",
    "谁是历史上获得奥运金牌最多的运动员?",
    "F1 赛车的最高时速大约是多少?",

    # 音乐
    "贝多芬的代表作有哪些?",
    "莫扎特是哪国人?",
    "肖邦以哪种乐器闻名?",
    "四大交响曲之王是谁?",
    "吉他有几根标准弦?",
    "世界上最大的音乐节是哪个?",
    "谁是《命运交响曲》的作曲家?",
    "摇滚乐起源于哪个国家?",
    "最古老的乐器是什么?",
    "古筝是哪个国家的传统乐器?",

    # 影视
    "《泰坦尼克号》的导演是谁?",
    "世界上票房最高的电影是哪部?",
    "奥斯卡最佳影片奖的评选标准是什么?",
    "漫威宇宙的第一部电影是哪部?",
    "《黑客帝国》的导演是谁?",
    "《星球大战》的主要角色是谁?",
    "《指环王》三部曲的导演是谁?",
    "电影特效中 CGI 代表什么?",
    "日本的著名动画导演有哪些?",
    "《肖申克的救赎》改编自谁的小说?",
]

@pytest.mark.parametrize("user_prompt", test_prompts)
def test_llm_json_format(user_prompt):
    """测试 LLM 是否返回符合 JSON 结构的有效格式"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_prompt},  # **去掉冗余格式要求**

    ]

    response = client.chat.completions.create(
        model="llama3.1:32k",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=32000,
        max_completion_tokens=32000,
        top_p=0.0,        # ✅ 限制可能性
    )

    response_text = response.choices[0].message.content
    logger.debug(f"Raw Response: {response_text}")

    # 解析 JSON
    try:
        output_json = json.loads(response_text)
        logger.debug(f"Parsed JSON: {output_json}")
        # ✅ 存储到 JSON 文件
        save_response_to_file(user_prompt, output_json)
        # 断言 JSON 结构符合预期
        assert isinstance(output_json, dict), "返回的数据应为 JSON 对象"
        assert "response" in output_json, "JSON 必须包含 'response' 键"
        assert isinstance(output_json["response"], str), "'response' 值必须是字符串"

    except json.JSONDecodeError:
        pytest.fail("返回的数据不是有效的 JSON 格式")


def save_response_to_file(question, response):
    """追加存储 JSON 响应到文件（逐行存储）"""
    with open(output_file, "a", encoding="utf-8") as f:
        json.dump({question: response}, f, ensure_ascii=False)
        f.write("\n")  # ✅ 换行，方便读取
        logger.info(f"Appended response for '{question}' to {output_file}")

