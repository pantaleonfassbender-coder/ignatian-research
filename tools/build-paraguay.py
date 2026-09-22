# -*- coding: utf-8 -*-
"""Build data/paraguay.json — The Reductions of Paraguay.

Two witnesses, one module. (1) L. A. Muratori, *A Relation of the Missions of
Paraguay* (London: J. Marmaduke, 1759; English translation of *Il cristianesimo
felice*, via the French) — Internet Archive
`bim_eighteenth-century_a-relation-of-the-missio_muratori-lodovico-anton_1759`,
public domain. Five chapters carried complete: V (the obstacles, and the
Mamelucos), IX (the music of the Indians), XV (the civil government), XVIII
(the military government), XX (the persecutions raised through envy). The OCR
keeps the long ſ as its own character, so ſ→s is deterministic; running heads
carry the 1759 pagination, which is captured for the page labels; catchwords
and page furniture are dropped; residual OCR damage is repaired in WORD_FIXES
and PARA_FIXES below, disclosed rather than silent. Chapter numbers whose
heads the OCR destroyed (XV) are restored from the book's own table of
contents and the chapter sequence; IX is confirmed by the table of contents
("CAP. IX. The Music of the Indians ... 87").

(2) A. Ruiz de Montoya, *Conquista espiritual* (Madrid 1639), quoted from the
Bilbao reprint of 1892 (IA `conquistaespiri00montgoog`), public domain: four
passages transcribed from the OCR and emended against the sense — the fleet of
rafts at the falls of the Paraná and the 300 canoes (1631, pp. 157–159), and
the deaths of Roque González and Alonso Rodríguez at Caaró (1628,
pp. 229–231). The English is this site's unofficial working translation,
dedicated CC0. Montoya's first person is the protagonist's.

Source text expected in the session scratchpad (auto-downloaded if absent).
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "paraguay.json")
CACHE = os.environ.get("PARAGUAY_CACHE",
    r"C:\Users\leofa\AppData\Local\Temp\claude\C--Users-leofa\db4f6386-b8a6-43a5-91f2-27e076520d66\scratchpad\paraguay\muratori1759.txt")
URL = ("https://archive.org/download/"
       "bim_eighteenth-century_a-relation-of-the-missio_muratori-lodovico-anton_1759/"
       "bim_eighteenth-century_a-relation-of-the-missio_muratori-lodovico-anton_1759_djvu.txt")

def load_source():
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        urllib.request.urlretrieve(URL, CACHE)
    t = open(CACHE, encoding="utf-8").read()
    return t.replace("\u017f", "s").replace("ﬅ", "st").replace("ﬂ", "fl").replace("ﬁ", "fi")

# ------------------------------------------------------- Muratori sections
# (start, end) are offsets into the ſ→s–normalised text; startPage anchors the
# page counter until the first running head inside the slice takes over.
SECTIONS = [
    dict(id="mur5",  zk="Mur. V",  page0=40,
         titel="The principal obstacles to the Indians' conversion",
         blurb="Why the missions nearly failed before they began: the example of the Europeans, "
               "the encomienda, and the slaving raids of the Mamelucos of São Paulo — the enemy "
               "the Reductions were built against.",
         start=76149, end=103150, open_fix=(r"^1 subject", "IT is easy to imagine how difficult it was to subject"),
         end_key="millions of Indians slaves"),
    dict(id="mur9",  zk="Mur. IX", page0=87,
         titel="The music of the Indians",
         blurb="The most famous pages of the book: missionaries who fished for souls with song, "
               "the chapels in every Reduction, orchestras of Indian-built organs, lutes and "
               "trumpets — and Father Cattaneo writing home to Milan for masses and vespers "
               "in music.",
         start=146815, end=152750, open_fix=(r"^Ntroducing", "Introducing"),
         end_key="canonical hours"),
    dict(id="mur15", zk="Mur. XV", page0=125,
         titel="The civil government of the christian settlements",
         blurb="The utopia's mechanics, soberly described: Indian magistrates under royal "
               "sovereignty, common fields and storehouses, no money within the towns — the "
               "chapter Europe's philosophes would quote for a century.",
         start=202047, end=217700, open_fix=(r"^H E", "THE"),
         end_key="cogent reasons for the contrary"),
    dict(id="mur18", zk="Mur. XVIII", page0=155,
         titel="The military government of the Reductions",
         blurb="The armed utopia: why the crown licensed Guaraní firearms, the militia that "
               "saved Buenos Aires, the drills after mass — the arrangement whose revocation "
               "in 1750 doomed the whole experiment.",
         start=245117, end=264855, open_fix=(r"^H O'?", "THO'"),
         end_key="chosen to be subject"),
    dict(id="mur20", zk="Mur. XX", page0=180,
         titel="The persecutions raised through envy",
         blurb="Muratori's defence of the missionaries against the standing accusations — "
               "hidden mines, kingdom-building, trade — written a decade before the Treaty of "
               "Madrid turned the accusations into policy.",
         start=282930, end=320160, open_fix=(r"^HE credit", "THE credit"),
         end_key="lawful sovereigns"),
]

HEAD_TITLE_WORDS = ("obstacle", "conversion", "music of the indians", "civil govern",
                    "settlement", "military govern", "reduction", "persecution", "envy",
                    "missionaries in paraguay", "way of life", "establishment")

def is_running_head(line):
    l = line.strip()
    m = re.match(r"^(\d{1,3})\s+(.{3,70})$", l) or re.match(r"^(.{3,70}?)\s+(\d{1,3})\s*[,.]?$", l)
    if not m:
        return None
    g = m.groups()
    page = int(g[0]) if g[0].isdigit() else int(g[1])
    title = (g[1] if g[0].isdigit() else g[0]).lower()
    if not (0 < page < 320):
        return None
    if any(w in title for w in HEAD_TITLE_WORDS):
        return page
    # generic head shape: few words, mostly title-ish, no sentence punctuation depth
    words = re.findall(r"[A-Za-z']+", title)
    if 1 <= len(words) <= 8 and sum(len(w) for w in words) / max(1, len(title)) > 0.6 \
       and not title.rstrip().endswith(("-", ";")):
        return page
    return None

def alpha_ratio(s):
    if not s:
        return 0
    return sum(c.isalpha() or c.isspace() for c in s) / len(s)

def clean_section(text, page0):
    lines = text.split("\n")
    paras, buf = [], []
    page = page0
    pending_page = None

    def flush():
        nonlocal buf, page, pending_page
        if buf:
            p = " ".join(buf)
            p = re.sub(r"(\w)[-¬]\s+(\w)", r"\1\2", p)
            p = re.sub(r"\s+", " ", p).strip()
            if len(p) > 2:
                paras.append({"page": page, "text": p})
            buf = []
        if pending_page:
            page = pending_page
            pending_page = None

    for ln in lines:
        l = ln.strip()
        if not l:
            flush()
            continue
        hp = is_running_head(l)
        if hp:
            # a head both ends the current page's text and announces the new page;
            # accept only plausible, near-monotonic pages (OCR fakes get dropped,
            # but the line is still page furniture and never body text)
            if page - 1 <= hp <= page + 4:
                pending_page = hp
            flush()
            continue
        if alpha_ratio(l) < 0.55 or not re.search(r"[A-Za-z]{2}", l):
            continue
        buf.append(l)
    flush()

    # catchwords: a very short paragraph whose text opens the next paragraph
    out = []
    for i, p in enumerate(paras):
        t = p["text"]
        if len(t) <= 24 and i + 1 < len(paras):
            probe = re.sub(r"[^a-z]", "", t.lower())
            nxt = re.sub(r"[^a-z]", "", paras[i + 1]["text"][:60].lower())
            if probe and probe in nxt:
                continue
        if len(t) < 40 and not re.search(r"[.!?]$", t) and i + 1 < len(paras):
            # stray fragment line (page furniture survivors) — but never a line
            # that the page turn split from its continuation (next starts lowercase)
            if not re.match(r"^[a-z]", paras[i + 1]["text"]):
                if alpha_ratio(t) < 0.8 or len(re.findall(r"[A-Za-z]{3,}", t)) < 3:
                    continue
        out.append(p)

    # merge paragraphs broken by page turns (next starts lowercase)
    merged = []
    for p in out:
        if merged and re.match(r"^[a-z]", p["text"]) and not merged[-1]["text"].endswith((".", "!", "?", ":", "\u201d", "'")):
            merged[-1]["text"] += " " + p["text"]
        else:
            merged.append(dict(p))
    return merged

# OCR repairs, applied to the assembled Muratori text. The print's own
# spellings (cloath, compleat, chuse, &c.) are kept; only scan damage is fixed.
WORD_FIXES = [
    (r"\boblerved\b", "observed"), (r"\blavage\b", "savage"), (r"\bmafic\b", "music"),
    (r"\bRedu[ZC]ions\b", "Reductions"), (r"\bReduclions\b", "Reductions"),
    (r"\bReduttions\b", "Reductions"), (r"\bReduQions\b", "Reductions"),
    (r"\bFesuits\b", "Jesuits"), (r"\bJeluits\b", "Jesuits"),
    (r"\bMif[fl]ionar", "Missionar"), (r"\bMissonar", "Missionar"),
    (r"\binstuments\b", "instruments"), (r"\bvi[ou]lincello\b", "violoncello"),
    (r"\bJudian\b", "Indian"), (r"\bJudians\b", "Indians"),
    (r"\bIndian s\b", "Indians"), (r"\bchriflian", "christian"),
    (r"\bTow\b(?= careful)", "How"), (r"\bMamelusses\b", "Mamelucos"),
    (r"\bMameluffes\b", "Mamelucos"), (r"\bconverfion\b", "conversion"),
    (r"\bfpirit", "spirit"), (r"\bmufic", "music"), (r"\bMufic", "Music"),
    (r"\bfoul", "soul"), (r"\bfome\b", "some"), (r"\bfuch\b", "such"),
    (r"\bthele\b", "these"), (r"\bthofe\b", "those"), (r"\bwhofe\b", "whose"),
    (r"\bcaufe", "cause"), (r"\bhoufe", "house"), (r"\bpleafure\b", "pleasure"),
    (r"\bagainft\b", "against"), (r"\bmoft\b", "most"), (r"\bfirft\b", "first"),
    (r"\balmoft\b", "almost"), (r"\bmuft\b", "must"), (r"\bbeft\b", "best"),
    (r"\bintereft", "interest"), (r"\bprieft", "priest"), (r"\bPrieft", "Priest"),
    (r"\bJefus\b", "Jesus"), (r"\bJefuit", "Jesuit"), (r"\bfettle", "settle"),
    (r"\bfleep\b", "sleep"), (r"\bfay\b", "say"), (r"\bfee\b", "see"),
    (r"\bfhall\b", "shall"), (r"\bfhould\b", "should"), (r"\bwifh\b", "wish"),
    (r"\bparifh", "parish"), (r"\bSpanifh\b", "Spanish"), (r"\bSpani(sh|ſh) Nation\b", "Spanish Nation"),
    (r"\bfubject", "subject"), (r"\bfociety\b", "society"), (r"\bSociety of Jefus\b", "Society of Jesus"),
    (r"'s\b(?=\s+Missionar)", "s"),
    # second pass, from the full read-through of the assembled text
    (r"\besnversion\b", "conversion"), (r"\bTadians\b", "Indians"),
    (r"\bIudiaus\b", "Indians"), (r"\bIdiaus\b", "Indians"), (r"\bIndiaus\b", "Indians"),
    (r"\bJadians\b", "Indians"), (r"\bTndians\b", "Indians"), (r"\bndians\b", "Indians"),
    (r"\bnecefl", "necess"), (r"\bSpamards\b", "Spaniards"), (r"\bSpanisb\b", "Spanish"),
    (r"\bSpanisp\b", "Spanish"), (r"\bSpaxish\b", "Spanish"), (r"\bSpanih\b", "Spanish"),
    (r"\bSpanizrds\b", "Spaniards"), (r"\bSpanis\b(?= troops)", "Spanish"),
    (r"\bSpaniso\b", "Spanish"), (r"\bSpaniars\b", "Spaniards"), (r"\bSaniards\b", "Spaniards"),
    (r"\bperniqous\b", "pernicious"), (r"\binferoir\b", "inferior"),
    (r"\bteyeral\b", "several"), (r"\beasiy\b", "easy"), (r"\bexpole\b", "expose"),
    (r"\bialvation\b", "salvation"), (r"\bflaves\b", "slaves"),
    (r"\bthac\b", "that"), (r"\btorts\b(?=, and churches)", "forts"),
    (r"\bRassiaus\b", "Russians"), (r"\bconguered\b", "conquered"), (r"\bfays\b", "says"),
    (r"\bthay\b", "they"), (r"\bfignalized\b", "signalized"), (r"\bCammandery\b", "Commandery"),
    (r"\bPzafters\b", "Piasters"), (r"\bPtasters\b", "Piasters"), (r"\bPirfer\b", "Piaster"),
    (r"\beig ht\b", "eight"), (r"\bwile\b(?= (ordinances|a regulation))", "wise"),
    (r"\bfo wile\b", "so wise"), (r"\bimposible\b", "impossible"), (r"\bprincipal!\b", "principal"),
    (r"\bane equity\b", "and equity"), (r"\bintenti - Ons\b", "intentions"),
    (r"\[rdians\b", "Indians"), (r"\[dans\b", "Indians"),
    (r"\bChiuquisaca\b", "Chuquisaca"), (r"\bBelegna\b", "Bologna"), (r"\bchattles\b", "chattels"),
    (r"\bFoseph\b", "Joseph"), (r"\bSanta Crux\b", "Santa Cruz"),
    (r"\bhve 1n\b", "live in"), (r"\bfo\b(?= (vast|justly|often|wile|many))", "so"),
    (r"\bEyven\b", "Even"), (r"\btegular\b", "regular"), (r"\binsatlable\b", "insatiable"),
    (r"\bicarce\b", "scarce"), (r"\baquainted\b", "acquainted"),
    (r"\btliey\b", "they"), (r"\bgunwder,?;?\b", "gunpowder."), (r"\bChriftianity\b", "Christianity"),
    (r"\bfix\b(?= (months|hundred|or))", "six"),
    (r"\bMitGonaries\b", "Missionaries"), (r"\bmasles\b", "masses"),
    (r"\b7taly\b", "Italy"), (r"\bSigner\b(?= Alberti)", "Signor"),
    (r"\bvifitation", "visitation"), (r"Redu[#Z/f]?[tf]?ions\b", "Reductions"),
    (r"\bReduftion\b", "Reduction"), (r"\bRedufion\b", "Reduction"), (r"\bRedutticn\b", "Reduction"),
    (r"\bReduktion\b", "Reduction"), (r"\bReductious\b", "Reductions"), (r"\bNeductious\b", "Reductions"),
    (r"\bRedudlions\b", "Reductions"), (r"\bReauctions\b", "Reductions"),
    (r"\bwon derful\b", "wonderful"), (r"\bpawer\b", "power"), (r"\ban the fiercest\b", "on the fiercest"),
    (r"\bteign\b", "reign"), (r"\bMi[fsl]{1,2}ionar", "Missionar"), (r"\bMil[fs]ionar", "Missionar"),
    (r"\bthape\b", "shape"), (r"\bvr well cured\b", "if well cured"),
    (r"\brasing\b", "raising"), (r"\bbrutilh\b", "brutish"), (r"\bipace\b", "space"),
    (r"\bcoarle\b", "coarse"), (r"\blowed Mayz\b", "sowed Mayz"),
    (r"\btelebrated\b", "celebrated"), (r"\bZurope\b", "Europe"),
    (r"\bbar\. barous\b", "barbarous"), (r"\bdefire\b", "desire"),
    (r"\bsaaded\b", "persuaded"), (r"\bCaltaneo", "Cattaneo"), (r"\bCa/taneo\b", "Cattaneo"),
    (r"\bainter\b", "painter"), (r"\bgoth\. of December\b", "30th of December"),
    (r"\bcuriolity\b", "curiosity"), (r"\bthole\b", "those"),
    (r"\bafresh date\b", "a fresh date"), (r"\bapprehendgd\b", "apprehended"),
    (r"\bChiaco\b", "Chaco"), (r"\bMELLo\b", "Mello"), (r"\bCacrque Cor uba\b", "Cacique Coruba"),
    (r"\bMamelu/- ?fes\b", "Mamelucos"), (r"\bMamelisses\b", "Mamelucos"),
    (r"\bMamelusf\s*Ni,", "Mamelucos,"), (r"\bMaelta\b", "Mazetta"),
    (r"\bdangersof\b", "dangers of"), (r"\ba fight for these tender\b", "a sight for these tender"),
    (r"\bfet out\b", "set out"), (r"\bTY the Bay\b", "to the Bay"),
    (r'"?Braf ?Is\b', "Brazils"), (r"\bBrafils\b", "Brazils"), (r"\bdiliverance\b", "deliverance"),
    (r"\bAt leaft\b", "At least"), (r'\benter" ?prise\b', "enterprise"),
    (r"\ba fling\b", "a sling"), (r"\bunderftanding\b", "understanding"),
    (r"\bfour core\b", "fourscore"), (r"\bfurnithed\b", "furnished"),
    (r"\binspe&", "inspect"), (r"\bo& castle\b", "of castle"), (r"\bfafe\b", "safe"),
    (r"\bindemntfied\b", "indemnified"), (r"\basa reward\b", "as a reward"),
    (r"\bPortugucse\b", "Portuguese"), (r"\bPoriuguese\b", "Portuguese"),
    (r"\bthe ven,", "the van,"), (r"\b7 ?erre-plain\b", "terre-plain"),
    (r"\byiclding the WL\b", "yielding the victory"), (r"\bsurptising\b", "surprising"),
    (r"\bhis bead\b", "his head"), (r"\bhis fide\b", "his side"),
    (r"\bto Jose ground\b", "to lose ground"), (r"\bsormer\b", "former"),
    (r"\bby found of trumpet\b", "by sound of trumpet"), (r"\badvan\. tage\b", "advantage"),
    (r"\bcalumaious\b", "calumnious"), (r"\ball forts\b", "all sorts"),
    (r"\bdelerved\b", "deserved"), (r"\btaken fram\b", "taken from"),
    (r"\bTo this effect essect\b", "To this effect,"), (r"\bCortal\b", "Coreal"),
    (r"\bCareal\b", "Coreal"), (r"\batter these rash\b", "after these rash"),
    (r"\bThele\b", "These"), (r"\bnow and taen\b", "now and then"),
    (r"\blift of all the mines\b", "list of all the mines"), (r"\bFracts\b", "tracts"),
    (r"\ba uarter\b", "a quarter"), (r"\bdiicharge\b", "discharge"), (r"\bLetus\b", "Let us"),
    (r"\bonesself\b", "one's self"), (r"\bther pressing\b", "their pressing"),
    (r"\bintolerable ke\b", "intolerable yoke"), (r"\bfull weil\b", "full well"),
    (r"\bperfon\b", "person"), (r"\bhaye\b", "have"), (r"\bBisho to visit\b", "Bishops to visit"),
    (r"\bot these deeds\b", "of these deeds"), (r"\bGo\. vernour\b", "Governour"),
    (r"\bsub3:&s\b", "subjects"), (r"\bCorreg ?iders?\b", "Corregidors"),
    (r"\bBerua\b", "Barua"), (r"\bdiicovered\b", "discovered"), (r"\bsent go\b", "sent to"),
    (r"\bimpu— tations\b", "imputations"), (r"\bIntherto\b", "hitherto"),
    (r"\bSscilies\b", "Sicilies"), (r"F\. “Aguilar", "F. Aguilar"),
    (r"\bsubje&", "subject"), (r"\bjnsolence\b", "insolence"), (r"\bte parish\b", "the parish"),
    (r"\bare - capable\b", "are capable"), (r"\bbee Father\b", "Father"),
    (r"d“ ?Aguilar", "d' Aguilar"), (r"\breafon\b", "reason"), (r"\bFilla-rica\b", "Villa-rica"),
    (r"\bnow\.made\b", "now made"), (r"\bdesetve\b", "deserve"),
    (r"\bmanufactutes\b", "manufactures"), (r"\boverptus\b", "overplus"),
    (r"\bMissions aries\b", "Missionaries"), (r"\bnecesfary and ufeful\b", "necessary and useful"),
    (r"\bthe lale\b", "the sale"), (r"\bglals\b", "glass"), (r"\bthar a Spaniard\b", "that a Spaniard"),
    (r"\brmitted\b", "permitted"), (r"\btlie Sanisb\b", "the Spanish"),
    (r"\bdragoens\b", "dragoons"), (r"\bproper ule\b", "proper use"),
    (r"\bviz,", "viz."), (r"\bro convert\b", "to convert"), (r"\bAbifoues\b", "Abipones"),
    (r"\byoridly\b", "worldly"), (r"\bhindring\b", "hindering"),
    (r"\blo many fugitives\b", "so many fugitives"), (r"\brelieye the fick\b", "relieve the sick"),
    (r"\bmake ule of thein\b", "make use of them"), (r"\btheirvanity\b", "their vanity"),
    (r"\bfreih\b", "fresh"), (r"\bGencral's\b", "General's"), (r"\bobsewed\b", "observed"),
    (r"\bs6 many\b", "so many"), (r"\basingle\b", "a single"), (r"\binconteftable\b", "incontestable"),
    (r"\bfupply\b", "supply"), (r"\brotectors\b", "protectors"), (r"\bina word\b", "in a word"),
    (r"\bPbilip\b", "Philip"), (r"F\. 4 Aguilar", "F. d' Aguilar"),
    (r"\bequipt were ready do march\b", "equipt were ready to march"),
    (r"\bJeseph\b", "Joseph"), (r"\bD\. Foseph\b", "D. Joseph"),
    (r"\bcom- ?ng routed\b", "completely routed"), (r"\btheir wes\b", "their lives"),
    (r"\blives ro to the mercy\b", "lives to the mercy"),
    (r"\bwho rously allowed\b", "who generously allowed"), (r"\bBrasl\b", "Brasil"),
    (r"\btha that\b", "that"), (r"\bexe perience\b", "experience"),
    (r"\bIuancvita\b", "Ivanovitz"), (r"\bmolt\b(?= (earnestly|to fix|own))", "most"),
    (r"\bmult own\b", "must own"), (r"\btrom certain\b", "from certain"),
    (r"\bpaid; with\b", "paid with"), (r"\bthey\.\. have\b", "they have"),
    (r"\bthese\. good\b", "these good"), (r"\bwere\.in\b", "were in"),
    (r"Redu#ton?s\b", "Reductions"), (r"Reduf/ions?\b", "Reduction"),
    (r"Redut#ions\b", "Reductions"), (r"Redut7ions\b", "Reductions"),
    (r"\b1s exacted\b", "is exacted"),
]

# Exact-string surgery on assembled paragraphs: page-turn losses restored from
# the raw scan, misplaced fragments returned to their sentences, quire and
# running-head debris excised. Every entry is a disclosed emendation.
PARA_FIXES = [
    ("This conduct of the 3 *. not * less prejudicial to the con- cerns nces.'",
     "This conduct is not less prejudicial to the con-"),
    ("subject to the Spa-", "subject to the Spaniards."),
    ("The rest of the Country is either niards. deserted, or possessed",
     "The rest of the Country is either deserted, or possessed"),
    ("prudence and equiHence the misfortune", "prudence and equity. Hence the misfortune"),
    ("the very authors of these wks A whe who transmit", "the very authors of these evils, who transmit"),
    ("Province of Tu- & (#7432,", "Province of Tucumán;"),
    ("the Indians had ial. & facred Spaniards", "the Indians had massacred Spaniards"),
    ("Such are the v fruits of oppression, pride, and covetousness. a should not be attended with pernicious conti",
     "Such are the fruits of oppression, pride, and covetousness;"),
    ("sequences; it must of necessity have another effect of very great prejudice to the crown of ar Spain. The best peopled Colonies are soon k. reduced. The Indian families are destroyed by fir degrees; and the number of inhabitants, the th main support of a state, and without which the MF ve",
     "and it must of necessity have another effect of very great prejudice to the crown of Spain. The best peopled Colonies are soon reduced. The Indian families are destroyed by degrees; and the number of inhabitants, the main support of a state, and without which the"),
    ("- most extended and fruitful Country", "most extended and fruitful Country"),
    ("College of Cor-", "College of Cor-"),
    ("agua dova in the Tucwnar,", "dova in the Tucuman,"),
    ("E With with Europeans.", "with Europeans."),
    ("that follow in this", "that follow in this work."),
    ("sold their slaves very cheap w others", "sold their slaves very cheap to others"),
    ("Nv The Principal Obstacles the inhuman treatment", "the inhuman treatment"),
    ("of fo wise a regulation,", "of so wise a re-"),
    ("gulation, and so agreeable to the laws of nature.", "gulation, and so agreeable to the laws of nature."),
    ("which they dis- honoured as desire to lead a licentious life with impunity.",
     "which they dis-"),
    ("or such", "or such as desire to lead a licentious life with impunity."),
    ("ü. 56 The Principal Obstacles, &c. of the Indians,", "of the Indians,"),
    ("above above two millions", "above two millions"),
    # IX
    ("of making' their advantage", "of making their advantage"),
    ("a new Reduction. %n Besides", "a new Reduction. Besides"),
    ("a band of. musicians", "a band of musicians"),
    ("inferior to that the Spanish cathedrals", "inferior to that of the Spanish cathedrals"),
    ('among * " bother other things', "among other things"),
    ('February 1730, would gladly have', 'February 1730: "I would gladly have'),
    ("to fix their a-", "to fix their abode there."),
    ("so. glorious for this charming art, as being highly. instrumental",
     "so glorious for this charming art, as being highly instrumental"),
    ("a singular, honour", "a singular honour"),
    # XV
    ("will not be easily appy", "will not be easily persuaded of it"),
    ("suffici- we F > sufficient", "sufficient"),
    ("difficult the christian Settlements.. Buy to produce precedents",
     "difficult to produce precedents"),
    ("carried to the ello of the Governor", "carried to the tribunal of the Governor"),
    ("these burthens, by the privileges", "these burthens, by the privileges"),
    ("has confirmed. The author wrote bis", "has confirmed."),
    (". first, all the Indians", "1st. All the Indians"),
    ("24ly.", "2dly."), ("3aly.", "3dly."),
    ("A the Caciques, as being noble", "4thly. The Caciques, as being noble"),
    ("perforis be made over in see", "persons be made over in fee"),
    ("Comm endam", "Commendam"), ("other other vexations", "other vexations"),
    ("theirembarkation", "their embarkation"), ("allo at at the expence", "also at the expence"),
    ("in Pera and Chili, which yield a pretty good vine",
     "in Peru and Chili, which yield a pretty good wine"),
    ("for their wse", "for their use"),
    ("catholic Maje- ty's", "catholic Majesty's"),
    ("their own defence. p", "their own defence."),
    ("advantage for the", "advantage for the"),
    ("wast have cost", "must have cost"),
    ("K 2 of of cattle", "of cattle"),
    ("herdsmen, ma-", "herdsmen, ma-"),
    ("Fons, joiners, and carters", "sons, joiners, and carters"),
    ("— 2 WW — — * + ow these satigues", "these fatigues"),
    ("ents, The same would happen", "The same would happen"),
    ("took care to let them that many better", "took care to let them know that many better"),
    ("spends his the christian Seltlements:. 13s ce days at work",
     "spends his days at work"),
    ("I think they would grace a", 'I think they would grace a collection."'),
    ("If the Indians have no great success", "If the Indians have no great success"),
    # XVIII
    ("these barbari-", "these barbari-"),
    ("I ans ans, who are enemies", "ans, who are enemies"),
    ("a crucifix in his respect a priest of Jesus Christ",
     "a crucifix in his hand, hoping they would respect a priest of Jesus Christ"),
    ("comforting their ae, hand, with hopes that men who went till under",
     "comforting their afflicted charge, with the hope that men who went still under"),
    ("Py As eds % tw TW -A—_ﬀ ws aged, and procuring", "and procuring"),
    ("Neither the 9 ious behaviour", "Neither the impious behaviour"),
    ('some” to work i in the mines', "some to work in the mines"),
    ("the Cavalry with, lances and", "the Cavalry with lances and fire arms."),
    ("To prevent any such fatal accidents for the were formed in every Reduction",
     "To prevent any such fatal accidents for the future, companies of foot, and troops of horse, were formed in every Reduction"),
    ("in order. AY future, companies of foot, and troops of horse,", "in order."),
    ("And this is — for the welfare", "And this is necessary for the welfare"),
    ("a hundred and fourscore miles to observe whether any thing is done, that seems",
     "a hundred and fourscore miles to observe whether any thing is done that seems"),
    ("M saw saw himself", "saw himself"),
    ("'n + make make this acknowledgement", "to make this acknowledgement"),
    ("+ _ officers to head them", "officers to head them"),
    ("VT 5 horses without riders", "The horses without riders"),
    ("Ndians came next", "Indians came next"),
    ("to ng the the terreplain", "to the terre-plain"),
    ("In 1735 four thousand", ""),
    # XX
    ("labour s 2 in in behalf", "labours in behalf"),
    ("against the — justice in the King's name in every Reduction.", "against the Missionaries"),
    ("now repeat it, administers", "now repeat it, administers justice in the King's name in every Reduction."),
    (". CY\" * N on, 8 * 1 P a * * — the relief", "the relief"),
    ("of & less than that", "or less than that"),
    ("change the ee the taking of such a step", "change the government, the taking of such a step"),
    ("7 he breed of Spaniards or Europeans with original Americaus. a",
     "* The breed of Spaniards or Europeans with original Americans."),
    ("— a ws arts — — the standard of rebellion, and in conjunction many instances",
     "many instances"),
    ("become their most implacable enemies;",
     "raise the standard of rebellion, and become their most implacable enemies;"),
    ("to set up with the Infidels to bring their whole force: a-",
     "to join with the Infidels and bring their whole force a-"),
    ("#xinst that handful", "gainst that handful"),
    ("his own = of", "his own use."),
    ("*Tis seen immediately, that the quantity of the goods they trade in 2 the wk aol he n= use use that is made",
     "'Tis seen immediately, that the quantity of the goods they trade in, and the use that is made"),
    ("Now this is the 7 -, unjalt", "Now this is the unjust"),
    ("— S..)IYITOLDp 2 tr &, yo & unjust and dangerous trade", "and dangerous trade"),
    ("To prevent these evils, the O3 Spaniards", "To prevent these evils, the"),
    ("Saniards were forbidden", "Spaniards were forbidden"),
    ("the Pampas settled in the country adjacent to Cordova, is to hope for the conversion of th",
     "the Pampas settled in the country adjacent to Cordova."),
    ("has been already gainst the Missionaries of Paraguay; 199 observed...",
     "has been already observed."),
    ("O 4 been been infallibly", "been infallibly"),
    ("totally ignorant of. Nn Would none of them have reveal - ed it:",
     "totally ignorant of it? Would none of them have revealed it?"),
    ("that a superior can use, all particulars", "to all particulars"),
    ("palliated trafic, or any charity, from the lands of the Reauctions, duftions, to poor Colleges",
     "palliated traffic, or any charity from the lands of the Reductions, even to poor Colleges"),
    ("nature.“", 'nature?"'),
    ("the Government found powerful rotectors", "the Governour found powerful protectors"),
    ("too strong strong a proof", "too strong a proof"),
    ("— — — — A WE\" mote the conversion", "mote the conversion"),
    ("nor silver, nor any money", "nor silver, nor any money"),
    ("<4. nor nor silver", "nor silver"),
    ("t 12 - ti", ""),
    ('FFP WARS. 4 S. % #7 4 * - IT io. " and it must', "and it must"),
]

UNIT_DROPS = {"dr.", "SS, r", "— wi wh a 2 v1.", "mg > ==", "Ow", "M 4 mar",
              "I; \"-.- a ot md a. wb\" ho tn ni. an."}
UNIT_PREFIX_DROPS = ("* N 5 n FO a",)

DANGLING = re.compile(r"\b(the|a|an|of|to|for|and|or|with|by|in|on|at|as|those|these|their|his|her|its|our|is|are|was|were|be|have|has|who|which|that)$", re.I)

def polish_units(units):
    out = []
    for u in units:
        en = u["en"]
        for old, new in PARA_FIXES:
            if old in en:
                en = en.replace(old, new)
        en = re.sub(r"^[^A-Za-z0-9\"'‘“*]+", "", en)   # leading symbol junk
        en = re.sub(r"\b([A-Za-z]{2,})\s+\1\b(?!\s+\1)",
                    lambda m: m.group(1) if m.group(1).lower() not in ("had", "that", "very", "so") else m.group(0),
                    en)                                           # page-turn word doubling
        en = en.replace("{", "").replace("}", "")
        en = re.sub(r"\s[&%]\s(?!c\.)", " ", en)         # quote-debris islands ('&c.' untouched)
        en = re.sub(r"\s<\s?", " ", en)
        en = re.sub(r"\s{2,}", " ", en).strip()
        real_words = len(re.findall(r"[A-Za-z]{3,}", en))
        if not en or en in UNIT_DROPS or en.startswith(UNIT_PREFIX_DROPS) \
           or (real_words <= 3 and len(en) < 220) \
           or (len(en) < 18 and alpha_ratio(en) < 0.7):
            continue
        u = dict(u); u["en"] = en
        out.append(u)
    # merge page-turn breaks: dangling function word, trailing hyphen, or a
    # continuation that begins lowercase after an unpunctuated end
    merged = []
    for u in out:
        if merged:
            prev = merged[-1]["en"]
            if prev.endswith("-"):
                merged[-1]["en"] = prev[:-1] + u["en"]
                continue
            if DANGLING.search(prev) or (re.match(r"^[a-z]", u["en"]) and not prev.endswith((".", "!", "?", ":", '"', "”"))):
                merged[-1]["en"] = prev + " " + u["en"]
                continue
        merged.append(u)
    # second pass over the merged text: fixes whose target only exists once
    # page-turn pieces are joined, and line-break hyphens inside paragraphs
    for u in merged:
        en = u["en"]
        for old, new in PARA_FIXES:
            if old in en:
                en = en.replace(old, new)
        en = re.sub(r"(\w)- (?=[a-z])", r"\1", en)
        u["en"] = re.sub(r"\s{2,}", " ", en).strip()
    return merged

def fix_text(s):
    for pat, rep in WORD_FIXES:
        s = re.sub(pat, rep, s)
    # long-s survivals rendered as '{', '|' inside words; stray page furniture
    s = re.sub(r"[{|](?=[a-z])", "", s)
    s = re.sub(r"\s*\|\s*", " ", s)
    s = re.sub(r"[©®„‚]+\*?", "", s)
    s = re.sub(r"[»«]", '"', s)
    s = re.sub(r'\s+[04&]"\s*', " ", s)          # mangled opening quotes „4" ©*
    s = re.sub(r"(?<=, )c\.(?=\s|$)", "&c.", s)  # the print's '&c.' lost its ampersand
    s = re.sub(r"\s+([,;:.!?])", r"\1", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def strip_chapter_furniture(units, open_fix, titel):
    # drop leading chapter-number lines and the chapter's own argument/title
    # paragraph (identified by its keywords); restore the opening drop-cap
    keys = [w.lower() for w in re.findall(r"[A-Za-z]{5,}", titel)]
    out = list(units)
    while out:
        head = out[0]["en"]
        low = head.lower()
        is_chap = re.match(r"^\s*C\s*H\s*A\s*P\b", head) and len(head) < 80
        is_title = len(head) < 230 and sum(k in low for k in keys) >= 2
        if not (is_chap or is_title):
            break
        first_label = out[0].get("label")
        out = out[1:]
        if out and first_label and "label" not in out[0]:
            out[0]["label"] = first_label
    if out and open_fix:
        out[0]["en"] = re.sub(open_fix[0], open_fix[1], out[0]["en"])
    return out

# ---------------------------------------------------------- Montoya (1892)
MONTOYA = [
    dict(page="p. 157",
         label="The fleet of rafts at the falls of the Paraná (1631)",
         orig="Volvamos ahora á nuestra flota de balsas, que iba caminando, al parecer segura "
              "de enemigos que por detrás dejaba, cuando tuvimos aviso que los españoles, "
              "vecinos de Guairá, nos aguardaban en un estrecho y peligroso paso que hace el "
              "famoso salto del Paraná, en cuya ribera habían fabricado una fortaleza de palos "
              "para impedirnos el paso y cautivar la gente. La traza era que desde este fuerte, "
              "al pasar las embarcaciones, fuesen derribando los remeros y gente que podía "
              "defenderse, y debilitando con esto aquella tropa, saliesen ellos á la presa. "
              "Supe el caso, y dudoso que fuese así, dejando la gente, me adelanté en una "
              "embarcación ligera. Hallé ser verdad; entré en aquel palenque, seguro de "
              "traición; quejéme dando mis razones, á que cerrando los oídos sacaron sus "
              "espadas, y poniéndome cinco á los pechos me quisieron tener por prisionero. "
              "Salí por medio de ellas ayudado de una sobrerropa que llevaba.",
         en="Let us return now to our fleet of rafts, which went on its way, safe, as it "
            "seemed, from the enemies it was leaving behind, when word reached us that the "
            "Spaniards, the settlers of Guairá, were waiting for us at the narrow and dangerous "
            "passage made by the famous falls of the Paraná, on whose bank they had built a "
            "stockade of timber to bar our passage and enslave the people. The plan was that "
            "from this fort, as the vessels passed, they would shoot down the rowers and "
            "whoever could defend himself, and, having weakened the company, come out for "
            "their prey. I learned of it and, doubting it could be so, left the people and "
            "went ahead in a light craft. I found it true; I entered that stockade, certain of "
            "treachery; I made my complaint and gave my reasons — at which, shutting their "
            "ears, they drew their swords, and setting five points at my breast would have "
            "taken me prisoner. I came out from among them, helped by an overgarment I wore."),
    dict(page="p. 158",
         label="Three embassies, and the fort gives way",
         orig="Volví á mis compañeros á consultar el caso, que causó á todos pena y dolor, "
              "viéndose perseguidos y atajados de la fortuna, que por todas partes quería hacer "
              "presa de ellos. Resolvimos que volviesen dos Padres á requerir á aquellos "
              "hombres nos diesen paso libre... Fuimos dos religiosos; roguélos que nos dejasen "
              "pasar; hallélos aún con más aceros á la resistencia... Los españoles, picados de "
              "lo que oyeron, recelaron su dureza; ya no se veían seguros en el fuerte, ya les "
              "parecía verse consumidos, y cuando la conciencia aprieta los cordeles aparece la "
              "verdad muy clara. Juzgaron su acción por muy injusta, y así, enviándonos "
              "mensajeros, nos pidieron que les diésemos término y seguro para salir de aquel "
              "palenque. Dióseles con mucha humanidad y cortesía.",
         en="I returned to my companions to take counsel, which brought grief and pain to "
            "all, seeing themselves hunted and cut off by a fortune that on every side sought "
            "to make them its prey. We resolved that two Fathers should go back and demand of "
            "those men free passage... I went myself with another religious; I begged them to "
            "let us pass, and found them harder set than ever on resistance... But the "
            "Spaniards, stung by what they had heard, began to mistrust their own hardness; "
            "they no longer felt safe in their fort, they seemed to themselves already "
            "consumed; and when conscience tightens the cords, the truth appears very plain. "
            "They judged their own action most unjust, and so, sending us messengers, they "
            "asked us for terms and safe-conduct to quit that stockade. It was granted them "
            "with much humanity and courtesy."),
    dict(page="pp. 158–159",
         label="Three hundred canoes over the falls",
         orig="Con esto tomamos aquel puesto, donde fué fuerza dejásemos las canoas; porque "
              "por allí es innavegable el río por la despeñada agua, que forma remolinos tales, "
              "que rehúsa la vista el verlos por el temor que causan. Con todo eso probamos á "
              "echar por aquellas rocas de agua 300 canoas, por ver si salían algunas sanas, "
              "porque pasadas 25 leguas que habíamos de fuerza caminar por tierra, habíamos de "
              "volver á tomar el mismo río y rumbo; pero el ímpetu del agua, la profundidad "
              "inmensa y el arrebatado movimiento con que daba con ellas en asperísimos "
              "escollos, las volvía astillas... Pasado ya aqueste impedimento, tratamos de "
              "seguir nuestro camino por tierra; todo viviente apercibía su carga: varones, "
              "mujeres y niños, acomodando sobre sus costillas sus alhajas y su comida.",
         en="With this we took that post, where of necessity we had to abandon the canoes; "
            "for there the river is unnavigable by reason of the falling water, which makes "
            "such whirlpools that the eye refuses to look on them for the terror they cause. "
            "Even so we tried sending three hundred canoes down over those rocks of water, to "
            "see whether any would come through whole; for after the twenty-five leagues we "
            "were forced to march overland, we had to take to the same river and course again. "
            "But the rush of the water, the immense depth, and the violent motion with which "
            "it dashed them on the sharpest reefs turned them all to splinters... That "
            "obstacle passed, we set ourselves to follow our road by land; every living soul "
            "took up a burden — men, women and children, settling on their shoulders their "
            "few treasures and their food."),
    dict(page="pp. 229–231",
         label="The deaths of Roque González and Alonso Rodríguez at Caaró (1628)",
         orig="Estaban tan ignorantes los Padres de esta alevosía, que los PP. Roque y Alonso "
              "trataron de celebrar fiesta á la dedicación del pueblo del Caaró... El santo "
              "P. Roque, después de haber dicho la Misa y dado (con la devoción que solía) "
              "gracias al Altísimo, por sus propias manos quiso atar la lengüeta á una "
              "campana, cosa nunca vista de aquella gente bárbara, para con su sonido "
              "regocijar la fiesta. Apenas le vió Carupé, cacique principal, ocupado en esta "
              "acción, cuando hizo señas á un esclavo suyo, que ya estaba prevenido, para que "
              "le matase. Levantó este vil esclavo una porra de armas, que aunque de madera "
              "imitaba al hierro en su dureza y forma, y dando al Padre un furioso golpe en el "
              "cerebro le hizo pedazos la cabeza, con que á golpes y repique de campana voló "
              "su alma regocijada al cielo. Hoy tenemos esta campana por reliquia... Partieron "
              "en cuadrilla á la choza donde el P. Alonso estaba, que al ruido de la algazara "
              "llegaron juntos él y su muerte á los umbrales... y el Padre con amor de hijo se "
              "acercó á su ya muerto Padre, repitiendo estas razones: ¿Hijos, por qué me "
              "matáis? ¿Qué hacéis, hijos? ... en los mismos umbrales le cogió la muerte.",
         en="So ignorant were the Fathers of this treachery that Fathers Roque and Alonso "
            "set about celebrating the feast of the dedication of the town of Caaró... The "
            "holy Father Roque, after saying mass and giving thanks to the Most High with his "
            "accustomed devotion, wished with his own hands to hang the clapper in a bell — a "
            "thing never yet seen among that barbarous people — to gladden the feast with its "
            "sound. Scarcely had Carupé, the principal cacique, seen him occupied in this work "
            "when he made a sign to a slave of his, already prepared, to kill him. That vile "
            "slave raised a war-club which, though of wood, imitated iron in hardness and "
            "form, and striking the Father a furious blow on the skull shattered his head — "
            "and so, amid blows and the pealing of the bell, his rejoicing soul flew to "
            "heaven. We keep that bell today as a relic... Then they went in a band to the "
            "hut where Father Alonso was, who at the noise of the tumult arrived together "
            "with his death at the threshold... and the Father, with a son's love, drew near "
            "his already dead Father, repeating these words: Children, why do you kill me? "
            "What are you doing, children? ... on that same threshold death took him."),
]

def build():
    t = load_source()
    sections = []
    n = 0
    for S in SECTIONS:
        paras = clean_section(t[S["start"]:S["end"]], S["page0"])
        units = []
        last_page = None
        for p in paras:
            u = {"en": fix_text(p["text"])}
            if p["page"] != last_page:
                u["label"] = f"p. {p['page']}"
                last_page = p["page"]
            units.append(u)
        units = strip_chapter_furniture(units, S.get("open_fix"), S["titel"])
        units = polish_units(units)
        if S.get("end_key"):
            for j, u in enumerate(units):
                if S["end_key"] in u["en"]:
                    units = units[:j + 1]
                    break
        for k, u in enumerate(units, start=1):
            n += 1
            u["n"] = n
            u["k"] = k
        sections.append({"id": S["id"], "zk": S["zk"], "titel": S["titel"],
                         "blurb": S["blurb"], "units": units})
        print(f"  {S['zk']:12s} {len(units):3d} ¶  (pp. {paras[0]['page']}–{paras[-1]['page']})")

    m_units = []
    for k, M in enumerate(MONTOYA, start=1):
        n += 1
        m_units.append({"n": n, "k": k, "orig": M["orig"], "en": M["en"],
                        "label": f"{M['label']} · {M['page']}"})
    sections.append({
        "id": "montoya", "zk": "Mont.",
        "titel": "Montoya's own voice: the exodus, and the martyrs of Caaró",
        "blurb": "Four passages of the Conquista espiritual (1639), bilingual: the protagonist "
                 "of the great exodus of 1631 at the falls of the Paraná — the stockade, the "
                 "three embassies, the three hundred canoes — and the deaths of Roque González "
                 "and Alonso Rodríguez at Caaró in 1628, with the bell kept as a relic.",
        "units": m_units})
    print(f"  {'Mont.':12s} {len(m_units):3d} ¶")

    data = {
        "id": "paraguay",
        "autor": "Muratori · Ruiz de Montoya",
        "titel": "The Reductions of Paraguay — Muratori's Relation, with Montoya's voice",
        "jahr": 1639,
        "lang": "es",
        "zitierweise": "Mur. c. N [k] · Mont. [k]",
        "quelle": ("English: L. A. Muratori, A Relation of the Missions of Paraguay (London "
                   "1759; Internet Archive bim_eighteenth-century_a-relation-of-the-missio_"
                   "muratori-lodovico-anton_1759), public domain — chapters V, IX, XV, XVIII "
                   "and XX carried complete, page numbers of the 1759 print on the paragraphs. "
                   "Spanish: A. Ruiz de Montoya, Conquista espiritual (Madrid 1639), quoted "
                   "from the Bilbao reprint of 1892 (IA conquistaespiri00montgoog), four "
                   "passages transcribed from the OCR and emended against the sense; the "
                   "English of those passages is this site's unofficial working translation."),
        "hinweis": ("The second program's opening module: the Society's boldest social "
                    "experiment, in the two voices that carried it to Europe — the outside "
                    "admirer and the protagonist. Muratori never saw Paraguay; he compiled "
                    "from the missionaries' letters, and says so; the 1759 London English "
                    "(made from the French) is carried as printed, its eighteenth-century "
                    "spellings kept and only scan damage repaired. Chapter numbers destroyed "
                    "by the OCR are restored from the book's own table of contents and the "
                    "chapter sequence. Montoya's four passages are the protagonist's own "
                    "first person, thirty years in the missions, written for the court of "
                    "Madrid. Part of the concordance and the citation-bound dialogue; not "
                    "part of the linguistic statistics, which describe the core corpus only."),
        "sections": sections,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    total = sum(len(s["units"]) for s in sections)
    print(f"wrote {os.path.normpath(OUT)}: {len(sections)} sections, {total} paragraphs")

if __name__ == "__main__":
    build()
