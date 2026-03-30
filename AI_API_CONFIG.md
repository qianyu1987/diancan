# 🤖 AI 圆桌讨论 - API 配置

## 📝 API 配置说明

以下是 6 个 AI 的 API 配置信息：

---

## 1. 🎯 豆包 (Doubao)

**API 端点**:
```
https://ark.cn-beijing.volces.com/api/v3
```

**模型**:
```
doubao-pro-32k
```

**API Key**:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: 字节跳动豆包模型，适合快速生成

---

## 2. 💻 通义千问 (Qwen)

**API 端点**:
```
https://dashscope.aliyuncs.com/compatible-mode/v1
```

**模型**:
```
qwen-plus
```

**API Key**:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: 阿里云通义千问模型，适合中文对话

---

## 3. 📱 智谱GLM (GLM)

**API 端点**:
```
https://open.bigmodel.cn/api/paas/v4
```

**模型**:
```
glm-4
```

**API Key**:
```
xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: 智谱AI模型，适合知识问答

---

## 4. 🏗️ DeepSeek

**API 端点**:
```
https://api.deepseek.com
```

**模型**:
```
deepseek-chat
```

**API Key**:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: DeepSeek 模型，性价比高

---

## 5. 🧠 DeepSeek-671B

**API 端点**:
```
https://api.deepseek.com
```

**模型**:
```
deepseek-coder
```

**API Key**:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: DeepSeek 大参数代码模型

---

## 6. 🤖 Claude (通过 OpenRouter)

**API 端点**:
```
https://openrouter.ai/api/v1
```

**模型**:
```
anthropic/claude-3-haiku
```

**API Key**:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**说明**: 通过 OpenRouter 访问 Claude

---

## 🔧 如何配置

### 方式 1: 直接编辑代码

在 `ai_team_roundtable.py` 中配置：

```python
import requests

# API 配置
API_CONFIG = {
    "豆包": {
        "endpoint": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-pro-32k",
        "api_key": "your-api-key-here"
    },
    "通义千问": {
        "endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "api_key": "your-api-key-here"
    },
    # ... 其他 AI
}
```

### 方式 2: 环境变量

```bash
# 设置环境变量
export DOUBAO_API_KEY="your-api-key"
export QWEN_API_KEY="your-api-key"
export GLM_API_KEY="your-api-key"
export DEEPSEEK_API_KEY="your-api-key"
export OPENROUTER_API_KEY="your-api-key"
```

### 方式 3: 配置文件

创建 `api_config.json`:

```json
{
    "豆包": {
        "endpoint": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-pro-32k",
        "api_key": "your-api-key"
    },
    "通义千问": {
        "endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "api_key": "your-api-key"
    }
}
```

---

## 📝 调用示例

### Python 示例

```python
import requests

def call_ai(name, prompt):
    config = API_CONFIG[name]
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(
        f"{config['endpoint']}/chat/completions",
        headers=headers,
        json=data
    )
    
    return response.json()
```

---

## ⚠️ 安全提示

1. **不要分享真实的 API Key**
2. **使用环境变量存储敏感信息**
3. **定期更换 API Key**
4. **设置 API 使用限额**

---

## 💡 获取 API Key

- **豆包**: https://console.volcengine.com/
- **通义千问**: https://dashscope.console.aliyun.com/
- **智谱GLM**: https://open.bigmodel.cn/
- **DeepSeek**: https://platform.deepseek.com/
- **OpenRouter**: https://openrouter.ai/

---

## 🔄 更新日志

- 2026-03-29: 创建文档

---

**注意**: 请将 `your-api-key-here` 替换为你自己的 API Key！
