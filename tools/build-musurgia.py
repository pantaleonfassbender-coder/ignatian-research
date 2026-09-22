# -*- coding: utf-8 -*-
"""Build data/musurgia.json — Kircher's Musurgia universalis (Rome 1650).

The Society's book of music, in a deliberately narrow cut. Source: the
Fribourg scan of Tomus I on the Internet Archive (`chepfl-lipr-AXC19_01`,
Musurgia universalis t. 1, Rome: Corbelletti, 1650), public domain; a second
scan (`bub_gb_97xCAAAAcAAJ`) stands as collation reference. The Latin below
was transcribed from the OCR and emended against the sense and the page
images (long-s, ligatures and the scan's æ→z class resolved; u/v left as
classicised); the English is this site's unofficial working translation,
dedicated CC0.

Three sections. (1) The Synopsis of the ten books, from the front matter —
Kircher's whole architecture in one page, ending in the ten Registers of the
decachordon naturae, up to 'the music of the Archetype, God's concert with
universal nature'. (2) The voices of the birds, Lib. I, pp. 28–32, with
Iconismus III (fol. 30) carried as an image: the nightingale as the Idea of
all music, and the cock, hen, quail, cuckoo and parrot in musical notation.
(3) The pathetic music, Lib. VII, pp. 550–551: the four conditions for
moving the affects, Timotheus and Alexander with Petrarch's quatrain, and
the temperaments — Kircher's program for renewing the miracles of ancient
music. Printed pages cited from the running heads; Iconismus III carries
its own folio number (fol. 30)."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "musurgia.json")

def u(n, k, orig, en, label=None, note=None, img=None, alt=None):
    d = {"n": n, "k": k}
    if orig: d["orig"] = " ".join(orig.split())
    if en: d["en"] = " ".join(en.split())
    if label: d["label"] = label
    if note: d["note"] = note
    if img: d["img"] = img
    if alt: d["alt"] = alt
    return d

SYN1_LA = """Liber I. Physiologicus, soni naturalis genesin, naturam et
proprietatem effectusque demonstrat. Liber II. Philologicus, soni
artificialis sive Musicae primam institutionem propagationemque inquirit.
Liber III. Arithmeticus, motuum harmonicorum scientiam per numeros, et novam
Musicam Algebraicam docet. Liber IV. Geometricus, intervallorum
consono-dissonorum originem per monochordi divisionem Geometricam,
Algebraicam, Mechanicam multiplici varietate ostendit. Liber V. Organicus,
instrumentorum omnis generis Musicorum structuram novis experimentis aperit.
Liber VI. Melotheticus, componendarum omnis generis cantilenarum novam et
demonstrativam methodum producit, continetque quicquid circa hoc negotium
curiosum, rarum et arcanum desiderari potest. Liber VII. Diacriticus,
comparationem veteris Musicae cum moderna instituit, abusus detegit, cantus
Ecclesiastici dignitatem commendat, methodumque aperit qua ad patheticae
Musicae perfectionem tandem perveniri possit."""
SYN1_EN = """Book I, the Physiological, demonstrates the genesis, nature,
property and effects of natural sound. Book II, the Philological, inquires
into the first institution and spread of artificial sound, that is, of
Music. Book III, the Arithmetical, teaches the science of harmonic motions
through numbers, and a new Algebraic Music. Book IV, the Geometrical, shows
the origin of the consonant and dissonant intervals through the division of
the monochord — geometrical, algebraical, mechanical — in manifold variety.
Book V, the Organic, opens by new experiments the structure of musical
instruments of every kind. Book VI, the Melothetic, produces a new and
demonstrative method of composing songs of every kind, and contains whatever
curious, rare and secret can be desired in this business. Book VII, the
Diacritic, institutes the comparison of ancient music with modern, uncovers
the abuses, commends the dignity of the Church's chant, and opens the method
by which the perfection of pathetic music may at last be reached."""

SYN2_LA = """Liber VIII. Mirificus, novam artem Musarithmicam exhibet, qua
quivis etiam Musicae imperitus ad perfectam componendi notitiam brevi
tempore pertingere possit; continetque Musicam Combinatoriam, Poeticam,
Rhetoricam, Planglossiam Musarithmicam omnibus linguis novo artificio
adaptatam. Liber IX. Magicus, reconditiora totius Musicae arcana producit;
continetque physiologiam consoni et dissoni, praeterea Magiam
Musico-medicam, Phonocampticam sive perfectam de Echo doctrinam, novam
tuborum otacousticorum sive auricularium fabricam, item statuarum ac aliorum
instrumentorum Musicorum autophonorum, seu per se sonantium, uti et
sympathicorum structuram curiosis ac novis experientiis docet; quibus
adnectitur Cryptologia Musica, qua occulti animi conceptus in distans per
sonos manifestantur. Liber X. Analogicus, decachordon naturae exhibet, quo
Deum in trium Mundorum — Elementaris, Coelestis, Archetypi — fabrica ad
Musicas proportiones respexisse per decem gradus, veluti per decem Naturae
Registra, demonstratur."""
SYN2_EN = """Book VIII, the Wonder-working, exhibits a new Musarithmic art
by which anyone, even one unskilled in Music, may in a short time attain a
perfect knowledge of composing; it contains a Combinatorial, a Poetic and a
Rhetorical Music, and adapts the Musarithmic 'Planglossia' to all languages
by a new artifice. Book IX, the Magical, brings forth the more hidden
secrets of all Music: the physiology of consonance and dissonance; besides
these, a Musico-medical Magic; the Phonocamptic, or perfect doctrine of the
Echo; a new construction of otacoustic or ear-trumpets; likewise the
structure of statues and of other self-sounding and sympathetic musical
instruments, taught by curious and new experiments — to which is annexed a
Musical Cryptology, whereby the hidden conceptions of the mind are made
known at a distance through sounds. Book X, the Analogical, exhibits the
ten-stringed instrument of nature, demonstrating that God, in the fabric of
the three Worlds — Elemental, Celestial, Archetypal — had regard to musical
proportions through ten degrees, as through ten Registers of Nature."""

SYN3_LA = """Registrum 1. Symphonismos Elementorum, sive Musicam
Elementarem. Registrum 2. Coelorum admirandam symphoniam in motibus,
influxibus effectibusque. Registrum 3. Lapidum, plantarum, animalium, in
physico, medico, chymico negotio. Registrum 4. Musicam Microcosmi cum
Megacosmo, id est minoris cum maiori mundo. Registrum 5. Musicam
Sphygmicam, sive pulsuum in venis arteriisque sese manifestantem.
Registrum 6. Musicam Ethicam, in appetitu sensitivo et rationali
elucescentem. Registrum 7. Musicam Politicam, Monarchicam, Aristocraticam,
Democraticam, Oeconomicam. Registrum 8. Musicam Metaphysicam, sive
potentiarum interiorum ad Angelos et Deum comparatam. Registrum 9. Musicam
Hierarchicam, sive Angelorum in novem choros distributorum. Registrum 10.
Musicam Archetypam, sive Dei cum universa natura concentum. — In decachordo
Psalterio psallam tibi."""
SYN3_EN = """Register 1: the symphonisms of the Elements, or Elemental
Music. Register 2: the admirable symphony of the heavens in their motions,
influences and effects. Register 3: of stones, plants and animals, in the
physical, medical and chymical business. Register 4: the Music of the
Microcosm with the Megacosm, that is, of the lesser with the greater world.
Register 5: the Sphygmic Music, showing itself in the pulses of veins and
arteries. Register 6: the Ethical Music, shining out in the sensitive and
the rational appetite. Register 7: the Political Music — monarchic,
aristocratic, democratic, economic. Register 8: the Metaphysical Music, of
the interior powers compared to the Angels and to God. Register 9: the
Hierarchic Music, of the Angels distributed into nine choirs. Register 10:
the Archetypal Music, or the concert of God with universal nature. — 'Upon
a psaltery of ten strings will I sing praises unto thee.'"""

