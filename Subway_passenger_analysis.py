import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 지하철 승하차 인원 데이터 다운로드
metro_all = pd.read_csv("C:\\Users\\정시은\\Downloads\\서울시 지하철 호선별 역별 시간대별 승하차 인원 정보_202410.csv",
                        encoding = "cp949")

# 2024년 10월 총 승객수만 추출
metro_recent = metro_all[metro_all['사용월'] == 202410]

# 불필요한 '작업일자' 칼럼 제거
metro_recent = metro_recent.drop(columns=['작업일자'])

print(metro_recent.head)

# object 타입 빼고 저장
numeric_col = metro_recent.select_dtypes(exclude='object').columns

# 호선별 각 숫자형 데이터 평균 계산
metro_line = metro_recent.groupby(['호선명'])[numeric_col].mean().reset_index()
metro_line = metro_line.drop(columns = ['사용월']).set_index('호선명')
metro_line = metro_line.mean(axis=1).sort_values(ascending=False)

# 한글 지원 그래프 출력
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 호선명, 지하철역별로 각 숫자형 열(예: 시간대별 승하차 인원)의 평균값을 담은 데이터프레임
metro_st = metro_recent.groupby(['호선명','지하철역']).mean().reset_index()

# 2호선만 추출
line = '2호선'
metro_st_line2 = metro_st[metro_st['호선명'] == line]
metro_st_line2

# metro_st_line2 에서 '승차인원' 이름이 포함된 열만 선택 - 컴프리헨션 사용
on_columns = [col for col in metro_st_line2.columns if '승차인원' in col]

# 승차 인원 데이터프레임 생성
metro_get_on = metro_st_line2[['지하철역'] + on_columns]

# '지하철역'을 인덱스로 설정
metro_get_on = metro_get_on.set_index('지하철역')

# '하차인원' 이름이 포함된 열만 선택
off_columns = [col for col in metro_st_line2.columns if '하차인원' in col]

# 하차 데이터프레임 생성
metro_get_off = metro_st_line2[['지하철역'] + off_columns]

# '지하철역'을 인덱스로 설정
metro_get_off = metro_get_off.set_index('지하철역')

# 위에서 소수점까지 나오는 float 형태로 나와서 그냥 int형으로 변환
# '지하철역'을 인덱스로 하는 빈 데이터프레임 생성하기
df = pd.DataFrame(index = metro_st_line2['지하철역'])

# 역 별 평균 승차 인원을 구해 정수로 형 변환하여 데이터 프레임에 저장하기
df['평균 승차 인원 수'] = metro_get_on.mean(axis=1).astype(int)

# 역 별 평균 하차 인원을 구해 정수로 형 변환하여 데이터 프레임에 저장하기
df['평균 하차 인원 수'] = metro_get_off.mean(axis=1).astype(int)

# df에 저장된 승차 인원 수 Top10
top10_on = df.sort_values(by='평균 승차 인원 수', ascending=False).head(10)

plt.figure(figsize=(10,5))
plt.bar(top10_on.index, top10_on['평균 승차 인원 수'])

# x에는 인덱스, y에는 그 값, enumerate 함수?
for x, y in enumerate(list(top10_on['평균 승차 인원 수'])):
    if x == 0:
        plt.annotate(y, (x-0.15, y), color = 'red')
    else:
        plt.annotate(y, (x-0.15, y))

plt.title('2024년 10월 평균 승차 인원 수 Top10')
plt.show()

# 하차 인원 수 Top10
top10_off = df.sort_values(by='평균 하차 인원 수', ascending=False).head(10)
plt.figure(figsize=(10,5))
plt.bar(top10_off.index, top10_off['평균 승차 인원 수'])

for x, y in enumerate(list(top10_off['평균 하차 인원 수'])):
    if x == 0:
        plt.annotate(y, (x-0.15, y), color = 'red')
    else:
        plt.annotate(y, (x-0.15, y))

plt.title('2024년 10월 평균 하차 인원 수 Top10')
plt.show()