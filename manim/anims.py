# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from random import randrange
from re import I
from unittest import skip
from manim import config as global_config
from icecream import ic
import colorsys
from collections import Counter
from utils.util_general import *


def create_bubble(scale = 1.0, color = text_color, length_scale = 1, speaking = False):
    if speaking == True:
        return ImageMobject("img/bubble.jpeg").scale_to_fit_width(2)
    
    scale = scale / 200.0
    pos = ORIGIN - np.array([489.071, 195.644, 0.0])*scale
    ret_objects = []

    c1 = Circle(
        radius = 28.5689 * scale,
        color = color
    ).move_to(np.array([489.071, 195.644, 0.0])*scale).shift(pos + 0.3*UP)
    print(c1.get_center())

    c2 = Circle(
        radius = 39.7392 * scale,
        color = color
    ).move_to(np.array([409.987, 274.728, 0.0])*scale).shift(pos + 0.15*UP)
    ret_objects += [c1, c2]

    pnts = [
        (373.367*RIGHT +  366.776 * UP) * scale + pos,
        (503.717*RIGHT +  453.873 * UP) * scale + pos,
        (464.612*RIGHT +  613.847 * UP) * scale + pos,
        (340.78*RIGHT +  643.472 * UP) * scale + pos,
        (131.628*RIGHT +  596.072 * UP) * scale + pos,
        (174.288*RIGHT +  388.106 * UP) * scale + pos,
    ]

    center = 0*LEFT
    for i in range(len(pnts)):
        pnts[i] += (length_scale - 1)*(pnts[i] - pnts[0])[0]*RIGHT
        center += pnts[i]
    center /= len(pnts)

    angles = np.array([120, 170, 120, 120, 180, 120])*1.5707963267/90.0


    for i in range(len(pnts)):
        ret_objects.append(
            ArcBetweenPoints(pnts[i], pnts[(i+1)%len(pnts)], angle = angles[i], color = color)
        )

    return Group(*ret_objects)#, center


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
    + r"{{1) The system is not a dictatorship of one voter. \\}}"
    + r"{{2) At least three candidates are elected by the system in at least one scenario. \\}}"
    + r"There exists at least one scenario where the system incentivizes strategic voting. ",
    color=text_color,
).scale(thm_scale)


example_table_str = ["ABC", "ABC","ABC","ABC", "BCA", "BCA", "CAB", "CAB", "CAB"]
majority_table_str = [ "BCA", "BAC", "BCA", "BAC", "BCA", "CAB", "CAB", "CAB", "CAB"]

def img_monkey(str, voting = False, width = 2):

    sc = 2
    if voting == "A":
        votes_for_img = SVGMobject("img/fruit/avocado.svg").scale_to_fit_width(width / sc)
    elif voting == "B":
        votes_for_img = SVGMobject("img/fruit/banana.svg").scale_to_fit_width(width / sc)
    elif voting == "C":
        votes_for_img = SVGMobject("img/fruit/coconut.svg").scale_to_fit_width(width / sc)
    else:
        votes_for_img = Dot().scale(0.0000001)

    if str == "A":
        if voting:
            monkey_img = ImageMobject("img/monkeys/avocado2.png").scale_to_fit_width(width)
            votes_for_img.shift(1*LEFT + 1*UP)
        else:
            monkey_img = ImageMobject("img/monkeys/avocado1.png" ).scale_to_fit_width(width)
    elif str == "B":
        if voting:
            monkey_img = ImageMobject("img/monkeys/banana2.png").scale_to_fit_width(width)
            votes_for_img.shift(1*LEFT + 1*UP)
        else:
            monkey_img = ImageMobject("img/monkeys/banana1.png" ).scale_to_fit_width(width)
    else:
        if voting:
            monkey_img = ImageMobject("img/monkeys/coconut2.png").scale_to_fit_width(width)
            votes_for_img.shift(1*LEFT + 1*UP)
        else:
            monkey_img = ImageMobject("img/monkeys/coconut1.png" ).scale_to_fit_width(width)
        
    return Group(monkey_img, votes_for_img)