BIRD1_LA = """Musicae totius veluti Ideam quandam in Luscinia sive Philomela
natura exhibuit, ut quomodo perfecta cantus ratio ordinanda, ac in gutture
moduli formandi sint, addiscant Phonasci. In solitudinibus simplicem tantum
cantum, veluti sibi canens aut exercitii causa, nullo modulatur apparatu; at
ubi auditores vicinos nacta fuerit, tum veluti vocis suae divitias exponens,
varietate admirabili innumeros fingit sonos: nunc enim in longum aequabiliter
eos producit, nunc eosdem inflectit, iam minutius et concisius canit; nunc
intorquet et quasi crispat vocem, nunc intendit, iam remittit; alios longos
concinit versus quasi heroicos, alios breves ut Sapphicos, interdum
brevissimos ut Adonios; quin etiam quasi musicae ludos et scalas habet.
Praeterea meditantur secum aliae iuniores, imitarique tentant quae ab
adultioribus percipiunt: audit discipula attentione magna, intelligitur
emendata correctio, et in docente quaedam reprehensio."""
BIRD1_EN = """In the nightingale — the Luscinia, or Philomela — nature has
exhibited as it were an Idea of all music, that singing-masters might learn
from her how the perfect scheme of song is to be ordered and its measures
formed in the throat. In the solitudes she sings only a simple song, as if
to herself or for practice, with no apparatus; but when she has found
listeners near, then, as though laying out the riches of her voice, she
fashions innumerable sounds with admirable variety: now she draws them out
long and evenly, now bends them, now sings more minutely and concisely; now
she twists and as it were crisps her voice, now strains it, now lets it
fall; some verses she sings long, as it were heroic, others short, like
Sapphics, sometimes shortest of all, like Adonics; nay, she has even her
musical games and scales. Moreover the younger ones meditate by themselves
and try to imitate what they catch from their elders: the pupil listens
with great attention, an emended correction is understood, and in the
teacher a certain reproof."""

