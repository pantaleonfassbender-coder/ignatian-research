# -*- coding: utf-8 -*-
"""Build data/servitus.json — Molina on the slave trade: De iustitia et
iure, tract. II, disputations 34–35.

The conscience line's third front. Luis de Molina, professor at Évora in
the kingdom that ran the trade, examined the Portuguese slave trade as a
moral theologian and as a field-worker: he questioned the returning
merchants in person — 'cum quibus locutus sum' — set down what the trade
looked like from inside, and passed judgment. Source: De Iustitia, Tomus
Primus (first published Cuenca 1593; carried from the Venice printing of
1594, 'apud Minimam Societatem'; Internet Archive `bub_gb_wcZhc3OG5VsC`),
public domain. The seven passages carried here were located through the
scan's OCR and then transcribed and emended BY EYE from the page images
(leaves 204, 213, 215, 216, 217; the OCR of the 1594 type served for
navigation — it had, among much else, turned the fourth conclusion's
number into 'a.'); contractions silently expanded, u/v classicised,
printed spellings (Aethyopes, coelum-class) kept. The English is this
site's unofficial working translation, dedicated CC0.

What the module carries, in the print's own order: the title of the trade
is not war but purchase, and the merchants' answers when questioned
(disp. 34); the market's logic reported — the value of the man as man,
and as redeemed by Christ's blood, does not enter the price (disp. 35);
the fourth conclusion — the trade as practised is unjust, its
practitioners in mortal sin and the state of eternal damnation, and king,
councillors, bishops and confessors bound each in his degree (disp. 35);
the wars that supply the slaves are 'rather robberies than wars', with
the night raid described and the trade itself named as their incitement
(disp. 35); the cruelties told in a refusal to tell them — the severed
arm used as a whip, the ships' dead (disp. 35); and the fifth conclusion,
which weighs the evangelization argument and refuses it: evil is not to
be done that good may come, and no man's servitude is to be permitted
unless its justice is established more clearly than light (disp. 35).

The entanglement is stated where it belongs, in the module's note and in
the introductory essay: the Society itself held slaves — on the Brazilian
and Spanish-American estates of its colleges and in the Maryland mission
— within the very period this module documents; Molina's own fourth
conclusion exempts no one by habit. Named next steps: Sandoval's De
instauranda Aethiopum salute (Seville 1627; no public-domain scan located
on the Internet Archive — the hunt continues elsewhere) and Vieira's
sermons to and about the enslaved (the original Lisbon printings are on
the Archive; Portuguese would be a new corpus language)."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "servitus.json")

def u(n, k, orig, en, label=None, note=None):
    d = {"n": n, "k": k}
    if orig: d["orig"] = " ".join(orig.split())
    if en: d["en"] = " ".join(en.split())
    if label: d["label"] = label
    if note: d["note"] = note
    return d

M1_LA = """Iam vero titulus, quo mancipia haec Lusitanorum servituti
subiiciuntur, non est ius aliquod belli, quod Lusitani cum illis gentibus
habeant; sed sola emptio, pro mercibusve permutatio. Quare iuxta ea, quae
disputatione praecedente dicta sunt, ut legitime a Lusitanis titulo
emptionis aut permutationis possideantur, necesse est, quando eis
venduntur, aut permutantur, aliquo alio titulo legitime redacta iam
fuisse in servitutem. Nisi forte aliquod eorum a Lusitanis ematur, ut a
morte suorum iusta, vel iniusta eruatur, iuxta ea quae disputatione
praecedente dicta sunt. Facta autem diligenti inquisitione, dicam paucis,
quod de hac re comperire potui."""
M1_EN = """Now the title by which these slaves are subjected to the
servitude of the Portuguese is not any right of war which the Portuguese
have with those nations, but purchase alone, or exchange for wares.
Wherefore, according to what was said in the preceding disputation, for
them to be legitimately possessed by the Portuguese under the title of
purchase or exchange, it is necessary that, when they are sold or
exchanged to them, they should already have been legitimately reduced to
servitude by some other title — unless perchance one of them be bought by
the Portuguese to be rescued from death at the hands of his own people,
just or unjust, according to what was said in the preceding disputation.
Having made diligent inquiry, I will say in few words what I have been
able to find out about this matter."""

M2_LA = """Lusitani nihil omnino curant de titulo, quo ii, qui ipsis in
commutationem pro mercibus venduntur, a suis, aut ab eorum adversariis in
servitutem redacti sint; sed quotquot illis afferuntur, tot emunt, modo,
pro pretii quantitate, illis placeant. Quin dicunt, nec si de titulo
inquirere vellent, quicquam certi possent reperire; idque aegre
paterentur Aethyopes, non secus ac inter nos aegre ferret venditor mercis
alicuius, si ab emptore interrogaretur de titulo, quo eam comparavit.
Denique quantum intelligere potui ex mercatoribus, qui eiusmodi mancipia
in Aethyopia emunt, eaque inde huc asportant (cum quibus locutus sum,
quique nihil eorum, quae retuli, diffitentur) illi nihil aliud curant in
hac negotiatione, quam suum lucrum et commodum; miranturque si quis illis
scrupulum velit iniicere; satisque praeclarum cum Aethyopibus, quos ita
emptos asportant, factum esse putant, cum hac ratione ad fidem
adducantur, et praeterea longe meliorem vitam, quoad corpus, inter nos
ducant, quam inter suos nudi, vilique cibo nutriti. Interrogati huiusmodi
mercatores, num interdum ab Aethyopibus venditum sportentur in navigia
mancipia, de quibus vel praesumptio sit, vel constet, furto esse ablata a
suis oppidanis? Respondent, id aliquando, tametsi non admodum frequenter,
accidere. Interrogati rursus, quanam conscientia ea emant, cum sciant
furto esse ablata, neque legitime in servitutem redacta? Quidam
respondit: Quoniam, nisi emantur, sunt continuo interficienda ab iis
ipsis, qui ea furati sunt, ne res detegatur, ipsique a suis ob delictum
interficiantur. Alius dixit, multos non audere ea emere: quoniam si res
detegatur, periclitabuntur ipsi mercatores. Eo quod lex mercatoribus ab
Aethyopibus sit imposita, ut privatim nullum ita emant, nisi accedente
simul sene aliquo Aethyope, qui et interpres sit, et videat, num furto
sit ablatum. Itaque comperi haec etiam emi. Quod si interdum non emantur,
raro mercatores propter conscientiam id non efficere, sed ut poenam,
indignationemque Aethyopum fugiant."""
M2_EN = """The Portuguese care nothing at all about the title by which
those who are sold to them in exchange for wares were reduced to
servitude by their own people or by their adversaries; but however many
are brought to them, so many they buy, provided only that, for the
quantity of the price, they please them. Indeed they say that even if
they wished to inquire into the title, they could find out nothing
certain; and that the Ethiopians would take it ill — just as among us a
seller of some ware would take it ill if he were questioned by the buyer
about the title by which he acquired it. Finally, so far as I could
understand from the merchants who buy such slaves in Ethiopia and carry
them from there to this country — with whom I have spoken, and who deny
nothing of what I have related — they care for nothing else in this
trade than their own profit and convenience; and they marvel if anyone
would cast a scruple into them; and they think they have dealt handsomely
enough with the Ethiopians whom they carry off thus bought, since by this
means they are brought to the faith, and moreover lead a far better life,
as regards the body, among us than they did among their own, naked and
fed on vile food. These merchants, being asked whether slaves are
sometimes carried aboard the ships, sold by the Ethiopians, of whom there
is either a presumption or a certainty that they were taken by theft from
their own townsmen — they answer that this happens sometimes, though not
very frequently. Asked again with what conscience they buy them, when
they know they were taken by theft and not legitimately reduced to
servitude — one answered: Because, unless they are bought, they will
straightway be killed by the very men who stole them, lest the thing be
discovered and they themselves be killed by their own people for the
crime. Another said that many dare not buy them, because if the thing is
discovered the merchants themselves will be in peril — a law having been
imposed on the merchants by the Ethiopians that no one may privately buy
in this way unless there be present at the same time some Ethiopian
elder, who serves as interpreter and sees whether it was taken by theft.
And so I have found that even these are bought. And if sometimes they are
not bought, it is rarely for conscience' sake that the merchants forbear,
but to escape the punishment and the indignation of the Ethiopians."""

M3_LA = """Ego negotiationem hanc in Guinea ex hoc capite damnare non
auderem, neque legi hactenus, qui eam damnet, aut in dubium ex hoc capite
eam revocet. Ratio est, quoniam res illae, licet inter nos vilipendantur,
apud illos tamen ob penuriam et raritatem plurimi aestimantur, tametsi ad
id conferat rudis, agrestisque ipsorum natura. Praeterea transportatio
earum tam longo maris tractu, tanta molestia et periculis, earum pretium
multum in illis locis merito auget, posito, quod Aethyopes illis rebus
delectentur, ac proinde eas velint emere. Item abundantia mancipiorum,
quae illis in locis vendenda exponuntur, vilius multo efficit illorum
pretium, quam si pauciora venderentur. Item sumptus faciendi in
mancipiis asportandis, molestia, et periculum in eisdem afferendis, tum
ne mancipia ipsa, tum etiam ne mercatores ipsi pereant, merito
mercatorum comparatione vilius multo facit pretium illorum, quam si haec
omnia non intervenirent. Neque hac in re attendi debet valor hominis,
qua homo est, neque item quatenus Christi sanguine est redemptus, ut
quidam de negotiatione hac admirans, eamque hac sola ratione suspectam
habens, obiiciebat: sed commoditas, quae a mercatore ex mancipio
asportando percipitur."""
M3_EN = """For my part I would not dare to condemn this trade in Guinea
on this head [the vileness of the price], nor have I read anyone hitherto
who condemns it, or calls it into doubt on this head. The reason is that
those wares, though despised among us, are valued very highly among them
because of scarcity and rarity — though their rude and rustic nature
contributes to it. Moreover the transport of them over so long a stretch
of sea, with such trouble and dangers, rightly raises their price much in
those places, granted that the Ethiopians delight in those things and
therefore wish to buy them. Likewise the abundance of slaves who are put
up for sale in those places makes their price much viler than if fewer
were sold. Likewise the expenses to be made in carrying the slaves off,
the trouble and the danger in bringing them — lest the slaves themselves,
and lest the merchants themselves, perish — rightly, by the merchants'
reckoning, makes their price much viler than if all these things did not
intervene. Nor in this matter is the value of the man, as he is a man, to
be considered, nor again insofar as he has been redeemed by the blood of
Christ — as a certain man, marvelling at this trade and holding it
suspect for this reason alone, objected — but the profit which the
merchant receives from the slave he carries away."""

M4_LA = """Forte non deerit, qui ex hoc capite sedare velit conscientias
ementium mancipia ab infidelibus in utraque Guinea, et in Cafreria, eaque
in hoc regnum, et ad alia loca asportantium, negotiationemque hanc iustam
ac licitam proferre audeat. Sit nihilominus quarta conclusio. Mihi longe
verisimilius est, negotiationem hanc ementium eiusmodi mancipia ab
infidelibus illis in locis, eaque inde asportantium, iniustam,
iniquamque esse, omnesque qui illam exercent, lethaliter peccare,
esseque in statu damnationis aeternae, nisi quem invincibilis ignorantia
excuset, in qua neminem eorum esse affirmare auderem. Regem praeterea,
et omnes, qui regni clavum in manu tenent, nec non Episcopos promontorii
viridis, et Insulae Divi Thomae, et qui horum omnium confessiones
audiunt, singulos in suo gradu et ordine, teneri curare, ut res haec
examinetur, et statuatur quid liceat, et quid non liceat, et ut
iniustitiae in posterum efficaciter resecentur; nisi eis aliquid, quod
me lateat, in facto ipso innotescat, aut principia alia eis eluceant,
quae ego ignorem. Ducor, quoniam lethale est peccatum, non solum contra
caritatem, sed etiam contra iustitiam, cum onere restituendi, emere ea,
de quibus verisimilis est praesumptio, aut esse merito debet (quamvis
avaritia obcaecante de ea non curetur) titulo iniusto esse comparata,
nec esse vendentium."""
M4_EN = """Perhaps there will not be wanting one who on this head would
quiet the consciences of those who buy slaves from the infidels in both
Guineas and in Cafraria, and carry them to this kingdom and to other
places, and who would dare to pronounce this trade just and licit. Let
there nevertheless be a fourth conclusion. To me it is by far more
probable that this trade of those who buy such slaves from the infidels
in those places, and carry them from there, is unjust and iniquitous;
and that all who practise it sin mortally, and are in the state of
eternal damnation, unless invincible ignorance excuse someone — in which
I would not dare to affirm that any of them stands. Moreover, that the
King, and all who hold the helm of the kingdom in their hand, as also
the Bishops of the Cape Verde promontory and of the Island of São Tomé,
and those who hear the confessions of all these, each in his own degree
and order, are bound to see to it that this matter be examined, and that
it be determined what is licit and what is not licit, and that the
injustices be henceforth effectively cut away — unless something that
escapes me should be known to them in the fact itself, or other
principles shine out to them which I do not know. I am led to this
because it is a mortal sin, not only against charity but also against
justice, with the burden of restitution, to buy things of which there is
a probable presumption — or deservedly ought to be, though through
blinding avarice no one troubles about it — that they were acquired by
an unjust title, and are not the sellers' to sell."""

