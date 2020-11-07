# API 가이드

**중요 안내 사항**
  - 모든 API요청은 POST로 보내야 합니다.
  - 꼭 https 를 사용해야 개인정보 노출 피해를 막을수 있습니다. (http 차단됨)
  - 반환값과 요청 모두 JSON으로 처리합니다.
  
# Routes
API BASE URL: https://api.leok.kr

## Route: /getdata
### Request (요청)
  ```
  {"school":"신사중","class":"3-2"} 
  ```

### Response (반환)
- 현재 날짜, 시간에 따라 다음교시의 과목정보를 반환합니다.
  - 월요일 오전 8:30 분에 요청 -> 월요일 1교시 수업 반환
  - 월요일 오전 9:30분에 요청 -> 월요일 2교시 수업 반환
``` 
{"note":"간단한 한마디, 노트","subject":"과학A(과목명)","url":"줌,구글클래스 등 링크"}
```

## Route: /getclassdata
### Request (요청)
  ```
  {"school":"신사중","class":"3-2"}
```
### Response (반환)
  - 요청한 학교, 학급에 대한 모든 정보를 반환합니다.
  - 구조가 복잡합니다, 구조는 
```
[
    [ #이 리스트는 하나의 요일을 뜻함 (0번->월, 1번->화, 2번->수 ....)
    {  #하나의 Dict(JSON)은 한 교시를 뜻함 (0번->1교시,1번->2교시,2번->3교시)
        "note": #간단한 설명,
        "subject": #과목명,
        "url": #줌링크"
    }, { #2교시
        "note": #간단한 설명,
        "subject": #과목명,
        "url": #줌링크"
    }, { #3교시
        "note": #간단한 설명,
        "subject": #과목명,
        "url": #줌링크"
    }, { #4교시
        "note": "가정책, 프린트 꼭 가져오기",
        "subject": "가정",
        "url": "https:\/\/classroom.google.com\/u\/2\/c\/NjY5Njc2MjM0Mzda"
    }, { #5교시
        "note": "국어 프린트 챙겨오기",
        "subject": "국어B",
        "url": "https:\/\/zoom.us\/j\/99931625319?pwd=MXRleW04R0dsRXJUaENNTS9pTGVCQT09"
    }, { #6교시
        "note": "수학책 지참",
        "subject": "수학",
        "url": "https:\/\/zoom.us\/j\/3758634096?pwd=cXFIaVZLSk9FVHVZWmJtVTVTT1hMQT09"
    }],
    [ #화
    ~~~
    ],
    [ #수
    ~~~
    ]
]
```
