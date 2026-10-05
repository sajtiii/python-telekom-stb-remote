package b4;

import android.content.Intent;
import android.util.Log;
import com.google.firebase.analytics.FirebaseAnalytics;
import java.io.ByteArrayInputStream;
import org.apache.commons.lang3.StringUtils;
import tmobile.hu.android.epgmiab.application.CustomApplication;
import tmobile.hu.android.epgmiab.application.e;

/* JADX INFO: compiled from: TaviranyitoEvents.java */
/* JADX INFO: loaded from: classes.dex */
public enum b {
    VOLUME_UP("volumeup", "HangFel"),
    VOLUME_DOWN("volumedown", "HangLe"),
    CHANNEL_UP("channelup", "ProgramFel"),
    CHANNEL_DOWN("channeldown", "ProgramLe"),
    UP("up", "NavigacioFel"),
    DOWN("down", "NavigacioLe"),
    LEFT("left", "NavigacioBal"),
    RIGHT("right", "NavigacioJobb"),
    OK("select", "NavigacioOk"),
    MENU("menu", "ShortcutMenu"),
    RED("red", "SzamPiros"),
    GREEN("green", "SzamZold"),
    YELLOW("yellow", "SzamSarga"),
    BLUE("blue", "SzamKek"),
    NUMBER_0("0", "Szam0"),
    NUMBER_1("1", "Szam1"),
    NUMBER_2("2", "Szam2"),
    NUMBER_3("3", "Szam3"),
    NUMBER_4("4", "Szam4"),
    NUMBER_5("5", "Szam5"),
    NUMBER_6("6", "Szam6"),
    NUMBER_7("7", "Szam7"),
    NUMBER_8("8", "Szam8"),
    NUMBER_9("9", "Szam9"),
    NUMBER_BACK("back", "NavigacioVissza"),
    NUMBER_ENTER("enter", "SzamEnter"),
    GUIDE("guide", "ShortcutMusorok"),
    VIDEO("vod", "ShortcutVideoteka"),
    OPTIONS("options", "ShortcutSettings"),
    TELETEXT("teletext", "Teletext"),
    MUTE("mute", "HangNemitas"),
    INFO("info", "NavigacioInfo"),
    FAST_FORWARD("ffwd", "LejatszasEloreteker"),
    SKIP_FORWARD("skipfwd", "LejatszasEloreteker"),
    EXIT("exit", "NavigacioKilepes"),
    RECENT("recent", "ShortcutKorabbi"),
    RECORDEDTV("recordedtv", "ShortcutFelvetelek"),
    STOP("stop", "LejatszasMegallit"),
    PLAY_PAUSE("playpause", "LejatszasPlaypause"),
    RECORD("record", "LejatszasFelvesz"),
    SKIP_BACK("skipback", "LejatszasVisszateker"),
    REWIND("rwd", "LejatszasVisszateker"),
    POWER("power", "NavigacioPower"),
    CLEAR("clear", "Clear"),
    APP_1("app1", "App1"),
    APP_2("app2", "App2"),
    APP_3("app3", "App3"),
    APP_4("app4", "App4"),
    APP_5("app5", "App5"),
    APP_6("app6", "App6"),
    FAVORITES("favorites", "Kedvencek"),
    HELP("help", "Segitseg"),
    SEARCH(FirebaseAnalytics.Event.SEARCH, "Kereses");


    /* JADX INFO: renamed from: d, reason: collision with root package name */
    private String f3465d;

    /* JADX INFO: renamed from: e, reason: collision with root package name */
    private String f3466e;

    /* JADX INFO: compiled from: TaviranyitoEvents.java */
    class a implements c {

        /* JADX INFO: renamed from: a, reason: collision with root package name */
        final /* synthetic */ g4.a f3467a;

        /* JADX INFO: renamed from: b, reason: collision with root package name */
        final /* synthetic */ String f3468b;

        /* JADX INFO: renamed from: c, reason: collision with root package name */
        final /* synthetic */ tmobile.hu.android.epgmiab.external.taviranyito.model.b f3469c;

