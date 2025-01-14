# coding=utf-8
from .pelts import *
from .names import *
from .sprites import *
from .game_essentials import *
from random import choice, randint
import math
import os.path


class Cat(object):
    used_screen = screen
    traits = ['古怪', '嗜血', '野心勃勃', '忠诚', '正直', '凶狠', '紧张', '严厉',
              '极具魅力', '沉着', '无畏', '慈爱', '顽皮', '孤僻', '冷酷', '忧虑', '报复心强',
              '不知廉耻', '忠实可靠', '麻烦精', '善解人意', '勇于冒险', '体贴周到', '富有同情心',
              '幼稚', '自信', '小心谨慎', '无私', '鲁莽', '机灵', '有责任心', '鬼鬼祟祟', '睿智']
    kit_traits = ['活泼', '恃强欺弱', '白日做梦', '神经质', '迷人', '渴求关注', '冲动',
                  '好奇', '专横', '麻烦精', '安静', '无畏', '甜美', '缺乏安全感', '吵闹', '礼貌']
    ages = ['幼崽', '青少年', '青年', '成年', '中年', '长老', '死亡']
    age_moons = {'幼崽': [0, 5], '青少年': [6, 11], '青年': [12, 47], '成年': [48, 95],
                 '中年': [96, 119], '长老': [120, 199]}
    gender_tags = {'雌性': 'F', '雄性': 'M'}
    skills = ['不错的猎手', '优秀的猎手', '杰出的猎手', '聪明', '很聪明', '极其聪明',
              '不错的战士', '优秀的战士', '杰出的战士', '不错的演说家', '出色的演说家',
              '杰出的演说家', '与星族有紧密的联系', '不错的导师', '优秀的导师',
              '杰出的导师']

    all_cats = {}  # ID: object

    def __init__(self, prefix=None, gender=None, status="幼崽", parent1=None, parent2=None, pelt=None,
                 eye_colour=None, suffix=None, ID=None, moons=None, example=False):
        self.gender = gender
        self.status = status
        self.age = None
        self.parent1 = parent1
        self.parent2 = parent2
        self.pelt = pelt
        self.eye_colour = eye_colour
        self.mentor = None
        self.former_mentor = []
        self.apprentice = []
        self.former_apprentices = []
        self.mate = None
        self.placement = None
        self.example = example
        self.dead = False
        self.died_by = None  # once the cat dies, tell the cause
        self.dead_for = 0  # moons
        self.thought = ''
        if ID is None:
            self.ID = str(randint(10000, 99999))
        else:
            self.ID = ID
        # personality trait and skill
        if self.status != '幼崽':
            self.trait = choice(self.traits)
            if self.status != '学徒' and self.status != '巫医学徒':
                self.skill = choice(self.skills)
            else:
                self.skill = '???'
        else:
            self.trait = self.trait = choice(self.kit_traits)
            self.skill = '???'
        if self.gender is None:
            self.gender = choice(["雌性", "雄性"])
        self.g_tag = self.gender_tags[self.gender]
        if status is None:
            self.age = choice(self.ages)
        else:
            if status in ['幼崽', '长老']:
                self.age = status
            elif status == '学徒':
                self.age = '青少年'
            elif status == '巫医学徒':
                self.age = '青少年'
            else:
                self.age = choice(['青年', '成年', '成年', '中年'])
        if moons is None:
            self.moons = randint(self.age_moons[self.age][0], self.age_moons[self.age][1])
        else:
            self.moons = moons

        # eye colour
        if self.eye_colour is None:
            a = randint(0, 200)
            if a == 1:
                self.eye_colour = choice(["BLUEYELLOW", "BLUEGREEN"])
            else:
                if self.parent1 is None:
                    self.eye_colour = choice(eye_colours)
                elif self.parent2 is None:
                    par1 = self.all_cats[self.parent1]
                    self.eye_colour = choice([par1.eye_colour, choice(eye_colours)])
                else:
                    par1 = self.all_cats[self.parent1]
                    par2 = self.all_cats[self.parent2]
                    self.eye_colour = choice([par1.eye_colour, par2.eye_colour, choice(eye_colours)])

        # pelt
        if self.pelt is None:
            if self.parent1 is None:
                # If pelt has not been picked manually, this function chooses one based on possible inheritances
                self.pelt = choose_pelt(self.gender)

            elif self.parent2 is None and self.parent1 in self.all_cats.keys():
                # 1 in 3 chance to inherit a single parent's pelt
                par1 = self.all_cats[self.parent1]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, None]),
                                        choice([par1.pelt.white, None]),
                                        choice([par1.pelt.name, None]),
                                        choice([par1.pelt.length, None]))

            elif self.parent1 in self.all_cats.keys() and self.parent2 in self.all_cats.keys():
                # 2 in 3 chance to inherit either parent's pelt
                par1 = self.all_cats[self.parent1]
                par2 = self.all_cats[self.parent2]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, par2.pelt.colour, None]),
                                        choice([par1.pelt.white, par2.pelt.white, None]),
                                        choice([par1.pelt.name, par2.pelt.name, None]),
                                        choice([par1.pelt.length, par2.pelt.length, None]))

        # NAME
        if self.pelt is not None:
            self.name = Name(status, prefix, suffix, self.pelt.colour, self.eye_colour, self.pelt.name)
        else:
            self.name = Name(status, prefix, suffix, eyes=self.eye_colour)

        # SPRITE
        self.age_sprites = {'幼崽': randint(0, 2), '青少年': randint(3, 5), '长老': randint(3, 5)}
        self.reverse = choice([True, False])
        self.skin = choice(skin_sprites)

        # scars & more
        scar_choice = randint(0, 15)
        if self.age in ['幼崽', '青少年']:
            scar_choice = randint(0, 50)
        elif self.age in ['青年', '成年']:
            scar_choice = randint(0, 20)
        if scar_choice == 1:
            self.specialty = choice([choice(scars1), choice(scars2)])
        else:
            self.specialty = None

        scar_choice2 = randint(0, 30)
        if self.age in ['幼崽', '青少年']:
            scar_choice2 = randint(0, 100)
        elif self.age in ['青年', '成年']:
            scar_choice2 = randint(0, 40)
        if scar_choice2 == 1:
            self.specialty2 = choice([choice(scars1), choice(scars2)])
        else:
            self.specialty2 = None

        # random event
        if self.pelt is not None:
            if self.pelt.length != '长毛':
                self.age_sprites['成年'] = randint(6, 8)
            else:
                self.age_sprites['成年'] = randint(0, 2)
            self.age_sprites['青年'] = self.age_sprites['成年']
            self.age_sprites['中年'] = self.age_sprites['成年']
            self.age_sprites['死亡'] = None  # The sprite that the cat has in starclan

            # WHITE PATCHES
            if self.pelt.white and self.pelt.white_patches is not None:
                pelt_choice = randint(0, 10)
                if pelt_choice == 1 and self.pelt.name in ['Calico', 'TwoColour', 'Tabby', 'Speckled'] \
                        and self.pelt.colour != 'WHITE':
                    self.white_patches = choice(['COLOURPOINT', 'COLOURPOINTCREAMY', 'RAGDOLL'])
                elif pelt_choice == 1 and self.pelt.name in ['Calico', 'TwoColour', 'Tabby', 'Speckled']:
                    self.white_patches = choice(['COLOURPOINT', 'RAGDOLL'])
                elif self.pelt.name in ['Tabby', 'Speckled', 'TwoColour'] and self.pelt.colour == 'WHITE':
                    self.white_patches = choice(
                        ['ANY', 'TUXEDO', 'LITTLE', 'VAN', 'ANY2', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG',
                         'LIGHTSONG', 'VITILIGO'])
                else:
                    self.white_patches = choice(self.pelt.white_patches)
            else:
                self.white_patches = choice(['EXTRA', None, None])

            # pattern for tortie/calico cats
            if self.pelt.name == 'Calico':
                self.pattern = choice(calico_pattern)
            elif self.pelt.name == 'Tortie':
                self.pattern = choice(tortie_pattern)
            else:
                self.pattern = None
        else:
            self.white_patches = None
            self.pattern = None

        # Sprite sizes
        self.sprite = None
        self.big_sprite = None
        self.large_sprite = None

        # experience and current patrol status
        self.experience = 0
        self.in_camp = 1

        experience_levels = ['很低', '低', '略低', '平均', '较高', '高', '很高',
                             '精通', '极致']
        self.experience_level = experience_levels[math.floor(self.experience / 10)]

        # SAVE CAT INTO ALL_CATS DICTIONARY IN CATS-CLASS
        self.all_cats[self.ID] = self

    def __repr__(self):
        return self.ID

    def one_moon(self):  # Go forward in time one moon
        if game.switches['timeskip']:
            key_copy = tuple(cat_class.all_cats.keys())
            for index, i in enumerate(key_copy):
                cat = cat_class.all_cats[i]
                if not cat.dead:
                    cat.in_camp = 1
                    self.perform_ceremonies(cat)
                    self.gain_scars(cat)
                    self.handle_deaths(cat)
                    self.create_interactions(cat, index, key_copy)
                    # possibly have kits
                    cat.have_kits()
                else:  # if cat was already dead
                    cat.dead_for += 1
            self.thoughts()

            # Age the clan itself
            game.clan.age += 1
            game.clan.current_season = game.clan.seasons[game.clan.age % 12]
            game.event_scroll_ct = 0
            has_med = False
            for cat in cat_class.all_cats.values():
                if str(cat.status) == "巫医" or str(cat.status) == "巫医学徒":
                    if not cat.dead:
                        has_med = True
                        break
            if not has_med:
                game.cur_events_list.insert(0, game.clan.name + "族群失去巫医了!")
            if game.clan.deputy == 0 or game.clan.deputy is None or game.clan.deputy.dead:
                game.cur_events_list.insert(0, game.clan.name + "族群失去副族长了!")
            if game.clan.leader.dead:
                game.cur_events_list.insert(0, game.clan.name + "族群失去族长了!")
        game.switches['进入下个月'] = False

    def perform_ceremonies(self,
                           cat):  # This function is called when apprentice/warrior/other ceremonies are performed every moon
        if game.clan.leader.dead and game.clan.deputy is not None and not game.clan.deputy.dead:
            game.clan.new_leader(game.clan.deputy)
            game.cur_events_list.append(
                str(game.clan.deputy.name) + ' 被任命为族群的新族长')
            game.clan.deputy = None
        if not cat.dead:
            cat.moons += 1
            if cat.status == '副族长' and game.clan.deputy is None:
                game.clan.deputy = cat
            if cat.moons > self.age_moons[cat.age][1]:
                # Give the cat a new age group, if old enough
                if cat.age != '长老':
                    cat.age = self.ages[self.ages.index(cat.age) + 1]
                # change the status
                if cat.status == '幼崽' and cat.age == '青少年':
                    cat.status_change('学徒')
                    game.cur_events_list.append(str(cat.name) + ' 开启了学徒生涯')
                elif cat.status == '学徒' and cat.age == '青年':
                    cat.status_change('武士')
                    cat.update_mentor()
                    game.cur_events_list.append(str(cat.name) + ' 获得了武士封号')
                elif cat.status == '巫医学徒' and cat.age == '青年':
                    cat.status_change('巫医')
                    cat.update_mentor()
                    game.cur_events_list.append(str(cat.name) + ' 获得了巫医封号')
                    game.clan.new_medicine_cat(cat)
                elif cat.status == '武士' and cat.age == '长老':
                    cat.status_change('长老')
                    game.cur_events_list.append(str(cat.name) + ' 加入了长老的行列')
                elif cat.status == '副族长' and cat.age == '长老':
                    cat.status_change('长老')
                    game.clan.deputy = None
                    game.cur_events_list.append('副族长 ' + str(cat.name) + ' 加入了长老的行列')

    def gain_scars(self, cat):
        # gaining scars with age
        if cat.specialty is None and cat.age != '幼崽':
            chance = 0
            if cat.age in ['青少年', '青年']:
                chance = randint(0, 50)
            elif cat.age in ['成年', '中年']:
                chance = randint(0, 70)
            else:
                chance = randint(0, 90)
            if chance == 1:
                cat.specialty = choice([choice(scars1), choice(scars2)])
                if cat.specialty == 'NOTAIL':
                    game.cur_events_list.append(str(cat.name) + ' 因为' + choice(
                        ['泼皮猫', '狗', '狐狸', '水獭', '家鼠', '鹰']) + '失去了尾巴')
                else:
                    game.cur_events_list.append(
                        str(cat.name) + ' 因为' + choice(
                            ['泼皮猫', '狗', '狐狸', '水獭', '家鼠', '鹰']) + '留下了一道疤')
            else:
                cat.specialty = None

        elif cat.specialty2 is None and cat.age != '幼崽':
            chance = 0
            if cat.age in ['青少年', '青年']:
                chance = randint(0, 50)
            elif cat.age in ['成年', '中年']:
                chance = randint(0, 70)
            else:
                chance = randint(0, 90)
            if chance == 1:
                cat.specialty2 = choice([choice(scars1), choice(scars2)])
                if cat.specialty2 == 'NOTAIL':
                    game.cur_events_list.append(str(cat.name) + ' 因为' + choice(
                        ['泼皮猫', '狗', '狐狸', '水獭', '家鼠', '鹰', '树', '獾', '敌族武士']) + '失去了尾巴')
                else:
                    game.cur_events_list.append(str(cat.name) + ' 因为' + choice(
                        ['泼皮猫', '狗', '狐狸', '水獭', '家鼠', '鹰', '树', '獾', '敌族武士']) + '留下了一道疤')
            else:
                cat.specialty2 = None

    def create_interactions(self, cat, index, key_copy):
        if randint(1, 50) == 49:
            # interact with other cat
            append_str = None
            # check if cat is dead
            if randint(1, 4) == 4:
                cat_number = key_copy[randint(0, index)]
            else:
                cat_number = key_copy[index - randint(1, index)]

            if self.all_cats[cat_number].dead:
                if randint(1, 4) == 4:
                    append_str = str(cat.name) + ' 正在为 ' + str(
                        self.all_cats[cat_number].name + '的离去而哀悼')
            elif cat_number == cat.ID:
                append_str = str(cat.name) + ' 认为他们真是疯了'
            else:
                # all other interactions here
                event_choice = randint(1, 6)
                if event_choice == 1:
                    if cat.specialty is None:
                        if cat.age in ['青少年', '青年']:
                            i = randint(0, 1)
                        elif cat.age in ['成年', '中年']:
                            i = randint(0, 2)
                        else:
                            i = randint(0, 10)
                        if i == 1:
                            cat.specialty = choice([choice(scars1), choice(scars2)])
                            if cat.age in ['幼崽']:
                                append_str = str(cat.name) + ' 在溜出营地时受伤了'
                            else:
                                if randint(1, 3) == 3 and (
                                        cat.status == '武士' or cat.status == '副族长'):
                                    append_str = str(
                                        cat.name) + ' 在保护 ' + str(
                                        self.all_cats[cat_number].name + ' 时受伤，加入了长老的行列')
                                    cat.status_change('长老')
                                else:
                                    append_str = str(cat.name) + ' 为了保护 ' + str(
                                        self.all_cats[cat_number].name) + ' 不被 ' + choice(
                                        ['rogue', 'dog', 'fox', 'otter', 'rat', 'hawk']) + ' 伤害时留下了一道疤'
                        else:
                            cat.specialty = None
                            append_str = str(cat.name) + ' 试图说服 ' + str(
                                self.all_cats[cat_number].name) + ' 一起溜出去'
                    elif cat.status != '幼崽':
                        cat.specialty = None
                        append_str = str(cat.name) + ' 试图说服 ' + str(
                            self.all_cats[cat_number].name) + ' 一起私奔'
                    elif game.clan.current_season != '秃叶季':
                        cat.specialty = None
                        append_str = str(cat.name) + ' 请求 ' + str(
                            self.all_cats[cat_number].name) + ' 向他们展示 ' + str(
                            game.clan.name) + 'Clan 营地'
                    else:
                        if game.clan.current_season == '秃叶季' and cat.status == '幼崽':
                            cat.dies()
                            append_str = str(cat.name) + '  在暴风雪中死于寒冷.'
                        else:
                            append_str = str(cat.name) + '  怅然若失'

                # defends
                elif event_choice == 2:
                    if cat.status == '族长':
                        append_str = str(cat.name) + ' 向 ' + str(self.all_cats[
                                                                     cat_number].name) + ' 承认族长肩负着沉重的责任'
                    elif game.clan.current_season == '秃叶季' and cat.status == '幼崽':
                        cat.dies()
                        append_str = str(self.all_cats[cat_number].name) + ' 发现 ' + str(
                            cat.name) + ' 在雪中离去了'
                    # sus
                elif event_choice == 3:
                    if cat.mate is not None and randint(1, 3) == 1:
                        append_str = str(cat.name) + ' 被 ' + str(
                            self.all_cats[cat_number].name) + ' 在一场关于 ' + str(
                            self.all_cats[cat.mate].name + ' 的争吵中杀死了')
                        cat.dies()
                    elif cat.mate is not None:
                        append_str = str(cat.name) + ' 与 ' + str(
                            self.all_cats[cat.mate].name + ' 分手了')
                        self.all_cats[cat.mate].mate = None
                        cat.mate = None
                    else:
                        valid_mates = 0
                        if not self.all_cats[cat_number].dead and self.all_cats[cat_number].age in [
                            '青年', '成年', '中年', '长老'] and \
                                cat != self.all_cats[cat_number] and cat.ID not in [
                            self.all_cats[cat_number].parent1, self.all_cats[cat_number].parent2] and \
                                self.all_cats[cat_number].ID not in [cat.parent1, cat.parent2] and \
                                self.all_cats[cat_number].mate is None and \
                                (self.all_cats[cat_number].parent1 is None or self.all_cats[
                                    cat_number].parent1 not in [cat.parent1, cat.parent2]) and \
                                (self.all_cats[cat_number].parent2 is None or self.all_cats[
                                    cat_number].parent2 not in [cat.parent1, cat.parent2]):

                            # Making sure the ages are appropriate
                            if (cat.age in ['中年', '长老'] and self.all_cats[cat_number].age in [
                                '中年', '长老']) or (self.all_cats[
                                                     cat_number].age != '长老' and cat.age != '长老' and cat.age != '幼崽' and cat.age != '青少年'):
                                valid_mates = 1

                        if self.all_cats[cat_number].ID == cat.ID:
                            valid_mates = 0

                        if valid_mates:
                            cat.mate = self.all_cats[cat_number].ID
                            self.all_cats[cat_number].mate = cat.ID
                            append_str = str(cat.name) + ' 和 ' + str(
                                self.all_cats[cat_number].name) + ' 结为伴侣'

                        else:
                            append_str = str(cat.name) + ' 和 ' + str(
                                self.all_cats[cat_number].name) + ' 谈论爱'

                    # angry mate
                elif event_choice == 4:
                    # training
                    if cat.status == '学徒':
                        append_str = str(cat.name) + ' 和他的导师 ' + str(cat.mentor.name + ' 一起训练')
                    elif cat.age in ['青少年', '青年', '成年', '中年']:
                        append_str = str(cat.name) + ' 从 ' + str(
                            self.all_cats[cat_number].name + ' 那里学到了些新动作')
                    else:
                        append_str = str(cat.name) + ' 和 ' + str(
                            self.all_cats[cat_number].name + ' 偷偷溜出营地')

                elif event_choice == 5:

                    # if cat has mate adopts kit, otherwise two invite in new cat
                    if randint(1, 4) < 4 and cat.status != '幼崽':
                        kit = Cat(moons=0)
                        game.clan.add_cat(kit)
                        append_str = str(cat.name) + ' 收养了一只名叫 ' + str(kit.name) + ' 的幼崽'
                    else:
                        kit = Cat(status='武士', moons=14)
                        game.clan.add_cat(kit)
                        append_str = str(cat.name) + ' 邀请了一只名为 ' + choice(
                            names.loner_names) + ' 的独行猫想要加入族群，他随即更名为 ' + str(kit.name) + ''
                        kit.skill = '前独行猫'

                elif event_choice == 6:
                    append_str = str(cat.name) + ' 和 ' + str(
                        self.all_cats[cat_number].name) + ' 死于传染病'
                    cat.dies()
                    self.all_cats[cat_number].dies()
                else:
                    append_str = str(cat.name) + ' 与 ' + str(
                        self.all_cats[cat_number].name + ' 互动')

            if game.cur_events_list is not None and append_str is not None and append_str != '':
                game.cur_events_list.append(append_str)
            else:
                game.cur_events_list = [append_str]

    def create_interactions2(self, cat):
        if randint(1, 50) == 1:
            interactions = []
            other_cat = self.all_cats.get(choice(list(self.all_cats.keys())))
            while cat == other_cat or other_cat.dead:
                other_cat = self.all_cats.get(choice(list(self.all_cats.keys())))
            name = str(cat.name)
            other_name = str(other_cat.name)
            event = choice([1, 1, 2])  # 1:general event 2:new cat joins
            if event == 1:
                if cat.status == '幼崽':
                    interactions.extend([name + ' 偷偷溜出营地后被训斥了',
                                         name + ' 失足跌下河后被 ' + other_name + ' 救了上来'])
                elif cat.status in ['学徒', '巫医学徒']:
                    interactions.extend([name + ' 偷偷溜出营地后被训斥了',
                                         name + ' 失足跌下河后被 ' + other_name + ' 救了上来',
                                         name + ' 不小心闯入了另一个族群的营地'])
                elif cat.status == '武士':
                    interactions.extend([name + ' 在族群营地外被捉住了',
                                         name + ' 因为违反武士守则被捉住了',
                                         name + ' 失踪了好几天',
                                         name + ' 相信自己是新预言的一部分'])
                elif cat.status == '巫医':
                    interactions.extend(
                        [name + ' 得知了一个新预言', name + ' 很担心绿咳症的爆发',
                         name + ' 因为缺少药草储存而担心',
                         name + ' 在拜访其他的巫医'])
                elif cat.status == '副族长':
                    interactions.extend([name + ' 在考虑退居长老巢穴',
                                         name + ' 给其他族群带去一则重要的信息'])
                elif cat.status == '族长':
                    interactions.extend(
                        [name + ' 在考虑退居长老巢穴', name + ' 承认他不剩几条命了',
                         name + ' 为了宣布重要的信息召开族群大会'])
                elif cat.status == '长老':
                    interactions.extend([name + ' 在迷路后被带回了营地'])
                if cat.age == other_cat.age:
                    interactions.extend([name + ' 试图说服 ' + other_name + ' 一起私奔'])
                if cat.mate == other_cat.ID:
                    if choice([1, 2, 3, 4]) == 1:
                        cat.mate = None
                        other_cat.mate = None
                        game.cur_events_list.append(name + ' 和 ' + other_name + ' 分手了')
                        return
                if cat.status not in ['幼崽', '学徒'] and other_cat.status not in ['幼崽',
                                                                               '学徒'] and cat.ID not in [
                    other_cat.parent1, other_cat.parent2] and other_cat.ID not in [cat.parent1,
                                                                                   cat.parent2] and cat.mate is None and other_cat.mate is None and cat.age == other_cat.age:
                    cat.mate = other_cat.ID
                    other_cat.mate = cat.ID
                    game.cur_events_list.append(name + ' 和 ' + other_name + ' 结为伴侣')
                    return
            elif event == 2:
                if cat.age != '幼崽':
                    type_of_new_cat = choice([1, 1, 2, 3, 4, 5, 6])
                    if type_of_new_cat == 1:
                        kit = Cat(moons=0)
                        game.clan.add_cat(kit)
                        game.cur_events_list.extend([name + ' 找到一只被遗弃的幼崽，并为他更名 ' + str(kit.name)])
                    elif type_of_new_cat == 2:
                        loner_name = choice(names.loner_names)
                        loner = Cat(prefix=loner_name, gender=choice(['雌性', '雄性']), status='武士',
                                    moons=randint(12, 120), suffix='')
                        game.clan.add_cat(loner)
                        game.cur_events_list.extend([name + ' 遇见一只名为 ' + str(
                            loner.name) + ' 的独行猫加入族群，他决定保留自己的名字'])
                    elif type_of_new_cat == 3:
                        loner = Cat(status='武士', moons=randint(12, 120))
                        game.clan.add_cat(loner)
                        game.cur_events_list.extend([name + ' 遇见一只名为 ' + choice(
                            names.loner_names) + ' 的独行猫想要加入族群。他随即更名为 ' + str(
                            loner.name)])
                    elif type_of_new_cat == 4:
                        warrior = Cat(status='武士', moons=randint(12, 150))
                        game.clan.add_cat(warrior)
                        game.cur_events_list.extend(
                            [name + ' 遇见一只来自 ' + choice(names.normal_prefixes) + 'Clan，名为 ' + str(
                                warrior.name) + ' 的武士，他想要加入族群'])
                    elif type_of_new_cat == 5:
                        loner_name = choice(names.loner_names)
                        loner = Cat(prefix=loner_name, gender=choice(['雌性', '雄性']), status='武士',
                                    moons=randint(12, 120), suffix='')
                        game.clan.add_cat(loner)
                        game.cur_events_list.extend(
                            [name + ' 遇见一只名为 ' + str(
                                loner_name) + ' 的宠物猫想要加入族群，他决定保留自己的名字'])
                    elif type_of_new_cat == 6:
                        loner = Cat(status='武士', moons=randint(12, 120))
                        game.clan.add_cat(loner)
                        game.cur_events_list.extend([name + ' finds a kittypet named ' + choice(
                            names.loner_names) + ' who wants to join the clan. They change their name to ' + str(
                            loner.name)])

            if len(interactions) > 0:
                game.cur_events_list.append(choice(interactions))

    def handle_deaths(self, cat):
        if randint(1, 300) == 1:
            if randint(1, 4) == 4:
                cat.dies()
                if game.cur_events_list is not None:
                    game.cur_events_list.append(
                        str(cat.name) + ' 在' + str(cat.moons) + '个月龄时被谋杀了')
            elif randint(1, 3) == 3:
                cat.dies()
                if game.cur_events_list is not None:
                    game.cur_events_list.append(
                        str(cat.name) + ' 在' + str(cat.moons) + '个月龄时因染上绿咳症去世了')
            else:
                cat.dies()
                if game.cur_events_list is not None:
                    game.cur_events_list.append(
                        str(cat.name) + ' 在' + str(cat.moons) + ' 个月龄时因意外去世了')

        if cat.moons > randint(150, 200):  # Cat dies of old age
            if choice([1, 2, 3, 4, 5, 6]) == 1:
                cat.dies()
                if game.cur_events_list is not None:
                    game.cur_events_list.append(
                        str(cat.name) + ' 在' + str(cat.moons) + ' 个月龄时加入了星族')

    def dies(self):  # This function is called every time a cat dies
        self.dead = True
        self.update_mentor()
        for app in self.apprentice:
            app.update_mentor()
        game.clan.add_to_starclan(self)

    def have_kits(self):
        # decide chances of having kits, and if it's possible at all
        chance = 0
        if self.mate is not None:
            if self.mate in self.all_cats:
                if self.all_cats[self.mate].dead:
                    chance = 0
                elif self.all_cats[self.mate].gender != self.gender and self.all_cats[
                    self.mate].age != '长老':
                    chance = 25
                elif game.settings['no gendered breeding'] and self.all_cats[
                    self.mate].age != '长老' and chance is not None:
                    chance = 25
                else:
                    chance = 0
            else:
                game.cur_events_list.append(
                    "警告: " + str(self.name) + " 不能与 #" + str(self.mate) + "结为伴侣")
                self.mate = None
        else:
            chance = 50
            if not game.settings['no unknown fathers']:
                chance = 0

        if self.age in ['幼崽', '青少年', '长老'] or self.example or \
                (not game.settings['no gendered breeding'] and self.gender == '雄性'):
            chance = 0

        # Decide randomly if kits will be born, if possible
        if chance != 0:
            hit = randint(0, chance)
            if len(game.clan.clan_cats) > 30:
                hit = randint(0, chance + 20)
            elif len(game.clan.clan_cats) < 10:
                hit = randint(0, chance - 10)
            kits = choice([1, 1, 2, 2, 3, 3, 4])
            if hit == 1 and self.mate is not None:
                if game.cur_events_list is not None:
                    game.cur_events_list.append(str(self.name) + ' 拥有了' + str(kits) + '只幼崽')
                else:
                    game.cur_events_list = [str(self.name) + ' 拥有了' + str(kits) + '只幼崽']

                for kit in range(kits):
                    kit = Cat(parent1=self.ID, parent2=self.mate, moons=0)
                    game.clan.add_cat(kit)
            elif hit == 1:
                game.cur_events_list.append(str(self.name) + ' 拥有了' + str(kits) + '只幼崽')

                for kit in range(kits):
                    kit = Cat(parent1=self.ID, moons=0)
                    game.clan.add_cat(kit)

    def thoughts(self):
        # actions or thoughts for all cats. These switch either every moon or every time the game is re-opened

        for c in self.all_cats.keys():
            other_cat = random.choice(list(self.all_cats.keys()))
            while other_cat == c:
                other_cat = random.choice(list(self.all_cats.keys()))
            other_cat = self.all_cats.get(other_cat)
            other_name = str(other_cat.name)
            cat = self.all_cats.get(c)
            thought = '没什么想法'  # placeholder thought - should never appear in game
            if cat.dead:
                # individual thoughts
                starclan_thoughts = ['感觉懒洋洋的', '花了很多时间打理毛发',
                                     '盼望着今天的到来', '感到沮丧...',
                                     '感到很开心！', '对其他族群感到好奇', '感觉今天活力四射！',
                                     "正在思考要传达的消息", "希望自己仍旧活着",
                                     "欣赏星族的领地", "思考自己的一生",
                                     "正思念着至亲",
                                     "希望尽快与巫医见面", "欣赏自己皮毛间的星辰",
                                     "观看一个族群仪式", "希望自己能赐予新族长一条命",
                                     "希望自己能被铭记", "正在观察族群",
                                     "有些担心族群",
                                     "在日光下放松", "有些担心两脚兽",
                                     "思考自己的古代先祖",
                                     "有些担心黑森林里的猫",
                                     "正在思考要传递给巫医的建议"]
                if other_cat.dead:
                    starclan_thoughts.extend([  # thoughts with other cats that are dead
                        '正在与 ' + other_name + ' 分享舌头',
                        '最近一直和 ' + other_name + ' 在一起',
                        '对 ' + other_name + ' 很生气',
                        '与 ' + other_name + ' 分享新鲜猎物',
                        '对 ' + other_name + ' 很好奇',
                        '正在和 ' + other_name + ' 交谈',
                        '不想和 ' + other_name + ' 讲话',
                        '与 ' + other_name + ' 发生了严重的争执',
                        '想和 ' + other_name + ' 黏在一起!',
                        '与 ' + other_name + ' 一起思考未来的预言',
                        '与  ' + other_name + ' 一起注视着族群'])
                elif not other_cat.dead:
                    starclan_thoughts.extend([  # thoughts with other cats that are alive
                        '正在注视着 ' + other_name,
                        '好奇 ' + other_name + ' 此时在做些什么',
                        '想要给 ' + other_name + ' 传递信息',
                        '在 ' + other_name + ' 的梦中漫步',
                        '为 ' + other_name + ' 感到骄傲',
                        '对 ' + other_name + ' 很失望',
                        '想要警告 ' + other_name,
                        '一直在关注 ' + other_name + ' 的成长'])
                if cat.status in ['幼崽', '学徒', '巫医学徒']:  # dead young cat thoughts
                    starclan_thoughts.extend(['希望自己有更多时间长大',
                                              '想知道自己的名号会是什么',
                                              '正在打搅星族的老猫',
                                              '正在了解星族的其他猫'])
                elif cat.status == '长老':  # dead elder thoughts
                    starclan_thoughts.extend(['很庆幸自己能度过如此长的一生',
                                              '为自己的关节不再疼痛而高兴',
                                              '正在给年轻的星族猫讲故事',
                                              '看护着年轻的星族猫', ])
                elif cat.status == '族长':  # dead leader thoughts
                    starclan_thoughts.extend(['希望自己是个好族长,'
                                              '希望自己能有十条命',
                                              '为自己来自星族感到骄傲', ])
                thought = choice(starclan_thoughts)  # sets current thought to a random applicable thought
            elif not cat.dead:
                # general individual thoughts
                thoughts = ['感觉懒洋洋的', '花了相当多时间打理毛发',
                            '期待今天将要发生的事', '感到沮丧...', '感到很兴奋',
                            '感到很紧张', '非常满足', "在营地中放松", '正在做白日梦',
                            '正在打盹', '感觉自己要疯了', '有些忧郁', "正在环顾营地",
                            '感到很开心！', '对其他族群很好奇', '感觉今天活力四射',
                            '今天只想单独呆着', "正在吃新鲜猎物",
                            '正前往厕所', '重新思考自己的猫生选择',
                            '拜访巫医巢穴', '度过了美好的一天', '度过了艰难的一天',
                            '正在自言自语', '后悔没有早点吃猎物堆上的鸟']
                if other_cat.dead:  # thoughts with other cats who are dead
                    if cat.status in ['幼崽', '学徒',
                                      '巫医学徒']:  # young cat thoughts about dead cat
                        thoughts.extend(['正在聆听 ' + other_name + ' 的故事',
                                         '想要更加了解 ' + other_name,
                                         '因为不能继续和 ' + other_name + ' 呆在一起而感到难过'])
                    elif cat.status in ['武士', '巫医', '副族长',
                                        '族长']:  # older cat thoughts about dead cat
                        thoughts.extend(['正在聆听 ' + other_name + ' 的故事',
                                         '想要更加了解 ' + other_name,
                                         '因为不能继续和 ' + other_name + ' 呆在一起而感到难过',
                                         '希望能去星族拜访 ' + other_name,
                                         '正在想念 ' + other_name])
                    if cat.status == '长老':  # elder thoughts about dead cat
                        thoughts.extend(['正在讲 ' + other_name + ' 的故事',
                                         '因为不能继续和 ' + other_name + ' 呆在一起而感到难过',
                                         '希望能去星族拜访 ' + other_name,
                                         '正在想念 ' + other_name,
                                         '希望 ' + other_name + ' 仍然活着',
                                         '找到一个曾经属于 ' + other_name + ' 的小玩意儿',
                                         '已经忘记 ' + other_name + ' 是谁了',
                                         '正深情地想着 ' + other_name])
                    if cat.status == '巫医' or cat.status == '巫医学徒' or cat.skill == '与星族有紧密的联系':  # medicine cat/strong connection thoughts about dead cat
                        thoughts.extend(['收到 ' + other_name + ' 给予的预言',
                                         '收到 ' + other_name + ' 给予的预兆',
                                         '梦见 ' + other_name + ' 指引了自己',
                                         '被 ' + other_name + ' 拜访了',
                                         '感受到 ' + other_name + ' 正在附近',
                                         '在梦中遇见 ' + other_name + ' , 正在警告自己......一些事情',
                                         '向 ' + other_name + ' 请求帮助'])
                elif not other_cat.dead:  # thoughts with other cat who is alive
                    if cat.status in ['武士', '长老', '副族长',
                                      '族长'] and other_cat.status == '学徒':  # older cat thoughts about younger cat
                        thoughts.extend(['正在给 ' + other_name + ' 一些建议',
                                         '正在给 ' + other_name + ' 讲述一种狩猎技巧',
                                         '正在责骂 ' + other_name,
                                         '交给 ' + other_name + ' 一个任务'])
                    if cat.status == '幼崽':  # kit thoughts
                        if other_cat.status == '幼崽':  # kit thoughts with other kit
                            thoughts.extend(['和 ' + other_name + ' 一起假装自己是一个武士',
                                             '和 ' + other_name + ' 一起玩苔藓球',
                                             '与 ' + other_name + ' 模拟战斗',
                                             '与 ' + other_name + ' 一起计划偷偷溜出营地',
                                             '正在抱怨 ' + other_name])
                        elif other_cat.status != '幼崽':  # kit thoughts about older cat
                            thoughts.extend(
                                ['正咬着 ' + other_name + ' 的尾巴', '把舌头伸向 ' + other_name,
                                 '对 ' + other_name + ' 发牢骚'])
                    elif cat.status in ['学徒', '巫医学徒', '武士', '巫医', '副族长',
                                        '族长']:
                        if other_cat.status == '幼崽':  # older cat thoughts about kit
                            thoughts.extend(['绊倒了 ' + other_name, '正在给 ' + other_name + ' 提建议'])
                        else:
                            thoughts.extend(['和 ' + other_name + ' 打架', '与 ' + other_name + ' 交谈',
                                             '与 ' + other_name + ' 分享猎物', '听到关于 ' + other_name + ' 的传言'])
                    if cat.age == other_cat.age:
                        thoughts.extend(
                            ['对 ' + other_name + ' 产生好感', '花很多时间与 ' + other_name + ' 相处'])
                if cat.status == '幼崽':
                    thoughts.extend(['自己玩苔藓球', '正在打扰长老们',
                                     '想知道自己的名号会是什么', '假装自己是个武士',
                                     '开始对草药感兴趣', '试图偷偷溜出营地',
                                     '在地上打滚', '追自己的尾巴玩',
                                     '正在玩一根棍子', '对自己的学徒仪式感到紧张',
                                     '对自己的学徒仪式感到兴奋', '好奇自己的导师会是谁',
                                     "练习打猎的蹲姿", '假装与敌族武士战斗',
                                     '想去打个盹', '做了个噩梦后很害怕',
                                     '认为自己在梦中遇见了一只星族猫', '想与其他猫依偎在一起',
                                     '希望其他猫别再把自己当小幼崽', '正在躲避其他猫',
                                     '兴奋地蹦蹦跳跳', '抱怨自己的肚子空空'])
                elif cat.status == '学徒':
                    thoughts.extend(
                        ['正在回想他们抓到一只肥兔子的时候', '想知道自己的名号会是什么',
                         '正在刺激自己的导师',
                         '正在和导师争吵', '正在聆听自己的导师讲话',
                         '想去拜访长老巢穴', "练习打猎技巧",
                         '假装与敌族武士战斗', '练习战斗技巧',
                         '开始对草药感兴趣', '自愿参加黎明巡逻队',
                         '自愿去采集草药', '希望能尽快参加战斗训练',
                         '正在对武士们恶作剧', '迫不及待地想成为一名武士',
                         '想知道自己是否足以成为武士', '正在采集苔藓',
                         '还不想成为一名武士', '正在说闲话', '表现得很焦虑'])
                elif cat.status == '巫医学徒':
                    thoughts.extend(
                        ['正在努力记住所有药草的名字', '正在数罂粟籽',
                         '正在帮忙整理药草储存', '想知道自己的名号会是什么',
                         '计划帮长老们处理他们的虱子', '期待着月半集会',
                         '想知道自己是否足以成为巫医',
                         '给一道小伤口上药', '正在制作新巢穴',
                         '为自己有能力照顾族猫而感到自豪'])
                elif cat.status == '巫医':
                    thoughts.extend(
                        ['正在寻找药草', '正在整理药草储存', '正在晒干药草',
                         '正在数罂粟籽', '正在收集蜘蛛网', '正在解析一个预兆',
                         '正在解析一个预言', '希望不久后能收到星族的指引',
                         '正在检查武士们的状态', '在照顾族群时感到有压力',
                         '正在考虑收一个新的学徒',
                         '想知道是否能从别的族群借到一些猫薄荷',
                         '期待着月半集会', '正在用蜘蛛网包扎伤口',
                         '在清理旧药草', '正在收集死亡浆果',
                         '为自己有能力照顾族猫而感到自豪', '把幼崽从自己的巢穴中赶出去'])
                elif cat.status == '武士':
                    thoughts.extend(
                        ['早些时候闻到了狐狸的气味', '早些时候闻到了别族武士的气味',
                         '帮忙采集药草', '正在思考爱情', '正在装饰自己的巢穴',
                         '正在用荆棘加固营地', '想被选为新的副族长',
                         '抓到一只肥兔子', '梦想成为族长', '表现得很可疑',
                         '试图为年轻猫们树立一个好榜样', '想加入巡逻队',
                         '想加入狩猎队', '希望能带领下一个巡逻队',
                         '正在守卫营地入口', '正在思考幼崽', '正在照看幼崽',
                         '正在说闲话', '计划去拜访巫医'])
                elif cat.status == '副族长':
                    thoughts.extend(
                        ['正在分配边境巡逻队', '正在分配狩猎队',
                         '想知道成为族长会是什么样子', '独自呆着',
                         '试图为年轻猫们树立一个好榜样', '正在思考幼崽',
                         '组织巡逻队时感到有压力', "想知道谁会赐予自己九条命"])
                elif cat.status == '族长':
                    thoughts.extend(
                        ['希望能看见来自星族的征兆', '希望自己能很好地领导族群',
                         '思考谁会成为新学徒的导师', '担心族群关系',
                         '正在独处', '试图为副族长树立一个好榜样',
                         '考虑是否组成一个联盟',
                         '正在争论是否应该和另一个族群宣战', '正在评估一些学徒',
                         '正在思考战斗策略', '几乎失去一条命',
                         '计算自己还剩几条命'])
                elif cat.status == '长老':
                    thoughts.extend(
                        ['抱怨自己的巢穴太粗糙', '抱怨自己疼痛的关节',
                         '讲述自己年轻时的故事', '给年轻猫提供建议',
                         '抱怨自己的窝里有刺', '对年轻猫颐指气使',
                         '给年轻猫讲鬼故事', '正在打着呼噜睡觉',
                         '怀念那些在过于年轻时就离去的猫', '抱怨最近的天气变得寒冷',
                         '庆幸自己活了这么久', '正在分享自己的智慧'])
                thought = choice(thoughts)
            cat.thought = thought

            # on_patrol = ['Is having a good time out on patrol', 'Wants to return to camp to see ' + other_name,
            #              'Is currently out on patrol', 'Is getting rained on during their patrol',
            #              'Is out hunting'] //will add later
            # interact_with_loner = ['Wants to know where ' + other_name + ' came from.'] // will add

    def status_change(self, new_status):
        # revealing of traits and skills
        if self.status == '幼崽':
            self.trait = choice(self.traits)
        if (self.status == '学徒' and new_status != '巫医学徒') or (
                self.status == '巫医学徒' and new_status != '学徒'):
            self.skill = choice(self.skills)

        self.status = new_status
        self.name.status = new_status
        if '学徒' in new_status:
            self.update_mentor()
        # update class dictionary
        self.all_cats[self.ID] = self

    def is_valid_mentor(self, potential_mentor):
        # dead cats can't be mentors
        if potential_mentor.dead:
            return False
        # Match jobs
        if self.status == '巫医学徒' and potential_mentor.status != '巫医':
            return False
        if self.status == '学徒' and potential_mentor.status not in ['族长', '副族长', '武士']:
            return False
        # If not an app, don't need a mentor
        if '学徒' not in self.status:
            return False
        # dead cats don't need mentors
        if self.dead:
            return False
        return True

    def update_mentor(self, new_mentor=None):
        if new_mentor is None:
            # If not reassigning and current mentor works, leave it
            if self.mentor and self.is_valid_mentor(self.mentor):
                return
        old_mentor = self.mentor
        # Should only have mentor if alive and some kind of apprentice
        if '学徒' in self.status and not self.dead:
            # Need to pick a random mentor if not specified
            if new_mentor is None:
                potential_mentors = []
                priority_mentors = []
                for cat in self.all_cats.values():
                    if self.is_valid_mentor(cat):
                        potential_mentors.append(cat)
                        if len(cat.apprentice) == 0:
                            priority_mentors.append(cat)
                # First try for a cat who currently has no apprentices
                if len(priority_mentors) > 0:
                    new_mentor = choice(priority_mentors)
                elif len(potential_mentors) > 0:
                    new_mentor = choice(potential_mentors)
            # Mentor changing to chosen/specified cat
            self.mentor = new_mentor
            if new_mentor is not None:
                if self not in new_mentor.apprentice:
                    new_mentor.apprentice.append(self)
                if self in new_mentor.former_apprentices:
                    new_mentor.former_apprentices.remove(self)
        else:
            self.mentor = None
        # Move from old mentor's apps to former apps
        if old_mentor is not None and old_mentor != self.mentor:
            if self in old_mentor.apprentice:
                old_mentor.apprentice.remove(self)
            if self not in old_mentor.former_apprentices:
                old_mentor.former_apprentices.append(self)
            if old_mentor not in self.former_mentor:
                self.former_mentor.append(old_mentor)

    def update_sprite(self):
        # First make pelt, if it wasn't possible before

        if self.pelt is None:
            if self.parent1 is None:
                # If pelt has not been picked manually, this function chooses one based on possible inheritances
                self.pelt = choose_pelt(self.gender)

            elif self.parent2 is None and self.parent1 in self.all_cats.keys():
                # 1 in 3 chance to inherit a single parent's pelt
                par1 = self.all_cats[self.parent1]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, None]),
                                        choice([par1.pelt.white, None]),
                                        choice([par1.pelt.name, None]),
                                        choice([par1.pelt.length, None]))

            elif self.parent1 in self.all_cats.keys() and self.parent2 in self.all_cats.keys():
                # 2 in 3 chance to inherit either parent's pelt
                par1 = self.all_cats[self.parent1]
                par2 = self.all_cats[self.parent2]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, par2.pelt.colour, None]),
                                        choice([par1.pelt.white, par2.pelt.white, None]),
                                        choice([par1.pelt.name, par2.pelt.name, None]),
                                        choice([par1.pelt.length, par2.pelt.length, None]))
            else:
                self.pelt = choose_pelt(self.gender)

        # THE SPRITE UPDATE
        # draw colour & style
        new_sprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

        if self.pelt.name not in ['Tortie', 'Calico']:
            if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                               '巫医学徒'] or self.age == '长老':
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + 'extra' + self.pelt.colour + str(
                        self.age_sprites[self.age])], (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + self.pelt.colour + str(self.age_sprites[self.age])],
                    (0, 0))
        else:
            if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                               '巫医学徒'] or self.age == '长老':
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + 'extra' + self.pattern + str(self.age_sprites[self.age])], (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + self.pattern + str(self.age_sprites[self.age])],
                    (0, 0))

        # draw white patches
        if self.white_patches is not None:
            if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                               '巫医学徒'] or self.age == '长老':
                new_sprite.blit(
                    sprites.sprites['whiteextra' + self.white_patches + str(self.age_sprites[self.age])],
                    (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites['white' + self.white_patches + str(self.age_sprites[self.age])], (0, 0))

        # draw eyes & scars1
        if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                           '巫医学徒'] or self.age == '长老':
            if self.specialty in scars1:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars1:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))
            new_sprite.blit(sprites.sprites['eyesextra' + self.eye_colour + str(self.age_sprites[self.age])],
                            (0, 0))
        else:
            if self.specialty in scars1:
                new_sprite.blit(sprites.sprites['scars' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars1:
                new_sprite.blit(sprites.sprites['scars' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))
            new_sprite.blit(sprites.sprites['eyes' + self.eye_colour + str(self.age_sprites[self.age])], (0, 0))

        # draw line art
        if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                           '巫医学徒'] or self.age == '长老':
            new_sprite.blit(sprites.sprites['lines' + str(self.age_sprites[self.age] + 9)], (0, 0))
        else:
            new_sprite.blit(sprites.sprites['lines' + str(self.age_sprites[self.age])], (0, 0))

        # draw skin and scars2 and scars3
        if self.pelt.length == '长毛' and self.status not in ['幼崽', '学徒',
                                                           '巫医学徒'] or self.age == '长老':
            new_sprite.blit(sprites.sprites['skinextra' + self.skin + str(self.age_sprites[self.age])], (0, 0))
            if self.specialty in scars2:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars2:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty in scars3:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars3:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))
        else:
            new_sprite.blit(sprites.sprites['skin' + self.skin + str(self.age_sprites[self.age])], (0, 0))
            if self.specialty in scars2:
                new_sprite.blit(sprites.sprites['scars' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars2:
                new_sprite.blit(sprites.sprites['scars' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty in scars3:
                new_sprite.blit(sprites.sprites['scars' + self.specialty + str(self.age_sprites[self.age])],
                                (0, 0))
            if self.specialty2 in scars3:
                new_sprite.blit(sprites.sprites['scars' + self.specialty2 + str(self.age_sprites[self.age])],
                                (0, 0))

        # reverse, if assigned so
        if self.reverse:
            new_sprite = pygame.transform.flip(new_sprite, True, False)

        # apply
        self.sprite = new_sprite
        self.big_sprite = pygame.transform.scale(new_sprite, (sprites.new_size, sprites.new_size))
        self.large_sprite = pygame.transform.scale(self.big_sprite, (sprites.size * 3, sprites.size * 3))

        # update class dictionary
        self.all_cats[self.ID] = self

    def draw(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - sprites.size / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.size
        self.used_screen.blit(self.sprite, new_pos)

    def draw_big(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - sprites.new_size / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.new_size
        self.used_screen.blit(self.big_sprite, new_pos)

    def draw_large(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - sprites.size * 3 / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.size * 3
        self.used_screen.blit(self.large_sprite, new_pos)

    def save_cats(self):
        data = ''
        for x in self.all_cats.values():
            # cat ID -- name prefix : name suffix
            data += x.ID + ',' + x.name.prefix + ':' + x.name.suffix + ','
            # cat gender -- status -- age -- trait
            data += x.gender + ',' + x.status + ',' + str(x.age) + ',' + x.trait + ','
            # cat parent1 -- parent2 -- mentor
            if x.parent1 is None:
                data += 'None ,'
            else:
                data += x.parent1 + ','
            if x.parent2 is None:
                data += 'None ,'
            else:
                data += x.parent2 + ','
            if x.mentor is None:
                data += 'None ,'
            else:
                data += x.mentor.ID + ','

            # pelt type -- colour -- white -- length
            data += x.pelt.name + ',' + x.pelt.colour + ',' + str(x.pelt.white) + ',' + x.pelt.length + ','
            # sprite 幼崽 -- 青少年
            data += str(x.age_sprites['幼崽']) + ',' + str(x.age_sprites['青少年']) + ','
            # sprite 成年 -- 长老
            data += str(x.age_sprites['成年']) + ',' + str(x.age_sprites['长老']) + ','
            # eye colour -- reverse -- white patches -- pattern
            data += x.eye_colour + ',' + str(x.reverse) + ',' + str(x.white_patches) + ',' + str(x.pattern) + ','
            # skin -- skill -- NONE  -- specs  -- moons
            data += x.skin + ',' + x.skill + ',' + 'None' + ',' + str(x.specialty) + ',' + str(x.moons) + ','
            # mate -- dead  -- dead sprite
            data += str(x.mate) + ',' + str(x.dead) + ',' + str(x.age_sprites['死亡'])

            # scar 2
            data += ',' + str(x.specialty2)
            # experience
            data += ',' + str(x.experience)
            # dead_for x moons
            data += ',' + str(x.dead_for)
            # apprentice
            if x.apprentice:
                data += ','
                for cat in x.apprentice:
                    data += str(cat.ID) + ';'
                # remove last semicolon
                data = data[:-1]
            else:
                data += ',' + 'None'
            # former apprentice
            if x.former_apprentices:
                data += ','
                for cat in x.former_apprentices:
                    data += str(cat.ID) + ';'
                # remove last semicolon
                data = data[:-1]
            else:
                data += ',' + 'None'
            # next cat
            data += '\n'

        # remove one last unnecessary new line
        data = data[:-1]

        if game.switches['naming_text'] != '':
            clanname = game.switches['naming_text']
        elif game.switches['clan_name'] != '':
            clanname = game.switches['clan_name']
        else:
            clanname = game.switches['clan_list'][0]
        with open('saves/' + clanname + 'cats.csv', 'w') as write_file:
            write_file.write(data)

    def load_cats(self):
        if game.switches['clan_list'][0].strip() == '':
            cat_data = ''
        else:
            if os.path.exists('saves/' + game.switches['clan_list'][0] + 'cats.csv'):
                with open('saves/' + game.switches['clan_list'][0] + 'cats.csv', 'r') as read_file:
                    cat_data = read_file.read()
            else:
                with open('saves/' + game.switches['clan_list'][0] + 'cats.txt', 'r') as read_file:
                    cat_data = read_file.read()

        if len(cat_data) > 0:
            cat_data = cat_data.replace('\t', ',')
            for i in cat_data.split('\n'):
                # CAT: ID(0) - prefix:suffix(1) - gender(2) - status(3) - age(4) - trait(5) - parent1(6) - parent2(7)
                #  - mentor(8)
                # PELT: pelt(9) - colour(10) - white(11) - length(12)
                # SPRITE: 幼崽(13) - apprentice(14) - warrior(15) - 长老(16) - eye colour(17) - reverse(18)
                # - white patches(19) - pattern(20) - skin(21) - skill(22) - NONE(23) - spec(24) - moons(25) - mate(26)
                # dead(27) - SPRITE:dead(28)
                if i.strip() != '':
                    attr = i.split(',')
                    for x in range(len(attr)):
                        attr[x] = attr[x].strip()
                        if attr[x] in ['None', 'None ']:
                            attr[x] = None
                        elif attr[x].upper() == 'TRUE':
                            attr[x] = True
                        elif attr[x].upper() == 'FALSE':
                            attr[x] = False

                    the_pelt = choose_pelt(attr[2], attr[10], attr[11], attr[9], attr[12], True)
                    the_cat = Cat(ID=attr[0], prefix=attr[1].split(':')[0], suffix=attr[1].split(':')[1],
                                  gender=attr[2],
                                  status=attr[3], pelt=the_pelt, parent1=attr[6], parent2=attr[7], eye_colour=attr[17])
                    the_cat.age, the_cat.mentor = attr[4], attr[8]
                    the_cat.age_sprites['幼崽'], the_cat.age_sprites['青少年'] = int(attr[13]), int(attr[14])
                    the_cat.age_sprites['成年'], the_cat.age_sprites['长老'] = int(attr[15]), int(attr[16])
                    the_cat.age_sprites['青年'], the_cat.age_sprites['中年'] = int(attr[15]), int(
                        attr[15])
                    the_cat.reverse, the_cat.white_patches, the_cat.pattern = attr[18], attr[19], attr[20]
                    the_cat.trait, the_cat.skin, the_cat.specialty = attr[5], attr[21], attr[24]

                    if len(attr) > 29:
                        the_cat.specialty2 = attr[29]
                    else:
                        the_cat.specialty2 = None

                    if len(attr) > 30:
                        the_cat.experience = int(attr[30])
                        experiencelevels = ['非常低', '低', '略低', '平均', '较高', '高',
                                            '很高', '精通', '极致']
                        the_cat.experience_level = experiencelevels[math.floor(int(the_cat.experience) / 10)]

                    else:
                        the_cat.experience = 0

                    if len(attr) > 25:
                        # Attributes that are to be added after the update
                        the_cat.moons = int(attr[25])
                        if len(attr) >= 27:
                            # assigning mate to cat, if any
                            the_cat.mate = attr[26]
                        if len(attr) >= 28:
                            # Is the cat dead
                            the_cat.dead = attr[27]
                            the_cat.age_sprites['死亡'] = attr[28]
                    if len(attr) > 31:
                        the_cat.dead_for = int(attr[31])
                    the_cat.skill = attr[22]

                    if len(attr) > 32 and attr[32] is not None:
                        the_cat.apprentice = attr[32].split(';')
                    if len(attr) > 33 and attr[33] is not None:
                        the_cat.former_apprentices = attr[33].split(';')

            for n in self.all_cats.values():
                # Load the mentors and apprentices after all cats have been loaded
                n.mentor = cat_class.all_cats.get(n.mentor)
                apps = []
                former_apps = []
                for app_id in n.apprentice:
                    app = cat_class.all_cats.get(app_id)
                    # Make sure if cat isn't an apprentice, they're a former apprentice
                    if '学徒' in app.status:
                        apps.append(app)
                    else:
                        former_apps.append(app)
                for f_app_id in n.former_apprentices:
                    f_app = cat_class.all_cats.get(f_app_id)
                    former_apps.append(f_app)
                n.apprentice = apps
                n.former_apprentices = former_apps
                n.update_sprite()

    def load(self, cat_dict):
        """ A function that takes a dictionary containing other dictionaries with attributes and values of all(?)
         cats from a save file and redistributes the values onto new cat object attributes.
         The dict is in form:
         cat_dict = { ID : [(prefix, suffix), {attribute: value}] }"""
        for cat in cat_dict.keys():  # cat is the ID of the cats
            # create the cat object
            name = cat_dict[cat][0]
            new_cat = Cat(prefix=name[0], suffix=name[1], ID=cat)

            # put attribute dict into easier accessible variable
            attr_dict = cat_dict[cat][1]

            # go through attributes
            for attr in attr_dict.keys():
                value = attr_dict[attr]  # value of attribute
                # turn value into other forms than string if necessary
                if value == 'None':
                    value = None
                elif value == 'False':
                    value = False
                elif value == 'True':
                    value = True

                # Assign values to cat object
                if attr == 'status':
                    new_cat.status = value  # STATUS
                if attr == 'parent1':
                    new_cat.parent1 = value  # PARENT1
                if attr == 'parent2':
                    new_cat.parent2 = value  # PARENT2
                if attr == '性别':
                    new_cat.gender = value  # SEX / GENDER
                if attr == '个月':
                    new_cat.moons = int(value)  # MOONS
                if attr == '年龄':
                    new_cat.age = int(value)  # AGE
                if attr == '死亡':
                    new_cat.dead = value  # dead ( OR NOT )
                if attr == '死亡时间':
                    new_cat.dead_for = int(value)  # dead FOR ( MOONS )
                if attr == '皮毛':
                    new_cat.pelt = value  # PELT
                if attr == '眼睛颜色':
                    new_cat.eye_colour = value  # EYES
                if attr == '伴侣':
                    new_cat.mate = value  # MATE
                if attr == '特征':
                    new_cat.trait = value  # TRAIT
                if attr == '技能':
                    new_cat.skill = value  # SKILL
                if attr == '导师':
                    new_cat.mentor = value

    def describe_color(self):
        pelt_list = {'WHITE': '白色', 'PALEGREY': '浅灰色', 'SILVER': '银色', 'GREY': '灰色', 'DARKGREY': '暗灰色', 'BLACK': '黑色',
                     'PALEGINGER': '浅姜色', 'GOLDEN': '金色', 'GINGER': '姜色',
                     'DARKGINGER': '暗姜色', 'LIGHTBROWN': '亮棕色', 'BROWN': '棕色', 'DARKBROWN': '暗棕色'}
        color_name = ''
        if self.pelt.name == 'SingleColour' or self.pelt.name == 'TwoColour':
            color_name = pelt_list.get(str(self.pelt.colour))  # str(self.pelt.colour).lower()
        elif self.pelt.name == "Tabby":
            color_name = pelt_list.get(str(self.pelt.colour)) + ' 虎斑'
        elif self.pelt.name == "Speckled":
            color_name = pelt_list.get(str(self.pelt.colour)) + ' 点斑'
        elif self.pelt.name == "Tortie" or self.pelt.name == "Calico":
            color_name = '玳瑁'  # check for calico or for white later

        # not enough to comment on
        if self.white_patches is None or self.white_patches in ['EXTRA']:
            color_name = color_name  # what is this even lol
        # enough to comment but not make calico
        elif self.white_patches in ['LITTLE', 'LITTLECREAMY', 'LIGHTTUXEDO', 'BUZZARDFANG']:
            color_name = color_name + ' 和白色'
        # and white
        elif self.white_patches in ['ANY', 'TUXEDO', 'ANY2', 'ANYCREAMY', 'TUXEDOCREAMY', 'ANY2CREAMY', 'BROKEN']:
            if color_name == 'tortie':
                color_name = '三花'
            else:
                color_name = color_name + ' 和白色'
        # white and
        elif self.white_patches in ['VAN', 'VANCREAMY', 'ONEEAR', 'LIGHTSONG']:
            color_name = '白色和' + color_name
        # colorpoint
        elif self.white_patches in ['COLOURPOINT', 'RAGDOLL', 'COLOURPOINTCREAMY']:
            color_name = color_name + '重点'
            if color_name == '暗姜色重点':
                color_name = '火焰重点'
        # vitiligo
        elif self.white_patches in ['VITILIGO']:
            color_name = color_name + '和白斑'
        else:
            color_name = color_name + ' color error'

        if color_name == '玳瑁':
            color_name = '玳瑁'

        if color_name == '白色和白色':
            color = name = '白色'

        return color_name

    def describe_cat(self):
        if self.gender == '雄性':
            sex = '公猫'
        else:
            sex = '母猫'
        description = self.describe_color()
        description += ' ' + str(self.pelt.length) + '的' + sex
        return description


# CAT CLASS ITEMS
cat_class = Cat(example=True)
game.cat_class = cat_class

# The randomized cat sprite in Main Menu screen
example_cat = Cat(status=choice(["幼崽", "学徒", "武士", "长老"]), example=True)
example_cat.update_sprite()


# Twelve example cats
def example_cats():
    e = random.sample(range(12), 2)
    for a in range(12):
        if a in e:
            game.choose_cats[a] = Cat(status='武士')
        else:
            game.choose_cats[a] = Cat(status=choice(['幼崽', '学徒', '武士', '武士', '长老']))
        game.choose_cats[a].update_sprite()
