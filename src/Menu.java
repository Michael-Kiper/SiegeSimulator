import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class Menu extends JFrame implements KeyListener {
    public boolean gameStarted = false;

    public Menu(int width, int height) {
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(width, height);
        this.setResizable(false);
        this.setLocationRelativeTo(null);
        this.setVisible(true);
    }

    public void startMenu() {
        JFrame menuFrame = new JFrame("Siege Simulator Menu");

        // Setup the initial menu
        menuFrame.setPreferredSize(new Dimension(WIDTH, HEIGHT));
        menuFrame.setMaximumSize(new Dimension(WIDTH, HEIGHT));
        menuFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        menuFrame.setResizable(false);
        menuFrame.setVisible(true);
    }

    @Override
    public void keyPressed(KeyEvent k) {
        switch(k.getKeyChar()) {

        }
    }

    @Override
    public void keyTyped(KeyEvent k) {

    }

    @Override
    public void keyReleased(KeyEvent k) {

    }
}
