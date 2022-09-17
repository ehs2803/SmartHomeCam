# SmartHomeCam (졸업작품)

## **작품 주제**

라즈베리파이와 인공지능을 이용한 스마트 홈캠 웹 서비스

## **주제 선정 배경**

1인 가구의 증가와 반려가구 1500만 시대에 따라 외출 중에 카메라를 통해 집안상황 확인, 방범 서비스, 화재감지, 반려동물을 확인을 할 수 있다.

## **작품명**

SmartHomeCam

## **개발기간**

2022.03 ~ 개발 중

## **작품 구성도**

1. 서비스 구성도

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/smarthomecam.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/smarthomecam.jpg)

## **데이터베이스**

---

![Untitled](images/Untitled.png)

![Untitled](images/Untitled%201.png)

## **작품 기능**

---

### **기능 - 계정**

---

![Untitled](images/Untitled%202.png)

![Untitled](images/Untitled%203.png)

회원가입과 로그인을 할 수 있습니다.

### **기능 - 홈캠 모드**

---

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam3.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam3.jpg)

사람탐지 모드입니다. 사람이 탐지되면 이미지, 탐지시간 등이 데이터베이스에 저장됩니다.

탐지 즉시 메일, 메시지 알림이 전송됩니다. 마이페이지에서 탐지 기록을 확인할 수 있습니다.

사람을 탐지할 때 YOLO 모델을 사용했습니다.

---

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam4.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam4.jpg)

---

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam5.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam5.jpg)

---

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam6.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam6.jpg)

---

![https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam7.jpg](https://github.com/ehs2803/SmartHomeCam/raw/main/images/homecam7.jpg)

---

### **기능 - 가족관리**

---

![Untitled](images/Untitled%204.png)

![Untitled](images/Untitled%205.png)

![Untitled](images/Untitled%206.png)

가구원을 등록, 조회, 수정, 삭제할 수 있습니다. 가구원을 등록할 때 이메일, 전화번호, 최대 3장의 얼굴사진을 등록할 수 있습니다.

여기서 입력한 이메일, 전화번호는 이메일, 메시지 알림 시 사용됩니다.

얼굴사진의 경우 외부인탐지 모드에서 외부인을 판단하는 기준으로 사용됩니다.

### **기능 - 실시간 스트리밍**

---

![Untitled](images/Untitled%207.png)

실시간 스트리밍을 확인할 수 있습니다. 이페이지에서는 녹음하기, 화면캡처, 연결끊기 기능이 있습니다.

녹음하기 버튼을 누르면 실시간 스트리밍으로 들어오는 이미지 프레임이 동영상으로 녹화가 시작되고, 다시한번 누르면 동영상이 저장됩니다.

화면캡처 버튼을 누르면 현재 이미지가 저장됩니다.

연결끊기 버튼을 클릭하면 홈캠과의 연결이 해제됩니다.

### **기능 - 사용자 저장 미디어 확인**

---

![Untitled](images/Untitled%208.png)

![Untitled](images/Untitled%209.png)

실시간 스트리밍 페이지에서 사용자가 저장한 동영상, 캡처 이미지를 조회, 삭제할 수 있습니다.

### **기능 - 홈캠 관리**

---

![Untitled](images/Untitled%2010.png)

홈캠 관리 페이지에서는 DB에 저장된 홈캠에 대해서 알림 확인, 모드 설정을 할 수 있습니다. on/off 버튼을 클릭해서 모드를 활성화, 비활성화 할 수 있습니다.

![Untitled](images/Untitled%2011.png)

알림 버튼을 클릭하면 위 페이지로 이동합니다. 특정 홈캠이 발생시킨 알림들을 확인할 수 있습니다.

미확인알림, 확인알림으로 구분되며, 자세한 내용보기를 클릭하면 해상 탐지에 대한 상세페이지로 이동합니다.

### **기능 - 알림확인**

---

![Untitled](images/Untitled%2012.png)

홈캠에서 탐지하면 알림이 발생하는데, 알림 페이지에서는 이러한 알림들을 한번에 확인할 수 있습니다.

![Untitled](images/Untitled%2013.png)

자세한 내용보기를 누르면 위 페이지와 같이 해당 탐지에 대해 상세내용을 제공합니다.

### **기능 - 홈캠 탐지 기록 확인**

---

![Untitled](images/Untitled%2014.png)
![Untitled](images/Untitled%2015.png)

5가지 홈캠 모드에서 탐지한 것들을 각 페이지에서 확인이 가능합니다. 자세히보기 버튼을 누르면 하단의 사진 페이지로 이동합니다. 삭제하기 버튼을 누르면 삭제됩니다.

### **기능 - 홈캠 탐지 기록 확인 - 반려동물**

---

![image](https://user-images.githubusercontent.com/65898555/189586144-829351f1-8766-402d-9196-18bb4a80ac30.png)
![Untitled](images/Untitled%2017.png)

반려동물 탐지의 경우 다른 모드와 다르게 그래프와 표 형태로 출력됩니다.

사용자가 원하는 날짜를 선택하고 조회하기 버튼을 클릭하면 그 날짜의 반려동물 탐지 기록을 보여줍니다. 

그래프의 경우 chart js를 이용했습니다.

### **기능 - 이메일, 메시지 알림**

---

![Untitled](images/Untitled%2018.png)

![Untitled](images/Untitled%2019.png)

반려동물 탐지를 제외한 모든 모드에서 특정 상황 만족 시 가구원 등록 시 입력된 이메일, 전화번호에 이메일, 메시지 알림을 전송합니다.

이메일 알림의 경우 원본사진, 객체 바운딩 사진이 함께 전송됩니다.

문자 메시지의 경우 텍스트로만 전송되고, AWS SNS를 이용했습니다.

