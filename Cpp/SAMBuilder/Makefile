CC=gcc
CXX=g++ -std=c++11 
RM=rm -f
CPPFLAGS= -I/usr/local/include  -g
LDFLAGS= 
LDLIBS=/usr/local/lib/libjansson.a

SRCS=ConcreteShearWall.cpp \
	SAMBuilder.cpp 

OBJS= ConcreteShearWall.o 

all: SAMBuilder 

SAMBuilder.o: SAMBuilder.cpp

ConcreteShearWall.o: ConcreteShearWall.cpp

SAMBuilder: $(OBJS) SAMBuilder.o
	$(CXX) $(LDFLAGS) -o SAMBuilder SAMBuilder.o $(OBJS) $(LDLIBS)

clean:
	$(RM) $(OBJS) *~ \#* SAMBuilder.o

distclean: clean
	$(RM) SAMBuilder 