BIRD2_LA = """Quis autem satis mirari potest tantam in tam parvo corpusculo
vocem, tam pertinacem spiritum? Breviter: omnia faucibus tam angustis
perficiuntur, quae tot exquisitis tibiarum tormentis ars hominum
excogitavit. Et ne quid artis deesset, plures singulis sunt cantus, nec
iidem omnibus, sed sui cuique; certant inter se, palamque animosa fit
contentio; morte finit saepe vitam, spiritu prius deficiente quam cantu: ut
merito totius harmonicae modulationis Epitome dici queat. Miram huius
aviculae modulationis vim cum saepius non sine admiratione attendissem,
maximum me invasit desiderium, non solum clausulas hasce longe admirabiles
in notas musicas transferendi, sed et anatomiam aviculae faciendi, ut sic
tantae modulationis causa plenius innotesceret: quorum et utrumque factum
est."""
BIRD2_EN = """Who can sufficiently marvel at so great a voice in so small a
body, at a breath so persevering? In brief: all that the art of man has
devised with so many exquisite engines of pipes is accomplished in a throat
so narrow. And that nothing of art should be wanting, each bird has several
songs, and not the same for all, but each her own; they contend with one
another, and the spirited contest is open; often she ends her life in
death, the breath failing before the song — so that she may deservedly be
called the Epitome of all harmonic modulation. Having often attended, not
without admiration, to the wondrous power of this little bird's modulation,
a very great desire seized me not only to transfer these most admirable
clausulae into musical notes, but also to make an anatomy of the little
bird, that the cause of so great a modulation might be more fully known —
and both were done."""

