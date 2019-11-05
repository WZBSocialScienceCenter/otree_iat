"""
Implicit Association Test (IAT) experiment -- pages.

November 2019
Markus Konrad <markus.konrad@wzb.eu>
"""


from collections import defaultdict

from django.conf import settings

from ._builtin import Page
from .models import STIMULI, STIMULI_LABELS, BLOCKS, Constants, Trial


class Intro(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'stimuli': [
                {
                    'label': STIMULI_LABELS[(c, l)],
                    'values': ', '.join(STIMULI[c][l])
                }
                for c in ('attributes', 'concepts')
                for l in STIMULI[c].keys()]
        }


class IATPage(Page):
    """
    Page for running IAT trials for a single block (round).
    """

    def vars_for_template(self):
        block_def = BLOCKS[self.round_number - 1]
        block_def['notice'] = block_def.get('notice', '')

        instructions = []
        stimulus_level_sides = defaultdict(dict)
        for side in ('left', 'right'):
            side_def = block_def[side]
            instructions.append({
                'classes': [{'class': cls, 'label': STIMULI_LABELS[(cls, lvl)]} for cls, lvl in side_def],
                'side': side,
                'key': Constants.capture_keycodes[side][1]
            })

            for cls, lvl in side_def:
                stimulus_level_sides[cls][lvl] = side

        return {
            'debug': settings.APPS_DEBUG,
            'block_def': block_def,
            'instructions': instructions,
            'keycodes_sides': {kcode: side for side, (kcode, _) in Constants.capture_keycodes.items()},
            'sides_keycodes': {side: kcode for side, (kcode, _) in Constants.capture_keycodes.items()},
            'stimulus_level_sides': stimulus_level_sides,
            'trials': Trial.objects.filter(player=self.player, block=self.round_number).order_by('trial')
        }

    def before_next_page(self):
        """
        Handle submitted trial responses.
        """

        # trial IDs, response keys and response times are submitted as aligned, comma separated values
        # split them
        trial_ids = self.form.data['trial_ids'].split(',')
        responses = self.form.data['responses'].split(',')
        response_times = self.form.data['response_times'].split(',')
        responses_correct = self.form.data['responses_correct'].split(',')

        if not trial_ids:
            raise ValueError('no input data for `trial_ids`')

        if not responses:
            raise ValueError('no input data for `responses`')

        if not response_times:
            raise ValueError('no input data for `response_times`')

        if not responses_correct:
            raise ValueError('no input data for `responses_correct`')

        if len(trial_ids) != len(responses) or len(responses) != len(response_times) != len(responses_correct):
            raise ValueError('input data for `trial_ids` (%d elements), `responses` (%d elements), '
                             '`response_times` (%d elements) and `responses_correct` (%d elements) are of '
                             'different length'
                             % (len(trial_ids), len(responses), len(response_times), len(responses_correct)))

        print('number of trials submitted from player %d: %d' % (self.player.pk, len(trial_ids)))

        # iterate through the aligned responses
        for trial_id, resp_key, resp_time_ms, resp_correct in zip(trial_ids, responses, response_times, responses_correct):
            # convert strings to integers
            trial_id = int(trial_id)
            resp_time_ms = int(resp_time_ms)
            resp_correct = bool(int(resp_correct))

            # fetch the Trial object
            trial = Trial.objects.get(pk=trial_id, player=self.player)

            # store the responses
            trial.response_key = resp_key
            trial.response_time_ms = resp_time_ms
            trial.response_correct = resp_correct

            print('> saving trial %d in block %d (trial ID %d): key %s, time %d, correct %d'
                  % (trial.trial, trial.block, trial.pk, trial.response_key, trial.response_time_ms,
                     trial.response_correct))

            trial.save()


class Outro(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Intro,
    IATPage,
    Outro
]
