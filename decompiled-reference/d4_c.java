package d4;

import android.util.Log;
import java.math.BigInteger;
import java.util.Arrays;

/* JADX INFO: compiled from: TaviranyitoCSParve64.java */
/* JADX INFO: loaded from: classes.dex */
public class c {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    public static final BigInteger f5646a = new BigInteger("4294967295");

    /* JADX INFO: renamed from: b, reason: collision with root package name */
    public static final BigInteger f5647b = new BigInteger("18446744073709551615");

    /* JADX INFO: renamed from: c, reason: collision with root package name */
    public static final BigInteger f5648c = new BigInteger(Integer.toString(255));

    public static void a(int[] iArr, b bVar, int[] iArr2, int[] iArr3, int i6) {
        Log.d("XmlParser", "CS64Decrypt.length: " + i6);
        Log.d("XmlParser", "CS64Decrypt.key: " + Arrays.toString(iArr));
        Log.d("XmlParser", "CS64Decrypt.csKey: " + bVar);
        Log.d("XmlParser", "CS64Decrypt.sBox: " + Arrays.toString(iArr2));
        Log.d("XmlParser", "CS64Decrypt.data: " + Arrays.toString(iArr3));
        int[] iArr4 = new int[8];
        int i7 = i6 + (-8);
        System.arraycopy(iArr3, i7, iArr4, 0, 8);
        for (int i8 = 0; i8 < 8; i8++) {
            Log.d("", "pMac[" + i8 + "]" + iArr4[i8] + "");
        }
        new a(iArr4).a(i7, iArr3);
        f.d(iArr, iArr2, iArr4);
        k(bVar.b(iArr3, i6, i(iArr4, 0)), iArr3, i7);
    }

    public static void b(int[] iArr, b bVar, int[] iArr2, int[] iArr3, int i6) {
        for (int i7 = 0; i7 < iArr.length; i7++) {
        }
        for (int i8 = 0; i8 < iArr2.length; i8++) {
        }
        int[] iArr4 = new int[8];
        k(bVar.a(iArr3, i6 / 4), iArr4, 0);
        f.e(iArr, iArr2, iArr4);
        int i9 = i6 - 8;
        System.arraycopy(iArr4, 0, iArr3, i9, 8);
        new a(iArr4).a(i9, iArr3);
    }

    public static BigInteger c(int[] iArr, int[] iArr2, long j6, long j7, long j8, int[] iArr3, int i6, b bVar) {
        for (int i7 = 0; i7 < iArr.length; i7++) {
            Log.d("CS64Hash", "Key[" + i7 + "]" + iArr[i7]);
        }
        Log.d("CS64Hash", "C=" + j6);
        Log.d("CS64Hash", "D=" + j7);
        Log.d("CS64Hash", "E=" + j8);
        for (int i8 = 0; i8 < iArr3.length; i8++) {
            Log.d("CS64Hash", "InText[" + i8 + "]" + iArr3[i8]);
        }
        Log.d("CS64Hash", "intextLeght=" + i6);
        BigInteger bigIntegerC = f.c(iArr, iArr2, iArr3, i6);
        b bVar2 = new b(bigIntegerC, j6, j7, j8);
        bVar.m(bVar2.e());
        bVar.n(bVar2.f());
        bVar.o(bVar2.g());
        bVar.p(bVar2.h());
        bVar.q(bVar2.i());
        bVar.r(bVar2.j());
        bVar.s(bVar2.k());
        bVar.t(bVar2.l());
        BigInteger bigIntegerXor = bVar.a(iArr3, i6 / 4).xor(bigIntegerC);
        Log.d("TaviranyitoCSParve64", "outHash" + bigIntegerXor);
        return bigIntegerXor;
    }

    public static BigInteger d(int[] iArr, int[] iArr2, long j6, long j7, long j8, int[] iArr3, int i6) {
        BigInteger bigIntegerC = f.c(iArr, iArr2, iArr3, i6);
        BigInteger bigIntegerXor = bigIntegerC.xor(f.b(iArr3, i6, bigIntegerC, j6, j7, j8));
        BigInteger bigIntegerXor2 = bigIntegerXor.xor(g.b(iArr3, i6, bigIntegerXor));
        return bigIntegerXor2.xor(g.a(iArr3, i6, bigIntegerXor2));
    }

