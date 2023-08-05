import datetime
from decimal import Decimal
from typing import List, Union, Tuple

import toloka.client as toloka

from crowdom import (
    base,
    evaluation,
    classification,
    classification_loop,
    duration,
    feedback_loop,
    control,
    mapping,
    pool as pool_config,
    worker,
)
from crowdom.objects import Audio, Text
from . import lib


class TolokaClientStub(lib.TolokaClientCallRecorderStub):
    def __init__(self, assignments: List[toloka.Assignment]):
        self.assignments = assignments
        super(TolokaClientStub, self).__init__()

    # will be called during checks retrieval
    def get_assignments(
        self,
        status: Union[toloka.Assignment.Status, List[toloka.Assignment.Status]],
        pool_id: str,
    ) -> List[toloka.Assignment]:
        if not isinstance(status, list):
            status = [status]
        return [assignment for assignment in self.assignments if assignment.status in status]

    # called by internal classification loop, mock closed pool
    def get_pool(self, pool_id: str) -> toloka.Pool:
        pool = toloka.Pool()
        pool.is_closed = lambda: True
        return pool

    # # called by internal classification loop, return empty because not check overlaps will change
    def get_tasks(self, request: toloka.search_requests.TaskSearchRequest) -> List[toloka.Task]:
        return []


