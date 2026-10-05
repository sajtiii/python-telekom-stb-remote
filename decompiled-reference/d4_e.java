package d4;

import android.util.Log;
import java.math.BigInteger;
import java.util.Arrays;
import tmobile.hu.android.epgmiab.external.taviranyito.communication.authentication.helper.TaviranyitoArgumentOutOfRangeException;

/* JADX INFO: compiled from: TaviranyitoHelper.java */
/* JADX INFO: loaded from: classes.dex */
public class e {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    private BigInteger f5651a;

    /* JADX INFO: renamed from: b, reason: collision with root package name */
    private b f5652b;

    /* JADX INFO: renamed from: c, reason: collision with root package name */
    private int[] f5653c;

    /* JADX INFO: renamed from: d, reason: collision with root package name */
    private int[] f5654d;

    public e(int[] iArr, int[] iArr2, long j6, long j7, long j8, int[] iArr3) throws TaviranyitoArgumentOutOfRangeException {
        if (iArr3.length == 0 || iArr3.length % 8 != 0) {
            throw new TaviranyitoArgumentOutOfRangeException("data");
        }
        if (iArr.length < 8) {
            throw new TaviranyitoArgumentOutOfRangeException("inputKey");
        }
        if (iArr2 == null || iArr2.length < 256) {
            throw new TaviranyitoArgumentOutOfRangeException("sbox");
        }
        this.f5653c = iArr;
        this.f5654d = iArr2;
        b bVar = new b();
        this.f5652b = bVar;
        e(c.c(this.f5653c, this.f5654d, j6 | 1, j7 | 1, j8 | 1, iArr3, iArr3.length, bVar));
    }

    public static BigInteger a(int[] iArr, int[] iArr2, long j6, long j7, long j8, int[] iArr3, int i6) throws TaviranyitoArgumentOutOfRangeException {
        if (i6 <= 0 || i6 > iArr3.length || (i6 & 7) != 0) {
            throw new TaviranyitoArgumentOutOfRangeException("data");
        }
        if (iArr.length < 8) {
            throw new TaviranyitoArgumentOutOfRangeException("inputKey");
        }
        if (iArr2 == null || iArr2.length < 256) {
            throw new TaviranyitoArgumentOutOfRangeException("sbox");
        }
        return c.d(iArr, iArr2, j6 | 1, j7 | 1, j8 | 1, iArr3, i6);
    }

    public void b(int[] iArr, int i6) throws TaviranyitoArgumentOutOfRangeException {
        if (i6 <= 0 || i6 > iArr.length || (i6 & 7) != 0) {
            Log.e("Pairing", "TaviranyitoHelper.Decrypt if feltételbe beléptünk");
            throw new TaviranyitoArgumentOutOfRangeException("data");
        }
        Log.d("Pairing", "TaviranyitoHelper.Decrypt if elkerülve");
        Log.d("XmlParser", "TaviranyitoHelper.length: " + i6);
        Log.d("XmlParser", "TaviranyitoHelper.key: " + Arrays.toString(this.f5653c));
        Log.d("XmlParser", "TaviranyitoHelper.csKey: " + this.f5652b);
        Log.d("XmlParser", "TaviranyitoHelper.sBox: " + Arrays.toString(this.f5654d));
        Log.d("XmlParser", "TaviranyitoHelper.data: " + Arrays.toString(iArr));
        c.a(this.f5653c, this.f5652b, this.f5654d, iArr, i6);
    }

    public void c(int[] iArr, int i6) throws TaviranyitoArgumentOutOfRangeException {
        if (i6 <= 0 || i6 > iArr.length || (i6 & 7) != 0) {
            throw new TaviranyitoArgumentOutOfRangeException("data");
        }
        c.b(this.f5653c, this.f5652b, this.f5654d, iArr, i6);
    }

    public BigInteger d() {
        return this.f5651a;
    }

    public void e(BigInteger bigInteger) {
        this.f5651a = bigInteger;
    }
}
