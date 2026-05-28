## 파이썬 오목 프로젝트 정리본 (이상정 , 박지훈 2인 프로젝트 작업 정리)
---
## 1. ⚪⚫ 오목게임 기본 설명 
`tkinter`라이브러리를 활용하여 제작한 오목게임이며 1:1로컬 대전모드와 AI와 한판붙는 AI대결모드가 존재한다.

### ✨주요기능
- **게임 모드 선택**: 1VS1 및 1VSAI 모드를 지원한다.
- **착수 시스템**: 클릭지점에서 가장 가까운 바둑판 교차점에 돌이 놓이도록 구현한다. (`round`함수 활용)
- **무르기(Undo)기능**:
  - 1VS1 : 직전 수 1개를 취소 할 수 있다.
  - AI모드 : 플레이어의 편의를 위하여 플레이어와 AI의 수를 동시에 취소할수있다. (2개삭제)
- **실시간 정보 표시**: 현재 턴 , 총 착수 횟수 , 마지막 착수 위치를 표시한다.
- **Reset기능** : 진행중인게임을 언제든지 리셋하고 다시 시작하거나 메인메뉴로 복귀할수있다.

### 기술스택 🛠
- **사용한 언어**: Python
- **사용한 라이브러리**: `tkinter`(GUI), `random`(AI부분 사용)

---

## 2. 📱 UI 인터페이스 구성 

### 레이아웃 구조 
<img width="409" height="430" alt="image" src="https://github.com/user-attachments/assets/b16c3502-4a6e-44b9-8633-d7d18e34e5e9" />

<img width="958" height="629" alt="image" src="https://github.com/user-attachments/assets/1c64cee4-6450-44f0-bd77-849da29e589b" />

    
| 구분 | 내용 | 비고 |
| --- | --- | --- |
| **메인 로비** | 게임 시작 전 모드 선택 (`1vs1`, `1vsAI`) 및 종료 | `#F5EEDC` 테마 |
| **게임 보드** | 15 x 15 사이즈의 정밀한 바둑판 영역 | `Canvas` 활용 |
| **대시보드** | 턴 정보, 마지막 좌표, 총 수 표시 | 실시간 업데이트 |
| **컨트롤러** | 무르기, 리셋, 그만두기 버튼 배치 | 우측 사이드바 |

---


### 🎮 오목 게임 GUI 구조 (Tkinter Frame 구조)

현재 오목 게임의 화면 및 프레임 계층 구조

```text
root (전체 창)
 │
 ├── menu_frame (메뉴 상자: 배경 #F5EEDC)
 │    └── 타이틀, 1vs1 버튼, AI 버튼, 그만두기 버튼
 │
 └── game_frame (게임 화면 상자)
      └── main_frame (레이아웃용 상자)
           ├── left (왼쪽 상자)
           │    └── background (바둑판 캔버스)
           │
           └── right (오른쪽 상자: 배경 #F5EEDC)
                ├── top 프레임 (플레이어 정보 라벨)
                ├── center (LabelFrame: 게임 정보, 턴, 수)
                ├── bottom 프레임 
                └── Reset, 무르기, QUIT 버튼들
```

#### Frame 에 대한 개념 공부 
- Frame은 위젯들을 담는 상자(컨테이너) 
  1) 화면 전환을 위해 사용
     - menu_frame 이라는 메뉴상자 와 game_frame이라는 게임화면 상자를 각각 만들어 따로작업하기 편하게 구현
     - 사용 메서드 : .forget() : 숨기는걸 의미 , .pack() : 붙이기 (보여주는걸 의미)
     - 메서드 (forget , pack) 를 번갈아 가면서 사용하며 메뉴와 게임 화면을 편리하게 전환   
  2) 화면 구역을 나누기 위해 사용
     - 게임 화면(game_frame) 내에서 왼쪽에 바둑판 , 오른쪽에 게임 정보를 배치 
     - left 프레임(바둑판) , right 프레임(정보창용)을 나누어 붙임(pack(side = "left"), pack(side="right"))
     




