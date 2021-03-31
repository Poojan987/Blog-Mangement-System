#include<stdio.h>
#include<conio.h>
#include<windows.h>
#include<ctype.h>
#include<stdlib.h>
#include<stdbool.h>
#include<time.h>
#include<string.h> 

void caseWin(void);
void askValue(void);
void drawBoard(void);
void menuBoll();
void menuTic();
void border();

COORD c = {0, 0};
void setxy (int x, int y)
{
 c.X = x; c.Y = y; // Set X and Y coordinates
 SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), c);
}

int count=0,stop=1,draw=0;
bool win=false;
int input1,input2;
char input11,input22;
char ticPlayer1[50],ticPlayer2[50];
int k=1,pointer;
char x='X',o='O';
char num[9]={'1','2','3','4','5','6','7','8','9'};
char player1[50],player2[50],movie[100],actor[50],actress[50],guess,check[50]={'A','E','I','O','U'},bolly[9]={'B','O','L','L','Y','W','O','O','D'};
int i=0,p=0,j=0,point=5,dash=0,chance=9,m=1,temp=0,w,nineChance=0,nameAsker=0;

int main(){
	top:
	printf("");
	int z;
 	system("color 90");
	border();
	//GAME MAIN MENU
 	setxy(25,25);
	printf("CHOOSE YOUR DESIRED GAME:\n");
	setxy(25,26);
	printf("1.BOLLYWOOD		2.TicTacToe");
	setxy(25,27);
	scanf("%d",&z);
	
	if(z!=1 && z!=2)
	{
		setxy(25,28);
		printf("INVALID ENTRY");
		fflush(stdin);
		goto top;
	}
	else if(z==2)
	{
		system("cls");
		border();
		menuTic();		
		drawBoard();
		askValue();
	}
	else if(z==1)
	{
		system("color F4");
		system("cls");
		border();
		menuBoll();	
		fflush(stdin);
		setxy(25,25);
		printf("ENTER QUESTIONER'S NAME: ");
		scanf("%[^\n]",player1);
		fflush(stdin);
		setxy(25,26);
		printf("ENTER PLAYER'S NAME: ");
		scanf("%[^\n]",player2);
		
		system("cls");
		border();
		setxy(25,25);
		printf("ENTER MOVIE/TV SERIES NAME:\n");
	    
		//ENTERING THE MOVIE/TV SERIES NAME BY QUESTIONER
	    setxy(25,26);
		do
		{
			movieFirstChar:
        		movie[p]=getch();
        	if(movie[0]==8)
        	{
        		goto movieFirstChar;
			}
        	else if(movie[p]==8 && movie[0]!=8)
        	{
        		putch('\b');
        		putch('\0');
        		putch('\b');
        		p--;
        		continue;
			}
    	   	else if(movie[p]!='\r')
			{
				if(movie[p]!=32)
    			{
					printf("*");
				}
				else if(movie[p]==32)
				{
					printf(" ");
				}
			}
			fflush(stdin);		
		p++; 
    	}while(movie[p-1]!='\r'); 
    	movie[p-1]='\0';
    
		//ENTERING THE ACTOR NAME BY QUESTIONER
    	fflush(stdin);
		setxy(25,27);	
    	printf("ENTER THE ACTOR'S/ACTRESS' NAME:\n");
		setxy(25,28);
		fflush(stdin);
	
		do
		{
			actorFirstChar:
        		actor[j]=getch();
        if(actor[0]==8)
        {
        	goto actorFirstChar;
		}
        else if(actor[j]==8 && actor[0]!=8)
        {
        	putch('\b');
        	putch('\0');
        	putch('\b');
        	j--;
        	continue;
        }
      	else if(actor[j]!='\r')
		{
			if(actor[j]!=32)
    		{
				printf("*");
			}
			else if(actor[j]==32)
			{
				printf(" ");
			}
		}		
		fflush(stdin);
		j++; 
    	}while(actor[j-1]!='\r'); 
		actor[j-1]='\0';
    
    	for(i=0;i<strlen(movie);i++)
		{
        	movie[i] = toupper(movie[i]);
    	}
    	
    	system("cls");
    	border();
    	
		setxy(25,25);
    	printf("THE MOVIE TO BE GUESSED IS AS FOLLOWS:\n");
    	setxy(25,26);
    	printf("BOLLYWOOD");
    
    	//PRINTING THE MOVIE NAME WITH VOWELS
    	setxy(25,27);
    	for(i=0;i<p-1;i++)
    	{
    		for(j=0;j<strlen(check);j++)
    		{
    			if(movie[i]==check[j])
    			{
    				printf(" %c ",movie[i]);
    				break;
				}
				else if(movie[i]==32)
				{
					printf("\t\t");
					break;
				}
				else if(j==4)
				{
					printf(" _ ");
					dash++;
				}
			}
		fflush(stdin);
		}
		temp=dash;

		//PLAYER'S TURN FOR GUESSING THE MOVIE/TV SERIES
		charInput:
		printf("\n");
		
		guessAgain:
		
		setxy(25,29);	
		printf("GUESS ANY LETTER: ");
		int guessDash=0;
		guess=getche();
	
		if(isalnum(guess)==0)
		{
			printf("INVALID CHARACTER\n");
			goto guessAgain;
		}
		guess=toupper(guess);
		check[point]=guess;

		printf("\n");
	
		setxy(25,33);
		for(i=0;i<p-1;i++)
   		{
    		for(j=0;j<strlen(check);j++)
    		{
    			if(movie[i]==check[j])
    			{
    				printf(" %c ",movie[i]);
    				break;
				}
				else if(movie[i]==32)
				{
					printf("\t\t");
					break;
				}
				else if(j==point)
				{
					printf(" _ ");
					guessDash++;
				}
			}
			fflush(stdin);
		}
	
	
		if(guessDash==temp )
		{
			setxy(28,31);
			for(i=m;i<=9;i++)
			{
				printf("%c",bolly[i]);
			}
			if(m>=5)
			{
				setxy(28,32);
				printf("THE ACTOR/ACTRESS IN THE MOVIE IS: ");
				puts(actor);
			}
		m++;
		}
		else if(guessDash<temp)
		{
			setxy(28,31);
			for(i=m-1;i<9;i++)
			{
				printf("%c",bolly[i]);
			}
		}
		temp=guessDash;
		nineChance++;
		point++;
		
		if(guessDash<=dash && guessDash>0 && nineChance<=8)
		{
			goto charInput;
		}
		else if(guessDash!=0 && nineChance>8)
		{
			setxy(25,37);
			printf("YOU LOSE! :( THE MOVIE IS: ");
			puts(movie);
		}
	}
	setxy(25,50);
	return 0;
}

