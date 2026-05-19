# 파이썬 오목게임 관련 코드 작업
from tkinter import *
import random # 임시로 AI랜덤 돌 두기 구현 위해서 추가



# ===================================
# 1. 게임 초기 세팅 및 디자인 관련 상수 
# ===================================
SIZE = 15 # 바둑판 크기 15 x 15 크기로하기위해서 
CELL_SIZE = 50 #한칸 크기를 50픽셀로 일단냅두고 
MARGIN = 50  #바깥여백 50픽셀
canvas_size = MARGIN * 2 + CELL_SIZE *(SIZE -1)

'''
바둑판 전체 픽셀 크기 
1. MARGIN : 외부요소와의 간격 -> 창 끝에 딱붙은채로 그림나오는거 막을려고 
   MARGIN * 2 : 양쪽 여백 모두 생각한것 width 에선 좌우 , height 에선 상하 여백 

2. CELL_SIZE , SIZE : 바둑판크기 관련 
   15 x 15 면 바둑알을 둘수있는 점은 15개지만 그사이 간격을 긋는 줄은 14개(SIZE - 1)

   한칸 크기(CELL_SIZE)를 40픽셀로 지정했기때메 바둑판자체 크기는 CELL_SIZE * (SIZE - 1)

3. 총크기 1번과 2를 더한거를 나타낸다. 
'''

# 게임 상태 변수 관련 
count = 0 #바둑알개수
history = [] #바둑알 순서 저장
board = [[0] * 15 for _ in range(15)] #착수 기록장 [0은 빈칸 1, 2는 흑,백돌 놓여짐]

last_marker = None

# 색상 및 스타일 조합 
BG_COLOR = "#F5EEDC"
TITLE_COLOR = "#333333"
BTN_COLOR = "#4E3629"
BTN_FONT_COLOR = "white"

'''
게임 시작 시 메뉴화면 세팅 + 디자인 
색상조합 AI 의 조언 
- 눈이편한 배이지색 #F5EEDC (배경) , 버튼 다크브라운 #4E3629 (버튼 배경)
- 짙은 회색글자 #333333 (제목 타이틀 색깔)
- 버튼 글자색 흰색으로 
'''



# ===================================
# 2. 메인 화면 (root) 및 화면전환 관련 코드 
# ===================================

root = Tk() # 창생성하는거 먼저
root.title("오목게임") #제목 



def game_start(mode):
    global game_mode
    game_mode = mode        # 선택된 모드 저장 2인인지 1인인지
    restart_game()          # 게임 리셋 , 게임들어갔다가 메뉴갔다가 다시 게임들어갈시 전부초기화
    menu_frame.pack_forget()#메뉴 숨기는거 의미 
    game_frame.pack()       # 게임화면 보여주는거의미 


#메인 메뉴 복귀
def Back():
    game_frame.pack_forget() #게임화면 안보이고
    menu_frame.pack()        #메뉴화면 보이게 




# ===================================
# 3. [화면 구역 1] 메뉴 화면 (menu_frame)
# ===================================

menu_frame = Frame(root) 
menu_frame.config(bg=BG_COLOR)
menu_frame.pack() 

title = Label(menu_frame,text="Omok Game" , width=20,height=5,bg=BG_COLOR,fg=TITLE_COLOR,font=("Arial",30,"bold"))
vs_people = Button(menu_frame, text=" 1 vs 1", width=20, height=2, command=lambda: game_start("1vs1"), bg=BTN_COLOR, fg=BTN_FONT_COLOR, font=("Arial", 15, "bold"), cursor="hand2", relief="flat") 
vs_AI = Button(menu_frame, text=" 1 vs AI", width=20, height=2, command=lambda: game_start("AI"), bg=BTN_COLOR, fg=BTN_FONT_COLOR, font=("Arial", 15, "bold"), cursor="hand2", relief="flat")
game_quit = Button(menu_frame, text = "  그만두기 ", width= 20, height = 2,bg=BTN_COLOR,fg=BTN_FONT_COLOR,font=("Arial",15,"bold"),cursor="hand2",relief="flat")


title.pack(padx=30,pady=10)
vs_people.pack(padx=15,pady=15)
vs_AI.pack(padx=15,pady=15)
game_quit.pack(padx=15,pady=15)
'''
padx= 위젯과 다른 위젯사이의 가로 간격 
pady= 위젯과 다른 위젯사이의 세로간격 
'''
# ===================================
# 4. [화면 구역 2] 게임 화면 (game_frame)
# ===================================
game_frame = Frame(root)

# 왼쪽 바둑판 오른쪽 게임 관련 정보창 분할을 위한 메인 레이아웃 프레임 
main_frame = Frame(game_frame)
main_frame.pack()

