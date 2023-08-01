from utils.util import *


# TODO jiny pozadi

HIGHLIGHT = ORANGE2


class Intro(MovingCameraScene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)
        (
            monkeys_img,
            monkeys_voting_img,
            orderings,
            explorer,
            background,
            whiteboard,
        ) = intro_images()

        self.add(background)

        self.play(arrive_from(explorer, RIGHT))
        self.wait()

        # Throughout my expeditions, I've visited many beautiful places, but none struck me as much as this faraway tropical island.

        # self.play(
        #     Group(background, explorer).animate.scale(1.05),
        #     run_time = 5
        # )
        # self.wait()

        # It was full of monkeys that were constantly arguing about which fruit is the best. I noticed three distinct groups among them, each one with a different opinion on the matter.

        # There was a group that really liked avocado, banana was their second choice, and they disliked coconuts.

        # “Avocado is the best!”

        ranges = [range(4), range(4, 6), range(6, 9)]

        for j in range(3):
            for i in ranges[j]:
                self.play(
                    FadeIn(monkeys_img[i]),
                )
                # self.wait()

            self.wait()

            self.play(
                FadeIn(orderings[j]),
            )
            self.wait()

            self.play(*[Wiggle(monkeys_img[i]) for i in ranges[j]])
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

        self.play(Wiggle(monkeys_img[2]))
        self.wait()
        self.play(Wiggle(monkeys_img[5]))
        self.wait()
        self.play(Wiggle(monkeys_img[8]))
        self.wait()

        # Ok, let’s try something simple: everybody will vote for exactly one fruit. Who votes for avocado?
        # 4 votes
        # Banana?
        # 3 votes
        # coconut?
        # 2 votes

        monkeys_votes_img = [monkeys_voting_img[i][0] for i in range(9)]

        for j in range(3):
            anims = []
            for i in ranges[j]:
                anims.append(Interpol(monkeys_img[i], monkeys_votes_img[i]))
            self.play(*anims)
            self.wait()

        # [(bude potřeba upravit předchozí text) ukážou se obrázky všech tří ovocí, opice se rozdělí do tří skupin podle toho, pro které ovoce hlasují.]

        winner_img = [
            get_crowned_fruit(label, True).move_to(5 * RIGHT).scale(3)
            for label in "ABC"
        ]

        self.play(FadeIn(winner_img[0]))
        self.wait()
        self.play(
            *[Interpol(i1, i2) for i1, i2 in zip(monkeys_votes_img, monkeys_img)],
            FadeOut(winner_img[0]),
        )
        self.wait()

        # Ok, avocado won. You are welcome.
        # monkeys who voted coconut: “But what about the second round? “

        self.play(*[Wiggle(monkeys_img[i]) for i in range(4, 6)])
        self.wait()

        # Ok, I guess a two-round election is fairer because now the coconut fans can also express their opinion on the remaining two fruits. So let’s do a second round: avocado? 4 votes. Banana? 5 votes

        monkeys_votes_img = (
            [monkeys_voting_img[i][0] for i in ranges[0]]
            + [monkeys_voting_img[i][1] for i in ranges[1]]
            + [monkeys_voting_img[i][0] for i in ranges[2]]
        )

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
        self.play(FadeIn(winner_img[2]))
        self.wait()
        self.play(
            *[Interpol(monkeys_votes_img[i], monkeys_img[i]) for i in range(9)],
            FadeOut(winner_img[2]),
        )
        self.wait()

        # But then it got worse.
        # [opice dělají šepty-šepty]

        # The monkeys who voted for avocado: “We protest!”
        # [možná drží banner na kterém je napsáno protest]

        self.next_section(skip_animations=False)
        monkeys_votes_img = (
            [monkeys_voting_img[i][1] for i in ranges[0]]
            + [monkeys_voting_img[i][0] for i in ranges[1]]
            + [monkeys_voting_img[i][0] for i in ranges[2]]
        )

        protest_tex = [
            Tex(str, color=BASE02)
            .scale(0.55)
            .move_to(monkeys_voting_img[i][0][0])
            .shift(0.5 * LEFT + 0.38 * UP)
            for i, str in enumerate(["PRO", "TE", "ST", "WE"])
        ]
        monkeys_protest = [
            VGroup(monkeys_voting_img[i][0][0], protest_tex[i]) for i in range(4)
        ]

        self.play(
            *[Interpol(monkeys_img[i], monkeys_protest[i][0]) for i in range(4)],
            *[FadeIn(monkeys_protest[i][1]) for i in range(4)],
        )
        self.wait()
        self.play(*[Wiggle(monkeys_protest[i]) for i in range(4)])
        self.wait()

        self.play(
            *[Interpol(monkeys_protest[i][0], monkeys_img[i]) for i in range(4)],
            *[FadeOut(monkeys_protest[i][1].set_z_index(9999)) for i in range(4)],
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

            if it == 0:
                self.play(*[Wiggle(monkeys_votes_img[i]) for i in ranges[0]])
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
        self.play(FadeIn(winner_img[1]))
        self.wait()
        self.play(
            *[Interpol(monkeys_votes_img[i], monkeys_img[i]) for i in range(9)],
            FadeOut(winner_img[1]),
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

        rec_four = SurroundingRectangle(Group(*monkeys_img[:4]), color=HIGHLIGHT)
        rec = rec_four.copy()
        self.play(FadeIn(rec))
        self.wait()

        rec_other = [
            SurroundingRectangle(orderings[0][1][i], color=HIGHLIGHT) for i in range(3)
        ]
        self.play(Transform(rec, rec_other[2]))
        self.wait()
        self.play(Transform(rec, rec_other[0]))
        self.wait()
        self.play(Transform(rec, rec_other[1]))
        self.wait()
        # self.play(Transform(rec, rec_four))
        # self.wait()
        self.play(FadeOut(rec))
        self.wait()

        # Picking the best fruit doesn’t sound so easy anymore! Especially the fact that monkeys can vote strategically and, with that, change the outcome of the election, is really annoying. An election should ideally be a competition of ideas, not a strategic game among voters. Wouldn't it be great to have a voting system that incentivizes all the monkeys to be truthful? But does such a system exist?

        self.next_section(skip_animations=False)

        i = 3
        sc = 1.2
        bubbles = [
            SVGMobject("img/bubble_think_full.svg")
            .scale_to_fit_height(sc * monkeys_img[i].height)
            .next_to(monkeys_img[i], LEFT, buff=SMALL_BUFF)
            .shift(1 * UP),
            SVGMobject("img/bubble_say_full.svg")
            .scale_to_fit_height(sc * monkeys_img[i].height)
            .next_to(monkeys_img[i], RIGHT, buff=SMALL_BUFF)
            .shift(1 * UP),
        ]
        bubbles[0] = Group(
            bubbles[0], FRUITS["A"].move_to(bubbles[0].get_center() + 0.07 * LEFT)
        )
        bubbles[1] = Group(bubbles[1], FRUITS["B"].move_to(bubbles[1].get_center()))

        self.play(FadeIn(bubbles[0]))
        self.wait()

        self.play(FadeIn(bubbles[1]))
        self.wait()

        self.play(FadeOut(Group(bubbles[0], bubbles[1])))
        self.wait()

        self.play(arrive_from(whiteboard, RIGHT), run_time=5)
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.17).move_to(
                whiteboard.get_center() + 0.5 * UP
            )
        )
        self.wait()