def ordering(str, background = None):
    w = 0.3
    f1 = FRUITS[str[0]].copy().scale_to_fit_width(w)
    f2 = FRUITS[str[1]].copy().scale_to_fit_width(w)
    f3 = FRUITS[str[2]].copy().scale_to_fit_width(w)
    fruits = Group(f1, f2, f3).arrange(DOWN)

    border = SurroundingRectangle(fruits, corner_radius = 0.3, color = text_color)
    if background!=None:
        border.set_opacity(1.0)
        border.set_color(background)

    return Group(border, fruits)

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

    def highlight(self):
        return self.indicate()


FRUITS = {
    f.label: f
    for f in (
        Fruit("A", SVGMobject("img/fruit/avocado.svg").scale(0.4)),
        Fruit("B", SVGMobject("img/fruit/banana.svg").scale(0.4)),
        Fruit("C", SVGMobject("img/fruit/coconut.svg").scale(0.4)),
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
        self.winner = get_fruit(winner).scale(self.scale_factor)
        # self.add(self.winner)
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


class Intro(Scene):
    def construct(self):
        default()
        self.next_section(skip_animations = False)

        background = ImageMobject("img/background-upscaled.png").scale_to_fit_width(config.frame_width)
        explorer = ImageMobject("img/explorer.png").scale_to_fit_height(5).to_corner(DR).shift(2*RIGHT) # TODO pridat polylogo na laptop
        self.add(background, explorer)

        # Throughout my expeditions, I've visited many beautiful places, but none struck me as much as this faraway tropical island. 

        
        self.play(
            Group(background, explorer).animate.scale(1.05),
            run_time = 5
        )
        self.wait()

        w = 1
        monkeys_img = [
         img_monkey(example_table_str[i][0], False, w) for i in range(len(example_table_str))
        ]
        
        monkeys_img[0].to_corner(DL)
        monkeys_img[1].next_to(monkeys_img[0], RIGHT)
        monkeys_img[2].next_to(monkeys_img[0], UP)
        monkeys_img[3].next_to(monkeys_img[0], UR)

        monkeys_img[4].to_edge(DOWN).shift(2*LEFT)
        monkeys_img[5].next_to(monkeys_img[4], RIGHT)

        monkeys_img[6].shift(4*LEFT + 2*UP)
        monkeys_img[7].next_to(monkeys_img[6], RIGHT)
        monkeys_img[8].next_to(monkeys_img[7], RIGHT)

        monkeys_voting_img = [
            [
                img_monkey(example_table_str[i][0], example_table_str[i][j], w).align_to(monkeys_img[i], DR)
                for j in range(3)
            ] for i in range(len(example_table_str))
        ]
        
        orderings = [
            ordering("ABC", background = BACKGROUND_COLOR).next_to(monkeys_img[3], RIGHT),
            ordering("BCA", background = BACKGROUND_COLOR).next_to(monkeys_img[5], RIGHT),
            ordering("CAB", background = BACKGROUND_COLOR).next_to(monkeys_img[8], RIGHT),
        ]

        # It was full of monkeys that were constantly arguing about which fruit is the best. I noticed three distinct groups among them, each one with a different opinion on the matter.
        
        # There was a group that really liked avocado, banana was their second choice, and they disliked coconuts. 

        # “Avocado is the best!”

        ranges = [range(4), range(4, 6), range(6, 9)]

        for j in range(3):
            for i in ranges[j]:
                self.play(
                    FadeIn(monkeys_img[i]),
                )
                #self.wait()

            self.wait()

            self.play(
                FadeIn(orderings[j]),
            )
            self.wait()

            self.play(
                *[Wiggle(monkeys_img[i]) for i in ranges[j]]
            )
            self.wait()

        # Second group were fond of banana, coconut was their second choice, and avocado was the third. 

        # “No, banana is better!”
        # Finally, there were two monkeys that loved coconuts, avocado was their second choice and banana the last one. 

        # “Team coconut!”

        # Silence! If there's disagreement, why not resolve it through a vote?
        # “Yes, why don’t we vote? ”
        # “But how do we do it?”
        # “Help us, big monkey.”

        # Charmed by their antics, I decided to help organize a vote. After all, there are just a few of them, so it can’t be that hard, right? 

        # Ok, let’s try something simple: everybody will vote for exactly one fruit. Who votes for avocado? 
        # 4 votes
        # Banana? 
        # 3 votes
        # coconut? 
        # 2 votes

        self.next_section(skip_animations = False)

        monkeys_votes_img = [monkeys_voting_img[i][0] for i in range(9)]

        for j in range(3):
            anims = []
            for i in ranges[j]:
                anims.append(Interpol(monkeys_img[i], monkeys_votes_img[i]))
            self.play(*anims)
            self.wait()

        # [(bude potřeba upravit předchozí text) ukážou se obrázky všech tří ovocí, opice se rozdělí do tří skupin podle toho, pro které ovoce hlasují.]

                
        winner_img = [
            Group(
                SVGMobject("img/crown.svg").scale_to_fit_width(2.0),
                SVGMobject("img/fruit/" + name).scale_to_fit_width(2.5),
            ).arrange(DOWN).move_to(2*RIGHT)
            for name in ["avocado.svg", "banana.svg", "coconut.svg"]
        ]

        self.play(
            FadeIn(winner_img[0])
        )
        self.wait()
        self.play(
            *[Interpol(i1, i2) for i1, i2 in zip(monkeys_votes_img, monkeys_img)],
            FadeOut(winner_img[0])
        )
        self.wait()


        # Ok, avocado won. You are welcome. 
        # monkeys who voted coconut: “But what about the second round? “ 

        # Ok, I guess a two-round election is fairer because now the coconut fans can also express their opinion on the remaining two fruits. So let’s do a second round: avocado? 4 votes. Banana? 5 votes

        monkeys_votes_img = [monkeys_voting_img[i][0] for i in ranges[0]] + [monkeys_voting_img[i][1] for i in ranges[1]] + [monkeys_voting_img[i][0] for i in ranges[2]]

        self.play(
            *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[0]],
        )
        self.wait()
        self.play(
            *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[1]],
            *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[2]],
        )
        self.wait()

        # [(upravit předchozí text) opice co by	ly pod banánem se přesunou pod citrón]

        # Hm, so now it looks like that banana, and not avocado should be the winner! 
        self.play(
            FadeIn(winner_img[2])
        )
        self.wait()
        self.play(
            *[Interpol(monkeys_votes_img[i], monkeys_img[i]) for i in range(9)],
            FadeOut(winner_img[2])
        )
        self.wait()


        # But then it got worse. 
        # [opice dělají šepty-šepty]

        # The monkeys who voted for avocado: “We protest!”
        # [možná drží banner na kterém je napsáno protest]

        monkeys_votes_img = [monkeys_voting_img[i][1] for i in ranges[0]] + [monkeys_voting_img[i][0] for i in ranges[1]] + [monkeys_voting_img[i][0] for i in ranges[2]]

        self.play(
            *[Wiggle(monkeys_img[i]) for i in ranges[0]]
        )
        self.wait()

        # Why? 
        # We made a mistake in the first round, can we run the election one more time? Please! 
        # [sigh] let’s do it one more time. First round. Who is for avocado?

        for it in range(2):
            self.play(
                *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[0]],
                *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[1]],
            )
            self.wait()
            self.play(
                *[Interpol(monkeys_img[i], monkeys_votes_img[i]) for i in ranges[2]],
            )
            self.wait()

            if it == 0:
                self.play(
                    *[Interpol(monkeys_votes_img[i], monkeys_img[i]) for i in range(9)],
                )
                self.wait()

        # [(upravit předchozí text) opice co by	ly pod banánem se přesunou pod citrón]

        # Hm, so now it looks like that banana, and not avocado should be the winner! 
        self.play(
            FadeIn(winner_img[1])
        )
        self.wait()
        self.play(
            *[Interpol(monkeys_votes_img[i], monkeys_img[i]) for i in range(9)],
            FadeOut(winner_img[1])
        )
        self.wait()




        # 2 votes
        # banana? 
        # 3 votes
        # coconut? 
        # 4 votes [hehe]

        # Interesting, now banana and coconut go to the second round. Who votes for banana?  
        # 3 votes coconut? 6 votes

        # [(upravit předchozí text) podobná animace s přesouváním opic. možná nakonci ty dvě opice udělají hahaha]

        # So now it’s even coconut that won. These two monkeys are pretty sly. They really don’t like banana. They also realized that their favorite, avocado, cannot win against banana in the second round. So, they rather voted for coconut because that’s their second choice. 

        rec_four = SurroundingRectangle(Group(*monkeys_img[:4]), color = RED)
        rec = rec_four.copy()
        self.play(FadeIn(rec))
        self.wait()

        rec_other = [SurroundingRectangle(orderings[0][1][i], color = RED) for i in range(3)]
        self.play(Transform(rec, rec_other[2]))
        self.wait()
        self.play(Transform(rec, rec_other[0]))
        self.wait()
        self.play(Transform(rec, rec_other[1]))
        self.wait()
        self.play(Transform(rec, rec_four))
        self.wait()
        self.play(FadeOut(rec))
        self.wait()

        # Picking the best fruit doesn’t sound so easy anymore! Especially the fact that monkeys can vote strategically and, with that, change the outcome of the election, is really annoying. An election should ideally be a competition of ideas, not a strategic game among voters. Wouldn't it be great to have a voting system that incentivizes all the monkeys to be truthful? But does such a system exist?



