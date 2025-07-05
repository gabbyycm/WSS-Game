package assistant;

public class OpenAIAssistant {
    public static String extractMood(String userInput) {
        userInput = userInput.toLowerCase();

        if (userInput.contains("happy")) return "happy";
        if (userInput.contains("chill")) return "chill";
        if (userInput.contains("sad")) return "sad";
        if (userInput.contains("focus") || userInput.contains("study")) return "focused";
        if (userInput.contains("relax")) return "relaxed";
        if (userInput.contains("energy") || userInput.contains("workout")) return "energetic";
        if (userInput.contains("calm")) return "calm";
        if (userInput.contains("nostalgia") || userInput.contains("90s")) return "nostalgic";

        return "unknown";
    }
}