class Polylogo(Scene):
    def construct(self):
        default()
        authors = Tex(  # napsat autory nakonec jestli nebudou tady
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)
        channel_name_without_o = Tex(r"p\hskip 5.28pt lylog", color=text_color)
        channel_name_without_o.scale(4).shift(1 * UP)

        logo_solarized = (
            load_svg("img/logo-solarized.svg")
            .scale(0.55)
            .move_to(2 * LEFT + 0.95 * UP + 0.49 * RIGHT)
        )
        self.play(
            # Write(authors),
            Write(channel_name),
        )
        self.play(FadeIn(logo_solarized))
        self.add(channel_name_without_o)
        self.remove(channel_name)

        mirek_logo = (
            ImageMobject("img/olsak.jpg").scale(1.5).shift(2 * DOWN + 2 * RIGHT)
        )
        mirek_tex = Tex(
            r"\raggedleft Based on a short story \\ by Mirek Olšák"
        ).next_to(mirek_logo, LEFT)

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
        # gs_group.move_to(ORIGIN)
        gs_down = gs_group.copy().shift(0.7 * DOWN)
        self.play(
            FadeIn(gs_down[0]),
        )
        self.wait()
        self.play(
            FadeIn(gs_down[1]),
        )
        gs_group[0].fade(1)
        self.wait()
        self.play(gs_down.animate.become(gs_group))
        self.wait()

        # I think that the most challenging aspect of the theorem is to understand what it is actually saying, so let’s try to slowly unpack this sentence.

        # First, we need to define what a voting system is.

        border = SurroundingRectangle(gs_tex[2], color=HIGHLIGHT)
        self.play(FadeIn(border))
        self.wait()

        # We have already seen two systems: The first one, where everybody votes for their favorite candidate and we pick the one with the most votes, is called the plurality voting.

        monkeys_img = (
            Group(*[img_monkey(pref[0], width=1.1) for pref in example_table_str])
            .arrange()
            .to_edge(LEFT, buff=1)
            .to_edge(DOWN)
            .shift(0.5 * UP)
        )

        # special_monkey = monkeys_img[0]
        # special_monkey.save_state()
        # special_monkey.move_to(ORIGIN).scale(2)

        # self.play(FadeIn(special_monkey))
        # self.wait()
        # ord = Preference(example_table_str[0]).next_to(special_monkey, RIGHT, buff=0.5)
        # self.play(FadeIn(ord))
        # self.wait()

        table = VotingTable(example_table_str).scale(1.5).shift(2 * LEFT + 0.5 * DOWN)
        monkey_scale = 0.4
        for col, monkey in zip(table.group, monkeys_img):
            col.save_state()
            col.scale(monkey_scale).next_to(monkey, UP)

        self.play(
            AnimationGroup(
                # FadeOut(ord),
                # special_monkey.animate.scale(0.5).move_to(
                #     special_monkey.saved_state.get_center()
                # ),
                *[
                    FadeIn(Group(table[i], monkeys_img[i]), run_time=0.5)
                    for i in range(9)
                ],
                lag_ratio=0.6,
            )
        )
        self.wait()

        # self.play(FadeIn(table))
        # self.wait()
        self.play(
            *(
                col.animate.scale(1 / monkey_scale).move_to(col.saved_state)
                for col in table.group
            ),
            FadeOut(monkeys_img),
        )
        self.wait()
        input_brace = BraceLabel(table, "input", UP)
        self.play(FadeIn(input_brace))
        self.play(table.winner_show("A"))
        output_brace = BraceLabel(table.results.winner, "output", UP)
        self.play(FadeIn(output_brace))
        self.wait()
        self.play(FadeOut(input_brace), FadeOut(output_brace))
        self.play(table.results_hide())
        self.wait(3)

        two_tex = (
            Tex("Two-round system:").next_to(table, UP, buff=0.5).align_to(table, LEFT)
        )
        self.play(FadeIn(two_tex))
        self.wait()

        table.two_round_system(self)
        self.wait()

        self.play(FadeOut(two_tex), FadeOut(table), table.results_hide())

        lines = (
            VGroup(
                *(
                    VGroup(get_fruit(char), MathTex(r": 50\,\%")).arrange(
                        RIGHT, buff=0.1
                    )
                    for char in "AB"
                )
            )
            .arrange(DOWN)
            .scale(2)
        ).shift(2.5 * LEFT + 0.5 * UP)

        quest_tex = Tex("?").scale(2.5).next_to(lines, RIGHT, buff=1)

        self.play(FadeIn(Group(lines, quest_tex)))
        self.wait()

        table = VotingTable(["AB"]).scale(1.5).move_to(lines).align_to(lines, RIGHT)

        comparison = (
            VGroup(
                get_fruit("A"),
                MathTex(">"),
                get_fruit("B"),
                MathTex(">"),
                get_fruit("C"),
            )
            .arrange()
            .to_edge(DOWN, buff=1.5)
        ).scale(1.5)

        self.play(FadeIn(comparison))
        self.wait()

        table.group.fade(1)
        self.play(table.winner_show("A"), FadeOut(quest_tex))
        self.wait()


class Statement2(Scene):
    def construct(self):
        default()

        # gs_tex[2].set_color(GREEN),
        self.add(gs_tex)
        border = SurroundingRectangle(gs_tex[4], color=HIGHLIGHT)
        self.play(FadeIn(border))
        self.wait()

        # Let’s go on, what do we mean by “sometimes incentivizes strategic voting”? Here is an example. Let’s look at this scenario with the plurality voting system and this voter in particular. So far, we did not distinguish between the true preference of the voter and the ranking that the voter actually writes on the ballot, we assumed this is always the same thing. But now let’s imagine that all other voters already cast their ballots and our voter actually sees what is written on them.

        i_voter = 3
        table = VotingTable(example_table_str).next_to(gs_tex, DOWN).shift(0.7 * DOWN)

        monkeys_img = (
            Group(*[img_monkey(pref[0], width=1) for pref in example_table_str])
            .arrange()
            .to_edge(LEFT, buff=1)
            .to_edge(DOWN)
            .shift(0.5 * UP)
        )
        self.play(FadeIn(monkeys_img))

        monkey_scale = 0.7
        for col, monkey in zip(table.group, monkeys_img):
            col.save_state()
            col.scale(monkey_scale).next_to(monkey, UP)

        self.play(FadeIn(table))
        self.wait()

        voter_border = SurroundingRectangle(monkeys_img[i_voter], color=HIGHLIGHT)
        self.play(FadeIn(voter_border))
        self.wait()

        self.play(
            *(
                col.animate.scale(1 / monkey_scale).move_to(col.saved_state)
                for i, col in enumerate(table.group)
                if i != i_voter
            ),
            FadeOut(monkeys_img[:i_voter]),
            FadeOut(monkeys_img[i_voter + 1 :]),
            FadeOut(voter_border),
        )
        self.wait()

        voter = monkeys_img[i_voter]
        voter.generate_target()
        voter.target.scale(1.8).move_to(ORIGIN).to_edge(
            DOWN, buff=0.2
        )  # align_to(voter, DOWN).shift(0.5*DOWN)

        h = 3
        sht = 1.2 * UP  # + 1 * RIGHT
        bubble = (
            load_svg("img/bubble_think.svg")
            .scale_to_fit_height(h)
            .next_to(voter.target, LEFT)
            .shift(sht)
        )
        order = table[i_voter].copy()
        self.add(order)
        table[i_voter].restore()
        self.remove(table[i_voter])
        self.play(
            MoveToTarget(voter),
            order.animate.scale(1 / monkey_scale).move_to(
                bubble.get_center() + bubble.width / 10 * LEFT + bubble.height / 20 * UP
            ),
        )
        self.play(FadeIn(bubble))
        self.wait()

        order_copy = order.copy()
        sc = 1.5
        self.play(order_copy.animate.move_to(table[i_voter]))
        self.wait()
        self.play(table.results_show("C"))
        self.wait()

        self.play(
            FadeOut(order_copy),
            table.winner_hide(),
        )
        self.wait()

        # Now it is time for our voter to decide what ranking to put on the ballot. The voter can of course use their true preference - in this case, the voting system elects Y as the winner. But the voter can also vote strategically and write a different ranking on the ballot. For example, if the voter casts this ballot, the voting system now elects Z as the winner.

        bubble2 = (
            load_svg("img/bubble_say.svg")
            .scale_to_fit_height(h)
            .next_to(voter, RIGHT)
            .shift(sht)
        )
        order2 = (
            table[i_voter]
            .copy()
            .rearrange("BAC", False)
            .move_to(bubble2.get_center())
            .align_to(order, UP)
        )
        self.play(FadeIn(bubble2), FadeIn(order2))
        self.wait()
        order2_copy = order2.copy()
        self.play(
            order2_copy.animate.move_to(table[i_voter]),
        )
        self.wait()
        self.play(
            table.results_show("A"),  # TODO problikne predchozi winner
        )
        self.wait()

        ar = (
            load_svg("img/arrow.svg")
            .scale_to_fit_width(1)
            .next_to(order.group[0], LEFT)
        )
        self.play(FadeIn(ar))
        self.wait()
        self.play(ar.animate.next_to(order.group[2], LEFT))
        self.wait()
        self.play(FadeOut(ar))
        self.wait()

        # TODO other monkeys

        for _ in range(2):
            self.play(order2_copy.rearrange("ABC"), table.results_show("C"))
            self.wait()
            self.play(order2_copy.rearrange("BAC"), table.results_show("A", DOWN))
            self.wait()

        # self.play(FadeOut(order2_copy))
        # self.wait()
        # self.play(table.results_hide())
        # self.wait()

        # What’s important, our voter actually prefers Z over Y, so it pays off to submit this dishonest ballot. Whenever this happens, we say that the voter is incentivized to vote strategically.

        # self.play(Circumscribe(order, color=HIGHLIGHT))
        # self.wait()

        border2 = SurroundingRectangle(gs_tex[3], color=HIGHLIGHT)
        self.play(
            *[FadeOut(o) for o in self.mobjects if o != gs_tex and o != border],
        )
        self.wait()
        self.play(
            Transform(border, border2),
        )
        self.wait()

        # self.play(
        #     FadeOut(border),
        #     gs_tex[4].animate.set_color(GREEN),
        # )
        # self.wait()

        # self.play(*[FadeOut(o) for o in self.mobjects if o != gs_tex])
        # self.wait()

        # So the definition is a bit different than what happened earlier because there, the whole group of monkeys coordinated. Also, the theorem is not saying that in every possible scenario, there is somebody who has this incentive. But, for any reasonable voting system we can find at least one scenario where strategic voting occurs.

        # self.play(Circumscribe(gs_tex[3], color=HIGHLIGHT), run_time=2)
        # self.wait()
        # self.play(gs_tex[3].animate.set_color(GREEN))
        # self.wait()

        # And this brings us to the word “reasonable”. The problem is: Think of the dictatorship voting system where the winner is always the top preference of voter number 3. By that I mean that system always outputs the fruit in the highlighted square. This voting system actually satisfies our definition of a voting system. Also, you can check that there is no scenario in which strategic voting helps anybody.

        border2 = SurroundingRectangle(gs_tex[1], color=HIGHLIGHT)
        self.play(Transform(border, border2))
        self.wait()

        table = VotingTable(example_table_str)
        table.move_to(0.5 * UP)
        self.play(FadeIn(table))
        self.wait()

        dictator = (
            ImageMobject(
                "img/dictator-small.png"
                if DRAFT == True or SMALL_PICTURES == True
                else "img/dictator.png"
            )
            .scale_to_fit_height(2)
            .next_to(table[2], DOWN)
        )
        self.play(FadeIn(dictator))
        self.wait()

        border_fruit = SurroundingRectangle(table[2].group[0], color=HIGHLIGHT)
        self.play(FadeIn(border_fruit))
        self.wait()
        self.play(table.results_show("A"))
        self.wait()

        for pos, new, win in [
            [2, "BAC", "B"],
            [4, "ACB", "B"],
            [5, "ACB", "B"],
            [2, "CBA", "C"],
            [0, "BAC", "C"],
            [8, "BAC", "C"],
            [2, "ABC", "A"],
            [1, "CBA", "A"],
            [2, "BAC", "B"],
            [2, "CBA", "C"],
            [6, "BAC", "C"],
            [7, "BCA", "C"],
        ]:
            self.play(table[pos].rearrange(new), table.winner_show(win))
        self.wait()

        self.play(
            FadeOut(table),
            FadeOut(border_fruit),
            table.results_hide(),
            FadeOut(dictator),
        )
        self.wait()

        # This is why we can prove the theorem only for voting systems that are in some sense reasonable. But how should we define it precisely? For now, let’s choose the following definition: I will say that a voting system is reasonable if, whenever there is a candidate that is the top preference for more than half of the voters, then this candidate should be elected by the voting system.

        reasonable_group.next_to(gs_tex, DOWN, buff=1).align_to(gs_tex, LEFT)

        majority_table = (
            VotingTable(majority_table_str)
            .align_to(reasonable_group, UP)
            .shift(2 * DOWN + 1 * LEFT)
        )

        self.play(FadeIn(reasonable_group))
        self.wait()
        self.play(FadeIn(majority_table))
        self.wait()

        self.play(*majority_table.indicate(0, indexes=range(5)), run_time=2)
        self.wait()
        self.play(majority_table.winner_show("B"))
        self.wait()
        # Both the plurality voting system and the two-round system satisfy this definition of being reasonable, so the definition makes some sense. We will now prove the theorem and then we will discuss this definition a bit more.

        self.wait(10)


