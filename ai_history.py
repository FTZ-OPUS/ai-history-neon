"""AI史诗 · 从一个问题到一个时代. Manim CE 0.21; 16:9 neon historical film."""
from pathlib import Path
import numpy as np
from manim import *

# Manim parses modified text SVGs and normally unlinks them immediately.
# Keep only those project-local temporary SVGs to avoid sandbox bulk-delete limits.
_original_unlink = Path.unlink

def _keep_text_svg(self, *args, **kwargs):
    if self.parent.name == "texts" and self.name.endswith("_.svg"):
        return None
    return _original_unlink(self, *args, **kwargs)

Path.unlink = _keep_text_svg

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.no_latex_cleanup = True
config.max_files_cached = 1000000

ROOT = Path(__file__).resolve().parent
BG, INK, DIM = "#0F1720", "#F6F2EA", "#A9B4C2"
CYAN, GOLD, PINK, GREEN, VIOLET, ORANGE = "#35E7FF", "#FFE14D", "#FF4FD8", "#5CFFB0", "#A98BFF", "#FF9F43"
WHALE, CLAUDE_C, DRAGON = "#4FA8FF", "#FF8B4A", "#B9A6FF"
FONT = "Kaiti SC"


def character_aura(w, h, color):
    """Layered ellipse glow so a cut-out figure sits in light instead of on a white card."""
    return VGroup(*[Ellipse(width=w*k, height=h*k2, stroke_width=0, fill_color=color).set_opacity(o)
                    for k, k2, o in [(1.7,1.4,.04),(1.42,1.22,.055),(1.15,1.07,.07)]])


def txt(s, size=40, color=INK, bold=False):
    return Text(s, font=FONT, font_size=size, color=color, weight=BOLD if bold else NORMAL)


def glow(mob, color=CYAN):
    return VGroup(mob.copy().set_stroke(color, width=24, opacity=.09),
                  mob.copy().set_stroke(color, width=12, opacity=.18), mob)


def line(a, b, color=CYAN, width=3):
    base = Line(a, b)
    return VGroup(base.copy().set_stroke(color, width=19, opacity=.07),
                  base.copy().set_stroke(color, width=9, opacity=.19),
                  base.set_stroke(color, width=width, opacity=.95))


def ring(radius, color=CYAN, center=ORIGIN, width=4):
    return VGroup(*[Circle(radius=radius).move_to(center).set_stroke(color, width=w, opacity=o)
                    for w, o in [(46,.025),(30,.055),(18,.10),(10,.24),(width,1)]])


def spark(p, color=CYAN, r=.075):
    return VGroup(Dot(p, radius=r*3.8, color=color, fill_opacity=.05),
                  Dot(p, radius=r*2.3, color=color, fill_opacity=.15),
                  Dot(p, radius=r, color=color), Dot(p, radius=r*.35, color=WHITE))


