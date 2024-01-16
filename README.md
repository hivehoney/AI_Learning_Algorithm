# Hybrid Genetic Algorithm-Simulated Annealing (HGASA) Algorithm를 사용하여 ETP(Examination Timetabling Problem) 문제 해결

<br />
<br />

## :notebook: 논문 소개
HYBRID METAHEURISTIC OF SIMULATED ANNEALING AND GENETIC ALGORITHM
FOR SOLVING EXAMINATION TIMETABLING PROBLEM

International Journal of Computer Science and Engineering (IJCSE) ISSN(P): 2278-9960; ISSN(E): 
2278-9979 Vol. 3, Issue 5, Sep 2014, 7-22 © IASET 

해당 논문은 대학 ETP(Examination Timetabling Problem)을 효과적으로 해결하기 위해 혼합 유전 알고리즘과 모의 담금질 기법을 통합한 방법을 소개한다.
기존의 문제 해결 방법을 개선하고 최적의 대학 시험 일정을 생성하기 위해 효과적인 알고리즘을 제시한다. 
유전 알고리즘과 모의 담금질의 결합은 각각의 장점을 살려 최적의 일정을 찾아내는데 도움을 제공하고 이를 통해 대학의 시험 일정 관리에 대한 효율성과 정확성을 향상시킨다.
해당 논문의 이론을 검증하기 위해 Python 언어를 사용하여 제안된 알고리즘을 구현하고 실험 결과를 통해 성능을 검증하였다.

<br />

## 🛠문제 정의

논문에서 제시한 ETP 문제는 다양한 제약 조건을 고려하면서 연속시험, 감독자 및 장소를 포함한 수용인원을 세트로 최적의 시간대를 찾는다. 감독자는 특정 횟수의 연속 시험 감독,
모든 시험을 완료할 날짜를 선택하고 연속 시험에 참석하는 동안 최적의 인원을 배치할 수 있는 시간표를 찾는다. 문제는 다음 그룹에 따라 정의 된다.

- 배정해야될 시험과목 및 시험시간
- 각 시험에 응시하는 학생 목록
- 수용 가능한 강의실 및 시간
- 슬롯 (강의실 및 시간 슬롯)
- 배치된 감독 인원

아래의 시간표는 2개의 강의실에 총 10개의 슬롯입니다.

강의실 | 0900-1000 | 1000-1100 | 1100-1200 | 1300-1400 | 1400-1500
 ----- | --------- | --------- | --------- | --------- | ---------
강의실 A | 1 | 2 | 3 | 4 | 5
강의실 B | 6 | 7 | 8 | 9 | 10

<br/>
본 논문에서 알고리즘의 적합도를 판단할 수 있는 제약조건은 아래와 같이 정의 되어있다.

<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/fdb5569c-0cfd-41bc-8e85-d31dc63ed9bf" alt="이미지" width="600" height="400"></p>
<p align="center"><i>제약조건</i></p>


- **Hard Constraints**
  - *HC01*: 학생이 한번에 치러야 할 시험의 수
  - *HC02*: 감독관이 한번에 감독해야 하는 시험의 수
  - *HC03*: 학생 하루 최대 시험 횟수
  - *HC04*: 수용 인원에 맞는 강의실 배정
  - *HC05*: 일정 내 모든 시험 배정

- **Soft Constraints**
  - *SC01*: 연속으로 시험을 보는 학생의 수
  - *SC02*: 교사의 연속 수업 시간의 총 수
<br>

## :open_file_folder: 데이터
해당 논문에서 제시한 입력 데이터는 test를 위해 아래와 같이 정의하였다.

- `학생 수`: num_supervisors = 9000
- `감독관` num_supervisors = 20
- `시험 수` num_course = 600
- `강의실 수` num_exam_rooms = 20
- `시간대 수` num_time_slots = 17*12
- `모집단 크기` population_size = 10

<br>

## :black_nib: Hybrid Genetic Algorithm-Simulated Annealing(HGASA) 알고리즘

하이브리드 유전 알고리즘 시뮬레이션 어닐링(HGASA) 알고리즘은 유전 알고리즘(GA)과 로컬 검색 방법으로 시뮬레이션 어닐링을 결합하여 수렴 속도를 가속화하는 것이다.
아래 그림은 HGASA 알고리즘의 순서도를 보여준다.
<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/995b2d16-f1f6-4b74-a50f-88ec72311cfb" alt="이미지" width="800" height="600"></p>
<p align="center"><i>HGASA algorithm 순서도</i></p>


