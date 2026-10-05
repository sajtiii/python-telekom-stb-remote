package d4;

import java.math.BigInteger;

/* JADX INFO: compiled from: TaviranyitoBV4Key.java */
/* JADX INFO: loaded from: classes.dex */
public class a {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    private int[] f5633a;

    /* JADX INFO: renamed from: d, reason: collision with root package name */
    private long f5636d;

    /* JADX INFO: renamed from: e, reason: collision with root package name */
    private long[] f5637e = new long[32];

    /* JADX INFO: renamed from: b, reason: collision with root package name */
    private int f5634b = 0;

    /* JADX INFO: renamed from: c, reason: collision with root package name */
    private int f5635c = 0;

    public a(int[] iArr) {
        int[] iArr2 = new int[256];
        this.f5633a = iArr2;
        for (int i6 = 0; i6 < 256; i6++) {
            iArr2[i6] = i6 & 255;
        }
        int i7 = 0;
        int i8 = 0;
        for (int i9 = 0; i9 < 256; i9++) {
            i7 = (i7 + iArr2[i9] + iArr[i8]) & 255;
            int i10 = iArr2[i9];
            iArr2[i9] = iArr2[i7];
            iArr2[i7] = i10;
            i8++;
            if (i8 == iArr.length) {
                i8 = 0;
            }
        }
        for (int i11 = 0; i11 < 256; i11++) {
            iArr2[i11] = iArr2[i11] & 255;
        }
        b();
    }

    private void b() {
        int[] iArr = this.f5633a;
        int[] iArr2 = new int[132];
        int i6 = 0;
        int i7 = 0;
        int i8 = 0;
        for (int i9 = 0; i9 < 132; i9++) {
            i7 = (i7 + 1) & 255;
            int i10 = iArr[i7] & 255;
            i8 = (i8 + i10) & 255;
            iArr[i7] = iArr[i8];
            iArr[i8] = i10 & 255;
            iArr2[i9] = iArr[(iArr[i7] + i10) & 255];
        }
        this.f5634b = i7 & 255;
        this.f5635c = i8 & 255;
        this.f5636d = c.h(iArr2, 0);
        while (true) {
            long[] jArr = this.f5637e;
            if (i6 >= jArr.length) {
                return;
            }
            int i11 = i6 + 1;
            jArr[i6] = c.h(iArr2, i11 * 4);
            i6 = i11;
        }
    }

    public void a(int i6, int[] iArr) {
        int i7 = this.f5634b;
        int i8 = this.f5635c;
        int[] iArr2 = this.f5633a;
        long[] jArr = this.f5637e;
        long j6 = this.f5636d;
        int i9 = i6 >> 2;
        int i10 = 0;
        while (true) {
            int i11 = i9 - 1;
            if (i9 <= 0) {
                this.f5634b = i7 & 255;
                this.f5635c = i8 & 255;
                this.f5636d = j6;
                return;
            }
            i7 = (i7 + 1) & 255;
            int i12 = iArr2[i7] & 255;
            i8 = (i8 + i12) & 255;
            iArr2[i7] = iArr2[i8];
            iArr2[i8] = i12 & 255;
            int i13 = (iArr2[i7] + iArr2[i8]) & 255;
            int i14 = i10 << 2;
            i10++;
            c.j(new BigInteger(Long.toString(c.h(iArr, i14))).xor(new BigInteger(Long.toString(j6)).multiply(new BigInteger(Integer.toString(iArr2[i13 & 255])))).and(c.f5646a).longValue(), iArr, i14);
            int i15 = i13 & 31;
            j6 = (j6 + jArr[i15]) & 4294967295L;
            iArr2[i13] = (int) (((long) iArr2[i13]) + jArr[i15]);
            iArr2[i13] = iArr2[i13] & 255;
            i9 = i11;
        }
    }
}
