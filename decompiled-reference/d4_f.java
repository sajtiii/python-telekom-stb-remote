package d4;

import java.math.BigInteger;

/* JADX INFO: compiled from: TaviranyitoMACHelper.java */
/* JADX INFO: loaded from: classes.dex */
public class f {
    private static long a(BigInteger bigInteger) {
        long jE = c.e(bigInteger);
        long jF = c.f(bigInteger);
        long j6 = (jE << 1) & 4294967295L;
        if (j6 >= 2147483647L) {
            j6 = (j6 - 2147483647L) & 4294967295L;
        }
        if (jF >= 2147483647L) {
            jF -= 2147483647L;
        }
        long j7 = (j6 + jF) & 4294967295L;
        return j7 >= 2147483647L ? (j7 - 2147483647L) & 4294967295L : j7;
    }

    public static BigInteger b(int[] iArr, int i6, BigInteger bigInteger, long j6, long j7, long j8) {
        int i7 = i6 / 4;
        BigInteger bigInteger2 = new BigInteger("0");
        BigInteger bigInteger3 = new BigInteger(Long.toString(a(new BigInteger(Long.toString(c.f(bigInteger))))));
        BigInteger bigInteger4 = new BigInteger(Long.toString(a(new BigInteger(Long.toString(c.e(bigInteger))))));
        BigInteger bigInteger5 = new BigInteger(Long.toString(j6));
        BigInteger bigInteger6 = new BigInteger(Long.toString(j7));
        BigInteger bigInteger7 = new BigInteger(Long.toString(j8));
        BigInteger bigIntegerMultiply = bigInteger7.multiply(new BigInteger(Long.toString(c.h(iArr, 0))));
        BigInteger bigInteger8 = c.f5647b;
        BigInteger bigInteger9 = new BigInteger(Long.toString(a(bigInteger3.multiply(new BigInteger(Long.toString(a(bigIntegerMultiply.and(bigInteger8))))).add(bigInteger4).and(bigInteger8))));
        BigInteger bigIntegerAnd = bigInteger2.add(bigInteger9).and(bigInteger8);
        BigInteger bigInteger10 = new BigInteger(Long.toString(a(bigInteger5.multiply(new BigInteger(Long.toString(a(bigInteger9.add(new BigInteger(Long.toString(c.h(iArr, 4)))).and(bigInteger8))))).add(bigInteger6).and(bigInteger8))));
        BigInteger bigIntegerAnd2 = bigIntegerAnd.add(bigInteger10).and(bigInteger8);
        int i8 = 1;
        int i9 = 2;
        while (i8 < (i7 >> 1)) {
            int i10 = i9 + 1;
            BigInteger bigIntegerAdd = bigInteger7.multiply(new BigInteger(Long.toString(c.h(iArr, i9 << 2)))).add(bigInteger10);
            BigInteger bigInteger11 = c.f5647b;
            BigInteger bigInteger12 = new BigInteger(Long.toString(a(bigInteger3.multiply(new BigInteger(Long.toString(a(bigIntegerAdd.and(bigInteger11))))).add(bigInteger4).and(bigInteger11))));
            BigInteger bigIntegerAnd3 = bigIntegerAnd2.add(bigInteger12).and(bigInteger11);
            BigInteger bigInteger13 = new BigInteger(Long.toString(a(bigInteger5.multiply(new BigInteger(Long.toString(a(bigInteger12.add(new BigInteger(Long.toString(c.h(iArr, i10 << 2)))).and(bigInteger11))))).add(bigInteger6).and(bigInteger11))));
            bigIntegerAnd2 = bigIntegerAnd3.add(bigInteger13).and(bigInteger11);
            i8++;
            bigInteger10 = bigInteger13;
            i9 = i10 + 1;
        }
        BigInteger bigIntegerAdd2 = bigInteger10.add(bigInteger4);
        BigInteger bigInteger14 = c.f5647b;
        return c.g(c.f(new BigInteger(Long.toString(a(bigIntegerAnd2.add(bigInteger6).and(bigInteger14))))), c.f(new BigInteger(Long.toString(a(bigIntegerAdd2.and(bigInteger14))))));
    }

    public static BigInteger c(int[] iArr, int[] iArr2, int[] iArr3, int i6) {
        int i7 = i6 / 8;
        int[] iArr4 = new int[8];
        for (int i8 = 0; i8 < i7; i8++) {
            for (int i9 = 0; i9 < 8; i9++) {
                iArr4[i9] = iArr4[i9] ^ iArr3[(i8 * 8) + i9];
            }
            e(iArr, iArr2, iArr4);
        }
        return c.i(iArr4, 0);
    }

    public static void d(int[] iArr, int[] iArr2, int[] iArr3) {
        for (int i6 = 1; i6 <= 8; i6++) {
            int i7 = iArr3[0];
            iArr3[0] = ((((i7 << 7) | (i7 >> 1)) & 255) - iArr2[((iArr[7] + iArr3[7]) + i6) & 255]) & 255;
            for (int i8 = 6; i8 >= 0; i8--) {
                int i9 = i8 + 1;
                int i10 = iArr3[i9];
                iArr3[i9] = ((((i10 << 7) | (i10 >> 1)) & 255) - iArr2[((iArr[i8] + iArr3[i8]) + i6) & 255]) & 255;
            }
        }
    }

    public static void e(int[] iArr, int[] iArr2, int[] iArr3) {
        for (int i6 = 8; i6 > 0; i6--) {
            int i7 = 0;
            while (i7 < 7) {
                int i8 = i7 + 1;
                int i9 = (iArr3[i8] + iArr2[(iArr[i7] + iArr3[i7] + i6) & 255]) & 255;
                iArr3[i8] = ((i9 >> 7) | (i9 << 1)) & 255;
                i7 = i8;
            }
            int i10 = (iArr3[0] + iArr2[(iArr[i7] + iArr3[i7] + i6) & 255]) & 255;
            iArr3[0] = ((i10 >> 7) | (i10 << 1)) & 255;
        }
    }
}