## 3. 핵심 로직 설명 (게임기능 등 )
### 3-1) 바둑판 세팅 및 바둑알 세팅 
```
#초기세팅
SIZE = 15
CELL_SIZE = 50
MARGIN = 50

canvas_size = MARGIN * 2 + CELL_SIZE * (SIZE - 1)
```
- 바둑판 크기를 15 X 15 로하기위해(SIZE)
- 바둑판에서 한칸의 크기를 50픽셀로 세팅(CELL_SIZE)
- 바깥여백을 50픽셀로 세팅 (MARGIN)
#### 바둑판 전체 픽셀 크기 (canvas_size)
1) MARGIN은 외부 요소와의 간격을 나타내는데 이코드에 넣은 이유는 바둑판이 창끝에 딱 붙은 채로 그림을 나오는걸 막기위해서이다.
2) MARGIN * 2 : 너비(width)에서는 좌우 , 높이(height)에서는 상하. 양쪽의 여백을 모두 고려하면 * 2를 해야한다.
3) 15 x 15 면 바둑알을 둘수있는 점은 15개이지만 , 그사이에 간격을 긋는 줄이 14개이며(SIZE - 1), 그 줄 하나의 크기가 CELL_SIZE이다.
   즉 , 바둑판 자체 크기는 MARGIN * 2 + CELL_SIZE * (SIZE - 1) 이다.

```
# 바둑판 줄긋기 
for i in range(15): 
    #가로먼저 긋기 (바둑판에서 한칸크기씩 내려가면서 가로줄이 그려지는코드)
    
    x0 = MARGIN #가로줄긋기때문에 처음 x좌표는 안바뀜 
    y0 = MARGIN + i * CELL_SIZE # 한칸크기씩 밑으로 내려가면서 그려짐 

    x1 = canvas_size - MARGIN #전체크기에서 여백을 뺀위치가 줄이 끝나는위치 
    y1 = y0 # 높이는 그대로 
    background.create_line(x0,y0,x1,y1)
    
    #세로 먼저 긋기 (바둑판에서 한칸크기씩 오른쪽으로 이동하면서 세로줄이 그려지는코드)
    x0 = MARGIN + i * CELL_SIZE 
    y0 = MARGIN 
    
    x1 = x0 
    y1 = canvas_size - MARGIN 
    background.create_line(x0,y0,x1,y1) 

```

### 3-2) 실시간 정보 세팅 



### 3-3) 게임 승패 확정 조건 (5목 관련)
```
directions = [
        (1, 0),   # 가로 
        (0, 1),   # 세로
        (1, 1),   # 대각선 ↘
        (1, -1)   # 대각선 ↗
    ]
```
#### 1단계 : 4가지 방향 정의 (directions)
- 오목에서 승리하는 조건 : 가로 , 세로, 대각선(2가지) 총 4개의 방향중 하나라도 동일한색으로 5개가 이어지면 승리한다
- (1,0) :  x가 늘어나는데 y는 그대로  => 가로
- (0,1) :  x가 그대로인데 y가 늘어남. => 세로
- (1,1) :  x도 늘어나고 y도 늘어남 => 대각선
- (1,-1) : x가 늘어나고 y는 줄어듬 => 대각선 2
- ```for dx, dy in directions ``` : 반복문을 활용하여 이 4가지 종류를 하나씩 검사한다. 

#### 2단계 : 양방향 뻗어나가기 탐색 (**상당히 중요**) 
- 방향을 정했을때 (ex : 가로(1,0) ) , 방금 둔 돌 위치를 기준으로 양옆으로 동일한 색을 가진 돌이 몇개나 있는지 개수 를 카운트해간다.
- 1) 현재 돌카운트 
     ```count_stone = 1 ``` : 현재위치에는 돌을 둔상태이기 때문에 돌이 이미 하나가있는걸로 시작
