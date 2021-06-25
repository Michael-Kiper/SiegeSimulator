import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.IOException;
import java.util.Random;
import java.awt.*;

public class Agent extends JPanel implements KeyListener {
    public Point pos;
    private int radius = 10;
    private Image pic;
    public JLabel label;
    public int health;


    Agent(int startingHealth, Random r, int width, int height, File cwd) {
        label = new JLabel();
        label.setBounds(0, 0, radius*2, radius*2);
        //label.setBackground(Color.black);
        label.setOpaque(true);

        String imagePath = cwd.toString() + "/Images/agent.png";
        try { pic = ImageIO.read(new File(imagePath)); }
        catch (IOException e) { e.printStackTrace(); }

        health = startingHealth;

        this.startingCoords(r, width, height);

        addKeyListener(this);
    }

    public void startingCoords(Random r, int width, int height) {
        pos = new Point(0, 0);
        int maxX = width/2 - (radius + 2) - 20; //the 20 is a buffer
        int minX = radius + 2;
        pos.x = r.nextInt(maxX) + minX;

        int maxY = height - (radius + 2) - 20;
        int minY = radius + 2;
        pos.y = r.nextInt(maxY) + minY;

        label.setLocation(pos);
    }

    public void drawAgent(Graphics g, Component c) {
        if (health > 0) {
            g.drawImage(pic, pos.x, pos.y, radius, radius, c);
        }
    }

    // Methods to change the position of the agent
    @Override
    public void keyTyped(KeyEvent k) {
        System.out.println(k.getKeyChar());
        switch(k.getKeyChar()) {
            case 'w' : pos.translate(0, 1);
                break;
            case 'a' : pos.translate(-1, 0);
                break;
            case 's' : pos.translate(0, -1);
                break;
            case 'd' : pos.translate(1, 0);
                break;
        }
    }

    @Override
    public void keyPressed(KeyEvent k) {

    }

    @Override
    public void keyReleased(KeyEvent k) {

    }
}
