import numpy as np
import penalty as pn
import copy


# 강의실 변경(수용인원이 같은 강의실 기준)
def neighbourhood_structure1(candidate, available_rooms):
    while True:
        random_rows = np.random.choice(candidate.shape[0], size=2, replace=False)
        course1 = copy.deepcopy(candidate[random_rows[0], :])
        course2 = copy.deepcopy(candidate[random_rows[1], :])

        room1_capacity = available_rooms[f"강의실{random_rows[0] + 1}"]["정원"]
        room2_capacity = available_rooms[f"강의실{random_rows[1] + 1}"]["정원"]

        # 크기가 같은 경우에만 교체
        if room1_capacity == room2_capacity:
            candidate[random_rows[0], :], candidate[random_rows[1], :] = course2, course1
            break
    return candidate


# 감독관 변경
def neighbourhood_structure2(available_rooms):
    # 감독 수
    supervisor_no = len(available_rooms)

    while True:
        # 두 감독을 랜덤으로 선택
        random_supervisors = np.random.choice(supervisor_no, size=2, replace=False)
        supervisor1 = available_rooms[f"강의실{random_supervisors[0] + 1}"]["감독관"]
        supervisor2 = available_rooms[f"강의실{random_supervisors[1] + 1}"]["감독관"]

        # 서로 다른 강의실에 배치
        if supervisor1 != supervisor2:
            available_rooms[f"강의실{random_supervisors[0] + 1}"]["감독관"], available_rooms[f"강의실{random_supervisors[1] + 1}"]["감독관"] = supervisor2, supervisor1
            break

    return available_rooms


# 시뮬레이티드 어닐링
def anneal(initial_temperature, ga_best, penalty_point, courses, available_rooms):
    temperature = initial_temperature
    final_temperature = 0.0001 * initial_temperature
    alpha = 0.99  # 온도 낮추기
    current_candidate = ga_best
    best_candidate = ga_best
    current_penalty_point = penalty_point
    best_penalty_point = penalty_point
    iteration = 100 #개선 체크
    neighbourhood_structure_no = 2 # 2가지 케이스의 랜덤
    cnt = 0

    while temperature >= final_temperature:
        new_candidate = copy.deepcopy(current_candidate)
        neighbourhood_structure = np.random.randint(neighbourhood_structure_no)

        if neighbourhood_structure == 0:
            new_candidate = neighbourhood_structure1(new_candidate, available_rooms)
            new_penalty_point = pn.penalty_calc(new_candidate, courses, available_rooms)
        elif neighbourhood_structure == 1:
            new_available_rooms = neighbourhood_structure2(available_rooms)
            new_penalty_point = pn.penalty_calc(new_candidate, courses, new_available_rooms)

        difference = new_penalty_point - current_penalty_point

        if difference < 0 or np.random.random() < np.exp((-1 * difference) / temperature):
            current_candidate = new_candidate
            current_penalty_point = new_penalty_point

        if current_penalty_point < best_penalty_point:
            best_candidate = current_candidate
            best_penalty_point = current_penalty_point

        temperature *= alpha
        cnt += 1

        print("[Iteration ", cnt, "] Penalty Point: ", best_penalty_point, sep="")

    return best_candidate, best_penalty_point
