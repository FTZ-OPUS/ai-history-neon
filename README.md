# AI 史诗 · 霓虹知识短片

> 从图灵的一个提问，到 2026 年的三家前沿模型。
> **21 幕 / 2 分 46 秒 / 1920×1080**，全部画面由 Manim 用代码逐帧绘制，没有用剪辑软件。

![封面](preview/poster.jpg)

**[▶ 观看压缩版预览](preview/preview-1080p30.mp4)**（9 MB，1080p30，含中文旁白）

---

## 这条片子讲了什么

一条暗底荧光的横屏知识短片，把 AI 七十多年压进两分半：历史事件与技术原理交替推进，每个关键原理都配一条公式和一段动态演示，最后落到 2026 年的三家模型。

不是 PPT 式的文字罗列——每屏只讲一件事，讲完即转场：

- **历史线**：图灵 → 达特茅斯 → 感知机 → 第一次寒冬 → 反向传播 → 深蓝 → AlexNet → AlphaGo → Transformer → ChatGPT
- **原理线**（穿插其中，配公式）：`y=σ(w·x+b)`、`ReLU`、`w←w−η∂L/∂w`、链式法则、缩放点积注意力、稀疏专家路由
- **2026 线**：Claude Opus 5.5 / GPT-6 Astra / DeepSeek V4.1 Flash，各一幕，收在「别急着问谁最强」

## 分幕表（21 幕 · 166.08 秒）

| # | 场景类 | 起 | 时长 | 内容 |
|---|---|---|---|---|
| 1 | `S00_Prologue` | 0.0 | 6.4 | 开场：三重霓虹光环 + 主标题 |
| 2 | `S01_Turing` | 6.4 | 6.1 | 1950 图灵与「模仿游戏」 |
| 3 | `S02_Dartmouth` | 12.5 | 5.5 | 1956 达特茅斯，学科得名 |
| 4 | `S03_Perceptron` | 18.0 | 8.5 | 1958 感知机 + 激活公式 |
| 5 | `S03b_Activation` | 26.5 | 10.8 | 原理①：ReLU 折线，动点实时滑过 |
| 6 | `S04_Winter` | 37.3 | 5.6 | AI 寒冬，研究并未停下 |
| 7 | `S05_Backprop` | 42.8 | 8.2 | 1986 反向传播 + 梯度下降 |
| 8 | `S05b_ChainRule` | 51.0 | 10.0 | 原理②：链式法则，误差倒流回输入 |
| 9 | `S06_DeepBlue` | 61.0 | 5.6 | 1997 深蓝 |
| 10 | `S07_ImageNet` | 66.6 | 6.0 | 2012 AlexNet，机器开始「看见」 |
| 11 | `S08_AlphaGo` | 72.5 | 6.1 | 2016 AlphaGo 与李世石 |
| 12 | `S09_Transformer` | 78.7 | 7.4 | 2017 注意力机制 |
| 13 | `S09b_AttentionMap` | 86.1 | 9.1 | 原理③：注意力热图 + `softmax(QKᵀ/√dₖ)V` |
| 14 | `S10_Generative` | 95.1 | 5.5 | 2022 ChatGPT 走向大众 |
| 15 | `S10b_Leap` | 100.6 | 9.5 | 2023–2025：多模态 → 长上下文 → 推理与代理 |
| 16 | `S11a_Cast` | 110.1 | 8.7 | 三位拟人主角同台 |
| 17 | `S12_Claude` | 118.8 | 10.4 | Claude Opus 5.5：长时编码与代理 |
| 18 | `S13_Astra` | 129.2 | 10.4 | GPT-6 Astra：在软件环境里行动 |
| 19 | `S14_DeepSeek` | 139.6 | 10.4 | DeepSeek V4.1 Flash：稀疏 MoE 与效率 |
| 20 | `S15_Compare` | 150.0 | 7.9 | 三条赛道，一把尺子量不出全部 |
| 21 | `S11_Finale` | 157.9 | 8.2 | 终章：下一章由我们共同决定 |

## 目录结构

```
.
├── ai_history.py              # 全部 21 幕动画（单文件，约 700 行）
├── render_film.py             # 逐幕渲染 → 拼接 → 合成音轨 → 混音
├── fetch_assets.py            # 从 Wikimedia 拉历史照片并做圆形裁切
├── audit_layout.py            # 干跑版面自检：文字越界 / 重叠
├── timeline_v2.json           # 分幕秒表（渲染后自动生成）
├── SOURCES.md                 # 史实链接、图片署名、口径说明
├── preview/                   # 封面图 + 压缩版预览
└── assets/
    ├── *.png                  # 6 张历史照片（已圆形裁切、调色）
    ├── attribution.json        # 作者 / 许可 / 原图链接
    └── characters/             # 3 张拟人角色透明图 + 原图 + 去背脚本
```