def test_give_bonuses_to_users():
    audios = [Audio(url=f'https://storage.net/{i}.wav') for i in range(6)]

    markup_assignments = [
        # accuracy = 0.75
        lib.create_markup_assignment(
            audio_text_pairs=[
                # OK
                (audios[2], Text(text='алло')),
                # OK
                (audios[5], Text(text='привет')),
                # OK
                (audios[3], Text(text='четыре шесть')),
                # BAD
                (audios[0], Text(text='нет не надо')),
                # UNKNOWN
                (audios[4], Text(text='леруа ?')),
            ],
            id='m1',
            status=toloka.Assignment.ACCEPTED,
            user_id='a',
        ),
        # accuracy = 0.5
        lib.create_markup_assignment(
            audio_text_pairs=[
                # BAD
                (audios[0], Text(text='нет не надо')),
                # OK
                (audios[4], Text(text='леруа мерлен')),
                # BAD
                (audios[3], Text(text='четырнадцать')),
                # OK
                (audios[1], Text(text='хорошо')),
                # UNKNOWN
                (audios[5], Text(text='?')),
            ],
            id='m2',
            status=toloka.Assignment.REJECTED,
            user_id='c',
        ),
    ]

    def generate_check_assignment(id: str, data: List[Tuple[str, str, bool]], user_id: str) -> toloka.Assignment:
        return toloka.Assignment(
            id=id,
            user_id=user_id,
            tasks=[
                lib.audio_transcript_check_mapping.to_task((Audio(url=url), Text(text=text))) for url, text, _ in data
            ],
            solutions=[
                lib.audio_transcript_check_mapping.to_solution((base.BinaryEvaluation(ok=ok),)) for _, _, ok in data
            ],
            status=toloka.Assignment.ACCEPTED,
        )

    check_assignments = [
        generate_check_assignment(
            'c1',
            [
                ('https://storage.net/0.wav', 'нет не надо', False),
                ('https://storage.net/1.wav', 'хорошо', True),
                ('https://storage.net/2.wav', 'алло', True),
                ('https://storage.net/3.wav', 'четыре шесть', False),
                ('https://storage.net/4.wav', 'леруа мерлен', True),
                ('https://storage.net/5.wav', 'првет', False),
            ],
            'b',
        ),
        generate_check_assignment(
            'c2',
            [
                ('https://storage.net/0.wav', 'нет не надо', False),
                ('https://storage.net/1.wav', '', False),
                ('https://storage.net/2.wav', 'алло', True),
                ('https://storage.net/3.wav', 'четырнадцать', False),
                ('https://storage.net/4.wav', 'леруа мерлен', True),
                ('https://storage.net/5.wav', 'привет', True),
            ],
            'a',
        ),
        generate_check_assignment(
            'c3',
            [
                ('https://storage.net/0.wav', 'нет спасибо не надо', True),
                ('https://storage.net/1.wav', 'хорошо', False),
                ('https://storage.net/3.wav', 'четырнадцать', False),
                ('https://storage.net/3.wav', 'четыре шесть', True),
                ('https://storage.net/4.wav', '? ?', False),
                ('https://storage.net/5.wav', 'привет', False),
            ],
            'd',
        ),
    ]

    stub = TolokaClientStub(check_assignments)

    fb_loop = feedback_loop.FeedbackLoop(
        pool_input_objects=[(audio,) for audio in audios],
        markup_task_mapping=mapping.TaskMapping(input_mapping=(lib.audio_mapping,), output_mapping=(lib.text_mapping,)),
        check_task_mapping=mapping.TaskMapping(
            input_mapping=(lib.audio_mapping, lib.text_mapping), output_mapping=(lib.binary_evaluation_mapping,)
        ),
        check_params=classification_loop.Params(
            control=feedback_loop.Control(rules=control.RuleBuilder().add_static_reward(threshold=0.5).build()),
            overlap=classification_loop.StaticOverlap(overlap=2),
            aggregation_algorithm=classification.AggregationAlgorithm.MAJORITY_VOTE,
            task_duration_function=None,  # noqa
        ),
        markup_params=feedback_loop.Params(
            control=control.Control(
                rules=control.RuleBuilder()
                .add_dynamic_reward(
                    min_bonus_amount_usd=0.02,
                    max_bonus_amount_usd=0.04,
                    min_accuracy_for_bonus=0.5,
                    bonus_granularity_num=3,
                )
                .build()
            ),
            assignment_check_sample=None,
            overlap=classification_loop.DynamicOverlap(min_overlap=1, max_overlap=None, confidence=0.5),
            task_duration_function=None,
        ),
        client=stub,  # noqa
        lang='RU',
    )

    fb_loop.check_loop.pool_cfg = pool_config.ClassificationConfig(
        project_id=None,
        private_name=None,
        reward_per_assignment=None,
        task_duration_hint=None,  # noqa
        real_tasks_count=6,
        control_tasks_count=0,
    )

    fb_loop.give_bonuses_to_users(check_pool_id='fake', markup_assignments=markup_assignments)

    assert stub.calls == [
        (
            'create_user_bonuses_async',
            (
                [
                    toloka.user_bonus.UserBonus(
                        user_id='a', assignment_id='m1', amount=Decimal(0.03), without_message=True
                    ),
                    toloka.user_bonus.UserBonus(
                        user_id='c', assignment_id='m2', amount=Decimal(0.02), without_message=True
                    ),
                ],
            ),
        ),
        (
            'wait_operation',
            (toloka.operations.UserBonusCreateBatchOperation(status=toloka.operations.Operation.Status.SUCCESS),),
        ),
    ]