class Film(Scene):
    def setup(self):
        self.camera.background_color = BG
        self.back = VGroup()
        rng = np.random.default_rng(138)
        for _ in range(90):
            x, y = rng.uniform(-7.9,7.9), rng.uniform(-4.4,4.4)
            self.back.add(Dot([x,y,0], radius=rng.uniform(.009,.022), color=CYAN).set_opacity(rng.uniform(.08,.32)))
        self.add(self.back)

    def wait(self, duration=1.0, **kwargs):
        return super().wait(duration * 2.25, **kwargs)

    def formula(self, latex, y=1.4, color=GOLD, size=65):
        equation = glow(MathTex(latex, font_size=size, color=color), color)
        equation.move_to([0, y, 0])
        if equation.width > 13.8:
            equation.scale_to_fit_width(13.8)
        self.play(FadeIn(equation, scale=1.14), run_time=.9)
        return equation

    def tag(self, year, title, color=CYAN):
        yr = glow(txt(str(year), 47, color, True), color)
        if yr.width > 2.5:
            yr.scale_to_fit_width(2.5)
        yr.move_to([-6.35, 3.75, 0])
        name = txt(title, 47, INK, True)
        if name.width > 11.6:
            name.scale_to_fit_width(11.6)
        name.move_to([1.45, 3.75, 0])
        self.play(FadeIn(yr, shift=RIGHT*.2), FadeIn(name, shift=UP*.12), run_time=.65)

    def caption(self, content, color=INK):
        t = txt(content, 38, color, True)
        if t.width > 13.5: t.scale_to_fit_width(13.5)
        t.move_to([0,-3.65,0])
        self.play(FadeIn(t, shift=UP*.16), run_time=.5)
        return t

    def photo(self, key, x=-4.5, y=.25, h=4.4, color=CYAN):
        im = ImageMobject(str(ROOT / 'assets' / f'{key}.png')).set_height(h).move_to([x,y,0])
        circle = ring(h*.48, color, im.get_center(), 3)
        self.play(FadeIn(im, scale=.82), FadeIn(circle), run_time=.9)
        return im, circle

    def character(self, key, x=-5.0, y=-.25, h=4.7, w=4.9, color=CYAN):
        im = ImageMobject(str(ROOT / 'assets' / 'characters' / f'{key}.png'))
        im.set_height(h)
        if im.width > w:
            im.set_width(w)
        im.move_to([x, y, 0])
        aura = character_aura(im.width, im.height, color).move_to(im.get_center())
        orbit = ring(max(im.width, im.height) * .58, color, im.get_center(), 2)
        orbit.set_opacity(.55)
        self.play(FadeIn(aura), FadeIn(orbit), run_time=.7)
        self.play(FadeIn(im, shift=RIGHT * .35, scale=1.04), run_time=.95)
        return im, orbit

    def clear(self, color=CYAN):
        incoming = [m for m in self.mobjects if m is not self.back]
        self.play(*[FadeOut(m, scale=.95) for m in incoming], run_time=.46)
        sweep = Rectangle(width=16, height=.035, stroke_width=0, fill_color=color, fill_opacity=.8).move_to(LEFT*7.8)
        self.add(sweep)
        self.play(sweep.animate.shift(RIGHT*15.6).set_opacity(0), run_time=.23)
        self.remove(sweep)


class S00_Prologue(Film):
    def construct(self):
        rings = VGroup(*[ring(r, c, width=2) for r,c in [(1.0,CYAN),(2.0,PINK),(3.0,GOLD)]])
        rings.scale(1.2).move_to([0,.2,0])
        self.play(*[Create(g) for g in rings], run_time=1.2)
        self.play(Rotate(rings[0], angle=PI/2), Rotate(rings[1], angle=-PI/3), run_time=.9)
        title=glow(txt('人类与人工智能', 102, GOLD, True),GOLD).move_to([0,.7,0])
        sub=txt('从一个问题，到一个时代', 47, INK, True).move_to([0,-.65,0])
        self.play(FadeIn(title,scale=1.2), run_time=.8)
        self.play(FadeIn(sub,shift=UP*.2),run_time=.55)
        self.wait(1.0)
        self.clear(GOLD)


class S01_Turing(Film):
    def construct(self):
        self.tag('1950','机器能思考吗？',GOLD)
        self.photo('turing', -4.75,.15,4.6,GOLD)
        q=glow(txt('CAN MACHINES THINK?',57,GOLD,True),GOLD).move_to([2.15,1.35,0])
        machine=VGroup(*[line([-1.0+i*.63,-1.6,0],[-1.0+i*.63,.1,0],CYAN,2) for i in range(9)])
        bits=VGroup(*[txt(str((i*7+3)%2),33,GREEN,True).move_to([-1.0+i*.63,-.7,0]) for i in range(9)])
        self.play(FadeIn(q,shift=UP*.15),run_time=.65)
        self.play(LaggedStart(*[Create(m) for m in machine],lag_ratio=.08), FadeIn(bits),run_time=.9)
        self.caption('图灵提出“模仿游戏”，把哲学问题变成实验')
        self.wait(.8); self.clear(GOLD)


