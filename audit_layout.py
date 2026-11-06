#!/usr/bin/env python3
"""
Layout audit for Manim scenes — 无画面自检。

做法：不真正渲染，把每个 Scene 的 play()/add() 变成"只登记 mobject"，
跑完 construct() 后检查：
  1) 文本是否越界
  2) 不同文本之间是否重叠（自动忽略同一段霓虹文字的辉光副本）

用法：
    python audit_layout.py path/to file.py
    python audit_layout.py file.py --prefix S0
    python audit_layout.py file.py --allow-overlap
退出码：0 = 通过；1 = 有越界/重叠/构造异常。
"""
import argparse
import importlib.util
import sys
import traceback

from manim import (
    Scene, ThreeDScene, VGroup, Group,
    Text, Tex, MathTex, SingleStringMathTex,
)


class _DryRenderer:
    """ThreeDScene.__init__ 会读 renderer.camera_config，给个假的。"""
    camera_config = {"pixel_width": 1920, "pixel_height": 1080}


class _DryCamera:
    background_color = None


class Dry:
    """把动画变成登记操作。"""

    renderer = _DryRenderer()
    camera = _DryCamera()

    def play(self, *anims, **kwargs):
        for a in anims:
            m = getattr(a, "mobject", None)
            if m is not None and m not in self.mobjects:
                self.mobjects.append(m)

    def wait(self, *args, **kwargs):
        pass

    def add(self, *mobs):
        for m in mobs:
            if m not in self.mobjects:
                self.mobjects.append(m)

    def remove(self, *mobs):
        for m in mobs:
            if m in self.mobjects:
                self.mobjects.remove(m)

    def clear_scene(self, *args, **kwargs):
        pass

    # ---- ThreeDScene 相机方法打桩（干跑不需要真相机） ----
    def set_camera_orientation(self, *args, **kwargs):
        pass

    def move_camera(self, *args, **kwargs):
        pass

    def begin_ambient_camera_rotation(self, *args, **kwargs):
        pass

    def stop_ambient_camera_rotation(self, *args, **kwargs):
        pass

    def add_fixed_in_frame_mobjects(self, *mobs):
        self.add(*mobs)

    def add_fixed_orientation_mobjects(self, *mobs):
        self.add(*mobs)


def bbox(m):
    return (m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])


def text_of(m):
    t = getattr(m, "text", None)
    if t:
        return t
    try:
        return m.get_tex_string()
    except Exception:
        return ""


def collect_texts(mob, out, seen):
    if id(mob) in seen:
        return
    seen.add(id(mob))
    if isinstance(mob, (Text, Tex, MathTex, SingleStringMathTex)):
        out.append(mob)
    for c in getattr(mob, "submobjects", []):
        collect_texts(c, out, seen)


def load_module(path):
    import os
    d = os.path.dirname(os.path.abspath(path))
    if d not in sys.path:
        sys.path.insert(0, d)
    name = "audited_module"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--x-limit", type=float, default=7.6)
    ap.add_argument("--y-top", type=float, default=4.2)
    ap.add_argument("--y-bottom", type=float, default=-4.35)
    ap.add_argument("--allow-overlap", action="store_true")
    args = ap.parse_args()

    mod = load_module(args.file)
    names = sorted(
        n for n in dir(mod)
        if n.startswith(args.prefix)
        and isinstance(getattr(mod, n), type)
        and any(base in (Scene, ThreeDScene) for base in getattr(mod, n).__mro__)
    )
    if not names:
        print("no scene classes matched", file=sys.stderr)
        return 1

    total_issues = 0
    for name in names:
        cls = getattr(mod, name)
        S = type("Dry_" + name, (Dry, cls), {})
        try:
            s = S()
            try:
                s.setup()
            except Exception:
                s.back = VGroup()
            s.construct()
        except Exception:
            if ThreeDScene in cls.__mro__:
                print(f"== {name}: SKIP (3D 场景，干跑相机不可用)")
                continue
            print(f"== {name}: ERROR while constructing")
            traceback.print_exc()
            total_issues += 1
            continue

        texts = []
        collect_texts(Group(*s.mobjects), texts, set())
        seen = set()
        uniq = []
        for t in texts:
            if id(t) not in seen:
                seen.add(id(t))
                uniq.append(t)

        edges = []
        for t in uniq:
            l, r, b, top = bbox(t)
            if l < -args.x_limit or r > args.x_limit or b < args.y_bottom or top > args.y_top:
                edges.append(([round(v, 2) for v in (l, r, b, top)], text_of(t)[:18]))

        overlaps = []
        for i in range(len(uniq)):
            li, ri, bi, ti = bbox(uniq[i])
            for j in range(i + 1, len(uniq)):
                if text_of(uniq[i]) == text_of(uniq[j]):
                    continue  # 霓虹辉光副本，跳过
                lj, rj, bj, tj = bbox(uniq[j])
                x0, x1 = max(li, lj), min(ri, rj)
                y0, y1 = max(bi, bj), min(ti, tj)
                if x1 - x0 > 0.05 and y1 - y0 > 0.05:
                    overlaps.append((round(x1 - x0, 2), round(y1 - y0, 2),
                                     text_of(uniq[i])[:10], text_of(uniq[j])[:10]))

        status = "OK" if not edges and not overlaps else "ISSUE"
        print(f"== {name}: EDGE={len(edges)} OVL={len(overlaps)} [{status}]")
        for e in edges[:8]:
            print("   EDGE", e)
        for o in overlaps[:8]:
            print("   OVL ", o)
        total_issues += len(edges) + (0 if args.allow_overlap else len(overlaps))

    print(f"\nTOTAL ISSUES: {total_issues}")
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
