package model;

public class Response {
    private String message;
    private float confidence;
    private boolean actionPerformed;

    public Response(String message, float confidence, boolean actionPerformed) {
        this.message = message;
        this.confidence = confidence;
        this.actionPerformed = actionPerformed;
    }

    public String getMessage() { return message; }
    public float getConfidence() { return confidence; }
    public boolean isActionPerformed() { return actionPerformed; }
}