# ===================================
# 4-1. 게임 화면 [왼쪽 구역 2] : 바둑판 표시 
# ===================================

left = Frame(main_frame)
left.pack(side="left")

background = Canvas(left, width = canvas_size, height=canvas_size,bg = "#DEB887")
background.pack()
'''
bg = ~ , 바둑판과 비슷한색 AI한테 추천받음 
'''

# 선긋기 (좌우) 15 x 15니까 총 15번반복하기 
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


# ===================================
# 4-2. 게임 화면 [오른쪽 구역] : 정보창 및 버튼  (right)
# ===================================

right = Frame(main_frame,bg="#F5EEDC",padx=50)
right.pack(side="right",fill="y")
# 오른쪽 위치 + 높이는 화면 가득 차게 (fill = "y")


# 상단에 플레이어 정보 대진 표 (1P vs 2P)
top = Frame(right, bg=BG_COLOR)
top.pack(side="top", pady=20)

player = Label(top,text="👤 1P(흑돌) \n\n VS \n\n 👤 2P(백돌)",font=("Arial",16,"bold"),bg="#F5EEDC",fg="#333333",justify="center")
player.pack(pady=20)

# 중단에: 현재 게임 정보 상태창 (LabelFrame)

center = LabelFrame(right, text="게임정보",bg=BG_COLOR,padx=40,pady=40,bd=3,relief="ridge",labelanchor="n")
center.pack(expand=True,fill="both",padx=20,pady=20)

# 누구차례인지 알려주는 라벨 
player_label = Label(center, text="● 1P (Black) Turn", font=("Arial", 22, "bold"), bg="#F5EEDC")
player_label.pack()

# 총 움직임을 알려주는 라벨
move_count_label = Label(center, text="Total Moves: 0", font=("Arial", 12), bg="#F5EEDC")
move_count_label.pack()

#마지막에 둔 돌 위치를 알려주는 라벨 
last_move_label = Label(center, text="Last Move: None", font=("Arial", 12), bg="#F5EEDC", fg="black")
last_move_label.pack(pady=10)


# 하단에: 기능 제어 버튼들 (Reset, 무르기 ,QUIT)  
bottom = Frame(right, bg=BG_COLOR)
bottom.pack(side="bottom", pady=20)


restart = Button(right,text="Reset",command=lambda:restart_game(),width=15, bg=BTN_COLOR,fg=BTN_FONT_COLOR,font=("Arial",15,"bold"))
restart.pack(pady=20)

undo_btn = Button(right, text="무르기", command=lambda:undo(), width=15, bg=BTN_COLOR, fg=BTN_FONT_COLOR, font=("Arial", 15, "bold"))
undo_btn.pack(pady=20)

menu_return = Button(right,text="QUIT",command=Back, width=15,bg=BTN_COLOR,fg=BTN_FONT_COLOR,font=("Arial",15,"bold"))
menu_return.pack(pady=20)



'''
root 는 전체창 
Frame(~) 는 ~안의 구역 나누기 => 메뉴화면과 게임화면을 나눔. 
menu_frame = 처음 게임시작 시 메뉴들이 나오는 화면을 의미하며 
game_frame = 일대일 or 1vs AI 와의 대결을 선택할시 화면이 나오도록의미 
'''


# ===================================
# 5. 게임 로직 및 이벤트 함수들 
# ===================================

# 누구 차례인지 알려주는 함수 (update_turn)
def update_turn():
    if count % 2 == 0:
        player_label.config(text="● 1P (Black) Turn", fg="black")
    else: 
        player_label.config(text="○ 2P (White) Turn", fg="gray")
    move_count_label.config(text=f"Total : {count} move")


# 5목 승리 판정 관련 알고리즘 **********중요***********
def check_win(x, y, stone):
    directions = [
        (1, 0),   # 가로 
        (0, 1),   # 세로
        (1, 1),   # 대각선 ↘
        (1, -1)   # 대각선 ↗
    ]

    for dx, dy in directions: # 방향을 하나씩 꺼내서 검사한다는 의미 dx: 첫번째인자 , dy : 두번째인자
        count_stone = 1 # 현재위치에 돌하나를 둔상태로 시작하니까돌이 하나있다는의미 즉, 현재 돌 포함해서 시작하라는의미

        # 정방향 검사
        nx, ny = x + dx, y + dy 
        while 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == stone: #바둑판안인지 아닌지 체크 및 같은색 돌이 있는지 확인하는것
            count_stone += 1
            nx += dx
            ny += dy

        # 반대방향 검사
        nx, ny = x - dx, y - dy
        while 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == stone:
            count_stone += 1
            nx -= dx
            ny -= dy

        # 5목 이상이면 승리
        if count_stone >= 5:
            return True

    return False


