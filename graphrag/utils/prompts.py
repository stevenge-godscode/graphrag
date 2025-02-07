@staticmethod
def remove_think_tag(text: str) -> str:
    import re
    # 使用正则表达式去除 <think> 标签及其内容
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    return cleaned_text

@staticmethod
def get_text_after_keyword(text: str, keyword: str) -> str:
    # 查找指定的 keyword 在 text 中的位置
    start_pos = text.find(keyword)
    if start_pos != -1:
        # 从 keyword 后的位置提取文本
        return text[start_pos + len(keyword):].strip()
    return ""  # 如果没有找到 keyword，返回空字符串