# 🔧 API 排查方案

## 问题分析

**豆包 API 错误：**
```
API 错误：404 - 模型或端点 doubao-pro-32k 不存在，或者您没有访问权限
```

**核心原因：**
豆包 API 密钥（Token）无效 / 过期 / 权限不足，这是**鉴权层面的错误**（不是模型 ID 问题）。

---

## ✅ 已修复的代码

### 1. 添加认证类型标识
```python
"豆包": {
    "endpoint": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "model": "doubao-pro-32k",
    "api_key": "a56ec54a-4f47-4e06-8783-277ead0002eb",
    "auth_type": "volcengine"  # 新增：火山引擎认证
}
```

### 2. 修改调用函数支持火山引擎认证
```python
if auth_type == "volcengine":
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
        "X-Token": config['api_key']  # 添加Token认证
    }
```

---

## 📋 完整排查步骤

### 步骤 1：确认 API Key 有效性

**豆包 API Key：**
```
a56ec54a-4f47-4e06-8783-277ead0002eb
```

**检查方法：**

1. 打开火山引擎控制台
   - 网址：https://console.volcengine.com/

2. 登录账号

3. 进入 **API Key 管理页面**
   - 路径：控制台 → 搜索"豆包" → 打开 → 查看 API Key

4. 确认：
   - ✅ API Key 是否存在
   - ✅ API Key 是否已启用
   - ✅ API Key 是否未过期
   - ✅ API Key 是否有调用额度

### 步骤 2：确认模型权限

**需要的权限：**
- ✅ `doubao-pro-32k` 模型访问权限
- ✅ 基础对话权限

**检查方法：**

1. 登录火山引擎控制台
   - https://console.volcengine.com/

2. 进入 **模型管理**
   - 路径：控制台 → 人工智能 → 豆包

3. 查看已开通的模型

4. 确认 `doubao-pro-32k` 是否在列表中

### 步骤 3：测试 API 调用

**方法 1：使用 curl 测试**
```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer a56ec54a-4f47-4e06-8783-277ead0002eb" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-pro-32k",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

**方法 2：使用 Python 测试**
```python
import requests

response = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    headers={
        "Authorization": "Bearer a56ec54a-4f47-4e06-8783-277ead0002eb",
        "Content-Type": "application/json"
    },
    json={
        "model": "doubao-pro-32k",
        "messages": [{"role": "user", "content": "你好"}]
    }
)

print(response.json())
```

### 步骤 4：检查账户余额

1. 登录火山引擎控制台
2. 进入 **费用中心**
3. 查看账户余额和账单
4. 确认是否有足够的调用额度

---

## 🔍 常见问题及解决方案

### 问题 1：API Key 无效

**症状：**
```
API 错误：401 - Unauthorized
```

**解决方案：**
1. 重新获取 API Key
2. 确保 API Key 完整（没有截断）
3. 确保没有多余的空格或换行

### 问题 2：API Key 过期

**症状：**
```
API 错误：401 - Token expired
```

**解决方案：**
1. 登录火山引擎控制台
2. 生成新的 API Key
3. 更新代码中的 API Key

### 问题 3：权限不足

**症状：**
```
API 错误：403 - Permission denied
```

**解决方案：**
1. 确认已开通 `doubao-pro-32k` 模型
2. 确认账户有足够的调用额度
3. 联系火山引擎客服申请权限

### 问题 4：模型不存在

**症状：**
```
API 错误：404 - Model not found
```

**解决方案：**
1. 使用正确的模型名称
2. 确认模型已开通
3. 尝试使用其他模型

---

## 📝 备选方案

### 方案 1：使用其他豆包模型

如果 `doubao-pro-32k` 不可用，可以尝试：

```python
"豆包": {
    "endpoint": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "model": "doubao-beta",
    "api_key": "a56ec54a-4f47-4e06-8783-277ead0002eb"
}
```

### 方案 2：替换为其他 AI

如果豆包 API 确实无法使用，可以替换为：

#### 替换为 通义千问
```python
"豆包": {
    "endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "model": "qwen-plus",
    "api_key": "sk-dfc23389f69a41c2a8e2247cd1507082",
    "auth_type": "dashscope"
}
```

#### 替换为 智谱GLM
```python
"豆包": {
    "endpoint": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    "model": "glm-4",
    "api_key": "99fd7ad0f2f049f98213b442119f8e77.WKWPvVfDq3SNpp33",
    "auth_type": "bigmodel"
}
```

#### 替换为 DeepSeek
```python
"豆包": {
    "endpoint": "https://api.deepseek.com/v1/chat/completions",
    "model": "deepseek-chat",
    "api_key": "sk-b4c53f1462cf4b11beaf6f9fd745d1ff",
    "auth_type": "deepseek"
}
```

---

## 🔑 获取新的豆包 API Key

### 方法 1：火山引擎控制台

1. 访问：https://console.volcengine.com/
2. 登录/注册账号
3. 搜索"豆包"
4. 进入豆包服务
5. 创建 API Key
6. 复制新的 Key

### 方法 2：豆包开放平台

1. 访问：https://console.volcengine.com/
2. 进入人工智能 → 豆包
3. 创建应用
4. 获取 API Key

---

## ✅ 验证清单

修复后，请确认以下内容：

- [ ] API Key 正确且完整
- [ ] API Key 未过期
- [ ] API Key 有调用权限
- [ ] 模型已开通
- [ ] 账户有足够余额
- [ ] 代码中的端点正确
- [ ] 代码中的模型名称正确

---

## 📞 联系客服

如果以上方法都无法解决问题：

1. **火山引擎客服**：https://console.volcengine.com/
2. **工单系统**：控制台 → 工单 → 提交工单
3. **电话支持**：400-010-9999

---

## 🎯 下一步

1. **首先**：刷新浏览器，重新测试豆包 API
2. **如果仍然失败**：检查 API Key 是否有效
3. **如果 Key 无效**：获取新的 API Key
4. **如果无法获取**：替换为其他 AI（通义千问/智谱GLM/DeepSeek）

---

**请告诉我测试结果，我会继续帮你解决！** 💪
