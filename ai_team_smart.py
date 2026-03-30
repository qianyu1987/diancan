#!/usr/bin/env python3
"""
AI 智能团队协作系统 - 真正调用 AI API
每个角色有独特人设，能够互相引用和协作
"""

import streamlit as st
import requests
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional

# ========== 配置 ==========
BACKEND_URL = "http://localhost:3000"  # 多 AI 集成后端
PROJECT_ROOT = r"D:\dingcan"
MINIPROGRAM_PAGES = os.path.join(PROJECT_ROOT, "miniprogram", "pages")
CLOUDFUNCTIONS_DIR = os.path.join(PROJECT_ROOT, "cloudfunctions")

# ========== AI 角色定义 ==========
# 每个角色有独特的 system prompt，定义其专业领域和思考方式
AI_ROLES = {
    "doubao": {
        "name": "🎯 豆包",
        "role": "全局军师",
        "emoji": "🎯",
        "color": "#E91E63",
        "service": "doubao",
        "system_prompt": """你是豆包AI，担任团队的「全局军师」角色。

你的职责：
1. 统筹全局，分析需求的核心价值和潜在风险
2. 从产品、技术、用户体验多维度思考问题
3. 给出战略层面的建议和方向性指导
4. 识别关键决策点和权衡取舍

你的思考风格：
- 宏观视角，不纠结细节
- 注重可行性和投入产出比
- 善于发现潜在问题和风险
- 给出清晰的建议和下一步行动

回复格式：
【豆包的战略分析】
1. 需求解读：...
2. 核心挑战：...
3. 建议方案：...
4. 风险提示：...

请用中文回复，简洁专业。"""
    },
    
    "tongyi": {
        "name": "💻 通义千问",
        "role": "代码工程师",
        "emoji": "💻",
        "color": "#FF9800",
        "service": "tongyi",
        "system_prompt": """你是通义千问，担任团队的「代码工程师」角色。

你的职责：
1. 将需求转化为可执行的代码实现
2. 设计清晰的代码架构和模块划分
3. 编写高质量、可维护的代码
4. 关注代码性能和最佳实践

你的代码风格：
- 优先使用微信小程序原生语法
- 注释清晰，命名规范
- 考虑错误处理和边界情况
- 提供完整可运行的代码

回复格式：
【通义千问的代码方案】

### 技术设计
...

### 代码实现
```javascript
// 完整代码
```

### 使用说明
...

请用中文回复，代码要有完整注释。"""
    },
    
    "zhipu": {
        "name": "📱 智谱GLM",
        "role": "产品经理",
        "emoji": "📱",
        "color": "#4CAF50",
        "service": "zhipu",
        "system_prompt": """你是智谱GLM，担任团队的「产品经理」角色。

你的职责：
1. 深入理解用户需求和痛点
2. 设计用户体验流程和交互方案
3. 定义产品功能和优先级
4. 平衡用户需求和技术可行性

你的思考方式：
- 以用户为中心设计体验
- 关注细节和情感化设计
- 考虑不同场景和用户类型
- 提供可落地的产品建议

回复格式：
【智谱GLM的产品方案】

### 用户场景
...

### 功能设计
...

### 交互流程
...

### 体验优化建议
...

请用中文回复，注重可读性和画面感。"""
    },
    
    "deepseek": {
        "name": "🏗️ DeepSeek",
        "role": "技术架构师",
        "emoji": "🏗️",
        "color": "#2196F3",
        "service": "deepseek",
        "system_prompt": """你是DeepSeek，担任团队的「技术架构师」角色。

你的职责：
1. 设计系统整体架构和技术选型
2. 定义数据库结构和 API 接口
3. 考虑性能、安全、可扩展性
4. 评审技术方案的合理性

你的架构原则：
- 简洁优先，避免过度设计
- 模块化，高内聚低耦合
- 考虑未来扩展性
- 性能和成本平衡

回复格式：
【DeepSeek的架构设计】

### 系统架构图
（用文字描述架构层次）

### 数据库设计
```javascript
// 集合结构
```

### API 接口设计
```javascript
// 接口定义
```

### 技术要点
...

请用中文回复，技术深度要够。"""
    },
    
    "deepseek-large": {
        "name": "🧠 DeepSeek-671B",
        "role": "技术领袖",
        "emoji": "🧠",
        "color": "#9C27B0",
        "service": "deepseek",  # 复用 deepseek 服务
        "system_prompt": """你是DeepSeek-671B，团队的「技术领袖」，拥有最深厚的技术功底。

你的职责：
1. 解决最复杂的技术难题
2. 进行深层优化和性能调优
3. 提供权威的技术决策
4. 指导团队的技术方向

你的思考深度：
- 不满足于表面解决方案
- 挖掘底层原理和本质
- 考虑极端情况和边界条件
- 给出最优解和替代方案

回复格式：
【DeepSeek-671B 深度分析】

### 问题本质
...

### 核心技术点
...

### 最优解决方案
...

### 性能优化策略
...

### 潜在问题与规避
...

请用中文回复，追求技术极致。"""
    },
    
    "claude": {
        "name": "🤖 Claude助手",
        "role": "代码优化师",
        "emoji": "🤖",
        "color": "#00BCD4",
        "service": "deepseek",  # 临时用 deepseek，可以换成其他
        "system_prompt": """你是Claude助手，担任团队的「代码优化师」角色。

你的职责：
1. 整合团队所有建议，输出最终方案
2. 优化代码质量和可读性
3. 补充缺失的细节和边界处理
4. 确保代码可以生产环境使用

你的输出标准：
- 代码完整可运行
- 考虑所有边界情况
- 错误处理完善
- 注释清晰详尽

回复格式：
【Claude 最终整合方案】

### 整合要点
（汇总其他成员的关键建议）

### 完整代码
```javascript
// 生产级代码，包含完整实现
```

### 关键特性
- ✅ ...
- ✅ ...

### 使用说明
...

请用中文回复，代码要可以直接使用。"""
    }
}

