# Compiler
CC = g++
CFLAGS = -Wall -Wextra -Werror

# Include, Source and Object directories
INCDIR = -I./include
SRCDIR = ./src
OBJDIR = ./out/obj

# Source and Object files
SRCS = $(wildcard $(SRCDIR)/*.cpp)
OBJS = $(patsubst $(SRCDIR)/%.cpp, $(OBJDIR)/%.o, $(SRCS))

# Target executable
TARGET = uc_comm

# Target
all : $(TARGET)

$(OBJS): $(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	$(OBJS): $(OBJDIR)/%.o: $(SRCDIR)/%.cpp
		$(CC) $(CFLAGS) $(INCDIR) -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) main.cpp -o ./out/$@

# Other targets
rebuild_run : 
	make clean
	make all
	make run

run : 
	./out/$(TARGET)

# Clean up object files and executable
clean:
	rm -f $(OBJDIR)/*.o ./out/$(TARGET)
