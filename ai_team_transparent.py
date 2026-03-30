import streamlit as st
import time
import os
import re
from datetime import datetime

# 配置
PROJECT_ROOT = r"D:\dingcan"
MINIPROGRAM_PAGES = os.path.join(PROJECT_ROOT, "miniprogram", "pages")
CLOUDFUNCTIONS_DIR = os.path.join(PROJECT_ROOT, "cloudfunctions")

# 6个模型详细信息
TEAM = [
    {
        "name": "🎯 豆包",
        "role": "全局军师",
        "color": "#E91E63",
        "thinking": "分析讨论主题的全局意义和风险...",
        "response": """【豆包的分析】

这个需求很有意思。让我从全局角度分析一下：

1. **核心需求分析**
   - 菜单浏览是订餐系统的基础功能
   - 需要支持分类筛选和搜索
   - 用户体验很重要

2. **技术方案**
   - 前端：小程序页面 + 组件
   - 后端：菜单管理云函数
   - 数据库：菜单表设计

3. **关键风险**
   - 菜单数据量大时的性能
   - 分类和搜索的效率
   - 缓存策略

建议先从基础功能开始，逐步优化。"""
    },
    {
        "name": "💻 通义千问",
        "role": "代码工程师",
        "color": "#FF9800",
        "thinking": "设计前端代码架构和实现细节...",
        "response": """【通义千问的代码设计】

好的，我来设计菜单浏览的代码架构。

**前端页面结构：**

```javascript
// pages/menu/index.js
Page({
  data: {
    categories: [],
    menus: [],
    selectedCategory: 'all',
    searchText: '',
    loading: false
  },
  
  onLoad() {
    this.loadCategories()
    this.loadMenus()
  },
  
  loadCategories() {
    wx.cloud.callFunction({
      name: 'menuMgr',
      data: { action: 'getCategories' },
      success: (res) => {
        this.setData({ categories: res.result.data })
      }
    })
  },
  
  loadMenus() {
    this.setData({ loading: true })
    wx.cloud.callFunction({
      name: 'menuMgr',
      data: { 
        action: 'getMenus',
        category: this.data.selectedCategory,
        search: this.data.searchText
      },
      success: (res) => {
        this.setData({ 
          menus: res.result.data,
          loading: false 
        })
      }
    })
  },
  
  onCategoryChange(e) {
    this.setData({ selectedCategory: e.currentTarget.dataset.category })
    this.loadMenus()
  },
  
  onSearch(e) {
    this.setData({ searchText: e.detail })
    this.loadMenus()
  }
})
```

这是基础框架，后续可以优化。"""
    },
    {
        "name": "📱 智谱GLM",
        "role": "产品经理",
        "color": "#4CAF50",
        "thinking": "思考用户体验和产品设计...",
        "response": """【智谱GLM的产品建议】

从产品角度，我补充一些用户体验的考虑：

**用户体验设计：**

1. **分类展示**
   - 横向滚动分类标签
   - 当前分类高亮显示
   - 支持"全部"分类

2. **菜品卡片**
   - 展示菜品图片、名称、价格
   - 支持快速加入购物车
   - 显示菜品评分和销量

3. **搜索功能**
   - 实时搜索建议
   - 搜索历史记录
   - 清空搜索按钮

4. **加载状态**
   - 骨架屏加载
   - 下拉刷新
   - 上拉加载更多

这样用户体验会更好。"""
    },
    {
        "name": "🏗️ DeepSeek",
        "role": "技术架构师",
        "color": "#2196F3",
        "thinking": "设计系统架构和数据库结构...",
        "response": """【DeepSeek的架构设计】

从架构角度，我设计数据库和云函数：

**数据库设计：**

```javascript
// 菜单表结构
{
  _id: "xxx",
  shopId: "shop123",
  name: "红烧肉",
  description: "精选五花肉，红烧入味",
  price: 28.8,
  category: "荤菜",
  image: "cloud://xxx.jpg",
  rating: 4.8,
  sales: 1250,
  status: "active",
  createTime: Date,
  updateTime: Date
}

// 分类表结构
{
  _id: "xxx",
  shopId: "shop123",
  name: "荤菜",
  order: 1,
  icon: "🍖"
}
```

**云函数接口：**

```javascript
// menuMgr 云函数
exports.main = async (event) => {
  const { action } = event
  
  switch(action) {
    case 'getCategories':
      // 返回分类列表
      break
    case 'getMenus':
      // 返回菜单列表（支持分类和搜索）
      break
    case 'getMenuDetail':
      // 返回菜品详情
      break
  }
}
```

这样架构清晰，易于扩展。"""
    },
    {
        "name": "🧠 DeepSeek-671B",
        "role": "技术领袖",
        "color": "#9C27B0",
        "thinking": "思考性能优化和深层技术问题...",
        "response": """【DeepSeek-671B的深度优化】

我从技术深度补充一些优化建议：

**性能优化策略：**

1. **缓存机制**
   - 分类数据缓存（1小时）
   - 菜单列表缓存（30分钟）
   - 搜索结果缓存

2. **数据库优化**
   - 在 category 字段建立索引
   - 在 shopId 字段建立索引
   - 在 name 字段建立全文索引

3. **API 优化**
   - 分页加载（每页20条）
   - 只返回必要字段
   - 使用 CDN 加速图片

4. **前端优化**
   - 虚拟列表渲染
   - 图片懒加载
   - 防抖搜索

这样可以支持大规模菜单数据。"""
    },
    {
        "name": "🤖 Claude助手",
        "role": "代码优化师",
        "color": "#00BCD4",
        "thinking": "整合所有建议，生成最终生产级代码...",
        "response": """【Claude的最终整合方案】

我来整合所有建议，生成最终的生产级代码：

**最终代码方案：**

```javascript
// pages/menu/index.js - 完整版本
Page({
  data: {
    categories: [],
    menus: [],
    selectedCategory: 'all',
    searchText: '',
    loading: false,
    page: 1,
    pageSize: 20,
    hasMore: true,
    categoryCache: null,
    cacheTTL: 3600000 // 1小时
  },
  
  onLoad() {
    this.loadCategories()
    this.loadMenus()
  },
  
  async loadCategories() {
    try {
      // 检查缓存
      const cached = wx.getStorageSync('categories_cache')
      if (cached && Date.now() - cached.time < this.data.cacheTTL) {
        this.setData({ categories: cached.data })
        return
      }
      
      // 调用云函数
      const res = await wx.cloud.callFunction({
        name: 'menuMgr',
        data: { action: 'getCategories' }
      })
      
      // 缓存结果
      wx.setStorageSync('categories_cache', {
        data: res.result.data,
        time: Date.now()
      })
      
      this.setData({ categories: res.result.data })
    } catch (err) {
      wx.showToast({ title: '加载分类失败', icon: 'error' })
    }
  },
  
  async loadMenus(append = false) {
    try {
      this.setData({ loading: true })
      
      const res = await wx.cloud.callFunction({
        name: 'menuMgr',
        data: {
          action: 'getMenus',
          category: this.data.selectedCategory,
          search: this.data.searchText,
          page: this.data.page,
          pageSize: this.data.pageSize
        }
      })
      
      const newMenus = append 
        ? [...this.data.menus, ...res.result.data]
        : res.result.data
      
      this.setData({
        menus: newMenus,
        loading: false,
        hasMore: res.result.data.length === this.data.pageSize
      })
    } catch (err) {
      wx.showToast({ title: '加载菜单失败', icon: 'error' })
      this.setData({ loading: false })
    }
  },
  
  onCategoryChange(e) {
    const category = e.currentTarget.dataset.category
    this.setData({ 
      selectedCategory: category,
      page: 1,
      menus: []
    })
    this.loadMenus()
  },
  
  onSearch(e) {
    this.setData({ 
      searchText: e.detail,
      page: 1,
      menus: []
    })
    // 防抖搜索
    clearTimeout(this.searchTimer)
    this.searchTimer = setTimeout(() => {
      this.loadMenus()
    }, 500)
  },
  
  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.setData({ page: this.data.page + 1 })
      this.loadMenus(true)
    }
  }
})
```

**关键特性：**
- ✅ 缓存机制（分类数据）
- ✅ 分页加载（支持上拉加载更多）
- ✅ 防抖搜索（避免频繁请求）
- ✅ 错误处理（用户提示）
- ✅ 性能优化（虚拟列表就绪）

这是生产级别的代码，可以直接使用。"""
    }
]