//----------	END OF BOTH THE GAME	----------//

//FUNCTIONS FOR TIC TAC TOE

	//FUNCTION FOR DECIDING WINNER
	void caseWin(void)
	{
		win=false;
		if((num[0]==num[1] && num[1]==num[2]) || (num[3]==num[4]) && (num[4]==num[5]) || (num[6]==num[7]) && (num[7]==num[8]))
		{
			win=true;
			system("cls");
			
			if(k % 2 != 0)
			{
				border();
				setxy(60,20);
				printf("%s IS WINNER",ticPlayer1);
				drawBoard();
			}
			else if(k % 2 ==0)
			{
				border();
				setxy(60,20);
				printf("%s IS WINNER",ticPlayer2);
				drawBoard();
			}
		}
		else if((num[0]==num[3] && num[3]==num[6]) || (num[1]==num[4]) && (num[4]==num[7]) || (num[2]==num[5]) && (num[5]==num[8]))
		{
			win=true;	
			system("cls");
			
			if(k % 2 != 0)
			{
				border();
				setxy(60,20);	
				printf("%s IS WINNER",ticPlayer1);
				drawBoard();
			}
			else if(k % 2 ==0)
			{
				border();
				setxy(60,20);
				printf("%s IS WINNER",ticPlayer2);
				drawBoard();
			}
		}
		else if((num[0]==num[4] && num[4]==num[8]) || (num[2]==num[4]) && (num[4]==num[6]) )
		{
			win=true;	
			system("cls");
		
			if(k % 2 != 0)
			{
				setxy(60,20);
				printf("%s IS WINNER",ticPlayer1);
				drawBoard();
			}
			else if(k % 2 ==0)
			{
				setxy(60,20);
				printf("%s IS WINNER",ticPlayer2);
				drawBoard();
			}
		}
		else if(k==9)
		{
			win=true;
			system("cls");
			setxy(60,20);
			printf("THIS GAME HAS RESULTED IN A DRAW\n");
			drawBoard();
		}
		else 
		{
			win=false;
		}
		
		if(win != true)
		{
			system("cls");
			drawBoard();
		}
	}
	
		
	
	//FUNCTION FOR ASKING VALUES ON BOARD
	
	void askValue(void)
	{
		if(k % 2 != 0)
		{
			fflush(stdin);
			setxy(25,40);
			printf("%s PLEASE ENTER A NUMBER: ",ticPlayer1);
			scanf("%d",&input1);
			fflush(stdin);
			if((input1<0 || input1>9 || num[input1-1]=='X' || num[input1-1]=='O'))
			{
				setxy(25,41);
				printf("INVALID NUMBER\n"); 
			}
			else
			{
				num[input1-1]=o;
				system("cls");
				caseWin();
				k++;
			}
		}
		else if(k % 2 == 0)
		{
			setxy(25,40);
			printf("%s PLEASE ENTER A NUMBER: ",ticPlayer2);
			scanf("%d",&input2);
			fflush(stdin);
			if((input2<0 || input2>9 || num[input2-1]=='X' || num[input2-1]=='O'))
			{
			setxy(25,41);
			printf("INVALID NUMBER\n");
			}
			else
			{
				num[input2-1]=x;
				system("cls");
				caseWin();
				k++;
			}
		}
		if(k<=9 && win!=true)
		{
			askValue();
		}
	}
	//FUNCTION FOR DRAWING THE TIC TAC TOE BOARD
	
	void drawBoard(void)
	{
		system("color 0a");
		border();
		setxy(60,10);	
		printf("--- TIC TAC TOE ---");
		
		if(nameAsker==0)
		{
			fflush(stdin);
			setxy(35,15);
			printf("PLAYER 1, ENTER YOUR NAME: ");
			scanf("%[^\n]",ticPlayer1);
			strupr(ticPlayer1);
			
			fflush(stdin);
			
			setxy(35,17);
			printf("PLAYER 2, ENTER YOUR NAME: ");
			scanf("%[^\n]",ticPlayer2);
			strupr(ticPlayer2);
			nameAsker++;
		}
		setxy(55,26);
		printf("%s (O)  -  %s (X)\n\n\n",ticPlayer1,ticPlayer2);
		count=0;

		for(i=0; i<9; i++) 
		{
			for(j=0; j<76; j++) 
			{
				if(j==61 || j==67) 
				{
				printf("|");
				} 
				else if(i==2 || i==5)
				{
					if(j>=56 && j<=72)
					{
						printf("_");
					}
					else
					{
						printf(" ");
					}
				}
				else if(i==1 || i==4 || i==7)
				{
					if(j==58|| j==64 || j==70)
					{
						printf("%c",num[count]);
						count++;
					}
					else
					{
						printf(" ");
					}
				}
				else
				{
				printf(" ");
				}
			}
		printf("\n");
		}
	border();
	}

