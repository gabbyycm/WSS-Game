package model;

import java.time.LocalDateTime;

public class Request {
    private String input;
    private LocalDateTime timestamp;
    private CommandType commandType;

    public Request(String input, CommandType commandType) {
        this.input = input;
        this.timestamp = LocalDateTime.now();
        this.commandType = commandType;
    }

    public String getInput() { return input; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public CommandType getCommandType() { return commandType; }
}