class S02_Dartmouth(Film):
    def construct(self):
        self.tag('1956','一个学科，有了名字',CYAN)
        self.photo('mccarthy',-4.7,.15,4.5,CYAN)
        word=glow(txt('ARTIFICIAL\nINTELLIGENCE',70,CYAN,True),CYAN).move_to([2.3,.75,0])
        who=txt('达特茅斯夏季研讨会',39,INK).move_to([2.3,-1.45,0])
        self.play(FadeIn(word,shift=UP*.25),run_time=.7)
        self.play(FadeIn(who),run_time=.5)
        self.caption('让机器模拟学习与智能：一个大胆的研究计划')
        self.wait(.7); self.clear()


class S03_Perceptron(Film):
    def construct(self):
        self.tag('1958','感知机：让机器学会分类',PINK)
        self.photo('rosenblatt',-5,.25,4.15,PINK)
        inp=[np.array([-1.55,y,0]) for y in [1.55,.4,-.75]]
        hub=np.array([1.15,.4,0]); out=[np.array([4.0,y,0]) for y in [1.25,-.55]]
        edges=VGroup(*[line(p,hub,PINK,2) for p in inp],*[line(hub,p,CYAN,2) for p in out])
        dots=VGroup(*[spark(p,PINK,.09) for p in inp],spark(hub,GOLD,.19),*[spark(p,CYAN,.12) for p in out])
        labels=VGroup(txt('输入',31,DIM).move_to([-1.6,-1.55,0]),txt('权重',31,GOLD).move_to([1.15,-.55,0]),txt('判断',31,CYAN).move_to([4,-1.55,0]))
        self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.08),run_time=.9)
        self.play(FadeIn(dots),FadeIn(labels),run_time=.6)
        pulse=spark(inp[0],GOLD,.11)
        self.play(FadeIn(pulse),run_time=.18)
        self.play(pulse.animate.move_to(hub),run_time=.47)
        self.play(pulse.animate.move_to(out[0]),run_time=.5)
        eq=glow(MathTex(r"y=\sigma(w_1x_1+w_2x_2+w_3x_3+b)",font_size=55,color=GOLD),GOLD)
        eq.move_to([1.45,-2.55,0])
        self.play(FadeIn(eq,shift=UP*.18),run_time=.7)
        self.caption('输入乘权重，加上偏置，再经过激活函数')
        self.wait(1.05); self.clear(PINK)


class S04_Winter(Film):
    def construct(self):
        self.tag('1970s—80s','热潮退去，研究没有停下',VIOLET)
        grid=VGroup(*[line([-6.5+i*.45,-2.2,0],[-5.7+i*.45,2.15,0],VIOLET,1) for i in range(30)])
        self.play(FadeIn(grid),run_time=.7)
        broken=glow(txt('AI WINTER',92,VIOLET,True),VIOLET).move_to([0,.55,0])
        self.play(FadeIn(broken,scale=1.4),run_time=.7)
        self.play(grid.animate.set_opacity(.13),run_time=.35)
        rebirth=glow(txt('1986  反向传播',63,GREEN,True),GREEN).move_to([0,-1.25,0])
        self.play(FadeIn(rebirth,shift=RIGHT*.4),run_time=.6)
        self.caption('误差沿网络回流，多层网络重新有了学习路径')
        self.wait(.6); self.clear(GREEN)


class S05_Backprop(Film):
    def construct(self):
        self.tag('1986','神经网络，再次点亮',GREEN)
        layers=[[-5.4,-1.5,0,1.5],[-2.1,-1.65,-.45,.75,1.95],[1.2,-1.65,-.45,.75,1.95],[4.6,-.65,.9]]
        positions=[]
        for col in layers:
            x,*ys=col
            positions.append([np.array([x,y,0]) for y in ys])
        edges=VGroup(*[line(a,b,CYAN if k<2 else GREEN,1.4) for k in range(3) for a in positions[k] for b in positions[k+1]])
        nodes=VGroup(*[spark(p,[PINK,CYAN,GREEN,GOLD][k],.11) for k,col in enumerate(positions) for p in col])
        self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.008),run_time=1.15)
        self.play(FadeIn(nodes),run_time=.5)
        for col in positions:
            flash=VGroup(*[spark(p,WHITE,.12) for p in col])
            self.play(FadeIn(flash),run_time=.13)
            self.play(FadeOut(flash),run_time=.14)
        back=line([4.6,.1,0],[-5.4,.1,0],PINK,6)
        self.play(Create(back),run_time=.5)
        formula=glow(MathTex(r"w\leftarrow w-\eta\frac{\partial L}{\partial w}",font_size=63,color=GOLD),GOLD)
        formula.move_to([0,-2.62,0])
        self.play(FadeIn(formula,shift=RIGHT*.2),run_time=.8)
        self.caption('前向计算损失，反向传递误差，沿梯度更新权重')
        self.wait(1.0); self.clear(GREEN)


