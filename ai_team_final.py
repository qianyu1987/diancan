import streamlit as st
import time
import os
import re
from datetime import datetime

# 配置
PROJECT_ROOT = r"D:\dingcan"
MINIPROGRAM_PAGES = os.path.join(PROJECT_ROOT, "miniprogram", "pages")
CLOUDFUNCTIONS_DIR = os.path.join(PROJECT_ROOT, "cloudfunctions")

# 6个模型
SPEAKERS = ["🎯 豆包", "💻 通义千问", "📱 智谱GLM", "🏗️ DeepSeek", "🧠 DeepSeek-671B", "🤖 Claude助手"]
ROLES = ["全局军师", "代码工程师", "产品经理", "技术架构师", "技术领袖", "代码优化师"]

# 模拟回复
MOCK_RESPONSES = {
    "🎯 豆包": "这个需求很有意思。从全局角度分析，菜单浏览是订餐系统的基础功能。需要支持分类筛选和搜索。关键风险是菜单数据量大时的性能。建议先从基础功能开始，逐步优化。",
    
    "💻 通义千问": """好的，我来设计菜单浏览的代码架构。

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
  }
})
```

这是基础框架，后续可以优化。""",
    
    "📱 智谱GLM": "从产品角度，我补充一些用户体验的考虑。分类展示应该支持横向滚动，当前分类高亮显示。菜品卡片需要展示图片、名称、价格，支持快速加入购物车。搜索功能应该有实时建议和搜索历史。这样用户体验会更好。",
    
    "🏗️ DeepSeek": """从架构角度，我设计数据库和云函数：

```javascript
// 菜单表结构
{
  _id: "xxx",
  shopId: "shop123",
  name: "红烧肉",
  price: 28.8,
  category: "荤菜",
  image: "cloud://xxx.jpg",
  rating: 4.8,
  sales: 1250,
  status: "active",
  createTime: Date,
  updateTime: Date
}

// 云函数接口
exports.main = async (event) => {
  const { action } = event
  switch(action) {
    case 'getCategories':
      // 返回分类列表
      break
    case 'getMenus':
      // 返回菜单列表
      break
  }
}
```

这样架构清晰，易于扩展。""",
    
    "🧠 DeepSeek-671B": "我从技术深度补充一些优化建议。分类数据应该缓存1小时，菜单列表缓存30分钟。在category和shopId字段建立索引。前端使用虚拟列表渲染，图片懒加载。搜索应该防抖处理。这样可以支持大规模菜单数据。",
    
    "🤖 Claude助手": """我来整合所有建议，生成最终的生产级代码：

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
    hasMore: true
  },
  
  onLoad() {
    this.loadCategories()
    this.loadMenus()
  },
  
  async loadCategories() {
    try {
      const cached = wx.getStorageSync('categories_cache')
      if (cached && Date.now() - cached.time < 3600000) {
        this.setData({ categories: cached.data })
        return
      }
      
      const res = await wx.cloud.callFunction({
        name: 'menuMgr',
        data: { action: 'getCategories' }
      })
      
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

这是生产级别的代码，包含缓存、分页、防抖、错误处理等所有最佳实践。"""
}

st.set_page_config(page_title="AI 6人开发团队", page_icon="🧩", layout="wide")

# 初始化 session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_discussing" not in st.session_state:
    st.session_state.is_discussing = False

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
st.markdown("<p style='text-align: center; color: rgba(0,0,0,0.6); font-size: 16px;'>演示版本 · 代码自动落地</p>", unsafe_allow_html=True)

# ===== 侧边栏 =====
with st.sidebar:
    st.markdown("### 🎭 团队成员")
    for i, speaker in enumerate(SPEAKERS):
        st.markdown(f"**{speaker}** - {ROLES[i]}")
    
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
    st.rerun()

if st.session_state.is_discussing and topic:
    if len(st.session_state.messages) < rounds:
        speaker_idx = len(st.session_state.messages) % len(SPEAKERS)
        speaker = SPEAKERS[speaker_idx]
        role = ROLES[speaker_idx]
        
        # 显示正在思考
        with st.spinner(f"🧠 {speaker} 正在思考..."):
            time.sleep(2)
            
            # 获取回复
            content = MOCK_RESPONSES.get(speaker, f"我是{speaker}，关于{topic}的看法...")
            
            st.session_state.messages.append({
                "speaker": speaker,
                "role": role,
                "content": content
            })
        
        st.rerun()
    else:
        st.session_state.is_discussing = False
        st.balloons()
        st.success("🎉 讨论完成！")

# ===== 显示对话 =====
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💬 对话记录")
    
    for idx, msg in enumerate(st.session_state.messages, 1):
        code_blocks = extract_code_blocks(msg['content'])
        code_count = len(code_blocks)
        
        with st.expander(f"**第{idx}轮** · {msg['speaker']} ({msg['role']})" + (f" · 📝 {code_count}个代码块" if code_count > 0 else ""), expanded=(idx == len(st.session_state.messages))):
            st.markdown(msg['content'])
            
            # 显示代码块
            if code_blocks:
                st.markdown("#### 📝 代码块")
                for i, (lang, code) in enumerate(code_blocks, 1):
                    with st.expander(f"代码 {i} ({lang})"):
                        st.code(code, language=lang)
                        
                        if st.button(f"💾 保存", key=f"save_{idx}_{i}"):
                            result = save_code_to_project(code, lang, topic)
                            if result[2]:
                                st.success(f"{result[0]}: {result[1]}")
                            else:
                                st.error(f"{result[0]}: {result[1]}")

# ===== 讨论结束 =====
if st.session_state.messages and len(st.session_state.messages) >= rounds and not st.session_state.is_discussing:
    st.markdown("---")
    st.markdown("### 📊 统计")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("发言数", len(st.session_state.messages))
    with col2:
        st.metric("参与者", len(SPEAKERS))
    with col3:
        code_count = sum(len(extract_code_blocks(msg['content'])) for msg in st.session_state.messages)
        st.metric("代码块", code_count)
    
    # 自动保存
    st.markdown("---")
    st.markdown("### 💻 代码落地")
    
    all_results = []
    for msg in st.session_state.messages:
        code_blocks = extract_code_blocks(msg['content'])
        for lang, code in code_blocks:
            if len(code) > 50:
                result = save_code_to_project(code, lang, topic)
                if result[2]:
                    all_results.append(result)
    
    if all_results:
        st.success(f"✅ 已保存 {len(all_results)} 个文件")
        for label, path in all_results:
            st.markdown(f"- {label}: `{path}`")

# ===== 清空 =====
if st.button("🗑️ 清空", disabled=st.session_state.is_discussing):
    st.session_state.messages = []
    st.session_state.is_discussing = False
    st.rerun()
