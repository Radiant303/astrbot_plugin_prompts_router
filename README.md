# 🎭 谄媚插件 — astrbot_plugin_prompts_router

> 为特定 QQ 用户群体单独设置 LLM 系统提示词，某种程度上保护你的BOT。

[![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-blue?style=flat-square)](https://github.com/Soulter/AstrBot)
[![Version](https://img.shields.io/badge/version-v1.3.0-green?style=flat-square)](#)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange?style=flat-square)](./LICENSE)

---

## ✨ 功能特性

- **精准路由** — 根据发送者的 QQ ID 精准匹配，仅对指定用户生效
- **提示词覆盖** — 在 LLM 请求前，动态替换系统提示词（System Prompt）
- **零侵入** — 基于 AstrBot 的 `on_llm_request` 钩子机制，不修改核心逻辑
- **配置热加载** — 通过 AstrBot 管理面板即可修改配置，无需重启

## 📦 安装

### 从 AstrBot 插件市场安装（推荐）

在 AstrBot 管理面板的 **插件市场** 中搜索 `astrbot_plugin_prompts_router` 或 `谄媚插件`，点击安装即可。

### 从 GitHub 仓库安装

在 AstrBot 管理面板中，选择 **从 Git 仓库安装**，输入仓库地址：

```
https://github.com/Radiant303/astrbot_plugin_prompts_router
```

## ⚙️ 配置说明

安装后，在 AstrBot 管理面板的 **插件管理 → 谄媚插件 → 配置** 中进行设置。

| 配置项   | 类型           | 默认值           | 说明                           |
| :------- | :------------- | :--------------- | :----------------------------- |
| `qq_id`  | `list<string>` | `[]`             | 需要特殊对待的 QQ 号列表       |
| `prompt` | `text`         | *(内置人格设定)* | 对上述 QQ 用户生效的系统提示词 |

### 配置示例

```json
{
  "qq_id": ["123456789", "987654321"],
  "prompt": "你是一只温柔的猫娘，叫做果粒，说话要软萌可爱~"
}
```

> **提示**：`qq_id` 列表为空时，插件不会对任何用户生效，相当于自动跳过。

## 🔧 工作原理

本插件利用 AstrBot 提供的 **LLM 请求钩子** (`@filter.on_llm_request()`) 来实现提示词路由：

```
用户发送消息
    │
    ▼
AstrBot 核心接收消息
    │
    ▼
触发 on_llm_request 钩子
    │
    ▼
┌─────────────────────────────┐
│  插件检查 sender QQ ID      │
│  是否在 qq_id 列表中        │
│                             │
│  ✅ 命中 → 替换 system_prompt │
│  ❌ 未命中 → 不做任何操作     │
└─────────────────────────────┘
    │
    ▼
请求发送至 LLM 模型
```

核心代码逻辑非常简洁：

```python
@filter.on_llm_request()
async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest):
    if len(self.qqid_list) == 0:
        return
    if event.get_sender_id() in self.qqid_list:
        req.system_prompt = self.prompt
```

## 🎯 使用场景

- **VIP 用户定制**：为特定用户提供专属的 AI 人格体验
- **个性化助手**：针对不同用户设定不同的回复风格和知识领域
- **角色扮演**：为特定好友启用趣味人格设定

## 📋 依赖要求

- **AstrBot** >= v4.5.0（推荐）
- 需要配置并启用至少一个 LLM Provider

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 [提交 Bug](https://github.com/Soulter/astrbot_plugin_prompts_router/issues)
- 💡 [功能建议](https://github.com/Soulter/astrbot_plugin_prompts_router/issues)

## 📄 许可证

本项目基于 [GNU AGPL-3.0](./LICENSE) 许可证开源。

## 📚 相关资源

- [AstrBot 官方文档](https://docs.astrbot.app)
- [AstrBot 插件开发指南](https://docs.astrbot.app/dev/star/plugin-new.html)
- [AstrBot GitHub](https://github.com/Soulter/AstrBot)
