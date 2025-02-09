@staticmethod
def remove_think_tag(text: str) -> str:
    import re
    # 使用正则表达式去除 <think> 标签及其内容
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    return cleaned_text

@staticmethod
def get_text_after_keyword(text: str, keyword: str) -> str:
    return text
    # 查找指定的 keyword 在 text 中的位置
    start_pos = text.find(keyword)
    if start_pos != -1:
        # 从 keyword 后的位置提取文本
        return text[start_pos + len(keyword):].strip()
    return ""  # 如果没有找到 keyword，返回空字符串

@staticmethod
def remove_md(text: str) -> str:
    """
    1. 纯 JSON（无 Markdown）
    2. JSON 被 Markdown 代码块包裹（```json ... ```)
    """
    # 去掉 Markdown 代码块
    return text.strip().strip("```json").strip("```")
