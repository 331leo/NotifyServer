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
```
[
    [{
        "note": "과학책 챙 기기, 줌에서 카메라 켜기, 꼭 온라인 클래스에서 출석체크 하기",
        "subject": "과학A",
        "url": "https:\/\/zoom.us\/j\/7841618002?pwd=TXU3Vno5ZzRPNDFGcHMrT2RmQkgwZz09"
    }, {
        "note": "사회책 챙기고, 프린트 가져오기",
        "subject": "사회",
        "url": "https:\/\/classroom.google.com"
    }]
]
```