st.set_page_config(page_title="AI 6人开发团队", page_icon="🧩", layout="wide")

# 初始化 session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_discussing" not in st.session_state:
    st.session_state.is_discussing = False
if "current_speaker_idx" not in st.session_state:
    st.session_state.current_speaker_idx = -1

# ===== 代码提取和保存函数 =====
def extract_code_blocks(content):
    """从文本中提取所有代码块"""
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return [(lang or 'text', code.strip()) for lang, code in matches if code.strip()]

def save_code_to_project(code, lang, topic):
    """将代码保存到项目"""
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

# ===== 标题 =====
st.markdown("<h1 style='text-align: center;'>🧩 订餐小程序 · 6人AI专家团队</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(0,0,0,0.6); font-size: 14px;'>完全透明版本 · 看清每个AI的思考过程</p>", unsafe_allow_html=True)

# ===== 侧边栏 =====
with st.sidebar:
    st.markdown("### 🎭 团队成员")
    for member in TEAM:
        st.markdown(f"**{member['name']}** - {member['role']}")
    
    st.markdown("---")
    st.markdown("### 📂 代码输出")
    st.markdown(f"`{PROJECT_ROOT}`")

# ===== 主界面 =====
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("💬 输入讨论主题", placeholder="如：开发菜单浏览功能，支持分类筛选")
with col2:
    rounds = st.slider("轮次", 3, 6, 6)

