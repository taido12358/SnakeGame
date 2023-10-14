uses crt;
const arenaSize=20;  //The size of the arena
startingSpeed=120;   //The starting speed(smaller=faster)
startingSize=18;     //The starting size of the snake
snakeColor=10;       //The snake color
foodColor=14;        //The food color
wallColor=9;         //The wall color
var xfood,yfood,count,size,cycle,i,last,first,score,negativePoints,food:integer;
keyCheck,sizeChange,foodNotOnSnake:boolean;
direction,d2:string;
speed:real;
Snake:array [1..2, 1..4000] of integer;
ch:char;
label start,lose;
begin
start:
begin
        clrscr;
        randomize;
        size:=startingSize+1;
        first:=size-1;
        speed:=startingSpeed;
        last:=0;
        score:=0;
        food:=0;
        negativePoints:=0;
        for count:=size downto 1 do
        begin
           snake[1,count]:=count+1;
           snake[2,count]:=2;
        end;
        direction:='right';
        repeat
        FoodNotOnSnake:=true;
        xfood:=random(arenaSize+8)+2;
        yfood:=random(arenaSize-2)+2;
        for i:=1 to first do
           for count:=first to size+1 do
              if ((xfood=snake[1,count])and(yfood=snake[2,count]))or((xfood=snake[1,i])and(yfood=snake[2,i])) then
                 foodNotOnSnake:=false;
        until foodNotOnSNake;
        xfood:=random(arenaSize+8)+2;
        yfood:=random(arenaSize-2)+2;
        textcolor(wallColor);
        gotoxy(1,1); 
        write('+');                     {4 goc xung quanh}
        gotoxy(arenaSize+10,1);
        write('+');
        gotoxy(1,arenaSize);
        write('+');
        gotoxy(arenaSize+10,arenaSize);
        write('+');
        for i:=2 to arenaSize+9 do
        begin
           gotoxy(i,1);
           write('_');                 {Tuong Ngang}
           gotoxy(i,arenaSize);
           write('_');
        end;
        for i:=2 to arenaSize-1 do
        begin
           gotoxy(1,i);                      
           write('/');                {Tuong doc}
           gotoxy(arenaSize+10,i);
           write('/');
        end;
        textcolor(white);
        while (true) do
        begin
        speed:=speed-0.01;
        textcolor(foodColor);
        gotoxy(xfood,yfood);
        write('O');
        textcolor(white);
        for count:=1 to size do
        begin
           textcolor(snakeColor);
           gotoxy(snake[1,count],snake[2,count]);
           if count=first+1 then
           begin
              case direction of
                 'up':write('C');              {Dau ran}
                 'down':write('C');
                 'left':write('C');
                 'right':write('C');
              end;
           end
           else
              write(#249);
           textcolor(white);
        end;
        gotoxy(1,1);
        for i:=1 to first-1 do
           for count:=first+1 to size-1 do
              if ((snake[1,first]=snake[1,count])and(snake[2,first]=snake[2,count]))or((snake[1,first]=snake[1,i])and(snake[2,first]=snake[2,i])) then
                 goto lose;
        sizeChange:=false;
        if (xfood=snake[1,first])and(yfood=snake[2,first]) then
        begin
           size:=size+1;
           snake[1,size]:=snake[1,last];
           snake[2,size]:=snake[2,last];
           sizeChange:=true;
           inc(food);
           speed:=speed-1;
           repeat
           FoodNotOnSnake:=true;
           xfood:=random(arenaSize+8)+2;
           yfood:=random(arenaSize-2)+2;
           for i:=1 to first-1 do
              for count:=first+1 to size+1 do
                 if ((xfood=snake[1,count])and(yfood=snake[2,count]))or((xfood=snake[1,i])and(yfood=snake[2,i])) then
                    foodNotOnSnake:=false;
        until foodNotOnSNake;
        end
        else inc(negativePoints);
        begin
        if last=size then
           last:=1
        else
           inc(last);
        end;
        if sizeChange then
        begin
           if first=size-1 then
              first:=1
           else
              inc(first);
        end
        else
        begin
        if first=size then
           first:=1
        else
           inc(first);
        end;
        gotoxy(snake[1,last],snake[2,last]);
        write(' ');
        if (snake[1,first]<2)or(snake[2,first]<2)or(snake[1,first]>=arenaSize+10)or(snake[2,first]>=arenaSize) then
           goto lose;
        if keypressed then
        begin
           ch:=readkey;
           if ch='p' then
              ch:=readkey;
           if ch=#0 then
           begin
              ch:=readkey;
              case ch of
                 #72:if direction<>'down' then
                        direction:='up';
                 #80:if direction<>'up' then
                        direction:='down';
                 #75:if direction<>'right' then
                        direction:='left';
                 #77:if direction<>'left' then
                        direction:='right';
              end;
           end
           else
           if ch=#27 then
              exit;
        end;
        if direction='left' then
        begin
           snake[1,last]:=snake[1,first]-1;
           snake[2,last]:=snake[2,first];
        end;
        if direction='right' then
        begin
           snake[1,last]:=snake[1,first]+1;
           snake[2,last]:=snake[2,first];
        end;
        if direction='up' then
        begin
           snake[1,last]:=snake[1,first];
           snake[2,last]:=snake[2,first]-1;
        end;
        if direction='down' then
        begin
           snake[1,last]:=snake[1,first];
           snake[2,last]:=snake[2,first]+1;
        end;
        score:=food*100-negativePoints;
        if score<0 then
           score:=0;
        gotoxy(5,arenaSize+1);
        write('Eaten food:',food);
        delay(round(speed));
        end;
end;
        lose:
        begin
           textcolor(12);
           gotoxy(arenaSize+11,1);
           writeln('Moi duoc co ',score,' diem da die roi');
           gotoxy(arenaSize+11,2);
           write('Nhan esc de quay lai');
           repeat
              ch:=readkey;
              if ch=#13 then
                 goto start;
           until ch=#27;
        end;
end.