BIRD3_LA = """Regulus proxime sequitur Lusciniam, qui nonnullas in formandis
glottismis clausulas mutuatur a Luscinia. Reliquae volucres vocem quidem
habent sonoram, sed nulla supramemorata glottismi specie adornatam, uti sunt
Gallus, Gallina, Coccyx, Hirundo, Upupa, Ulula, Coturnix similesque: cum
enim vox earum ad hominum delectationem non sit ordinata, eam tantum vocem,
quae passionibus animi explicandis sufficiat, exprimunt. Sed non abs re me
facturum existimavi, si quarundam voces hic musicis modulis referam. Et
quidem Gallus in primis varias voces edit: aliam quidem dum zelotypia
agitatur, aliam dum init gallinas, aliam dum tempus indicat, quae vox
propria Galli est, unde et gallicinium; format autem vocem suam eo fere
modo, quem in Iconismo III nota A exprimunt."""
BIRD3_EN = """The wren follows next after the nightingale, borrowing from
her some clausulae in the forming of his glottisms. The remaining birds
have indeed a sonorous voice, but adorned with none of the above-mentioned
kinds of glottism — such are the cock, the hen, the cuckoo, the swallow,
the hoopoe, the owl, the quail and their like: for since their voice is not
ordered to the delight of men, they utter only such voice as suffices to
declare the passions of their soul. Yet I judged it not amiss to render
here the voices of some of them in musical measures. And first the cock
utters various voices: one when he is stirred by jealousy, another when he
treads the hens, another when he tells the hour — which is the cock's own
voice, whence 'gallicinium', cock-crow; and he forms it in nearly the
manner which the notes at A in Iconismus III express."""

BIRD4_LA = """Gallina vero similiter varias format voces: aliter enim
vociferatur dum pullos convocat, aliter dum parturit, aliter dum cholera
ardet. Dum ova parturit, ex unisono per sextam saltum facit, uti in
Iconismo III nota B exprimunt; vocem vero convocantis pullos suos in dicto
Iconismo notae C indicant. Coturnix semper et identidem sequentem repetit
cantus loco pigolismum, ut nota D in Iconismo III exponunt. Coccyx sive
Cuculus, nomen a voce sortitus, bisyllabam vocem semper teretizat, non in
unisono, sed perfectissimae tertiae minoris intervallo, ut apparet in notis
E Iconismi III."""
BIRD4_EN = """The hen likewise forms various voices: she cries one way when
she calls her chicks together, another when she is laying, another when her
choler burns. When she lays her eggs she makes a leap from the unison
through a sixth, as the notes at B in Iconismus III express; and the voice
with which she calls her chicks the notes at C indicate. The quail, always
and again, repeats in place of a song the following 'pigolism', as note D
in Iconismus III sets out. The cuckoo — Coccyx, named from his voice —
forever rolls his two-syllable call, not in unison, but at the interval of
a most perfect minor third, as appears at the notes E of Iconismus III."""

BIRD5_LA = """Non secus omnium volucrium cantus exprimi possent, si cui
otium foret singularum in formandis vocibus processum observare: nam in
singulis certum quendam motum, vocis prorsus a reliquis distinctum,
reperiet. Ita Hirundines fritinniunt, pupizant Upupae, kichlizant Turdi,
Perdices titibizant, struthizat Passer, Pica kittabizat, gratitat anser,
pisitat sturnus. Merula omnium optime differentias harmonicas exprimit: ita
ut quod Psittacus, Pica, Corvus, Monedula in voce humana exprimenda, quod
Luscinia et reliquae voces phonascae in exprimendis glottismis possunt, hoc
inter ceteras omnes aves Merula canendo potest, praesertim si a dextro
Magistro praecentore instituatur."""
BIRD5_EN = """In the same way the songs of all birds could be expressed, if
anyone had leisure to observe the procedure of each in forming its voice:
for in each he will find a certain motion of voice utterly distinct from
the rest. So the swallows twitter, the hoopoes 'pupize', the thrushes
'kichlize', the partridges 'titibize', the sparrow 'struthizes', the magpie
'kittabizes', the goose gaggles, the starling 'pisitates'. The blackbird
best of all expresses the harmonic differences: so that what the parrot,
magpie, raven and jackdaw can do in rendering the human voice, and the
nightingale and the other singing voices in rendering glottisms, this
among all other birds the blackbird can do by song — above all if she be
trained by a skilful master-precentor."""

