package c4;

import android.util.Log;
import d4.c;
import d4.e;
import java.util.Arrays;

/* JADX INFO: compiled from: TaviranyitoTransactionCodec.java */
/* JADX INFO: loaded from: classes.dex */
public class b {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    e f3935a;

    public b(int[] iArr, int[] iArr2) throws Exception {
        this.f3935a = new e(iArr2, a.f3934a, 1206402005L, 2418584567L, 3864493069L, iArr);
        Log.d("Pairing", "TaviranyitoTransactionCodec inicializ�l�s v�ge");
    }

    public int[] a(int[] iArr, int i6, int i7) {
        Log.e("", "End-start =" + i7 + "-" + i6 + "");
        int i8 = i7 - i6;
        if (i8 <= 0 || i6 < 0 || i6 > iArr.length || iArr.length == 0) {
            return null;
        }
        int[] iArr2 = new int[i8];
        for (int i9 = 0; i9 < i8; i9++) {
            iArr2[i9] = iArr[i6 + i9];
        }
        return iArr2;
    }

    public String b(int[] iArr) throws Exception {
        Log.d("Pairing", "IntData: " + Arrays.toString(iArr));
        if ((iArr.length & 7) != 0 || iArr.length < 12) {
            return null;
        }
        Log.d("Pairing", "TaviranyitoHelper.Decrypt kezdete");
        this.f3935a.b(iArr, iArr.length);
        Log.d("Pairing", "Origlength sz�mol�s start");
        long jH = c.h(iArr, 0);
        if (jH > iArr.length - 12) {
            Log.e("Pairing", "Invalid Decode Length");
            jH = iArr.length - 12;
        }
        if (c.i(iArr, iArr.length - 8) != this.f3935a.d()) {
            Log.e("Pairing", "Invalid Hash");
        }
        Log.d("Pairing", "Long to Int");
        int i6 = ((int) jH) + 4;
        Log.d("Pairing", "Copy Of Range start");
        a(iArr, 4, i6);
        Log.d("Pairing", "Result Starting");
        String str = new String(k4.a.c(a(iArr, 4, i6)), "UTF-8");
        Log.d("Pairing", "Decode result: " + str);
        return str;
    }

    public int[] c(String str) throws Exception {
        if (str == null) {
            return null;
        }
        int length = str.getBytes("UTF8").length;
        int i6 = (length + 12 + 7) & (-8);
        int[] iArr = new int[i6];
        long j6 = length;
        c.j(j6, iArr, 0);
        c.k(this.f3935a.d(), iArr, i6 - 8);
        byte[] bytes = str.getBytes("UTF8");
        for (int i7 = 0; i7 < bytes.length; i7++) {
            iArr[i7 + 4] = bytes[i7];
        }
        this.f3935a.c(iArr, i6);
        return iArr;
    }
}