M5_LA = """Sed iam ad Aethyopum bella veniamus. Sane quam rarissime
praesumendum est ea iusta esse. Etenim, qui se inter eos potentiores
arbitrantur, alios iniuste invadunt, et opprimere conantur; atque hi
sunt, qui maiores mancipiorum venalium praedas asportant, aliis iniuriam
sustinentibus, mancipiisque ipsis iniuste suam libertatem amittentibus.
Narravit mihi quidam dignus fide, qui inter Cafres longo tempore fuerat
versatus, quique parum scrupuli in emendis eiusmodi mancipiis habebat,
esse in ea regione inter alios quendam veluti regem, qui subditos
audaces et praeferoces habebat, quos caeteri multum timebant; huncque,
ut magnam mancipiorum copiam quaestus gratia cogeret, consuevisse de
nocte in loca circumvicina impetum facere, militibus in varios pagos
distributis; ubi vero ad proxima loca ventum est, et iam colloquiis
apta, vocem quam maxime contendere ac proclamare, se advenisse,
admonereque ut sibi consulant, et advertant, quanto sint ipsi armis
superiores, potentioresque illis, foreque ut, nisi tot in servitutem
tradant, omnes internecione ferant; tunc miseros illos, perterritos ne
omnes caedantur, ingredi domum, et hunc exponere extra domum filium vel
filiam, et claudere ostium, alium unam ex uxoribus, etc., eoque modo
captivos duci ac vendi. Quod de Aethiopum bellis, quibus ordinarie
capiunt mancipia, quae Lusitanis vendunt, praesumendum esse arbitror
(iuxta ea, quae mercatores ipsi, nulla tormentorum vi coacti, dum
interrogantur, respondent) est, potius illa esse latrocinia, quam bella.
Quin et negotiatio haec Lusitanorum occasio, incitamentumque videtur
illis esse, exercendi inter se eiusmodi hominum praedas, aut certe longe
frequentius, atque in maiori hominum numero, quam si non esset ea
negotiatio. Id quod negotiationem quoque inficit atque damnat."""
M5_EN = """But let us now come to the wars of the Ethiopians. Assuredly
it is most rarely to be presumed that they are just. For those among
them who reckon themselves the more powerful unjustly invade the others
and try to crush them; and these are they who carry off the greater
booties of slaves for sale, while the others suffer the injury, and the
slaves themselves unjustly lose their liberty. A man worthy of belief,
who had lived long among the Cafres and who had little scruple in buying
such slaves, told me that in that region there is among others one who
is as it were a king, who had bold and very fierce subjects whom the
rest greatly feared; and that this man, in order to gather a great store
of slaves for the sake of gain, was accustomed to make an assault by
night upon the surrounding places, his soldiers being distributed
through the various villages; and when they had come to the nearest
places, now within earshot, to strain his voice to the utmost and
proclaim that he had come, and to warn them to look to themselves and
consider how much superior in arms and more powerful than they he was,
and that unless they handed over so many into servitude, he would
destroy them all; and that then those wretched people, terrified lest
they all be slaughtered, would go into the house, and one would put out
of doors a son or a daughter and shut the door, another one of his
wives, and so forth; and in this manner they were led away captive and
sold. As for the wars of the Ethiopians, by which they ordinarily take
the slaves they sell to the Portuguese, I judge it is to be presumed —
according to what the merchants themselves, compelled by no force of
torture, answer when they are questioned — that they are rather
robberies than wars. Nay more, this trade of the Portuguese appears to
be for them the occasion and the incitement to carry on such raids of
men among themselves — or certainly far more frequently, and upon a
greater number of men, than if that trade did not exist. Which thing,
too, infects and condemns the trade."""