PATH1_LA = """Si itaque harmoniae accedat numerus determinatus et
proportionatus, iam veluti duplicatas vires acquirit, movetque animum non
ad intrinsecos tantum affectus, sed et ad extrinsecos quosdam et exoticos
corporis motus, ut in choreis patet, in quibus numerosus harmoniae
hyperorchematicae sonus saltatores ad saltus pari ratione numerosos et
harmoniae dictae clausulis proportionatos nescio qua abdita vi sollicitat
et instimulat; patet et in tarantismo affectis, ut paulo post dicetur."""
PATH1_EN = """If therefore to harmony there be added a determinate and
proportioned number, it acquires as it were doubled powers, and moves the
soul not only to inward affects but also to certain outward and exotic
motions of the body — as is plain in dances, where the numerous sound of
the hyperorchematic harmony, by I know not what hidden force, solicits and
spurs the dancers to leaps equally numerous and proportioned to the
harmony's clausulae; and it is plain too in those seized by tarantism, as
will be said a little below."""

PATH2_LA = """Harmonico vero numero et proportioni si accedat verborum in
ipsa oratione abscondita vis et energia, praesertim si pathetica fuerit
insignemque historiam aut tragicum casum continuerit, dici vix potest
quantum haec tria in unum coniuncta possint ad animos dispositos in
quoscunque affectus incitandos. Dixi animos dispositos: quia nisi quarta
conditio, hoc est audientis dispositio, praecesserit, citius saxum quam
hominem indispositum incapacemque moveris."""
PATH2_EN = """But if to harmonic number and proportion there be added the
hidden force and energy of the words in the oration itself — above all if
it be pathetic, and contain some signal history or tragic case — it can
scarcely be said how much these three, joined into one, can do to incite
disposed souls to any affects whatsoever. I said disposed souls: for
unless the fourth condition, that is the disposition of the hearer, has
gone before, you will sooner move a rock than an indisposed and incapable
man."""

PATH3_LA = """Quicunque igitur martialem virum bella spirantem commovere
volet, ita harmoniam numerosque, ita orationem dispositam habere necesse
est, ut et harmonia ipsa numerusque nescio quid tumultuarium habeat, et
oratio ipsa magnifica alicuius Herois gesta contineat; et his ita
comparatis, necessarium in auditore bellici furoris effectum producet. Hoc
pacto Timotheus Alexandrum in furorem et ad arma capienda incitasse
verisimile est; cum enim Rex martio spiritu turgeret gloriamque prae
omnibus mortalibus ambiret, iuxta celeberrimos Itali poetae versus —
'Giunto Alessandro alla famosa tomba / del fero Achille, sospirando disse:
/ O fortunato, che sì chiara tromba / avesti, e chi di te sì alto
scrisse!' — Timotheus vero, naturam Regis optime perspectam habens,
harmonicos modulos adeo apte ad orationis de bellica gloria institutae vim
et energiam adaptare potuit, ut desideratum effectum obtineret."""
PATH3_EN = """Whoever therefore would stir a martial man breathing war must
have his harmony and his numbers, and his oration, so disposed that the
harmony and the number themselves have I know not what of tumult in them,
and the oration itself, magnificent, contain the deeds of some Hero; and
with these so prepared, he will of necessity produce in the hearer the
effect of warlike fury. In this way it is likely that Timotheus incited
Alexander to fury and to seize his arms; for since the King swelled with a
martial spirit and sought glory before all mortals — after the most
celebrated verses of the Italian poet: 'When Alexander came to the famous
tomb of fierce Achilles, sighing he said: O fortunate man, who had so
clear a trumpet, and one to write of you so high!' — Timotheus, who had
the King's nature perfectly in view, was able to fit his harmonic measures
so aptly to the force and energy of an oration framed on warlike glory,
that he obtained the desired effect."""

