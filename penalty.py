from collections import Counter
import numpy as np

'''
고려된 제약사항 (HC:하드 제약 / SC:소프트 제약조건)
- HC1 학생이 한 번에 치르게 될 [시험의 수 (students - 연속 시간 제외)
- HC2 교사가 한 번에 들어야 하는 수업 수 (supervisors - 중복 시간 제외)
- HC3 일정 내 시험 횟수 -- 학생 하루 최대 시험 횟수 (3회)
- HC4 수업이 예정된 강의실의 종류와 수용인원
- HC5 과목 시험 일정이 잡혀 있는 시간대 수
- SC1 학생의 두 시험(또는 행사) 사이의 총 자유 시간 슬롯 수 (2시간)
- SC2 교사의 연속 수업 시간의 총 수
'''


def penalty_calc(chromosome, courses, available_rooms):
    num_exam_rooms, num_time_slots = chromosome.shape
    penalty_point, hc_cnt, sc_cnt = 0, 0, 0

    # 염색체에서 감독관 할당 정보 추출
    supervisors_assign = [info["감독관"] for room_info in available_rooms.values() for info in
                          [room_info] * chromosome.shape[1]]

    # 각 감독관이 할당된 시간대를 추적하는 딕셔너리 생성
    supervisor_schedule = {supervisor: set() for supervisor in supervisors_assign}
    duplicate_schedule = {supervisor: set() for supervisor in supervisors_assign}

    # HC2 제약조건
    for room_idx, room_schedule in enumerate(chromosome):
        for time_slot, exam in enumerate(room_schedule):
            if exam != 0:
                supervisor = available_rooms[f"강의실{room_idx + 1}"]["감독관"]

                # 감독관이 이미 동일한 시간에 다른 발표에 할당되어 있는지 확인
                if time_slot in supervisor_schedule[supervisor]:
                    penalty_point += 1000
                    hc_cnt = 1
                    duplicate_schedule[supervisor].add(time_slot)
                else:
                    supervisor_schedule[supervisor].add(time_slot)

    # SC2 제약조건
    for supervisor, schedule in supervisor_schedule.items():
        sorted_schedule = sorted(schedule)  # 시간대 정렬
        continuous_time, cnt = 0, 0

        for i in range(1, len(sorted_schedule)):
            # 시간대가 연속될 경우 +1
            if sorted_schedule[i] == sorted_schedule[i - 1] + 1:
                continuous_time += 1
            else:
                if continuous_time >= 6:
                    cnt += continuous_time // 4
                # 연속하는 수업 카운트 초기화
                continuous_time = 0

        if continuous_time >= 6:
            cnt += continuous_time // 4

        # 감독관 개별 체크
        penalty_point += cnt * 100
        sc_cnt += 1

    # SC1, HC3 제약조건
    for start_time in range(0, num_time_slots, 12):
        end_time = start_time + 12
        period = {}
        rest = []

        for col_idx in range(start_time, end_time):
            column = chromosome[:, col_idx]
            crs = column[np.nonzero(column)[0]]

            for course_idx in crs:
                if course_idx not in period:
                    period[course_idx] = {
                        "st": col_idx,
                        "et": col_idx + 2,
                        "key": course_idx  # 강의 번호 추가
                    }

        # SC1 제약조건
        sorted_periods = sorted(period.values(), key=lambda x: x["st"])
        for i in range(1, len(sorted_periods)):
            time_diff = sorted_periods[i]["st"] - sorted_periods[i - 1]["et"]
            if 0 < time_diff < 2:
                rest.append([sorted_periods[i - 1]['key'], sorted_periods[i]['key']])

        # rest에 담긴 강의의 학생 중복 여부 확인
        for pair in rest:
            course_1_students = set(courses[pair[0] - 1]["학생"])
            course_2_students = set(courses[pair[1] - 1]["학생"])

            # 중복 학생 찾기
            overlapping_students = course_1_students.intersection(course_2_students)
            penalty_point = len(overlapping_students) * 100

        # HC3 제약조건
        student_list = []
        for value in period:
            student_list.extend(courses[value - 1]["학생"])

        student_counts = Counter(student_list)
        students_over = [student for student, count in student_counts.items() if count > 3]
        penalty_point += len(students_over) * 1000

    return penalty_point