class S06_DeepBlue(Film):
    def construct(self):
        self.tag('1997','深蓝击败国际象棋世界冠军',GOLD)
        self.photo('deepblue',-4.7,.2,4.2,GOLD)
        board=VGroup()
        for r in range(8):
            for c in range(8):
                color=CYAN if (r+c)%2 else '#26394A'
                board.add(Square(side_length=.49, stroke_color=CYAN, stroke_width=1, fill_color=color, fill_opacity=.30 if (r+c)%2 else .55).move_to([.1+c*.49,1.72-r*.49,0]))
        self.play(LaggedStart(*[FadeIn(row) for row in board],lag_ratio=.006),run_time=.8)
        knight=glow(txt('♞',117,GOLD,True),GOLD).move_to([2,-.05,0])
        self.play(FadeIn(knight,scale=1.9),run_time=.7)
        self.caption('计算与搜索，第一次在巅峰棋局赢过人类')
        self.wait(.6); self.clear(GOLD)


class S07_ImageNet(Film):
    def construct(self):
        self.tag('2012','AlexNet：机器开始“看见”',PINK)
        self.photo('hinton',-5,.25,4.2,PINK)
        tiles=VGroup()
        rng=np.random.default_rng(19)
        colors=[CYAN,PINK,GOLD,GREEN,VIOLET]
        for i in range(7):
            for j in range(7):
                x,y=-1.5+j*.74,2.2-i*.64
                tiles.add(Square(.53,stroke_width=1.4,stroke_color=colors[(i+j)%5],fill_color=colors[(i*3+j)%5],fill_opacity=rng.uniform(.1,.35)).move_to([x,y,0]))
        self.play(LaggedStart(*[FadeIn(s,scale=.7) for s in tiles],lag_ratio=.02),run_time=1.15)
        scan=line([-1.85,2.55,0],[3.45,2.55,0],GOLD,5)
        self.add(scan)
        self.play(scan.animate.shift(DOWN*4.1),run_time=.95)
        self.remove(scan)
        self.caption('大数据、GPU、深度学习，在图像识别中汇合')
        self.wait(.5); self.clear(PINK)


class S08_AlphaGo(Film):
    def construct(self):
        self.tag('2016','AlphaGo：下一手，超出想象',GREEN)
        self.photo('leedol',-5,.22,4.25,GREEN)
        board=VGroup(*[line([-.9+i*.35,-2.25,0],[-.9+i*.35,2.1,0],DIM,1) for i in range(13)],
                     *[line([-.9,-2.25+i*.35,0],[3.3,-2.25+i*.35,0],DIM,1) for i in range(13)])
        self.play(FadeIn(board),run_time=.65)
        moves=[(1,1),(7,8),(4,5),(8,3),(5,10),(6,6),(10,8),(3,8)]
        stones=VGroup()
        for k,(r,c) in enumerate(moves):
            p=[-.9+c*.35,-2.25+r*.35,0]
            stone=spark(p,GREEN if k%2 else GOLD,.115)
            stones.add(stone)
            self.play(FadeIn(stone,scale=1.7),run_time=.18)
        self.caption('神经网络与搜索，让机器学会在棋盘上探索')
        self.wait(.55); self.clear(GREEN)


