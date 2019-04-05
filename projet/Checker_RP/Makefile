all: Checker

Instance.o: Instance.cpp  Instance.h
	g++ -c Instance.cpp

Checker.o: Checker.cpp Instance.h
	g++ -c Checker.cpp

Checker: Instance.o Checker.o
	g++ -o Checker Checker.o Instance.o

clean:
	rm Checker
	rm -f *.o