class Proof1(Scene):
    def construct(self):
        default()
        self.add(gs_tex)

        # Ok, let’s first try to understand why in our scenario with monkeys it was so hard to choose the best fruit. Why is it that there were always so many monkeys unhappy about the result? Well, if you look at the rankings of the monkeys, you can see that there is some kind of cycle here. Some monkeys prefer avocado over banana over coconut, some prefer banana over coconut over avocado, and some prefer coconut over avocado over banana.

        table = VotingTable(example_table_str).set_z_index(1000)
        self.play(FadeIn(table))
        self.wait()

        self.play(table.animate.next_to(gs_tex, DOWN, buff=0.5).shift(RIGHT))
        self.wait()

        w = 0.7
        rad = 1.5
        condorcet_group = VGroup(
            *(get_fruit(letter).scale_to_fit_width(w) for letter in "ABC")
        )
        vec = UP
        for i in range(3):
            condorcet_group[i].shift(rad * vec)
            vec = rotate_vector(vec, np.radians(120))

        arrows = []

        def update_label(arrow):
            arrow.label.become(MathTex(f"{arrow.a}:{arrow.b}").move_to(arrow.label))

        for i in range(3):
            start = condorcet_group[i].get_center()
            end = condorcet_group[(i + 1) % 3].get_center()
            arrow = Arrow(
                start=start,
                end=end,
                buff=w * 0.8,
                color=text_color,
            )
            dir = end - start
            dir /= (dir * dir).sum() ** 0.5
            if i == 1:
                shift = 0.4
            else:
                shift = 0.6
            arrow.label = (
                Dot().move_to(arrow).shift(shift * rotate_vector(dir, -np.radians(90)))
            )
            arrow.a, arrow.b = 0, 0
            condorcet_group.add(arrow, arrow.label)
            arrows.append(arrow)

        nums = [(7, 2), (6, 3), (5, 4)]
        for i in range(3):
            arrows[i].a, arrows[i].b = nums[i]
            update_label(arrows[i])
            arrows[i].label.fade(1)

        condorcet_group.next_to(table, DOWN, buff=0.5).shift(LEFT)

        self.play(FadeIn(condorcet_group))
        self.wait()

        # [tabulka s preferencemi, pod ní cyklus]
        # And here is the crazy thing that’s happening here. If you look at how many monkeys prefer avocado over banana
        # , it is 5:3.
        # (napíše se do condorcetova cyklu)
        # If you look at how many prefer banana over coconut, it is 6:2. And if you look at how many prefer coconut over avocado, it is again 5:3! So whatever fruit ends up being elected, there is always another candidate that, if you compare it with the winner in a head-to-head election, actually beats the winner.

        # The fact that this can happen is called Condorcet paradox and I will use the word Condorcet cycle for any such scenario, that is, any scenario with three groups of voters with cyclic preferences where also each group has less than half of all the voters.

        trash = []

        def wind_around(pref):
            anims = []
            for l in pref.ordering:
                i = ord(l) - ord("A")
                trash.append(condorcet_group[i].copy())
                anims.append(pref.at(l)[0].animate.become(trash[-1]))

            def arrow_updater(start, end, start_target):
                done = False

                orig = start.get_center()
                target = start_target.get_center()

                def updater(arrow):
                    # nonlocal done
                    # if done:
                    #    return
                    # if (start.get_center() == start_target.get_center()).all():
                    #    done = True
                    #    update_label(arrow)
                    alpha = np.linalg.norm(
                        start.get_center() - target
                    ) / np.linalg.norm(orig - target)
                    arrow.become(
                        Arrow(
                            start=start.get_center(), end=end.get_center(), buff=0.8 * w
                        )
                        .set_z_index(arrow.z_index)
                        .fade((1 - alpha) ** 2)
                    )

                return updater

            for arrow, a, b in zip(pref.arrows, pref.ordering, pref.ordering[1:]):
                i = ord(a) - ord("A")
                arrow.add_updater(
                    arrow_updater(*pref.at(a), *pref.at(b), condorcet_group[i])
                )

            return anims

        anims = []
        for i, o in enumerate(table.group):
            o.arrowed = o.copy().set_z_index(2000 - i)

        self.play(
            *(
                o.arrowed.animate.scale(1.5)
                .next_to(
                    table, LEFT, buff=(4 - ord(o.ordering[0]) + ord("A") - 0.1 * i)
                )
                .shift(DOWN)
                for i, o in enumerate(table.group)
            )
        )
        self.play(
            *(AnimationGroup(*o.arrowed.become_arrowed()) for o in table.group),
            run_time=1,
        )
        for i, o in enumerate(table.group):
            for arrow in o.arrowed.arrows:
                arrow.set_z_index(2000 - i)
        for l, r, f in [(0, 4, 2), (4, 6, 0), (6, 9, 1)]:
            f = 2 * f + 3
            self.play(FadeOut(condorcet_group[f]))
            self.play(
                AnimationGroup(
                    *(
                        AnimationGroup(*wind_around(o.arrowed), run_time=1.5)
                        for o in table.group[l:r]
                    ),
                    lag_ratio=1,
                )
            )
            for mobj in self.mobjects:
                mobj.clear_updaters()
            for o in table.group[l:r]:
                self.remove(o.arrowed)
            for o in trash:
                self.remove(o)
            self.remove(self.mobjects[-1])
            self.play(FadeIn(condorcet_group[f]))

        for a in range(3):
            b = (a + 1) % 3
            c = (b + 1) % 3
            abc = "ABC"
            self.play(
                *table.fadeout(abc[c]),
                condorcet_group[a].indicate(),
                condorcet_group[b].indicate(),
                run_time=2,
            )
            self.wait()
            update_label(arrows[a])
            self.play(*table.indicate("#"), FadeIn(arrows[a].label), run_time=2)
            self.wait()
            self.play(*table.fadein(abc[c]))
            self.wait()

        paradox_tex = Tex(r"Condorcet paradox")
        paradox_arrow = Arrow(start=ORIGIN, end=1 * LEFT)
        paradox_group = (
            Group(paradox_arrow, paradox_tex)
            .arrange(RIGHT)
            .next_to(condorcet_group, RIGHT)
        )

        cycle_tex = Tex(r"Condorcet cycle")
        cycle_arrow = Arrow(start=ORIGIN, end=1 * UP)
        cycle_group = (
            Group(cycle_arrow, cycle_tex)
            .arrange_in_grid(cols=1, cell_alignment=LEFT)
            .next_to(paradox_group, UP)
            .align_to(paradox_tex, LEFT)
        )

        self.play(FadeIn(paradox_group))
        self.wait()

        self.play(FadeIn(cycle_group))
        self.wait()

        shift = 3 * LEFT + UP
        self.play(
            FadeOut(paradox_group, cycle_group, table),
            condorcet_group.animate.shift(shift),
        )
        implies_counterexample = (
            Tex(r"$\Rightarrow$ strategic voting").scale(1.5).next_to(condorcet_group)
        )
        self.wait()
        self.play(FadeIn(implies_counterexample), run_time=1.5)
        self.wait(3)

        # Ultimately, condorcet paradox is the reason why voting is straightforward with two candidates, but becomes very tricky if you have at least three of them.

        # TODO animace kde se ztratí kokos a cyklus změní na šipku?

        self.play(*[FadeOut(o) for o in self.mobjects if o != gs_tex])
        self.wait()


