import assistant.MusicAssistant;
import model.*;

import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Welcome! What's your name? ");
        String name = scanner.nextLine();

        System.out.print("How old are you? ");
        int age = Integer.parseInt(scanner.nextLine());

        System.out.print("What's your favorite genre (e.g., Pop, Lo-Fi, Rock)? ");
        String genre = scanner.nextLine();

        boolean isPremium = true;

        UserProfile user = new UserProfile(name, age, Map.of("music", genre), isPremium);
        MusicAssistant assistant = new MusicAssistant(user);

        assistant.greetUser();

        while (true) {
            System.out.print("\nEnter your music request (or type 'exit' to quit): ");
            String input = scanner.nextLine();
            if (input.equalsIgnoreCase("exit")) {
                System.out.println("Goodbye!");
                break;
            }

            Request request = new Request(input, CommandType.MUSIC);
            Response response = assistant.handleRequest(request);
            System.out.println("Assistant: " + response.getMessage());
        }

        scanner.close();
    }
}