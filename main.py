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
        
        # 正确获取配置 + 防御性拷贝
        qq_ids = config.get("qq_id", []) or []
        self.qqid_list = set(str(qq_id).strip() for qq_id in qq_ids if qq_id)
        self.prompt = config.get("prompt", "你是一个温柔的人")

    @filter.on_llm_request()
    async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest):
        if not self.qqid_list or not self.prompt:
            return
        
        # 类型统一为字符串
        sender_id = str(event.get_sender_id())
        
        if sender_id in self.qqid_list:
            req.system_prompt = self.prompt
            logger.debug(f"已为 {sender_id} 应用特殊提示词")

    async def terminate(self):
        logger.info("Prompt Router 插件已卸载")