M6_LA = """Hoc loco nihil de saevitia dicam, qua interdum eiusmodi
mancipia tractantur, dum ab illis, quos Tangosmaos aut pomberos
appellant, ab interioribus locis ad navigia asportantur. Fertur enim
praescindi interdum brachium unius, mortuumque relinqui: eo vero,
tanquam flagello, alios percuti atque agi, ut mortis timore iter
faciant, aliasque saevitias in eos exerceri. Dum enim miseri a suis
avelli, vinctosque ita se produci vident, partim a more patriae, partim
servitutis metu, mortisque horrore (metuunt quippe ne interficiantur et
devorentur) retardati pergere renuunt; ii etiam, qui eos ducunt,
interdum non qualicunque eorum passu sunt contenti. Nihil item dicam de
saevitia, qua in navigiis, dum asportantur, tractari saepe soleant, et
qua multi sint, qui, ut multum lucrentur, tam multos asportant, ut
necesse sit plurimos illorum mori propter navigii angustias, quibus
velut carcere noctes atque dies includuntur. Haec enim, et his similia,
vitia sunt negotiantium, quae negotiationem ipsam non efficiunt per se
iniustam et illicitam; illis tamen mederi, tum ad Episcopos, parochos,
et confessarios spectat, tum etiam ad gubernatores illarum provinciarum,
et huius regni, ad aliosque regis ministros: expediretque forte, ut
aliquae ea de re conderentur leges. Atque utinam graviora alia
infortunia ob hoc negotiationis genus tanto tempore dissimulatum, ut
aliqui timent, non evenerint."""
M6_EN = """In this place I will say nothing of the cruelty with which
such slaves are sometimes treated while they are carried from the inland
places to the ships by those whom they call Tangosmaos or pomberos. For
it is reported that sometimes the arm of one is cut off, and he is left
dead; and with it, as with a whip, the others are struck and driven, that
they may make the journey for fear of death; and that other cruelties are
practised upon them. For when the wretches see themselves torn from their
own people and led along thus in chains, held back partly by the custom
of their native land, partly by the fear of servitude and the horror of
death — for they fear they will be killed and devoured — they refuse to
go on; and those who lead them are sometimes not content with whatever
pace they can make. Likewise I will say nothing of the cruelty with which
they are often wont to be treated in the ships while they are carried
across, and of the fact that there are many who, in order to make much
profit, carry so many that very many of them must die from the narrowness
of the ship, in which they are shut up, as in a prison, night and day.
For these things, and the like of them, are vices of the traders, which
do not make the trade itself of its own nature unjust and illicit; yet to
remedy them belongs both to the bishops, parish priests and confessors,
and also to the governors of those provinces and of this kingdom, and to
the king's other ministers: and it would perhaps be expedient that some
laws be enacted on this matter. And would that other, graver misfortunes
have not come to pass — as some fear — on account of this kind of trade,
so long winked at."""