PATH4_LA = """Musica igitur ut moveat, non qualecunque subiectum vult, sed
illud cuius humor naturalis musicae congruit: videmus enim quod doria,
verbi gratia, harmonia non omnes, sed illos quibus ipsa congruit, moveat;
cuius rei causa est complexionum diversitas, quae maxime in hoc negotio
attendenda est. Hinc melancholici, humore lento gravati, acutis spissisque
clausulis abhorrent; cholerici vero, spiritu agili et mobili gaudentes,
acutis spissisque modulis impense delectantur. Hinc igitur, si veterum
musicorum miracula renovare velint, respicere debent musici nostri, ut
primo alicuius subiecti inclinationem et naturalem habitudinem explorent,
deinde iuxta eandem numeros harmonicos verborumque themata instituant."""
PATH4_EN = """Music, therefore, that it may move, does not want just any
subject, but that one whose natural humour agrees with the music: for we
see that the Dorian harmony, for example, moves not all men, but those
with whom it agrees; and the cause of this is the diversity of
complexions, which in this business is above all to be attended to. Hence
the melancholic, weighed down by a slow humour, shrink from sharp and
crowded clausulae; while the choleric, rejoicing in an agile and mobile
spirit, take intense delight in sharp and crowded measures. Hence, if our
musicians would renew the miracles of the ancient musicians, they must see
to it first to explore the inclination and natural disposition of some
subject, and then, according to the same, to institute their harmonic
numbers and the themes of their words."""

