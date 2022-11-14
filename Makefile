
OUTFILE		=		outtest.txt

ERRFILE		=		errtest.txt

SRC			+=		TestImplementation.c	\
					TestImplementation.h

OBJ 		=		$(SRC:.c=.o)

CFLAGS 		+=		-g

NAME 		=		ribou_kook

$(NAME):	$(OBJ)
		gcc $(OBJ) $(CFLAGS) -o $(NAME)

all:		$(NAME)

clean:
		rm -rf $(OBJ)

fclean:		clean
		rm -rf $(NAME)

tester_la_recette:
		./kook_ce_truc TestImplementation.kc > $(OUTFILE) 2> $(ERRFILE)

test_binary:
		./$(NAME)

destroy:
		rm -rf $(SRC) $(OUTFILE) $(ERRFILE)


.PHONY: 	all clean fclean tester_la_recette test_binary destroy