class S09_Transformer(Film):
    def construct(self):
        self.tag('2017','注意力机制，重写语言模型',CYAN)
        label=glow(txt('ATTENTION IS ALL YOU NEED',49,CYAN,True),CYAN).move_to([0,2.6,0])
        self.play(FadeIn(label,shift=UP*.2),run_time=.65)
        words=['每','个','词','都','看','向','其','他','词']
        points=[[-5.6+i*1.4,-1.55,0] for i in range(9)]
        bonds=VGroup(*[line(points[i],points[j], [CYAN,VIOLET,PINK][(i+j)%3],1.3) for i in range(9) for j in range(i+1,9) if (i+j)%3!=0])
        self.play(LaggedStart(*[Create(e) for e in bonds],lag_ratio=.012),run_time=1.2)
        nodes=VGroup(*[spark(p,GOLD,.13) for p in points])
        letters=VGroup(*[txt(w,46,INK,True).move_to(p+DOWN*.75) for w,p in zip(words,points)])
        self.play(FadeIn(nodes),FadeIn(letters),run_time=.55)
        eq=glow(MathTex(r"\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\!\left(\frac{QK^{\mathsf T}}{\sqrt{d_k}}\right)V",font_size=45,color=GOLD),GOLD)
        eq.move_to([0,.45,0])
        self.play(FadeIn(eq,shift=UP*.15),run_time=.8)
        self.caption('查询、键和值：让每个词选择要关注的上下文')
        self.wait(1.05); self.clear(CYAN)


class S10_Generative(Film):
    def construct(self):
        self.tag('2022','ChatGPT 走向大众',GOLD)
        prompt=glow(txt('你好，未来。',83,GOLD,True),GOLD).move_to([0,1.65,0])
        self.play(FadeIn(prompt,scale=1.2),run_time=.65)
        lines=VGroup(*[line([-5.8,-.4-i*.52,0],[5.6-i*.55,-.4-i*.52,0], [CYAN,PINK,GREEN][i%3],2) for i in range(5)])
        self.play(LaggedStart(*[Create(g) for g in lines],lag_ratio=.18),run_time=1.25)
        sub=glow(txt('文字 · 图像 · 声音 · 代码',53,INK,True),CYAN).move_to([0,-2.35,0])
        self.play(FadeIn(sub,shift=UP*.15),run_time=.6)
        self.caption('AI 从实验室走进日常，也带来新的责任')
        self.wait(.5); self.clear(GOLD)


class S03b_Activation(Film):
    def construct(self):
        self.tag('原理 01','神经元何时被点亮？',PINK)
        ax=Axes(x_range=[-3,3,1],y_range=[-1,3,1],x_length=8.8,y_length=4.3,
                axis_config={'color':DIM,'stroke_width':2},tips=False).move_to([0,-.15,0])
        curve=ax.plot(lambda x:max(0,x),x_range=[-3,3],color=GREEN,stroke_width=6)
        halo=curve.copy().set_stroke(GREEN,width=22,opacity=.14)
        self.play(Create(ax),run_time=.8)
        self.play(Create(halo),Create(curve),run_time=1.15)
        self.formula(r"\operatorname{ReLU}(z)=\max(0,z)",y=2.55,color=GOLD,size=62)
        track=ValueTracker(-2.8)
        dot=always_redraw(lambda:spark(ax.c2p(track.get_value(),max(0,track.get_value())),GOLD,.12))
        self.add(dot)
        self.play(track.animate.set_value(2.6),run_time=2.5,rate_func=linear)
        self.caption('负值被抑制，正值被放行：非线性让网络能学复杂边界')
        self.wait(1.6); self.clear(PINK)


class S05b_ChainRule(Film):
    def construct(self):
        self.tag('原理 02','误差怎样穿过一整张网络？',GREEN)
        nodes=VGroup(*[spark([x,0,0],col,.15) for x,col in [(-4,PINK),(0,CYAN),(4,GOLD)]])
        links=VGroup(line([-4,0,0],[0,0,0],CYAN,5),line([0,0,0],[4,0,0],GREEN,5))
        self.play(*[Create(l) for l in links],FadeIn(nodes),run_time=1.1)
        names=VGroup(*[txt(s,38,c,True).move_to([x,-1.2,0]) for x,s,c in [(-4,'输入',PINK),(0,'隐藏层',CYAN),(4,'损失',GOLD)]])
        self.play(FadeIn(names),run_time=.5)
        self.formula(r"\frac{\partial L}{\partial w_1}=\frac{\partial L}{\partial h}\cdot\frac{\partial h}{\partial w_1}",y=2.1,color=GOLD,size=58)
        traveling=spark([4,0,0],PINK,.19)
        self.play(FadeIn(traveling),run_time=.2)
        self.play(traveling.animate.move_to([0,0,0]),run_time=.8)
        self.play(traveling.animate.move_to([-4,0,0]),run_time=.8)
        self.caption('链式法则把末端的误差，一层一层传回起点')
        self.wait(1.7); self.clear(GREEN)


