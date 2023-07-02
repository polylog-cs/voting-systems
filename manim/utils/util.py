# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from random import randrange
from re import I
from unittest import skip
from manim import config as global_config
from icecream import ic
import colorsys
from collections import Counter
from manim import *
from .util_general import *

DRAFT = False


def create_bubble(scale=1.0, color=text_color, length_scale=1, speaking=False):
    if speaking == True:
        return ImageMobject("img/bubble.jpeg").scale_to_fit_width(2)

    scale = scale / 200.0
    pos = ORIGIN - np.array([489.071, 195.644, 0.0]) * scale
    ret_objects = []

    c1 = (
        Circle(radius=28.5689 * scale, color=color)
        .move_to(np.array([489.071, 195.644, 0.0]) * scale)
        .shift(pos + 0.3 * UP)
    )
    print(c1.get_center())

    c2 = (
        Circle(radius=39.7392 * scale, color=color)
        .move_to(np.array([409.987, 274.728, 0.0]) * scale)
        .shift(pos + 0.15 * UP)
    )
    ret_objects += [c1, c2]

    pnts = [
        (373.367 * RIGHT + 366.776 * UP) * scale + pos,
        (503.717 * RIGHT + 453.873 * UP) * scale + pos,
        (464.612 * RIGHT + 613.847 * UP) * scale + pos,
        (340.78 * RIGHT + 643.472 * UP) * scale + pos,
        (131.628 * RIGHT + 596.072 * UP) * scale + pos,
        (174.288 * RIGHT + 388.106 * UP) * scale + pos,
    ]

    center = 0 * LEFT
    for i in range(len(pnts)):
        pnts[i] += (length_scale - 1) * (pnts[i] - pnts[0])[0] * RIGHT
        center += pnts[i]
    center /= len(pnts)

    angles = np.array([120, 170, 120, 120, 180, 120]) * 1.5707963267 / 90.0

    for i in range(len(pnts)):
        ret_objects.append(
            ArcBetweenPoints(
                pnts[i], pnts[(i + 1) % len(pnts)], angle=angles[i], color=color
            )
        )

    return Group(*ret_objects)  # , center


thm_scale = 0.8
gs_title = Tex("Gibbard-Satterthwaite Theorem:", color=text_color)
gs_tex = Tex(
    "{{Any }}{{reasonable }}{{voting system }}{{sometimes }}{{incentivizes strategic voting. }}",
    color=text_color,
).scale(thm_scale)
gs_group = (
    VGroup(gs_title, gs_tex)
    .arrange_in_grid(cols=1, cell_alignment=LEFT)
    .to_edge(UP, buff=0.5)
    .to_edge(LEFT)
)
gs_new_tex = Tex(
    r"{{For any number of voters, any number of candidates, consider any voting system that satisfies: \\ }}"
    + r"{{1) The system is not a dictatorship of one voter. \\}}"
    + r"{{2) At least three candidates are elected by the system in at least one scenario. \\}}"
    + r"There exists at least one scenario where the system incentivizes strategic voting. ",
    color=text_color,
).scale(thm_scale)

reasonable1_tex = Tex("{{Reasonable system: }}", color=TEXT_COLOR)
reasonable2_tex = Tex(
    r"{{\raggedright The candidate which is the first choice for majority\\ is always the winner. }}",
    color=TEXT_COLOR,
).scale(0.8)
reasonable_group = Group(reasonable1_tex, reasonable2_tex).arrange(RIGHT)

example_table_str = ["ABC", "ABC", "ABC", "ABC", "BCA", "BCA", "CAB", "CAB", "CAB"]

proof_table_strings = [example_table_str.copy()]
for i in range(4):
    new_str = proof_table_strings[-1].copy()
    new_str[i] = "BAC"
    proof_table_strings.append(new_str)

majority_table_str = ["BCA", "BAC", "BCA", "BAC", "BCA", "CAB", "CAB", "CAB", "CAB"]


def img_monkey(kind, voting=False, width=2):
    sc = 2
    if voting:
        votes_for_img = get_fruit(voting)  # TODO: replace with a banner
        votes_for_img.scale_to_fit_width(width / sc).shift(1 * LEFT + 1 * UP)
    else:
        votes_for_img = Dot().scale(0.0000001)

    kinds = {"A": "avocado", "B": "banana", "C": "coconut"}
    filename = f"img/monkeys/{kinds[kind]}{'_voting' if voting else ''}.png"
    monkey_img = ImageMobject(filename).scale_to_fit_width(width)
    return Group(monkey_img, votes_for_img)


