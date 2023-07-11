class FixedAllocation:
    def __init__(self, n, m, k, data):
        self.n = n    # process 가 갖는 page 개수 (최대 100)
        self.m = m    # 할당 page frame 개수 (최대 20)
        self.k = k    # page reference string 길이 (최대 1,000)
        self.data = data   # page reference string, string을 원소로 갖는 k size list
        self.memory_state = []   # 현재 메모리 상태

        if n > 100 or m > 20 or k > 1000:
            raise ValueError("입력 값의 범위가 올바르지 않습니다.")

        elif n < 0 or m < 0 or k < 0:
            raise ValueError("입력 값의 범위가 올바르지 않습니다.")

        if len(self.data) != k:
            raise Exception("page reference string의 길이와 주어진 page reference string 입력값이 일치하지 않음")

    # TODO page fault 확인 하기
    def check_pf(self, page):
        if page in self.memory_state:   # page fault 발생 하지 않은 경우
            return " "
        else:   # page fault 발생한 경우
            return "F"


# TODO MIN 기법
class MINReplacement(FixedAllocation):
    def __init__(self, n, m, k, data):
        super().__init__(n, m, k, data)

    def min_replacement(self):
        pf_cnt = 0
        mr = ""

        for i, page in enumerate(self.data):
            pf = super().check_pf(page)   # page fault 발생 했는 지 확인

            if pf == "F":   # page fault 발생 하지 않은 경우
                pf_cnt += 1   # page fault 발생 횟수 count

                # memory assign
                if len(self.memory_state) < self.m:   # 메모리 할당 가능한 공간 남아 있는 경우
                    self.memory_state.append(page)   # 메모리 page 할당

                # page replacement
                else:   # victim 선정 하는 경우
                    # 각 page 별 현재 시점 에서 다음에 reference 되는 시점 까지의 시간 계산
                    distance = []   # 각 page 별 거리 저장 하는 리스트
                    for temp in self.memory_state:
                        if temp in self.data[i:]:
                            d = min(list(x for x, y in enumerate(self.data[i:]) if y == temp))
                        else:
                            d = 999
                        distance.append(d)

                    # tie-breaking rule: smallest page frame number
                    self.memory_state[distance.index(max(distance))] = page

            # print(f"t = {i+1}일 때 memory state:", self.memory_state, " / referenced page: ", page)
            mr += "t = " + str(i+1) + "일 때 memory state: " + str(self.memory_state) + "  " + pf + "\n"

        print("총 page fault 횟수", pf_cnt)
        print("메모리 상태 변화 과정 (page fault 발생 위치 표시)")
        print(mr)


class FIFOReplacement(FixedAllocation):
    def __init__(self, n, m, k, data):
        super().__init__(n, m, k, data)

    def fifo_replacement(self):
        pf_cnt = 0
        mr = ""
        queue = []

        for i, page in enumerate(self.data):
            pf = super().check_pf(page)

            if pf == "F":   # page fault 발생한 경우
                pf_cnt += 1

                # memory assign
                if len(self.memory_state) < self.m:
                    self.memory_state.append(page)
                    queue.append(page)   # 새롭게 할당된 page enqueue

                # replacement
                else:
                    replace_page = queue.pop(0)   # 가장 먼저 할당된 page dequeue
                    replace_index = self.memory_state.index(replace_page)
                    self.memory_state[replace_index] = page   # page replacement
                    queue.append(page)   # 새롭게 할당된 page enqueue

            mr += "t = " + str(i+1) + "일 때 memory state: " + str(self.memory_state) + "  " + pf + "\n"

        print("총 page fault 횟수", pf_cnt)
        print("메모리 상태 변화 과정 (page fault 발생 위치 표시)")
        print(mr)


