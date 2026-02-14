from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
from astrbot.core.provider.entities import ProviderRequest


@register(
    "astrbot_plugin_prompts_router",
    "Radiant303",
    "为特定QQ用户群体单独设置LLM系统提示词",
    "1.0.0",
)
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.qqid_list = set(config.qq_id)
        self.prompt = config.prompt

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.on_llm_request()
    async def my_custom_hook_1(
        self, event: AstrMessageEvent, req: ProviderRequest
    ):  # 请注意有三个参数
        if len(self.qqid_list) == 0:
            return
        if event.get_sender_id() in self.qqid_list:
            req.system_prompt = self.prompt

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("插件已卸载")
