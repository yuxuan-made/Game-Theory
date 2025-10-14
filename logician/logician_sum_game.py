import numpy as np
from typing import List, Tuple, Set, Dict

class Logician:
    '''
    A logician has his/her own number, but he/she doesn't know.
    There are 3 logicians, and each of them can see the other two's numbers.
    One logician's number is the sum of the other two's numbers.
    The numbers are all positive integers (greater than 0), and they know that.
    '''
    def __init__(self, logician_id: int, others_numbers: List[int]) -> None:
        '''
        logician_id: 逻辑学家的ID (0, 1, 2)
        others_numbers: 看到的其他两个逻辑学家的数字 [int, int]
        '''
        self.logician_id = logician_id
        self.others_numbers = others_numbers
        self.possible_numbers = self._calculate_possible_numbers()
        
    def _calculate_possible_numbers(self) -> Set[int]:
        '''计算自己可能的数字'''
        a, b = self.others_numbers
        possibilities = set()
        
        # 自己可能是两者的和
        possibilities.add(a + b)
        
        # 自己可能是两者的差的绝对值（当两数不相等时）
        if a != b:
            possibilities.add(abs(a - b))
            
        return possibilities
    
    def can_deduce_immediately(self) -> bool:
        '''
        边界条件1：立即推断
        如果看到的两个数字相等，则立即知道自己是两者的和
        '''
        return self.others_numbers[0] == self.others_numbers[1]
    
    def knows_answer(self) -> bool:
        '''判断是否知道答案（只有一个可能）'''
        return len(self.possible_numbers) == 1


