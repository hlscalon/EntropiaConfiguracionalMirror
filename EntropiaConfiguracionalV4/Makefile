CC = g++
CFLAGS = -O3 -Wall -shared -std=c++14
LIBS = -Isrc/cpp/libs/Aboria/src -Isrc/cpp/libs/Aboria/third-party -Isrc/cpp/libs/pybind11/include
PYTHON = -fPIC `python-config --includes`
DEFINES = -DABORIA_LOG_LEVEL=1 -LOG #-DDEBUG
OBJECT = boost_graph.so
SOURCES = src/cpp/*.cpp

main:
	$(CC) $(CFLAGS) $(LIBS) $(PYTHON) $(DEFINES) $(SOURCES) -o $(OBJECT)
	mv $(OBJECT) src/python

