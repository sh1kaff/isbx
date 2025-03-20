import java.security.SecureRandom;

public class Gen
{
    public static String toBitString(final byte val) { 
        return String.format("%8s", Integer.toBinaryString(val & 0xFF)).replace(' ', '0'); 
    }

    public static void main(String[] args) {
        SecureRandom random = new SecureRandom();
        byte bytes[] = new byte[16];
        random.nextBytes(bytes);

        for (byte b : bytes) System.out.print(toBitString(b));
    }