class LogicianSumGame:
    '''
    三个逻辑学家数字游戏的完整实现
    '''
    def __init__(self, numbers: List[int]):
        '''
        numbers: 三个逻辑学家的数字 [a, b, c]
        '''
        # 验证输入：所有数字必须是正整数（大于0）
        if not all(isinstance(n, int) and n > 0 for n in numbers):
            raise ValueError("输入不合法：所有数字必须是正整数（大于0）")
            
        self.original_numbers = numbers.copy()
        self.numbers = sorted(numbers)  # 排序便于处理
        
        # 验证输入合法性：必须有一个数是另外两个的和
        if not (self.numbers[0] + self.numbers[1] == self.numbers[2]):
            raise ValueError("输入不合法：必须有一个数是另外两个的和")
        
        # 创建逻辑学家对象
        self.logicians = []
        for i in range(3):
            others = [self.original_numbers[j] for j in range(3) if j != i]
            self.logicians.append(Logician(i, others))
        
        # 记录当前轮次
        self.current_round = 0
        
        # 缓存：用于存储已经计算过的假设场景结果
        # key: (假设的三元组tuple, 检查的轮次, checker_id)
        # value: bool (是否应该知道答案)
        self.cache = {}
        
    def simulate_reasoning(self, logician_id: int) -> bool:
        '''
        模拟逻辑学家的推理过程
        
        参数:
            logician_id: 逻辑学家ID
            
        返回: 该逻辑学家是否能确定自己的数字
        '''
        logician = self.logicians[logician_id]
        
        # 边界条件1：直接推断
        if logician.can_deduce_immediately():
            deduced_value = sum(logician.others_numbers)
            logician.possible_numbers = {deduced_value}
            return True
        
        # 检查当前可能性
        return logician.knows_answer()
    
    def update_possibilities_after_no(self, speaking_logician_id: int):
        '''
        当某个逻辑学家说"不知道"后，更新所有逻辑学家的可能性空间
        '''
        # 对于每个其他逻辑学家，更新其可能性
        for listener_id in range(3):
            if listener_id == speaking_logician_id:
                continue
                
            listener = self.logicians[listener_id]
            invalid_candidates = set()
            
            # 检查每个可能的候选数字
            for candidate in list(listener.possible_numbers):
                # 构建假设场景：如果listener的数字是candidate
                hypothetical_numbers = self.original_numbers.copy()
                hypothetical_numbers[listener_id] = candidate
                
                # 完整模拟到当前轮，检查speaking_logician是否应该知道答案
                if self._would_know_in_scenario(tuple(hypothetical_numbers), speaking_logician_id, self.current_round):
                    # 在这个假设下，speaking_logician应该知道答案
                    # 但实际上说了"不知道"，所以这个假设矛盾
                    invalid_candidates.add(candidate)
            
            # 从可能性中移除无效候选
            listener.possible_numbers -= invalid_candidates
    
    def _would_know_in_scenario(self, hypothetical_numbers: Tuple[int, int, int], checker_id: int, target_round: int) -> bool:
        '''
        检查在假设场景下，checker在target_round轮是否应该知道答案
        通过递归模拟前target_round-1轮的推理过程
        
        参数:
            hypothetical_numbers: 假设的三个数字配置 (tuple)
            checker_id: 要检查的逻辑学家ID
            target_round: 目标轮次
            
        返回: 在假设场景下，checker在target_round轮是否应该知道答案
        '''
        # 检查缓存
        cache_key = (hypothetical_numbers, checker_id, target_round)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 检查这个配置是否合法（必须满足一个数是另外两个的和）
        sorted_hyp = sorted(hypothetical_numbers)
        if sorted_hyp[0] + sorted_hyp[1] != sorted_hyp[2]:
            self.cache[cache_key] = False
            return False
        
        # 初始化假设场景下每个逻辑学家的可能性空间
        # possible_sets[i] 表示逻辑学家i的可能数字集合
        possible_sets = [set() for _ in range(3)]
        
        for i in range(3):
            others = [hypothetical_numbers[j] for j in range(3) if j != i]
            a, b = others
            
            # 计算初始可能性
            possible_sets[i].add(a + b)
            if a != b:
                possible_sets[i].add(abs(a - b))
            
            # 过滤掉不满足游戏规则的可能性
            valid = set()
            for candidate in possible_sets[i]:
                test_triple = sorted([candidate, a, b])
                if test_triple[0] + test_triple[1] == test_triple[2]:
                    valid.add(candidate)
            possible_sets[i] = valid
        
        # 模拟前 target_round-1 轮的推理过程
        for round_num in range(1, target_round):
            speaker_id = (round_num - 1) % 3
            
            # 检查该逻辑学家是否能立即推断（边界条件）
            others = [hypothetical_numbers[j] for j in range(3) if j != speaker_id]
            if others[0] == others[1]:
                # 如果看到的两个数相等，应该立即知道
                # 但实际游戏还在继续，说明这个假设与现实矛盾
                self.cache[cache_key] = False
                return False
            
            # 检查是否只有一个可能
            if len(possible_sets[speaker_id]) == 1:
                # 如果之前轮次就应该知道，但实际没有，说明假设矛盾
                self.cache[cache_key] = False
                return False
            
            # 该轮回答"不知道"，更新所有人的可能性空间
            # 对于每个其他逻辑学家
            for listener_id in range(3):
                if listener_id == speaker_id:
                    continue
                
                invalid_candidates = set()
                
                # 检查listener的每个可能候选
                for candidate in list(possible_sets[listener_id]):
                    # 构建更深层的假设：如果listener是candidate
                    deeper_hyp = list(hypothetical_numbers)
                    deeper_hyp[listener_id] = candidate
                    
                    # 递归检查：在这个更深层假设下，speaker在round_num轮是否应该知道
                    if self._would_know_in_scenario(tuple(deeper_hyp), speaker_id, round_num):
                        # 应该知道但实际说不知道，矛盾
                        invalid_candidates.add(candidate)
                
                # 从可能性中移除无效候选
                possible_sets[listener_id] -= invalid_candidates
        
        # 现在检查在 target_round 轮，checker 是否应该知道答案
        others = [hypothetical_numbers[j] for j in range(3) if j != checker_id]
        
        # 边界条件检查
        if others[0] == others[1]:
            self.cache[cache_key] = True
            return True
        
        # 检查可能性数量
        result = len(possible_sets[checker_id]) == 1
        self.cache[cache_key] = result
        return result

    def play_game(self, max_rounds: int = 10) -> List[Tuple[int, bool, int]]:
        '''
        运行游戏

        轮次定义：每个逻辑学家的每次发言都是一个轮次
        轮次1: 逻辑学家0发言
        轮次2: 逻辑学家1发言  
        轮次3: 逻辑学家2发言
        轮次4: 逻辑学家0发言
        ...
        
        返回: [(logician_id, knows_answer, round), ...]
        '''
        print(f"游戏开始！三个数字为: {self.original_numbers}")
        print(f"排序后: {self.numbers} (满足 {self.numbers[0]} + {self.numbers[1]} = {self.numbers[2]})")
        
        results = []
        
        for round_num in range(1, max_rounds + 1):
            # 计算当前轮次应该发言的逻辑学家
            logician_id = (round_num - 1) % 3
            
            print(f"\n=== 第 {round_num} 轮 ===")
            
            logician = self.logicians[logician_id]
            can_deduce = self.simulate_reasoning(logician_id)
            
            actual_number = self.original_numbers[logician_id]
            
            print(f"逻辑学家 {logician_id} 发言:")
            print(f"  实际数字: {actual_number}")
            print(f"  看到数字: {logician.others_numbers}")
            print(f"  可能数字: {sorted(logician.possible_numbers)}")
            print(f"  回答: {'知道' if can_deduce else '不知道'}")
            
            results.append((logician_id, can_deduce, round_num))
            
            if can_deduce:
                print(f"\n🎉 游戏结束！逻辑学家 {logician_id} 在第 {round_num} 轮知道了自己的数字！")
                deduced = list(logician.possible_numbers)[0]
                print(f"推断出的数字: {deduced}")
                return results
            else:
                # 当回答"不知道"时，更新所有人的可能性空间
                self.current_round = round_num
                self.update_possibilities_after_no(logician_id)
                print(f"\n更新后的可能性:")
                for i, log in enumerate(self.logicians):
                    print(f"  逻辑学家 {i}: {sorted(log.possible_numbers)}")
        
        print(f"\n游戏在 {max_rounds} 轮后仍未结束")
        return results


def test_game():
    '''
    测试不同的游戏场景
    '''
    print("=" * 50)
    print("逻辑学家数字游戏测试")
    print("=" * 50)
    
    test_cases = [
        [3, 8, 11],
        [8, 3, 11],
        [3, 11, 8],
        [11, 8, 3],
        [11, 3, 8]
    ]
    
    for i, numbers in enumerate(test_cases, 1):
        print(f"\n{'='*20} 测试用例 {i} {'='*20}")
        print(f"输入数字: {numbers}")
        
        try:
            game = LogicianSumGame(numbers)
            results = game.play_game(max_rounds=50)
            
            print(f"\n结果总结:")
            for logician_id, knows, round_num in results:
                if knows:
                    print(f"逻辑学家 {logician_id} 在第 {round_num} 轮知道答案")
                    break
        except ValueError as e:
            print(f"错误: {e}")
        
        print("\n" + "="*50)


if __name__ == "__main__":
    test_game()


