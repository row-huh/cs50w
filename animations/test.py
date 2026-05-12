from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def stick_figure(scale=1.0, color=WHITE):
    """Return a VGroup stick figure centred at origin."""
    head   = Circle(radius=0.18*scale, color=color, stroke_width=2.5)
    head.move_to(UP * 0.72 * scale)

    torso  = Line(UP*0.54*scale, DOWN*0.18*scale, color=color, stroke_width=2.5)

    # arms
    shoulder = UP * 0.36 * scale
    l_arm = Line(shoulder, shoulder + LEFT*0.45*scale + DOWN*0.3*scale,
                 color=color, stroke_width=2.5)
    r_arm = Line(shoulder, shoulder + RIGHT*0.45*scale + DOWN*0.3*scale,
                 color=color, stroke_width=2.5)

    # legs
    hip = DOWN * 0.18 * scale
    l_leg = Line(hip, hip + LEFT*0.3*scale + DOWN*0.54*scale,
                 color=color, stroke_width=2.5)
    r_leg = Line(hip, hip + RIGHT*0.3*scale + DOWN*0.54*scale,
                 color=color, stroke_width=2.5)

    return VGroup(head, torso, l_arm, r_arm, l_leg, r_leg)


def arm_pose(shoulder, elbow_angle_deg, upper_len=0.9, lower_len=0.75,
             color=YELLOW, stroke_width=3.5):
    """
    Return (upper_arm Line, lower_arm Line, elbow Dot, wrist Dot).
    elbow_angle_deg = angle the forearm makes relative to vertical upper arm.
    shoulder is a numpy array [x, y, 0].
    """
    # upper arm hangs straight down from shoulder
    elbow_pos = shoulder + np.array([0, -upper_len, 0])

    rad = np.radians(elbow_angle_deg)
    wrist_pos = elbow_pos + np.array([np.sin(rad)*lower_len, -np.cos(rad)*lower_len, 0])

    upper = Line(shoulder, elbow_pos, color=color, stroke_width=stroke_width)
    lower = Line(elbow_pos, wrist_pos, color=color, stroke_width=stroke_width)
    elbow_dot = Dot(elbow_pos, color=RED, radius=0.08)
    wrist_dot  = Dot(wrist_pos, color=ORANGE, radius=0.06)

    return VGroup(upper, lower, elbow_dot, wrist_dot), elbow_pos, wrist_pos


# ─────────────────────────────────────────────────────────────────────────────
# Scene 1 – Title card
# ─────────────────────────────────────────────────────────────────────────────

class S1_Title(Scene):
    def construct(self):
        title = Text("PhysioGuide", font_size=72, color=BLUE_B, weight=BOLD)
        sub   = Text("How it works — and why it's hard",
                     font_size=30, color=GRAY_A)
        sub.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.4)
        self.play(FadeIn(sub, shift=UP*0.2))
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, sub)))


# ─────────────────────────────────────────────────────────────────────────────
# Scene 2 – Normal workflow (doctor → patient)
# ─────────────────────────────────────────────────────────────────────────────

class S2_NormalFlow(Scene):
    def construct(self):
        header = Text("The Normal Workflow", font_size=38, color=BLUE_B)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))

        # ── Doctor figure ──
        doc = stick_figure(scale=0.9, color=BLUE_C)
        doc.move_to(LEFT*4.5 + DOWN*0.4)
        doc_label = Text("Doctor", font_size=22, color=BLUE_C)
        doc_label.next_to(doc, DOWN, buff=0.12)

        # ── Patient figure ──
        pat = stick_figure(scale=0.9, color=GREEN_C)
        pat.move_to(RIGHT*4.5 + DOWN*0.4)
        pat_label = Text("Patient", font_size=22, color=GREEN_C)
        pat_label.next_to(pat, DOWN, buff=0.12)

        self.play(FadeIn(doc, doc_label), FadeIn(pat, pat_label))
        self.wait(0.3)

        # ── Prescription arrow ──
        arrow = Arrow(LEFT*2.8, RIGHT*2.8, color=YELLOW, buff=0.1,
                      stroke_width=4)
        arrow.shift(DOWN*0.4)

        rx_box = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15,
                                  color=YELLOW, fill_color=DARK_GRAY,
                                  fill_opacity=0.85, stroke_width=2)
        rx_box.move_to(ORIGIN + DOWN*0.4)

        rx_lines = VGroup(
            Text("Exercise: Bicep Curl", font_size=17, color=WHITE),
            Text("Max ROM: 120°",        font_size=17, color=WHITE),
            Text("Reps: 10",             font_size=17, color=WHITE),
        ).arrange(DOWN, buff=0.08).move_to(rx_box)

        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(FadeIn(rx_box), Write(rx_lines), run_time=0.9)
        self.wait(0.6)

        # ── Summary arrow back ──
        arrow_back = Arrow(RIGHT*2.8, LEFT*2.8, color=TEAL, buff=0.1,
                           stroke_width=4)
        arrow_back.shift(UP*0.6 + DOWN*0.4)

        summary_text = Text("Session summary sent back",
                            font_size=18, color=TEAL)
        summary_text.next_to(arrow_back, UP, buff=0.1)

        self.play(GrowArrow(arrow_back), FadeIn(summary_text))
        self.wait(1.2)

        self.play(FadeOut(VGroup(
            header, doc, doc_label, pat, pat_label,
            arrow, rx_box, rx_lines, arrow_back, summary_text
        )))


