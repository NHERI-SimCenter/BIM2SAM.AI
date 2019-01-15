CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS= -I /usr/local/include
LDFLAGS= 
LDLIBS=/usr/local/lib/libjansson.a

SRCS=TclBuilder.o TclBuilder.cpp \
	OpenSeesTclBuilder.cpp 

OBJS_PRE=TclBuilder.o OpenSeesTclBuilder.o

all: TclBuilder

debug: CPPFLAGS += -DDEBUG -g
debug: all

OpenSeesTclBuilder.o: OpenSeesTclBuilder.cpp OpenSeesTclBuilder.h


TclBuilder.o: TclBuilder.cpp OpenSeesTclBuilder.h


TclBuilder: $(OBJS_PRE)
	$(CXX) $(LDFLAGS) -o TclBuilder $(OBJS_PRE) $(LDLIBS) 

clean:
	$(RM) *~ \#* *.o *.out

distclean: clean
	$(RM) TclBuilder 