M7_LA = """Sit nihilominus quinta conclusio. Interim dum illis omnibus
nationibus (in quibus ostium magnum et evidens apertum est, desidiaque
nostra pereunt) concionatores non suppetunt, aliique Ecclesiastici
ministri, qui ea, quae Iesu Christi sunt, quaerant; sane viris piis huic
causae servitutis favendum est, quantum salva conscientia fieri possit:
eo quod miseris captivis tantum bonum, quantum est fides, extrahi a
barbara illa et impia hominum colluvione, et inter Christianos vivere,
ac vitam finire, tametsi cum servitutis perpetuae miseria coniunctum, ea
ratione obveniat. Quia tamen facienda non sunt mala, ut eveniant bona,
iique qui illos asportant, non spirituale eorum bonum, sed temporale
suum lucrum quaerunt; non plus negotiationem hanc approbare fas est, nec
Episcopis Viridis promontorii, et Insulae Divi Thomae confessariisque,
aut iis, qui regni huius clavum tenent, eam permittere licebit, quam
iustitia, et proximi caritas patiantur. Quod si ministri Evangelii ad
nationes illas barbaras idonei mitterentur, in suisque regionibus ad
fidem converterentur, tunc sane omnes pii consulere potius deberent, ac
favere miserorum hominum libertati; neque aliter servitus cuiusque
illorum est permittenda, quam si luce clarius eam iustam esse constet.
Tum quod libertatis causae, quippe quae piissima est, per se sit
suffragandum."""
M7_EN = """Let there nevertheless be a fifth conclusion. In the meantime,
while preachers are not to be had for all those nations — in which a
great and evident door stands open, and through our sloth they perish —
nor other ministers of the Church who seek the things that are Jesus
Christ's, pious men may indeed favour this cause of servitude, so far as
it can be done with a safe conscience: because in this way there comes to
the wretched captives so great a good as is the faith — to be drawn out
of that barbarous and impious sink of men, and to live among Christians,
and to end their life there, though it be joined with the misery of
perpetual servitude. Yet because evils are not to be done that goods may
come, and because those who carry them off seek not their spiritual good
but their own temporal profit, it is no more lawful to approve this
trade — nor will it be permitted to the Bishops of the Cape Verde
promontory and of the Island of São Tomé, and to the confessors, or to
those who hold the helm of this kingdom, to allow it — than justice and
the charity of one's neighbour can bear. But if fit ministers of the
Gospel were sent to those barbarous nations, and they were converted to
the faith in their own regions, then assuredly all the pious ought rather
to take counsel for, and to favour, the liberty of these wretched men;
nor is the servitude of any one of them to be permitted otherwise than if
it be established, more clearly than light, that it is just. And further,
because the cause of liberty, being the most pious of causes, is of
itself to be favoured."""