## 环境与运行

需要 **Manim Community v0.21**、MacTeX、ffmpeg。本项目在 Apple Silicon + macOS 上验证。

```bash
# 依赖（示例）
python3 -m venv ~/venvs/manim && ~/venvs/manim/bin/pip install manim scipy pillow requests

# 整片渲染（1080p60，逐幕渲染后自动拼接并合成音轨）
~/venvs/manim/bin/python render_film.py --rebuild

# 只渲染还没渲染过的场景
~/venvs/manim/bin/python render_film.py

# 快速预览（1080p15，用来验观感）
~/venvs/manim/bin/python render_film.py --preview --rebuild

# 版面自检：EDGE 与 OVL 都应为 0
~/venvs/manim/bin/python audit_layout.py ai_history.py --prefix S
```

`render_film.py` 里的 `MANIM` / `FFMPEG` / `FFPROBE` 三个路径按本机环境改一下即可，其余路径都用相对定位。

## 视觉系统（想复用可以直接抄）

整片只有一个自建的视觉层，都写在 `ai_history.py` 顶部的辅助函数里：

| 函数 | 作用 |
|---|---|
| `glow(mob, color)` | 三层描边副本 + 实体，模拟荧光灯管的辉光 |
| `line(a, b, color, w)` | 同上的线段版，用于网络连接 |
| `ring(r, color)` | 五层同心圆，做光环与轨道 |
| `spark(p, color)` | 四层同心圆点，做信号脉冲 |
| `character_aura(w, h, color)` | 三层椭圆光晕，让抠图角色坐在光里而不是贴在黑底上 |
| `Film.clear(color)` | 整页淡出 + 一道横扫亮线，作为统一转场 |

配色固定为：底色 `#0F1720`、正文 `#F6F2EA`、注释 `#A9B4C2`，主色青 `#35E7FF`、金 `#FFE14D`、粉 `#FF4FD8`、绿 `#5CFFB0`、紫 `#A98BFF`。

字体用 macOS 自带 `Kaiti SC`（楷体）；所有公式走 `MathTex`，中文一律 `Text`，两者用 `VGroup` 混排——**绝不在 MathTex 里写中文**。

## 复刻时会踩的坑（都已在代码里处理）

1. **Manim 的批量删除保护**：每编译一次公式都会清理 `.aux/.log/.dvi`，一部片子上千次删除会撞上沙箱的删除配额，进程「成功退出」但什么都没渲染。`ai_history.py` 里两行配置解决：`config["no_latex_cleanup"]=True`、`config["max_files_cached"]=1000000`。
2. **文字 SVG 的临时文件**：Manim 解析完文字会立刻 `unlink` 临时 SVG，累计同样会撞配额。本项目在文件开头把 `media/texts` 下的这类临时文件保留下来（`Path.unlink` 局部替换），不改 Manim 安装本身。
3. **白底插画去背不能全局抠白**：角色有白裙子、白头发，全局抠会连衣服一起吃掉。`assets/characters/process_characters.py` 改成「只删与画面边缘连通的近白像素」，去背后再腐蚀 1px + 羽化 1.4px，避免深底上出现白边。
4. **长年份标签会越界**：`tag()` 里对年份做了 `scale_to_fit_width(2.5)`，否则 `1970s—80s` 这种会捅出左边界。
5. **时长校准**：`Film.wait` 被统一乘了一个系数（本项目 2.25），只拉长停留、不动动画 `run_time`，一个数字就能整体调片长。

## 素材与版权

历史照片来自 Wikimedia Commons（图灵为公有领域，其余为 CC BY / CC BY-SA），逐张的作者、许可与原始链接见 **[SOURCES.md](SOURCES.md)** 与 `assets/attribution.json`。

三张角色插画由项目作者提供，本仓库仅做去背、裁切与缩放，未修改画风。片中角色只承担拟人化代言的叙事功能，不代表官方形象或官方授权。

## 说明

- 片中 2026 年三家模型的能力描述均取自各厂商公开介绍，不做统一评测排名；`DeepSeek` 的官方产品名是 **V4.1 Flash**，部分第三方站点写作「1017」，那是版本日期标识。
- 公式是教学示意，用于解释通用机制，不暗示各厂商内部实现完全相同。
- 仓库内的预览视频为压缩版（1080p30 / CRF24）。原始成片为 1080p60。