class Polylogo(Scene):
    def construct(self):
        default()
        authors = Tex(# napsat autory nakonec jestli nebudou tady
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
            #Write(authors),
            Write(channel_name),
        )
        self.play(FadeIn(logo_solarized))
        self.add(channel_name_without_o)
        self.remove(channel_name)

        mirek_logo = ImageMobject("img/olsak.jpg").scale(1.5).shift(2*DOWN + 2*RIGHT)
        mirek_tex = Tex(r"\raggedleft Based on a short story \\ by Mirek Olšák").next_to(mirek_logo, LEFT)

        self.play(
            FadeIn(mirek_logo),
            Write(mirek_tex),
        )
        self.wait()


        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()

class Statement1(Scene):
    def construct(self):
        default()
        # Unfortunately, the answer is no and because I took my whiteboard with me, I will explain why. I will prove to you the Gibbard-Satterthwaite theorem which says that any reasonable voting system sometimes incentivizes strategic voting. 
        gs_group.move_to(ORIGIN)
        self.play(
            FadeIn(gs_title),
            )
        self.wait()
        self.play(
            FadeIn(gs_tex),
            )
        self.wait()
        self.play(
            FadeOut(gs_title),
            )
        self.wait()
        self.play(
            gs_tex.animate.to_edge(UP, buff = 0.5),
            )
        self.wait()


        # I think that the most challenging aspect of the theorem is to understand what it is actually saying, so let’s try to slowly unpack this sentence. 

        # First, we need to define what a voting system is. 

        border = SurroundingRectangle(gs_tex[2], color  = RED)
        self.play(FadeIn(border))
        self.wait() 
        
        # We have already seen two systems: The first one, where everybody votes for their favorite candidate and we pick the one with the most votes, is called the plurality voting. 

        monkeys_img = Group(*[img_monkey(example_table_str[i][0], voting = False, width = 2) for i in range(len(example_table_str))]).arrange_in_grid(rows = 3).to_edge(LEFT, buff = 1)
        monkeys_voting_img = Group(*[img_monkey(example_table_str[i][0], voting = True, width = 2) for i in range(len(example_table_str))]).arrange_in_grid(rows = 3).move_to(monkeys_img.get_center())
        monkeys_votingA_img = Group(*[img_monkey("A", voting = True, width = 2) for i in range(len(example_table_str))]).arrange_in_grid(rows = 3).move_to(monkeys_img.get_center())

        plurality_tex = Tex("Plurality voting:").next_to(gs_title, DOWN, buff = 1)
        arrow = Tex(r"$\rightarrow$").scale(3).next_to(monkeys_img, RIGHT)
        result = FRUITS["C"].next_to(arrow, RIGHT)

        self.play(
            FadeIn(monkeys_img)
        )
        self.wait()
        self.play(
            *[ReplacementTransform(img1, img2) for img1, img2 in zip(monkeys_img, monkeys_voting_img)]
        )
        self.wait()
        
        self.play(
            FadeIn(arrow)
        )
        self.wait()

        self.play(
            FadeIn(result)
        )
        self.wait()

        self.play(
            *[ReplacementTransform(img2, img1) for img1, img2 in zip(monkeys_img, monkeys_voting_img)],
            FadeOut(arrow),
            FadeOut(result),
        )
        self.wait()

        # The other one where the two most popular candidates from the first round compete in the second round run-off is called the two round system. 

        result = FRUITS["B"].next_to(arrow, RIGHT)
        self.play(
            *[ReplacementTransform(img1, img2) for img1, img2 in zip(monkeys_img, monkeys_voting_img)]
        )
        self.wait()
        
        self.play(
            *[ReplacementTransform(img2, img1) for img1, img2 in list(zip(monkeys_img, monkeys_voting_img))[:2]]
        )
        self.wait()
        
        self.play(
            *[ReplacementTransform(img1, img2) for img1, img2 in list(zip(monkeys_img, monkeys_votingA_img))[:2]]
        )
        self.wait()
        
        self.play(
            FadeIn(arrow)
        )
        self.wait()

        self.play(
            FadeIn(result)
        )
        self.wait()

        self.play(
            *[ReplacementTransform(img2, img1) for img1, img2 in list(zip(monkeys_img, monkeys_voting_img))[2:]],
            *[ReplacementTransform(img2, img1) for img1, img2 in list(zip(monkeys_img, monkeys_votingA_img))[:2]],
            FadeOut(arrow),
            FadeOut(result),
        )
        self.wait()

        # Both of these systems have in common that you can think of each voter as having some ranking of the candidates. We can then imagine that the voter writes this ranking on their ballot, the voting system is simply a function that gets all the ballots as input, and its output is the elected winner. 

        orderings = Group(*[ordering(example_table_str[i]).move_to(monkeys_img[i].get_center()).shift(1*RIGHT + 1*UP) for i in range(len(example_table_str))])
        self.play(
            FadeIn(orderings)
        )
        self.wait()

        table = VotingTable(example_table_str).next_to(monkeys_img, RIGHT)
        self.play(
            FadeIn(table)
        )
        self.wait()

        self.play(
            table.results_show("A")
        )
        self.wait()

        self.play(
            FadeOut(monkeys_img),
            FadeOut(orderings),
            table.animate.move_to(ORIGIN)
        )
        self.wait()

        # Example: We think of the two-round system as a system where the voters need to vote twice. But if every voter writes down their complete ranking of candidates on the ballot, we don’t need the second round at all. We can simulate the two round process just from the information on the ballots. 

        self.play(
            *table.two_round_system()
        )
        self.wait()

        # [suggestivní animace kde máme tabulku s preferencemi voterů a animace pro oba volební systémy, 
        # -> obrázek vítěze, možná s korunkou nebo tak něco
        # ]

        # As a quick aside, how should we deal with ties? Well, we could adjust our definition of a voting system to allow them, but then everything becomes a bit clumsy, so instead let’s say that in our example voting systems we always break ties alphabetically, so avocado over banana over coconut. 

        table2 = VotingTable(["AB", "AB", "AB", "AB", "BA", "BA", "BA", "BA"])
        self.play(
            FadeOut(table),
            FadeIn(table2),
            FadeOut(border),
            gs_tex[2].animate.set_color(GREEN),
        )
        self.wait()

