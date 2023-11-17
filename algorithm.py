import random

'''
    조건
    1. 20,100명 학생 --
    2. 토요일/일요일 제외한 17일 --
    3. 652개의 수업 과 52개 시험장 --
    4. 시간장 총 좌석 수 6,872
    
    E = {e1, . . . , en} 일정 기간 내에 예정
    P = {p1, . . . , 오후}
    
    시험 시간표 자동생성 DATA SET
    - 이용 가능 장소 및 해당 수용 인원  --
    - 특별시험 장소 및 수용인원 --
    - 필기과목 목록 --
    - 시험 또는 강좌별 등록된 모든 학생 목록 --
    - 참여 가능한 감독관 목록 -- 
    - 최대 시험 기간 및 각 시험 시간 --
    
    고려된 제약사항 (HC:하드 제약 / SC:소프트 제약조건)
    - HC1 학생이 한 번에 치르게 될 시험의 수 (students - 연속 시간 제외)
    - HC2 교사가 한 번에 들어야 하는 수업 수 (supervisors - 중복 시간 제외)
    
    - HC3 일정 내 시험 횟수 --
    - HC4 수업이 예정된 강의실의 종류와 수용인원 --
    - HC5 과목 시험 일정이 잡혀 있는 시간대 수  --
    
    - SC1 학생의 두 시험(또는 행사) 사이의 총 자유 시간 슬롯 수
    
    - SC2 교사의 연속 수업 총 수
    
    ETP 해결을 위해 개발된 SAGA 하이브리드 알고리즘은 다음과 같다.
    1. T:초기온도 / 냉각속도 값을 설정 - SA
    2. Param - N: 염색체 길이 / 세대 수 / 인구규모
    3. N:염색체 - 시간 슬롯 시퀀스 및 강의실 용량 시퀀스 생성
    4. 목적함수를 이용하여 각 염색체에 대한 최적의 공간 수용 값을 찾는다. (N개의 강의실 중 최대 강의실 수용 값이 최적값)
    5. 염색체 수에서 2개 염색체 선택(선택 수행)
    6. 선택한 염색체를 교차(0.9%) 새로운 염색체를 돌연변이
    7. 새로 생성된 염색체의 타임슬롯 값을 목적함수로 검증
    8. N개의 최상의 염색체를 선택
    9. 최적값이 일정기간 개선이 없을 경우 새로운 염색체을 search
    10. 현재 위치가 좋지 않을경우라도 exp-(ΔE/KT) 확률로 새로운 염색체 선택 - SA
    * ΔE: 초기 온도 T와 가장 좋은 염색체 값의 온도 사이 차이 / K: 볼츠만 상수 1.381 x 10-23
    11. 냉각 - SA
    12. 일정 반복 및 최적 값이 연속적으로 없을 경우 종료 - 개선이 있을 경우 3단계 이동 - SA
'''

#Calc
def objective_function(schedule):
    penalty = 0

    # HC1 학생이 한 번에 치르게 될 시험의 수
    for student in students:
        exams_count = count_exams_for_student(schedule, student)
        if exams_count > max_exams_per_day:
            penalty += exams_count - max_exams_per_day

    # HC2 교사가 한 번에 들어야 하는 수업 수
    for teacher in teachers:
        lectures_count = count_lectures_for_teacher(schedule, teacher)
        if lectures_count > max_lectures_per_day:
            penalty += lectures_count - max_lectures_per_day

    # HC3 일정 내 시험 횟수
    total_exams = count_total_exams(schedule)
    if total_exams > max_exams_in_schedule:
        penalty += total_exams - max_exams_in_schedule

    # HC4 수업이 예정된 강의실의 종류와 수용인원
    for exam in schedule:
        if not is_valid_exam_room(exam):
            penalty += 1

    # HC5 과목 시험 일정이 잡혀 있는 시간대 수
    subjects_schedule_count = count_subjects_schedule(schedule)
    if subjects_schedule_count < total_subjects_count:
        penalty += total_subjects_count - subjects_schedule_count

    return penalty


def simulated_annealing(initial_solution, temperature, cooling_rate):
    current_solution = initial_solution
    while temperature > 0:
        new_solution = neighbor(current_solution)
        if new_solution.fitness > current_solution.fitness:
            current_solution = new_solution
        else:
            probability = math.exp(-(new_solution.fitness - current_solution.fitness) / temperature)
            if random.random() < probability:
                current_solution = new_solution
        temperature *= cooling_rate
    return current_solution


def genetic_algorithm(population, mutation_rate, crossover_rate):
    for _ in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(population, 2)
            if random.random() < crossover_rate:
                new_child = crossover(parent1, parent2)
            else:
                new_child = parent1
            new_child = mutate(new_child, mutation_rate)
            new_population.append(new_child)
    return new_population


def neighbor(solution):
    # 임의의 시험과 강의실을 교체합니다.
    exam1, exam2 = random.sample(solution.exams, 2)
    room1, room2 = random.sample(solution.rooms, 2)
    new_solution = solution.copy()
    new_solution.exams[exam1] = room2
    new_solution.exams[exam2] = room1
    return new_solution


def crossover(parent1, parent2):
    # 임의의 위치에서 두 솔루션을 교차합니다.
    cut1 = random.randint(0, len(parent1.exams) - 1)
    cut2 = random.randint(0, len(parent2.exams) - 1)
    new_child1 = parent1[:cut1] + parent2[cut1:cut2] + parent1[cut2:]
    new_child2 = parent2[:cut1] + parent1[cut1:cut2] + parent2[cut2:]
    return new_child1, new_child2


def mutate(solution, mutation_rate):
    # 임의의 시험의 강의실을 변경합니다.
    exam = random.randint(0, len(solution.exams) - 1)
    new_room = random.randint(0, len(solution.rooms) - 1)
    solution.exams[exam] = new_room
    return solution


def fitness(solution):
    # 솔루션의 품질을 계산합니다.
    # 여기에는 충돌, 겹치는 강의실, 그리고 기타 제약 조건을 고려한 계산이 포함됩니다.
    return 0


def main():
    # 문제의 매개변수를 설정합니다.
    exams = [1, 2, 3, 4, 5]
    rooms = [1, 2, 3, 4, 5]
    constraints = [
        # Exam 1과 Exam 2는 같은 시간대에 할당될 수 없습니다.
        (1, 2),
        # Exam 3과 Exam 4는 같은 강의실에 할당될 수 없습니다.
        (3, 4),
    ]

    # 초기 솔루션을 생성합니다.
    initial_solution = {
        "exams": [1, 2, 3, 4, 5],
        "rooms": [1, 2, 3, 4, 5],
    }

    # 시뮬레이티드 애니얼링을 사용하여 초기 솔루션을 개선합니다.
    improved_solution = simulated_annealing(initial_solution, 100, 0.99)

    # 유전 알고리즘을 사용하여 개선된 솔루션을 개선합니다.
    population = [improved_solution]
    for _ in range(100):
        population = genetic_algorithm(population, 0.01, 0.75)

    # 최상의 솔루션을 출력합니다.
    best_solution = min(population, key=lambda solution: solution.fitness)
    print(best_solution)


if __name__ == "__main__":
    main()
