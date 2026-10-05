package c4;

import android.util.Log;
import d4.c;
import d4.e;
import java.math.BigInteger;

/* JADX INFO: compiled from: TaviranyitoCompanionShared.java */
/* JADX INFO: loaded from: classes.dex */
public class a {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    public static final int[] f3934a = {48, 179, 102, 100, 0, 1, 0, 0, 18, 112, 89, 255, 158, 237, 151, 7, 201, 249, 254, 152, 232, 21, 90, 96, 183, 210, 187, 12, 165, 236, 200, 135, 8, 226, 155, 239, 93, 110, 121, 35, 135, 95, 239, 165, 170, 47, 156, 99, 135, 43, 119, 196, 126, 199, 226, 134, 160, 190, 53, 136, 23, 49, 195, 211, 186, 140, 88, 146, 104, 218, 249, 178, 149, 135, 211, 11, 107, 131, 155, 175, 143, 125, 17, 111, 201, 149, 13, 177, 91, 125, 187, 104, 239, 94, 243, 124, 33, 46, 36, 214, 0, 130, 55, 72, 45, 55, 4, 183, 39, 250, 120, 97, 225, 13, 214, 113, 216, 229, 12, 3, 52, 251, 164, 33, 113, 117, 57, 67, 85, 249, 41, 10, 4, 173, 70, 31, 20, 159, 110, 84, 199, 141, 16, 224, 176, 250, 136, 0, 72, 35, 85, 210, 117, 15, 121, 36, 129, 131, 86, 76, 46, 243, 53, 161, 133, 204, 3, 164, 118, 42, 235, 222, 70, 250, 25, 153, 81, 162, 180, 158, 162, 32, 41, 158, 173, 210, 106, 32, 40, 71, 109, 112, 4, 104, 187, 200, 136, 41, 81, 210, 82, 139, 197, 64, 115, 222, 216, 87, 191, 174, 174, 150, 238, 10, 40, 119, 13, 118, 244, 82, 250, 152, 68, 112, 250, 17, 50, 198, 77, 254, 252, 59, 69, 120, 89, 28, 109, 58, 136, 82, 26, 66, 129, 13, 232, 103, 175, 5, 20, 192, 7, 194, 233, 128, 173, 33};

    public static String a(int[] iArr, int[] iArr2, byte[] bArr, int i6, int i7) throws Exception {
        Log.d("Pairing", "HASH_Compid");
        for (int i8 = 0; i8 < iArr.length; i8++) {
            Log.d("Pairing", "HASH_Compid[" + i8 + "]" + iArr[i8]);
        }
        Log.d("Pairing", "HASH_Compkey");
        for (int i9 = 0; i9 < iArr2.length; i9++) {
            Log.d("Pairing", "HASH_CompKey[" + i9 + "]" + iArr2[i9]);
        }
        Log.d("Pairing", "HASH_HostAddr");
        for (int i10 = 0; i10 < bArr.length; i10++) {
            Log.d("Pairing", "HASH_HostAddr[" + i10 + "]" + ((int) bArr[i10]));
        }
        Log.d("Pairing", "HASH_Seq=" + i6);
        Log.d("Pairing", "HASH_lenght" + i7);
        int[] iArr3 = new int[16];
        long j6 = (long) i6;
        c.j(j6, iArr3, 0);
        long j7 = i7;
        c.j(j7, iArr3, 4);
        for (int i11 = 0; i11 < 4; i11++) {
            iArr3[i11 + 8] = (bArr[i11] + 256) & 255;
        }
        System.arraycopy(iArr, 0, iArr3, 12, 4);
        Log.d("Pairing", "HASH_INTArray");
        for (int i12 = 0; i12 < 16; i12++) {
            Log.d("Pairing", "HASH_INTarray[" + i12 + "]" + iArr3[i12]);
        }
        BigInteger bigIntegerA = e.a(iArr2, f3934a, 1206402005L, 2418584567L, 3864493069L, iArr3, 16);
        Log.d("Pairing", "HASH_hashCode" + bigIntegerA);
        String str = e4.a.b(j6, 8) + e4.a.b(j7, 8) + e4.a.a(bigIntegerA, 16);
        Log.d("Pairing", "HASH_hash_end" + str.toUpperCase());
        return str.toUpperCase();
    }
}