class Proof2(MovingCameraScene):
    def construct(self):
        default()
        self.add(gs_tex)
        self.next_section(skip_animations=False)
        # Remember, our goal is to demonstrate that for any reasonable voting system, there exists a scenario where a certain voter has an incentive to vote strategically. It turns out that any Condorcet cycle is almost, but not quite, such a scenario.

        self.play(Circumscribe(gs_tex, color=HIGHLIGHT))
        self.wait()

        tables = VGroup(*[VotingTable(str).shift(LEFT) for str in proof_table_strings])
        table = tables[0].copy()

        # self.play(FadeIn(tables[2]))  # TODO

        # self.play(FadeOut(tables[2]))

        # Let me explain. Let’s consider an arbitrary reasonable voting system like plurality voting or the two-round system. The system needs to elect a winner in this Condorcet cycle. Without loss of generality, let’s say that it elects the coconut.

        self.play(FadeIn(table))
        self.wait()
        self.play(table.winner_show("C"))
        self.wait()

        # But now let’s look at this group of voters for whom the coconut is the bottom choice. Intuitively, these voters have the biggest incentive to try some kind of strategic voting because they are most unhappy with the result.

        border = SurroundingRectangle(Group(*table[:4]), color=HIGHLIGHT)
        self.play(FadeIn(border))
        self.wait()

        # What if all these voters simultaneously cast a ballot that swaps avocado and banana?

        self.play(
            *table.rearrange("BAC", indexes=range(4)),
        )
        self.wait()
        # self.play(FadeOut(border))
        # self.wait()

        # In this case, you can see that by the properties of the Condorcet cycle, a majority of voters have the banana as their first choice. But wait a minute, our definition of a reasonable voting system says that in this case, the voting system has to elect the banana as the winner.

        border.generate_target()
        border.target = SurroundingRectangle(
            Group(table[0].group[1], table[5].group[0]), color=HIGHLIGHT
        )
        border.save_state()

        self.play(MoveToTarget(border))
        self.wait()

        reasonable_group.next_to(gs_tex, DOWN, buff=0.5)

        self.play(FadeIn(reasonable_group))
        self.wait()

        self.play(table.winner_show("B"))
        self.wait()

        self.play(border.animate.restore(), FadeOut(reasonable_group))
        self.wait()

        for x in range(3):
            self.play(*table.rearrange("ABC", indexes=range(4)), table.winner_show("C"))
            self.wait(0.2)

            if x == 2:
                break

            self.play(
                *table.rearrange("BAC", indexes=range(4)), table.winner_show("B", DOWN)
            )
            self.wait(0.2)

        self.play(table.results_hide())
        self.wait()

        # So, if all of these voters coordinate and vote strategically, they can achieve a result that they like more than what happens when they tell the truth. This is by the way exactly what the four sly monkeys did at the beginning when we tried to use the two-round system to elect the winner.
        # We are already very close to proving the theorem. The only problem is that we want to find a scenario where only one voter has the incentive to vote strategically. Right now, that is not the case. Only if this whole group can coordinate, it pays off.

        self.play(Indicate(border, color=HIGHLIGHT))
        self.wait()

        self.play(FadeOut(border), FadeOut(gs_tex))
        self.wait()

        # Here is the idea needed to finish the proof. For a minute, forget strategic voting and just think of these two scenarios as inputs to the voting system. We know that the voting system elects the coconut in the first scenario and the avocado in the second one. Now let’s imagine all of these intermediate inputs to the voting system where each time just one monkey flips the avocado with the banana.

        # We don’t really know who the winner is in these intermediate situations, after all, we are considering an arbitrary voting system in our proof. But because the winner is different at the beginning and at the end, we know that it has to change at some point.

        for t in tables:
            t.scale(0.5)
        tables.arrange(DOWN, buff=0.5)
        tables.move_to(ORIGIN)

        scale = 2.5
        self.play(
            Transform(table, tables[0]),
            self.camera.frame.animate.scale(1 / scale).move_to(tables[0:2]),
        )
        # self.play(Circumscribe(Group(table[0].group[0], table[5].group[1]), color=HIGHLIGHT))
        self.wait()

        for i, table in enumerate(tables[:-1]):
            self.play(self.camera.frame.animate.move_to(tables[i : i + 2]))
            self.add(tables[i])
            table = tables[i].copy()
            self.play(table.animate.next_to(tables[i], DOWN, buff=MED_LARGE_BUFF))
            self.play(table[i].rearrange("BAC"))
            shift = tables[i].get_center() - table.get_center()
            # self.play(table.animate.shift(shift), tables[: i + 1].animate.shift(shift))
            self.remove(table)

        self.play(self.camera.frame.animate.move_to(tables).scale(scale))
        self.play(
            tables[0].winner_show("C"),
        )
        self.wait()
        self.play(
            tables[-1].winner_show("B"),
        )
        self.wait()

        self.add(tables[0].results)
        self.play(Circumscribe(tables[0], color=HIGHLIGHT))
        self.wait()

        self.play(*[t.winner_show("?") for t in tables[1:-1]])
        self.wait()

        self.play(
            Succession(
                tables[1].winner_show("C"),
                Wait(),
                tables[2].winner_show("C"),
                Wait(),
                tables[3].winner_show("D"),
                Wait(),
            )
        )

        # So let’s look at the two scenarios where the winner changes for the first time, from the coconut to some other candidate.

        border = SurroundingRectangle(Group(*tables[2:4]), color=HIGHLIGHT)

        self.play(FadeIn(border))
        self.wait()

        self.next_section(skip_animations=False)
        dif = 4 * DOWN

        sc = 2.5
        tables.generate_target()
        tables.target.scale(sc)
        tables.target.arrange(DOWN, buff=3)
        where = (tables.target[2].get_center() + tables.target[3].get_center()) / 2.0
        tables.target.shift(-where + 1 * LEFT)
        self.remove(*self.mobjects)

        border.generate_target()
        border.target = SurroundingRectangle(
            Group(*tables.target[2:4]), color=HIGHLIGHT
        )

        winner_groups = []
        for i in range(5):
            winner_groups.append(Group(tables[i].results.winner, tables[i].arrow))
            winner_groups[i].generate_target()
            winner_groups[i].target.scale(sc).next_to(tables.target[i], RIGHT)

        # grp = Group(
        #     tables,
        #     border,
        #     Group(*( for table in tables)),
        # )

        # self.add(grp)
        self.play(
            MoveToTarget(tables),
            MoveToTarget(border),
            *[MoveToTarget(g) for g in winner_groups],
        )
        self.wait()

        self.play(FadeOut(border))

        borders = [
            SurroundingRectangle(tables[2][2], color=HIGHLIGHT),
            SurroundingRectangle(tables[3][2], color=HIGHLIGHT),
        ]

        self.play(FadeIn(Group(*borders)))
        self.wait()

        # self.play(
        #     FadeOut(Group(tables[2][2], tables[3][2]))
        # )
        # self.wait()

        # self.play(
        #     # FadeIn(Group(tables[2][2], tables[3][2])),
        #     FadeOut(Group(*borders))
        # )
        # self.wait()

        monkey = img_monkey("A", width=1.5).shift(0 * sc * LEFT)

        bubble = (
            load_svg("img/bubble_think.svg")
            .scale_to_fit_height(1.5 * sc)
            .next_to(monkey, LEFT)
            .shift(1 * sc * UP)
        )

        self.play(FadeIn(monkey))
        self.play(
            FadeIn(bubble),
            FadeOut(borders[0]),
            tables[2][:2].animate.shift(1 * LEFT),
            Group(
                tables[2][3:], tables[2].results.winner, tables[2].arrow
            ).animate.shift(1 * RIGHT),
        )
        self.wait()

        self.play(Circumscribe(tables[2].results.winner, color=HIGHLIGHT))
        self.wait()

        bubble2 = (
            load_svg("img/bubble_say.svg")
            .rotate(PI)
            .scale_to_fit_height(1.5 * sc)
            .next_to(monkey, LEFT)
            .shift(1 * sc * DOWN)
        )

        self.play(
            FadeIn(bubble2),
            FadeOut(borders[1]),
            tables[3][:2].animate.shift(1 * LEFT),
            Group(
                tables[3][3:], tables[3].results.winner, tables[3].arrow
            ).animate.shift(1 * RIGHT),
        )
        self.wait()

        self.play(Circumscribe(tables[3].results.winner, color=HIGHLIGHT))
        self.wait()

        self.play(Circumscribe(tables[2], color=HIGHLIGHT))
        self.wait()

        # Let’s also focus on this voter. Do you see how to finish the proof? Well, let’s imagine that the top scenario contains the honest preferences of all the voters. If this voter votes honestly, X is the winner. But what if they vote strategically and cast a ballot with ZYX instead of YZX? Well, we know that then the outcome of the voting system changes from X to some other candidate. But look, X is the worst option for our voter, so whatever the change, the voter will prefer it!

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()

        table = VotingTable(example_table_str)
        self.play(FadeIn(table))
        self.wait()

        self.play(table.winner_show("C"))
        self.wait()

        self.play(table[0].rearrange("BAC"))
        self.play(table[1].rearrange("BAC"))

        for _ in range(3):
            self.play(table[2].rearrange("BAC"), table.winner_show("D"))
            self.play(table[2].rearrange("ABC"), table.winner_show("C"))

        self.wait(5)

        # And this finishes the proof of the Gibbard-Satterthwaite theorem. To summarize, if you come up with any reasonable voting system, I can look at any Condorcet cycle scenario and tweak it a little bit to find a scenario where your voting system gives some voter the incentive to vote strategically.


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

        self.play(*table.highlight("A", indexes=range(5, len(table.group))))
        self.wait()

        self.play(*table.highlight("B", indexes=range(0, len(table.group))))
        self.wait()
        # self.play(*table.highlight("B", indexes=range(5)))
        # self.wait()

        # So maybe we should think about the theorem one more time and try to prove it with a definition of “reasonable” that permits as many voting systems as possible. That is exactly what Gibbard and Satterthwaite did, this is their theorem in full glory. They found out that these two conditions on the voting system suffice to prove the theorem, and they are also necessary. The proof of this more general theorem is similar to our proof but more tedious, so let’s skip it.

        line.save_state()
        table.save_state()
        table.results.winner.save_state()
        table.arrow.save_state()

        r_tex = Tex(r"Reasonable = ??").next_to(gs_group, DOWN).shift(1 * DOWN)
        self.play(
            Group(line, table, table.results.winner, table.arrow).animate.shift(
                2 * DOWN
            ),
        )
        self.play(
            FadeIn(r_tex),
        )
        self.wait()

        self.play(FadeOut(gs_tex), FadeOut(r_tex))
        self.wait()
        self.play(
            FadeIn(gs_new_tex),
        )  # line.animate.next_to(gs_new_tex, DOWN))
        self.wait()

        self.play(Circumscribe(Group(*gs_new_tex[1:3]), color=HIGHLIGHT))
        self.wait()

        self.play(FadeOut(gs_new_tex))
        self.wait()
        self.play(
            FadeIn(gs_tex),
            # line.animate.next_to(gs_tex, DOWN),
            FadeOut(line),
            FadeOut(Group(table, table.arrow, table.results.winner)),
            # table.animate.restore(),
            # table.arrow.animate.restore(),
            # table.results.winner.animate.restore(),
        )
        self.wait()


