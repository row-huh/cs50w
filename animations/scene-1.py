from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Stick figure builder — returns individual parts so we can animate them
# ─────────────────────────────────────────────────────────────────────────────

def make_figure(scale=1.0, body_color=WHITE, pos=ORIGIN):
    """
    Returns a dict of named VGroups/Mobjects so arms etc. can be animated.
    All parts are positioned relative to `pos`.
    """
    s = scale

    head  = Circle(radius=0.22*s, color=body_color, stroke_width=3)
    head.move_to(pos + UP*0.88*s)

    torso = Line(pos + UP*0.66*s, pos + DOWN*0.22*s,
                 color=body_color, stroke_width=3)

    # right arm (screen-right = character's right)
    r_shoulder = pos + UP*0.55*s
    r_arm_upper = Line(r_shoulder,
                       r_shoulder + RIGHT*0.4*s + DOWN*0.35*s,
                       color=body_color, stroke_width=3)
    r_elbow = r_shoulder + RIGHT*0.4*s + DOWN*0.35*s
    r_arm_lower = Line(r_elbow,
                       r_elbow + RIGHT*0.2*s + DOWN*0.38*s,
                       color=body_color, stroke_width=3)

    # left arm
    l_shoulder = pos + UP*0.55*s
    l_arm_upper = Line(l_shoulder,
                       l_shoulder + LEFT*0.4*s + DOWN*0.35*s,
                       color=body_color, stroke_width=3)
    l_elbow = l_shoulder + LEFT*0.4*s + DOWN*0.35*s
    l_arm_lower = Line(l_elbow,
                       l_elbow + LEFT*0.2*s + DOWN*0.38*s,
                       color=body_color, stroke_width=3)

    # legs
    hip = pos + DOWN*0.22*s
    r_leg = Line(hip, hip + RIGHT*0.3*s + DOWN*0.68*s,
                 color=body_color, stroke_width=3)
    l_leg = Line(hip, hip + LEFT*0.3*s  + DOWN*0.68*s,
                 color=body_color, stroke_width=3)

    parts = dict(
        head=head, torso=torso,
        r_arm_upper=r_arm_upper, r_arm_lower=r_arm_lower,
        l_arm_upper=l_arm_upper, l_arm_lower=l_arm_lower,
        r_leg=r_leg, l_leg=l_leg,
    )
    body = VGroup(*parts.values())
    return body, parts


def arm_raised(scale=1.0, pos=ORIGIN, body_color=WHITE, side="right", raise_deg=160):
    """Return upper+lower arm VGroup for a raised arm (shoulder flex)."""
    s = scale
    shoulder = pos + UP*0.55*s
    direction = RIGHT if side == "right" else LEFT
    sign = 1 if side == "right" else -1

    rad = np.radians(raise_deg)
    # upper arm points upward at raise_deg from vertical
    upper_end = shoulder + np.array([sign * np.sin(rad)*0.55*s,
                                      np.cos(rad)*0.55*s, 0])
    upper = Line(shoulder, upper_end, color=body_color, stroke_width=3)

    # lower arm extends roughly forward from elbow
    lower_end = upper_end + np.array([sign*0.25*s, -0.3*s, 0])
    lower = Line(upper_end, lower_end, color=body_color, stroke_width=3)

    return VGroup(upper, lower), upper_end


def arm_half_raised(scale=1.0, pos=ORIGIN, body_color=WHITE, side="right", raise_deg=70):
    """Return upper+lower arm for a mid-raise (struggling attempt)."""
    return arm_raised(scale, pos, body_color, side, raise_deg)


# ─────────────────────────────────────────────────────────────────────────────
# The Scene
# ─────────────────────────────────────────────────────────────────────────────

