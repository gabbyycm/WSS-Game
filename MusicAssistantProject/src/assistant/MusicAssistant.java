package assistant;

import model.*;

public class MusicAssistant extends AIAssistant {

    public MusicAssistant(UserProfile user) {
        super(user);
    }

    @Override
    public void greetUser() {
        System.out.println("Hey " + user.getName() + ", ready for some music?");
    }

    @Override
    public Response handleRequest(Request request) {
        String input = request.getInput().toLowerCase();
        String mood = OpenAIAssistant.extractMood(input);

        if (mood.equalsIgnoreCase("happy") ||
            mood.equalsIgnoreCase("chill") ||
            mood.equalsIgnoreCase("sad") ||
            mood.equalsIgnoreCase("focused") ||
            mood.equalsIgnoreCase("focus") ||
            mood.equalsIgnoreCase("relaxed") ||
            mood.equalsIgnoreCase("energetic") ||
            mood.equalsIgnoreCase("calm") ||
            mood.equalsIgnoreCase("nostalgic")) {

            return recommendPlaylist(mood);
        }

        return generateResponse("Sorry, I couldn't find a playlist for that mood.");
    }

    public Response recommendPlaylist(String mood) {
        String playlist = user.getPreferences().getOrDefault("music", "Your Mix") + " - " + mood + " vibes";
        return new Response("Playing playlist: " + playlist, 0.9f, true);
    }
}