class ArrowThm(Scene):
    def construct(self):
        default()
        # There is one more related theorem I want to mention – Arrow’s theorem.

        self.add(gs_group.to_edge(UP, buff=0.5))
        arrow_title = Tex(r"Arrow's Theorem:")
        arrow_tex = Tex(
            r"{{\parbox{1000em}{No reasonable voting system satisfies the }}{{independence of irrelevant alternatives.} }}"
        ).scale(thm_scale * 0.85)
        arrow_full = (
            Group(arrow_title, arrow_tex)
            .arrange(DOWN)
            .next_to(gs_group, DOWN, buff=0.5)
        )

        self.play(FadeIn(arrow_title))
        self.wait()

        # That theorem also talks about voting systems, but a little bit more general ones that not only elect the winner but rank all the candidates from best to worst.

        table = VotingTable(example_table_str).shift(2 * LEFT + 1.5 * DOWN)

        self.play(FadeIn(table))
        self.wait()

        self.play(table.results_show("ABC"))
        self.wait()

        # (animace s tabulkou, outcome se změní z vítěze na order)

        # Arrow’s theorem says that if there are at least three candidates, any reasonable voting system for ordering them will not satisfy the so-called independence of irrelevant alternatives.

        # This is a condition that says that if you look at how the voting system orders any two candidates, for example here it decides that banana is above coconut

        self.play(*table.results.highlight("A"))
        self.wait()
        self.play(*table.results.highlight("B"))
        self.wait()
        # (vyznačí se že outcome je banana lepší než coconut nebo naopak)

        # this decision should not depend on whatever the voters’ opinion on the avocado is.

        self.play(*table.fadeout("C"), *table.results.fadeout("C"))
        self.wait()

        # In other words, in all of these situations, the banana has to be above the coconut.
        # [animace kde avocado skáče nahoru a dolu u různých voterů, outcome je furt banana lepší než coconut]

        # self.play(
        #     Succession(
        #         AnimationGroup(table[0].rearrange("ABC")),
        #         AnimationGroup(table[1].rearrange("ABC"), table.results_show("BAC")),
        #         AnimationGroup(table[2].rearrange("ABC")),
        #     )
        # )

        # self.play(
        #     *(
        #         AnimationGroup(table[i].rearrange(example_table_str[i]))
        #         for i in range(len(example_table_str))
        #     )
        # )

        # TODO pridat neco takovehleho

        mkarrow = lambda: CurvedArrow(
            table.results.at("A")[0][1].get_center() + 0.5 * RIGHT,
            table.results.at("B")[0][1].get_center() + 0.5 * RIGHT,
            angle=-TAU / 4,
        )
        ar = mkarrow()
        ar.add_updater(lambda obj: obj.become(mkarrow()))
        self.play(FadeIn(ar))
        self.wait()

        for _ in range(2):
            l = list(range(len(example_table_str))) + list(
                range(len(example_table_str) - 2, 0, -1)
            )
            for i in l:
                anims = []
                anims.append(table[i].random_change("C"))
                if random.randint(0, 2) == 0:
                    anims.append(
                        table.results_show(random.choice(["ABC", "ACB", "CAB"]))
                    )
                self.play(*anims)

        ar.clear_updaters()
        self.wait()

        # The first part of our proof can actually be used to prove a version of Arrow’s theorem, but if you use the textbook definition of a reasonable voting system, the proof again becomes a bit tedious.

        # Both Arrow and Gibbard-Satterthwaite theorems are good examples showing that while we often like to think that important mathematical theorems are simply-looking statements that turn out to be insanely complicated to prove, it is not always like that.
        # (možná někde problikne statement Fermata nebo P vs NP?)

        self.play(FadeIn(arrow_tex))
        self.wait()

        self.play(table.results_hide(), FadeOut(table), FadeOut(ar))
        self.wait()

        fermat_tex = Tex(
            r"Does $a^n + b^n = c^n, n > 2$ \\ have solutions in $\mathbb{N}$?"
        )
        pnp_tex = Tex(r"Does P = NP?")
        thm_group = Group(fermat_tex, pnp_tex).arrange(RIGHT, buff=3).shift(1 * DOWN)

        self.play(
            Succession(
                FadeIn(fermat_tex),
                FadeIn(pnp_tex),
                Wait(),
            )
        )
        self.play(FadeOut(thm_group))
        self.wait()

        # For me, the biggest insight of those two theorems is simply noticing that there is something to prove. Strategic voting is not just a sociological fact, but it is a fundamental flaw of every voting system, and so is the lack of independence of irrelevant alternatives. Or is it?

        border = SurroundingRectangle(gs_tex[4], color=HIGHLIGHT)
        border2 = SurroundingRectangle(arrow_tex[1], color=HIGHLIGHT)

        self.play(FadeIn(border))
        self.wait()
        self.play(Transform(border, border2))
        self.wait()

        explorer = (
            ImageMobject(
                f"img/explorer{'_small' if DRAFT == True or SMALL_PICTURES == True else ''}.png"
            )
            .scale_to_fit_width(12)
            .shift(5 * DOWN)
        )

        self.play(arrive_from(explorer, DOWN))
        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects if o != explorer],
            explorer.animate.shift(5 * DOWN),
        )
        self.wait()

        # [vsauce pauza + trošku zoom?]