def test_get_results():
    # check all verdicts (BAD, UNKNOWN, OK)
    # check solutions sorting
    # - case then both solutions verdict is UNKNOWN and we prefer solution from better assignment

    assignment_id_to_accuracy_and_precision_recall = {
        '0': (1 / 3, 3 / 4),
        '1': (2 / 3, 3 / 4),
        '2': (1 / 2, 2 / 4),
        '3': (1 / 1, 1 / 2),
    }

    def generate_task_result(
        solutions: List[Tuple[str, feedback_loop.SolutionVerdict, str, str]],
    ) -> List[feedback_loop.Solution]:
        return [
            feedback_loop.Solution(
                solution=(Text(text=text),),
                verdict=verdict,
                worker=worker.Human(toloka.Assignment(user_id=user_id, id=assignment_id)),
                evaluation=evaluation.SolutionEvaluation(
                    ok=verdict == feedback_loop.SolutionVerdict.OK,
                    confidence=None,
                    worker_labels=[],  # noqa
                )
                if verdict != feedback_loop.SolutionVerdict.UNKNOWN
                else None,
                assignment_accuracy=assignment_id_to_accuracy_and_precision_recall[assignment_id][0],
                assignment_evaluation_recall=assignment_id_to_accuracy_and_precision_recall[assignment_id][1],
            )
            for text, verdict, assignment_id, user_id in solutions
        ]

    assert feedback_loop.get_results(
        pool_input_objects=[
            # test results order corresponds to pool input objects order
            (Audio(url=f'https://storage.net/{i}.wav'),)
            for i in range(6)
        ],
        markup_assignments=[
            lib.create_markup_assignment(
                audio_text_pairs=[
                    # UNKNOWN
                    (Audio(url='https://storage.net/2.wav'), Text(text='? до свидания')),
                    # BAD
                    (Audio(url='https://storage.net/5.wav'), Text(text='')),
                    # OK
                    (Audio(url='https://storage.net/0.wav'), Text(text='але')),
                    # BAD
                    (Audio(url='https://storage.net/1.wav'), Text(text='позови аператора')),
                ],
                id='0',
                status=toloka.Assignment.REJECTED,
                user_id='c',
            ),
            lib.create_markup_assignment(
                audio_text_pairs=[
                    # BAD
                    (Audio(url='https://storage.net/1.wav'), Text(text='позови аператора')),
                    # UNKNOWN
                    (Audio(url='https://storage.net/2.wav'), Text(text='да до свидания')),
                    # OK
                    (Audio(url='https://storage.net/3.wav'), Text(text='леруа мерлен')),
                    # OK
                    (Audio(url='https://storage.net/4.wav'), Text(text='нет не надо')),
                ],
                id='1',
                status=toloka.Assignment.REJECTED,
                user_id='a',
            ),
            lib.create_markup_assignment(
                audio_text_pairs=[
                    # UNKNOWN
                    (Audio(url='https://storage.net/3.wav'), Text(text='? мерлен')),
                    # BAD
                    (Audio(url='https://storage.net/2.wav'), Text(text='? досвидания')),
                    # OK
                    (Audio(url='https://storage.net/5.wav'), Text(text='нет')),
                    # UNKNOWN
                    (Audio(url='https://storage.net/1.wav'), Text(text='позовите оператора')),
                ],
                id='2',
                status=toloka.Assignment.REJECTED,
                user_id='b',
            ),
            lib.create_markup_assignment(
                audio_text_pairs=[
                    # OK
                    (Audio(url='https://storage.net/2.wav'), Text(text='да хорошо до свидания')),
                    # UNKNOWN
                    (Audio(url='https://storage.net/1.wav'), Text(text='угу позовите оператора')),
                ],
                id='3',
                status=toloka.Assignment.ACCEPTED,
                user_id='e',
            ),
        ],
        solution_id_to_evaluation=lib.generate_evaluations(
            [
                ('https://storage.net/5.wav', '', False),
                ('https://storage.net/0.wav', 'але', True),
                ('https://storage.net/1.wav', 'позови аператора', False),
                ('https://storage.net/3.wav', 'леруа мерлен', True),
                ('https://storage.net/4.wav', 'нет не надо', True),
                ('https://storage.net/2.wav', '? досвидания', False),
                ('https://storage.net/5.wav', 'нет', True),
                ('https://storage.net/2.wav', 'да хорошо до свидания', True),
            ]
        ),
        markup_task_mapping=lib.audio_transcript_mapping,
        check_task_mapping=lib.audio_transcript_check_mapping,
    ) == [
        generate_task_result(solutions=[('але', feedback_loop.SolutionVerdict.OK, '0', 'c')]),
        generate_task_result(
            solutions=[
                ('угу позовите оператора', feedback_loop.SolutionVerdict.UNKNOWN, '3', 'e'),
                ('позовите оператора', feedback_loop.SolutionVerdict.UNKNOWN, '2', 'b'),
                ('позови аператора', feedback_loop.SolutionVerdict.BAD, '1', 'a'),
                ('позови аператора', feedback_loop.SolutionVerdict.BAD, '0', 'c'),
            ],
        ),
        generate_task_result(
            solutions=[
                ('да хорошо до свидания', feedback_loop.SolutionVerdict.OK, '3', 'e'),
                ('да до свидания', feedback_loop.SolutionVerdict.UNKNOWN, '1', 'a'),
                ('? до свидания', feedback_loop.SolutionVerdict.UNKNOWN, '0', 'c'),
                ('? досвидания', feedback_loop.SolutionVerdict.BAD, '2', 'b'),
            ],
        ),
        generate_task_result(
            solutions=[
                ('леруа мерлен', feedback_loop.SolutionVerdict.OK, '1', 'a'),
                ('? мерлен', feedback_loop.SolutionVerdict.UNKNOWN, '2', 'b'),
            ],
        ),
        generate_task_result(
            solutions=[('нет не надо', feedback_loop.SolutionVerdict.OK, '1', 'a')],
        ),
        generate_task_result(
            solutions=[
                ('нет', feedback_loop.SolutionVerdict.OK, '2', 'b'),
                ('', feedback_loop.SolutionVerdict.BAD, '0', 'c'),
            ],
        ),
    ]


