CC=gcc
CFLAGS=-I.
DEPS = log.h listen.h
OBJ = main.o listen.o log.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
clean:
	rm -f $(OBJ) main