class Approval(Scene):
    def construct(self):
        default()

        # It turns out that the full story is more complicated; to understand why, let’s look at one popular voting system called approval voting. This is an extremely simple voting system where every voter can give a vote to as many candidates as they want and then you order the candidates by how many votes they got.

        approval_tex = Tex("Approval voting").scale(2).to_edge(UP)
        self.play(FadeIn(approval_tex))
        self.wait()

        nothing = Dot().scale(0.00001)
        thumbsup_img = load_svg("img/icon.svg").scale(0.3)
        w = 1
        monkey_img1 = img_monkey("A").scale_to_fit_width(w)
        monkey_img2 = img_monkey("B").scale_to_fit_width(w)
        monkey_img3 = img_monkey("C").scale_to_fit_width(w)

        fruit_width = 1

        approval_data = [
            [
                nothing.copy(),
                monkey_img1.copy(),
                monkey_img3.copy(),
                monkey_img3.copy(),
                monkey_img1.copy(),
                monkey_img2.copy(),
                monkey_img2.copy(),
                Tex("Sum"),
            ],
            [
                FRUITS["A"].copy().scale(fruit_width),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                nothing.copy(),
                Tex("3"),
            ],
            [
                FRUITS["B"].copy().scale(fruit_width),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                Tex("5"),
            ],
            [
                FRUITS["C"].copy().scale(fruit_width),
                nothing.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                thumbsup_img.copy(),
                nothing.copy(),
                thumbsup_img.copy(),
                Tex("4"),
            ],
        ]
        approval_table = Group(
            *[item for row in approval_data for item in row]
        ).arrange_in_grid(rows=4, buff=0.3)

        Group(*[approval_data[i][-1] for i in range(4)]).shift(1 * RIGHT)

        self.play(
            Succession(
                *[
                    AnimationGroup(*[FadeIn(approval_data[i][j]) for i in range(4)])
                    for j in range(len(approval_data[0]))
                ]
            )
        )
        self.wait()

        lines = [Group(*approval_data[i]) for i in range(1, 4)]

        for i, j in [[0, 1], [0, 2]]:
            lines[i].generate_target()
            lines[i].target.move_to(lines[j].get_center())
            lines[j].generate_target()
            lines[j].target.move_to(lines[i].get_center())

            self.play(
                MoveToTarget(lines[i]),
                MoveToTarget(lines[j]),
            )
            self.wait()

        self.play(FadeOut(approval_table))
        self.wait()

        # For example, if you order the videos of your favorite YouTuber by popularity, one way you can do it is by sorting them by how many likes they got, and that is basically approval voting, with the addition of negative votes.

        v_width = 2
        v_scale = 0.7
        videos_data = []

        thumb_data = [
            ["img/thumbnail1.png", "17k likes"],
            ["img/thumbnail2.png", "2k likes"],
            ["img/thumbnail3.png", "5k likes"],
            ["img/thumbnail4.png", "35k likes"],
        ]

        for str1, str2 in thumb_data:
            img = ImageMobject(str1).scale_to_fit_width(v_width)
            border = SurroundingRectangle(img, color=GRAY, buff=0)
            tex = Tex(str2).scale(v_scale)
            gr = Group(Group(img, border), tex).arrange_in_grid(
                cols=1, cell_alignment=LEFT, buff=0.1
            )
            videos_data.append(gr)

        videos_group_table = Group(*videos_data).arrange_in_grid(cols=2, buff=0.8)

        self.play(*[FadeIn(v) for v in videos_group_table])
        self.wait()

        videos_group = Group(*[videos_group_table[i] for i in [3, 0, 2, 1]])
        self.play(videos_group.animate.arrange(DOWN, buff=0.5).shift(5 * LEFT))
        self.wait()

        # The way we order movies by their average rating is also similar to approval voting.
        # [třeba: pár videí od polylogu a u nich napsané kolik mají liků, potom záběr na imdb/netflix a nějaký seznam top filmů]

        movies_img = (
            ImageMobject("img/movies_short.png")
            .scale_to_fit_width(6)
            .shift(1 * RIGHT)
            .to_edge(DOWN, buff=0.5)
        )
        self.play(FadeIn(movies_img))
        self.wait()

        self.play(FadeOut(videos_group), FadeOut(movies_img))
        self.wait()

        # But notice that approval voting and its variants do not fit our definition that a voting system requires every voter to simply rank the candidates on the ballot and uses this information

        monkeys_img = (
            Group(*[img_monkey(pref[0], width=1) for pref in example_table_str])
            .arrange()
            .to_edge(LEFT, buff=1)
            .to_edge(DOWN)
            .shift(0.5 * UP)
        )

        table = VotingTable(example_table_str).scale(1.5).shift(0.5 * DOWN)
        monkey_scale = 0.4
        for col, monkey in zip(table.group, monkeys_img):
            col.save_state()
            col.scale(monkey_scale).next_to(monkey, UP)

        self.play(
            AnimationGroup(
                FadeIn(monkeys_img),
                lag_ratio=0.3,
            ),
            FadeIn(table),
        )

        self.wait()
        self.play(
            *(
                col.animate.scale(1 / monkey_scale).move_to(col.saved_state)
                for col in table.group
            ),
            FadeOut(monkeys_img),
        )
        self.wait()
        input_brace = BraceLabel(table, "input", UP)
        self.play(FadeIn(input_brace))

        # table = VotingTable(example_table_str).scale(0.5)  # .to_edge(RIGHT, buff = 2)

        # self.play(AnimationGroup(*table.indicate(), lag_ratio=0.51))
        # self.wait()

        # # to elect the winner.

        # self.play(table.winner_show("A"))
        # self.wait()
        # self.play(FadeOut(table))
        # self.wait()

        # Even if I tell you how I would rank these videos, you still don’t know which ones of them I would give a like to.

        # for v in videos_group:
        #     v.generate_target()
        # videos_group2 = Group(*[videos_data[i].target for i in [3, 2, 1, 0]]).arrange(DOWN).move_to(videos_group.get_center())

        # self.play(
        #     *[MoveToTarget(v) for v in videos_group]
        # )
        # self.wait()

        self.play(FadeOut(Group(table, input_brace)))
        self.wait()

        videos_group = (
            Group(
                *[
                    Group(g[0], Tex(f"{i+1}. ")).arrange(LEFT)
                    for i, g in enumerate(videos_group)
                ]
            )
            .arrange(DOWN, buff=0.3)
            .next_to(approval_tex, DOWN, buff=0.5)
            .shift(2 * LEFT)
        )

        text_group = Group(*(g[1] for g in videos_group))
        videos_group = Group(*[g[0] for g in videos_group])

        self.play(FadeIn(videos_group))
        self.wait()

        self.play(
            AnimationGroup(
                *[FadeIn(t) for t in text_group], lag_ratio=0.5, group=text_group
            ),
        )
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

        self.play(FadeIn(likes[0]))
        self.play(FadeIn(likes[1]))
        self.play(
            likes[0].animate.rotate(PI),
            likes[1].animate.rotate(PI),
            *[FadeIn(dislikes[i]) for i in range(2, 4)],
        )
        self.wait()

        self.play(
            FadeOut(arrow),
            *(FadeOut(t) for t in text_group),
            *[FadeOut(o) for o in (set(likes + dislikes) & set(self.mobjects))],
        )
        self.play(
            Group(*[g for g in videos_group])
            .animate.arrange_in_grid(rows=2)
            .shift(1 * LEFT)
        )
        self.wait()

        # So, our proofs of Arrow and Gibbard-Satterthwaite don't directly apply to these types of voting systems. And actually, Arrow’s theorem cannot hold there, because approval voting does satisfy the independence of irrelevant alternatives: If I tell you that [video] got X likes and [video] got Y likes, you know that in the final ranking, [video] will be above [video] and this conclusion is not affected by how many likes all the other videos got. So Arrow’s theorem may not be as fundamental as it looked like.

        i1 = 0
        j1 = 3
        i2 = 3
        j2 = 2

        st = 2.5 * RIGHT
        self.play(videos_group[i1].animate.move_to(st + 1.5 * UP))
        tex1 = Tex(thumb_data[j1][1]).next_to(videos_group[i1], RIGHT, buff=0.5)
        self.play(FadeIn(tex1))
        self.wait()
        # self.play(videos_group[i1][1].animate.set_color(text_color))
        self.play(videos_group[i2].animate.move_to(st + 1.5 * DOWN))
        tex2 = Tex(thumb_data[j2][1]).next_to(videos_group[i2], RIGHT, buff=0.5)
        self.play(FadeIn(tex2))
        self.wait()
        # self.play(videos_group[i2][1].animate.set_color(text_color))

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
            Group(*[videos_group[i].target for i in [0, 1, 3, 2]])
            .arrange(DOWN)
            .move_to(greater_tex.get_center())
            .next_to(approval_tex, DOWN, buff=0.5)
            .shift(st)
        )
        self.play(FadeOut(greater_tex))
        shft1 = (videos_group[i1].get_center() - videos_group[i1].target.get_center())[
            1
        ] * DOWN
        shft2 = (videos_group[i2].get_center() - videos_group[i2].target.get_center())[
            1
        ] * DOWN
        self.play(
            *[MoveToTarget(v) for v in videos_group],
            tex1.animate.shift(shft1),
            tex2.animate.shift(shft2),
        )

        self.play(*[v[1].animate.set_color(text_color) for v in videos_group])
        self.wait()

        # However, even the approval voting system sometimes incentivizes strategic voting! For example, if you really want this video to become our most liked video, but you see that currently, it is only the fifth one, you should first give it a like (and subscribe!). But then you should also dislike all the videos above it, regardless of your opinion of them. You can in fact generalize Gibbard-Satterthwaite theorem so that it applies to pretty much every voting system, so, unfortunately, in one way or another, strategic voting will always be with us.

        # self.play(videos_group.animate.move_to(ORIGIN).next_to(approval_tex, DOWN))
        # self.wait()

        ar_tex = Tex(
            r"{{\raggedright Arrow's Theorem\\}}{{\;\;\;\;\;\;\;$\rightarrow$ not so fundamental}}"
        )
        gs_tex = Tex(
            r"{{\raggedright Gibbard-Satterthwaite Theorem\\}}{{\;\;\;\;\;\;\;$\rightarrow$ super-duper fundamental}}"
        )
        Group(ar_tex[1], gs_tex[1]).scale(0.8)

        smart_tex = (
            Group(ar_tex, gs_tex)
            .arrange_in_grid(cols=1, cell_alignment=LEFT, buff=1.5)
            .to_edge(LEFT)
        )

        self.play(FadeIn(ar_tex))
        self.wait()

        self.play(FadeOut(Group(tex1, tex2)))
        self.wait()

        i_like = 3

        self.play(videos_group[i_like][1].animate.set_color(HIGHLIGHT))
        self.wait()

        self.play(
            FadeIn(thumbsup_img.copy().next_to(videos_group[i_like], RIGHT, buff=1))
        )
        self.wait()

        self.play(
            *[
                FadeIn(
                    thumbsup_img.copy()
                    .rotate(PI)
                    .next_to(videos_group[i], RIGHT, buff=1)
                )
                for i in range(len(videos_group))
                if videos_group[i].get_center()[1]
                > videos_group[i_like].get_center()[1]
            ]
        )
        self.wait()

        self.play(FadeIn(gs_tex))
        self.wait(5)