void menuTic()
{
	//TIC TAC TOE MAIN MENU
	system("color 0a");
	int select;
	setxy(25,25);
	printf("1.START TicTacToe\n");
	setxy(25,26);
	printf("2.HOW TO PLAY TicTacToe\n");
	setxy(25,27);
	printf("3.QUIT\n");
	setxy(25,29);
	printf("ENTER YOUR CHOICE: ");
	scanf("%d",&select);
	
	FILE *fp;
	char ch;
	
	switch (select)
	{
		//GAME START PROGRAM
		case 1:		
			system("cls");
			border();
			setxy(25,25);
			break;
			
		//GAME DESCRIPTION
		case 2:
			system("cls");
			fp = fopen("How to Play - 1.txt","r");
			ch = fgetc(fp);
			while(ch != EOF)
			{
			printf("%c",ch);
			ch=fgetc(fp);
			}
			fclose(fp);
			menuTic();
			break;
		
		//GAME QUIT PROGRAM
		case 3:
			system("cls");
			setxy(25,31);
			exit(0);
			break;
		
		//INVALID ENTRY PROGRAM
		default:
			setxy(25,31);
			printf("INVALID ENTRY\n");
			fflush(stdin);
			menuTic();	}
}


void menuBoll()
{
	//BOLLYWOOD MAIN MENU
	system("color F4");
	int select;
	setxy(25,25);
	printf("1.START BOLLYWOOD");
	setxy(25,26);
	printf("2.HOW TO PLAY BOLLYWOOD");
	setxy(25,27);
	printf("3.QUIT");
	setxy(25,29);
	printf("ENTER YOUR CHOICE: ");
	scanf("%d",&select);
	
	FILE *fp1;
	char ch1;
	
	switch (select)
	{
		//GAME START PROGRAM
		case 1:
			system("cls");
			border();
			setxy(25,25);
			break;
			
		//GAME DESCRIPTION
		case 2:
			system("cls");
			fp1 = fopen("How to Play - 2.txt","r");
			ch1 = fgetc(fp1);
			while(ch1 != EOF)
			{
			printf("%c",ch1);
			ch1=fgetc(fp1);
			}
			fclose(fp1);
			printf("\n");
			menuBoll();
			break;
		
		//GAME QUIT PROGRAM
		case 3:
			system("cls");
			setxy(25,31);
			exit(0);
			break;
		
		//INVALID ENTRY PROGRAM
		default:
			setxy(25,31);
			printf("INVALID ENTRY");
			fflush(stdin);
			menuBoll();		
	}
}
//BORDER AROUND THE GAME
void border()
{
	//TOP BORDER LINE
 	setxy(15,5); 
 	for(w=0; w<100; w++)
 	{
 		printf("%c", 223);
	}
 
 	//BOTTOM BORDER LINE
 	setxy(15,45);
 	for(w=0; w<=100; w++)
 	{
 		printf("%c", 223);
	}

 	//LEFT AND RIGHT BORDER LINE
 	for(w=0; w<40; w++)
 	{
  		setxy(15,5+w);
  		printf("%c",219);	 
  		setxy(115,5+w);
  		printf("%c",219);
   		printf("\n");
	}
}