def ordering(str, background = None):
    w = 0.4
    f1 = FRUITS[str[0]].copy().scale_to_fit_width(w)
    f2 = FRUITS[str[1]].copy().scale_to_fit_width(w)
    f3 = FRUITS[str[2]].copy().scale_to_fit_width(w)
    fruits = VGroup(f1, f2, f3).arrange(DOWN)

    border = SurroundingRectangle(fruits, corner_radius=0.2, color=text_color)
    if background != None:
        border.set_opacity(1.0)
        border.set_color(background)

    return VGroup(border, fruits)


class Fruit(VMobject):
    def __init__(self, label, normal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.singleton = normal
        self.add(normal)

    def gray(self):
        self.singleton.save_state()
        anims = []
        if self.singleton.submobjects:
            for subm in self.singleton.submobjects:
                color = subm.get_color()
                color.saturation = 0
                anims.append(subm.animate.set_color(color))
            return AnimationGroup(*anims)
        color = self.singleton.get_color()
        color.saturation = 0
        return self.singleton.animate.set_color(color)

    def ungray(self):
        return self.singleton.animate.restore()

    def fadeout(self):
        self.save_state()
        return self.animate.fade(0.9)

    def fadein(self):
        return self.animate.restore()

    def indicate(self):
        return Indicate(self, color=None)

    def highlight(self):
        return self.indicate()


FRUITS = [
    Fruit("A", load_svg("img/fruit/avocado.svg")),
    Fruit("B", load_svg("img/fruit/banana.svg")),
    Fruit("C", load_svg("img/fruit/coconut.svg")),
    Fruit(
        "D",
        VGroup(
            load_svg("img/fruit/avocado.svg"),
            Tex(r"/"),
            load_svg("img/fruit/banana.svg"),
        ).arrange(RIGHT),
    ),
    Fruit("?", Tex(r"?")),
]

if DRAFT:
    FRUITS = [
        Fruit(
            letter, Circle().set_stroke_width(0).set_fill(color, 1).scale((1, 1.28, 0))
        )
        for letter, color in (("A", GREEN), ("B", YELLOW), ("C", RED), ("?", GRAY))
    ]

FRUITS = {f.label: f.scale_to_fit_width(0.35) for f in FRUITS}


def get_fruit(label):
    return FRUITS[label].copy()


def get_crowned_fruit(label):
    fruit = get_fruit(label)
    crown = SVGMobject("img/crown.svg").scale_to_fit_width(fruit.width * 0.8)
    fruit_group = VGroup(crown, fruit).arrange(DOWN, buff=SMALL_BUFF)
    background = SurroundingRectangle(fruit_group, fill_opacity = 0.7, color = BACKGROUND_COLOR, corner_radius = 0.3)
    return VGroup(background, fruit_group)


def row_broadcast(fn):
    def inner(self, indexes, *args, **kwargs):
        l = []
        for f in self.at(indexes):
            l += [fn(f, *args, **kwargs)]
        return AnimationGroup(*l)

    return inner


class Preference(VMobject):
    # Those get generated automagically by the code below this class definition
    BROADCAST_METHODS = ["gray", "ungray", "fadeout", "fadein", "indicate", "highlight"]

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

    def rearrange(self, ordering):
        self.ordering = ordering
        positions = list(reversed(sorted(obj.get_y() for obj in self.group)))
        return AnimationGroup(
            *(
                self.at(label)[0].animate.set_y(positions[i])
                for i, label in enumerate(ordering)
            )
        )

    def push_down(self, label):
        ordering = list(self.ordering)
        ordering.remove(label)
        ordering.append(label)
        return self.rearrange(ordering)

    def highlight(self, *args, **kwargs):
        return self.indicate(*args, **kwargs)


for method in Preference.BROADCAST_METHODS:

    def create_broadcast(method):
        child_method = getattr(Fruit, method)

        def row_broadcast(self, indexes=None, *args, **kwargs):
            if indexes is None:
                indexes = range(len(self.group))
            l = []
            for f in self.at(indexes):
                l += [child_method(f, *args, **kwargs)]
            return AnimationGroup(*l)

        return row_broadcast

    setattr(Preference, method, create_broadcast(method))


class VotingResults(VMobject):
    scale_factor = 1
    is_hidden = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def scale(self, scale_factor, *args, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, *args, **kwargs)

    def hide(self):
        self.is_hidden = True

    def show(self, results):
        self.is_hidden = False


class VotingWinner(VotingResults):
    winner = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_to(self, *args, **kwargs):
        return self.winner.next_to(*args, **kwargs)

    def hide(self):
        super().hide()
        self.remove(self.winner)
        return FadeOut(self.winner)

    def show(self, winner):
        was_hidden = self.is_hidden
        super().show(winner)
        old_winner = self.winner
        self.winner = get_crowned_fruit(winner).scale(1.5).scale(self.scale_factor)
        if was_hidden:
            return FadeIn(self.winner)
        else:
            self.remove(old_winner)
            return AnimationGroup(
                FadeOut(old_winner, shift=UP), FadeIn(self.winner, shift=UP)
            )


class VotingOrdering(VotingResults):
    ordering = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_to(self, *args, **kwargs):
        return self.ordering.next_to(*args, **kwargs)

    def hide(self):
        super().hide()
        self.remove(self.ordering)
        return FadeOut(self.ordering)

    def show(self, ordering):
        was_hidden = self.is_hidden
        super().show(ordering)
        old_ordering = self.ordering
        fruits = [get_fruit(o).scale(self.scale_factor) for o in ordering]
        hor_buff = 0.3 * self.scale_factor
        if was_hidden:
            numbers = VGroup(
                *(
                    Tex(f"{i + 1}.").scale(1.5 * self.scale_factor)
                    for i, _ in enumerate(fruits)
                )
            ).arrange(DOWN, buff=0.5 * self.scale_factor)
            fruits = VGroup(*(get_fruit(f).scale(self.scale_factor) for f in ordering))
            for i, fruit in enumerate(fruits):
                fruit.next_to(numbers[i], buff=hor_buff)
            self.ordering = VGroup(numbers, fruits)
            return FadeIn(self.ordering)
        else:
            return AnimationGroup(
                *(
                    fruit.animate.next_to(
                        self.ordering[0][ordering.index(fruit.label)],
                        buff=hor_buff,
                    )
                    for fruit in self.ordering[1]
                )
            )

    def _ix(self, label_or_index):
        if type(label_or_index) == int:
            return label_or_index
        for i, m in enumerate(self.ordering[1]):
            if label_or_index == m.label:
                return i
        return None

    def at(self, ixs):
        is_single = type(ixs) == int or type(ixs) == str
        if is_single:
            ixs = [ixs]
        l = []
        for ix in ixs:
            ix = self._ix(ix)
            l.append((self.ordering[0][ix], self.ordering[1][ix]))
        return l

    def highlight(self, ixs):
        anims = []
        for _, f in self.at(ixs):
            anims.append(f.highlight())
        return anims


class VotingTable(VMobject):
    results = VotingWinner()
    num_of_voters = 9  # TODO
    scale_factor = 1
    # Those get generated automagically by the code below this class definition
    BROADCAST_METHODS = [
        "gray",
        "ungray",
        "fadeout",
        "fadein",
        "push_down",
        "rearrange",
        "indicate",
        "highlight",
    ]

    def __init__(self, preferences, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = VGroup()
        for preference in preferences:
            self.group.add(Preference(preference))
        self.C = len(preferences[0])
        self.group.arrange()
        self.arrow = None
        self.add(self.group)
        self.add(self.results)

    def _ixs(self, ixs):
        if ixs is None:
            ixs = range(len(self.group))
        if type(ixs) == int:
            ixs = [ixs]
        return ixs

    def __getitem__(self, i):
        return self.group[i]

    def scale(self, scale_factor, *args, **kwargs):
        self.scale_factor *= scale_factor
        self.results.scale(scale_factor)
        return super().scale(scale_factor, *args, **kwargs)

    def results_hide(self):
        self.remove(self.arrow)
        return AnimationGroup(self.results.hide(), FadeOut(self.arrow))

    def results_show(self, results):
        arrow = (
            MathTex("\Rightarrow")
            .scale(2 * self.scale_factor)
            .next_to(self.group, buff=0.5 * self.scale_factor)
        )
        if self.arrow is None:
            self.arrow = arrow
        else:
            self.arrow.become(arrow)
        anims = []
        if len(results) > 1 and not isinstance(self.results, VotingOrdering):
            anims.append(self.results.hide())
            self.results = VotingOrdering().scale(self.scale_factor)
        if len(results) == 1 and not isinstance(self.results, VotingWinner):
            anims.append(self.results.hide())
            self.results = VotingWinner().scale(self.scale_factor)
        if self.results.is_hidden:
            # self.add(self.arrow)
            anims.append(FadeIn(self.arrow))

        anims.append(self.results.show(results))
        self.results.next_to(self.arrow, buff=0.5 * self.scale_factor)
        return AnimationGroup(*anims)

    winner_show = results_show
    winner_hide = results_hide

    def results_change(self, results):
        # TODO
        return self.results_show(results)

    def candidates_by_votes(self):
        votes = [voter.ordering[0] for voter in self.group]
        ret = [a[0] for a in Counter(votes).most_common()]
        for candidate in self.group[0].ordering:
            if candidate not in ret:
                # got zero votes
                ret.append(candidate)
        return ret

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
        ret.append(self.results_show(winner))
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
        ret.append(self.results_show(winner))
        ret.append(AnimationGroup(*restore_anims))

        return ret

    def nejake_funkce_pro_mysli_si_X_ale_rika_Y(self):
        pass


for method in VotingTable.BROADCAST_METHODS:

    def create_broadcast(method):
        child_method = getattr(Preference, method)

        def column_broadcast(self, *args, indexes=None, **kwargs):
            anims = []
            for ix in self._ixs(indexes):
                anims.append(child_method(self.group[ix], *args, **kwargs))
            return anims

        return column_broadcast

    setattr(VotingTable, method, create_broadcast(method))


class Interpol(AnimationGroup):
    def __init__(self, mobject_old, mobject_new, **kwargs):
        # Call the parent constructor with the animations
        super().__init__(FadeOut(mobject_old), FadeIn(mobject_new), **kwargs)


def monkey_images():
    w = 1
    monkeys_img = [
        img_monkey(example_table_str[i][0], False, w)
        for i in range(len(example_table_str))
    ]

    monkeys_img[0].to_corner(DL).shift(0.1 * DOWN)
    monkeys_img[1].next_to(monkeys_img[0], RIGHT).shift(0.1*DOWN)
    monkeys_img[2].next_to(monkeys_img[1], RIGHT).shift(0.15  *UP)
    monkeys_img[3].next_to(monkeys_img[0], UR)

    monkeys_img[4].to_edge(DOWN).shift(1.5 * LEFT)
    monkeys_img[5].next_to(monkeys_img[4], RIGHT).shift(0.2*DOWN)

    monkeys_img[6].shift(4 * LEFT + 2 * UP).shift(0.2*UP + 0.5*RIGHT)
    monkeys_img[7].next_to(monkeys_img[6], RIGHT).shift(-0.1*RIGHT + 0.2*DOWN)
    monkeys_img[8].next_to(monkeys_img[7], RIGHT).shift(0.2*LEFT + 0.1*DOWN)

    monkeys_voting_img = [
        [
            img_monkey(example_table_str[i][0], example_table_str[i][j], w).align_to(
                monkeys_img[i], DR
            )
            for j in range(3)
        ]
        for i in range(len(example_table_str))
    ]

    orderings = [
        ordering("ABC", background=BACKGROUND_COLOR).next_to(monkeys_img[3], RIGHT),
        ordering("BCA", background=BACKGROUND_COLOR).next_to(monkeys_img[5], RIGHT),
        ordering("CAB", background=BACKGROUND_COLOR).next_to(monkeys_img[8], RIGHT),
    ]

    explorer = (
        ImageMobject("img/explorer.png")
        .scale_to_fit_height(5)
        .to_corner(DR)
        .shift(2 * LEFT + 0.4*DOWN)
    )  # TODO pridat polylogo na laptop

    background = ImageMobject("img/background-upscaled.png").scale_to_fit_width(
        config.frame_width
    )

    return monkeys_img, monkeys_voting_img, orderings, explorer, background