# ===== 讨论进度 =====
if st.session_state.messages or st.session_state.is_discussing:
    st.markdown("---")
    progress = len(st.session_state.messages) / rounds
    st.markdown(f"### 📊 进度：{len(st.session_state.messages)}/{rounds} 轮")
    st.progress(min(progress, 1.0))

# ===== 讨论逻辑 =====
if st.button("🚀 开始讨论", type="primary", disabled=st.session_state.is_discussing) and topic:
    st.session_state.messages = []
    st.session_state.is_discussing = True
    st.session_state.current_speaker_idx = 0
    st.rerun()

if st.session_state.is_discussing and topic:
    if len(st.session_state.messages) < rounds:
        speaker_idx = len(st.session_state.messages) % len(TEAM)
        member = TEAM[speaker_idx]
        
        # 显示思考过程
        st.markdown("---")
        st.markdown(f"### 🧠 {member['name']} 正在思考...")
        
        # 显示思考内容
        thinking_placeholder = st.empty()
        thinking_placeholder.info(f"💭 {member['thinking']}")
        
        # 模拟思考延迟
        time.sleep(2)
        
        # 清除思考提示
        thinking_placeholder.empty()
        
        # 添加消息
        st.session_state.messages.append({
            "name": member['name'],
            "role": member['role'],
            "color": member['color'],
            "thinking": member['thinking'],
            "response": member['response']
        })
        
        st.rerun()
    else:
        st.session_state.is_discussing = False
        st.balloons()
        st.success("🎉 讨论完成！")

# ===== 显示对话 =====
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💬 完整对话记录")
    
    for idx, msg in enumerate(st.session_state.messages, 1):
        code_blocks = extract_code_blocks(msg['response'])
        code_count = len(code_blocks)
        
        # 创建可展开的对话框
        with st.expander(f"**第{idx}轮** · {msg['name']} ({msg['role']})" + (f" · 📝 {code_count}个代码块" if code_count > 0 else ""), expanded=(idx == len(st.session_state.messages))):
            # 显示思考过程
            st.markdown(f"**💭 思考过程：** {msg['thinking']}")
            st.markdown("---")
            
            # 显示完整回复
            st.markdown(f"**📝 完整回复：**")
            st.markdown(msg['response'])
            
            # 显示代码块
            if code_blocks:
                st.markdown("---")
                st.markdown("#### 📝 代码块")
                for i, (lang, code) in enumerate(code_blocks, 1):
                    with st.expander(f"代码 {i} ({lang})"):
                        st.code(code, language=lang)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"💾 保存代码 {i}", key=f"save_{idx}_{i}"):
                                result = save_code_to_project(code, lang, topic)
                                if result[2]:
                                    st.success(f"{result[0]}: {result[1]}")
                                else:
                                    st.error(f"{result[0]}: {result[1]}")
                        with col2:
                            if st.button(f"📋 复制代码 {i}", key=f"copy_{idx}_{i}"):
                                st.info("代码已复制（请手动复制）")

# ===== 讨论结束 =====
if st.session_state.messages and len(st.session_state.messages) >= rounds and not st.session_state.is_discussing:
    st.markdown("---")
    st.markdown("### 📊 讨论统计")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💬 发言数", len(st.session_state.messages))
    with col2:
        st.metric("👥 参与者", len(TEAM))
    with col3:
        code_count = sum(len(extract_code_blocks(msg['response'])) for msg in st.session_state.messages)
        st.metric("💻 代码块", code_count)
    
    # 自动保存
    st.markdown("---")
    st.markdown("### 💻 代码自动落地")
    
    all_results = []
    for msg in st.session_state.messages:
        code_blocks = extract_code_blocks(msg['response'])
        for lang, code in code_blocks:
            if len(code) > 50:
                result = save_code_to_project(code, lang, topic)
                if result[2]:
                    all_results.append(result)
    
    if all_results:
        st.success(f"✅ 已自动保存 {len(all_results)} 个文件到项目")
        for label, path in all_results:
            st.markdown(f"- **{label}**: `{path}`")
    else:
        st.info("📭 本次讨论中未发现可落地的代码")

# ===== 清空 =====
if st.button("🗑️ 清空讨论", disabled=st.session_state.is_discussing):
    st.session_state.messages = []
    st.session_state.is_discussing = False
    st.session_state.current_speaker_idx = -1
    st.rerun()
