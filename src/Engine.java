import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.util.Random;

public class Engine {
    private static final int WIDTH = 900;
    private static final int HEIGHT = 500;
    private File CWD = new File(System.getProperty("user.dir"));
    public JFrame gameFrame = new JFrame("Siege Simulator");


    public void init() {
        // Create the frame
        gameFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        gameFrame.setSize(WIDTH, HEIGHT);
        gameFrame.setResizable(false);
        gameFrame.setLocationRelativeTo(null);

        String seedString = "123425aad3";
        long validString = errorHandleSeed(seedString);
        if (validString == -1) {
            return;
        }

        runGame(validString);
    }


    // Returns seed if valid string; -1 otherwise
    public long errorHandleSeed(String seedString) {
        seedString = seedString.toLowerCase().replaceAll("[a-z]", "");

        if (seedString.length() == 0) {
            return -1;
        }
        long seed = Long.parseLong(seedString);
        if (seed > 9223372036854775807L) {
            return -1;
        }
        return seed;
    }


    public void runGame(long seed) {
        //create the pseudo-random positions for the agents
        Random psuedoRand = new Random(seed);

        //import the Special Agent
        Agent agent = new Agent(1, psuedoRand, WIDTH, HEIGHT, CWD);
        agent.startingCoords(psuedoRand, WIDTH, HEIGHT);
        gameFrame.add(agent.label);


        gameFrame.setVisible(true);
    }
}
