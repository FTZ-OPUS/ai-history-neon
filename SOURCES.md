# 素材与史实

本片为 1920×1080 横屏。所有神经网络、棋盘、注意力热图、公式与界面元素均由本项目代码绘制；音效与人声之外的音乐为程序合成。外部图片只有两类：Wikimedia Commons 的历史照片，以及项目作者提供的三张拟人插画。

## 历史照片

六张图均已裁切为圆形并做过轻度调色。逐张的作者、许可、原图详情链接见 [`assets/attribution.json`](assets/attribution.json)。

| 用途 | 文件 | 许可 |
|---|---|---|
| 1950 图灵 | `assets/turing.png` | Public domain（Elliott & Fry, 1951） |
| 1956 达特茅斯 | `assets/mccarthy.png` | CC BY 2.0 |
| 1958 感知机 | `assets/rosenblatt.png` | CC BY-SA 4.0 |
| 1997 深蓝 | `assets/deepblue.png` | CC BY 2.0 |
| 2012 深度学习 | `assets/hinton.png` | CC BY-SA 4.0 |
| 2016 人机对局 | `assets/leedol.png` | CC BY 2.0 |

使用 CC BY / CC BY-SA 图片时需保留署名；二次发布前请回到原图页面核对最新授权条件。

## 史实线索

- 1950 图灵《Computing Machinery and Intelligence》提出 imitation game：<https://academic.oup.com/mind/article/LIX/236/433/986238>
- 1956 达特茅斯夏季人工智能研究计划（1955 年提案首次使用 artificial intelligence 一词）：<https://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html>
- 1958 Rosenblatt 感知机论文：<https://pubmed.ncbi.nlm.nih.gov/13602029/>
- 1986 Rumelhart / Hinton / Williams 反向传播论文：<https://www.nature.com/articles/323533a0>
- 1997 IBM 深蓝战胜卡斯帕罗夫：<https://www.ibm.com/history/deep-blue>
- 2012 AlexNet / ImageNet 论文：<https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks>
- 2016 AlphaGo 与李世石 4:1 对局：<https://deepmind.google/discover/blog/alphago-the-story-so-far/>
- 2017 Transformer / Attention Is All You Need：<https://arxiv.org/abs/1706.03762>
- 2022 ChatGPT 公开发布：<https://openai.com/index/chatgpt/>
- 2026 Claude Opus 5.5 官方介绍（长时编码、代理与知识工作）：<https://www.anthropic.com/claude-opus-5-5>
- 2026 GPT-6 Astra 官方介绍（电脑操作、软件工程、科研等）：<https://openai.com/index/gpt-6-astra/>
- 2026 DeepSeek V4.1 Flash 官方中文介绍（视觉、MoE、缓存优化）：<https://www.deepseek.com/zh/news/deepseek-v4-1-flash>

## 公式口径

片中出现的公式是**教学示意**，用于解释通用机制：

- 感知机激活 `y = σ(w·x + b)`
- `ReLU(z) = max(0, z)`
- 梯度下降 `w ← w − η·∂L/∂w`
- 反向传播的链式法则 `∂L/∂w₁ = (∂L/∂h)·(∂h/∂w₁)`
- 缩放点积注意力 `Attention(Q,K,V) = softmax(QKᵀ/√dₖ)·V`
- 稀疏专家路由 `y = Σ_{i∈TopK(x)} gᵢ(x)·Eᵢ(x)`

它们不暗示 2026 各家模型内部公开了完全相同的具体实现。

## 需要澄清的两处

- **DeepSeek 的型号名**：官方产品名是 **V4.1 Flash**；部分第三方站点写作「V4.1 Flash 1017」，那是 10 月 17 日的版本标识，厂商介绍页并未以此命名，因此片中采用官方名称。
- **2026 三家能力**：OpenAI 官方为 GPT-6 Astra，Anthropic 为 Claude Opus 5.5；三家描述均采用厂商公开的应用定位（长时编码代理 / 电脑操作与科研 / 视觉与高效推理），不代表本片独立实测或统一评测排名。

## 概念可视化的边界

片中的神经网络、AI 寒冬、注意力热图都是概念示意，不是真实设备运行记录。「AI 冬天」用年代区间呈现，不暗示史上只有一次寒冬。图灵 1951 年肖像用于 1950 章节、麦卡锡 2006 年肖像用于 1956 章节、辛顿 2024 年肖像用于 2012 章节，均为人物识别照，并非历史现场摄影。

## 角色插画

- 三张拟人插画由项目作者提供：DeepSeek（鲸鱼女仆）、Claude（白橙裙读书少女）、GPT（白发龙角少女）。版权与原始作者以作者提供的来源为准。
- DeepSeek 原图顶部的中文标语与左下角水印已裁掉；三张图的白底均按「只删与画面边缘连通的近白像素」方式去除，白色服装得以保留。
- 处理脚本：[`assets/characters/process_characters.py`](assets/characters/process_characters.py)（原图在 `assets/characters/raw/`）。
- 角色只承担拟人化代言的叙事功能，不代表官方形象或官方授权。

## 配音与音轨

成片含中文旁白（晓伊音色）与程序合成的氛围音乐：人声 loudnorm 到 −16 LUFS，音乐压到 0.22 后混合，画面流不重编码。分幕秒表见 [`timeline_v2.json`](timeline_v2.json)。
