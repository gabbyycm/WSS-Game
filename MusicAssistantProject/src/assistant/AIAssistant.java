package assistant;

import model.Request;
import model.Response;
import model.UserProfile;

public abstract class AIAssistant {
    protected UserProfile user;

    public AIAssistant(UserProfile user) {
        this.user = user;
    }

    public abstract void greetUser();
    public abstract Response handleRequest(Request request);

    public Response generateResponse(String msg) {
        return new Response(msg, 0.5f, false);
    }
}
