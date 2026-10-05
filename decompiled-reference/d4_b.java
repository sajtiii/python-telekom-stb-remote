package d4;

import java.math.BigInteger;

/* JADX INFO: compiled from: TaviranyitoCS64Key.java */
/* JADX INFO: loaded from: classes.dex */
public class b {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    private long f5638a;

    /* JADX INFO: renamed from: b, reason: collision with root package name */
    private long f5639b;

    /* JADX INFO: renamed from: c, reason: collision with root package name */
    private long f5640c;

    /* JADX INFO: renamed from: d, reason: collision with root package name */
    private long f5641d;

    /* JADX INFO: renamed from: e, reason: collision with root package name */
    private long f5642e;

    /* JADX INFO: renamed from: f, reason: collision with root package name */
    private long f5643f;

    /* JADX INFO: renamed from: g, reason: collision with root package name */
    private long f5644g;

    /* JADX INFO: renamed from: h, reason: collision with root package name */
    private long f5645h;

    public b() {
    }

    private static void c(long j6, long j7, d dVar) {
        long j8 = j6;
        long j9 = 1;
        long j10 = 1;
        long j11 = 0;
        long j12 = 0;
        long j13 = j7;
        while (j13 != 0) {
            long j14 = (j8 / j13) & 4294967295L;
            long j15 = (j9 - (j14 * j11)) & 4294967295L;
            long j16 = j10;
            j10 = (j12 - (j14 * j10)) & 4294967295L;
            j12 = j16;
            j9 = j11;
            j11 = j15;
            long j17 = j13;
            j13 = (j8 % j13) & 4294967295L;
            j8 = j17;
        }
        dVar.c(j9);
        dVar.d(j12);
    }

    private static long d(long j6) {
        d dVar = new d();
        if (1 == j6) {
            return 1L;
        }
        c(j6, (4294967295L % j6) + 1, dVar);
        return (dVar.a() - (dVar.b() * (4294967295L / j6))) & 4294967295L;
    }

    public BigInteger a(int[] iArr, int i6) {
        long jH = ((this.f5638a * ((this.f5642e * c.h(iArr, 0)) & 4294967295L)) + this.f5639b) & 4294967295L;
        long jH2 = ((this.f5640c * (c.h(iArr, 4) + jH)) + this.f5641d) & 4294967295L;
        long j6 = (jH + jH2) & 4294967295L;
        int i7 = 1;
        int i8 = 2;
        while (i7 < i6 / 2) {
            int i9 = i8 + 1;
            long jH3 = ((this.f5638a * (jH2 + ((this.f5642e * c.h(iArr, i8 << 2)) & 4294967295L))) + this.f5639b) & 4294967295L;
            long j7 = (j6 + jH3) & 4294967295L;
            jH2 = ((this.f5640c * (jH3 + c.h(iArr, i9 << 2))) + this.f5641d) & 4294967295L;
            j6 = (j7 + jH2) & 4294967295L;
            i7++;
            i8 = i9 + 1;
        }
        BigInteger bigInteger = new BigInteger(Long.toString(jH2));
        return bigInteger.shiftLeft(32).add(new BigInteger(Long.toString(j6))).and(c.f5647b);
    }

    public BigInteger b(int[] iArr, int i6, BigInteger bigInteger) {
        long jE;
        int i7 = i6 / 4;
        long jF = c.f(bigInteger);
        long jE2 = c.e(bigInteger);
        long jF2 = 0;
        if (i7 > 2) {
            BigInteger bigIntegerA = a(iArr, i7 - 2);
            jF2 = c.f(bigIntegerA);
            jE = c.e(bigIntegerA);
        } else {
            jE = 0;
        }
        this.f5643f = d(this.f5638a);
        this.f5644g = d(this.f5640c);
        this.f5645h = d(this.f5642e);
        long jLongValue = new BigInteger("0").add(new BigInteger(Long.toString(jF))).subtract(new BigInteger(Long.toString(jF2))).subtract(new BigInteger(Long.toString(jE2))).and(new BigInteger("4294967295")).longValue();
        return c.g(new BigInteger(Long.toString(this.f5645h)).multiply(new BigInteger(Long.toString(jLongValue)).subtract(new BigInteger(Long.toString(this.f5639b))).multiply(new BigInteger(Long.toString(this.f5643f))).subtract(new BigInteger(Long.toString(jE)))).and(new BigInteger("4294967295")).longValue(), new BigInteger("0").add(new BigInteger(Long.toString(this.f5644g))).multiply(new BigInteger(Long.toString(jE2)).subtract(new BigInteger(Long.toString(this.f5641d))).and(new BigInteger("4294967295"))).subtract(new BigInteger(Long.toString(jLongValue))).and(new BigInteger("4294967295")).longValue());
    }

    public long e() {
        return this.f5638a;
    }

    public long f() {
        return this.f5639b;
    }

    public long g() {
        return this.f5640c;
    }

    public long h() {
        return this.f5641d;
    }

    public long i() {
        return this.f5642e;
    }

    public long j() {
        return this.f5643f;
    }

    public long k() {
        return this.f5644g;
    }

    public long l() {
        return this.f5645h;
    }

    public void m(long j6) {
        this.f5638a = j6;
    }

    public void n(long j6) {
        this.f5639b = j6;
    }

    public void o(long j6) {
        this.f5640c = j6;
    }

    public void p(long j6) {
        this.f5641d = j6;
    }

    public void q(long j6) {
        this.f5642e = j6;
    }

    public void r(long j6) {
        this.f5643f = j6;
    }

    public void s(long j6) {
        this.f5644g = j6;
    }

    public void t(long j6) {
        this.f5645h = j6;
    }

    public b(BigInteger bigInteger, long j6, long j7, long j8) {
        long jE = c.e(bigInteger);
        long jF = c.f(bigInteger);
        this.f5638a = (jF | 1) & 4294967295L;
        this.f5639b = (jE | 1) & 4294967295L;
        this.f5640c = ((j6 ^ jF) | 1) & 4294967295L;
        this.f5641d = ((jE ^ j7) | 1) & 4294967295L;
        this.f5642e = ((j8 ^ jF) | 1) & 4294967295L;
    }
}
