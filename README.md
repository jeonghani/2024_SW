## 💡 DM: Daily Mystery

생성형 AI를 이용하여 매일 새로운 추리 게임 문제를 제공하는 서비스입니다.

[DM: Daily Mystery 플레이 하러가기](https://dailymystery.netlify.app/)


[시연영상 바로가기](https://www.youtube.com/watch?v=hf4fHv8SU2k)

[프론트 레포지토리](https://github.com/sj102300/SWDigital) | 
[백엔드 레포지토리](https://github.com/namewhat99/docker-ci-cd) | 
[AI 레포지토리](https://github.com/jeonghani/2024_SW)

<br/>

## 👫 팀 소개

프론트: [이승주](https://github.com/sj102300) / [류지승](https://github.com/JiSeungRyu)

백엔드: [이광훈](https://github.com/namewhat99)

AI: [정한이](https://github.com/jeonghani)


<br/>

## 📜 프로젝트 소개

<img width="600" alt="화면 캡쳐" src="https://github.com/user-attachments/assets/19527a75-17ca-4a23-a956-4d554f71e529">

- 개발 동기 및 서비스 기획
    
    <ins>“기존 추리 게임의 문제점을 생성형 AI를 통해 해결하자”</ins>
    
    하나의 문제 개발에 많은 시간과 비용 소모 ⇒ 생성형 AI의 창의력을 활용해 해결
    
    정해진 선택지 내에서 선택해서 문제를 풀이 (자유도가 낮음) ⇒ 용의자를 자유롭게 심문할 기회 제공
    
    한번 플레이한 게임은 더 이상 플레이 하지 않음 ⇒ 생성형 AI를 이용해 매일 새로운 문제 제공
    
- 기능 명세
  1. 게임 시작 및 사건 배경 설명
  2. 추리 메인 페이지에서 용의자 및 증거 물품 정보를 확인
  3. 의심가는 용의자에게 10번의 심문 기회 제공 (챗봇 형식)
  4. 범인 선택
  5. 사건의 전말 및 범인 확인
  6. 하루에 한번만 풀이 가능, 다음 날 자정이 되면 새로운 문제로 다시 플레이
  

<br/>

## 💻 사용 기술 및 개발 과정

<img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=React&logoColor=black"/> <img src="https://img.shields.io/badge/Typescript-3178C6?style=flat-square&logo=Typescript&logoColor=white"/>
<img src="https://img.shields.io/badge/Tailwind CSS-06B6D4?style=flat-square&logo=Tailwind CSS&logoColor=white"/>
<img src="https://img.shields.io/badge/styled components-DB7093?style=flat-square&logo=styled-components&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Spring-6DB33F?style=flat-square&logo=Spring&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/>


<img width="600" alt="개발 파이프라인" src="https://github.com/user-attachments/assets/1babbd15-38b0-446d-9645-62eac81df2e9">

매일 자정에 GPT-4o & Dalle3 API로 문제에 필요한 리소스 생성 → DB에 저장

React.ts로 클라이언트 구축 / Springboot + MySQL로 서버 구축

GPT 응답 stream 형태로 전달 → 실시간으로 소통하는 챗봇 구현