class S09b_AttentionMap(Film):
    def construct(self):
        self.tag('原理 03','注意力，不是平均分配',CYAN)
        words=['机','器','学','会','理','解']
        scores=np.array([[.54,.13,.08,.10,.10,.05],[.08,.45,.12,.11,.13,.11],
                         [.07,.13,.25,.24,.22,.09],[.08,.10,.34,.18,.22,.08],
                         [.06,.09,.20,.12,.45,.08],[.07,.09,.08,.13,.27,.36]])
        cells=VGroup()
        for r in range(6):
            for c in range(6):
                cell=Square(side_length=.54,stroke_color=CYAN,stroke_width=1,
                            fill_color=PINK if scores[r,c]>.3 else CYAN,
                            fill_opacity=float(.13+scores[r,c]*1.3)).move_to([-1.5+c*.6,1.85-r*.6,0])
                cells.add(cell)
        left=VGroup(*[txt(w,34,INK,True).move_to([-2.35,1.85-r*.6,0]) for r,w in enumerate(words)])
        top=VGroup(*[txt(w,34,GOLD,True).move_to([-1.5+c*.6,2.55,0]) for c,w in enumerate(words)])
        self.play(LaggedStart(*[FadeIn(c,scale=.7) for c in cells],lag_ratio=.016),run_time=1.6)
        self.play(FadeIn(left),FadeIn(top),run_time=.5)
        guide=ring(.42,GOLD,[-1.5+2*.6,1.85-3*.6,0],3)
        self.play(FadeIn(guide,scale=1.6),run_time=.5)
        self.formula(r"\alpha_{ij}=\operatorname{softmax}\!\left(\frac{q_i\cdot k_j}{\sqrt{d_k}}\right)",y=-2.5,color=GREEN,size=44)
        self.caption('矩阵里越亮，表示一个词对另一个词关注越多')
        self.wait(1.65); self.clear(CYAN)


class S10b_Leap(Film):
    def construct(self):
        self.tag('2023—2025','从对话，到调用工具',VIOLET)
        years=[('2023','多模态',CYAN),('2024','长上下文',PINK),('2025','推理与代理',GREEN)]
        nodes=VGroup(*[spark([-4.8+i*4.8,.7,0],col,.22) for i,(_,_,col) in enumerate(years)])
        bars=VGroup(*[line([-4.8+i*4.8,.7,0],[-4.8+(i+1)*4.8,.7,0],years[i+1][2],5) for i in range(2)])
        self.play(LaggedStart(*[Create(b) for b in bars],lag_ratio=.3),run_time=1.15)
        self.play(LaggedStart(*[FadeIn(n,scale=1.7) for n in nodes],lag_ratio=.25),run_time=.8)
        labels=VGroup(*[VGroup(txt(y,42,col,True),txt(label,36,INK)).arrange(DOWN,buff=.28).move_to([-4.8+i*4.8,-.75,0]) for i,(y,label,col) in enumerate(years)])
        self.play(LaggedStart(*[FadeIn(m,shift=UP*.25) for m in labels],lag_ratio=.25),run_time=1.1)
        self.formula(r"\mathrm{AI}:\quad \mathrm{perceive}\ \longrightarrow\ \mathrm{reason}\ \longrightarrow\ \mathrm{act}",y=2.5,color=GOLD,size=51)
        self.caption('这是一条能力演进示意线，不代表每一年只有一种突破')
        self.wait(1.65); self.clear(VIOLET)