class Scene1(Scene):
    def construct(self):

        # ═══════════════════════════════════════════════════════════
        # ACT 1 — Introduce Grace
        # ═══════════════════════════════════════════════════════════

        grace_pos = ORIGIN + DOWN*0.5
        grace, gp = make_figure(scale=1.15, body_color=WHITE, pos=grace_pos)

        name_lbl = Text("Grace", font_size=30, color=YELLOW)
        name_lbl.next_to(grace, DOWN, buff=0.18)

        self.play(FadeIn(grace), Write(name_lbl), run_time=0.9)
        self.wait(0.3)

        # shoulder pain — red dot on the right shoulder
        shoulder_dot = Dot(grace_pos + UP*0.55*1.15 + RIGHT*0.05,
                           radius=0.13, color=RED, fill_opacity=0.9)
        pain_ring = Circle(radius=0.22, color=RED, stroke_width=2.5,
                           fill_opacity=0)
        pain_ring.move_to(shoulder_dot)

        pain_lbl = Text("frozen\nshoulder", font_size=17, color=RED)
        pain_lbl.next_to(shoulder_dot, RIGHT, buff=0.18)

        self.play(GrowFromCenter(shoulder_dot))
        self.play(
            Create(pain_ring),
            FadeIn(pain_lbl, shift=RIGHT*0.1),
        )

        # pulsing ring to sell the pain
        self.play(
            pain_ring.animate.scale(1.45).set_opacity(0),
            run_time=0.7, rate_func=rush_into
        )
        self.remove(pain_ring)
        self.wait(0.3)

        # Grace tries to raise arm — only gets halfway
        r_arm_up, _ = arm_half_raised(scale=1.15, pos=grace_pos,
                                       body_color=WHITE, side="right",
                                       raise_deg=55)
        r_arm_up.move_to(r_arm_up.get_center())   # keep in world space

        # replace right arm parts with struggling raised version
        r_upper_orig = gp["r_arm_upper"]
        r_lower_orig = gp["r_arm_lower"]

        self.play(
            Transform(r_upper_orig, r_arm_up[0]),
            Transform(r_lower_orig, r_arm_up[1]),
            run_time=1.0, rate_func=there_and_back_with_pause
        )

        # pain flash
        self.play(
            Flash(shoulder_dot, color=RED, line_length=0.18,
                  num_lines=8, run_time=0.5)
        )

        subtitle = Text("Grace has a frozen shoulder — he can barely lift his arm.",
                        font_size=19, color=GRAY_A)
        subtitle.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(subtitle))
        self.wait(1.2)
        self.play(FadeOut(subtitle))

        # ═══════════════════════════════════════════════════════════
        # ACT 2 — Grace walks to the doctor
        # ═══════════════════════════════════════════════════════════

        # slide Grace to the left to make room
        self.play(grace.animate.shift(LEFT*3.2),
                  name_lbl.animate.shift(LEFT*3.2),
                  shoulder_dot.animate.shift(LEFT*3.2),
                  pain_lbl.animate.shift(LEFT*3.2),
                  run_time=0.8)

        # Doctor figure on the right
        doc_pos = RIGHT*3.0 + DOWN*0.5
        doctor, dp = make_figure(scale=1.15, body_color=BLUE_C, pos=doc_pos)
        doc_lbl = Text("Doctor", font_size=30, color=BLUE_C)
        doc_lbl.next_to(doctor, DOWN, buff=0.18)

        # doctor has a little cross / stethoscope indicator
        cross_v = Line(doc_pos + UP*0.3 + RIGHT*0.55,
                       doc_pos + UP*0.3 + RIGHT*0.55 + UP*0.25,
                       color=RED, stroke_width=3)
        cross_h = Line(doc_pos + UP*0.3 + RIGHT*0.55 + UP*0.12 + LEFT*0.1,
                       doc_pos + UP*0.3 + RIGHT*0.55 + UP*0.12 + RIGHT*0.1,
                       color=RED, stroke_width=3)
        med_cross = VGroup(cross_v, cross_h)

        self.play(FadeIn(doctor, doc_lbl), Create(med_cross))

        # walking arrow between them
        walk_arrow = Arrow(LEFT*1.2 + DOWN*1.3, RIGHT*1.2 + DOWN*1.3,
                           color=YELLOW, stroke_width=3, buff=0.1)
        walk_lbl = Text("walks to clinic", font_size=17, color=YELLOW)
        walk_lbl.next_to(walk_arrow, DOWN, buff=0.12)
        self.play(GrowArrow(walk_arrow), FadeIn(walk_lbl))
        self.wait(0.5)

        # speech bubble from doctor: "do these exercises at home"
        bubble_rect = RoundedRectangle(
            width=3.2, height=1.1, corner_radius=0.2,
            fill_color="#1a1a2e", fill_opacity=0.95,
            stroke_color=BLUE_C, stroke_width=2
        )
        bubble_rect.move_to(doc_pos + UP*1.85 + LEFT*0.8)

        bubble_lines = VGroup(
            Text("Do these exercises",  font_size=16, color=WHITE),
            Text("at home. Daily.",     font_size=16, color=WHITE),
            Text("Raise arm to 160°",   font_size=16, color=TEAL),
        ).arrange(DOWN, buff=0.08).move_to(bubble_rect)

        # small tail for speech bubble
        tail = Triangle(fill_color="#1a1a2e", fill_opacity=0.95,
                        stroke_color=BLUE_C, stroke_width=2)
        tail.scale(0.18).rotate(PI/6)
        tail.next_to(bubble_rect, RIGHT+DOWN, buff=-0.1)
        tail.shift(LEFT*0.3 + DOWN*0.1)

        speech = VGroup(bubble_rect, bubble_lines, tail)

        self.play(FadeIn(speech, shift=DOWN*0.15))
        self.wait(1.2)

        # Grace looks satisfied — small checkmark above head
        grace_head_pos = grace_pos + LEFT*3.2 + UP*0.88*1.15
        checkmark = Text("✓", font_size=32, color=GREEN)
        checkmark.move_to(grace_head_pos + UP*0.45)
        self.play(GrowFromCenter(checkmark))
        self.wait(0.6)

        self.play(FadeOut(VGroup(
            speech, walk_arrow, walk_lbl, checkmark,
            doctor, doc_lbl, med_cross
        )))

        # ═══════════════════════════════════════════════════════════
        # ACT 3 — Grace goes home, tries to exercise
        # ═══════════════════════════════════════════════════════════

        # bring Grace back to center
        self.play(
            grace.animate.move_to(grace_pos),
            name_lbl.animate.next_to(grace_pos + DOWN*0.9*1.15, DOWN, buff=0.18),
            shoulder_dot.animate.move_to(grace_pos + UP*0.55*1.15 + RIGHT*0.05),
            pain_lbl.animate.next_to(grace_pos + UP*0.55*1.15 + RIGHT*0.05, RIGHT, buff=0.18),
            run_time=0.7
        )

        home_lbl = Text("🏠  at home", font_size=22, color=GRAY_A)
        home_lbl.to_edge(UP, buff=0.4)
        self.play(FadeIn(home_lbl))

        # Grace attempts shoulder flex — raise to 160°
        # ---- attempt 1: overshoots weirdly (wrong posture)  ----
        attempt_lbl = Text("Attempt #1", font_size=20, color=YELLOW)
        attempt_lbl.to_edge(UP, buff=0.85)

        # good arm motion: right arm raises to 160 but LEFT arm also flails (wrong)
        r_correct, _ = arm_raised(scale=1.15, pos=grace_pos,
                                   body_color=WHITE, side="right", raise_deg=160)
        l_wrong, _   = arm_raised(scale=1.15, pos=grace_pos,
                                   body_color=WHITE, side="left", raise_deg=110)

        self.play(Write(attempt_lbl))

        # right arm goes up — looks like it's straining
        self.play(
            Transform(gp["r_arm_upper"], r_correct[0]),
            Transform(gp["r_arm_lower"], r_correct[1]),
            run_time=1.2, rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            Flash(shoulder_dot, color=RED, line_length=0.15, num_lines=7)
        )

        # wrong: left arm compensates incorrectly
        self.play(
            Transform(gp["l_arm_upper"], l_wrong[0]),
            Transform(gp["l_arm_lower"], l_wrong[1]),
            run_time=0.8
        )

        wrong_tag = Text("⚠ wrong posture", font_size=18, color=RED)
        wrong_tag.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(wrong_tag))
        self.wait(0.6)

        # ---- attempt 2: arm barely goes up, gives up ----
        r_low, _   = arm_half_raised(scale=1.15, pos=grace_pos,
                                      body_color=WHITE, side="right", raise_deg=40)
        l_rest_upper = Line(grace_pos + UP*0.55*1.15,
                             grace_pos + UP*0.55*1.15 + LEFT*0.4*1.15 + DOWN*0.35*1.15,
                             color=WHITE, stroke_width=3)
        l_rest_lower = Line(
            grace_pos + UP*0.55*1.15 + LEFT*0.4*1.15 + DOWN*0.35*1.15,
            grace_pos + UP*0.55*1.15 + LEFT*0.4*1.15 + DOWN*0.35*1.15 + LEFT*0.2*1.15 + DOWN*0.38*1.15,
            color=WHITE, stroke_width=3
        )

        attempt2_lbl = Text("Attempt #2", font_size=20, color=YELLOW)
        attempt2_lbl.to_edge(UP, buff=0.85)

        self.play(
            Transform(attempt_lbl, attempt2_lbl),
            FadeOut(wrong_tag),
            run_time=0.5
        )
        self.play(
            Transform(gp["r_arm_upper"], r_low[0]),
            Transform(gp["r_arm_lower"], r_low[1]),
            Transform(gp["l_arm_upper"], l_rest_upper),
            Transform(gp["l_arm_lower"], l_rest_lower),
            run_time=1.0
        )
        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════
        # ACT 4 — Grace looks defeated
        # ═══════════════════════════════════════════════════════════

        # droop head slightly
        defeated_head = Circle(radius=0.22*1.15, color=WHITE, stroke_width=3)
        defeated_head.move_to(grace_pos + UP*0.88*1.15 + DOWN*0.12)   # slight droop

        # sad mouth inside head
        sad_mouth = Arc(radius=0.09, angle=PI, start_angle=0,
                        color=WHITE, stroke_width=2)
        sad_mouth.move_to(grace_pos + UP*0.88*1.15 + DOWN*0.12 + DOWN*0.06)
        sad_mouth.rotate(PI)   # flip to sad

        # eyes
        l_eye = Dot(grace_pos + UP*0.88*1.15 + DOWN*0.12 + LEFT*0.07 + UP*0.04,
                    radius=0.02, color=WHITE)
        r_eye = Dot(grace_pos + UP*0.88*1.15 + DOWN*0.12 + RIGHT*0.07 + UP*0.04,
                    radius=0.02, color=WHITE)

        self.play(
            Transform(gp["head"], defeated_head),
            FadeIn(sad_mouth, l_eye, r_eye),
            FadeOut(attempt_lbl),
            run_time=0.8
        )

        # sweat drop
        sweat = Dot(grace_pos + UP*0.88*1.15 + RIGHT*0.28,
                    radius=0.055, color=BLUE, fill_opacity=0.85)
        self.play(GrowFromCenter(sweat))

        # "..." thought bubble
        thought_dots = Text("...", font_size=36, color=GRAY_A)
        thought_dots.move_to(grace_pos + UP*1.85)
        self.play(FadeIn(thought_dots, shift=UP*0.1))

        # caption
        defeated_caption = Text(
            "Grace has no idea what he's doing wrong.\nHis recovery is at an impasse.",
            font_size=21, color=RED_A, line_spacing=1.4
        )
        defeated_caption.to_edge(DOWN, buff=0.45)
        self.play(Write(defeated_caption, run_time=1.5))
        self.wait(1.0)

        # final hook: question mark appears
        q_mark = Text("?", font_size=80, color=YELLOW, weight=BOLD)
        q_mark.move_to(ORIGIN + RIGHT*2.8 + UP*0.2)
        self.play(GrowFromCenter(q_mark))

        hook = Text("If only there was a guide at home too…",
                    font_size=22, color=YELLOW, slant=ITALIC)
        hook.to_edge(DOWN, buff=0.15)
        self.play(
            FadeOut(defeated_caption),
            FadeIn(hook)
        )
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            grace, name_lbl, shoulder_dot, pain_lbl,
            sad_mouth, l_eye, r_eye, sweat,
            thought_dots, home_lbl, q_mark, hook
        )))