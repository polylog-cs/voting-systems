# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from random import randrange
from re import I
from unittest import skip
from manim import config as global_config
from icecream import ic
import colorsys
from collections import Counter
from utils.util_general import *

thm_scale = 0.8
gs_title = Tex("Gibbard-Satterthwaite Theorem:", color=text_color)
gs_tex = Tex(
    "{{Any }}{{reasonable }}{{voting system }}{{sometimes }}{{incentivizes strategic voting. }}",
    color=text_color,
).scale(thm_scale)
gs_group = (
    Group(gs_title, gs_tex)
    .arrange_in_grid(cols=1, cell_alignment=LEFT)
    .to_edge(UP, buff=0.5)
    .to_edge(LEFT)
)
gs_new_tex = Tex(
    r"{{For any number of voters, any number of candidates, consider any voting system that satisfies: \\ }}"
    + r"{{1) The system is not a dictatorship of one voter. }}"
    + r"{{2) At least three candidates are elected by the system in at least one scenario. }}"
    + r"There exists at least one scenario where the system incentivizes strategic voting. ",
    color=text_color,
).scale(thm_scale)


example_table_str = ["ABC", "ABC", "BCA", "BCA", "BCA", "CAB", "CAB", "CAB", "CAB"]


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
        Fruit("D", Circle(color=BLUE).set_fill(BLUE, 1).scale(0.4)),
    )
}


def get_fruit(label):
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

    def highlight(self, label):  # TODO
        return Wait()


def column_broadcast(fn):
    def inner(self, *args, indexes=None, **kwargs):
        anims = []
        for ix in self._ixs(indexes):
            anims.append(fn(self.group[ix], *args, **kwargs))
        return anims

    return inner


class VotingTable(VMobject):
    winner = None
    num_of_voters = 9  # TODO

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

    def create_resulting_ranking(self, str):
        # u Arrow je vysledek ne jeden kandidat ale order
        pass

    def rearrange_resulting_ranking(self, str):
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


class Reasonable(Scene):
    def construct(self):
        default()

        line = Line(start=10 * LEFT, end=10 * RIGHT, color=text_color).next_to(
            gs_group, DOWN
        )
        self.add(gs_group, line)
        gs_new_tex.move_to(gs_tex.get_center()).align_to(gs_tex, UP)

        #         There is an elephant in the room though - our definition of a reasonable voting system. Remember, we postulated that for example in this scenario, every reasonable system has to elect X, because more than half of the voters have X as their top choice.

        # reasonable_tex = Tex(r"Reasonable = ")
        table = VotingTable(
            ["ABCD", "ABCD", "ABCD", "ABCD", "ABCD", "BCDA", "BCDA", "BCDA", "BCDA"]
        )

        self.play(FadeIn(table))
        self.wait()

        self.play(table.winner_show("A"))
        self.wait()

        self.play(*[table[i].highlight("A") for i in range(5)])
        self.wait()

        # But X is also the bottom choice for almost half of the voters so isn’t Y also a good candidate for the winner? There are in fact some popular voting systems [ See Borda count] that would elect Y in this scenario.

        self.play(*[table[i].highlight("A") for i in range(5, table.num_of_voters)])
        self.wait()

        self.play(*[table[i].highlight("B") for i in range(table.num_of_voters)])
        self.wait()

        # So maybe we should think about the theorem one more time and try to prove it with a definition of “reasonable” that permits as many voting systems as possible. That is exactly what Gibbard and Satterthwaite did, this is their theorem in full glory. They found out that these two conditions on the voting system suffice to prove the theorem, and they are also necessary. The proof of this more general theorem is similar to our proof but more tedious, so let’s skip it.

        self.play(FadeOut(gs_tex))
        self.wait()
        self.play(FadeIn(gs_new_tex), line.animate.next_to(gs_new_tex, DOWN))
        self.wait()

        self.play(Circumscribe(Group(*gs_new_tex[1:3]), color=RED))
        self.wait()

        self.play(FadeOut(gs_new_tex))
        self.wait()
        self.play(FadeIn(gs_tex), line.animate.next_to(gs_tex, DOWN))
        self.wait()


