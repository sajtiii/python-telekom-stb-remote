package b4;

/* JADX INFO: compiled from: TaviranyitoCommand.java */
/* JADX INFO: loaded from: classes.dex */
public class a {

    /* JADX INFO: renamed from: a, reason: collision with root package name */
    private String f3435a;

    /* JADX INFO: renamed from: b, reason: collision with root package name */
    private String f3436b;

    public a(String str, String[] strArr) {
        String strConcat = "op=" + str;
        for (int i6 = 0; i6 < strArr.length; i6 += 2) {
            strConcat = strConcat.concat('&' + strArr[i6] + '=' + strArr[i6 + 1]);
        }
        this.f3435a = strConcat;
        this.f3436b = str;
    }

    public String a() {
        return this.f3436b;
    }

    public String b() {
        return this.f3435a;
    }

    public a(String str) {
        this.f3435a = "op=" + str;
        this.f3436b = str;
    }
}