# ─────────────────────────────────────────────────────────────────────────────
# Scene 3 – Problem Einz  (manual ROM threshold)
# ─────────────────────────────────────────────────────────────────────────────

class S3_ProblemEinz(Scene):
    def construct(self):
        header = Text("Problem Einz: Manual ROM Thresholds",
                      font_size=34, color=RED_B, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))

        # Doctor drowning in a pile of patient cards
        doc = stick_figure(scale=0.85, color=BLUE_C)
        doc.move_to(ORIGIN + DOWN*0.5)
        self.play(FadeIn(doc))

        # Stack of patient cards raining down
        cards = []
        labels = [
            "Ali — Bicep Curl — 110°",
            "Sara — Shoulder Flex — 95°",
            "Omar — Knee Ext — 130°",
            "Zara — Hip Flex — 80°",
            "Bilal — Elbow Ext — 140°",
        ]
        for i, txt in enumerate(labels):
            card = RoundedRectangle(width=3.2, height=0.52,
                                    corner_radius=0.1,
                                    fill_color=DARK_GRAY, fill_opacity=0.9,
                                    stroke_color=YELLOW, stroke_width=1.5)
            lbl  = Text(txt, font_size=15, color=WHITE).move_to(card)
            grp  = VGroup(card, lbl)
            grp.move_to(np.array([-4 + i*0.5, 3.2, 0]))
            cards.append(grp)

        self.play(LaggedStart(*[FadeIn(c, shift=DOWN*0.3) for c in cards],
                              lag_ratio=0.18))

        # Cards pile onto the doctor
        targets = [doc.get_center() + np.array([0.1*i - 0.2, -0.2 - 0.12*i, 0])
                   for i in range(len(cards))]
        self.play(LaggedStart(
            *[c.animate.move_to(t).scale(0.7)
              for c, t in zip(cards, targets)],
            lag_ratio=0.15), run_time=1.4)

        # Stress indicators
        excls = VGroup(*[
            Text("!", font_size=30, color=RED).move_to(
                doc.get_top() + np.array([0.3*j - 0.3, 0.5 + 0.1*j, 0]))
            for j in range(3)
        ])
        self.play(LaggedStart(*[GrowFromCenter(e) for e in excls],
                              lag_ratio=0.2))

        quote = Text(
            '"Doctor expected to set threshold\nfor every patient, every exercise."',
            font_size=22, color=YELLOW, slant=ITALIC
        )
        quote.to_edge(DOWN, buff=0.55)
        self.play(Write(quote))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            header, doc, quote, excls, *cards
        )))


# ─────────────────────────────────────────────────────────────────────────────
# Scene 4 – Problem Zwei  (raw x,y coords from MediaPipe)
# ─────────────────────────────────────────────────────────────────────────────

