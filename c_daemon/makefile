CC = gcc
# -MMD generate dependency file
# -MP generate phony targets for each dependency, workaround in case a file is removed
CFLAGS_COMPILE = -MMD -MP -Iinclude
CFLAGS_DEBUG = -g -Wall -Wextra
CFLAGS = $(CFLAGS_COMPILE) $(CFLAGS_DEBUG)

LD = gcc
LDFLAGS =


BIN_DIR = bin/
SRC_DIR = src/
BUILD_DIR = build/

SRC_C := $(shell find $(SRC_DIR) -type f -name "*.c")
SRC = $(SRC_C)
OBJ = $(SRC:%=$(BUILD_DIR)%.o)
DEP = $(OBJ:.o=.d)

.PHONY: bin clean

bin: $(BIN_DIR)c_daemon

$(BIN_DIR)c_daemon: $(OBJ)
	@$(LD) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)%.c.o: %.c
	@mkdir -p $(dir $@)
	@$(CC) -c $< -o $@ $(CFLAGS)

clean:
	rm -r $(BUILD_DIR)
	rm -r $(BIN_DIR)

-include $(DEP)