- 2) 정방향 검사(앞으로)
     ```
     nx , ny = x + dx , y + dy
     while 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == stone:
          count_stone += 1
          nx += dx
          ny += dy
     ```
     
     - ``` 0 <= nx < 15 and 0 <= ny < 15 ``` : 바둑판 내부에 위치하는지 확인 
     - ``` board[nx][ny] == stone``` : 바둑알이 있는지 유무확인 + 같은 색인지 확인 
     - 위에 3가지를 전부다 확인후 통과할시에 돌카운트 증가 및 다음 좌표 이동
       
- 3) 반대 방향 검사(뒤로)
     - 돌을 '줄의 중간'에 놓았을수도 있기 때문에 반대쪽 방향도 검사할 필요가있다.
     ```
     nx, ny = x - dx, y -dy
     while 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == stone:
          count_stone += 1
          nx -= dx
          ny -= dy
     ```
-  +) 방향 검사 대입 해보기
       -검사할 가로 방향 벡터가 dx = 1 , dy = 0 
       -정방향(오른쪽)으로 갈시에 , x에 dx를 더해야 오른쪽으로 이동 (nx = x + dx -> nx = x+1)
       -반대방향(왼쪽)으로 갈시에 , x에서 dx를 빼야 왼쪽으로 이동 (nx = x - dx -> nx = x-1)
       ex)
       -바둑판 중앙인 (7,7)에 돌을 두었다고 가정을 해볼시에 가로 방향(dx = 1 , dy = 0)을 검사할때는 좌표를 다음과         같이 세팅 하게된다.
       - 정 방향 첫 출발  nx = 7 + 1(dx) : 8 , ny = 7 + 0(dy) : 7 즉 (8,7)인 오른쪽 칸부터 검사를 시작
       - 반대 방향 첫 출발 nx = 7 - 1(dx) : 6 , ny = 7 - 0(dy) : 7 즉 (6,7)인 왼쪽 칸부터 검사를 시작  
- 4) 승리 조건 비교 및 반환
     ```
     if count_stone >= 5:
        return True 
     ```
     - 한 방향의 [정방향 + 반대 방향] 검사가 끝났을때 , 돌의 총개수(count_stone)가 5개이상이면  
     -
     -
     