class S11a_Cast(Film):
    def construct(self):
        self.tag('2026','这一年，三位主角同台',GOLD)
        specs=[('deepseek','DeepSeek',WHALE,3.35,None),
               ('claude','Claude',CLAUDE_C,None,3.75),
               ('gpt','GPT',DRAGON,None,3.75)]
        figs=[]
        for i,(key,label,color,w,h) in enumerate(specs):
            im=ImageMobject(str(ROOT/'assets'/'characters'/f'{key}.png'))
            if h: im.set_height(h)
            if w: im.set_width(w)
            if im.height>3.75: im.set_height(3.75)
            im.move_to([-4.75+i*4.75,0,0])
            im.align_to([0,-1.32,0],DOWN)
            aura=character_aura(im.width,im.height,color).move_to(im.get_center())
            figs.append((im,aura,label,color))
        for im,aura,label,color in figs:
            self.play(FadeIn(aura),FadeIn(im,shift=UP*.3,scale=1.05),run_time=.75)
        names=VGroup(*[txt(label,40,color,True).move_to([im.get_center()[0],-1.85,0]) for im,_,label,color in figs])
        self.play(LaggedStart(*[FadeIn(n,shift=UP*.2) for n in names],lag_ratio=.2),run_time=.8)
        self.caption('同一代前沿模型，三条不同的技术取向')
        self.wait(1.7); self.clear(GOLD)


class S12_Claude(Film):
    def construct(self):
        self.tag('2026','Claude Opus 5.5',CLAUDE_C)
        self.character('claude',x=-5.15,y=-.35,h=4.55,w=2.95,color=CLAUDE_C)
        name=txt('CLAUDE OPUS 5.5',46,CLAUDE_C,True).move_to([-1.45,2.45,0],aligned_edge=LEFT)
        self.play(FadeIn(name,shift=RIGHT*.25),run_time=.7)
        rows=[('长时编码','跨文件、跨仓库的迁移与审查'),
              ('多工具代理','自己规划、调用、再检查'),
              ('专业知识工作','文档、表格与研究')]
        group=VGroup()
        for i,(label,sub) in enumerate(rows):
            row=VGroup(Dot(radius=.085,color=CLAUDE_C),
                       VGroup(txt(label,36,INK,True),txt(sub,26,DIM)).arrange(DOWN,buff=.08,aligned_edge=LEFT)
                       ).arrange(RIGHT,buff=.3)
            row.move_to([-1.45,1.15-i*.95,0],aligned_edge=LEFT)
            group.add(row)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.25) for r in group],lag_ratio=.24),run_time=1.2)
        pipe=glow(MathTex(r"\mathrm{goal}\to\mathrm{plan}\to\mathrm{tools}\to\mathrm{verify}",font_size=44,color=GOLD),GOLD)
        pipe.move_to([3.05,-2.15,0])
        self.play(FadeIn(pipe,shift=UP*.15),run_time=.75)
        self.caption('厂商定位：跑得久、能自查的编码与代理伙伴')
        self.wait(1.9); self.clear(CLAUDE_C)


class S13_Astra(Film):
    def construct(self):
        self.tag('2026','GPT-6 Astra',CYAN)
        self.character('gpt',x=-5.15,y=-.35,h=4.55,w=2.95,color=DRAGON)
        name=txt('GPT-6  ASTRA',52,CYAN,True).move_to([-1.45,2.45,0],aligned_edge=LEFT)
        self.play(FadeIn(name,shift=RIGHT*.25),run_time=.7)
        rows=[('电脑操作','在真实软件界面里完成任务'),
              ('软件工程','写码、测试、排查、交付'),
              ('科研与文档','分析数据，产出可用材料')]
        group=VGroup()
        for i,(label,sub) in enumerate(rows):
            row=VGroup(Dot(radius=.085,color=DRAGON),
                       VGroup(txt(label,36,INK,True),txt(sub,26,DIM)).arrange(DOWN,buff=.08,aligned_edge=LEFT)
                       ).arrange(RIGHT,buff=.3)
            row.move_to([-1.45,1.15-i*.95,0],aligned_edge=LEFT)
            group.add(row)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.25) for r in group],lag_ratio=.24),run_time=1.2)
        pipe=glow(MathTex(r"\mathrm{observe}\to\mathrm{act}\to\mathrm{check}",font_size=46,color=GOLD),GOLD)
        pipe.move_to([3.05,-2.15,0])
        self.play(FadeIn(pipe,shift=UP*.15),run_time=.75)
        self.caption('厂商介绍：把“会用电脑”当成核心能力')
        self.wait(1.9); self.clear(CYAN)


