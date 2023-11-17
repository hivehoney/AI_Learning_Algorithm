import random

# 학생 수, 감독관, 수업 수, 시험장 수, 시간대 수
num_students = 20100
num_supervisors = 100
num_lectures = 652
num_exam_rooms = 52
num_time_slots = 17

# 이용 가능한 장소 및 해당 수용 인원, 감독관 목록 등 데이터 최소 13일 12시간 기준 하루 처리 52 (한타임 최소 5개강의)
available_rooms = {"강의실 A": 50, "강의실 B": 40, "강의실 C": 30, "강의실 D": 30, "강의실 E": 30}
special_exam_rooms = {"특별실 X": 100, "특별실 Y": 80}
supervisors = [f"감독관{i}" for i in range(1, num_supervisors + 1)]


# 강의 및 시험 정보 생성
lectures = [{"subject": f"과목{i}", "학생 목록": []} for i in range(num_lectures)]
lectures += [{"subject": f"시험{i}", "학생 목록": []} for i in range(num_exam_rooms)]
exams = [{"subject": lecture["subject"], "location": "", "time": 0, "supervisors": "", "students": []} for lecture in lectures]


# 수업별 한정된 인원의 학생 배치
for lecture in lectures:
    students_in_lecture = random.sample(range(1, num_students + 1), min(random.randint(10, 20), num_students))
    lecture["students"] = students_in_lecture


# 시험 및 강의 일정 생성
def generate_exam_schedule():
    start_time = 480  # 8:00 AM를 분 단위로 표현
    end_time = 1200   # 8:00 PM를 분 단위로 표현
    time_step = 60    # 1시간 간격으로 배치

    # 강의실 별 시간 초기화
    room_times = {room: start_time for room in available_rooms.keys()}

    for i, exam in enumerate(exams):
        # 시험 정보 추가
        exam["location"] = random.choice(list(available_rooms.keys()))
        room_time = room_times[exam["location"]]

        # exam_time_addition 값을 미리 할당받아 exam["time"]에 저장
        exam_time_addition = random.randint(1, 3) * 60
        exam["time"] = f"{room_time}~{room_time + exam_time_addition}"
        exam["supervisors"] = random.choice(supervisors)
        exam["students"] = random.sample(lectures[i]["학생 목록"], min(30, len(lectures[i]["학생 목록"])))

        # 1~3시간의 시간대 추가
        room_times[exam["location"]] += exam_time_addition

# 시험 일정 출력
def print_exam_schedule():
    for i, exam in enumerate(exams, start=1):
        total_students = len(exam['students'])
        print(f"일정: {exam['subject']} - 장소: {exam['location']}, 시간대: {exam['time']}, 감독관 및 교사: {exam['supervisors']},학생수: {total_students}, 학생 목록: {exam['students']}" )


def main():
    # 예시 시험 일정 생성 및 출력
    generate_exam_schedule()
    print_exam_schedule()


if __name__ == "__main__":
    main()
