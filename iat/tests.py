"""
Implicit Association Test (IAT) experiment -- automated tests.

November 2019
Markus Konrad <markus.konrad@wzb.eu>
"""

import random
from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants, Trial, BLOCKS, STIMULI

avail_response_keys = [k for k, _ in Constants.capture_keycodes.values()]


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield pages.Intro

        block_def = BLOCKS[self.round_number - 1]

        # check existing Trial objects in DB
        trials_pre = Trial.objects.filter(player=self.player, block=self.round_number).order_by('trial')
        n_trials_pre = len(trials_pre)
        assert n_trials_pre == block_def['n']

        known_stimuli = set()
        for i, t in enumerate(trials_pre):
            assert t.block == self.round_number
            assert t.trial == i+1
            assert t.player == self.player

            # must be set:
            assert t.stimulus_class in STIMULI
            assert t.stimulus_level in STIMULI[t.stimulus_class]
            assert t.stimulus in STIMULI[t.stimulus_class][t.stimulus_level]
            assert t.stimulus not in known_stimuli   # show each stimulus only once per block
            known_stimuli.add(t.stimulus)

            # must be empty before trial is run:
            assert t.response_key is None
            assert t.response_time_ms is None
            assert t.response_correct is None

        # prepare submit with random inputs for each trial
        trial_ids = [t.pk for t in trials_pre]
        response_keys = [random.choice(avail_response_keys) for _ in range(n_trials_pre)]
        response_times = [random.randint(100, 1100) for _ in range(n_trials_pre)]
        responses_correct = [random.randint(0, 1) for _ in range(n_trials_pre)]

        # submit trials
        yield (pages.IATPage, {
            'trial_ids': ','.join(map(str, trial_ids)),
            'responses': ','.join(response_keys),
            'response_times': ','.join(map(str, response_times)),
            'responses_correct': ','.join(map(str, responses_correct)),
        })

        # check stored Trial objects after submission
        trials_post = Trial.objects.filter(player=self.player, block=self.round_number).order_by('trial')
        n_trials_post = len(trials_post)
        assert n_trials_post == n_trials_pre

        for i, (t_pre, t_post) in enumerate(zip(trials_pre, trials_post)):
            assert t_pre.pk == t_post.pk == trial_ids[i]
            assert t_pre.block == t_post.block == self.round_number
            assert t_pre.trial == t_post.trial == i+1
            assert t_post.player == self.player

            # must be unchanged
            assert t_pre.stimulus_class == t_post.stimulus_class
            assert t_pre.stimulus_level == t_post.stimulus_level
            assert t_pre.stimulus == t_post.stimulus

            # must be set according to submitted values
            assert t_post.response_key == response_keys[i]
            assert t_post.response_time_ms == response_times[i]
            assert t_post.response_correct == bool(responses_correct[i])

        if self.round_number == Constants.num_rounds:
            yield pages.Outro