<br>

### :black_nib: 초기 모집단

초기 후보 해 집합과 제약 조건 집한은 행렬을 사용하여 표현한다. 행렬은 임의의 데이터를 가지고 행렬로 표현된다.
모집단의 크기인 population_size 만큼 초기 모집단을 생성한 후 제약조건에 따른 적합도를 계산한다.



<br>

### :black_nib: 적합도 계산

HC5 제약조건은 초기 모집단을 생성시 소명한다. 각각의 HC 제약조건은 +1000, SC제약조건은 +100으로 적합도를 계산한다.
페널티 점수가 높을수록 솔루션의 적합도가 떨어진다.

자세한 사항은 `penalty.py` 참조.

<br>

### :black_nib: Genetic Algorithm (GA)

초기 모집단을 기준으로 유전자 알고리즘은 2개의 염색체만 선택해 교차연산과 돌연변이 연산을 거쳐 2명의 자녀를 낳는다.
이를 통해 적합도를 계산하여 기존 적합도 보다 높을 시에는 해당 모집단으로 교체한다.

-----------------------------------

#### :arrow_down_small: 인구 초기화

모집단의 규모는 10개로 설정되어 이번 ETP 문제에 적합한 규모로 초기화 한다.
각 시험일정의 염색체에는 무작위로 슬롯이 할당되며, 이 할당은 일정을 위반하지 않도록 이루어진다. 
특히, HC4, HC5 제약조건을 해결한 초기 모집단을 생성하므로 해당 제약조건의 페널티 계산은 피할 수 있다.

자세한 사항은 `test.py`, `genetic.py` 파일 참조.


-----------------------------------

#### :arrow_down_small: 선택

각 염색체 중 무작위로 2개의 염색체를 선택한다.

자세한 사항은  `genetic.py` 파일 참조.

-----------------------------------

#### :arrow_down_small: 크로스오버 및 복구

2점 교차 연산을 진행하기 위해 선정된 2개의 염색체의 랜덤 슬롯 범위를 지정한다. 이후 해당 염색체의 범위를 서로 교체한 뒤 HC4, HC5 제약조건에 맞지 않는 시험일정을 찾아
랜덤 슬롯 범위내에 위치를 재정의 한다. 아래그림은 2점 교차 연산 과정을 예시로 든 그림이다.

![image](https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/ac29d70e-dc81-4bc8-91b4-4a3149c0b27e)

<p align="center"><i>두 개의의 부모 염색체 교차</i></p>

복구 작업은 HC4, HC5 제약조건을 위반하지 않는 조건하에 랜덤 배치하여 해당 제약조건을 위반하지 않게 한다.

자세한 사항은  `genetic.py` 파일 `crossover`, `repair`  함수 참조.

-----------------------------------

#### :arrow_down_small: 돌연변이

2점 교차 연산이 진행된 각각의 자식 염색체들의 무작위로 강의 순서를 변경한다.
아래 그림은 돌연변이 연산 과정을 예시로 든 그림이다.

![mutation](https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/6ddcefb8-6097-4401-88cd-9803ed050da1)

<p align="center"><i>자식 염색체의 돌연변이 연산</i></p>

자세한 사항은  `genetic.py` 파일 `mutation`  함수 참조.

-----------------------------------

#### :arrow_down_small: 적합도 평가

적합점수를 기준으로 염색체를 재정렬하여 상위 10개의 염색체만 재지정한다. 이를 통해 초기 모집단에서 1세대가 개선된 모집단이 형성된다.

자세한 사항은  `genetic.py` 파일 참조.

<br>

### :black_nib: Simulated Annealing (SA)

시뮬레이션 어닐링(SA)은 통계 물리학 개념을 기반으로 한 최적화 알고리즘으로, 현재 솔루션을 이웃 솔루션으로 교체하거나 기존 솔루션을 확률적으로 선택하여 전역 최적해를 찾는다.
초기 후보는 이전 알고리즘의 최적해이며, 높은 확률로 개선된 이웃을 선택하며 점차 최적해를 찾아간다. SA는 로컬 미니마에 빠지지 않고 전역 최적해를 찾을 수 있는 특징을 가지고 있다.