class LRUReplacement(FixedAllocation):
    def __init__(self, n, m, k, data):
        super().__init__(n, m, k, data)

    def lru_replacement(self):
        pf_cnt = 0
        mr = ""

        for i, page in enumerate(self.data):
            pf = super().check_pf(page)

            if pf == "F":   # page fault 발생한 경우
                pf_cnt += 1

                # memory assign
                if len(self.memory_state) < self.m:
                    self.memory_state.append(page)

                # page replacement
                else:
                    distance = []
                    for temp in self.memory_state:
                        # 가장 최근에 reference 되었던 시점 계산
                        d = max(list(x for x, y in enumerate(self.data[:i]) if y == temp))
                        distance.append(d)

                    self.memory_state[distance.index(min(distance))] = page

            mr += "t = " + str(i+1) + "일 때 memory state: " + str(self.memory_state) + "  " + pf + "\n"

        print("총 page fault 횟수", pf_cnt)
        print("메모리 상태 변화 과정 (page fault 발생 위치 표시)")
        print(mr)


class LFUReplacement(FixedAllocation):
    def __init__(self, n, m, k, data):
        super().__init__(n, m, k, data)

    def lfu_replacement(self):
        pf_cnt = 0
        mr = ""

        for i, page in enumerate(self.data):
            pf = super().check_pf(page)

            if pf == "F":   # page fault 발생한 경우
                pf_cnt += 1

                # memory assign
                if len(self.memory_state) < self.m:
                    self.memory_state.append(page)

                # page replacement
                else:
                    refer_cnt = []   # page reference count list
                    distance = []   # tie-breaking 위한 LRU 리스트
                    for temp in self.memory_state:
                        # page reference count 계산
                        cnt = self.data[:i].count(temp)
                        refer_cnt.append(cnt)
                        # tie-breaking 위해 가장 최근에 reference 되었던 시점 계산
                        d = max(list(x for x, y in enumerate(self.data[:i]) if y == temp))
                        distance.append(d)

                    if refer_cnt.count(min(refer_cnt)) > 1:   # tie 발생한 경우
                        self.memory_state[distance.index(min(distance))] = page   # LRU Algorithm
                    else:   # tie 발생하지 않은 경우
                        self.memory_state[refer_cnt.index(min(refer_cnt))] = page   # LFU Algorithm

            mr += "t = " + str(i + 1) + "일 때 memory state: " + str(self.memory_state) + "  " + pf + "\n"

        print("총 page fault 횟수", pf_cnt)
        print("메모리 상태 변화 과정 (page fault 발생 위치 표시)")
        print(mr)


class WSMemoryManagement:
    def __init__(self, n, w, k, data):
        self.n = n   # process 가 갖는 page 개수 (최대 100)
        self.w = w   # window size (최대 100)
        self.k = k   # page reference string 길이 (최대 1,000)
        self.data = data   # page reference string, string을 원소로 갖는 k size list
        self.memory_state = []   # 현재 메모리 상태

        if n > 100 or w > 100 or k > 1000:
            raise ValueError("입력 값의 범위가 올바르지 않습니다.")

        elif n < 0 or w < 0 or k < 0:
            raise ValueError("입력 값의 범위가 올바르지 않습니다.")

        if len(self.data) != k:
            raise Exception("page reference string의 길이와 주어진 page reference string 입력값이 일치하지 않음")

    def check_pf(self, page):
        if page in self.memory_state:
            return " "
        else:
            return "F"

    def ws_memory_management(self):
        pf_cnt = 0
        mr = ""

        for i, page in enumerate(self.data):
            pf = self.check_pf(page)

            # page fault check
            if pf == "F":
                pf_cnt += 1

            # memory assign
            if i < self.w:
                self.memory_state = sorted(list(set(self.data[:i+1])))

            # memory management
            else:
                self.memory_state = sorted(list(set(self.data[i-self.w:i+1])))

            mr += "t = " + str(i + 1) + "일 때 memory state: " + str(self.memory_state) + "  " + pf + "\n"

        print("총 page fault 횟수", pf_cnt)
        print("메모리 상태 변화 과정 (page fault 발생 위치 표시)")
        print(mr)
