from openai._client import OpenAI

class DeepSeekClient(OpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 继承父类的初始化方法

    def custom_method(self, prompt: str):
        """
        自定义方法，可以用于特殊的 API 调用逻辑
        """
        response = self.completions.create(
            model="deepseek-r1:32b",
            prompt=prompt,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

# 示例：创建一个自定义客户端实例
client = DeepSeekClient(api_key="your-api-key")

# 调用自定义方法
response = client.custom_method("你好，世界!")
print(response)


from openai._client import AsyncOpenAI

class DeepSeekAsyncClient(AsyncOpenAI):
    async def async_custom_method(self, prompt: str):
        response = await self.completions.create(
            model="deepseek-r1:32b",
            prompt=prompt,
            temperature=0.7,
        )
        return response.choices[0].text.strip()