<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/3464fd3f-6e85-451d-90fc-dcc3be24f7a5" alt="이미지" width="800" height="600"></p>
<p align="center"><i>Simulated Annealing 과정</i></p>

-----------------------------------

#### :arrow_down_small: 랜덤 교체

각 반복에서 무작위로 이웃 구조물 교체방법을 선택하여 후보 염색체를 생성합니다.

- **강의실 변경**<br>
수용인원이 가능한 강의실을 기준으로 강의실을 변경합니다.
- **감독관 변경**<br>
랜덤으로 감독관을 변경합니다.

자세한 사항은  `simul.py` 파일 참조.

-----------------------------------

#### :arrow_down_small: 진행 과정

SA는 중지 기준이 충족될 때까지 여러 번 반복하여 수행된다. 이 절차는 다음 단계에 따라 진행된다.

1. **초기 어닐링 온도 설정**  
초기 어닐링 온도는 GA를 통해 얻은 모집단의 최저 및 최고 적합도 계산 값 사이의 차이로 설정됩니다.
2. **랜덤 이웃 구조 적용**  
3. **적합도 계산**  
새로 생성된 이웃 솔루션의 적합도를 계산하고, 현재 모집단과 비교합니다.
개선이 있으면 교체하고, 그렇지 않으면 난수 R을 생성하고 확률 밀도 함수 값 e^(-δ/T)을 계산하여 이웃을 채택합니다.
5. **냉방 일람표**  
지수 냉각 방식(ECS)을 사용하여 온도가 천천히 감소하도록 합니다.
7. **최종 온도**  
최종 온도는 정지 조건을 나타내며, 초기 온도의 0.0001로 설정됩니다.
이러한 단계를 통해 SA는 초기 온도에서 출발하여 냉각되면서 최적해를 찾아가는 과정을 수행합니다.


자세한 사항은 `simul.py` 파일 참조.

-----------------------------------
<br />

## :speech_balloon: Python에서의 구현

2가지의 외부 패키지를 사용하여 HGASA 알고리즘을 구현했습니다.

- [NumPy](https://numpy.org/devdocs/index.html)<br>
NumPy는 강력한 n차원 배열 구조와 수치 컴퓨팅 도구를 제공합니다. 매트릭스를 만드는 것이 이상적이며, 파이썬 리스트보다 훨씬 빠른 데이터 액세스 속도와 효율적인 메모리 사용이 가능합니다.
- [Matplotlib](https://matplotlib.org/api/index.html)<br>
Matplotlib는 Python에서 대화형 시각화를 만들기 위한 포괄적인 라이브러리입니다. API 중 하나인 파이플롯은 그림에서 대화형 그림을 만드는 데 사용됩니다. 상호 작용 그림은 HGASA의 반복 횟수에 따른 벌점 개선 그래프를 보여줍니다. 그래프를 확대, 이동, 구성 및 저장할 수 있습니다.
<br>

## :chart_with_upwards_trend: 수행 결과 분석


GA, SA, SAGA 연산자/피연산자 총 종류 및 개수 비교


<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/384a6c2e-1748-44e4-be31-267ac2111c36" alt="이미지" width="500" height="300"></p>
<p align="center"><i>프로그램 볼륨 체크</i></p>

<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/4bcd8802-8230-4484-bed4-e10323d6eae8" alt="이미지" width="600" height="400"></p>
<p align="center"><i>프로그램 볼륨 체크</i></p>

<p align=center><img src="https://github.com/hivehoney/AI_Learning_Algorithm/assets/74287295/c0b63144-8bdb-4fad-97d7-945d1220c389" alt="이미지" width="500" height="300"></p>
<p align="center"><i>전체 결과</i></p>


<br>

## :black_nib: 인용
- [Akinwale, Oyeleye C., et al. "Hybrid metaheuristic of simulated annealing and genetic algorithm for solving examination timetabling problem." International Journal of Computer Science and Engineering (IJCSE), India 3.5 (2014): 7-22.](https://scholar.google.co.kr/scholar?hl=ko&as_sdt=0%2C5&q=HYBRID+METAHEURISTIC+OF+SIMULATED+ANNEALING+AND+GENETIC+ALGORITHM&btnG=)
- [Suanpang, Pannee, et al. "Tourism Service Scheduling in Smart City Based on Hybrid Genetic Algorithm Simulated Annealing Algorithm." Sustainability 14.23 (2022): 16293.](https://www.mdpi.com/2071-1050/14/23/16293)