class Arrow(Scene):
    def construct(self):
        default()
        # There is one more related theorem I want to mention – Arrow’s theorem.

        self.add(gs_group)
        arrow_title = Tex(r"Arrow's theorem:")
        arrow_tex = Tex(
            r"{{Any reasonable voting system doesn't satisfy the }}{{\emph{independence of irrelevant alternatives}. }}"
        ).scale(thm_scale)
        arrow_full = (
            Group(arrow_title, arrow_tex)
            .arrange_in_grid(cols=1, cell_alignment=LEFT)
            .next_to(gs_group, DOWN, buff=0.5)
            .to_edge(LEFT)
        )

        self.play(FadeIn(arrow_title))
        self.wait()

        # That theorem also talks about voting systems, but a little bit more general ones that not only elect the winner but rank all the candidates from best to worst.

        table = VotingTable(example_table_str)

        self.play(FadeIn(table))
        self.wait()

        self.play(table.create_resulting_ranking("CBA"))
        self.wait()

        # (animace s tabulkou, outcome se změní z vítěze na order)

        # Arrow’s theorem says that if there are at least three candidates, any reasonable voting system for ordering them will not satisfy the so-called independence of irrelevant alternatives.

        self.play(FadeIn(arrow_tex))
        self.wait()

        # This is a condition that says that if you look at how the voting system orders any two candidates, for example here it decides that banana is above coconut

        self.play(table.vysledne_poradi.highlight("B"))
        self.wait()
        self.play(table.vysledne_poradi.highlight("C"))
        self.wait()

        # (vyznačí se že outcome je banana lepší než coconut nebo naopak)

        # this decision should not depend on whatever the voters’ opinion on the avocado is.

        self.play(*table.gray("A"))
        self.wait()

        # In other words, in all of these situations, the banana has to be above the coconut.
        # [animace kde avocado skáče nahoru a dolu u různých voterů, outcome je furt banana lepší než coconut]

        self.play(
            Succession(
                AnimationGroup(table[0].rearrange("ABC")),
                AnimationGroup(
                    table[1].rearrange("ABC"), table.vysledne_poradi.rearrange("BAC")
                ),
                AnimationGroup(table[2].rearrange("ABC")),
            )
        )

        # The first part of our proof can actually be used to prove a version of Arrow’s theorem, but if you use the textbook definition of a reasonable voting system, the proof again becomes a bit tedious.

        self.play(
            *[
                table[i].rearrange(example_table_str[i])
                for i in range(len(example_table_str))
            ]
        )

        for _ in range(2):
            self.play(
                *[table[i].rearrange("ABC") for i in range(5, 9)],
                table.vysledne_poradi.rearrange("ABC")
            )
            self.wait()
            self.play(
                *[table[i].rearrange("CAB") for i in range(5, 9)],
                table.vysledne_poradi.rearrange("CBA")
            )
            self.wait()

        # Both Arrow and Gibbard-Satterthwaite theorems are good examples showing that while we often like to think that important mathematical theorems are simply-looking statements that turn out to be insanely complicated to prove, it is not always like that.
        # (možná někde problikne statement Fermata nebo P vs NP?)

        self.play(FadeOut(table))
        self.wait()

        fermat_tex = Tex(
            r"$a^n + b^n \not= c^n, n > 2$ \\ does not have solutions in $\mathbb{N}$"
        )
        pnp_tex = Tex(r"Does P = NP?")
        self.play(
            Succession(
                FadeIn(fermat_tex),
                FadeIn(pnp_tex),
                Wait(),
                FadeOut(fermat_tex),
                FadeOut(pnp_tex),
                Wait(),
            )
        )
        # For me, the biggest insight of those two theorems is simply noticing that there is something to prove. Strategic voting is not just a sociological fact, but it is a fundamental flaw of every voting system, and so is the lack of independence of irrelevant alternatives. Or is it?

        self.play(Indicate(gs_tex[4], color=text_color))
        self.wait()
        self.play(Indicate(arrow_tex[1], color=text_color))
        self.wait()

        # [vsauce pauza + trošku zoom?]


