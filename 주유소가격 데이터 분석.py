# 주유소가격 데이터 분석

# 데이터 불러오기
# 2022년 주유소들의 일자별 가격 데이터

# 상반기, 하반기 주유소 데이터 가격조회
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data1 = pd.read_csv('data/2022년_서울_상반기_일별_가격.csv', encoding = 'cp949')
data2 = pd.read_csv('data/2022년_서울_하반기_일별_가격.csv', encoding = 'cp949')
print(data1.shape, data2.shape)

# 상반기, 하반기 DataFrame 합치기
data = pd.concat([data1, data2], ignore_index = True)
print(data.shape)

# DataFrame 기본 정보 조회
print(data.info())

# Data 확인
print(data.head())

# 결측치 확인
print(data.isnull().sum())

# 정수/실수 타입 컬럼
print(data.describe())

# 문자열 타입 컬럼
print(data.describe(include = 'object'))

# 상표 컬럼의 고유값 조회
print(data['상표'].unique())
print(data['상표'].value_counts())
print(data['상표'].value_counts(normalize = True))

# 지역 컬럼의 고유값 조회
print(data['지역'].unique())
print(data['지역'].value_counts())
print(data['지역'].value_counts(normalize = True))

# 셀프여부 조회
print(data['셀프여부'].value_counts())

# 지역 컬럼의 값을 이용하여 "구" 컬럼 생성
data['구'] = data['지역'].apply(lambda x : x.split()[1])
print(data.head())

# 기간 컬럼을 datetime 타입으로 변경
data['기간'] = pd.to_datetime(data['기간'], format = "%Y%m%d")
print(data.head())

# 기간 컬럼을 이용해 "월", "일" "요일" 컬럼 생성
data['월'] = data['기간'].dt.month
data['일'] = data['기간'].dt.day
data['요일'] = data['기간'].dt.weekday
print(data.head())

# 요일 - 0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일 로 변경
data['요일'] = data['요일'].apply(lambda x : '월화수목금토일'[x])
print(data.head())

# 전처리 완료 -> 파일로 저장
data.to_csv('data/2022년_주유소_가격_데이터_전체.csv', index = False)



# 분석
# 휘발유 가격이 가장 비싼 5개 행 조회
print(data.sort_values(['휘발유', '기간'], ascending = [False, True]).head())

# 휘발유 가격이 가장 저렴한 5개 행 조회 (단 0원인 주유소 제외)
print(data.query('휘발유 != 0').sort_values(['휘발유', '기간']).head())

# 고급휘발유 가격이 가장 비싼 5개 행 조회
print(data.sort_values(['고급휘발유', '기간'], ascending = [False, True]).head())

# 고급휘발유 가격이 가장 저렴한 5개 행 조회 (단 0원인 주유소 제외)
print(data.query('고급휘발유 != 0').sort_values(['고급휘발유', '기간']).head())

# 경유 가격이 가장 비싼 5개 행 조회
print(data.sort_values(['경유', '기간'], ascending = [False, True]).head())

# 경유 가격이 가장 저렴한 5개 행 조회 (단 0원인 주유소 제외)
print(data.query('경유 != 0').sort_values(['경유', '기간']).head())

# 상표별 휘발유 평균가격 조회
상표별_휘발유_평균가격 = data.groupby('상표')['휘발유'].mean().sort_values()
print(상표별_휘발유_평균가격)

# 0원인 주유소는 빼고 계산
상표별_휘발유_평균가격_1 = data.query('휘발유 != 0').groupby('상표')['휘발유'].mean().sort_values()
print(상표별_휘발유_평균가격_1)

# 상표별 휘발유 평균가격 시각화
휘발유_전체평균 = np.round(data['휘발유'].mean(), 2)
상표별_휘발유_평균가격.plot(kind = 'bar', rot = 45)

plt.axhline(휘발유_전체평균, color = 'red', linestyle = ':', label = f'전체평균:{휘발유_전체평균}')
for i in range(상표별_휘발유_평균가격.size):
    txt = str(np.round(상표별_휘발유_평균가격[i]))
    plt.text(i-0.3, 상표별_휘발유_평균가격[i], txt)
    
plt.title('상표별 휘발유 평균가격')
plt.ylim(1000, 2050)
plt.legend(bbox_to_anchor = (1, 1), loc = 'upper left')
plt.show()

# 셀프 주유소와 일반 주유소 개수 확인
print(data['셀프여부'].value_counts())
print(data['셀프여부'].value_counts(normalize = True))

# 셀프 여부에 따른 휘발유 평균 가격 비교
print(data.groupby('셀프여부')['휘발유'].mean())
print(data.query('휘발유 != 0').groupby('셀프여부')['휘발유'].mean())

# 상표별 일반/셀프 주유소의 휘발유 가격 평균 비교
상표_셀프여부별_휘발유평균 = data.pivot_table(index = '상표', columns = '셀프여부', values = '휘발유', aggfunc = 'mean', margins = True)
print(상표_셀프여부별_휘발유평균)