def test_speed_control():
    audios = [Audio(url=f'https://storage.net/{i}.wav') for i in range(6)]
    markup_assignment_solutions = [
        lib.create_markup_assignment(
            audio_text_pairs=[
                (audios[0], Text(text='алло')),
                (audios[1], Text(text='привет')),
            ],
            id='m1',
            user_id='a',
            duration=datetime.timedelta(seconds=40),
        ),
        lib.create_markup_assignment(
            audio_text_pairs=[
                (audios[2], Text(text='нет')),
                (audios[3], Text(text='да спасибо')),
            ],
            id='m2',
            user_id='b',
            duration=datetime.timedelta(seconds=10),
        ),
        lib.create_markup_assignment(
            audio_text_pairs=[
                (audios[4], Text(text='нет')),
                (audios[5], Text(text='да спасибо')),
            ],
            id='m3',
            user_id='c',
            duration=datetime.timedelta(seconds=3),
        ),
    ]
    stub = TolokaClientStub([assignment for assignment, _ in markup_assignment_solutions])

    fb_loop = feedback_loop.FeedbackLoop(
        pool_input_objects=[(audio,) for audio in audios],
        markup_task_mapping=mapping.TaskMapping(input_mapping=(lib.audio_mapping,), output_mapping=(lib.text_mapping,)),
        check_task_mapping=mapping.TaskMapping(
            input_mapping=(lib.audio_mapping, lib.text_mapping), output_mapping=(lib.binary_evaluation_mapping,)
        ),
        check_params=classification_loop.Params(
            control=None,  # noqa
            overlap=None,  # noqa
            aggregation_algorithm=None,
            task_duration_function=None,  # noqa
        ),
        markup_params=feedback_loop.Params(
            control=control.Control(
                rules=control.RuleBuilder().add_speed_control(ratio_rand=0.1, ratio_poor=0.3).rules
            ),
            assignment_check_sample=None,
            overlap=None,  # noqa
            task_duration_function=duration.get_const_task_duration_function(datetime.timedelta(seconds=20)),
        ),
        client=stub,  # noqa
        lang='RU',
    )
    assert ([markup_assignment_solutions[i] for i in [0, 1]], [markup_assignment_solutions[-1]]) == fb_loop.get_markups(
        markup_pool_id='fake', check_pool_id=None  # noqa
    )
    assert [
        (
            'set_user_restriction',
            (
                toloka.user_restriction.PoolUserRestriction(
                    user_id='b',
                    private_comment='Fast submits, 0.1 < time <= 0.3',
                    will_expire=datetime.datetime(2020, 11, 5, 8, 0, 10),
                ),
            ),
        ),
        (
            'set_user_restriction',
            (
                toloka.user_restriction.PoolUserRestriction(
                    user_id='c',
                    private_comment='Fast submits, <= 0.1',
                    will_expire=datetime.datetime(2020, 11, 6, 0, 0, 3),
                ),
            ),
        ),
        (
            'patch_assignment',
            (
                'm3',
                toloka.AssignmentPatch(
                    public_comment='Мало правильных решений', status=toloka.Assignment.Status.REJECTED
                ),
            ),
        ),
    ] == stub.calls