# 角色发言顺序
ROLE_ORDER = ["doubao", "zhipu", "deepseek", "tongyi", "deepseek-large", "claude"]

# ========== API 调用 ==========
def call_ai_service(service: str, message: str, system_prompt: str, context: str = "") -> Dict:
    """调用后端 AI 服务"""
    try:
        # 构建完整 prompt
        full_message = f"{context}\n\n当前讨论主题：{message}" if context else message
        
        payload = {
            "message": full_message,
            "services": [service]
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get("results", {}).get(service, {})
            
            if "error" in result:
                return {"success": False, "error": result["error"]}
            
            content = result.get("content", "")
            return {
                "success": True,
                "content": content,
                "usage": result.get("usage", {}),
                "model": result.get("model", "")
            }
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "请求超时，AI 正在思考复杂问题..."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "无法连接到 AI 服务，请检查后端是否启动"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def build_context(messages: List[Dict], current_role: str) -> str:
    """构建对话上下文，让 AI 能看到之前的讨论"""
    if not messages:
        return ""
    
    context_parts = ["【之前的讨论记录】"]
    
    for msg in messages[-4:]:  # 只取最近4条，避免 token 过多
        speaker = msg.get("name", "未知")
        content = msg.get("content", "")
        # 截取关键内容
        if len(content) > 500:
            content = content[:500] + "..."
        context_parts.append(f"\n{speaker}：\n{content}")
    
    return "\n".join(context_parts)


# ========== 代码处理 ==========
def extract_code_blocks(content: str) -> List[tuple]:
    """提取代码块"""
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return [(lang or 'text', code.strip()) for lang, code in matches if code.strip()]


def save_code_to_project(code: str, lang: str, topic: str) -> tuple:
    """保存代码到项目"""
    try:
        safe_topic = re.sub(r'[^\w\u4e00-\u9fff]', '', topic)[:20].replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if lang in ['js', 'javascript']:
            filename = f"{safe_topic}_{timestamp}.js"
            filepath = os.path.join(MINIPROGRAM_PAGES, filename)
            os.makedirs(MINIPROGRAM_PAGES, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            return ("✅ 页面JS", filepath, True)
        elif lang in ['json']:
            filename = f"{safe_topic}_{timestamp}.json"
            filepath = os.path.join(MINIPROGRAM_PAGES, filename)
            os.makedirs(MINIPROGRAM_PAGES, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            return ("✅ JSON配置", filepath, True)
        else:
            func_name = f"{safe_topic}_{timestamp}"
            func_dir = os.path.join(CLOUDFUNCTIONS_DIR, func_name)
            os.makedirs(func_dir, exist_ok=True)
            with open(os.path.join(func_dir, "index.js"), 'w', encoding='utf-8') as f:
                f.write(code)
            with open(os.path.join(func_dir, "config.json"), 'w', encoding='utf-8') as f:
                f.write('{"permissions": {"openapi": []}}')
            return ("✅ 云函数", func_dir, True)
    except Exception as e:
        return ("❌ 保存失败", str(e), False)


# ========== Streamlit 配置 ==========
st.set_page_config(
    page_title="AI 智能团队协作系统",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Session State ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "total_rounds" not in st.session_state:
    st.session_state.total_rounds = 6
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "speaking_idx" not in st.session_state:
    st.session_state.speaking_idx = -1
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "error" not in st.session_state:
    st.session_state.error = None

# ========== 样式 ==========
st.markdown("""
<style>
/* 整体风格 */
.main {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

/* 团队容器 */
.team-container {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 15px;
    margin: 30px 0;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    flex-wrap: wrap;
}

.team-member {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 15px;
    border-radius: 15px;
    transition: all 0.3s ease;
    min-width: 100px;
}

.team-member.speaking {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
    transform: scale(1.1);
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
}

.character {
    font-size: 50px;
    transition: all 0.3s ease;
}

.team-member.speaking .character {
    animation: bounce 0.6s ease-in-out infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.name-tag {
    font-weight: bold;
    font-size: 13px;
    text-align: center;
    color: white;
}

.role-tag {
    font-size: 11px;
    color: #aaa;
    text-align: center;
}

.status-tag {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 10px;
    background: rgba(255,255,255,0.1);
}

.status-tag.speaking {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
}

/* 对话框 */
.chat-container {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    border-left: 4px solid;
}

.chat-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.chat-emoji {
    font-size: 30px;
}

.chat-name {
    font-size: 18px;
    font-weight: bold;
    color: white;
}

.chat-role {
    font-size: 12px;
    color: #888;
    margin-left: auto;
}

.chat-content {
    color: #ddd;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}

.chat-content code {
    background: rgba(0,0,0,0.3);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
}

/* 加载动画 */
.loading-dots {
    display: inline-flex;
    gap: 5px;
}

.loading-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: loading 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes loading {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

/* 按钮美化 */
.stButton button {
    border-radius: 10px;
    font-weight: bold;
}

/* 输入框美化 */
.stTextInput input {
    border-radius: 10px;
}

/* 进度条 */
.progress-container {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ========== 标题 ==========
st.markdown("""
<h1 style='text-align: center; color: white;'>
    🧠 AI 智能团队协作系统
</h1>
<p style='text-align: center; color: #888; font-size: 14px;'>
    真正调用 AI API · 智能协作 · 代码落地
</p>
""", unsafe_allow_html=True)

# ========== 检查后端连接 ==========
@st.cache_resource
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("services", {})
        return False, {}
    except:
        return False, {}

backend_ok, available_services = check_backend()

if not backend_ok:
    st.error("⚠️ 无法连接到 AI 后端服务，请确保后端运行在 http://localhost:3000")
    st.info("💡 启动命令: cd multi-ai-integration/backend && node server.js")
else:
    with st.sidebar:
        st.success("✅ 后端已连接")
        st.markdown("### 🔌 AI 服务状态")
        for service, configured in available_services.items():
            icon = "✅" if configured else "❌"
            name = AI_ROLES.get(service, {}).get("name", service)
            st.markdown(f"{icon} {name}")

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎭 团队成员")
    for role_id in ROLE_ORDER:
        role = AI_ROLES[role_id]
        st.markdown(f"**{role['emoji']} {role['name'].split()[1]}** - {role['role']}")
    
    st.markdown("---")
    st.markdown("### 📂 代码输出目录")
    st.code(PROJECT_ROOT, language="text")

# ========== 主界面 ==========
col1, col2 = st.columns([4, 1])

with col1:
    topic = st.text_input(
        "💬 输入讨论主题",
        placeholder="如：开发菜单浏览功能，支持分类筛选和搜索",
        value=st.session_state.topic
    )

with col2:
    rounds = st.select_slider("轮次", options=[3, 4, 5, 6], value=st.session_state.total_rounds)

# ========== 可视化团队 ==========
st.markdown("---")

html_content = '<div class="team-container">'

for idx, role_id in enumerate(ROLE_ORDER):
    role = AI_ROLES[role_id]
    is_speaking = (idx == st.session_state.speaking_idx)
    speaking_class = "speaking" if is_speaking else ""
    
    status = "🗣️ 发言中" if is_speaking else "🪑 等待"
    
    html_content += f'''
    <div class="team-member {speaking_class}">
        <div class="character">{role['emoji']}</div>
        <div class="name-tag">{role['name'].split()[1]}</div>
        <div class="role-tag">{role['role']}</div>
        <div class="status-tag {speaking_class}">{status}</div>
    </div>
    '''

html_content += '</div>'
st.markdown(html_content, unsafe_allow_html=True)

# ========== 进度显示 ==========
if st.session_state.messages:
    progress = len(st.session_state.messages) / rounds
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: white;">📊 讨论进度</span>
            <span style="color: #667eea;">{len(st.session_state.messages)}/{rounds} 轮</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;">
            <div style="background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 10px; height: 100%; width: {min(progress * 100, 100)}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== 控制按钮 ==========
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 开始讨论", type="primary", use_container_width=True, disabled=st.session_state.is_processing):
        if topic:
            st.session_state.messages = []
            st.session_state.current_round = 0
            st.session_state.total_rounds = rounds
            st.session_state.topic = topic
            st.session_state.speaking_idx = -1
            st.session_state.error = None
            st.rerun()
        else:
            st.error("请输入讨论主题")

with col2:
    next_disabled = (
        st.session_state.is_processing or 
        len(st.session_state.messages) == 0 or
        st.session_state.current_round >= st.session_state.total_rounds
    )
    
    if st.button("➡️ 下一轮", use_container_width=True, disabled=next_disabled):
        if st.session_state.current_round < st.session_state.total_rounds:
            st.session_state.is_processing = True
            st.session_state.error = None
            
            # 获取当前发言者
            role_idx = st.session_state.current_round % len(ROLE_ORDER)
            role_id = ROLE_ORDER[role_idx]
            role = AI_ROLES[role_id]
            
            st.session_state.speaking_idx = role_idx
            
            # 构建上下文
            context = build_context(st.session_state.messages, role_id)
            
            # 调用 AI
            with st.spinner(f"{role['name']} 正在思考..."):
                result = call_ai_service(
                    role['service'],
                    st.session_state.topic,
                    role['system_prompt'],
                    context
                )
            
            if result['success']:
                st.session_state.messages.append({
                    "role_id": role_id,
                    "name": role['name'],
                    "role": role['role'],
                    "emoji": role['emoji'],
                    "color": role['color'],
                    "content": result['content'],
                    "usage": result.get('usage', {}),
                    "timestamp": datetime.now().isoformat()
                })
                st.session_state.current_round += 1
            else:
                st.session_state.error = result['error']
            
            st.session_state.is_processing = False
            st.rerun()

with col3:
    if st.button("🔄 重置", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_round = 0
        st.session_state.speaking_idx = -1
        st.session_state.is_processing = False
        st.session_state.error = None
        st.rerun()

# ========== 错误显示 ==========
if st.session_state.error:
    st.error(f"❌ {st.session_state.error}")

# ========== 对话历史 ==========
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💬 讨论记录")
    
    for msg in st.session_state.messages:
        color = msg.get('color', '#667eea')
        
        st.markdown(f"""
        <div class="chat-container" style="border-left-color: {color};">
            <div class="chat-header">
                <span class="chat-emoji">{msg['emoji']}</span>
                <span class="chat-name">{msg['name']}</span>
                <span class="chat-role">{msg['role']}</span>
            </div>
            <div class="chat-content">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 代码块处理
        code_blocks = extract_code_blocks(msg['content'])
        if code_blocks:
            for i, (lang, code) in enumerate(code_blocks, 1):
                with st.expander(f"📄 代码块 {i} ({lang})", expanded=False):
                    st.code(code, language=lang)
                    
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        if st.button(f"💾 保存到项目", key=f"save_{msg['role_id']}_{i}"):
                            result = save_code_to_project(code, lang, st.session_state.topic)
                            if result[2]:
                                st.success(f"{result[0]}: `{result[1]}`")
                            else:
                                st.error(f"{result[0]}: {result[1]}")

# ========== 讨论完成 ==========
if st.session_state.messages and st.session_state.current_round >= st.session_state.total_rounds:
    st.markdown("---")
    st.markdown("### 🎉 讨论完成！")
    
    # 统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    total_tokens = sum(msg.get('usage', {}).get('total_tokens', 0) for msg in st.session_state.messages)
    total_code = sum(len(extract_code_blocks(msg['content'])) for msg in st.session_state.messages)
    
    with col1:
        st.metric("💬 发言数", len(st.session_state.messages))
    with col2:
        st.metric("👥 参与者", len(ROLE_ORDER))
    with col3:
        st.metric("💻 代码块", total_code)
    with col4:
        st.metric("📊 Token", total_tokens)
    
    # 批量保存代码
    if total_code > 0:
        st.markdown("---")
        st.markdown("### 💾 代码批量保存")
        
        if st.button("📥 保存所有代码到项目", type="primary"):
            saved = []
            for msg in st.session_state.messages:
                for lang, code in extract_code_blocks(msg['content']):
                    if len(code) > 50:
                        result = save_code_to_project(code, lang, st.session_state.topic)
                        if result[2]:
                            saved.append(result)
            
            if saved:
                st.success(f"✅ 成功保存 {len(saved)} 个文件！")
                for label, path, _ in saved:
                    st.markdown(f"- **{label}**: `{path}`")
            else:
                st.warning("没有找到可保存的代码")
        
        st.balloons()

# ========== 底部信息 ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
    🧠 AI 智能团队协作系统 | 真正调用 AI API | 自动代码落地
</div>
""", unsafe_allow_html=True)