    public static long e(BigInteger bigInteger) {
        return bigInteger.shiftRight(32).and(f5646a).longValue();
    }

    public static long f(BigInteger bigInteger) {
        return bigInteger.and(f5646a).longValue();
    }

    public static BigInteger g(long j6, long j7) {
        return new BigInteger(Long.toString(j6)).shiftLeft(32).or(new BigInteger(Long.toString(j7))).and(f5647b);
    }

    public static long h(int[] iArr, int i6) {
        int i7 = i6 + 1;
        long j6 = ((long) iArr[i6]) << 24;
        int i8 = i7 + 1;
        long j7 = j6 | (((long) iArr[i7]) << 16);
        int i9 = i8 + 1;
        return ((long) iArr[i9]) | j7 | (((long) iArr[i8]) << 8);
    }

    public static BigInteger i(int[] iArr, int i6) {
        int i7 = i6 + 1;
        BigInteger bigIntegerShiftLeft = new BigInteger(Integer.toString(iArr[i6])).shiftLeft(56);
        int i8 = i7 + 1;
        BigInteger bigIntegerShiftLeft2 = new BigInteger(Integer.toString(iArr[i7])).shiftLeft(48);
        int i9 = i8 + 1;
        BigInteger bigIntegerShiftLeft3 = new BigInteger(Integer.toString(iArr[i8])).shiftLeft(40);
        int i10 = i9 + 1;
        BigInteger bigIntegerShiftLeft4 = new BigInteger(Integer.toString(iArr[i9])).shiftLeft(32);
        int i11 = i10 + 1;
        BigInteger bigIntegerShiftLeft5 = new BigInteger(Integer.toString(iArr[i10])).shiftLeft(24);
        int i12 = i11 + 1;
        BigInteger bigIntegerShiftLeft6 = new BigInteger(Integer.toString(iArr[i11])).shiftLeft(16);
        BigInteger bigIntegerShiftLeft7 = new BigInteger(Integer.toString(iArr[i12])).shiftLeft(8);
        return bigIntegerShiftLeft.or(bigIntegerShiftLeft2).or(bigIntegerShiftLeft3).or(bigIntegerShiftLeft4).or(bigIntegerShiftLeft5).or(bigIntegerShiftLeft6).or(bigIntegerShiftLeft7).or(new BigInteger(Integer.toString(iArr[i12 + 1])));
    }

    public static void j(long j6, int[] iArr, int i6) {
        int i7 = i6 + 1;
        iArr[i6] = (int) ((j6 >> 24) & 255);
        int i8 = i7 + 1;
        iArr[i7] = (int) ((j6 >> 16) & 255);
        iArr[i8] = (int) ((j6 >> 8) & 255);
        iArr[i8 + 1] = (int) (j6 & 255);
    }

    public static void k(BigInteger bigInteger, int[] iArr, int i6) {
        int i7 = i6 + 1;
        BigInteger bigIntegerShiftRight = bigInteger.shiftRight(56);
        BigInteger bigInteger2 = f5648c;
        iArr[i6] = (int) bigIntegerShiftRight.and(bigInteger2).longValue();
        int i8 = i7 + 1;
        iArr[i7] = (int) bigInteger.shiftRight(48).and(bigInteger2).longValue();
        int i9 = i8 + 1;
        iArr[i8] = (int) bigInteger.shiftRight(40).and(bigInteger2).longValue();
        int i10 = i9 + 1;
        iArr[i9] = (int) bigInteger.shiftRight(32).and(bigInteger2).longValue();
        int i11 = i10 + 1;
        iArr[i10] = (int) bigInteger.shiftRight(24).and(bigInteger2).longValue();
        int i12 = i11 + 1;
        iArr[i11] = (int) bigInteger.shiftRight(16).and(bigInteger2).longValue();
        iArr[i12] = (int) bigInteger.shiftRight(8).and(bigInteger2).longValue();
        iArr[i12 + 1] = (int) bigInteger.and(bigInteger2).longValue();
    }
}
