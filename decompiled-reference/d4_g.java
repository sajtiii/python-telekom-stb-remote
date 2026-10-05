package d4;

import java.math.BigInteger;

/* JADX INFO: compiled from: TaviranyitoWordSwapHelper.java */
/* JADX INFO: loaded from: classes.dex */
public class g {
    public static BigInteger a(int[] iArr, int i6, BigInteger bigInteger) {
        int i7 = i6 / 4;
        long jF = c.f(bigInteger) | 1;
        long jE = 1 | c.e(bigInteger);
        i iVar = new i();
        while (i7 > 1) {
            g(jF, -1396992403L, -1651782415L, 2032963901L, -1328225133L, 0L, iArr, iVar);
            g(jE, 1708849391L, 413217561L, 1824744093L, 1082356119L, 0L, iArr, iVar);
            i7 -= 2;
        }
        if (i7 == 1) {
            g(jF, -1396992403L, -1651782415L, 2032963901L, -1328225133L, 0L, iArr, iVar);
            f(jE, 1708849391L, 413217561L, 1824744093L, 1082356119L, 0L, iVar);
        }
        return c.g(iVar.b(), iVar.c());
    }

    public static BigInteger b(int[] iArr, int i6, BigInteger bigInteger) {
        int i7 = i6 / 4;
        long jF = c.f(bigInteger) | 1;
        long jE = 1 | c.e(bigInteger);
        h hVar = new h();
        while (i7 > 1) {
            e(jF, 817042533L, 957654963L, 2008139383L, -1584789045L, iArr, hVar);
            e(jE, 1488610021L, 1525158095L, 224458411L, -530701063L, iArr, hVar);
            i7 -= 2;
        }
        if (i7 == 1) {
            e(jF, 817042533L, 957654963L, 2008139383L, -1584789045L, iArr, hVar);
            d(jE, 1488610021L, 1525158095L, 224458411L, -530701063L, hVar);
        }
        return c.g(hVar.b(), hVar.d());
    }

    private static long c(long j6) {
        return ((j6 << 16) | (j6 >> 16)) & 4294967295L;
    }

    private static void d(long j6, long j7, long j8, long j9, long j10, h hVar) {
        hVar.c();
        long jD = hVar.d();
        long jB = hVar.b();
        int iA = hVar.a();
        long jC = ((j6 * jD) + (c(jD) * j7)) & 4294967295L;
        long jC2 = ((((c(jC) * j8) + (j9 * jC)) & 4294967295L) + (c(jC) * j10)) & 4294967295L;
        hVar.e(iA);
        hVar.f(4294967295L & (jB + jC2));
        hVar.g(jC);
        hVar.h(jC2);
    }

    private static void e(long j6, long j7, long j8, long j9, long j10, int[] iArr, h hVar) {
        hVar.c();
        long jD = hVar.d();
        long jB = hVar.b();
        int iA = hVar.a();
        long jH = (jD + c.h(iArr, iA << 2)) & 4294967295L;
        long jC = ((jH * j6) + (c(jH) * j7)) & 4294967295L;
        long jC2 = ((((c(jC) * j8) + (jC * j9)) & 4294967295L) + (c(jC) * j10)) & 4294967295L;
        hVar.e(iA + 1);
        hVar.f((jB + jC2) & 4294967295L);
        hVar.g(jC);
        hVar.h(jC2);
    }

    private static void f(long j6, long j7, long j8, long j9, long j10, long j11, i iVar) {
        long jC = iVar.c();
        long jB = iVar.b();
        iVar.d();
        int iA = iVar.a();
        long jC2 = c((jC * j6) & 4294967295L);
        long jC3 = (((c((c((c((jC2 * j7) & 4294967295L) * j8) & 4294967295L) * j9) & 4294967295L) * j10) & 4294967295L) + (jC2 * j11)) & 4294967295L;
        iVar.e(iA);
        iVar.f((jB + jC3) & 4294967295L);
        iVar.g(jC3);
        iVar.h(jC2);
    }

    private static void g(long j6, long j7, long j8, long j9, long j10, long j11, int[] iArr, i iVar) {
        long jC = iVar.c();
        long jB = iVar.b();
        iVar.d();
        int iA = iVar.a();
        long jC2 = c((((jC + c.h(iArr, iA << 2)) & 4294967295L) * j6) & 4294967295L);
        long jC3 = (((c((c((c((jC2 * j7) & 4294967295L) * j8) & 4294967295L) * j9) & 4294967295L) * j10) & 4294967295L) + (jC2 * j11)) & 4294967295L;
        iVar.e(iA + 1);
        iVar.f((jB + jC3) & 4294967295L);
        iVar.g(jC3);
        iVar.h(jC2);
    }
}