DATA = {
    "id": "musurgia",
    "autor": "Athanasius Kircher",
    "titel": "Musurgia universalis — the Society's book of music (Rome 1650)",
    "jahr": 1650,
    "lang": "la",
    "zitierweise": "Musurg. syn./I/VII [k]",
    "quelle": ("Latin: Musurgia universalis, sive Ars magna consoni et dissoni, Tomus I "
               "(Rome: Corbelletti, 1650); Internet Archive chepfl-lipr-AXC19_01 (Fribourg "
               "scan), collated where doubtful with bub_gb_97xCAAAAcAAJ; both public "
               "domain. OCR transcribed and emended against the sense and the page "
               "images. English: this site's unofficial working translation."),
    "hinweis": ("The second program's music module, cut deliberately narrow from a work "
                "of over a thousand folio pages: the Synopsis of the ten books (the whole "
                "architecture of universal music, from the physiology of sound to God's "
                "concert with nature); the voices of the birds from Book I, with "
                "Iconismus III carried as an image — the nightingale as the Idea of all "
                "music, transcribed into notation and then dissected; and the doctrine of "
                "the affects from Book VII — the four conditions for moving the soul, "
                "Timotheus before Alexander with Petrarch's quatrain on Achilles, and the "
                "temperaments. Kircher wrote at the Collegio Romano; Muratori's chapter on "
                "the music of the Reductions (Mur. IX) shows the same Society's music at "
                "the other end of the world. The paragraph numbering is this site's own; "
                "pages follow the running heads of the 1650 print. Part of the concordance "
                "and the citation-bound dialogue; not part of the linguistic statistics, "
                "which describe the core corpus only."),
    "sections": [
        {"id": "synopsis", "zk": "Musurg. syn.",
         "titel": "The Synopsis of the ten books",
         "blurb": ("Kircher's whole design on one page of the front matter: ten books "
                   "from the physiology of natural sound to the decachordon naturae — "
                   "the ten Registers by which the world itself is composed, ending in "
                   "the music of the Archetype, God's concert with universal nature."),
         "units": [
             u(1, 1, SYN1_LA, SYN1_EN, label="Books I–VII"),
             u(2, 2, SYN2_LA, SYN2_EN, label="Books VIII–X"),
             u(3, 3, SYN3_LA, SYN3_EN, label="The ten Registers of the decachordon naturae",
               note="The closing verse is Psalm 143(144):9 — 'upon a psaltery of ten strings will I sing praises unto thee' — the whole work folded into one psalm line."),
         ]},
        {"id": "birds", "zk": "Musurg. I",
         "titel": "The voices of the birds",
         "blurb": ("Lib. I, pp. 28–32: the nightingale as nature's Idea of all music — "
                   "her heroic, Sapphic and Adonic verses, her pupils and their corrected "
                   "lessons, her death with the breath failing before the song — and then "
                   "the cock, the hen, the quail and the cuckoo, set down in musical "
                   "notation on Iconismus III."),
         "units": [
             u(4, 1, BIRD1_LA, BIRD1_EN, label="p. 28–29 · the Idea of all music"),
             u(5, 2, BIRD2_LA, BIRD2_EN, label="p. 29 · the Epitome — transcribed, then dissected",
               note="Kircher did both: the clausulae went onto the musical scale (Iconismus III), and the bird under the knife — the anatomy of the syrinx follows in the print."),
             u(6, 3, None,
               ("The promise kept: 'Glottismi modulationum sibilo exprimendi in Luscinia "
                "obseruati' — the nightingale's glottisms observed and set on the musical "
                "scale, pigolismus, glazismus, teretismus, and one passage Kircher can "
                "only call 'chromatico-enharmonicum nescio quid affectans'. Below, "
                "'Diuersarum uolucrium voces notis musicis expressae': the cock's "
                "gallicinium (A), the laying hen with her leap of a sixth and the hen "
                "calling her chicks 'glo glo glo' (B, C), the quail's 'bikebik' (D), the "
                "cuckoo's minor third 'gucu gucu' (E) — and, on the branch, the parrot "
                "with his Greek greeting, χαῖρε."),
               label="Iconismus III, fol. 30 — the notation plate",
               img="assets/musurgia/iconismus3.jpg",
               alt="Iconismus III of the Musurgia universalis (1650): the nightingale's glottisms — pigolismus, glazismus, teretismus, and a 'chromatico-enharmonicum nescio quid' — in musical notation, and below, the voices of divers birds expressed in notes: cock, laying hen, hen calling her chicks, cuckoo, quail, and a parrot greeting in Greek."),
             u(7, 4, BIRD3_LA, BIRD3_EN, label="p. 31 · the cock"),
             u(8, 5, BIRD4_LA, BIRD4_EN, label="p. 31–32 · hen, quail, cuckoo",
               note="The cuckoo's minor third — 'perfectissimae tertiae minoris intervallo' — is the plate's note E."),
             u(9, 6, BIRD5_LA, BIRD5_EN, label="p. 32 · the onomatopoeias, and the blackbird"),
         ]},
        {"id": "pathetica", "zk": "Musurg. VII",
         "titel": "The pathetic music — how the affects are moved",
         "blurb": ("Lib. VII, pp. 550–551: harmony alone is not enough. Number doubles "
                   "its force, the words' hidden energy triples it — and without the "
                   "fourth condition, the hearer's disposition, 'you will sooner move a "
                   "rock than an indisposed man.' Timotheus and Alexander prove the rule; "
                   "the temperaments explain it; and Kircher closes with the program of "
                   "renewing the miracles of ancient music."),
         "units": [
             u(10, 1, PATH1_LA, PATH1_EN, label="p. 550 · harmony and number",
               note="The tarantism promised 'a little below' follows in the print: Kircher's famous discussion of the tarantella as musical medicine."),
             u(11, 2, PATH2_LA, PATH2_EN, label="p. 550 · the words, and the fourth condition"),
             u(12, 3, PATH3_LA, PATH3_EN, label="p. 550–551 · Timotheus before Alexander",
               note="The Italian quatrain is Petrarch (Canzoniere 187): Alexander at the tomb of Achilles, envying him his Homer."),
             u(13, 4, PATH4_LA, PATH4_EN, label="p. 551 · the temperaments, and the program"),
         ]},
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
n = sum(len(s["units"]) for s in DATA["sections"])
print(f"wrote {os.path.normpath(OUT)}: {len(DATA['sections'])} sections, {n} units")
