# vim: set fileencoding=utf-8
import copy
import random
import struct
from typing import Optional, Dict, Any, List, Tuple

from ..course import IIDXCourse
from ..base import IIDXBase

from core.common import ValidatedDict, VersionConstants, Time, ID, intish
from core.data import Data, UserID, Score
from core.protocol import Node


class IIDXBistrover(IIDXCourse, IIDXBase):
    name = 'Beatmania IIDX BISTROVER'
    version = VersionConstants.IIDX_BISTROVER

    GAME_CLTYPE_SINGLE = 0
    GAME_CLTYPE_DOUBLE = 1

    DAN_STAGES = 4

    GAME_CLEAR_STATUS_NO_PLAY = 0
    GAME_CLEAR_STATUS_FAILED = 1
    GAME_CLEAR_STATUS_ASSIST_CLEAR = 2
    GAME_CLEAR_STATUS_EASY_CLEAR = 3
    GAME_CLEAR_STATUS_CLEAR = 4
    GAME_CLEAR_STATUS_HARD_CLEAR = 5
    GAME_CLEAR_STATUS_EX_HARD_CLEAR = 6
    GAME_CLEAR_STATUS_FULL_COMBO = 7

    GAME_GHOST_TYPE_RIVAL = 1
    GAME_GHOST_TYPE_GLOBAL_TOP = 2
    GAME_GHOST_TYPE_GLOBAL_AVERAGE = 3
    GAME_GHOST_TYPE_LOCAL_TOP = 4
    GAME_GHOST_TYPE_LOCAL_AVERAGE = 5
    GAME_GHOST_TYPE_DAN_TOP = 6
    GAME_GHOST_TYPE_DAN_AVERAGE = 7
    GAME_GHOST_TYPE_RIVAL_TOP = 8
    GAME_GHOST_TYPE_RIVAL_AVERAGE = 9

    GAME_GHOST_LENGTH = 64

    GAME_SP_DAN_RANK_7_KYU = 0
    GAME_SP_DAN_RANK_6_KYU = 1
    GAME_SP_DAN_RANK_5_KYU = 2
    GAME_SP_DAN_RANK_4_KYU = 3
    GAME_SP_DAN_RANK_3_KYU = 4
    GAME_SP_DAN_RANK_2_KYU = 5
    GAME_SP_DAN_RANK_1_KYU = 6
    GAME_SP_DAN_RANK_1_DAN = 7
    GAME_SP_DAN_RANK_2_DAN = 8
    GAME_SP_DAN_RANK_3_DAN = 9
    GAME_SP_DAN_RANK_4_DAN = 10
    GAME_SP_DAN_RANK_5_DAN = 11
    GAME_SP_DAN_RANK_6_DAN = 12
    GAME_SP_DAN_RANK_7_DAN = 13
    GAME_SP_DAN_RANK_8_DAN = 14
    GAME_SP_DAN_RANK_9_DAN = 15
    GAME_SP_DAN_RANK_10_DAN = 16
    GAME_SP_DAN_RANK_CHUDEN = 17
    GAME_SP_DAN_RANK_KAIDEN = 18

    GAME_DP_DAN_RANK_7_KYU = 0
    GAME_DP_DAN_RANK_6_KYU = 1
    GAME_DP_DAN_RANK_5_KYU = 2
    GAME_DP_DAN_RANK_4_KYU = 3
    GAME_DP_DAN_RANK_3_KYU = 4
    GAME_DP_DAN_RANK_2_KYU = 5
    GAME_DP_DAN_RANK_1_KYU = 6
    GAME_DP_DAN_RANK_1_DAN = 7
    GAME_DP_DAN_RANK_2_DAN = 8
    GAME_DP_DAN_RANK_3_DAN = 9
    GAME_DP_DAN_RANK_4_DAN = 10
    GAME_DP_DAN_RANK_5_DAN = 11
    GAME_DP_DAN_RANK_6_DAN = 12
    GAME_DP_DAN_RANK_7_DAN = 13
    GAME_DP_DAN_RANK_8_DAN = 14
    GAME_DP_DAN_RANK_9_DAN = 15
    GAME_DP_DAN_RANK_10_DAN = 16
    GAME_DP_DAN_RANK_CHUDEN = 17
    GAME_DP_DAN_RANK_KAIDEN = 18

    GAME_CHART_TYPE_B7 = 0
    GAME_CHART_TYPE_N7 = 1
    GAME_CHART_TYPE_H7 = 2
    GAME_CHART_TYPE_A7 = 3
    GAME_CHART_TYPE_L7 = 4
    GAME_CHART_TYPE_B14 = 5  # THere are no B14 charts in the game but this would be the id if there were
    GAME_CHART_TYPE_N14 = 6
    GAME_CHART_TYPE_H14 = 7
    GAME_CHART_TYPE_A14 = 8
    GAME_CHART_TYPE_L14 = 9

    FAVORITE_LIST_LENGTH = 20

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXBistrover(self.data, self.config, self.model)

    def game_to_db_chart(self, db_chart: int) -> int:
        return {
            self.GAME_CHART_TYPE_B7: self.CHART_TYPE_B7,
            self.GAME_CHART_TYPE_N7: self.CHART_TYPE_N7,
            self.GAME_CHART_TYPE_H7: self.CHART_TYPE_H7,
            self.GAME_CHART_TYPE_A7: self.CHART_TYPE_A7,
            self.GAME_CHART_TYPE_L7: self.CHART_TYPE_L7,
            self.GAME_CHART_TYPE_B14: self.CHART_TYPE_B14,
            self.GAME_CHART_TYPE_N14: self.CHART_TYPE_N14,
            self.GAME_CHART_TYPE_H14: self.CHART_TYPE_H14,
            self.GAME_CHART_TYPE_A14: self.CHART_TYPE_A14,
            self.GAME_CHART_TYPE_L14: self.CHART_TYPE_L14,
        }[db_chart]

    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """
        Return all of our front-end modifiably settings.
        """
        return {
            'bools': [
                {
                    'name': 'Global Shop Ranking',
                    'tip': 'Return network-wide ranking instead of shop ranking on results screen.',
                    'category': 'game_config',
                    'setting': 'global_shop_ranking',
                }
            ]
        }

    def db_to_game_status(self, db_status: int) -> int:
        return {
            self.CLEAR_STATUS_NO_PLAY: self.GAME_CLEAR_STATUS_NO_PLAY,
            self.CLEAR_STATUS_FAILED: self.GAME_CLEAR_STATUS_FAILED,
            self.CLEAR_STATUS_ASSIST_CLEAR: self.GAME_CLEAR_STATUS_ASSIST_CLEAR,
            self.CLEAR_STATUS_EASY_CLEAR: self.GAME_CLEAR_STATUS_EASY_CLEAR,
            self.CLEAR_STATUS_CLEAR: self.GAME_CLEAR_STATUS_CLEAR,
            self.CLEAR_STATUS_HARD_CLEAR: self.GAME_CLEAR_STATUS_HARD_CLEAR,
            self.CLEAR_STATUS_EX_HARD_CLEAR: self.GAME_CLEAR_STATUS_EX_HARD_CLEAR,
            self.CLEAR_STATUS_FULL_COMBO: self.GAME_CLEAR_STATUS_FULL_COMBO,
        }[db_status]

    def game_to_db_status(self, game_status: int) -> int:
        return {
            self.GAME_CLEAR_STATUS_NO_PLAY: self.CLEAR_STATUS_NO_PLAY,
            self.GAME_CLEAR_STATUS_FAILED: self.CLEAR_STATUS_FAILED,
            self.GAME_CLEAR_STATUS_ASSIST_CLEAR: self.CLEAR_STATUS_ASSIST_CLEAR,
            self.GAME_CLEAR_STATUS_EASY_CLEAR: self.CLEAR_STATUS_EASY_CLEAR,
            self.GAME_CLEAR_STATUS_CLEAR: self.CLEAR_STATUS_CLEAR,
            self.GAME_CLEAR_STATUS_HARD_CLEAR: self.CLEAR_STATUS_HARD_CLEAR,
            self.GAME_CLEAR_STATUS_EX_HARD_CLEAR: self.CLEAR_STATUS_EX_HARD_CLEAR,
            self.GAME_CLEAR_STATUS_FULL_COMBO: self.CLEAR_STATUS_FULL_COMBO,
        }[game_status]

    def db_to_game_rank(self, db_dan: int, cltype: int) -> int:
        # Special case for no DAN rank
        if db_dan == -1:
            return -1

        if cltype == self.GAME_CLTYPE_SINGLE:
            return {
                self.DAN_RANK_7_KYU: self.GAME_SP_DAN_RANK_7_KYU,
                self.DAN_RANK_6_KYU: self.GAME_SP_DAN_RANK_6_KYU,
                self.DAN_RANK_5_KYU: self.GAME_SP_DAN_RANK_5_KYU,
                self.DAN_RANK_4_KYU: self.GAME_SP_DAN_RANK_4_KYU,
                self.DAN_RANK_3_KYU: self.GAME_SP_DAN_RANK_3_KYU,
                self.DAN_RANK_2_KYU: self.GAME_SP_DAN_RANK_2_KYU,
                self.DAN_RANK_1_KYU: self.GAME_SP_DAN_RANK_1_KYU,
                self.DAN_RANK_1_DAN: self.GAME_SP_DAN_RANK_1_DAN,
                self.DAN_RANK_2_DAN: self.GAME_SP_DAN_RANK_2_DAN,
                self.DAN_RANK_3_DAN: self.GAME_SP_DAN_RANK_3_DAN,
                self.DAN_RANK_4_DAN: self.GAME_SP_DAN_RANK_4_DAN,
                self.DAN_RANK_5_DAN: self.GAME_SP_DAN_RANK_5_DAN,
                self.DAN_RANK_6_DAN: self.GAME_SP_DAN_RANK_6_DAN,
                self.DAN_RANK_7_DAN: self.GAME_SP_DAN_RANK_7_DAN,
                self.DAN_RANK_8_DAN: self.GAME_SP_DAN_RANK_8_DAN,
                self.DAN_RANK_9_DAN: self.GAME_SP_DAN_RANK_9_DAN,
                self.DAN_RANK_10_DAN: self.GAME_SP_DAN_RANK_10_DAN,
                self.DAN_RANK_CHUDEN: self.GAME_SP_DAN_RANK_CHUDEN,
                self.DAN_RANK_KAIDEN: self.GAME_SP_DAN_RANK_KAIDEN,
            }[db_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.DAN_RANK_7_KYU: self.GAME_DP_DAN_RANK_7_KYU,
                self.DAN_RANK_6_KYU: self.GAME_DP_DAN_RANK_6_KYU,
                self.DAN_RANK_5_KYU: self.GAME_DP_DAN_RANK_5_KYU,
                self.DAN_RANK_4_KYU: self.GAME_DP_DAN_RANK_4_KYU,
                self.DAN_RANK_3_KYU: self.GAME_DP_DAN_RANK_3_KYU,
                self.DAN_RANK_2_KYU: self.GAME_DP_DAN_RANK_2_KYU,
                self.DAN_RANK_1_KYU: self.GAME_DP_DAN_RANK_1_KYU,
                self.DAN_RANK_1_DAN: self.GAME_DP_DAN_RANK_1_DAN,
                self.DAN_RANK_2_DAN: self.GAME_DP_DAN_RANK_2_DAN,
                self.DAN_RANK_3_DAN: self.GAME_DP_DAN_RANK_3_DAN,
                self.DAN_RANK_4_DAN: self.GAME_DP_DAN_RANK_4_DAN,
                self.DAN_RANK_5_DAN: self.GAME_DP_DAN_RANK_5_DAN,
                self.DAN_RANK_6_DAN: self.GAME_DP_DAN_RANK_6_DAN,
                self.DAN_RANK_7_DAN: self.GAME_DP_DAN_RANK_7_DAN,
                self.DAN_RANK_8_DAN: self.GAME_DP_DAN_RANK_8_DAN,
                self.DAN_RANK_9_DAN: self.GAME_DP_DAN_RANK_9_DAN,
                self.DAN_RANK_10_DAN: self.GAME_DP_DAN_RANK_10_DAN,
                self.DAN_RANK_CHUDEN: self.GAME_DP_DAN_RANK_CHUDEN,
                self.DAN_RANK_KAIDEN: self.GAME_DP_DAN_RANK_KAIDEN,
            }[db_dan]
        else:
            raise Exception('Invalid cltype!')

    def game_to_db_rank(self, game_dan: int, cltype: int) -> int:
        # Special case for no DAN rank
        if game_dan == -1:
            return -1

        if cltype == self.GAME_CLTYPE_SINGLE:
            return {
                self.GAME_SP_DAN_RANK_7_KYU: self.DAN_RANK_7_KYU,
                self.GAME_SP_DAN_RANK_6_KYU: self.DAN_RANK_6_KYU,
                self.GAME_SP_DAN_RANK_5_KYU: self.DAN_RANK_5_KYU,
                self.GAME_SP_DAN_RANK_4_KYU: self.DAN_RANK_4_KYU,
                self.GAME_SP_DAN_RANK_3_KYU: self.DAN_RANK_3_KYU,
                self.GAME_SP_DAN_RANK_2_KYU: self.DAN_RANK_2_KYU,
                self.GAME_SP_DAN_RANK_1_KYU: self.DAN_RANK_1_KYU,
                self.GAME_SP_DAN_RANK_1_DAN: self.DAN_RANK_1_DAN,
                self.GAME_SP_DAN_RANK_2_DAN: self.DAN_RANK_2_DAN,
                self.GAME_SP_DAN_RANK_3_DAN: self.DAN_RANK_3_DAN,
                self.GAME_SP_DAN_RANK_4_DAN: self.DAN_RANK_4_DAN,
                self.GAME_SP_DAN_RANK_5_DAN: self.DAN_RANK_5_DAN,
                self.GAME_SP_DAN_RANK_6_DAN: self.DAN_RANK_6_DAN,
                self.GAME_SP_DAN_RANK_7_DAN: self.DAN_RANK_7_DAN,
                self.GAME_SP_DAN_RANK_8_DAN: self.DAN_RANK_8_DAN,
                self.GAME_SP_DAN_RANK_9_DAN: self.DAN_RANK_9_DAN,
                self.GAME_SP_DAN_RANK_10_DAN: self.DAN_RANK_10_DAN,
                self.GAME_SP_DAN_RANK_CHUDEN: self.DAN_RANK_CHUDEN,
                self.GAME_SP_DAN_RANK_KAIDEN: self.DAN_RANK_KAIDEN,
            }[game_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.GAME_DP_DAN_RANK_7_KYU: self.DAN_RANK_7_KYU,
                self.GAME_DP_DAN_RANK_6_KYU: self.DAN_RANK_6_KYU,
                self.GAME_DP_DAN_RANK_5_KYU: self.DAN_RANK_5_KYU,
                self.GAME_DP_DAN_RANK_4_KYU: self.DAN_RANK_4_KYU,
                self.GAME_DP_DAN_RANK_3_KYU: self.DAN_RANK_3_KYU,
                self.GAME_DP_DAN_RANK_2_KYU: self.DAN_RANK_2_KYU,
                self.GAME_DP_DAN_RANK_1_KYU: self.DAN_RANK_1_KYU,
                self.GAME_DP_DAN_RANK_1_DAN: self.DAN_RANK_1_DAN,
                self.GAME_DP_DAN_RANK_2_DAN: self.DAN_RANK_2_DAN,
                self.GAME_DP_DAN_RANK_3_DAN: self.DAN_RANK_3_DAN,
                self.GAME_DP_DAN_RANK_4_DAN: self.DAN_RANK_4_DAN,
                self.GAME_DP_DAN_RANK_5_DAN: self.DAN_RANK_5_DAN,
                self.GAME_DP_DAN_RANK_6_DAN: self.DAN_RANK_6_DAN,
                self.GAME_DP_DAN_RANK_7_DAN: self.DAN_RANK_7_DAN,
                self.GAME_DP_DAN_RANK_8_DAN: self.DAN_RANK_8_DAN,
                self.GAME_DP_DAN_RANK_9_DAN: self.DAN_RANK_9_DAN,
                self.GAME_DP_DAN_RANK_10_DAN: self.DAN_RANK_10_DAN,
                self.GAME_DP_DAN_RANK_CHUDEN: self.DAN_RANK_CHUDEN,
                self.GAME_DP_DAN_RANK_KAIDEN: self.DAN_RANK_KAIDEN,
            }[game_dan]
        else:
            raise Exception('Invalid cltype!')

    # Override base method from iidx 27 and on
    def make_score_struct(self, scores: List[Score], cltype: int, index: int) -> List[List[int]]:
        scorestruct: Dict[int, List[int]] = {}

        for score in scores:
            musicid = score.id
            chart = score.chart

            # Filter to only singles/doubles charts
            if cltype == self.CLEAR_TYPE_SINGLE:
                if chart not in [
                    self.CHART_TYPE_B7,
                    self.CHART_TYPE_N7,
                    self.CHART_TYPE_H7,
                    self.CHART_TYPE_A7,
                    self.CHART_TYPE_L7,
                ]:
                    continue
                chartindex = {
                    self.CHART_TYPE_B7: 0,
                    self.CHART_TYPE_N7: 1,
                    self.CHART_TYPE_H7: 2,
                    self.CHART_TYPE_A7: 3,
                    self.CHART_TYPE_L7: 4,
                }[chart]
            if cltype == self.CLEAR_TYPE_DOUBLE:
                if chart not in [
                    self.CHART_TYPE_B14,
                    self.CHART_TYPE_N14,
                    self.CHART_TYPE_H14,
                    self.CHART_TYPE_A14,
                    self.CHART_TYPE_L14,
                ]:
                    continue
                chartindex = {
                    self.CHART_TYPE_B14: 0,
                    self.CHART_TYPE_N14: 1,
                    self.CHART_TYPE_H14: 2,
                    self.CHART_TYPE_A14: 3,
                    self.CHART_TYPE_L14: 4,
                }[chart]

            if musicid not in scorestruct:
                scorestruct[musicid] = [
                    index,  # -1 is our scores, positive is rival index
                    musicid,  # Music ID!
                    0,  # Beginner status,
                    0,  # Normal status,
                    0,  # Hyper status,
                    0,  # Another status,
                    0,  # Leggendaria status,
                    0,  # EX score beginner,
                    0,  # EX score normal,
                    0,  # EX score hyper,
                    0,  # EX score another,
                    0,  # EX score leggendaria
                    -1,  # Miss count beginnner
                    -1,  # Miss count normal,
                    -1,  # Miss count hyper,
                    -1,  # Miss count another,
                    -1,  # Miss count leggendaria,
                ]

            scorestruct[musicid][chartindex + 2] = self.db_to_game_status(score.data.get_int('clear_status'))
            scorestruct[musicid][chartindex + 7] = score.points
            scorestruct[musicid][chartindex + 12] = score.data.get_int('miss_count', -1)

        return [scorestruct[s] for s in scorestruct]

    async def handle_IIDX28shop_getname_request(self, request: Node) -> Node:
        machine = await self.data.local.machine.get_machine(self.config['machine']['pcbid'])
        if machine is not None:
            machine_name = machine.name
            close = machine.data.get_bool('close')
            hour = machine.data.get_int('hour')
            minute = machine.data.get_int('minute')
        else:
            machine_name = ''
            close = False
            hour = 0
            minute = 0

        root = Node.void('IIDX28shop')
        root.set_attribute('opname', machine_name)
        root.set_attribute('pid', '51')
        root.set_attribute('cls_opt', '1' if close else '0')
        root.set_attribute('hr', str(hour))
        root.set_attribute('mi', str(minute))
        return root

    async def handle_IIDX28shop_savename_request(self, request: Node) -> Node:
        await self.update_machine_name(request.attribute('opname'))

        shop_close = intish(request.attribute('cls_opt')) or 0
        minutes = intish(request.attribute('mnt')) or 0
        hours = intish(request.attribute('hr')) or 0

        await self.update_machine_data({
            'close': shop_close != 0,
            'minutes': minutes,
            'hours': hours,
        })

        return Node.void('IIDX28shop')

    async def handle_IIDX28shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void('IIDX28shop')

    async def handle_IIDX28shop_sendescapepackageinfo_request(self, request: Node) -> Node:
        root = Node.void('IIDX28shop')
        root.set_attribute('expire', str((Time.now() + 86400 * 365) * 1000))
        return root

    async def handle_IIDX28shop_getconvention_request(self, request: Node) -> Node:
        root = Node.void('IIDX28shop')
        machine = await self.data.local.machine.get_machine(self.config['machine']['pcbid'])
        if machine.arcade is not None:
            course = await self.data.local.machine.get_settings(machine.arcade, self.game, self.music_version, 'shop_course')
        else:
            course = None

        if course is None:
            course = ValidatedDict()

        root.set_attribute('music_0', str(course.get_int('music_0', 20032)))
        root.set_attribute('music_1', str(course.get_int('music_1', 20009)))
        root.set_attribute('music_2', str(course.get_int('music_2', 20015)))
        root.set_attribute('music_3', str(course.get_int('music_3', 20064)))
        root.add_child(Node.bool('valid', course.get_bool('valid')))
        return root

    async def handle_IIDX28shop_setconvention_request(self, request: Node) -> Node:
        machine = await self.data.local.machine.get_machine(self.config['machine']['pcbid'])
        if machine.arcade is not None:
            course = ValidatedDict()
            course.replace_int('music_0', request.child_value('music_0'))
            course.replace_int('music_1', request.child_value('music_1'))
            course.replace_int('music_2', request.child_value('music_2'))
            course.replace_int('music_3', request.child_value('music_3'))
            course.replace_bool('valid', request.child_value('valid'))
            await self.data.local.machine.put_settings(machine.arcade, self.game, self.music_version, 'shop_course', course)

        return Node.void('IIDX28shop')

    async def handle_IIDX28ranking_getranker_request(self, request: Node) -> Node:
        root = Node.void('IIDX28ranking')

        return root

    async def handle_IIDX28music_crate_request(self, request: Node) -> Node:
        root = Node.void('IIDX28music')

        return root

    async def handle_IIDX28music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute('cltype'))

        root = Node.void('IIDX28music')
        style = Node.void('style')
        root.add_child(style)
        style.set_attribute('type', str(cltype))

        for rivalid in [-1, 0, 1, 2, 3, 4]:
            if rivalid == -1:
                attr = 'iidxid'
            else:
                attr = f'iidxid{rivalid}'

            try:
                extid = int(request.attribute(attr))
            except Exception:
                # Invalid extid
                continue
            userid = await self.data.local.user.from_extid(self.game, self.version, extid)
            if userid is not None:
                scores = await self.data.local.music.get_scores(self.game, self.music_version, userid)

                # Grab score data for user/rival
                scoredata = self.make_score_struct(
                    scores,
                    self.CLEAR_TYPE_SINGLE if cltype == self.GAME_CLTYPE_SINGLE else self.CLEAR_TYPE_DOUBLE,
                    rivalid,
                )
                for s in scoredata:
                    root.add_child(Node.s16_array('m', s))

                # Grab most played for user/rival
                most_played = [
                    play[0] for play in
                    await self.data.local.music.get_most_played(self.game, self.music_version, userid, 20)
                ]
                if len(most_played) < 20:
                    most_played.extend([0] * (20 - len(most_played)))
                best = Node.u16_array('best', most_played)
                best.set_attribute('rno', str(rivalid))
                root.add_child(best)

        return root

    async def handle_IIDX28music_appoint_request(self, request: Node) -> Node:
        musicid = int(request.attribute('mid'))
        game_chart = int(request.attribute('clid'))
        chart = self.game_to_db_chart(game_chart)
        ghost_type = int(request.attribute('ctype'))
        extid = int(request.attribute('iidxid'))
        userid = await self.data.local.user.from_extid(self.game, self.version, extid)

        root = Node.void('IIDX28music')

        if userid is not None:
            # Try to look up previous ghost for user
            my_score = await self.data.local.music.get_score(self.game, self.music_version, userid, musicid, chart)
            if my_score is not None:
                mydata = Node.binary('mydata', my_score.data.get_bytes('ghost'))
                mydata.set_attribute('score', str(my_score.points))
                root.add_child(mydata)

            ghost_score = await self.get_ghost(
                {
                    self.GAME_GHOST_TYPE_RIVAL: self.GHOST_TYPE_RIVAL,
                    self.GAME_GHOST_TYPE_GLOBAL_TOP: self.GHOST_TYPE_GLOBAL_TOP,
                    self.GAME_GHOST_TYPE_GLOBAL_AVERAGE: self.GHOST_TYPE_GLOBAL_AVERAGE,
                    self.GAME_GHOST_TYPE_LOCAL_TOP: self.GHOST_TYPE_LOCAL_TOP,
                    self.GAME_GHOST_TYPE_LOCAL_AVERAGE: self.GHOST_TYPE_LOCAL_AVERAGE,
                    self.GAME_GHOST_TYPE_DAN_TOP: self.GHOST_TYPE_DAN_TOP,
                    self.GAME_GHOST_TYPE_DAN_AVERAGE: self.GHOST_TYPE_DAN_AVERAGE,
                    self.GAME_GHOST_TYPE_RIVAL_TOP: self.GHOST_TYPE_RIVAL_TOP,
                    self.GAME_GHOST_TYPE_RIVAL_AVERAGE: self.GHOST_TYPE_RIVAL_AVERAGE,
                }.get(ghost_type, self.GHOST_TYPE_NONE),
                request.attribute('subtype'),
                self.GAME_GHOST_LENGTH,
                musicid,
                chart,
                userid,
            )

            # Add ghost score if we support it
            if ghost_score is not None:
                sdata = Node.binary('sdata', ghost_score['ghost'])
                sdata.set_attribute('score', str(ghost_score['score']))
                if 'name' in ghost_score:
                    sdata.set_attribute('name', ghost_score['name'])
                if 'pid' in ghost_score:
                    sdata.set_attribute('pid', str(ghost_score['pid']))
                if 'extid' in ghost_score:
                    sdata.set_attribute('riidxid', str(ghost_score['extid']))
                root.add_child(sdata)

        return root

    async def handle_IIDX28music_reg_request(self, request: Node) -> Node:
        extid = int(request.attribute('iidxid'))
        musicid = int(request.attribute('mid'))
        game_chart = int(request.attribute('clid'))
        userid = await self.data.local.user.from_extid(self.game, self.version, extid)
        chart = self.game_to_db_chart(game_chart)

        if userid is not None:
            clear_status = self.game_to_db_status(int(request.attribute('cflg')))
            pgreats = int(request.attribute('pgnum'))
            greats = int(request.attribute('gnum'))
            miss_count = int(request.attribute('mnum'))
            ghost = request.child_value('ghost')
            shopid = ID.parse_machine_id(request.attribute('convid'))

            await self.update_score(
                userid,
                musicid,
                chart,
                clear_status,
                pgreats,
                greats,
                miss_count,
                ghost,
                shopid,
            )

        # Calculate and return statistics about this song
        root = Node.void('IIDX28music')
        root.set_attribute('clid', request.attribute('clid'))
        root.set_attribute('mid', request.attribute('mid'))

        root.set_attribute('crate', '0')
        root.set_attribute('frate', '0')
        root.set_attribute('rankside', '0')

        if userid is not None:
            # Shop ranking
            shopdata = Node.void('shopdata')
            root.add_child(shopdata)
            shopdata.set_attribute('rank', '1')

            # Grab the rank of some other players on this song
            ranklist = Node.void('ranklist')
            root.add_child(ranklist)
            ranklist.set_attribute('total_user_num', '1')

            profile = await self.get_profile(userid)
            score = await self.data.local.music.get_score(game=self.game, version=self.music_version, userid=userid, songid=musicid, songchart=chart)

            data = Node.void('data')
            ranklist.add_child(data)
            data.set_attribute('iidx_id', str(profile.get_int('extid')))
            data.set_attribute('name', profile.get_str('name'))

            machine_name = ''
            if 'shop_location' in profile:
                shop_id = profile.get_int('shop_location')
                machine = await self.get_machine_by_id(shop_id)
                if machine is not None:
                    machine_name = machine.name
            data.set_attribute('opname', machine_name)
            data.set_attribute('rnum', '1')
            data.set_attribute('score', str(score.points))
            data.set_attribute('clflg', str(self.db_to_game_status(score.data.get_int('clear_status'))))
            data.set_attribute('pid', str(profile.get_int('pid')))
            data.set_attribute('myFlg', '1' if score == userid else '0')
            data.set_attribute('achieve', '0')

            data.set_attribute('sgrade', str(
                self.db_to_game_rank(profile.get_int(self.DAN_RANKING_SINGLE, -1), self.GAME_CLTYPE_SINGLE),
            ))
            data.set_attribute('dgrade', str(
                self.db_to_game_rank(profile.get_int(self.DAN_RANKING_DOUBLE, -1), self.GAME_CLTYPE_DOUBLE),
            ))

            qpro = profile.get_dict('qpro')
            data.set_attribute('head', str(qpro.get_int('head')))
            data.set_attribute('hair', str(qpro.get_int('hair')))
            data.set_attribute('face', str(qpro.get_int('face')))
            data.set_attribute('body', str(qpro.get_int('body')))
            data.set_attribute('hand', str(qpro.get_int('hand')))

        return root

    async def handle_IIDX28music_play_request(self, request: Node) -> Node:
        musicid = int(request.attribute('mid'))
        game_chart = int(request.attribute('clid'))
        clear_status = self.game_to_db_status(int(request.attribute('cflg')))
        chart = self.game_to_db_chart(game_chart)
        await self.update_score(
            None,  # No userid since its anonymous
            musicid,
            chart,
            clear_status,
            0,  # No ex score
            0,  # No ex score
            0,  # No miss count
            None,  # No ghost
            None,  # No shop for this user
        )

        # Calculate and return statistics about this song
        root = Node.void('IIDX28music')
        root.set_attribute('clid', request.attribute('clid'))
        root.set_attribute('mid', request.attribute('mid'))
        root.set_attribute('crate', '0')
        root.set_attribute('frate', '0')

        return root

    async def handle_IIDX28grade_raised_request(self, request: Node) -> Node:
        extid = int(request.attribute('iidxid'))
        cltype = int(request.attribute('gtype'))
        rank = self.game_to_db_rank(int(request.attribute('gid')), cltype)

        userid = await self.data.local.user.from_extid(self.game, self.version, extid)
        if userid is not None:
            percent = int(request.attribute('achi'))
            stages_cleared = int(request.attribute('cstage'))
            cleared = stages_cleared == self.DAN_STAGES

            if cltype == self.GAME_CLTYPE_SINGLE:
                index = self.DAN_RANKING_SINGLE
            else:
                index = self.DAN_RANKING_DOUBLE

            await self.update_rank(
                userid,
                index,
                rank,
                percent,
                cleared,
                stages_cleared,
            )

        # Figure out number of players that played this ranking
        all_achievements = await self.data.local.user.get_all_achievements(self.game, self.version)
        num_players = 0
        for [_, ach] in all_achievements:
            if ach.type != index:
                continue
            if ach.id != rank:
                continue
            num_players = num_players + 1

        root = Node.void('IIDX28grade')
        root.set_attribute('pnum', str(num_players))
        return root

    async def handle_IIDX28pc_common_request(self, request: Node) -> Node:
        root = Node.void('IIDX28pc')
        root.set_attribute('expire', '600')

        ir = Node.void('ir')
        root.add_child(ir)
        ir.set_attribute('beat', '2')

        escape_package_info = Node.void('escape_package_info')
        root.add_child(escape_package_info)

        vip_black_pass = Node.void('vip_pass_black')
        root.add_child(vip_black_pass)

        newsong_another = Node.void('newsong_another')
        root.add_child(newsong_another)
        newsong_another.set_attribute('open', '1')

        deller_bonus = Node.void('deller_bonus')
        root.add_child(deller_bonus)
        deller_bonus.set_attribute('open', '1')

        common_evnet = Node.void('common_evnet')  # Yes, this is misspelled in the game
        root.add_child(common_evnet)
        common_evnet.set_attribute('flg', '0')

        expert = Node.void('expert')
        root.add_child(expert)
        expert.set_attribute('phase', '1')

        expert_random_select = Node.void('expert_random_secret')
        root.add_child(expert_random_select)
        expert_random_select.set_attribute('phase', '1')

        expert_full = Node.void('expert_secret_full_open')
        root.add_child(expert_full)

        # some new nodes for rootage

        system_voice = Node.void('system_voice_phase')
        root.add_child(system_voice)
        system_voice.set_attribute('phase', '1')

        anniv20 = Node.void('anniv20_phase')
        root.add_child(anniv20)
        anniv20.set_attribute('phase', '1')

        return root

    async def handle_IIDX28pc_delete_request(self, request: Node) -> Node:
        return Node.void('IIDX28pc')

    async def handle_IIDX28pc_playstart_request(self, request: Node) -> Node:
        return Node.void('IIDX28pc')

    async def handle_IIDX28pc_playend_request(self, request: Node) -> Node:
        return Node.void('IIDX28pc')

    async def handle_IIDX28pc_visit_request(self, request: Node) -> Node:
        root = Node.void('IIDX28pc')
        root.set_attribute('anum', '0')
        root.set_attribute('snum', '0')
        root.set_attribute('pnum', '0')
        root.set_attribute('aflg', '0')
        root.set_attribute('sflg', '0')
        root.set_attribute('pflg', '0')
        return root

    async def handle_IIDX28pc_shopregister_request(self, request: Node) -> Node:
        extid = int(request.child_value('iidx_id'))
        location = ID.parse_machine_id(request.child_value('location_id'))

        userid = await self.data.local.user.from_extid(self.game, self.version, extid)
        if userid is not None:
            profile = self.get_profile(userid)
            if profile is None:
                profile = ValidatedDict()
            profile.replace_int('shop_location', location)
            await self.put_profile(userid, profile)

        root = Node.void('IIDX28pc')
        return root

    async def handle_IIDX28pc_oldget_request(self, request: Node) -> Node:
        refid = request.attribute('rid')
        userid = await self.data.local.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = oldversion.get_profile(userid)
        else:
            profile = None

        root = Node.void('IIDX28pc')
        root.set_attribute('status', '1' if profile is None else '0')
        return root

    async def handle_IIDX28pc_getname_request(self, request: Node) -> Node:
        refid = request.attribute('rid')
        userid = await self.data.local.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = await oldversion.get_profile(userid)
        else:
            profile = None
        if profile is None:
            raise Exception(
                'Should not get here if we have no profile, we should ' +
                'have returned \'1\' in the \'oldget\' method above ' +
                'which should tell the game not to present a migration.'
            )

        root = Node.void('IIDX28pc')
        root.set_attribute('name', profile.get_str('name'))
        root.set_attribute('idstr', ID.format_extid(profile.get_int('extid')))
        root.set_attribute('pid', str(profile.get_int('pid')))
        return root

    async def handle_IIDX28pc_takeover_request(self, request: Node) -> Node:
        refid = request.attribute('rid')
        name = request.attribute('name')
        pid = int(request.attribute('pid'))
        newprofile = await self.new_profile_by_refid(refid, name, pid)

        root = Node.void('IIDX28pc')
        if newprofile is not None:
            root.set_attribute('id', str(newprofile.get_int('extid')))
        return root

    async def handle_IIDX28pc_reg_request(self, request: Node) -> Node:
        refid = request.attribute('rid')
        name = request.attribute('name')
        pid = int(request.attribute('pid'))
        profile = await self.new_profile_by_refid(refid, name, pid)

        root = Node.void('IIDX28pc')
        if profile is not None:
            root.set_attribute('id', str(profile.get_int('extid')))
            root.set_attribute('id_str', ID.format_extid(profile.get_int('extid')))
        return root

    async def handle_IIDX28pc_get_request(self, request: Node) -> Node:
        refid = request.attribute('rid')
        root = await self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void('IIDX28pc')

        return root

    async def handle_IIDX28pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute('iidxid'))
        await self.put_profile_by_extid(extid, request)

        return Node.void('IIDX28pc')

    async def handle_IIDX28pc_logout_request(self, request: Node) -> Node:
        return Node.void('IIDX28pc')

    async def handle_IIDX28gameSystem_systemInfo_request(self, request: Node) -> Node:
        return Node.void('IIDX27gameSystem')

    async def format_profile(self, userid: UserID, profile: ValidatedDict) -> Node:
        root = Node.void('IIDX28pc')

        # Look up play stats we bridge to every mix
        play_stats = await self.get_play_statistics(userid)

        # Look up judge window adjustments
        judge_dict = profile.get_dict('machine_judge_adjust')
        machine_judge = judge_dict.get_dict(self.config['machine']['pcbid'])

        # Profile data
        pcdata = Node.void('pcdata')
        root.add_child(pcdata)
        pcdata.set_attribute('id', str(profile.get_int('extid')))
        pcdata.set_attribute('idstr', ID.format_extid(profile.get_int('extid')))
        pcdata.set_attribute('name', profile.get_str('name'))
        pcdata.set_attribute('pid', str(profile.get_int('pid')))
        pcdata.set_attribute('spnum', str(play_stats.get_int('single_plays')))
        pcdata.set_attribute('dpnum', str(play_stats.get_int('double_plays')))
        pcdata.set_attribute('sach', str(play_stats.get_int('single_dj_points')))
        pcdata.set_attribute('dach', str(play_stats.get_int('double_dj_points')))
        pcdata.set_attribute('mode', str(profile.get_int('mode')))
        pcdata.set_attribute('pmode', str(profile.get_int('pmode')))
        pcdata.set_attribute('rtype', str(profile.get_int('rtype')))
        pcdata.set_attribute('sp_opt', str(profile.get_int('sp_opt')))
        pcdata.set_attribute('dp_opt', str(profile.get_int('dp_opt')))
        pcdata.set_attribute('dp_opt2', str(profile.get_int('dp_opt2')))
        pcdata.set_attribute('gpos', str(profile.get_int('gpos')))
        pcdata.set_attribute('s_sorttype', str(profile.get_int('s_sorttype')))
        pcdata.set_attribute('d_sorttype', str(profile.get_int('d_sorttype')))
        pcdata.set_attribute('s_pace', str(profile.get_int('s_pace')))
        pcdata.set_attribute('d_pace', str(profile.get_int('d_pace')))
        pcdata.set_attribute('s_gno', str(profile.get_int('s_gno')))
        pcdata.set_attribute('d_gno', str(profile.get_int('d_gno')))
        pcdata.set_attribute('s_sub_gno', str(profile.get_int('s_sub_gno')))
        pcdata.set_attribute('d_sub_gno', str(profile.get_int('d_sub_gno')))
        pcdata.set_attribute('s_gtype', str(profile.get_int('s_gtype')))
        pcdata.set_attribute('d_gtype', str(profile.get_int('d_gtype')))
        pcdata.set_attribute('s_sdlen', str(profile.get_int('s_sdlen')))
        pcdata.set_attribute('d_sdlen', str(profile.get_int('d_sdlen')))
        pcdata.set_attribute('s_sdtype', str(profile.get_int('s_sdtype')))
        pcdata.set_attribute('d_sdtype', str(profile.get_int('d_sdtype')))
        pcdata.set_attribute('s_timing', str(profile.get_int('s_timing')))
        pcdata.set_attribute('d_timing', str(profile.get_int('d_timing')))
        pcdata.set_attribute('s_notes', str(profile.get_float('s_notes')))
        pcdata.set_attribute('d_notes', str(profile.get_float('d_notes')))
        pcdata.set_attribute('s_judge', str(profile.get_int('s_judge')))
        pcdata.set_attribute('d_judge', str(profile.get_int('d_judge')))
        pcdata.set_attribute('s_judgeAdj', str(machine_judge.get_int('single')))
        pcdata.set_attribute('d_judgeAdj', str(machine_judge.get_int('double')))
        pcdata.set_attribute('s_hispeed', str(profile.get_float('s_hispeed')))
        pcdata.set_attribute('d_hispeed', str(profile.get_float('d_hispeed')))
        pcdata.set_attribute('s_liflen', str(profile.get_int('s_lift')))
        pcdata.set_attribute('d_liflen', str(profile.get_int('d_lift')))
        pcdata.set_attribute('s_disp_judge', str(profile.get_int('s_disp_judge')))
        pcdata.set_attribute('d_disp_judge', str(profile.get_int('d_disp_judge')))
        pcdata.set_attribute('s_opstyle', str(profile.get_int('s_opstyle')))
        pcdata.set_attribute('d_opstyle', str(profile.get_int('d_opstyle')))
        pcdata.set_attribute('s_graph_score', str(profile.get_int('s_graph_score')))
        pcdata.set_attribute('d_graph_score', str(profile.get_int('d_graph_score')))
        pcdata.set_attribute('s_auto_scrach', str(profile.get_int('s_auto_scrach')))
        pcdata.set_attribute('d_auto_scrach', str(profile.get_int('d_auto_scrach')))
        pcdata.set_attribute('s_gauge_disp', str(profile.get_int('s_gauge_disp')))
        pcdata.set_attribute('d_gauge_disp', str(profile.get_int('d_gauge_disp')))
        pcdata.set_attribute('s_lane_brignt', str(profile.get_int('s_lane_brignt')))
        pcdata.set_attribute('d_lane_brignt', str(profile.get_int('d_lane_brignt')))
        pcdata.set_attribute('s_camera_layout', str(profile.get_int('s_camera_layout')))
        pcdata.set_attribute('d_camera_layout', str(profile.get_int('d_camera_layout')))
        pcdata.set_attribute('s_ghost_score', str(profile.get_int('s_ghost_score')))
        pcdata.set_attribute('d_ghost_score', str(profile.get_int('d_ghost_score')))
        pcdata.set_attribute('s_tsujigiri_disp', str(profile.get_int('s_tsujigiri_disp')))
        pcdata.set_attribute('d_tsujigiri_disp', str(profile.get_int('d_tsujigiri_disp')))
        #########################################################################
        pcdata.set_attribute('ngrade', str(profile.get_int('ngrade')))

        legendarias = Node.void('leggendaria_open')
        root.add_child(legendarias)

        # Song unlock flags
        secret_dict = profile.get_dict('secret')
        secret = Node.void('secret')
        root.add_child(secret)
        secret.add_child(Node.s64_array('flg1', secret_dict.get_int_array('flg1', 3)))
        secret.add_child(Node.s64_array('flg2', secret_dict.get_int_array('flg2', 3)))
        secret.add_child(Node.s64_array('flg3', secret_dict.get_int_array('flg3', 3)))
        secret.add_child(Node.s64_array('flg4', secret_dict.get_int_array('flg4', 3)))

        # Qpro secret data from step-up mode
        qpro_secrete_dict = profile.get_dict('qpro_secret')
        qpro_secret = Node.void('qpro_secret')
        root.add_child(qpro_secret)
        qpro_secret.add_child(Node.s64_array('head', qpro_secrete_dict.get_int_array('head', 5)))
        qpro_secret.add_child(Node.s64_array('hair', qpro_secrete_dict.get_int_array('hair', 5)))
        qpro_secret.add_child(Node.s64_array('face', qpro_secrete_dict.get_int_array('face', 5)))
        qpro_secret.add_child(Node.s64_array('body', qpro_secrete_dict.get_int_array('body', 5)))
        qpro_secret.add_child(Node.s64_array('hand', qpro_secrete_dict.get_int_array('hand', 5)))

        # DAN rankings
        grade = Node.void('grade')
        root.add_child(grade)
        grade.set_attribute('sgid', str(self.db_to_game_rank(profile.get_int(self.DAN_RANKING_SINGLE, -1), self.GAME_CLTYPE_SINGLE)))
        grade.set_attribute('dgid', str(self.db_to_game_rank(profile.get_int(self.DAN_RANKING_DOUBLE, -1), self.GAME_CLTYPE_DOUBLE)))
        achievements = await self.data.local.user.get_achievements(self.game, self.version, userid)
        for rank in achievements:
            if rank.type == self.DAN_RANKING_SINGLE:
                grade.add_child(Node.u8_array('g', [
                    self.GAME_CLTYPE_SINGLE,
                    self.db_to_game_rank(rank.id, self.GAME_CLTYPE_SINGLE),
                    rank.data.get_int('stages_cleared'),
                    rank.data.get_int('percent'),
                ]))
            if rank.type == self.DAN_RANKING_DOUBLE:
                grade.add_child(Node.u8_array('g', [
                    self.GAME_CLTYPE_DOUBLE,
                    self.db_to_game_rank(rank.id, self.GAME_CLTYPE_DOUBLE),
                    rank.data.get_int('stages_cleared'),
                    rank.data.get_int('percent'),
                ]))

        # User settings
        settings_dict = profile.get_dict('settings')
        skin = Node.s16_array(
            'skin',
            [
                settings_dict.get_int('frame'),
                settings_dict.get_int('turntable'),
                settings_dict.get_int('burst'),
                settings_dict.get_int('bgm'),
                settings_dict.get_int('flags'),
                settings_dict.get_int('towel'),
                settings_dict.get_int('judge_pos'),
                settings_dict.get_int('voice'),
                settings_dict.get_int('noteskin'),
                settings_dict.get_int('full_combo'),
                settings_dict.get_int('beam'),
                settings_dict.get_int('judge'),
                0,
                settings_dict.get_int('disable_song_preview'),
                settings_dict.get_int('pacemaker'),
                settings_dict.get_int('effector_lock'),
                settings_dict.get_int('effector_preset'),
                0,
                0,
                1,
            ],
        )
        root.add_child(skin)

        # Qpro data
        qpro_dict = profile.get_dict('qpro')
        root.add_child(Node.u32_array(
            'qprodata',
            [
                qpro_dict.get_int('head'),
                qpro_dict.get_int('hair'),
                qpro_dict.get_int('face'),
                qpro_dict.get_int('hand'),
                qpro_dict.get_int('body'),
            ],
        ))

        # Rivals
        rlist = Node.void('rlist')
        root.add_child(rlist)

        # DJ RANK
        for dj_rank in achievements:
            if dj_rank.type != 'dj_rank':
                continue

            dj_rank_node = Node.void('dj_rank')
            root.add_child(dj_rank_node)
            dj_rank_node.set_attribute('style', str(dj_rank.id))
            dj_rank_node.add_child(Node.s32_array('rank', dj_rank.data.get_int_array('rank', 15)))
            dj_rank_node.add_child(Node.s32_array('point', dj_rank.data.get_int_array('point', 15)))

        # notes radar saving
        for notes_radar in achievements:
            if notes_radar.type != 'notes_radar':
                continue

            notes_radar_node = Node.void('notes_radar')
            root.add_child(notes_radar_node)
            notes_radar_node.set_attribute('style', str(notes_radar.id))
            notes_radar_node.add_child(Node.s32_array('radar_score', notes_radar.data.get_int_array('radar_score', 6)))

        dj_rank_ranking_node = Node.void('dj_rank_ranking')
        root.add_child(dj_rank_ranking_node)
        dj_rank_ranking_node.set_attribute('style', '0')
        for j in range(15):
            detail = Node.void('detail')
            dj_rank_ranking_node.add_child(detail)
            detail.set_attribute('category', str(j))
            detail.set_attribute('total_user', '0')
            detail.set_attribute('rank', '0')
            detail.set_attribute('platinum_point', '0')
            detail.set_attribute('platinum_rank', '0')
            detail.set_attribute('gold_point', '0')
            detail.set_attribute('gold_rank', '0')
            detail.set_attribute('silver_point', '0')
            detail.set_attribute('silver_rank', '0')
            detail.set_attribute('bronze_point', '0')
            detail.set_attribute('bronze_rank', '0')
            detail.set_attribute('white_point', '0')
            detail.set_attribute('white_rank', '0')

        dj_rank_ranking_node = Node.void('dj_rank_ranking')
        root.add_child(dj_rank_ranking_node)
        dj_rank_ranking_node.set_attribute('style', '1')
        for j in range(15):
            detail = Node.void('detail')
            dj_rank_ranking_node.add_child(detail)
            detail.set_attribute('category', str(j))
            detail.set_attribute('total_user', '0')
            detail.set_attribute('rank', '0')
            detail.set_attribute('platinum_point', '0')
            detail.set_attribute('platinum_rank', '0')
            detail.set_attribute('gold_point', '0')
            detail.set_attribute('gold_rank', '0')
            detail.set_attribute('silver_point', '0')
            detail.set_attribute('silver_rank', '0')
            detail.set_attribute('bronze_point', '0')
            detail.set_attribute('bronze_rank', '0')
            detail.set_attribute('white_point', '0')
            detail.set_attribute('white_rank', '0')

        tonyutsu = Node.void('tonyutsu')
        tonyutsu_dict = profile.get_dict('tonyutsu')
        tonyutsu.set_attribute('platinum_pass', str(tonyutsu_dict.get_int('platiunum_pass')))
        tonyutsu.set_attribute('black_pass', str(tonyutsu_dict.get_int('black_pass')))

        # If the user joined a particular shop, let the game know.
        if 'shop_location' in profile:
            shop_id = profile.get_int('shop_location')
            machine = await self.get_machine_by_id(shop_id)
            if machine is not None:
                join_shop = Node.void('join_shop')
                root.add_child(join_shop)
                join_shop.set_attribute('joinflg', '1')
                join_shop.set_attribute('join_cflg', '1')
                join_shop.set_attribute('join_id', ID.format_machine_id(machine.id))
                join_shop.set_attribute('join_name', machine.name)

        # Daily recommendations
        entry = await self.data.local.game.get_time_sensitive_settings(self.game, self.version, 'dailies')
        if entry is not None:
            packinfo = Node.void('packinfo')
            root.add_child(packinfo)

            pack_id = int(entry['start_time'] / 86400)
            packinfo.set_attribute('pack_id', str(pack_id))
            packinfo.set_attribute('music_0', str(entry['music'][0]))
            packinfo.set_attribute('music_1', str(entry['music'][1]))
            packinfo.set_attribute('music_2', str(entry['music'][2]))
        else:
            # No dailies :(
            pack_id = None

        # Tran medals and shit
        achievement_node = Node.void('achievements')
        root.add_child(achievement_node)

        # Dailies
        if pack_id is None:
            achievement_node.set_attribute('pack', '0')
            achievement_node.set_attribute('pack_comp', '0')
        else:
            daily_played = await self.data.local.user.get_achievement(self.game, self.version, userid, pack_id, 'daily')
            if daily_played is None:
                daily_played = ValidatedDict()
            achievement_node.set_attribute('pack', str(daily_played.get_int('pack_flg')))
            achievement_node.set_attribute('pack_comp', str(daily_played.get_int('pack_comp')))

        # Weeklies
        achievement_node.set_attribute('last_weekly', str(profile.get_int('last_weekly')))
        achievement_node.set_attribute('weekly_num', str(profile.get_int('weekly_num')))

        # Prefecture visit flag
        achievement_node.set_attribute('visit_flg', str(profile.get_int('visit_flg')))

        # Number of rivals beaten
        achievement_node.set_attribute('rival_crush', str(profile.get_int('rival_crush')))

        # Tran medals
        achievement_node.add_child(Node.s64_array('trophy', profile.get_int_array('trophy', 20)))

        # Track deller
        deller = Node.void('deller')
        root.add_child(deller)
        deller.set_attribute('deller', str(profile.get_int('deller')))
        deller.set_attribute('rate', '0')

        # Expert points
        expert_point = Node.void('expert_point')
        root.add_child(expert_point)
        for rank in achievements:
            if rank.type == 'expert_point':
                detail = Node.void('detail')
                expert_point.add_child(detail)
                detail.set_attribute('course_id', str(rank.id))
                detail.set_attribute('n_point', str(rank.data.get_int('normal_points')))
                detail.set_attribute('h_point', str(rank.data.get_int('hyper_points')))
                detail.set_attribute('a_point', str(rank.data.get_int('another_points')))

        # language setting
        language = Node.void('language_setting')
        root.add_child(language)
        language.set_attribute('language', str(profile.get_int('language')))

        nostalgia = Node.void('nostalgia_open')
        root.add_child(nostalgia)

        root.add_child(Node.void('bind_eaappli'))
        pay_per_use = Node.void('pay_per_use')
        root.add_child(pay_per_use)
        pay_per_use.set_attribute('item_num', '99')

        # bpl_supporter
        bpl_supporter = Node.void('bpl_supporter')
        root.add_child(bpl_supporter)
        bpl_dict = profile.get_dict('bpl')
        bpl_supporter.set_attribute('support_team', str(bpl_dict.get_int('support_team')))

        return root

    async def unformat_profile(self, userid: UserID, request: Node, oldprofile: ValidatedDict) -> ValidatedDict:
        newprofile = copy.deepcopy(oldprofile)
        play_stats = await self.get_play_statistics(userid)

        # Track play counts
        cltype = int(request.attribute('cltype'))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.increment_int('single_plays')
        if cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.increment_int('double_plays')

        # Track DJ points
        play_stats.replace_int('single_dj_points', int(request.attribute('s_achi')))
        play_stats.replace_int('double_dj_points', int(request.attribute('d_achi')))

        # Profile settings
        newprofile.replace_int('sp_opt', int(request.attribute('sp_opt')))
        newprofile.replace_int('dp_opt', int(request.attribute('dp_opt')))
        newprofile.replace_int('dp_opt2', int(request.attribute('dp_opt2')))
        newprofile.replace_int('gpos', int(request.attribute('gpos')))
        newprofile.replace_int('s_sorttype', int(request.attribute('s_sorttype')))
        newprofile.replace_int('d_sorttype', int(request.attribute('d_sorttype')))
        newprofile.replace_int('s_disp_judge', int(request.attribute('s_disp_judge')))
        newprofile.replace_int('d_disp_judge', int(request.attribute('d_disp_judge')))
        newprofile.replace_int('s_pace', int(request.attribute('s_pace')))
        newprofile.replace_int('d_pace', int(request.attribute('d_pace')))
        newprofile.replace_int('s_gno', int(request.attribute('s_gno')))
        newprofile.replace_int('d_gno', int(request.attribute('d_gno')))
        newprofile.replace_int('s_sub_gno', int(request.attribute('s_sub_gno')))
        newprofile.replace_int('d_sub_gno', int(request.attribute('d_sub_gno')))
        newprofile.replace_int('s_gtype', int(request.attribute('s_gtype')))
        newprofile.replace_int('d_gtype', int(request.attribute('d_gtype')))
        newprofile.replace_int('s_sdlen', int(request.attribute('s_sdlen')))
        newprofile.replace_int('d_sdlen', int(request.attribute('d_sdlen')))
        newprofile.replace_int('s_sdtype', int(request.attribute('s_sdtype')))
        newprofile.replace_int('d_sdtype', int(request.attribute('d_sdtype')))
        newprofile.replace_int('s_timing', int(request.attribute('s_timing')))
        newprofile.replace_int('d_timing', int(request.attribute('d_timing')))
        newprofile.replace_float('s_notes', float(request.attribute('s_notes')))
        newprofile.replace_float('d_notes', float(request.attribute('d_notes')))
        newprofile.replace_int('s_judge', int(request.attribute('s_judge')))
        newprofile.replace_int('d_judge', int(request.attribute('d_judge')))
        newprofile.replace_float('s_hispeed', float(request.attribute('s_hispeed')))
        newprofile.replace_float('d_hispeed', float(request.attribute('d_hispeed')))
        newprofile.replace_int('s_opstyle', int(request.attribute('s_opstyle')))
        newprofile.replace_int('d_opstyle', int(request.attribute('d_opstyle')))
        newprofile.replace_int('s_graph_score', int(request.attribute('s_graph_score')))
        newprofile.replace_int('d_graph_score', int(request.attribute('d_graph_score')))
        newprofile.replace_int('s_auto_scrach', int(request.attribute('s_auto_scrach')))
        newprofile.replace_int('d_auto_scrach', int(request.attribute('d_auto_scrach')))
        newprofile.replace_int('s_gauge_disp', int(request.attribute('s_gauge_disp')))
        newprofile.replace_int('d_gauge_disp', int(request.attribute('d_gauge_disp')))
        newprofile.replace_int('s_lane_brignt', int(request.attribute('s_lane_brignt')))
        newprofile.replace_int('d_lane_brignt', int(request.attribute('d_lane_brignt')))
        newprofile.replace_int('s_camera_layout', int(request.attribute('s_camera_layout')))
        newprofile.replace_int('d_camera_layout', int(request.attribute('d_camera_layout')))
        newprofile.replace_int('s_ghost_score', int(request.attribute('s_ghost_score')))
        newprofile.replace_int('d_ghost_score', int(request.attribute('d_ghost_score')))
        newprofile.replace_int('s_tsujigiri_disp', int(request.attribute('s_tsujigiri_disp')))
        newprofile.replace_int('d_tsujigiri_disp', int(request.attribute('d_tsujigiri_disp')))
        newprofile.replace_int('s_lift', int(request.attribute('s_lift')))
        newprofile.replace_int('d_lift', int(request.attribute('d_lift')))
        newprofile.replace_int('mode', int(request.attribute('mode')))
        newprofile.replace_int('pmode', int(request.attribute('pmode')))
        newprofile.replace_int('ngrade', int(request.attribute('ngrade')))
        newprofile.replace_int('rtype', int(request.attribute('rtype')))

        # Update judge window adjustments per-machine
        judge_dict = newprofile.get_dict('machine_judge_adjust')
        machine_judge = judge_dict.get_dict(self.config['machine']['pcbid'])
        machine_judge.replace_int('single', int(request.attribute('s_judgeAdj')))
        machine_judge.replace_int('double', int(request.attribute('d_judgeAdj')))
        judge_dict.replace_dict(self.config['machine']['pcbid'], machine_judge)
        newprofile.replace_dict('machine_judge_adjust', judge_dict)

        # Secret flags saving
        secret = request.child('secret')
        if secret is not None:
            secret_dict = newprofile.get_dict('secret')
            secret_dict.replace_int_array('flg1', 3, secret.child_value('flg1'))
            secret_dict.replace_int_array('flg2', 3, secret.child_value('flg2'))
            secret_dict.replace_int_array('flg3', 3, secret.child_value('flg3'))
            secret_dict.replace_int_array('flg4', 3, secret.child_value('flg4'))
            newprofile.replace_dict('secret', secret_dict)

        # Basic achievements
        achievements = request.child('achievements')
        if achievements is not None:
            newprofile.replace_int('visit_flg', int(achievements.attribute('visit_flg')))
            newprofile.replace_int('last_weekly', int(achievements.attribute('last_weekly')))
            newprofile.replace_int('weekly_num', int(achievements.attribute('weekly_num')))

            pack_id = int(achievements.attribute('pack_id'))
            if pack_id > 0:
                await self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    pack_id,
                    'daily',
                    {
                        'pack_flg': int(achievements.attribute('pack_flg')),
                        'pack_comp': int(achievements.attribute('pack_comp')),
                    },
                )

            trophies = achievements.child('trophy')
            if trophies is not None:
                # We only load the first 20 in profile load.
                newprofile.replace_int_array('trophy', 20, trophies.value[:20])

        # Deller saving
        deller = request.child('deller')
        if deller is not None:
            newprofile.replace_int('deller', newprofile.get_int('deller') + int(deller.attribute('deller')))

        # Secret course expert point saving
        expert_point = request.child('expert_point')
        if expert_point is not None:
            courseid = int(expert_point.attribute('course_id'))

            # Update achievement to track expert points
            expert_point_achievement = await self.data.local.user.get_achievement(
                self.game,
                self.version,
                userid,
                courseid,
                'expert_point',
            )
            if expert_point_achievement is None:
                expert_point_achievement = ValidatedDict()
            expert_point_achievement.replace_int(
                'normal_points',
                int(expert_point.attribute('n_point')),
            )
            expert_point_achievement.replace_int(
                'hyper_points',
                int(expert_point.attribute('h_point')),
            )
            expert_point_achievement.replace_int(
                'another_points',
                int(expert_point.attribute('a_point')),
            )

            await self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                courseid,
                'expert_point',
                expert_point_achievement,
            )

        # Favorites saving
        for favorite in request.children:
            singles = []
            doubles = []
            name = None
            if favorite.name in ['favorite', 'extra_favorite']:
                if favorite.name == 'favorite':
                    name = 'favorite1'
                elif favorite.name == 'extra_favorite':
                    folder = favorite.attribute('folder_id')
                    if folder == '0':
                        name = 'favorite2'
                    if folder == '1':
                        name = 'favorite3'
                if name is None:
                    continue

                single_music_bin = favorite.child_value('sp_mlist')
                single_chart_bin = favorite.child_value('sp_clist')
                double_music_bin = favorite.child_value('dp_mlist')
                double_chart_bin = favorite.child_value('dp_clist')

                for i in range(self.FAVORITE_LIST_LENGTH):
                    singles.append({
                        'id': struct.unpack('<L', single_music_bin[(i * 4):((i + 1) * 4)])[0],
                        'chart': struct.unpack('B', single_chart_bin[i:(i + 1)])[0],
                    })
                    doubles.append({
                        'id': struct.unpack('<L', double_music_bin[(i * 4):((i + 1) * 4)])[0],
                        'chart': struct.unpack('B', double_chart_bin[i:(i + 1)])[0],
                    })

            # Filter out empty charts
            singles = [single for single in singles if single['id'] != 0]
            doubles = [double for double in doubles if double['id'] != 0]

            newprofile.replace_dict(
                name,
                {
                    'single': singles,
                    'double': doubles,
                },
            )

        # DJ rank saving
        for dj_rank in request.children:
            if dj_rank.name != 'dj_rank':
                continue

            rankid = int(dj_rank.attribute('style'))
            rank = dj_rank.child_value('rank')
            point = dj_rank.child_value('point')

            await self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                rankid,
                'dj_rank',
                {
                    'rank': rank,
                    'point': point,
                }
            )

        # note radar saving
        for notes_radar in request.children:
            if notes_radar.name != 'notes_radar':
                continue

            rankid = int(notes_radar.attribute('style'))
            score = notes_radar.child_value('radar_score')

            await self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                rankid,
                'notes_radar',
                {
                    'radar_score': score,
                }
            )

        # Step-up mode
        step = request.child('step')
        if step is not None:
            step_dict = newprofile.get_dict('step')
            step_dict.replace_int('enemy_damage', int(step.attribute('enemy_damage')))
            step_dict.replace_int('progress', int(step.attribute('progress')))
            step_dict.replace_bool('is_track_ticket', bool(step.child_value('is_track_ticket')))
            step_dict.replace_int('sp_level', int(step.attribute('sp_level')))
            step_dict.replace_int('dp_level', int(step.attribute('dp_level')))
            step_dict.replace_int('sp_mplay', int(step.attribute('sp_mplay')))
            step_dict.replace_int('dp_mplay', int(step.attribute('dp_mplay')))
            step_dict.replace_int('sp_mission_point', str(step_dict.get_int('sp_mission_point')))
            step_dict.replace_int('dp_mission_point', str(step_dict.get_int('dp_mission_point')))
            step_dict.replace_int('sp_dj_mission_level', str(step_dict.get_int('sp_dj_mission_level@')))
            step_dict.replace_int('dp_dj_mission_level', str(step_dict.get_int('dp_dj_mission_level@')))
            step_dict.replace_int('sp_clear_mission_level', str(step_dict.get_int('sp_clear_mission_level')))
            step_dict.replace_int('dp_clear_mission_level', str(step_dict.get_int('dp_clear_mission_level')))
            step_dict.replace_int('sp_dj_mission_clear', str(step_dict.get_int('sp_dj_mission_clear')))
            step_dict.replace_int('dp_dj_mission_clear', str(step_dict.get_int('dp_dj_mission_clear')))
            step_dict.replace_int('sp_clear_mission_clear', str(step_dict.get_int('sp_clear_mission_clear')))
            step_dict.replace_int('dp_clear_mission_clear', str(step_dict.get_int('dp_clear_mission_clear')))
            step_dict.replace_int('tips_read_list', str(step_dict.get_int('tips_read_list')))
            newprofile.replace_dict('step', step_dict)

        # QPro equip in step-up mode
        qpro_equip = request.child('qpro_equip')
        if qpro_equip is not None:
            qpro_dict = newprofile.get_dict('qpro')
            qpro_dict.replace_int('head', int(qpro_equip.attribute('head')))
            qpro_dict.replace_int('hair', int(qpro_equip.attribute('hair')))
            qpro_dict.replace_int('face', int(qpro_equip.attribute('face')))
            qpro_dict.replace_int('hand', int(qpro_equip.attribute('hand')))
            qpro_dict.replace_int('body', int(qpro_equip.attribute('body')))
            newprofile.replace_dict('qpro', qpro_dict)

        # Qpro secret unlocks in step-up mode
        qpro_secret = request.child('qpro_secret')
        if qpro_secret is not None:
            qpro_secret_dict = newprofile.get_dict('qpro_secret')
            qpro_secret_dict.replace_int_array('head', 5, qpro_secret.child_value('head'))
            qpro_secret_dict.replace_int_array('hair', 5, qpro_secret.child_value('hair'))
            qpro_secret_dict.replace_int_array('face', 5, qpro_secret.child_value('face'))
            qpro_secret_dict.replace_int_array('body', 5, qpro_secret.child_value('body'))
            qpro_secret_dict.replace_int_array('hand', 5, qpro_secret.child_value('hand'))
            newprofile.replace_dict('qpro_secret', qpro_secret_dict)

        # tonyutsu saving
        tonyutsu = request.child('tonyutsu')
        if tonyutsu is not None:
            tonyutsu_dict = newprofile.get_dict('tonyutsu')
            tonyutsu_dict.replace_int('platinum_pass', tonyutsu.attribute('platinum_pass'))
            tonyutsu_dict.replace_int('black_pass', tonyutsu.attribute('black_pass'))

        # language select saving
        language = request.child('language_setting')
        if language is not None:
            newprofile.replace_int('language', int(language.attribute('language')))

        # Keep track of play statistics across all mixes
        await self.update_play_statistics(userid, play_stats)

        return newprofile