class Debriefing(Scene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)

        # But how big of a problem is it, actually? First of all, there are many situations where strategic voting is not really the main concern. For example, when you want to rank movies or entries to a math exposition contest, how well the voting system scales with the number of candidates is probably a bigger issue than strategic voting.
        # https://www.3blue1brown.com/blog/some2
        # https://www.youtube.com/playlist?list=PLnQX-jgAF5pTZXPiD8ciEARRylD9brJXU

        w = 5
        some_left_img = ImageMobject(
            f"img/some1{'-small.png' if DRAFT == True or SMALL_PICTURES == True else '.jpg'}"
        ).scale_to_fit_width(w)
        some_leftleft_img = ImageMobject("img/some1left.png").scale_to_fit_width(
            w * 0.3
        )
        some_right_img = ImageMobject(
            f"img/some2{'-small' if DRAFT == True or SMALL_PICTURES == True else ''}.png"
        ).scale_to_fit_width(w)
        Group(some_left_img, some_right_img).arrange(RIGHT)
        some_left_img.to_edge(UP)
        some_right_img.to_edge(UP)
        some_leftleft_img.align_to(some_left_img, UL).shift(
            w * 0.065 * RIGHT + w * 0.06 * DOWN
        )

        self.add(some_left_img, some_leftleft_img, some_right_img)

        self.play(
            some_left_img.animate(rate_func=ease_in_out_quadlinear(0.15)).to_edge(DOWN),
            some_right_img.animate(rate_func=ease_in_out_quadlinear(0.15)).to_edge(
                DOWN
            ),
            run_time=10,
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
            r"Most systems are not going to work badly all of the time. \\ All I proved is that all can work badly \emph{at} times."
        )
        Group(quote_tex, arrow_group).arrange(DOWN, buff=0.7).shift(0.5 * UP)

        self.play(FadeIn(arrow_group))
        self.wait()
        self.play(Write(quote_tex), run_time=5)
        self.wait()
        self.play(FadeOut(arrow_group), FadeOut(quote_tex))
        self.wait()

        # Some systems actually work pretty well most of the time - imagine political elections based on approval voting and try to come up with a plausible scenario where a lot of people would vote strategically - it is actually not so easy!

        # TODO

        # Some time back, a small group of voting theorists ranked the voting systems on how good they are for political elections and approval voting actually ended up on the top.
        self.next_section(skip_animations=False)

        voting_data = [
            [
                Tex(r"\textbf{Position}"),
                Tex(r"\textbf{Method}"),
                Tex(r"\textbf{Approval votes}"),
            ],
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
            .to_edge(UP, buff=0.5)
        )
        Group(*voting_data[0]).shift(0.2 * UP)

        self.play(
            AnimationGroup(
                *[FadeIn(Group(*row[:2])) for row in voting_data], lag_ratio=0.25
            )
        )
        self.wait()

        self.play(Circumscribe(Group(*voting_data[1][0:2]), color=HIGHLIGHT))
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
                color=HIGHLIGHT,
            )
        )
        self.wait()

        arrow = (
            load_svg("img/arrow.svg")
            .scale_to_fit_width(1.5)
            .next_to(voting_data[1][0], LEFT, buff=0.5)
        )
        self.play(FadeIn(arrow))
        self.wait()
        self.play(arrow.animate.next_to(voting_data[2][0], LEFT, buff=0.5))
        self.wait()

        self.play(arrow.animate.next_to(voting_data[5][0], LEFT, buff=0.5))
        self.wait()

        self.play(
            voting_group.animate.shift(
                voting_data[5][0].get_center() - voting_data[-1][0].get_center()
            ),
            run_time=2,
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
            .arrange_in_grid(cols=2, cell_alignment=RIGHT)
            .shift(2.8 * DOWN)
            .to_edge(LEFT)
        )

        self.play(arrive_from(bush_gore_table, LEFT))
        self.wait(0.3)
        self.play(bush_gore_table.animate.shift(5 * LEFT))
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
        Group(*shame_table[20:]).shift(1.2 * DOWN)
        Group(*shame_table[:20]).shift(1.5 * UP)
        shame_tex = Tex("Shame.", font_size=300).shift(0.1 * DOWN)

        self.play(
            AnimationGroup(
                Succession(*[FadeIn(o) for o in shame_table], lag_ratio=0.2),
                AnimationGroup(FadeIn(shame_tex), run_time=11),
            )
        )
        self.wait(5)