        a(g4.a aVar, String str, tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar) {
            this.f3467a = aVar;
            this.f3468b = str;
            this.f3469c = bVar;
        }

        @Override // b4.c
        public void a(String str, tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar) {
            if (str.equalsIgnoreCase("error")) {
                this.f3467a.e();
                this.f3467a.c(bVar);
                this.f3467a.a();
                b.g(false, this.f3468b, bVar);
                return;
            }
            try {
                j4.a aVarA = new f4.a().a(new ByteArrayInputStream(str.getBytes("UTF-8")));
                Log.d("Pairing", "Pairing Info parse-olva: " + aVarA.toString());
                bVar.u(aVarA.a());
                bVar.v(aVarA.b());
                bVar.A(aVarA.d());
                bVar.y("Device");
                if (StringUtils.isNotEmpty(aVarA.c())) {
                    bVar.w(aVarA.c());
                    bVar.y(aVarA.c());
                }
                if (StringUtils.isNotEmpty(aVarA.e())) {
                    this.f3467a.e();
                    for (tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar2 : this.f3467a.d()) {
                        if (StringUtils.equals(bVar2.h(), aVarA.e())) {
                            if (bVar2.c() != null) {
                                bVar.w(bVar2.c());
                            }
                            this.f3467a.c(bVar2);
                        }
                    }
                    this.f3467a.a();
                    bVar.B(aVarA.e());
                }
                bVar.s(true);
                bVar.t(true);
                if (StringUtils.isEmpty(this.f3468b)) {
                    e.a().M1().e(this.f3469c, this.f3467a);
                }
                e.a().v().c(bVar);
                tmobile.hu.android.epgmiab.external.taviranyito.model.a.a();
                b.g(true, this.f3468b, bVar);
            } catch (Exception e6) {
                this.f3467a.e();
                this.f3467a.c(bVar);
                this.f3467a.a();
                Log.e(getClass().getSimpleName(), "Exception occurred.", e6);
                b.g(false, this.f3468b, bVar);
            }
        }
    }

    b(String str, String str2) {
        this.f3465d = str;
        this.f3466e = str2;
    }

    public static b b(String str) {
        for (b bVar : values()) {
            if (bVar.f3465d.equals(str)) {
                return bVar;
            }
        }
        throw new IllegalArgumentException("The provided command type [" + str + "] is not valid!");
    }

    public static void e(tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar, String str, String str2) {
        Log.d("IPTVRemote", "Pairing Button Pressed|" + bVar.d() + "|" + str + "|");
        bVar.o(str, bVar.e(), "", new a(new g4.a(CustomApplication.b()), str2, bVar));
    }

    public static void f(tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar, String str) {
        if (bVar == null) {
            Log.d("IPTVRemote", "No device selected for command [" + str + "]");
            return;
        }
        Log.d("IPTVRemote", "" + str + " Button Pressed|" + bVar.d() + "");
        bVar.p(str);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public static void g(boolean z5, String str, tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar) {
        Log.d("Broadcast", "Pairing broadcast sent");
        Intent intent = new Intent("PAIRING_BROADCAST");
        intent.putExtra("PAIRING_BROADCAST_RESULT", z5);
        if (!StringUtils.isEmpty(str)) {
            intent.putExtra("PAIRING_BROADCAST_PIN", str);
        }
        intent.putExtra("PAIRING_BROADCAST_DEVICE", bVar);
        c0.a.b(CustomApplication.b()).d(intent);
    }

    public static void h(tmobile.hu.android.epgmiab.external.taviranyito.model.b bVar, String str) {
        if (bVar == null) {
            Log.d("IPTVRemote", "No device selected");
            return;
        }
        Log.d("IPTVRemote", "" + str + "  tune to TaviranyitoChannelXML|" + bVar.d() + "");
        bVar.q(str);
    }

    public String c() {
        return this.f3465d;
    }

    public String d() {
        return this.f3466e;
    }
}