class Approval(Scene):
    def construct(self):
        default()

        # It turns out that the full story is more complicated; to understand why, let’s look at one popular voting system called approval voting. This is an extremely simple voting system where every voter can give a vote to as many candidates as they want and then you order the candidates by how many votes they got.

        nothing = Dot().scale(0.00001)
        thumbsup_img = SVGMobject("img/icon.svg").scale(0.3)
        monkey_scale = 0.3
        monkey_img1 = ImageMobject("img/monkeys/avocado1.png").scale(monkey_scale)
        monkey_img2 = ImageMobject("img/monkeys/avocado1.png").scale(monkey_scale)
        monkey_img3 = ImageMobject("img/monkeys/avocado1.png").scale(monkey_scale)
        fruit_width = 1
        avocado_img = ImageMobject("img/fruit/avocado.png").scale_to_fit_width(
            fruit_width
        )
        banana_img = ImageMobject("img/fruit/banana.png").scale_to_fit_width(
            fruit_width
        )
        coconut_img = ImageMobject("img/fruit/coconut.png").scale_to_fit_width(
            fruit_width
        )
        # self.add(thumbsup_img)

        approval_data = [
            [
                nothing.copy(),
                monkey_img1.copy(),
                monkey_img2.copy(),
                monkey_img3.copy(),
                monkey_img1.copy(),
                monkey_img1.copy(),
                monkey_img1.copy(),
                Tex("Sum"),
            ],
            [
                avocado_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                Tex("5"),
            ],
            [
                banana_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                nothing.copy(),
                nothing.copy(),
                Tex("2"),
            ],
            [
                coconut_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                Tex("3"),
            ],
        ]
        approval_table = Group(
            *[item for row in approval_data for item in row]
        ).arrange_in_grid(rows=4, buff=0.1)

        self.play(
            Succession(
                *[
                    AnimationGroup(*[FadeIn(approval_data[i][j]) for i in range(4)])
                    for j in range(len(approval_data[0]))
                ]
            )
        )
        self.wait()

        # TODO hezky udelat posledni sloupec a preskladat radky podle poctu hlasu

        self.play(FadeOut(approval_table))
        self.wait()

        # For example, if you order the videos of your favorite YouTuber by popularity, one way you can do it is by sorting them by how many likes they got, and that is basically approval voting, with the addition of negative votes.

        v_width = 2
        v_scale = 0.7
        videos_data = []

        for str1, str2 in [
            ["img/thumbnail1.png", "10k likes"],
            ["img/thumbnail2.png", "10k likes"],
            ["img/thumbnail3.png", "10k likes"],
            ["img/thumbnail1.png", "10k likes"],
        ]:
            img = ImageMobject(str1).scale_to_fit_width(v_width)
            border = SurroundingRectangle(img, color=GRAY, buff=0)
            tex = Tex(str2).scale(v_scale)
            videos_data.append(Group(Group(img, border), tex).arrange(DOWN))

        videos_group = Group(*videos_data).arrange_in_grid(cols=2)

        self.play(FadeIn(videos_group))
        self.wait()

        self.play(videos_group.animate.arrange(DOWN).shift(3 * LEFT))
        self.wait()

        # The way we order movies by their average rating is also similar to approval voting.
        # [třeba: pár videí od polylogu a u nich napsané kolik mají liků, potom záběr na imdb/netflix a nějaký seznam top filmů]

        self.play(FadeOut(videos_group))
        self.wait()

        # But notice that approval voting and its variants do not fit our definition that a voting system requires every voter to simply rank the candidates on the ballot and uses this information

        table = VotingTable(example_table_str).scale(0.5)  # .to_edge(RIGHT, buff = 2)

        self.play(
            Succession(
                *[Indicate(table[i]) for i in range(table.num_of_voters)], lag_ratio=0.5
            )
        )
        self.wait()

        # to elect the winner.

        self.play(table.winner_show("A"))
        self.wait()
        self.play(FadeOut(table))
        self.wait()

        # Even if I tell you how I would rank these videos, you still don’t know which ones of them I would give a like to.

        # for v in videos_group:
        #     v.generate_target()
        # videos_group2 = Group(*[videos_data[i].target for i in [3, 2, 1, 0]]).arrange(DOWN).move_to(videos_group.get_center())

        # self.play(
        #     *[MoveToTarget(v) for v in videos_group]
        # )
        # self.wait()

        self.play(FadeIn(videos_group))
        self.wait()

        arrow = (
            Tex(r"$\overset{?}{\rightarrow}$")
            .scale(3)
            .next_to(videos_group, RIGHT, buff=1)
        )

        likes = []
        dislikes = []
        for i in range(len(videos_group)):
            like = thumbsup_img.copy().next_to(arrow, RIGHT, buff=1)
            like.shift((videos_group[i].get_center()[1] - like.get_center()[1]) * UP)
            likes.append(like)
            dislike = thumbsup_img.copy().rotate(PI).next_to(arrow, RIGHT, buff=1)
            dislike.shift(
                (videos_group[i].get_center()[1] - dislike.get_center()[1]) * UP
            )
            dislikes.append(dislike)

        # [mám furt těch samých pár videí od polylogu, pripadne 3B1B, seřadí se a ukazují se různé možnosti jestli dám like jen prvnímu, prvním dvěma, atd.Like může být palec nahoru. Můžeme mít i dislike]

        self.play(FadeIn(arrow))
        self.wait()

        self.play(
            Succession(
                AnimationGroup(FadeIn(likes[0])),
                AnimationGroup(FadeIn(likes[1])),
                AnimationGroup(FadeIn(dislikes[3])),
            )
        )
        self.wait()

        self.play(
            FadeOut(arrow),
            *[v[1].animate.set_color(BACKGROUND_COLOR) for v in videos_group],
            *[FadeOut(o) for o in (set(likes + dislikes) & set(self.mobjects))]
        )
        self.play(Group(*[g for g in videos_group]).animate.arrange_in_grid(rows=2))
        self.wait()

        # So, our proofs of Arrow and Gibbard-Satterthwaite don't directly apply to these types of voting systems. And actually, Arrow’s theorem cannot hold there, because approval voting does satisfy the independence of irrelevant alternatives: If I tell you that [video] got X likes and [video] got Y likes, you know that in the final ranking, [video] will be above [video] and this conclusion is not affected by how many likes all the other videos got. So Arrow’s theorem may not be as fundamental as it looked like.

        i1 = 1
        i2 = 3

        self.play(videos_group[i1].animate.move_to(2 * RIGHT + 1.5 * UP))
        self.wait()
        self.play(videos_group[i1][1].animate.set_color(text_color))
        self.wait()
        self.play(videos_group[i2].animate.move_to(2 * RIGHT + 1.5 * DOWN))
        self.wait()
        self.play(videos_group[i2][1].animate.set_color(text_color))
        self.wait()

        greater_tex = (
            Tex(r"$<$")
            .rotate(PI / 2.0)
            .move_to(
                videos_group[i1].get_center() / 2.0
                + videos_group[i2].get_center() / 2.0
            )
        )
        self.play(FadeIn(greater_tex))
        self.wait()

        for v in videos_group:
            v.generate_target()

        new_videos_group = (
            Group(*[videos_group[i].target for i in [3, 2, 1, 0]])
            .arrange(DOWN)
            .move_to(greater_tex.get_center())
        )
        self.play(FadeOut(greater_tex))
        self.play(*[MoveToTarget(v) for v in videos_group])
        self.play(*[v[1].animate.set_color(text_color) for v in videos_group])
        self.wait()

        # However, even the approval voting system sometimes incentivizes strategic voting! For example, if you really want this video to become our most liked video, but you see that currently, it is only the fifth one, you should first give it a like (and subscribe!). But then you should also dislike all the videos above it, regardless of your opinion of them. You can in fact generalize Gibbard-Satterthwaite theorem so that it applies to pretty much every voting system, so, unfortunately, in one way or another, strategic voting will always be with us.

        self.play(videos_group.animate.move_to(ORIGIN))
        self.wait()

        i_like = 1
        self.play(FadeIn(thumbsup_img.copy().next_to(videos_group[i_like])))
        self.wait()

        self.play(
            *[
                FadeIn(thumbsup_img.copy().rotate(PI).next_to(videos_group[i]))
                for i in range(len(videos_group))
                if videos_group[i].get_center()[1]
                > videos_group[i_like].get_center()[1]
            ]
        )
        self.wait()