class S4_ProblemZwei(Scene):
    def construct(self):
        header = Text("Problem Zwei: Raw Coords ≠ Angle",
                      font_size=34, color=RED_B, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))

        # ── left panel: animated arm ──
        shoulder_pos = np.array([-3.8, 1.2, 0])

        # Animate the arm moving through several elbow angles
        angles = [0, 30, 60, 90, 120, 90, 60, 30, 0]

        # build first pose
        first_arm, elbow_pos, wrist_pos = arm_pose(
            shoulder_pos, angles[0], color=YELLOW)
        self.play(FadeIn(first_arm))

        # elbow & wrist coord labels
        elbow_lbl = always_redraw(lambda: Text(
            f"elbow", font_size=14, color=RED
        ).next_to(first_arm[2], LEFT, buff=0.08))   # dummy – replaced below

        t_label = Text("t = 0", font_size=18, color=GRAY_A)
        t_label.move_to(np.array([-3.8, -0.2, 0]))

        self.play(FadeIn(t_label))

        # Raw data table on the right
        table_title = Text("MediaPipe sees:", font_size=20, color=GRAY_A)
        table_title.move_to(np.array([1.8, 2.0, 0]))
        self.play(FadeIn(table_title))

        # We'll build rows one by one
        rows = []
        row_template = [
            (0,  "(90, 80)",  "(90, 152)"),
            (1,  "(91, 80)",  "(88, 148)"),
            (2,  "(92, 79)",  "(84, 141)"),
            (3,  "(91, 78)",  "(79, 132)"),
            (4,  "(90, 77)",  "(73, 122)"),
        ]

        col_headers = VGroup(
            Text("t",        font_size=16, color=BLUE_B).move_to(np.array([0.8,  1.5, 0])),
            Text("knee(x,y)",font_size=16, color=BLUE_B).move_to(np.array([2.1,  1.5, 0])),
            Text("hip(x,y)", font_size=16, color=BLUE_B).move_to(np.array([3.6,  1.5, 0])),
        )
        hline = Line(np.array([0.2, 1.3, 0]), np.array([4.5, 1.3, 0]),
                     color=GRAY, stroke_width=1)
        self.play(FadeIn(col_headers), Create(hline))

        for idx, (t, knee, hip) in enumerate(row_template):
            y = 1.1 - idx * 0.32
            row = VGroup(
                Text(str(t),  font_size=15, color=WHITE).move_to(np.array([0.8,  y, 0])),
                Text(knee,    font_size=15, color=GREEN_C).move_to(np.array([2.1,  y, 0])),
                Text(hip,     font_size=15, color=ORANGE).move_to(np.array([3.6,  y, 0])),
            )

            # animate arm to matching angle
            new_angle = angles[idx]
            new_arm, _, _ = arm_pose(shoulder_pos, new_angle, color=YELLOW)
            new_t = Text(f"t = {t}", font_size=18, color=GRAY_A)
            new_t.move_to(np.array([-3.8, -0.2, 0]))

            self.play(
                Transform(first_arm, new_arm),
                FadeIn(row, shift=RIGHT*0.15),
                Transform(t_label, new_t),
                run_time=0.55
            )
            rows.append(row)

        # Problem callout
        callout = RoundedRectangle(width=5.5, height=0.75, corner_radius=0.12,
                                   fill_color="#3a0000", fill_opacity=0.9,
                                   stroke_color=RED, stroke_width=2)
        callout.to_edge(DOWN, buff=0.45)
        callout_txt = Text(
            "How do you turn (x, y) over time → a comparable angle?",
            font_size=19, color=RED_A
        ).move_to(callout)
        self.play(FadeIn(callout), Write(callout_txt))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            header, first_arm, t_label, table_title,
            col_headers, hline, callout, callout_txt, *rows
        )))


# ─────────────────────────────────────────────────────────────────────────────
# Scene 5 – The Solution  (coords → angle → template curve → live comparison)
# ─────────────────────────────────────────────────────────────────────────────