class S14_DeepSeek(Film):
    def construct(self):
        self.tag('2026','DeepSeek V4.1 Flash',WHALE)
        self.character('deepseek',x=-4.95,y=-.55,h=4.1,w=4.75,color=WHALE)
        name=txt('DEEPSEEK  V4.1  FLASH',40,WHALE,True).move_to([-2.05,2.45,0],aligned_edge=LEFT)
        self.play(FadeIn(name,shift=RIGHT*.25),run_time=.7)
        rows=[('原生视觉','看得懂图，不只读文字'),
              ('稀疏 MoE','只叫醒部分专家，成本更低'),
              ('缓存更省','长任务推理更轻')]
        group=VGroup()
        for i,(label,sub) in enumerate(rows):
            row=VGroup(Dot(radius=.085,color=WHALE),
                       VGroup(txt(label,36,INK,True),txt(sub,26,DIM)).arrange(DOWN,buff=.08,aligned_edge=LEFT)
                       ).arrange(RIGHT,buff=.3)
            row.move_to([-2.05,1.15-i*.95,0],aligned_edge=LEFT)
            group.add(row)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.25) for r in group],lag_ratio=.24),run_time=1.2)
        pipe=glow(MathTex(r"y=\sum_{i\in\mathrm{TopK}(x)}g_i(x)E_i(x)",font_size=46,color=GOLD),GOLD)
        pipe.move_to([2.95,-2.2,0])
        self.play(FadeIn(pipe,shift=UP*.15),run_time=.75)
        self.caption('官方介绍：原生视觉、稀疏激活、更小的缓存开销')
        self.wait(1.9); self.clear(WHALE)


class S15_Compare(Film):
    def construct(self):
        self.tag('2026','前沿模型，不只有一条赛道',GOLD)
        data=[('Claude Opus 5.5','长任务 · 代码代理',VIOLET),('GPT-6 Astra','电脑操作 · 科研',CYAN),
              ('DeepSeek V4.1 Flash','视觉 · 高效推理',GREEN)]
        rows=VGroup()
        for i,(name,detail,color) in enumerate(data):
            y=1.7-i*1.65
            stripe=line([-5.85,y,0],[-3.8,y,0],color,7)
            text=txt(name,44,color,True).move_to([-.65,y+.3,0])
            desc=txt(detail,33,INK).move_to([-.65,y-.4,0])
            rows.add(VGroup(stripe,text,desc))
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.35) for r in rows],lag_ratio=.24),run_time=1.5)
        self.caption('不同任务、权限和评测方法，不能压成一个“谁最强”')
        self.wait(2.0); self.clear(GOLD)


class S11_Finale(Film):
    def construct(self):
        self.tag('1950—今天','一段仍在书写的历史',CYAN)
        columns=[(-5.1,PINK),(-2.55,CYAN),(0,GOLD),(2.55,GREEN),(5.1,VIOLET)]
        stars=VGroup(*[spark([x,0,0],col,.22) for x,col in columns])
        rails=VGroup(*[line([columns[i][0],0,0],[columns[i+1][0],0,0],columns[i+1][1],4) for i in range(4)])
        self.play(LaggedStart(*[Create(x) for x in rails],lag_ratio=.2),run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s,scale=1.7) for s in stars],lag_ratio=.12),run_time=.75)
        core=glow(txt('下一章，由我们共同决定',77,GOLD,True),GOLD).move_to([0,1.5,0])
        self.play(FadeIn(core,scale=1.18),run_time=.8)
        small=txt('THE STORY IS STILL BEING WRITTEN',31,DIM).move_to([0,-1.7,0])
        self.play(FadeIn(small),run_time=.5)
        self.wait(2.0)