class Statement2(Scene):
    def construct(self):
        default()
        
        gs_tex[2].set_color(GREEN),
        self.add(
            gs_tex.to_edge(UP, buff = 0.5),
            )
        border = SurroundingRectangle(gs_tex[4], color  = RED)
        self.play(FadeIn(border))
        self.wait() 

        # Let’s go on, what do we mean by “sometimes incentivizes strategic voting”? Here is an example. Let’s look at this scenario with the plurality voting system and this voter in particular. So far, we did not distinguish between the true preference of the voter and the ranking that the voter actually writes on the ballot, we assumed this is always the same thing. But now let’s imagine that all other voters already cast their ballots and our voter actually sees what is written on them. 

        i_voter = 3
        table = VotingTable(example_table_str).next_to(gs_tex, DOWN)
        voter = img_monkey("A").scale(2).next_to(table[i_voter], DOWN, buff = 1)

        self.play(
            *[FadeIn(table[i]) for i in range(table.num_of_voters) if i != i_voter]
        )
        self.wait()
        self.play(
            FadeIn(voter)
        )
        self.wait()


        bubble = create_bubble().next_to(voter, LEFT).shift(1*UP)
        order = ordering("ABC").move_to(bubble.get_center())
        self.play(
            FadeIn(bubble),
            FadeIn(order)
        )
        self.wait()

        sc = 2
        self.play(
            order.animate.scale(sc).move_to(table[i_voter].get_center())
        )
        self.wait()
        self.play(
            order.animate.scale(1.0/sc).move_to(bubble.get_center())
        )
        self.wait()

        self.play(
            table.results_show("A")
        )
        self.wait()
        self.play(
            table.results_hide()
        )
        self.wait()
        
        # Now it is time for our voter to decide what ranking to put on the ballot. The voter can of course use their true preference - in this case, the voting system elects Y as the winner. But the voter can also vote strategically and write a different ranking on the ballot. For example, if the voter casts this ballot, the voting system now elects Z as the winner. 

        bubble2 = create_bubble(speaking = True).next_to(voter, RIGHT).shift(1*UP)
        order2 = ordering("CAB").move_to(bubble2.get_center())
        self.play(
            FadeIn(bubble2),
            FadeIn(order2)
        )
        self.wait()
        self.play(
            order2.animate.scale(sc).move_to(table[i_voter].get_center())
        )
        self.wait()
        self.play(
            order2.animate.scale(1.0/sc).move_to(bubble2.get_center())
        )
        self.wait()

        self.play(
            table.results_show("B")
        )
        self.wait()
        self.play(
            table.results_hide()
        )
        self.wait()

        # What’s important, our voter actually prefers Z over Y, so it pays off to submit this dishonest ballot. Whenever this happens, we say that the voter is incentivized to vote strategically. 

        self.play(
            Circumscribe(order, color = RED)
        )
        self.wait()

        self.play(
            FadeOut(border),
            gs_tex[4].animate.set_color(GREEN),
        )
        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects if o != gs_tex]
        )
        self.wait()

        # So the definition is a bit different than what happened earlier because there, the whole group of monkeys coordinated. Also, the theorem is not saying that in every possible scenario, there is somebody who has this incentive. But, for any reasonable voting system we can find at least one scenario where strategic voting occurs. 

        self.play(
            Circumscribe(gs_tex, color = RED)
        )
        self.wait()
        self.play(
            gs_tex[3].animate.set_color(GREEN)
        )
        self.wait()

        # And this brings us to the word “reasonable”. The problem is: Think of the dictatorship voting system where the winner is always the top preference of voter number 3. By that I mean that system always outputs the fruit in the highlighted square. This voting system actually satisfies our definition of a voting system. Also, you can check that there is no scenario in which strategic voting helps anybody. 
        
    
        border = SurroundingRectangle(gs_tex[1], color = RED)
        self.play(
            FadeIn(border)
        )
        self.wait()

        table.move_to(ORIGIN)
        self.play(
            FadeIn(table)
        )
        self.wait()

        border_fruit = SurroundingRectangle(table[3][0], color = RED)
        self.play(
            FadeIn(border_fruit),
            table.results_show("B")
        )
        self.wait()
        self.play(
            FadeOut(table),
            FadeOut(border_fruit)
        )
        self.wait()

        # This is why we can prove the theorem only for voting systems that are in some sense reasonable. But how should we define it precisely? For now, let’s choose the following definition: I will say that a voting system is reasonable if, whenever there is a candidate that is the top preference for more than half of the voters, then this candidate should be elected by the voting system. 

        reasonable1_tex = Tex("{{Reasonable system: }}").next_to(gs_tex, DOWN, buff = 1).align_to(gs_tex, LEFT)
        reasonable_tex = Tex(r"{{\raggedright The candidate which is the first choice for majority\\ is always the winner. }}").scale(0.8).next_to(reasonable1_tex, RIGHT)
        majority_table = VotingTable(majority_table_str).align_to(reasonable_tex, UP).shift(1*DOWN)

        self.play(FadeIn(reasonable_tex), FadeIn(reasonable1_tex))
        self.wait()
        self.play(FadeIn(majority_table))
        self.wait()

        self.play(
            *[Indicate(majority_table[i][0]) for i in range(5)]
        )
        self.wait()
        self.play(
            table.winner_show("A")
        )
        self.wait()
        # Both the plurality voting system and the two-round system satisfy this definition of being reasonable, so the definition makes some sense. We will now prove the theorem and then we will discuss this definition a bit more. 

        self.wait(10)


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
            ["ABC", "ABC", "ABC", "ABC", "ABC", "BCA", "BCA", "BCA", "BCA"]
        ).shift(2 * LEFT)

        self.play(FadeIn(table))
        self.wait()

        self.play(table.winner_show("A"))
        self.wait()

        self.play(*table.highlight("A", indexes=range(5)))
        self.wait()

        # But X is also the bottom choice for almost half of the voters so isn’t Y also a good candidate for the winner? There are in fact some popular voting systems [ See Borda count] that would elect Y in this scenario.

        self.play(*table.highlight("A", indexes=range(5, table.num_of_voters)))
        self.wait()

        self.play(*table.highlight("B", indexes=range(5, table.num_of_voters)))
        self.wait()
        self.play(*table.highlight("B", indexes=range(5)))
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

        table = VotingTable(example_table_str).shift(2 * LEFT)

        self.play(FadeIn(table))
        self.wait()

        self.play(table.results_show("CBA"))
        self.wait()

        # (animace s tabulkou, outcome se změní z vítěze na order)

        # Arrow’s theorem says that if there are at least three candidates, any reasonable voting system for ordering them will not satisfy the so-called independence of irrelevant alternatives.

        self.play(FadeIn(arrow_tex))
        self.wait()

        # This is a condition that says that if you look at how the voting system orders any two candidates, for example here it decides that banana is above coconut

        self.play(*table.results.highlight("B"))
        self.wait()
        self.play(*table.results.highlight("C"))
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
                AnimationGroup(table[1].rearrange("ABC"), table.results_show("BAC")),
                AnimationGroup(table[2].rearrange("ABC")),
            )
        )

        # The first part of our proof can actually be used to prove a version of Arrow’s theorem, but if you use the textbook definition of a reasonable voting system, the proof again becomes a bit tedious.

        self.play(
            *(
                AnimationGroup(table[i].rearrange(example_table_str[i]))
                for i in range(len(example_table_str))
            )
        )

        for _ in range(2):
            self.play(
                *table.rearrange("ABC", indexes=range(5, 9)),
                table.results_show("ABC"),
            )
            self.wait()
            self.play(
                *table.rearrange("CBA", indexes=range(5, 9)),
                table.results_show("CBA"),
            )
            self.wait()

        # Both Arrow and Gibbard-Satterthwaite theorems are good examples showing that while we often like to think that important mathematical theorems are simply-looking statements that turn out to be insanely complicated to prove, it is not always like that.
        # (možná někde problikne statement Fermata nebo P vs NP?)

        self.play(table.results_hide(), FadeOut(table))
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

        self.play(AnimationGroup(*table.indicate(), lag_ratio=0.51))
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
            *[FadeOut(o) for o in (set(likes + dislikes) & set(self.mobjects))],
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
        self.play(table[0].rearrange("CAB"), table[1].rearrange("CAB"))
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
        self.play(table2[0].rearrange("BCA"))
        self.wait(10)
