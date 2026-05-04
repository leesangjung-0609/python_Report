# 파이썬 오목게임 관련 코드 작업
from tkinter import *

SIZE = 15 # 바둑판 크기 15 x 15 크기로하기위해서 
CELL_SIZE = 40 #한칸 크기를 40픽셀로 일단냅두고 
MARGIN = 40  #바깥여백 40픽셀

count = 0 #바둑알개수


canvas_size = MARGIN * 2 + CELL_SIZE * (SIZE -1)
'''
바둑판 전체 픽셀 크기 
1. MARGIN : 외부요소와의 간격 -> 창 끝에 딱붙은채로 그림나오는거 막을려고 
   MARGIN * 2 : 양쪽 여백 모두 생각한것 width 에선 좌우 , height 에선 상하 여백 

2. CELL_SIZE , SIZE : 바둑판크기 관련 
   15 x 15 면 바둑알을 둘수있는 점은 15개지만 그사이 간격을 긋는 줄은 14개(SIZE - 1)

   한칸 크기(CELL_SIZE)를 40픽셀로 지정했기때메 바둑판자체 크기는 CELL_SIZE * (SIZE - 1)

3. 총크기 1번과 2를 더한거를 나타낸다. 

'''

root = Tk() # 창생성하는거 먼저
root.title("오목게임") #제목 


background = Canvas(root, width = canvas_size, height=canvas_size,bg = "#DEB887")
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


#바둑알 넣기
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
        background.create_oval(
        draw_x - radius , draw_y - radius,
        draw_x + radius , draw_y + radius,
        fill="black" 
        )
    else :
        background.create_oval(
        draw_x - radius , draw_y - radius,
        draw_x + radius , draw_y + radius,
        fill="white" 
        )
    
    



background.bind("<Button-1>",Insertion)
#왼쪽 마우스 클릭시 바둑알넣는 작업 




root.mainloop() #이거없으면 안된다. 