# 상표별 일반/셀프 주유소의 휘발유 가격 평균 비교 시각화
상표_셀프여부별_휘발유평균[['셀프', '일반']].iloc[:-1].plot(kind='bar', title = '상표, 셀프여부별 휘발유 평균가격 비교',
                                            rot = 45, ylim = (1200, 2100), figsize = (10, 7))
plt.legend(bbox_to_anchor = (1, 1), loc = 'upper left')
plt.show()

# 휘발유 가격 boxplot
data.query('휘발유 != 0')['휘발유'].plot(kind = 'box', title = '휘발유 가격 분포')
plt.show()

# 상표별 휘발유 가격의 분포를 boxplot으로 시각화
plt.figure(figsize = (8, 5))
sns.violinplot(data = data.query('휘발유 != 0'), y = '휘발유', x = '상표')
plt.title('상표별 휘발유 가격 분포')
plt.show()

# 상표별 일반/셀프 주유소의 휘발유 가격에 대한 분포 확인 - boxplot으로 시각화
plt.figure(figsize = (10, 7))
sns.violinplot(data = data.query('휘발유 != 0'), y = '휘발유', x = '상표', hue = '셀프여부')
plt.title('상표별 일반/셀프 주유소의 휘발유 가격 분포')
plt.show()

# 구별 휘발유 가격의 평균
result = data.query('휘발유 != 0').groupby('구')['휘발유'].mean().sort_values(ascending = False)
print(result)

# 평균 가격이 가장 높은 구의 상표별 휘발유 평균가격
print(data[data['구'] == result.index[0]].groupby('상표')['휘발유'].mean())

# 월 평균 휘발유 가격
월별_평균_휘발유가격 = data.query('휘발유 != 0').groupby('월')['휘발유'].mean()
print(월별_평균_휘발유가격)

# 월 평균 휘발유 가격 변화추이를 시각화
월별_평균_휘발유가격.plot(figsize = (15, 4))
plt.xticks(range(1, 13), labels = [str(i) + '월' for i in range(1 ,13)])
plt.grid(True, linestyle = ':')
plt.title('월 평균 휘발유 가격 변화추이')
plt.show()

pd.options.display.max_columns = 30

# 각 구의 월별 평균 휘발유 가격
구_월별_휘발유_평균가격 = np.round(data.pivot_table(index = '월', columns = '구', values = '휘발유', aggfunc = 'mean'), 2)
print(구_월별_휘발유_평균가격)

# 각 구의 월별 평균가격의 변화추이 시각화
구_월별_휘발유_평균가격.plot(figsize = (15, 5), title = '각 구의 월별 평균가격의 변화추이', ylabel = '평균가격')
plt.legend(bbox_to_anchor = (1, 1), loc = 'upper left', title = '구', ncol = 2)
plt.show()

# 가장 휘발유가격이 비싼 주유소 상위 5 - (같은 주유소가 여러개 나오므로 가장 비싼 가격을 기준으로 집계)
비싼주유소 = data.groupby(['상호', '주소'])['휘발유'].max().sort_values(ascending = False).head()
print(비싼주유소)

# 가장 휘발유가격이 저렴한 주유소 상위 5 - (같은 주유소가 여러개 나오므로 가장 비싼 가격을 기준으로 집계)
저렴한주유소 = data.query('휘발유 != 0').groupby(['상호', '주소'])['휘발유'].max().sort_values().head()
print(저렴한주유소)

# 모든 값이 같은 중복 행을 제거
data.query("상호 == '서남주유소'")[['상호', '주소', '지역', '상표', '경유']].drop_duplicates()

# index나 컬럼이 여러개 => Multi-Index
# 특정 level의 index를 조회 (level -> 밖에서 안쪽으로 0~N 1씩 증가 (음수 index도 존재))
print(저렴한주유소.index.get_level_values(0)) # level 0 index값들을 조회(상호)
print(저렴한주유소.index.get_level_values(1)) # level 1 index값들을 조회(주소)
print(저렴한주유소.index.get_level_values(-1)) # level -1 index값들을 조회(마지막)

# 휘발유 비싼 주유소의 상위 5개의 상호, 지역, 주소 조회(중복제거)
# 비싼 주유소 조회결과에 추가정보를 확인
data.loc[data['상호'].isin(비싼주유소.index.get_level_values(0)) &
         data['주소'].isin(비싼주유소.index.get_level_values(1)),
         ['상호', '지역', '주소']].drop_duplicates()

# 휘발유 저렴한 주유소의 상위 5개의 상호, 지역, 주소 조회(중복제거)
data.query('상호 in @ 저렴한주유소.index.get_level_values(0) and 주소 in @ 저렴한주유소.index.get_level_values(1)')\
    [['상호', '지역', '주소']].drop_duplicates()
    
# 고급 휘발유를 가장 많이 파는 구 조회
print(data.query('고급휘발유 != 0').groupby('구')['고급휘발유'].count()) # 동일 주유소 count

print(data.query('고급휘발유 != 0')[['구', '상호', '주소']].drop_duplicates().groupby('구').count()['상호']\
    .sort_values(ascending = False))