def move_marker(draw_x, draw_y): 
    '''
    마지막 돌위에 빨간색 점마커를 그리는 함수
    '''
    global last_marker
    # 이전 마커 존재시 캔버스에서 제거 
    if last_marker is not None: 
        background.delete(last_marker)

    

    #마지막으로 둔돌 정중앙에 반지름 3픽셀의 쪼꼬만한 원표시 
    marker_radius = 3 
    last_marker = background.create_oval(
        draw_x - marker_radius, draw_y - marker_radius,
        draw_x + marker_radius, draw_y + marker_radius,
        fill="red", outline="red" # 가운데 표시가 빨간색 + 마지막으로 둔돌 잘표시되게 외곽도 빨간색 
    )





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


    update_turn() #턴 보여주는거 함수호출

    #만약 AI대전이라면 ai 불러오기
    if game_mode == "AI" and count % 2 == 1:
        root.after(500, ai_move)
        

# ai 돌 넣기 
def ai_move():
    global count

    if count % 2 == 0:
        return

    empty_spots = []
    for y in range(15):
        for x in range(15):
            if board[y][x] == 0:
                empty_spots.append((x, y)) 
                
    if not empty_spots: # 판이 꽉 찼으면 더 이상 두지 않음
        return
    
    # 빈 칸 중 무작위 한 칸 뽑아서 돌 두기
    position_x, position_y = random.choice(empty_spots)
    
    # 화면에 그릴 픽셀 좌표로 변환 
    draw_x = position_x * CELL_SIZE + MARGIN
    draw_y = position_y * CELL_SIZE + MARGIN 
    radius = CELL_SIZE // 2 - 5 
    
    count += 1 # AI가 돌을 뒀으니 카운트 1 증가
    
    # AI 백돌은 2로 저장
    board[position_y][position_x] = 2 
    stone =background.create_oval(
        draw_x - radius, draw_y - radius,
        draw_x + radius, draw_y + radius,
        fill="white", outline="white"
    )
    
    history.append((stone, position_x, position_y)) # 둔 돌 색, 좌표 저장
    
    last_move_label.config(text=f"Last Move: AI 백돌 ({position_x + 1}, {position_y + 1})")
    
    move_marker(draw_x, draw_y)
    
    
    update_turn() # 턴을 다시 사람한테 넘김
    

#다시시작    
def restart_game():
    global count 
    count = 0 #횟수 리셋 
    history.clear() # 돌 기록 지우기
    background.delete("all") #싹다지우기 
    last_marker = None # 마커 변수도 초기화 
    #기록장 지우기
    for y in range(15):
        for x in range(15):
            board[y][x] = 0
    
    update_turn()

    # 다시 바둑판그리기 
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

    #5월 13일 작업본 3 
    background.bind("<Button-1>", Insertion)
    #여기까지 5월13일 작업본 3


    
#무르기
def undo():
    global count, last_marker
    if not history: # 돌을 하나도 놓지 않았으면 무시
        return
        
    if game_mode == "AI":
        # AI 모드: (내 돌 + AI 돌) 2개를 빼야 다시 내 턴이 됨
        if len(history) >= 2:
            for _ in range(2):
                stone_id, px, py = history.pop() # 기록장에 맨 마지막 돌 지우기
                background.delete(stone_id) # 화면에서 지우기
                board[py][px] = 0 # 착수 기록장에 빈칸(0)으로 변경
                count -= 1 # 턴 되돌리기
        else: # 돌이 1개만 있을 경우엔 1개만 무르기
            stone_id, px, py = history.pop()
            background.delete(stone_id)
            board[py][px] = 0
            count -= 1
    else:
        # 1vs1 모드: 직전에 둔 1개 무르기
        stone_id, px, py = history.pop()
        background.delete(stone_id)
        board[py][px] = 0
        count -= 1

    # 무르기 후 마커 갱신 
    if last_marker is not None:
        background.delete(last_marker)
        last_marker = None 

    if history : # 무르고 나서도 바둑판에 돌이 존재할시에 
        # 그직전의 돌위치를 찾고 빨간 점 다시 찍기 
        _,px,py = history[-1]
        draw_x = px * CELL_SIZE + MARGIN 
        draw_y = py * CELL_SIZE + MARGIN 
        move_marker(draw_x, draw_y)

        
    last_move_label.config(text="Last Move: 무르기 사용됨")
    update_turn()
    background.bind("<Button-1>", Insertion) # ★ 뇌정지 방지: 무르기 시 클릭 기능 재활성화



background.bind("<Button-1>",Insertion)
#왼쪽 마우스 클릭시 바둑알넣는 작업 
root.mainloop() #이거없으면 안된다. 



