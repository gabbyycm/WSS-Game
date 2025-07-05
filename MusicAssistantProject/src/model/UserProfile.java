package model;

import java.util.Map;

public class UserProfile {
    private String name;
    private int age;
    private Map<String, String> preferences;
    private boolean isPremium;

    public UserProfile(String name, int age, Map<String, String> preferences, boolean isPremium) {
        if (name == null || name.isEmpty()) throw new IllegalArgumentException("Name is required");
        if (age < 0) throw new IllegalArgumentException("Age must be non-negative");
        this.name = name;
        this.age = age;
        this.preferences = preferences;
        this.isPremium = isPremium;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public Map<String, String> getPreferences() { return preferences; }
    public boolean isPremium() { return isPremium; }
}
