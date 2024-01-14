import random
import numpy as np
import genetic as ga
import penalty as pn
import simul as sa


def hybrid_system():
    # 학생 수, 감독관, 시험 수, 강의실 수, 시간대 수, 모집단 크기
    num_students = 9000
    num_supervisors = 20
    num_course = 600
    num_exam_rooms = 20
    num_time_slots = 17*12
    population_size = 10
    courses = []
    supervisors = [f"감독관{i}" for i in range(1, num_supervisors + 1)]

    # 이용 가능한 장소 및 해당 수용 인원, 감독관 목록 등 데이터 최소 13일 12시간 기준 하루 처리 52 (한타임 최소 5개강의)
    available_rooms = {
        f"강의실{i}": {
            "감독관": random.choice(supervisors),
            "정원": random.randint(50, 100) // 10 * 10
        }
        for i in range(1, num_exam_rooms + 1)
    }

    # 강의 및 시험 정보 생성
    for _ in range(num_course):
        personnel = int(random.sample(range(3, 10), 1)[0] * 10)
        students_in_lecture = random.sample(range(1, num_students + 1), personnel)

        course = {
            "인원": personnel,
            "학생": students_in_lecture
        }
        courses.append(course)

    # HC5 제약조건 17(일) × 12(시간대) 각 강의별 3차원 행렬
    population = np.zeros((population_size, num_exam_rooms, num_time_slots), dtype=int)
    penalty_points = np.zeros(population_size, dtype=int)

    # 초기 모집단 생성
    for i in range(population_size):
        chromosome = ga.generate_chromosome(courses, available_rooms, num_exam_rooms, num_time_slots)
        population[i] = chromosome
        penalty_point = pn.penalty_calc(chromosome, courses, available_rooms)
        penalty_points[i] = penalty_point


    #페널티 포인트를 기준으로 초기 모집단 정렬
    population = population[penalty_points.argsort()]
    penalty_points = penalty_points[penalty_points.argsort()]

    # # 100세대에 대한 유전 알고리즘을 실행
    max_generations = 100
    population, penalty_points = ga.reproduction(population, penalty_points, max_generations, courses, available_rooms)

    # 시뮬레이티드 어닐링
    temperature = 100
    ga_best = population[0]
    penalty_point = penalty_points[0]
    best_candidate, best_penalty_point = sa.anneal(temperature, ga_best, penalty_point, courses, available_rooms)
    
    print("================= 최종 =================")
    print("최적점수 ", best_penalty_point)


def main():
    hybrid_system()


if __name__ == "__main__":
    main()
