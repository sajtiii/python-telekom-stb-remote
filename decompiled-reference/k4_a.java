package k4;

/* JADX INFO: compiled from: TaviranyitoConverter.java */
/* JADX INFO: loaded from: classes.dex */
public class a {
    public static int[] a(byte[] bArr) {
        int[] iArr = new int[bArr.length];
        for (int i6 = 0; i6 < bArr.length; i6++) {
            iArr[i6] = bArr[i6] & 255;
        }
        return iArr;
    }

    public static int b(char c6) {
        if (c6 >= '0' && c6 <= '9') {
            return c6 - '0';
        }
        int i6 = 97;
        if (c6 < 'a' || c6 > 'f') {
            i6 = 65;
            if (c6 < 'A' || c6 > 'F') {
                return -1;
            }
        }
        return (c6 + '\n') - i6;
    }

    public static byte[] c(int[] iArr) {
        byte[] bArr = new byte[iArr.length];
        for (int i6 = 0; i6 < iArr.length; i6++) {
            bArr[i6] = (byte) (iArr[i6] & 255);
        }
        return bArr;
    }
}