class S5_Solution(Scene):
    def construct(self):
        header = Text("The Solution: Coords → Angle → Template",
                      font_size=32, color=GREEN_B, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))

        # ── Step 1: show angle computation ──
        step1 = Text("Step 1 – Compute elbow angle from 3 joints",
                     font_size=22, color=YELLOW)
        step1.move_to(UP*2.0)
        self.play(FadeIn(step1, shift=RIGHT*0.2))

        shoulder_pos = np.array([-1.5, 0.8, 0])
        elbow_pos_   = np.array([-1.5, -0.1, 0])
        wrist_pos_   = np.array([-0.7, -0.8, 0])

        joints = [shoulder_pos, elbow_pos_, wrist_pos_]
        dots   = VGroup(*[Dot(p, radius=0.08, color=RED) for p in joints])
        segs   = VGroup(
            Line(shoulder_pos, elbow_pos_, color=YELLOW, stroke_width=3.5),
            Line(elbow_pos_,   wrist_pos_, color=YELLOW, stroke_width=3.5),
        )
        labels_j = VGroup(
            Text("shoulder", font_size=13, color=GRAY_A).next_to(dots[0], UP,   buff=0.07),
            Text("elbow",    font_size=13, color=RED     ).next_to(dots[1], LEFT, buff=0.07),
            Text("wrist",    font_size=13, color=ORANGE  ).next_to(dots[2], DOWN, buff=0.07),
        )

        self.play(Create(segs), FadeIn(dots), FadeIn(labels_j))

        # angle arc at elbow
        vec_up   = shoulder_pos - elbow_pos_
        vec_down = wrist_pos_   - elbow_pos_
        ang_val  = np.degrees(np.arccos(
            np.dot(vec_up, vec_down) /
            (np.linalg.norm(vec_up) * np.linalg.norm(vec_down))
        ))
        arc = Arc(radius=0.35, angle=np.radians(ang_val),
                  start_angle=np.radians(270 - ang_val/2),
                  color=TEAL, stroke_width=2.5)
        arc.move_arc_center_to(elbow_pos_)

        angle_num = Text(f"{ang_val:.0f}°", font_size=20, color=TEAL)
        angle_num.move_to(elbow_pos_ + np.array([0.55, 0.1, 0]))

        self.play(Create(arc), FadeIn(angle_num))
        self.wait(0.6)

        # ── Step 2: plot angle over time ──
        step2 = Text("Step 2 – Plot angle over time → template curve",
                     font_size=22, color=YELLOW)
        step2.move_to(UP*2.0)
        self.play(
            FadeOut(step1), FadeIn(step2, shift=RIGHT*0.2),
            FadeOut(VGroup(segs, dots, labels_j, arc, angle_num))
        )

        # axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 150, 30],
            x_length=5.5,
            y_length=3.0,
            axis_config={"color": GRAY, "stroke_width": 1.8},
            tips=False,
        ).move_to(DOWN*0.3)

        x_lbl = Text("time (frames)", font_size=16, color=GRAY_A)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.2)
        y_lbl = Text("angle (°)", font_size=16, color=GRAY_A)
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI/2)

        self.play(Create(axes), FadeIn(x_lbl, y_lbl))

        # Template curve (smooth sine-like curl)
        template_fn = lambda t: 70 * np.sin(np.pi * t / 10) + 10
        template_curve = axes.plot(template_fn, x_range=[0, 10],
                                   color=GREEN, stroke_width=3)
        template_lbl = Text("Template (recorded rep)",
                            font_size=17, color=GREEN)
        template_lbl.move_to(axes.c2p(5, 90) + UP*0.4)

        self.play(Create(template_curve, run_time=1.8))
        self.play(FadeIn(template_lbl))
        self.wait(0.5)

        # ── Step 3: live curve vs template ──
        step3 = Text("Step 3 – Compare live rep against template",
                     font_size=22, color=YELLOW)
        step3.move_to(UP*2.0)
        self.play(FadeOut(step2), FadeIn(step3, shift=RIGHT*0.2))

        # live curve – slightly noisy & potentially exceeds threshold
        live_fn = lambda t: 68 * np.sin(np.pi * t / 10) + 10 + 8 * np.sin(3*t)
        live_curve = axes.plot(live_fn, x_range=[0, 10],
                               color=ORANGE, stroke_width=2.5,
                               stroke_opacity=0.9)
        live_lbl = Text("Live rep", font_size=17, color=ORANGE)
        live_lbl.move_to(axes.c2p(5, 110))

        self.play(Create(live_curve, run_time=2.0))
        self.play(FadeIn(live_lbl))

        # ROM threshold line
        threshold_y = 120
        thresh_line = axes.plot(lambda t: threshold_y, x_range=[0, 10],
                                color=RED, stroke_width=2,
                                )
        thresh_lbl = Text("Doctor's ROM limit", font_size=15, color=RED)
        thresh_lbl.move_to(axes.c2p(8.5, 128))

        self.play(Create(thresh_line), FadeIn(thresh_lbl))
        self.wait(0.4)

        # Nudge flash where live exceeds threshold
        nudge_dot = Dot(axes.c2p(2.5, 120), radius=0.12,
                        color=RED, fill_opacity=0.9)
        nudge_ring = Circle(radius=0.3, color=RED, stroke_width=2)
        nudge_ring.move_to(nudge_dot)
        nudge_txt  = Text("⚡ nudge!", font_size=18, color=RED_A)
        nudge_txt.next_to(nudge_dot, UP, buff=0.15)

        self.play(
            Flash(nudge_dot, color=RED, line_length=0.2, num_lines=10),
            GrowFromCenter(nudge_dot),
        )
        self.play(Write(nudge_txt))
        self.wait(1.5)

        # ── Final summary ──
        self.play(FadeOut(VGroup(
            header, step3, axes, x_lbl, y_lbl,
            template_curve, template_lbl,
            live_curve, live_lbl,
            thresh_line, thresh_lbl,
            nudge_dot, nudge_txt
        )))

        summary_lines = VGroup(
            Text("coords(x, y)  ──►  angle(°)",   font_size=26, color=BLUE_B),
            Text("angle(°) over time  ──►  template", font_size=26, color=GREEN),
            Text("template vs live  ──►  nudge / score", font_size=26, color=YELLOW),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(LaggedStart(
            *[Write(l) for l in summary_lines], lag_ratio=0.4
        ), run_time=2.2)
        self.wait(2)
        self.play(FadeOut(summary_lines))


# ─────────────────────────────────────────────────────────────────────────────
# Master scene – plays all acts in sequence
# ─────────────────────────────────────────────────────────────────────────────

class PhysioExplainer(Scene):
    def construct(self):
        for SceneCls in [S1_Title, S2_NormalFlow, S3_ProblemEinz,
                         S4_ProblemZwei, S5_Solution]:
            SceneCls.construct(self)