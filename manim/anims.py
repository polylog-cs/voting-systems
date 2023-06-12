# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from random import randrange
from re import I
from unittest import skip
from manim import config as global_config
from icecream import ic
import colorsys
from collections import Counter
from utils.util_general import *


class Fruit(VMobject):
    def __init__(self, label, normal, gray: VMobject = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self._normal = normal
        if gray is None:
            color = normal.get_color()
            color.saturation = 0
            gray = normal.copy().set_color(color)
        self._gray = gray
        self._faded = normal.copy().fade(0.9)
        self.add(self._normal)

    def gray(self):
        self._gray.move_to(self._normal)
        self._normal.save_state()
        return self._normal.animate.become(self._gray)

    def ungray(self):
        return self._normal.animate.restore()

    def fadeout(self):
        self._faded.move_to(self._normal)
        self._normal.save_state()
        return self._normal.animate.become(self._faded)

    def fadein(self):
        return self._normal.animate.restore()

    def indicate(self):
        return Indicate(self, color=None)


FRUITS = {
    f.label: f
    for f in (
        Fruit("A", Circle(color=GREEN).set_fill(GREEN, 1).scale(0.4)),
        Fruit("B", Square(color=YELLOW).set_fill(YELLOW, 1).scale(0.4)),
        Fruit("C", Square(color=RED).set_fill(RED, 1).scale(0.4)),
    )
}


def get_fruit(label):
    assert label in list("ABC")
    return FRUITS[label].copy()


def row_broadcast(fn):
    def inner(self, indexes, *args, **kwargs):
        l = []
        for f in self.at(indexes):
            l += [fn(f, *args, **kwargs)]
        return AnimationGroup(*l)

    return inner


class Preference(VMobject):
    def __init__(self, ordering, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = VGroup()
        for label in ordering:
            fruit = get_fruit(label)
            self.group.add(fruit)
        self.ordering = ordering
        self.group.arrange(DOWN)
        self.add(self.group)

    def _ix(self, label_or_index):
        if type(label_or_index) == int:
            return label_or_index
        for i, m in enumerate(self.group):
            if label_or_index == m.label:
                return i
        return None

    def at(self, ixs):
        is_single = type(ixs) == int or type(ixs) == str
        if is_single:
            ixs = [ixs]
        l = []
        for ix in ixs:
            l.append(self.group[self._ix(ix)])
        return l

    @row_broadcast
    def gray(cell):
        return cell.gray()

    @row_broadcast
    def ungray(cell):
        return cell.ungray()

    @row_broadcast
    def fadeout(cell):
        return cell.fadeout()

    @row_broadcast
    def fadein(cell):
        return cell.fadein()

    @row_broadcast
    def indicate(cell):
        return cell.indicate()

    def rearrange(self, ordering):
        self.ordering = ordering
        positions = list(reversed(sorted(obj.get_y() for obj in self.group)))
        return [
            self.at(label)[0].animate.set_y(positions[i])
            for i, label in enumerate(ordering)
        ]

    def push_down(self, label):
        ordering = list(self.ordering)
        ordering.remove(label)
        ordering.append(label)
        return AnimationGroup(*self.rearrange(ordering))


def column_broadcast(fn):
    def inner(self, *args, indexes=None, **kwargs):
        anims = []
        for ix in self._ixs(indexes):
            anims.append(fn(self.group[ix], *args, **kwargs))
        return anims

    return inner


class VotingTable(VMobject):
    winner = None

    def __init__(self, preferences, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = VGroup()
        for preference in preferences:
            self.group.add(Preference(preference))
        self.C = len(preferences[0])
        self.group.arrange()
        self.arrow = MathTex("\Rightarrow").scale(1.5).next_to(self.group, buff=0.5)
        self.arrow.shown = False
        self.add(self.group)

    def _ixs(self, ixs):
        if ixs is None:
            ixs = range(len(self.group))
        if type(ixs) == int:
            ixs = [ixs]
        return ixs

    @column_broadcast
    def gray(col, label):
        return col.gray(label)

    @column_broadcast
    def ungray(col, label):
        return col.ungray(label)

    @column_broadcast
    def fadeout(col, label):
        return col.fadeout(label)

    @column_broadcast
    def fadein(col, label):
        return col.fadein(label)

    @column_broadcast
    def push_down(col, label):
        return col.push_down(label)

    def __getitem__(self, i):
        return self.group[i]

    def winner_hide(self):
        winner = self.winner
        self.winner = None
        return FadeOut(winner, self.arrow)

    def winner_show(self, winner):
        old_winner = self.winner
        self.winner = get_fruit(winner).next_to(self.arrow, buff=0.5)
        if old_winner is None:
            return FadeIn(self.winner, self.arrow)
        else:
            return AnimationGroup(
                FadeOut(old_winner, shift=UP), FadeIn(self.winner, shift=UP)
            )

    def create_resulting_ranking(self):
        # u Arrow je vysledek ne jeden kandidat ale order
        pass

    def change_resulting_ranking(self):
        # u Arrow je vysledek ne jeden kandidat ale order
        pass

    def candidates_by_votes(self):
        votes = [voter.ordering[0] for voter in self.group]
        return [a[0] for a in Counter(votes).most_common()]

    def plurality_system(self):
        # zahraje animaci co se pusti pri vysvetleni plurality vote.
        # treba neco jako nejdriv ctverecek kolem top choice u kazdeho volice
        # a pak ctverecek jen kolem pluralitniho a pak se zobrazi winner nebo tak neco
        ret = []
        ret.append(AnimationGroup(*self.gray(range(1, self.C))))
        winner = self.candidates_by_votes()[0]
        anims = []
        for col in self.group:
            if col.ordering[0] != winner:
                continue
            anims.append(col.at(0)[0].indicate())
        ret.append(AnimationGroup(*anims))
        ret.append(self.winner_show(winner))
        return ret

    def two_round_system(self):
        ret = []
        top = self.candidates_by_votes()
        top2 = top[:2]
        ret.append(AnimationGroup(*self.gray(range(1, self.C))))
        ret.append(
            AnimationGroup(
                *(
                    col.at(0)[0].indicate()
                    for col in self.group
                    if col.ordering[0] == top2[0]
                )
            )
        )
        ret.append(
            AnimationGroup(
                *(
                    col.at(0)[0].indicate()
                    for col in self.group
                    if col.ordering[0] == top2[1]
                )
            )
        )
        ret.append(AnimationGroup(*self.ungray(range(1, self.C))))
        ret.append(AnimationGroup(*self.fadeout(top[2:])))
        winner = Counter(
            [[c for c in col.ordering if c in top2][0] for col in self.group]
        ).most_common()[0][0]
        anims = []
        winner_anims = []
        restore_anims = []
        for col in self.group:
            found = False
            for a in col.ordering:
                if a not in top2:
                    continue
                if not found:
                    found = True
                    if a == winner:
                        winner_anims.append(col.indicate(a))
                else:
                    anims.append(col.gray(a))
                    restore_anims.append(col.ungray(a))
        restore_anims += self.fadein(top[2:])
        ret.append(AnimationGroup(*anims))
        ret.append(AnimationGroup(*winner_anims))
        ret.append(self.winner_show(winner))
        ret.append(AnimationGroup(*restore_anims))

        return ret

    def nejake_funkce_pro_mysli_si_X_ale_rika_Y(self):
        pass


class Polylogo(Scene):
    def construct(self):
        default()
        authors = Tex(
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)
        channel_name_without_o = Tex(r"p\hskip 5.28pt lylog", color=text_color)
        channel_name_without_o.scale(4).shift(1 * UP)

        logo_solarized = (
            SVGMobject("img/logo-solarized.svg")
            .scale(0.55)
            .move_to(2 * LEFT + 0.95 * UP + 0.49 * RIGHT)
        )
        self.play(
            Write(authors),
            Write(channel_name),
        )
        self.play(FadeIn(logo_solarized))
        self.add(channel_name_without_o)
        self.remove(channel_name)

        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


class Playground(Scene):
    def construct(self):
        default()
        table = VotingTable(["ABC", "BCA", "CAB", "ABC", "BCA", "ABC"])
        self.add(table)
        self.wait(1)
        anims = table.two_round_system()
        for anim in anims:
            self.play(anim)
        self.wait(10)


class Explore(Scene):
    def construct(self):
        table = VotingTable(["ABC", "BCA", "ACB"])
        self.add(table)
        self.wait(1)
        self.play(*table[0].rearrange("CAB"), *table[1].rearrange("CAB"))
        self.wait(1)
        self.play(*table.push_down("A"))
        self.wait(1)
        self.play(*table.gray("C"))
        self.wait(1)
        self.play(*table.gray("A"))
        self.wait(1)
        self.play(*table.ungray("C"))
        self.wait(1)
        self.play(*table.ungray("A"))
        self.wait(1)

        self.play(table.animate.shift(1 * RIGHT + 2 * UP))
        table2 = table.copy()
        self.play(table2.animate.shift(4 * DOWN))
        self.play(*table.push_down("B"))
        self.play(*table2[0].rearrange("BCA"))
        self.wait(10)
