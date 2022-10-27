<img width="800" alt="image" src="https://user-images.githubusercontent.com/65898555/197901714-30723c20-683e-4c15-b159-5bb8d64105e9.png">
이미 도커 이미지가 있다면 삭제한다. 삭제 오류가 나면 -f 옵션을 주어 강제 삭제.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/65898555/197901949-6e0090e7-cfa0-443e-a242-ced8e42dcd7a.png">
도커허브에서 이미지를 pull 한다.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/65898555/197902152-d036280a-2803-4950-a3ca-c592646ff082.png">
git pull이 오류가 날 경우 기존 폴더를 삭제한다.

<img width="765" alt="image" src="https://user-images.githubusercontent.com/65898555/197902316-702145ae-3da6-4081-9f3d-79e1a12d6577.png">
git clone

<img width="300" alt="image" src="https://user-images.githubusercontent.com/65898555/197902446-af6fbcd6-c0f0-422b-a7a3-438bc668425f.png">
.env.prod 파일과 yolo 모델과 관련된 cfg, weights 파일 4개를 파이질라를 사용해 추가한다.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/65898555/197903437-9e099949-63c6-4d6b-971e-c4bfe680adfc.png">
docker 이미지명과 태그를 바꾼다.

![image](https://user-images.githubusercontent.com/65898555/197903601-90b30fa6-56ed-42c1-b149-2a8e959837bf.png)

docker-compose up -d 명령어를 통해 컨테이너를 실행한다.

![image](https://user-images.githubusercontent.com/65898555/197903701-808e1737-5af2-4e38-9a8e-95fbd70cab15.png)
![image](https://user-images.githubusercontent.com/65898555/197903755-3e0ca476-274b-4f9b-8fa4-b891fda91ceb.png)
정상적으로 실행된다.

![image](https://user-images.githubusercontent.com/65898555/197904160-2a5e5cc6-5046-4a34-9cae-3145f60b9556.png)
실시간 스트리밍이 불가능한 문제는 gunicorn에서 thread 옵션을 사용해서 해결했다.

![image](https://user-images.githubusercontent.com/65898555/197904078-57863d29-a532-4aae-b5ca-34ddb0a42a65.png)
실시간 스트리밍과 함께 ajax 통신이 정상적으로 동작한다. 
