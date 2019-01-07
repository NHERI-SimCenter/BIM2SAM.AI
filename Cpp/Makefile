CC=gcc
CXX=g++ -std=c++11 
RM=rm -f
CPPFLAGS= -I/usr/local/include  -g
LDFLAGS= 
LDLIBS=/usr/local/lib/libjansson.a

SRCS=ConcreteShearWall.cpp \
	createSAM.cpp 

OBJS= ConcreteShearWall.o 

all: createSAM 

createSAM.o: createSAM.cpp

ConcreteShearWall.o: ConcreteShearWall.cpp

createSAM: $(OBJS) createSAM.o
	$(CXX) $(LDFLAGS) -o createSAM createSAM.o $(OBJS) $(LDLIBS)

clean:
	$(RM) $(OBJS) *~ \#* createSAM.o

distclean: clean
	$(RM) createSAM 


