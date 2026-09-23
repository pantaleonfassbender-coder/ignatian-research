# -*- coding: utf-8 -*-
"""Build data/cenodoxus.json — Bidermann's Cenodoxus, from the Ludi
theatrales of 1666: the Jesuit stage.

The source hunt the registry demanded has succeeded. Source: Jacob
Bidermann, Ludi theatrales sacri sive opera comica posthuma, Pars prima
(Munich: Johann Wagner, printed by Johann Wilhelm Schell, 1666) — the
posthumous collected printing of the plays; Cenodoxus stands second in
the volume (printed pp. 78–160), after the title's own order Belisarius,
Cenodoxus, Cosmarchia, Josephus, Macarius Romanus. Digitisation: the
Regensburg copy (Staatliche Bibliothek, 999/Lat.rec.224) at the MDZ,
Münchener DigitalisierungsZentrum, bsb11103594, with page-level OCR; the
modern editions of 1963/65 remain in copyright and were not consulted,
exactly as the registry's condition required. The play itself was written
for the Augsburg stage in 1602 and famously performed at Munich in 1609;
the 1666 printing is its editio collecta and the text carried here.

Text craft: the passages were located through the MDZ's hOCR and emended
against the sense; the crux pages (the DAMNATUS page, printed p. 153, and
the closing page, printed p. 158) were verified by eye against the page
images — which settled one reading the OCR had garbled: the print really
has 'piceata flammarum volumina', the pitch-black rolling flames, not a
corruption. Long s and ligatures resolved, u/v and i/j classicised, æ
written out, the print's speaker sigla kept (CEN., BRUN., OMN., …), the
printed page numbers carried on the labels. English: this site's
unofficial working translation, dedicated CC0.

The cut, deliberately narrow: Bidermann's own preface (the Paris doctor
legend, Bruno, and the honest 'fabula est'); the devil's harvest
monologue from Act I with Philautia and Hypocrisis as the two engines;
the three cries of the corpse from Act V — ACCUSATUS SUM, IUDICATUS SUM
(with Bruno's 'we live, and live not'), the Judge's sentence, IUSTO DEI
IUDICIO DAMNATUS SUM — with Bruno's 'hic ure, hic seca' prayer; and
Bruno's resolve — 'vivere prohibet; terret mori', the cause said more
clearly by being kept silent, 'Non creditur, non creditur, non
creditur', and 'Perdere haec malo, quam perire': the founding of the
Carthusians as the play's exit from the stage."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "cenodoxus.json")

def u(n, k, orig, en, label=None, note=None):
    d = {"n": n, "k": k}
    if orig: d["orig"] = " ".join(orig.split())
    if en: d["en"] = " ".join(en.split())
    if label: d["label"] = label
    if note: d["note"] = note
    return d

LECT_LA = """Parisiaci Doctoris passim meminere multi: nomen haud ullis
temere traditum. Iureconsultum alicubi legis; et magna eruditionis, nec
nulla virtutis fama clarum: ut naturae concesserit, in feretro
resedisse; indidem se reum, altero post die, iudicatum; denique
perennibus flammis addictum, proclamasse: eundemque Brunoni,
Carthusiensium auctori, primum auctorem fuisse, ut cum paucis aliis et
locum et vitam in melius mutaret. Haec historia. Caeterum, quod illi
Cenodoxo nomen facimus, eiusque superbiam vitiaque superbiae cognata
notamus, fabula est. Quo enim crimine sit accusatus, nobis in incerto
habetur: quod inter flagitia propius fieri et honestius repraesentari
potuit, posuimus; hominem nulla insuper traductum calumnia cupimus. Nam
si talis illi vita fuit, convitium haud fecimus: si non fuit, alius
vitam, huius mortem memoramus."""
LECT_EN = """Of the Doctor of Paris many have made mention everywhere:
a name not rashly handed down by anyone. In one place you read that he
was a jurisconsult, famous for great learning and for no small repute of
virtue; that when he had yielded to nature, he sat up on the bier; that
from the same place, on the next day, he proclaimed himself judged; and
finally, sentenced to everlasting flames — and that this man was for
Bruno, the founder of the Carthusians, the first author of his changing,
with a few others, both his place and his life for the better. So much
is history. For the rest — that we give him the name Cenodoxus, and mark
his pride and the vices akin to pride — is fable. For with what crime he
was accused is held uncertain by us: we have set down what, among
disgraces, could most nearly have happened and be most decently
represented; and we desire, moreover, that the man be traduced by no
calumny. For if his life was such, we have made no insult; if it was
not, we commemorate another's life, and this man's death."""

PHIL_LA = """Nec ulla satias implet illam belluae voraginem. Sitit
bibendo, et esurit vorando. Quicquid ingero, diram famem accendit. Omnes
undique socii mei quaerunt, ferunt, trahuntque rapiuntque omnia;
tantusque continenter ingruit hominum ruentium imber, ut obstupescam
quempiam terris superstitem inveniri. Sicubi emergo rursus has in auras,
illico superesse tantum segetis admiror Stygi, ac si fuisset nulla
messis hactenus. Paene nihil opus est viribus meis: sua plerique sponte
pessum eunt. Hinc pauculi caeco resistunt Marte; quos Philautia
Hypocrisisque facile transversos agunt. Sed fallor, an recentia superi
alitis adverto vestigia? profecto iam adfuit hostis meus; domum hanc
nove communiit: neque enim aditus ita huc liber est, ut anteidhac fuit.
Repellor viribus tacitis ego. Heu me! male olim hoc metui, ut ille ne
meam praedam mihi ereptum iret."""
PHIL_EN = """Nor does any satiety fill that maw of the beast. It
thirsts by drinking, and hungers by devouring. Whatever I pour in only
kindles the dire famine. All my companions everywhere seek, carry, drag
and snatch everything; and so great a rain of men rushing down pours in
without cease that I am astonished anyone is found left alive on earth.
Whenever I come up again into these airs, I marvel at once that so much
of the harvest is still left for Styx, as if there had been no reaping
hitherto. There is almost no need of my powers: most men go to ruin of
their own accord. Hence only a very few resist in the blind battle — and
these Philautia and Hypocrisis easily lead astray. But am I deceived, or
do I notice the fresh footprints of the winged one from above? Truly my
enemy has just been here; he has newly fortified this house: for the
entrance here is not so free as it was before. I am driven back by
silent powers. Woe is me! this is what I long feared, that he would go
and snatch my prey from me."""

FUN1_LA = """CHOR. Eheu, Curia iam cares magistro; eheu, Patria iam
cares patrono; eheu, Gallia iam cares parente; eheu, Terra cares, cares
salute! CEN. Heu, heu! OMN. DEUS serva. Quid est miraculi? CEN. Heu,
heu: verendi apud tribunal Iudicis ACCUSATUS SUM. OMN. Serva DEUS:
parce, superae Rector domus. BRUN. Quid audio? HUG. Quid sentio? LAUD.
Quid contuor? BRUN. Quid haec sibi novitas? quis occupat tremor
frigusque membra? HUG. Nihil animae inest corpori. LAUD. Paenissime
perii: pedibus aegre meis insisto. BRUN. Pavet animus; inhorrescunt mei
artus: titubat horrore lingua noxio. Audistis eiulantem, et horribili
sono exclamitantem? OMN. Audivimus. Nil tetrius, nil horribilius
anteidhac. BRUN. Ut extulit pallentia ora morte! ut aegra lumina
divaricavit! ut asperis e faucibus extorsit illa verba! HUG. Quid
portenditis novitate, Superi, tam nova? LAUD. Ergone facili adeo
vicissitudine bona adversaque fortuna mortales subit? Beatior heri
nemo, quam Cenodoxus; infelicior hodie videtur nemo. HUG. An accusatus
est Cenodoxus? OMN. Omnes periimus, quando pereunt tales. BRUN.
Periisse non putandus ideo erit Cenodoxus: absit, de viro integerrimo
hoc suspicari. Nam improba Cacodaemonis ferenda fortasse fuit
accusatio; ut omnia solet carpere, et mendaciis afflare. Nam accusare
quosvis, liberum est."""
FUN1_EN = """CHORUS. Alas, the court now lacks its master; alas, the
fatherland now lacks its patron; alas, France now lacks its parent;
alas, Earth, you lack, you lack your health! CENODOXUS [from the bier].
Woe, woe! ALL. God preserve us. What marvel is this? CENODOXUS. Woe,
woe: before the tribunal of the dread Judge I AM ACCUSED. ALL. Preserve
us, God: spare us, Ruler of the house above. BRUNO. What do I hear?
HUGO. What do I feel? LAUDWIN. What do I behold? BRUNO. What does this
strange thing mean? what trembling and cold seizes my limbs? HUGO.
There is no soul left in my body. LAUDWIN. I am all but dead: I hardly
stand on my feet. BRUNO. My mind quakes; my joints shudder; my tongue
stumbles with noxious horror. Did you hear him wailing, and crying out
with horrible sound? ALL. We heard. Nothing more hideous, nothing more
horrible ever before. BRUNO. How he lifted up a face pale with death!
how he wrenched apart his sick eyes! how he wrung those words from his
harsh throat! HUGO. What do you portend, powers above, by a strangeness
so strange? LAUDWIN. Does fortune, good and adverse, then overtake
mortals by so easy a turn? Yesterday no one more blessed than
Cenodoxus; today no one seems more unhappy. HUGO. Is Cenodoxus
accused? ALL. We are all lost, when such men are lost. BRUNO. Cenodoxus
is not therefore to be thought lost: far be it from us to suspect this
of a man of utter integrity. For perhaps the wicked accusation of the
Evil Spirit had to be borne — as he is wont to carp at everything and
breathe lies upon it. For to accuse whomever one pleases is free to
him."""

FUN2_LA = """HUG. Iudicatus ergo a Numine Cenodoxus? ipseque praeco
iudicii sui? O tristem visu, o lugubrem catastrophen! LAUD. DEUS! quid
haec sibi volunt teterrima spectacula, an miracula? Mihine mortui vox
vera sonuit? tamque dira nuntiat mortalibus de rebus immortalibus?
BRUN. Horresco pristini memor adhuc funeris, et iam novo auget horror
antiquus metu. Audire non tam mortuum, quam mortuus loqui ipse videor.
HUG. Supplicemus Numini hac nocte; et iram molliamus Iudicis, siqua
impiatus fortean migraverit Cenodoxus orbe. BRUN. Differamus interim
tumulare corpus. LAUD. Atqui iudicatus est; quid proderis? BRUN. Nec
vero constat undique quae iudicii fuerit peracta formula. Innoxios
quoque iudicare dicimur, cum absolvimus. Cenodoxus ergo absolvitur
fortasse iudicatus; aut incendio piaculari urgetur. OMN. Ergo haec
alterum res differatur in diem. BRUN. Quae tempora incidimus? eheu,
vivimus, nec vivimus: morique cogimur, neque sinimur mori."""
FUN2_EN = """HUGO. Cenodoxus judged, then, by the Godhead? and himself
the herald of his own judgment? O sad to see, o mournful catastrophe!
LAUDWIN. God! what do these most hideous spectacles — or miracles —
mean? Did the voice of a dead man truly sound for me? and does it
announce to mortals things so dire concerning things immortal? BRUNO. I
shudder, still remembering the first funeral, and now the old horror
grows with new fear. I seem not so much to hear a dead man as to be a
dead man speaking myself. HUGO. Let us supplicate the Godhead this
night, and soften the Judge's wrath, if perchance Cenodoxus has
departed the world unatoned. BRUNO. Let us meanwhile defer burying the
body. LAUDWIN. And yet he is judged; what good will you do? BRUNO. Nor
indeed is it established from any side what formula of judgment was
carried out. We are said to judge the innocent too, when we acquit.
Perhaps then Cenodoxus, being judged, is acquitted; or he is pressed by
the purging fire. ALL. Then let the matter be deferred to another day.
BRUNO. What times have we fallen upon? Alas, we live, and live not; we
are compelled to die, and are not permitted to die."""

FUN3_LA = """[CHRISTUS IUDEX.] Te meis laboribus itineribusque perditum
quaesiveram; et cum sim ubique, nuspiam te repereram. Iniurias et
contumelias tui amore sustinui; esseque odio plurimis non horrui, dum
te quasi unicum unice amare possem. Verbera, flagra corpore innoxio pro
noxio te pertuli. Crucem necemque subii, ut exires tuam. Has testor
ipse manus, pedesque vulnere consauciatos: haec tropaea, hosce clavos,
quae cuncta contueris hic praesentia. Loquatur universa terrae machina;
loquatur universa caeli curia: maiora me nequiisse ponere merita, nec
debuisse; dummodo ego temet mihi tibique memet dedicatum obstringerem.
Sed esse tanto alienior, quo charior occoeperas; meritaque delictis mea
pariare vel superare quam creberrimis frustra volebas. Arrogantia meam
submissionem vincere; et modestiam superbia; candorem hypocrisi; bona
malis. Ego superbiam olim non tuli caelituum inultam; tune tuam ferri
putes? I, digna lue supplicia; patere perpetes per omnis aevitatis
omnes terminos flammas paratas daemoni malo; quibus lamenta dentiumque
stridor perpetim exaudientur: inde nulla aeternitas eripiet. SPIR. Heu,
heu, heu! cadite montes super me, obruiteque una. OMNES IUDICES. Iusta
iudicia DEI. Pereat scelestus."""
FUN3_EN = """[CHRIST THE JUDGE.] With my labours and my journeys I had
sought you when you were lost; and though I am everywhere, nowhere had
I found you. Injuries and insults I endured for love of you; and I did
not shrink from being hateful to very many, so long as I might love you
uniquely, as though you were the only one. Blows and scourges I bore
for you, on a guiltless body for a guilty one. I underwent the cross
and death, that you might escape yours. I call to witness these very
hands, and these feet wounded through: these trophies, these nails —
all of which you behold present here. Let the whole fabric of the earth
speak; let the whole court of heaven speak: greater merits I could not
have laid down, nor owed — provided only that I might bind you
dedicated to me, and myself to you. But you began to be the more
estranged, the dearer you had become; and you strove in vain to balance
or outdo my merits with offences as frequent as could be: to conquer my
submission with arrogance, my modesty with pride, my candour with
hypocrisy, good things with evil. I once did not leave the pride of the
heaven-dwellers unavenged — do you think yours will be borne? Go, pay
the punishments you have deserved; suffer, through all the bounds of
all eternity, the perpetual flames prepared for the evil demon, in
which laments and the gnashing of teeth will be heard for ever: from
there no eternity will rescue you. THE SPIRIT. Woe, woe, woe! Fall,
mountains, upon me, and bury me together. ALL THE JUDGES. Just are the
judgments of GOD. Let the wicked man perish."""

FUN4_LA = """BRUN. Cum horrore redeo ad funus hoc, unde toties cum
horrore abivi. LAUD. Utinam haec secundos exitus prodigia sortiantur.
HUG. Utinam. Sed modo ad funus instaurandum adeste; et ultimum
Cenodoxo honorem habete; si tamen licet. CEN. Heu me, heu miserrimum
omnium; heu, heu, heu! OMN. DEUS! O Christe! CEN. Mittite, mittite
istas, mittite nil profuturas postmodum exequias. Mihi nequitis ultra
adminiculari. Perierit, utinam perierit mater illa, quae edidit
infausta me; o miserum! o miserrimumque me mortalium: IUSTO DEI
IUDICIO DAMNATUS SUM. Perennes eheu iam rogos passurus abeo. OMN.
Parce, parce, Numinis severa dextra. LAUD. Periimus, ni iudicas
punisque mitius scelera mortalium. BRUN. Ah, quid animi est perituro?
HUG. Quid putem quondam futurum me misello? LAUD. Deficit animus
timore. BRUN. Vivere aeque displicet morique. OMN. Quo fugimus? quid
agimus?"""
FUN4_EN = """BRUNO. With horror I return to this funeral, from which so
often I have gone away with horror. LAUDWIN. May these prodigies be
allotted a favourable issue. HUGO. May they. But now come to renew the
funeral, and pay Cenodoxus the last honour — if indeed it is
permitted. CENODOXUS [from the bier]. Woe is me, woe, most wretched of
all; woe, woe, woe! ALL. God! O Christ! CENODOXUS. Dismiss, dismiss
these, dismiss these obsequies that hereafter will profit nothing. You
can help me no further. Would that she had perished, would she had
perished, that mother who bore me to misfortune; o wretched, o most
wretched of mortals that I am: BY THE JUST JUDGMENT OF GOD I AM DAMNED.
Alas, I go now to suffer everlasting fires. ALL. Spare us, spare us,
severe right hand of the Godhead. LAUDWIN. We are lost, unless you
judge and punish the crimes of mortals more mildly. BRUNO. Ah, what
heart can he have who is about to perish? HUGO. What must I think will
one day become of wretched me? LAUDWIN. My mind fails with fear. BRUNO.
Living displeases me, and dying, equally. ALL. Whither do we fly? what
are we to do?"""

FUN5_LA = """BRUN. Hic, Numen, ure, caede, plecte, seca, feri, saevi;
nihil relinquito hic cruciatuum, ut alibi parcas. LAUD. O DEI recondita
sensa! Quis enim pronuper usquam sanctior Cenodoxo erat habitus? quis
innocentior? Sed illa sanctitas et innocentia apud severi Iudicis
subsellia nec sanctitas fuit, nec innocentia. BRUN. Relinquo dirum
funus; et qui nescio succurrere alteri, mihi ipsi consulam."""
FUN5_EN = """BRUNO. Here, o Godhead, burn, strike, smite, cut, wound,
rage; leave out no torment here, that you may spare elsewhere. LAUDWIN.
O hidden counsels of God! For who, till just now, was anywhere held
holier than Cenodoxus? who more innocent? But that holiness and that
innocence, before the benches of the severe Judge, were neither
holiness nor innocence. BRUNO. I leave this dreadful funeral; and I,
who know not how to succour another, will take counsel for myself."""

BRU1_LA = """BRUN. Nihil est necesse, credo, multis dicere, cur vos
potissimum evocarim. Nam docet loquiturque causam, me tacente, mortui
vox viva: quae me vosque noctes ac dies terrefacit; inque gaudiis
gaudia negat: suamque metuit vita vitam; animum animus: suspecta sunt,
quaecunque sunt. Molestiam creant amoena; et inopiam faciunt opes.
Tormenta deliciae novant; premitque spem timor perennis. Esitare,
litteris vacare, disputare, legere, colloqui Cenodoxus arcet:
dormientem me excitat; vigilem exanimat: adest mihi, quoties abest.
Quid multa? vivere prohibet; terret mori. STEPH. Obsedit idem luctus
et animum meum, Bruno; sed anceps consilii, quid ordiar ignoro. ANDR.
Suade, Bruno, siquid suppetit. BRUN. Pacare meque vosque statui.
Vivere in his periculis, ubi alios viderim periisse, taedet. OMN.
Omnibus inest taedium hoc idem: deest medela."""
BRU1_EN = """BRUNO. There is no need, I think, to say much about why I
have called you above all others. For, though I am silent, the living
voice of the dead man teaches and speaks the cause: the voice that
terrifies me and you by night and by day, and in the midst of joys
denies joy; life fears its own life, mind its own mind: whatever
things are, are suspect. Pleasant things create distress; riches make
poverty. Delights renew torments; and a perennial fear presses down
hope. Eating, giving time to letters, disputing, reading, conversing —
Cenodoxus bars them all: he wakes me when I sleep; when I wake, he
takes the life out of me: he is with me as often as he is absent. In
short: he forbids living, and makes dying a terror. STEPHEN. The same
grief has besieged my mind too, Bruno; but uncertain in counsel, I know
not where to begin. ANDREW. Advise us, Bruno, if anything is at hand.
BRUNO. I have resolved to bring peace to myself and to you. To live
amid these dangers, where I have seen others perish, wearies me. ALL.
The same weariness is in us all; the remedy is lacking."""

BRU2_LA = """BRUN. Socii, novimus qua sanctitate, quaque virtute fuerit
vitam agere visus ille, quem modo vidimus supplicia luere apud Stygem
extremissima. OMN. Hoc ipse nobis dixit audientibus. ANDR. Quam causam
oportet huius esse? BRUN. Utinam, utinam disertius causam addidisset!
ilicet fugeremus illam; et quicquid illum perdidit, nos perderemus. Sed
profecto clarius causam tacendo dixit; et salubrius ita supprimendo
expressit. Odium diceret causam fuisse? nos etiam odium statim
excluderemus; alia crimina in sinu aleremus. Arrogantia se diceret
praecipitem iisse? fugeret arrogantiam noster animus; sed ceteris
periculum inesse vitiis crederet nullum. Bene itaque tacuerat singula,
ut nos omnia metuere disceremus. STEPH. Hoc recte quidem. Sed quid
cavere tu potissimum iubes nos, Bruno? BRUN. Quid? Cenodoxus omnia
monuit cavenda, dum cavere similem iusserat obitum. Timenda vita nobis
talis est; talem necem timere serum est. Vivere ita nolit ille,
quisquis ita nolit mori."""
BRU2_EN = """BRUNO. Companions, we know with what holiness and what
virtue that man seemed to lead his life whom we have just seen paying
the utmost penalties by the Styx. ALL. He told us so himself, in our
hearing. ANDREW. What must the cause of this be? BRUNO. Would, would
that he had added the cause more explicitly! We should flee it at
once, and whatever destroyed him, we should destroy. But in truth he
told the cause more clearly by keeping silent, and expressed it more
wholesomely by suppressing it. Had he said hatred was the cause? we
should at once shut out hatred too — and nurse the other crimes in our
bosom. Had he said he went headlong through arrogance? our mind would
flee arrogance, but would believe no danger lay in the other vices. So
he had done well to be silent about the particulars, that we might
learn to fear everything. STEPHEN. Rightly so. But what above all do
you bid us guard against, Bruno? BRUNO. What? Cenodoxus warned that
everything is to be guarded against, when he ordered us to guard
against a death like his. It is such a life that we must fear; to fear
such a death is too late. Let him refuse so to live, whoever refuses so
to die."""

BRU3_LA = """BRUN. Ah, quid putemus esse, perpeti inferas perenne
flammas? longa mortis taedia? vermesque viperasque conscientiae? et
alia mille? Malo conticescere, quam pauca dicere. Quicquid enim dixero,
parum erit, nihil erit. Imo quicquid dixero dicam; idque milliesque
dicam millies, interrogatus de inferorum miseria: Non creditur, non
creditur, non creditur. Testare, miser; hic, hic renuncia: ex tuis
honoribus capis levamen in tuis cruciatibus? num laude capta submoves
piceata flammarum volumina, qualibus nunc usque et usque et usque et
usque et usque nunc affligeris? Iam iam, miser, iam desinunt placere
tibi, quae hodieque vani quaerimus stultique mortales. Modo omnes
gloriam sectamur; olim ut noxiam exsecrabimur. Ah sero, sero. Nolo
paenitudinem hanc seram opperiri: est animus antevertere, socii mei,
iam non mei. OMN. Sumus, erimus tui. HUG. Itane, Bruno? tu tibi legas
sidera, nobis relinquas Tartara? sequar ego, sequar. BRUN. Abi,
voluptas; hinc abite, gloriae cupidines; iam delicatae corporis valete
vestes: annuli, imo compedes, non annuli. Valete, honores; talibus
remunerari si soletis praemiis vestros clientes, non meam ridebitis
dementiam; ridebo vestram. HUG. Cedite, opes; abite, gloriae; ite,
litterae; valete, saecli incommoda. BRUN. Imo vos mei salvete, iam
valete, socii. Perdere haec malo, quam perire. OMN. Non recedimus.
STEPH. Quocunque ducito, modo procul duxeris Cenodoxo, et hinc, ubi
periit. OMN. Valete, vos inanitates. ANDR. Sequor. Abite saeculi
retinacula. OMN. Sequimur, sequimur omnes."""
BRU3_EN = """BRUNO. Ah, what are we to think it is, to endure the
nether flames everlastingly? the long wearinesses of death? the worms
and vipers of conscience? and a thousand things besides? I would
rather fall silent than say little. For whatever I shall say will be
too little, will be nothing. Nay, whatever I say I will say, and say
it a thousand times a thousand, when questioned about the misery of
the damned: It is not believed, it is not believed, it is not
believed. Bear witness, wretched one; here, here declare it: do you
draw from your honours any relief in your torments? do you, with the
praise you caught, put away the pitch-black rolling flames with which
now and ever and ever and ever and ever now you are afflicted? Now at
last, wretch, now the things cease to please you which we vain and
foolish mortals still seek today. Now we all chase glory; one day we
shall curse it as our ruin. Ah, too late, too late. I will not wait
for this late repentance: my mind is to forestall it, my companions —
mine now no longer. ALL. We are and will be yours. HUGO. Is it so,
Bruno? you would choose the stars for yourself, and leave Tartarus to
us? I will follow, I will follow. BRUNO. Away, pleasure; away from
here, lusts of glory; and now farewell, dainty garments of the body:
rings — fetters rather, not rings. Farewell, honours; if you are wont
to reward your clients with such wages, you will not laugh at my
madness; I shall laugh at yours. HUGO. Give way, riches; away,
glories; go, letters; farewell, inconveniences of the age. BRUNO. Nay,
as mine — greetings to you, and now farewell, companions. I would
rather lose these things than be lost. ALL. We do not draw back.
STEPHEN. Lead wherever you will, so long as you lead far from
Cenodoxus, and from here, where he perished. ALL. Farewell, you
vanities. ANDREW. I follow. Away, tethers of the age. ALL. We follow,
we follow all."""

DATA = {
    "id": "cenodoxus",
    "autor": "Jacob Bidermann",
    "titel": "Cenodoxus — the Jesuit stage (1602; printed 1666)",
    "jahr": 1602,
    "lang": "la",
    "zitierweise": "Cen. Lect./I/V/Brun. [k]",
    "quelle": ("Latin: Jacob Bidermann, Ludi theatrales sacri sive opera comica posthuma, "
               "Pars prima (Munich: Johann Wagner, 1666), the posthumous collected "
               "printing, in which Cenodoxus stands second (printed pp. 78–160); "
               "digitisation of the Regensburg copy at the MDZ (bsb11103594), located "
               "through its page OCR, emended against the sense, the crux pages verified "
               "by eye against the page images. The play was written for Augsburg in "
               "1602; the famous Munich performance of 1609 is reported to have sent "
               "fourteen courtiers into the Exercises. The modern editions of 1963/65 are "
               "in copyright and were not consulted, as the registry's condition "
               "required. English: this site's unofficial working translation (CC0)."),
    "hinweis": ("The schools' own art, at its darkest and greatest: the comico-tragoedia "
                "of the Paris doctor damned for vainglory, played by and for the "
                "colleges the Ratio built. The cut is deliberately narrow: Bidermann's "
                "preface, which separates history from fable and refuses calumny; the "
                "devil's harvest monologue with Philautia and Hypocrisis, self-love and "
                "hypocrisy, as the engines that need no hell to help them; the three "
                "cries of the corpse at the funeral — accused, judged, damned — with the "
                "sentence of Christ the Judge between them and Bruno's 'here burn, here "
                "cut' prayer after them; and Bruno's resolve, in which the play walks "
                "off its own stage into history: the founding of the Carthusians. The "
                "speaker sigla are the print's; the printed page numbers stand on the "
                "labels; the paragraph numbering is this site's own. Part of the "
                "concordance and the citation-bound dialogue; not part of the linguistic "
                "statistics, which describe the core corpus only."),
    "sections": [
        {"id": "lectori", "zk": "Cen. Lect.",
         "titel": "Lectori, Spectatori — history and fable",
         "blurb": ("Bidermann's own preface: the Paris doctor legend as the histories "
                   "hand it down, Bruno's conversion as its fruit — and the honest "
                   "boundary: the name Cenodoxus, 'vainglory', and the crime itself are "
                   "fable, chosen as what could 'most decently be represented'."),
         "units": [
             u(1, 1, LECT_LA, LECT_EN, label="p. 78 · the preface",
               note="'Haec historia … fabula est' — a Jesuit playwright stating his sources and his inventions apart, on the first page: the apparatus's own habit, practised on stage in 1602."),
         ]},
        {"id": "philautia", "zk": "Cen. I",
         "titel": "The devil's harvest — Philautia and Hypocrisis",
         "blurb": ("Act I: the demon marvels that anyone is left alive on earth, since "
                   "most men go to ruin of their own accord — and the few who resist "
                   "are led astray by Self-love and Hypocrisy, the two allegories that "
                   "will undo the doctor without a single spectacular sin."),
         "units": [
             u(2, 1, PHIL_LA, PHIL_EN, label="p. 93 · 'sua plerique sponte pessum eunt'",
               note="The play's moral engine in one line: hell's powers are almost unnecessary — 'quos Philautia Hypocrisisque facile transversos agunt.' The guardian angel's fresh footprints at the scene's end are the counter-machinery."),
         ]},
        {"id": "funus", "zk": "Cen. V",
         "titel": "The three cries — accused, judged, damned",
         "blurb": ("Act V, the funeral: three times the corpse rises on the bier and "
                   "interrupts its own obsequies — ACCUSATUS SUM, IUDICATUS SUM, IUSTO "
                   "DEI IUDICIO DAMNATUS SUM — with the sentence of Christ the Judge "
                   "spoken in between, and Bruno's prayer after: here burn, here cut, "
                   "that you may spare elsewhere."),
         "units": [
             u(3, 1, FUN1_LA, FUN1_EN, label="p. 143 · the first cry: ACCUSATUS SUM",
               note="Bruno's first reflex is the charitable one — the accusation may be the devil's slander, 'for to accuse whomever one pleases is free to him.'"),
             u(4, 2, FUN2_LA, FUN2_EN, label="p. 150 · the second cry: judged — and the deferral",
               note="Bruno still argues for hope — 'we are said to judge the innocent too, when we acquit' — and closes with the play's most quoted despair: 'eheu, vivimus, nec vivimus: morique cogimur, neque sinimur mori.'"),
             u(5, 3, FUN3_LA, FUN3_EN, label="p. 152 · the sentence of Christ the Judge",
               note="The judgment scene the audience saw between the second and third funeral: the wounds as witnesses, the merits that could not be greater — and the sentence, 'I, digna lue supplicia.'"),
             u(6, 4, FUN4_LA, FUN4_EN, label="p. 153 · the third cry: DAMNATUS SUM",
               note="The print sets the line in capitals, as this edition preserves: 'IUSTO DEI IUDICIO DAMNATUS SUM.' Verified by eye against the page image."),
             u(7, 5, FUN5_LA, FUN5_EN, label="p. 154 · Bruno's prayer: here burn, here cut",
               note="'Hic, Numen, ure, caede, plecte, seca, feri, saevi' — Augustine's 'hic ure, hic seca' made a dramatic exit line; the holiness that was no holiness 'apud severi Iudicis subsellia' closes the scene."),
         ]},
        {"id": "bruno", "zk": "Cen. Brun.",
         "titel": "Bruno's resolve — the play walks into history",
         "blurb": ("Act V, the last scenes: Bruno gathers the six companions; the dead "
                   "man's living voice forbids living and makes dying a terror; the "
                   "cause was said more clearly by being kept silent; and the resolve — "
                   "'Non creditur' three times, 'perdere haec malo, quam perire' — "
                   "leads them off the stage toward the Grande Chartreuse."),
         "units": [
             u(8, 1, BRU1_LA, BRU1_EN, label="p. 156 · 'vivere prohibet; terret mori'"),
             u(9, 2, BRU2_LA, BRU2_EN, label="p. 157 · the cause said by silence",
               note="The play's hermeneutics of its own riddle: had the corpse named one vice, the hearers would have nursed all the others — 'bene itaque tacuerat singula, ut nos omnia metuere disceremus.'"),
             u(10, 3, BRU3_LA, BRU3_EN, label="p. 158 · Non creditur — and the departure",
               note="The print italicises the triple 'Non creditur'; the crux 'piceata flammarum volumina' — the pitch-black rolling flames — was verified by eye (the OCR had garbled it). 'Perdere haec malo, quam perire': the Carthusian founding as the exit."),
         ]},
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
n = sum(len(s["units"]) for s in DATA["sections"])
print(f"wrote {os.path.normpath(OUT)}: {len(DATA['sections'])} sections, {n} units")