class Outro(MovingCameraScene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)
        (
            monkeys_img,
            monkeys_voting_img,
            orderings,
            explorer,
            background,
            whiteboard,
        ) = intro_images(False)
        self.add(background, explorer, whiteboard, *monkeys_img)

        zoom = 0.17
        where = whiteboard.get_center() + 0.5 * UP
        shame_img = (
            ImageMobject("img/shame.png")
            .scale_to_fit_width(config["frame_width"] * zoom)
            .move_to(where)
        )
        self.add(shame_img)
        self.camera.frame.save_state()
        self.camera.frame.scale(zoom).move_to(where)
        self.play(self.camera.frame.animate.restore())
        self.wait()

        # [tady se zase může “oddálit tabule”]
        # So, my dear monkeys, the short answer is that voting is complicated. But, as a practical choice, I would recommend you to use…

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(
                explorer.get_center() + 1.5 * UP
            )
        )
        self.wait()

        # Hold on a second! I have an idea! How about making the vote randomized?
        # [je vtipná jednoduchá animace pro heuréka moment? ]

        ex2 = explorer.copy()
        self.play(
            Flash(
                explorer.get_center() + 1.5 * UP + 0 * RIGHT,
                line_length=2,
            ),
            AnimationGroup(FadeIn(ex2), run_time=0.00001),
        )
        self.remove(ex2)
        self.wait()

        self.play(self.camera.frame.animate.restore())
        self.wait()

        # It will work like this: Every monkey gives me a ballot featuring only their most preferred candidate, then I elect the winner by shuffling all the ballots and choosing a random one.

        self.play(
            *[
                Interpol(monkeys_img[i], monkeys_voting_img[i][0])
                for i in range(len(monkeys_img))
            ]
        )
        self.wait()

        anims = []
        for i in range(len(monkeys_img)):
            start = monkeys_voting_img[i][0][1].get_center()
            end = (
                explorer.get_center()
                + 0.5 * RIGHT
                + 0.2 * DOWN
                + random.uniform(0, 0.2) * RIGHT
            )
            midpoint = (start + end) / 2
            midpoint[1] = max(start[1], end[1])
            midpoint += 1 * UP

            a = 2 * end[1] - 4 * midpoint[1] + 2 * start[1]
            b = 4 * midpoint[1] - 3 * start[1] - end[1]
            c = start[1]

            path = ParametricFunction(
                lambda t: np.array(
                    [t * end[0] + (1 - t) * start[0], a * t**2 + b * t + c, 0]
                ),
                t_range=[0, 1],
            )

            # self.add(path)
            anims.append(
                MoveAlongPath(monkeys_voting_img[i][0][1].set_z_index(999), path)
            )

            # print(start, midpoint, end)

        random.shuffle(anims)

        explorer_bag = (
            ImageMobject(
                f"img/explorer_bag{'_small' if DRAFT or SMALL_PICTURES else ''}.png"
            )
            .scale_to_fit_width(explorer.width)
            .move_to(explorer.get_center())
            .set_z_index(1042)
        )

        self.play(
            *anims,
            *[
                Interpol(monkeys_voting_img[i][0][0], monkeys_img[i])
                for i in range(len(monkeys_img))
            ],
            AnimationGroup(FadeIn(explorer_bag), run_time=0.0001),
        )
        # self.play(
        #     *[FadeOut(monkeys_voting_img[i][0][1]) for i in range(len(monkeys_img))]
        # )
        self.wait()

        for _ in range(3):
            self.play(
                Wiggle(
                    Group(
                        explorer,
                        *[monkeys_voting_img[i][0][1] for i in range(len(monkeys_img))],
                        explorer_bag,
                    ),
                    scale_value=1,
                )
            )
        self.wait()

        self.add_sound("audio/drum_roll.mp3")
        self.wait(4)
        self.add_sound("audio/polylog_success.wav")

        # Clearly, strategic voting does not help in this voting system because if your ballot is chosen, you definitely want your most preferred candidate to be on it!  Also, the more monkeys vote for a candidate, the more likely the candidate is to be elected – I think it’s really amazing actually!

        # opičky podezřívavě: “ok?”
        # (udělá se to)

        # … and the winner is

        # [napínavá hudba jako bubnování nebo tak něco]

        # a coconut! A few monkeys were quite happy,

        winner_img = [
            get_crowned_fruit(label, True).move_to(5 * RIGHT).scale(3)
            for label in "ABC"
        ]
        self.next_section(skip_animations=False)

        # self.play(
        #     FadeIn(winner_img[1])
        # )
        # self.wait()

        self.play(
            monkeys_voting_img[4][0][1]
            .animate.move_to(
                explorer.get_center() + 0.5 * RIGHT + 0.2 * DOWN + 0.5 * LEFT + 1 * UP
            )
            .scale(1.3)
        )
        self.play(
            Flash(
                monkeys_voting_img[4][0][1].get_center() + 0.2 * LEFT,
                line_length=2,
            ),
            AnimationGroup(
                FadeIn(monkeys_voting_img[4][0][1].copy()), run_time=0.00001
            ),
        )
        self.wait()

        h = 1
        self.play(
            ApplyMethod(monkeys_img[4].shift, UP * h),
            ApplyMethod(monkeys_img[5].shift, UP * h),
            rate_func=rush_from,  # Slow down as it moves upwards
            run_time=0.5,  # Duration of the up motion
        )

        self.play(
            ApplyMethod(monkeys_img[4].shift, DOWN * h),
            ApplyMethod(monkeys_img[5].shift, DOWN * h),
            rate_func=rush_into,  # Slow down as it moves upwards
            run_time=0.5,  # Duration of the up motion
        )
        self.wait()

        # “Yay!”

        # but the rest of them…

        # [opičky začnou protestovat nebo házet banány nebo něco jiného, paňáček uteče ze záběru]

        # “Hey, You didn’t shuffle them enough, redo it!”
        # “No, You shuffled way too much!”
        # "This was supposed to be a random fruit, not coconut!"
        # "stolen elections!"

        indices = [0, 8, 2, 7]
        for i in indices:
            self.play(Wiggle(monkeys_img[i]))
            self.wait()

        # TODO risa podivat se jestli zbude cas

        anims = []
        monkey_angry_pos = [monkeys_img[i].get_center() for i in [0, 1, 2, 3, 6, 7, 8]]
        symrand = lambda s: random.uniform(-1, 1) * s
        symrand2d = lambda s: symrand(s) * RIGHT + symrand(s) * UP
        for it in range(15):
            fruit = random.choice("ABC")
            start = random.choice(monkey_angry_pos) + symrand2d(0.5)
            v0 = 30 + symrand(5)
            g = 50
            target = (explorer.get_center() + 2 * UP + symrand2d(1)) - start
            x, y = target[0], target[1]
            angle = np.arctan(
                (v0**2 - (v0**4 - g * (g * x**2 + 2 * y * v0**2)) ** 0.5)
                / (g * x)
            )
            parametric = lambda t: start + np.array(
                [
                    v0 * t * np.cos(angle),
                    v0 * t * np.sin(angle) - 0.5 * g * t**2,
                    0,
                ]
            )
            path = ParametricFunction(
                parametric,
                t_range=[0, 1],
            )
            # self.add(path, Dot(target + start), Dot(start))
            f = FRUITS[fruit].copy().move_to(-10 * LEFT)
            if it < 3:
                time = [0, 1.5, 2.5][it]
            else:
                time = 2 + 0.4 * it
            anims.append(
                Succession(
                    Wait(time), MoveAlongPath(f, path, rate_func=linear, run_time=2)
                )
            )

        background_above = (
            ImageMobject(f"img/background-above.png")
            .scale_to_fit_width(config.frame_width)
            .next_to(background, UP, buff=0)
        )
        self.add(background_above)
        self.play(
            *anims,
            Succession(
                Wait(2),
                AnimationGroup(
                    self.camera.frame.animate.align_to(background_above, UP),
                    run_time=10,
                ),
            ),
        )

        self.wait()

        # [oddálí se záběr, vidíme jen ostrov uprostřed oceánu]

        # I had to leave the island pretty quickly then. The rumor has it the monkeys are still out there, arguing. But now about which voting system is the best one…

        # [závěrečné poděkování patronům a some, možná midjourney bloopers? možná odkázat na roughgardenovy lecture notes?]


class Thanks(Scene):
    def construct(self):
        default()
        Tex.set_default(color=WHITE)
        background_above = (
            ImageMobject(f"img/background-above.png")
            .scale_to_fit_width(config.frame_width)
            .to_edge(UP, buff=0)
        )
        self.add(background_above)
        s = [
            Tex(
                r"Video by Richard Hladík, Filip Hlásek, Václav Rozhoň, and Václav Volhejn"
            ).scale(0.8),
            Tex(r"Inspired by a short story by Mirek Olšák").scale(0.8),
            Tex(
                "Big thanks to the organizers of SoME2, the amazing Manim Community, "
            ).scale(0.8),
            Tex("Jan Petr, Hanka Rozhoňová, ").scale(0.8),
            Tex("and our amazing Patrons: ").scale(0.8),
            Tex(r"sjbtrn and Tomáš Sláma").scale(1),
        ]
        texs = Group(*s).arrange_in_grid(cols=1, cell_alignment=LEFT)

        see_description = Tex(
            r"See video description for links \\ and some more related math."
        ).scale(1.5)

        Group(texs[3], texs[5]).shift(0.5 * RIGHT)
        see_description.move_to(ORIGIN).to_edge(DOWN, buff=1)

        cred = texs[:2]
        cred.move_to(3 * UP)

        thanks = texs[2:]
        thanks.move_to(2.3 * DOWN)

        self.play(FadeIn(texs))
        self.wait(2)
        self.play(FadeOut(texs))
        self.wait(0.5)
        self.play(FadeIn(see_description))
        self.wait(2)
        self.play(FadeOut(see_description))
        self.wait()