class Debriefing(Scene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)

        # But how big of a problem is it, actually? First of all, there are many situations where strategic voting is not really the main concern. For example, when you want to rank movies or entries to a math exposition contest, how well the voting system scales with the number of candidates is probably a bigger issue than strategic voting.
        # https://www.3blue1brown.com/blog/some2
        # https://www.youtube.com/playlist?list=PLnQX-jgAF5pTZXPiD8ciEARRylD9brJXU

        w = 5
        some_left_img = ImageMobject("img/some1-small.png").scale_to_fit_width(w)
        some_leftleft_img = ImageMobject("img/some1left.png").scale_to_fit_width(
            w * 0.3
        )
        some_right_img = ImageMobject("img/some2-small.png").scale_to_fit_width(w)
        Group(some_left_img, some_right_img).arrange(RIGHT)
        some_left_img.to_edge(UP)
        some_right_img.to_edge(UP)
        some_leftleft_img.align_to(some_left_img, UL).shift(
            w * 0.065 * RIGHT + w * 0.06 * DOWN
        )

        self.add(some_left_img, some_leftleft_img, some_right_img)

        self.play(
            some_left_img.animate.to_edge(DOWN),
            some_right_img.animate.to_edge(DOWN),
            run_time=7,
        )
        self.wait()
        self.play(
            FadeOut(some_left_img),
            FadeOut(some_leftleft_img),
            FadeOut(some_right_img),
        )
        self.wait()

        # But even in political elections, it is good to remember what Kenneth Arrow said about his own theorem:

        arrow_img = ImageMobject("img/arrow.jpg").scale_to_fit_width(3)
        arrow_tex = Tex("Kenneth Arrow")
        arrow_group = Group(arrow_img, arrow_tex).arrange(DOWN)

        quote_tex = Tex(
            r"Most systems are not going to work badly all of the time. \\ All I proved is that all can work badly at times."
        )
        Group(quote_tex, arrow_group).arrange(DOWN, buff=1)

        self.play(FadeIn(arrow_group))
        self.play(Write(quote_tex))
        self.wait()
        self.play(FadeOut(arrow_group), FadeOut(quote_tex))
        self.wait()

        # Some systems actually work pretty well most of the time - imagine political elections based on approval voting and try to come up with a plausible scenario where a lot of people would vote strategically - it is actually not so easy!

        # TODO

        # Some time back, a small group of voting theorists ranked the voting systems on how good they are for political elections and approval voting actually ended up on the top.
        self.next_section(skip_animations=False)

        voting_data = [
            [Tex("Position"), Tex("Method"), Tex("Approval votes")],
            [Tex("1"), Tex("Approval voting"), Tex("15")],
            [Tex("2"), Tex(r"Alternative vote\\ (Instant runoff)"), Tex("10")],
            [Tex("3"), Tex("Copeland's method"), Tex("9")],
            [Tex("4"), Tex("Kemeny-Young method"), Tex("8")],
            [Tex("5"), Tex("Two-round system"), Tex("6")],
            [Tex("5"), Tex("Coombs' method"), Tex("6")],
            [Tex("7"), Tex("Minimax"), Tex("5")],
            [Tex("7"), Tex("Majority judgement"), Tex("5")],
            [Tex("9"), Tex("Borda count"), Tex("4")],
            [Tex("10"), Tex("Black's method"), Tex("3")],
            [Tex("11"), Tex("Range voting"), Tex("2")],
            [Tex("11"), Tex("Nanson's method"), Tex("2")],
            [Tex("13"), Tex("Leximin method"), Tex("1")],
            [Tex("13"), Tex("Smith's method"), Tex("1")],
            [Tex("13"), Tex("Uncovered set method"), Tex("1")],
            [Tex("16"), Tex("Fishburn's method"), Tex("0")],
            [Tex("16"), Tex("Untrapped set"), Tex("0")],
            [Tex("16"), Tex("Plurality voting"), Tex("0")],
        ]

        voting_group = (
            Group(*[o for l in voting_data for o in l])
            .scale(1)
            .arrange_in_grid(cols=3)
            .to_edge(UP)
            .shift(1 * DOWN)
        )

        self.play(FadeIn(*[element for row in voting_data for element in row[:2]]))
        self.wait()

        self.play(Circumscribe(Group(*voting_data[1][0:2]), color=RED))
        self.wait()

        # You might be wondering, "Okay, but which voting system did they use to compile this list?" and it was, well, approval voting itself… [reveal the right column of the table - approval votes for each option].

        obama_img = ImageMobject("img/obama.webp").scale_to_fit_width(8)
        self.play(FadeIn(obama_img))
        self.wait()
        self.play(FadeOut(obama_img))
        self.wait()

        # In any case, just based on the number of votes for each option, you can really see that there are some good voting systems like approval voting; another very popular one is the alternative vote a.k.a. instant runoff. Then there are some decent ones, like the two-round system, a lot of mediocre ones, and then, at the very bottom with zero approval votes, we see plurality voting, which did you know is used for elections in most English-speaking countries?

        self.play(FadeIn(*[row[2] for row in voting_data]))
        self.wait()

        self.play(
            Circumscribe(
                Group(*[voting_data[i][2] for i in range(1, len(voting_data))]),
                color=RED,
            )
        )
        self.wait()

        arrow = (
            ImageMobject("img/arrow.png")
            .scale_to_fit_width(1.5)
            .next_to(voting_data[1][0], LEFT, buff=0.5)
        )
        self.play(FadeIn(arrow))
        self.wait()
        self.play(
            voting_group.animate.shift(
                voting_data[1][0].get_center() - voting_data[2][0].get_center()
            )
        )
        self.wait()

        self.play(
            voting_group.animate.shift(
                voting_data[2][0].get_center() - voting_data[5][0].get_center()
            )
        )
        self.wait()

        self.play(
            voting_group.animate.shift(
                voting_data[5][0].get_center() - voting_data[-1][0].get_center()
            )
        )
        self.wait()

        bush_gore_table = (
            Group(
                Tex("Bush:"),
                Tex("2\,912\,790"),
                Tex("Gore:"),
                Tex("2\,912\,253"),
                Tex("Nader:"),
                Tex("97\,488"),
            )
            .arrange_in_grid(cols=2)
            .shift(2 * DOWN)
        )

        self.play(FadeIn(bush_gore_table))
        self.wait()

        self.play(FadeOut(bush_gore_table))
        self.wait()

        self.play(FadeOut(voting_group), FadeOut(arrow))
        self.wait()

        self.next_section(skip_animations=False)

        shame_list = [
            "Azerbaijan",
            "Bangladesh",
            "Belize",
            "Bhutan",
            "Botswana",
            "Burma",
            "Canada",
            "Congo",
            "Cote d'Ivoire",
            "Eritrea",
            "Ethiopia",
            "Gabon",
            "Gambia",
            "Ghana",
            "India",
            "Iran",
            "Jamaica",
            "Kenya",
            "Kuwait",
            "Laos",
            "Liberia",
            "Malawi",
            "Malaysia",
            "Maldives",
            "Nigeria",
            "Oman",
            "Sierra Leone",
            "Singapore",
            # "Solomon Islands",
            "Swaziland",
            "Tanzania",
            "Uganda",
            "United Kingdom",
            "United States",
            "Yemen",
            "Zambia",
        ]

        shame_table = Group(
            *[Tex(str).scale(0.7) for str in shame_list]
        ).arrange_in_grid(cols=5)
        Group(*shame_table[20:]).shift(1.0 * DOWN)
        Group(*shame_table[:20]).shift(1.5 * UP)
        shame_tex = Tex("Shame.", font_size=300)

        self.play(
            AnimationGroup(
                Succession(*[FadeIn(o) for o in shame_table], lag_ratio=0.2),
                AnimationGroup(FadeIn(shame_tex), run_time=10),
            )
        )
        self.wait()
        return

        self.wait()


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