DATA = {
    "id": "servitus",
    "autor": "Luis de Molina",
    "titel": "De iustitia et iure — the slave trade before the conscience (1593)",
    "jahr": 1593,
    "lang": "la",
    "zitierweise": "Mol. 34/35 [k]",
    "quelle": ("Latin: Luis de Molina, De Iustitia, Tomus Primus (first published Cuenca "
               "1593; carried from the Venice printing of 1594, 'apud Minimam Societatem'; "
               "Internet Archive bub_gb_wcZhc3OG5VsC), tract. II, disputations 34–35; "
               "public domain. The seven passages carried were located through the OCR and "
               "then transcribed and emended by eye from the page images (leaves 204, 213, "
               "215–217); contractions silently expanded, u/v classicised, the print's "
               "spellings (Aethyopes) kept. English: this site's unofficial working "
               "translation (CC0). Named next steps: Sandoval's De instauranda Aethiopum "
               "salute (Seville 1627 — no public-domain scan yet located) and Vieira's "
               "sermons to and about the enslaved (original printings on the Archive; "
               "Portuguese would be a new corpus language)."),
    "hinweis": ("The conscience line's third front, and its hardest sentence to read "
                "aloud: the Society's own theologian examining the trade of the kingdom "
                "the Society served. Molina questioned the returning merchants himself — "
                "'cum quibus locutus sum' — and his fourth conclusion is carried here "
                "whole: the trade as practised is unjust, its practitioners in mortal sin "
                "and the state of eternal damnation, with king, councillors, bishops and "
                "confessors bound each in his degree. The failure is stated with the "
                "voice: the Society itself held slaves within this very period, on the "
                "Brazilian and Spanish-American estates of its colleges and later in the "
                "Maryland mission; Cartagena's college, where Sandoval wrote and Claver "
                "served, ran on enslaved labour; and Molina himself, in the fifth "
                "conclusion, weighs the evangelization argument seriously before refusing "
                "it — the module carries his ambivalence as it stands, including the "
                "pricing discussion in which 'the value of the man as man' enters the "
                "reckoning only as the market's omission. The paragraph numbering is this "
                "site's own; the disputation numbers are the book's. Part of the "
                "concordance and the citation-bound dialogue; not part of the linguistic "
                "statistics, which describe the core corpus only."),
    "sections": [
        {"id": "disp34", "zk": "Mol. 34",
         "titel": "Disputation 34 — the trade examined",
         "blurb": ("From which places the slaves are carried off by the Portuguese, and "
                   "by what title: not war but purchase alone — and the merchants' own "
                   "answers when questioned, set down by the theologian who spoke with "
                   "them."),
         "units": [
             u(1, 1, M1_LA, M1_EN, label="The title is not war, but purchase",
               note="'Facta autem diligenti inquisitione, dicam paucis, quod de hac re comperire potui' — the method statement: moral theology as field inquiry, at Évora and Lisbon, among the returning merchants."),
             u(2, 2, M2_LA, M2_EN, label="The merchants questioned",
               note="The whole trade in three answers: no one asks about titles; stolen people are bought 'lest they be killed by the very men who stole them'; and where buying is refused, it is rarely for conscience' sake."),
         ]},
        {"id": "disp35", "zk": "Mol. 35",
         "titel": "Disputation 35 — the judgment",
         "blurb": ("What is to be held concerning the slaves from the Lusitanian "
                   "commerce: the market's logic reported, the fourth conclusion — "
                   "unjust, iniquitous, mortal sin — the wars that are rather robberies, "
                   "the cruelties told in a refusal to tell them, and the fifth "
                   "conclusion, which weighs the argument from evangelization and "
                   "refuses it."),
         "units": [
             u(3, 1, M3_LA, M3_EN, label="The price of a man — the market's logic reported",
               note="The most chilling sentence in the module is a description, not a judgment: in the pricing of the trade 'the value of the man, as he is a man, is not to be considered, nor insofar as he has been redeemed by the blood of Christ' — the objection of the unnamed 'certain man' who found the trade suspect for that reason alone is preserved inside the sentence that sets it aside."),
             u(4, 2, M4_LA, M4_EN, label="The fourth conclusion — the verdict",
               note="Eye-verified against the page image (the OCR had destroyed the conclusion's number): 'omnesque qui illam exercent, lethaliter peccare, esseque in statu damnationis aeternae' — and the chain of responsibility from the King to the confessors, 'singulos in suo gradu et ordine'."),
             u(5, 3, M5_LA, M5_EN, label="Rather robberies than wars",
               note="The night raid described to Molina by a slave-buyer 'worthy of belief' — and the conclusion that the Portuguese trade is itself the occasion and incitement of the raids: 'Id quod negotiationem quoque inficit atque damnat.'"),
             u(6, 4, M6_LA, M6_EN, label="The cruelties, told as a refusal to tell",
               note="A praeteritio that carries everything it declines to say: the severed arm used as a whip, the ships in which 'very many of them must die from the narrowness'. Molina files these as 'vices of the traders' that do not of themselves make the trade unjust — the taxonomy is part of the document, carried as it stands."),
             u(7, 5, M7_LA, M7_EN, label="The fifth conclusion — evangelization weighed, and refused",
               note="'Facienda non sunt mala, ut eveniant bona' — and the standard that ends the module: no man's servitude is to be permitted 'unless it be established, more clearly than light, that it is just'; the cause of liberty, 'being the most pious of causes, is of itself to be favoured'."),
         ]},
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
n = sum(len(s["units"]) for s in DATA["sections"])
print(f"wrote {os.path.normpath(OUT)}: {len(DATA['sections'])} sections, {n} units")