### 3-4) 바둑알 착수 
```
#바둑알 넣기 관련 함수

def Insertion(event):
    global count # 글로벌 변수 

    x = event.x #마우스로 클릭한부분 좌표
    y = event.y #마우스로 클릭한부분 좌표 
    '''
    background.create_oval(x-MARGIN/2,y-MARGIN/2,x+MARGIN/2,y+MARGIN/2,fill="black")
    이거하면 교차점에 두는게 안됨. round사용하여 좌표 정수변환 + 가까운위치지정
    '''

    position_x = round((x-MARGIN)/CELL_SIZE)
    position_y = round((y-MARGIN)/CELL_SIZE)
    '''
    1.MARGIN 뺴는거 : 기본 여백제거 
    2.CELL_SIZE로 나누는이유 
    : x 좌표나올시 164대충이런식 칸크기(CELL_SIZE)로 나눠야 몇번째칸인지 확인가능
    3. round : 가장가까운점이동 

    '''
    if position_x < 0 or position_x > 14 or position_y < 0 or position_y > 14:
        return #바둑판을 벗어난 곳에 착수되는 것 방지
    if board[position_y][position_x] != 0:
        return # 이미 돌이 놓여있는데 또 착수되는 것을 방지
        
    draw_x = position_x * CELL_SIZE + MARGIN
    draw_y = position_y * CELL_SIZE + MARGIN 
    '''
    - position_x,y는 몇번째 칸인지만 확인해주기만함 
    - 따라서 그리기시작할위치계산은 칸크기를 곱하고 여백을더해야함
    '''
    radius = CELL_SIZE // 2 - 5 
    
    count += 1
    #바둑알 개수 카운팅 
    #나중에 흑 백 순서대로 나오게 만들려고 
    
    if(count % 2 == 1) :
        board[position_y][position_x] = 1
        stone = background.create_oval(
        draw_x - radius , draw_y - radius,
        draw_x + radius , draw_y + radius,
        fill="black" ,outline="black"
        )
        last_move_label.config(text=f"Last Move: 흑돌 ({position_x + 1}, {position_y + 1})")
    else :
        board[position_y][position_x] = 2
        stone = background.create_oval(
        draw_x - radius , draw_y - radius,
        draw_x + radius , draw_y + radius,
        fill="white" , outline="white"
        )
        last_move_label.config(text=f"Last Move: 백돌 ({position_x + 1}, {position_y + 1})")
   
   
    history.append((stone, position_x, position_y)) # 둔 돌 색, 좌표 저장
    move_marker(draw_x, draw_y)
    
    # ==============5월13일작업본 2
    # 승리 체크
    if check_win(position_x, position_y, board[position_y][position_x]):
        
        if board[position_y][position_x] == 1:
            player_label.config(text="🎉 흑돌 승리!")
        else:
            player_label.config(text="🎉 백돌 승리!")

        background.unbind("<Button-1>")  # 클릭 막기
        return
    # ==============여기까지 5월 13일작업본2
    
    # [추가] 1vs1 모드 혹은 1vsAI 모드에서 사람이 마지막 돌을 두어 비겼을 때 체크
    if check_draw():
        root.after(100, handle_draw)
        return


    update_turn() #턴 보여주는거 함수호출

    #만약 AI대전이라면 ai 불러오기
    if game_mode == "AI" and count % 2 == 1:
        root.after(500, ai_move)

.
.
.
.
.
.



background.bind("<Button-1>",Insertion) #왼쪽마우스 클릭시 바둑알 넣는작업 
```
#### 1. background.bind("<Button-1>",Insertion)
- "<Button-1>" : Tkinter에서는 마우스 왼쪽버튼을 클릭하는 문자열이 Button-1 (+ Button-2는 마우스 휠클릭 , Button-3는 마우스 오른쪽 버튼클릭 )
- 이벤트 바인딩(.bind) : background(바둑판)위에서 마우스 왼쪽버튼을 누르는 이벤트("Button-1")가 발생할시에 , Insertion함수를 실행하라는의미 
- 콜백 함수 (Callback Function) : 특정 조건(이벤트)이 충족 되었을때 시스템(Tkinter)에 의해 나중에 역으로 호출되는 함수이다.  
#### 2. def Inertion(event) :
-  background.bin 를 통해 함수 호출시 마우스 클릭한 위치에 관련된 정보를 event객체에 담아서 전달한다. (x,y 좌표 전부다.)

#### 3.


#### 4. 

#### 5.





## 4. 협업 관련 작업 정리본 (수시로 갱신할예정)

### 5월1일 ~ 5월 14일 작업 정리본 + 회의 정리본 
1) 바둑판 기본세팅 및 GUI 화면 설계  
2) 흑 , 백 바둑알 두는 이벤트 함수구현 
3) 인공지능과의대결 + 사람과의 대결 + 이 오목프로젝트에 필요한 요소들 정리
   - 3-1) 게임리셋 기능 관련 구현 
   - 3-2) 무르기 기능 관련 구현 
4) 5월7일 프로젝트 1차발표 
   - 4-1) 기본 GUI구성화면 설명 
   - 4-2) 바둑알을둘수있고 나가기 , 게임리셋 등과 같은 기본 설계를 해둔 기능관련 간단설명
6) 누구차례인지 알려주는 TURN관련 인터페이스와 착수위치를 알려주는 좌표 정보 구현
7) 바둑알을 이미둔곳에 한번더클릭시 다른 바둑알이 겹치는 현상 제거

### 5월 15일 ~ 작업 정리본 + 회의 정리본 
1) 오목둘시 승리판정 처리 공부 + 처리 완료 
   > [!NOTE] 
   > 바둑판 전체를 탐색하여 가로, 세로, 대각선 방향으로 돌이 5개 연속 놓였는지 검증하는 승리 조건 알고리즘을  구현 및 테스트 완료
2) 마지막으로 착수한 바둑알을 빨간점으로 표시
   - 무르기할시에도 마지막으로 둔 바둑알을 빨간점으로 표시
3) 코드 정리









