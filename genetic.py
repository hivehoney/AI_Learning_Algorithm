import copy
import numpy as np
import random
import penalty as pn


# HC4 제약조건 체크
def is_valid_assignment(population, room, room_capacity, personnel, start_time_slot, end_time_slot):
    # 강의실 크기 체크
    if personnel <= room_capacity:
        # 빈강의실 체크
        return not np.any(population[room, start_time_slot:end_time_slot])
    return False


# HC4, HC5 제약조건을 해결한 초기 모집단
def generate_chromosome(courses, available_rooms, num_exam_rooms, num_time_slots):
    population = np.zeros((num_exam_rooms, num_time_slots), dtype=int)

    for i, personnel in enumerate(courses):
        # 시험시간 고정
        consecutive_slots = 3

        # 강의실 배정
        while True:
            room = random.randint(0, num_exam_rooms - 1)
            room_capacity = available_rooms[f"강의실{room + 1}"]["정원"]

            # 하루가 넘어가지 않도록 조정
            start_time_slot_base = random.randint(0, num_time_slots // 12 - 1)
            start_time_slot = start_time_slot_base * 12 + random.randint(0, 8)
            end_time_slot = start_time_slot + consecutive_slots

            # HC4 유효성 검사
            if is_valid_assignment(population, room, room_capacity, personnel['인원'], start_time_slot, end_time_slot):
                population[room, start_time_slot:end_time_slot] = i + 1
                break

    return population


# 2개의 염색체를 선택
def selection(population, penalty_points):
    tournament_size = 2

    # 첫 번째 토너먼트 선택을 기반으로 첫 번째 염색체를 선택
    t1, t2 = np.random.choice(range(population.shape[0]), tournament_size)
    first = t1 if penalty_points[t1] <= penalty_points[t2] else t2

    # 선택된 2개의 염색체가 동일하지 않은지 확인
    while True:
        # 2차 토너먼트 선택에 따라 2번째 염색체를 선택
        t1, t2 = np.random.choice(range(population.shape[0]), tournament_size)
        second = t1 if penalty_points[t1] <= penalty_points[t2] else t2

        if second != first:
            break

    return population[first], population[second]


# 2점 크로스오버 수행
def crossover(first_parent, second_parent):
    first_child = np.copy(first_parent)
    second_child = np.copy(second_parent)
    zero_columns = np.where((first_child == 0).all(axis=0) & (second_child == 0).all(axis=0))[0]
    # zero_columns에서 무작위로 cutpoint1과 cutpoint2를 선택합니다.
    cutpoint1, cutpoint2 = np.random.choice(zero_columns, 2, replace=False)

    if cutpoint1 > cutpoint2:
        cutpoint1, cutpoint2 = cutpoint2, cutpoint1

    first_different = set()
    second_different = set()

    # 이점 교차
    first_child[:, cutpoint1:cutpoint2], second_child[:, cutpoint1:cutpoint2] = second_child[:, cutpoint1:cutpoint2], np.copy(first_child[:, cutpoint1:cutpoint2])
    first_different.update(first_child[:, cutpoint1:cutpoint2][first_child[:, cutpoint1:cutpoint2] > 0])
    second_different.update(second_child[:, cutpoint1:cutpoint2][second_child[:, cutpoint1:cutpoint2] > 0])

    # 중복된 값 제거
    common_values = first_different.intersection(second_different)
    first_different.difference_update(common_values)
    second_different.difference_update(common_values)

    first_child = repair(first_child, cutpoint1, cutpoint2, first_different, second_different)
    second_child = repair(second_child, cutpoint1, cutpoint2, second_different, first_different)
    return first_child, second_child


# 교차 후 염색체의 돌연변이 교환
def mutation(chromosome):
    # 강의 랜덤 선택
    random_numbers = random.sample(range(1, 101), 2)
    random_mutation1 = np.where(chromosome[:, :] == random_numbers[0])
    random_mutation2 = np.where(chromosome[:, :] == random_numbers[1])

    # 한 시험당 3시간
    for i in range(3):
        chromosome[random_mutation1[0][i]][random_mutation1[1][i]] = random_numbers[1]
        chromosome[random_mutation2[0][i]][random_mutation2[1][i]] = random_numbers[0]

    return chromosome


# 교차 후 염색체 복구
def repair(child, cutpoint1, cutpoint2, source_set, target_set):
    max_length = max(len(source_set), len(target_set))
    source_list = list(source_set)
    target_list = copy.deepcopy(target_set)

    for i in range(max_length):
        # source_set에서 value의 위치 찾기
        if i < len(source_list):
            indices_source = np.where(child[:, cutpoint1:cutpoint2] == source_list[i])
            start_slot = cutpoint1+indices_source[1][0]
            end_slot = cutpoint1+indices_source[1][2]
        else:
            while True:
                # 전체 시간표 중 0인 랜덤 위치 선정
                random_row = np.random.randint(0, child.shape[0])
                random_col = np.random.randint(0, child.shape[1]-3)

                # 연속적 시간의 값이 모두 0인 위치 찾기
                if child[random_row][random_col] == 0 and child[random_row][random_col+1] == 0 and child[random_row][random_col+2] == 0:
                    rows = [random_row, random_row, random_row]
                    cols = [random_col, random_col+1, random_col+2]
                    indices_source = [rows, cols]
                    start_slot = indices_source[1][0]
                    end_slot = indices_source[1][2]
                    break

        if len(indices_source[1]) >= 3:
            # target_set에서 동일한 위치의 값 찾기
            target_value = next(iter(target_list), None)

            if target_value is not None:
                # 찾은 값으로 교환
                child[indices_source[0], start_slot:end_slot+1] = target_value
                # print("변경위치 확인"+str(np.where(child[:, :] == target_value)[1]))
                target_list.remove(target_value)
            else:
                child[indices_source[0], start_slot:end_slot+1] = 0
    return child


# 정상상태 유전 알고리즘 - 집단 내 염색체 2개 교체
def replacement(population, penalty_points, first_child, second_child, first_penalty_point, second_penalty_point):
    # 개선된 염색체 교체(적합점수 기준판단)
    population_size = len(population)
    population[population_size - 1], population[population_size - 2] = first_child, second_child
    penalty_points[population_size - 1], penalty_points[population_size - 2] = first_penalty_point, second_penalty_point

    # 적합점수 기준 재정렬
    population = population[penalty_points.argsort()]
    penalty_points = penalty_points[penalty_points.argsort()]

    return population, penalty_points


# 새로운 세대에서 새로운 염색체를 재생산
def reproduction(population, penalty_points, max_generations, courses, available_rooms):
    for generation in range(max_generations):
        first_parent, second_parent = selection(population, penalty_points)
        first_child, second_child = crossover(first_parent, second_parent)
        first_child = mutation(first_child)
        second_child = mutation(second_child)

        first_penalty_point = pn.penalty_calc(first_child, courses, available_rooms)
        second_penalty_point = pn.penalty_calc(second_child, courses, available_rooms)

        population, penalty_points = replacement(population, penalty_points, first_child, second_child, first_penalty_point, second_penalty_point)
        print("[진행 ", generation + 1, "] Penalty Point: ", penalty_points[0], sep="")

    return population, penalty_points
