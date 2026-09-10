# -*- coding: utf-8 -*-
# Build data/imago.json — Imago primi saeculi Societatis Iesu (Antwerp:
# Plantin press of Balthasar Moretus, 1640), the Society's centenary volume:
# the iconographic pilot of this apparatus.
#
# Images: rendered from the Internet Archive scan imagoprimisaecul00boll
# (public domain), cropped to the plates; files in assets/imago/. PDF leaves
# (printed pages): 8 (engraved title), 212 (199), 213 (200), 339 (326),
# 465 (452), 472 (459), 578 (565), 730 (717), 734 (721), 954 (941). The
# emblem runs sit at the end of each book (PDF leaves 185-217, 330-343,
# 465-493, 574-594, 726-740, 950-965).
#
# The Dutch mirror: the same year and press issued the Af-Beeldinghe van
# d'eerste eeuwe der Societeyt Iesu (Internet Archive afbeeldinghevand00boll,
# public domain), the vernacular counterpart with the same plates and Dutch
# verses by Adriaen Poirters SJ. Each emblem here carries its Dutch page as a
# closing unit (assets/imago/nl-*.jpg, PDF leaf = printed page + 11), with
# the page heading and Poirters's rhymed gloss on the lemma transcribed by
# eye. For the forge emblem his first stanza is transcribed and translated
# in full - the Dutch page even glosses the pun: 'Faber, alias Smidt'.
# Latin: transcribed BY EYE from the same page images (long s normalised to
# s, ae ligature to ae, u/v as printed); the OCR was used only to locate the
# pages. English: unofficial working translations made for this site (CC0).
#
# Usage: python tools/build-imago.py
import io, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def units(rows):
    out = []
    for k, r in enumerate(rows, start=1):
        u = {'n': k, 'k': k}
        u.update(r)
        out.append(u)
    return out

def add(lst, rows):
    """Append rows to an already-numbered unit list, continuing n/k."""
    for r in rows:
        k = len(lst) + 1
        u = {'n': k, 'k': k}
        u.update(r)
        lst.append(u)

# The Dutch mirror pages: printed page, page heading, and Poirters's rhymed
# gloss on the Latin lemma (printed in braces beside it), each transcribed
# by eye from the page images of the Af-Beeldinghe.
NL = {
 'alitem':  (136, 'Vernieuwinghe vanden gheest.',
             "Te voren kroop, / Nu vliegh en loop.",
             "Renewal of the spirit. — 'Before, I crept; now I fly and run.'"),
 'orbis':   (204, 'De Seyndinghe nae Indien.',
             "Een alleen / VVas my te kleen.",
             "The mission to the Indies. — 'One alone was too small for me.'"),
 'monstrat': (270, 'Het boecksken vande gheestelijcke Oeffeninghen is eenen '
              'sekeren leydts-man om eenen staet des leuens te verkiesen.',
             "Vraeght hier raedt, / Eer ghy gaet.",
             "The little book of the Spiritual Exercises is a sure guide for "
             "choosing a state of life. — 'Ask counsel here, before you go.'"),
 'sagitta': (388, 'De Societeyt wordt te vergheefs vande benijders bevochten.',
             "Als 't Gode behaeght, / Beter benijdt, dan beklaeght.",
             "The Society is assailed by the envious in vain. — 'As it pleases "
             "God: better envied than pitied.'"),
 'faber':   (508, 'Ignatius ghebruyckt Faber, alias Smidt, tot de bekeeringhe '
              'van Xauerius.',
             "Al is 't vier vverm, / 't Vereyscht 's smits erm.",
             "Ignatius employs Faber — alias Smith — for the conversion of "
             "Xavier. — 'Though the fire be warm, it needs the smith's arm.' "
             "The Dutch page spells the pun out in its heading."),
 'animas':  (690, "De Seyndinghe nae 't legher.",
             "Der sielen buyt / Kies ick voor uyt.",
             "The mission to the army. — 'The booty of souls I choose first.'"),
 'nexus':   (134, 'Vernieuwinghe der beloften.',
             "Het maeckt hem vast, / Soo langh het wast.",
             "Renewal of the vows. — 'It binds him fast, as long as it grows.'"),
 'omnibus': (258, 'Werck-lieden der Societeyt.',
             "Ghelijck / Aen ieghelijck.",
             "The workmen of the Society. — 'Like unto everyone.'"),
 'terra':   (514, 'Xauerius de wereldt doorreyst hebbende, sterft inden '
              'ingangh van China.',
             "Als de ronde is ghedaen, / Sult ghy onder d'aerde gaen.",
             "Xavier, having journeyed through the world, dies at the gate of "
             "China. — 'When the round is done, you shall go under the earth.'"),
}
def nl_unit(name):
    p, kop, gloss, en = NL[name]
    return {'img': f'assets/imago/nl-{name}.jpg',
            'alt': (f'The same emblem in the Dutch Af-Beeldinghe of 1640, '
                    f'p. {p}: the plate re-engraved smaller, above the Latin '
                    f'lemma with a rhymed Dutch gloss and the vernacular verse '
                    f'of Adriaen Poirters.'),
            'label': f'The Dutch mirror — Af-Beeldinghe 1640, p. {p}',
            'orig': f'{kop} — {gloss}',
            'en': en}

FRONT = units([
 {'img': 'assets/imago/frontispiece.jpg',
  'alt': ('Engraved title of the Imago primi saeculi (Antwerp 1640): the Society '
          'personified, crowned with the IHS monogram, above the Plantin imprint '
          'of Balthasar Moretus; putti carry the medallions of the six books and '
          'banderoles of the Doctors, Martyrs and Virgins.'),
  'en': ("The engraved title, by the Galle workshop for the Plantin press: the "
         "Society sits enthroned as a crowned figure bearing the IHS, her titulus "
         "reading 'Imago primi saeculi Societatis Iesu a Provincia Flandro-Belgica "
         "eiusdem Societatis repraesentata' — the image of the Society's first "
         "century, presented by its Flemish-Belgian province. Around her, putti "
         "display six emblem medallions, one for each book of the volume: the "
         "Society born, growing, working, suffering, honoured, and the province "
         "itself. The imprint reads 'Antverpiae ex officina Plantiniana Balthasaris "
         "Moreti, anno Societatis saeculari M.DC.XL' — in the Society's centenary "
         "year, 1640. Everything the volume's critics would later mock is already "
         "here: the scale, the self-confidence, the apparatus of triumph."),
  'label': 'The engraved title of 1640'},
])

ORBIS = units([
 {'img': 'assets/imago/unus-non-sufficit-orbis.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 326: a winged genius stands '
          'between two globes — the old world and the new — holding a bow, his '
          'arrow pointing across them.'),
  'orig': 'Societatis Missiones Indicae. — Vnus non sufficit orbis.',
  'en': ("The missions of the Society to the Indies. — One world is not enough. "
         "The lemma adapts Juvenal on Alexander (Sat. X 168: 'unus Pellaeo iuveni "
         "non sufficit orbis'); the epigram makes the comparison explicit."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Esse quid hoc dicam generosae mentis? vtrumque / Hic puer amplexus expedit ante globum.',
  'en': 'What shall I call this but greatness of mind? This boy holds both globes clasped before him.'},
 {'orig': 'Dic puer, an toto pectus tibi latius orbe est, / Et minor est animo mundus vterque tuo?',
  'en': 'Say, boy — is your breast wider than the whole world, and are both worlds together smaller than your spirit?'},
 {'orig': 'Sic quondam AEmathio iuueni par non fuit orbis; / Et quo non potuit praelia, vota tulit.',
  'en': 'So once the world was no match for the Emathian youth: where he could not carry war, he carried wishes.'},
 {'orig': 'Ille tamen victor Regnorum, ad flumina Gangis / Constitit, & magno victus ab orbe fuit.',
  'en': 'Yet he, the conqueror of kingdoms, halted at the streams of the Ganges, and by the greatness of the world was himself conquered.'},
 {'orig': 'Maior amor Gangem superans, pelagusque profundum, / Victor in extremis finibus orbis agit.',
  'en': 'A greater love overcomes the Ganges and the deep sea, and works as conqueror at the farthest ends of the earth.'},
 {'orig': 'Illius in castris qui signa sequuntur IESV / (Ignauus tali quis velit esse duce?)',
  'en': "Those who follow the standards of JESUS in his camp — who would consent to be idle under such a leader? —"},
 {'orig': 'Quid mirum, Herculeas vltra ac freta vasta columnas, / Quaerere & Eoos, quaerere & Hesperios?',
  'en': 'what wonder that, beyond the columns of Hercules and the vast straits, they seek out the peoples of the dawn and of the evening alike?'},
 {'orig': 'Dius amor nullis arctatur finibus; illos / Igneus Ignatî spiritus intus agit.',
  'en': 'Divine love is straitened by no boundaries: the fiery spirit of Ignatius drives them on from within.'},
 {'orig': 'Exemplum ducis, atque animarum lucra decusque, / Et magno in terris fixa trophaea Deo,',
  'en': "Their leader's example, the winning of souls and its honour, and trophies planted on earth to the great God,"},
 {'orig': 'Ingentes animos faciunt, quos expleat vnus / Qui dulci recreat numine corda Deus.',
  'en': 'make their spirits vast — spirits that only the one God can fill, who refreshes hearts with his sweet presence.'},
])

ALITEM = units([
 {'img': 'assets/imago/mutor-in-alitem.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 200: in a cartouche, a '
          'butterfly breaks out of the silkworm’s cocoon in an open landscape.'),
  'orig': 'Renouatio spiritus. — Nouum mutor in alitem. Horat.',
  'en': ("The renewal of the spirit. — I am changed into a new winged creature. "
         "The lemma adapts Horace (Odes II 20, 'album mutor in alitem'); the "
         "engraving gives the ode's swan to the silkworm, and the renewal to the "
         "yearly renovation of vows and spirit in the Society's houses."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Vix bene conclusit proprio se carcere bombyx, / Et nouus inde tibi protinus ales adest.',
  'en': 'Scarcely has the silkworm shut itself into the prison of its own making, when out of it, all at once, a new winged creature stands before you.'},
 {'orig': 'Iam vigor, & volucres creuere in tergora pennae: / Qui modo serpebat, si lubet, ecce volat.',
  'en': 'Now there is strength, and flying feathers have grown upon its back: what just now crept — look, if it pleases — flies.'},
 {'orig': 'Nempe sibi talem format natura recessum, / Remigij alarum quo fabricetur opus.',
  'en': 'For nature shapes itself such a retreat precisely so that the oarage of wings may be built within it.'},
 {'orig': 'Ite agite, & sacris, Socij, vos claudite septis, / Roboris aetherei crescat vt inde vigor.',
  'en': 'Go then, companions, and shut yourselves within the sacred enclosures, that from there the strength of heavenly vigour may grow.'},
 {'orig': 'Innouat hîc vires, hîc sacrae semina flammae / Sufficit, hîc alas Daedalus aptat amor.',
  'en': 'Here love renews strength, here it supplies the seeds of the sacred flame, here — a Daedalus — it fits on the wings.'},
])

MONSTRAT = units([
 {'img': 'assets/imago/hac-monstrat-eundum.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 459: a traveller at a parting '
          'of ways looks up to a statue of Mercury on a pedestal, its arm pointing '
          'out the road; crosses mark the false paths.'),
  'orig': 'Libellus Exercitiorum dux certissimus ad eligendum vitae statum. — Hac monstrat eundum.',
  'en': ("The little book of the Exercises, the surest guide for choosing a state "
         "of life. — This way, it shows, one must go. A wayside Mercury for the "
         "book of the election: the apparatus's own core text, drawn as an emblem "
         "by the Society's centenary."),
  'label': 'The emblem and its lemma'},
 {'orig': 'In varias dissecta vias se semita pandit, / Et longis circum flexibus errat iter:',
  'en': 'The footpath splits and spreads into many ways, and the road wanders all about in long windings:'},
 {'orig': 'Cumque tibi dubius centum diuortia trames / Praebeat, e centum est vna tenenda via.',
  'en': 'and though the doubtful track offer you a hundred partings, of the hundred there is one way to be held.'},
 {'orig': 'Si semel incerto per deuia calle feraris, / Certa tuum cingent mille pericla caput.',
  'en': 'If once you are carried down an uncertain path into trackless country, a thousand certain dangers will ring your head.'},
 {'orig': 'Haec vrsis insessa, feros tegit illa leones, / Hic fallit caecos subdola fossa pedes.',
  'en': 'This road is beset with bears, that one hides savage lions; here a treacherous ditch cheats unseeing feet.'},
 {'orig': 'Ad caput illa redit crebro perplexa recursu, / Ista viatorum silua cruore madet.',
  'en': 'That one, tangled, runs back again and again to its own beginning; that wood is soaked with the blood of travellers.'},
 {'orig': 'O! quis in hoc ductor discrimine fila ministret, / Aut Ariadnaeo stamine signet iter?',
  'en': "Oh, what guide in this peril will hand us the threads, or mark out the way with Ariadne's clew?"},
 {'orig': 'Nocte Pharos inter Mareotica saxa regebat / Lumine deprensas officiosa rates.',
  'en': 'By night the Pharos, dutiful with its light, steered among the Mareotic rocks the ships it caught sight of;'},
 {'orig': 'Isacidas fluctus inter ducebat Erythrae / Designans facilem praeuia flamma fugam.',
  'en': "among the waves of the Red Sea a flame going before led the sons of Israel, tracing out an easy flight."},
 {'orig': 'Parce queri: tibi iam positis Ignatius armis / Caelesti rutilam praetulit igne facem.',
  'en': 'Cease complaining: Ignatius, his weapons now laid down, has carried before you a torch glowing with heavenly fire.'},
 {'orig': 'Paruus mole liber, sed rerum pondere magnus, / Non dubia cupidum ducet ad astra via.',
  'en': 'A book small in bulk but great in the weight of its matter will lead the longing soul to the stars by no uncertain way.'},
 {'orig': 'Ne violis, ne crede rosis: hac monstrat eundum, / Saeuit vbi in teneros plurima spina pedes.',
  'en': 'Trust neither the violets nor the roses: this way, it shows, one must go — where many a thorn rages against tender feet.'},
 {'orig': 'Hoc duce nec Pharios ignes, nec fila requires: / Certior hic Cresso stamine ductor erit.',
  'en': 'With this guide you will need neither the fires of Pharos nor the threads: this guide will be surer than the Cretan clew.'},
])

SAGITTA = units([
 {'img': 'assets/imago/solem-nulla-sagitta.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 565: four fools in motley '
          'shoot arrows at the sun; the arrows turn in the air and fall back '
          'toward the archers.'),
  'orig': 'Societas frustra oppugnatur ab inuidis. — Solem nulla sagitta ferit.',
  'en': ("The Society is attacked by the envious in vain. — No arrow strikes the "
         "sun. The Society's own answer, in 1640, to a century of Monita, "
         "pamphlets and polemic: read it beside the counter-voices this apparatus "
         "carries — and note that the archers are drawn as fools."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Stulte, quid in caelum non peruenientia mittis / Tela? quid insano praelia Marte geris?',
  'en': "Fool, why do you shoot at the sky weapons that will never arrive? Why wage battles under a madman's Mars?"},
 {'orig': 'Laedere ne solem possis, locus ipse tuetur; / Immensa nostro distat ab orbe via.',
  'en': 'Its very place protects the sun from your wounding: it stands an immeasurable way from our world.'},
 {'orig': 'Caucasus excelso licet imponatur Olympo, / Et super hos vastus Pelion Ossa premat:',
  'en': 'Though Caucasus be piled on high Olympus, and above them vast Pelion press down upon Ossa,'},
 {'orig': 'Non secus ac ima positus si valle maneres, / In stolidum recident spicula missa caput.',
  'en': 'no differently than if you stood in the deepest valley, the darts you send will fall back on your stupid head.'},
 {'orig': 'Tangere fac possis, radiorum luce corusca / Hostem ne videas impediere tuum.',
  'en': 'Suppose you could reach it: the flashing light of its rays will keep you from so much as seeing your enemy.'},
 {'orig': 'Fallere, si solem spectare haec carmina credis: / Stultitiam damnant, liuida turba, tuam.',
  'en': 'You deceive yourself if you think these verses concern the sun: it is your folly they condemn, you envious crowd.'},
 {'orig': 'Liuor iners claris Heroum detrahit ausis, / Et iaculo solem non feriente petit.',
  'en': 'Sluggish envy disparages the shining deeds of heroes, and aims at the sun with a javelin that never strikes.'},
 {'orig': 'Si coeant, quotquot tam dira insania versat, / Non legio in terris grandior vlla foret.',
  'en': 'If all whom so dire a madness drives were to band together, no legion on earth would be greater.'},
 {'orig': 'Sed tamen inuictae IESV sub nomine turmae / Hoc genus ante alios vimque manusque parat.',
  'en': 'And yet it is against the unconquered squadrons under the name of JESUS that this breed, before all others, readies its force and its hands.'},
 {'orig': 'Quisquis es, insanis frustra conatibus vti / Desine: nam Solem nulla sagitta ferit.',
  'en': 'Whoever you are, cease to spend mad efforts in vain: for no arrow strikes the sun.'},
 {'orig': 'Despicit ex alta vesanos arce furores; / Et ferit auctores missa sagitta suos.',
  'en': 'From its high citadel it looks down on the ravings of the frenzied; and the arrow that was shot strikes those who sent it.'},
])

FABER = units([
 {'img': 'assets/imago/solus-non-sufficit-ignis.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 717: a smith at his forge '
          'works a glowing piece of iron on the anvil, the furnace blazing '
          'behind him.'),
  'orig': 'Ignatius P. Fabrum adhibet ad conuersionem Xauerij. — Solus non sufficit ignis.',
  'en': ("Ignatius employs Father Faber for the conversion of Xavier. — Fire alone "
         "does not suffice. The lemma answers the volume's own most famous line "
         "('one world is not enough'), and the whole epigram turns on a double "
         "sense the engraving keeps visible: faber is the smith at the anvil, and "
         "Faber is Peter Favre — whose journal this apparatus carries — the added "
         "hand by which Ignatius's fire finally forged Xavier."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Arte opus Ignati: solus non sufficit ignis: / Arte opus est: flectes arte, quod igne nequis.',
  'en': 'Art is needed, Ignatius — fire alone does not suffice. Art is needed: by art you will bend what you cannot bend by fire.'},
 {'orig': 'Vidi ego, caelatum clypei cum fingeret orbem, / Non solo ferrum molliit igne faber.',
  'en': 'I once watched a smith shaping the embossed circle of a shield: he softened the iron not by fire alone.'},
 {'orig': 'Non labor vnus erat: pars vrget follibus auras, / Mersaque stridenti temperat aera lacu;',
  'en': 'It was not one labour: one hand drives the air with the bellows and tempers the plunged bronze in the hissing trough;'},
 {'orig': 'Pars massam exercet, pars altera forcipe versat, / Haec duris aptat cotibus, illa terit.',
  'en': 'one works the mass, another turns it with the tongs; this one sets it to the hard whetstones, that one grinds.'},
 {'orig': 'Manabat plenis sudor per corpora riuis: / Vsque adeo multa flectitur arte chalybs.',
  'en': 'Sweat ran down their bodies in full streams: so much art it takes to bend steel.'},
 {'orig': 'Aestuat, & valido flagrat Xauerius igne; / Formari solo non tamen igne valet.',
  'en': 'Xavier seethes and blazes with a strong fire; yet by fire alone he cannot be formed.'},
 {'orig': 'Verum vbi solertis Fabri manus addita, sese / In partem duci quamlibet arte sinit.',
  'en': 'But once the hand of the skilful smith — of Faber — is added, he lets himself be guided by art into any shape whatever.'},
 {'orig': 'Adspice vt immissos exercet spiritus ignes, / Totaque flammato massa recocta foco est.',
  'en': 'See how the blast plies the fires let into him, and the whole mass is forged anew in the flaming hearth.'},
 {'orig': 'Ardentes animos (animus stridoribus ardens / Proditur) iniectae temperat imber aquae.',
  'en': 'A shower of water, thrown on, tempers the burning spirit — for a spirit on fire betrays itself by its hissing.'},
 {'orig': 'Quem gemitum referunt auditi incudibus ictus? / Qua non exhaustus sedulitate labor?',
  'en': 'What a groan the blows give back, heard upon the anvils! What diligence has this labour not spent?'},
 {'orig': 'Mille operum Faber est: nec respirare potestas. / Tantae Xauerium fingere molis erat.',
  'en': 'The Smith is a smith of a thousand tasks, with no leave to draw breath: so great a work was it to fashion Xavier.'},
])

ANIMAS = units([
 {'img': 'assets/imago/da-mihi-animas.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 941: Abraham, returned from '
          'battle with his armed men, faces the crowned king of Sodom over a heap '
          'of captured vessels; the king gestures toward the freed captives.'),
  'orig': 'Missio Castrensis. — Da mihi animas, cetera tolle tibi.',
  'en': ("The mission to the army camps. — Give me the souls, take the rest for "
         "yourself (Genesis 14:21). The Flemish province's emblem for its army "
         "chaplains: Abraham refusing the spoils of Sodom, keeping only the "
         "persons — a verse with a long afterlife as a motto of pastoral care."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Hinc venit Assyria & Babylonis robur in armis; / Inde Gomorrhaei stant Sodomaeque duces.',
  'en': 'From this side come Assyria and the strength of Babylon in arms; on that side stand the captains of Gomorrah and Sodom.'},
 {'orig': 'Insonuere tubae: miscent certamina Reges: / Alterno late sanguine terra madet.',
  'en': 'The trumpets have sounded; the kings join battle; far and wide the earth is soaked with the blood of both.'},
 {'orig': 'Iam Sodomae cecidere Duces; iam vincula passi, / Felices socios qui cecidere vocant.',
  'en': "Now Sodom's captains have fallen; now those who suffer chains call happy the comrades who fell."},
 {'orig': 'Immeritum quoque Lot tristis fortuna coegit / Barbara captiua vincula ferre manu.',
  'en': 'Undeserving Lot too a sad fortune has forced to bear barbarous chains upon his captive hands.'},
 {'orig': 'Non tulit hanc sortem, neque tantum dedecus Abram: / Hoc duce tercentum, stant noua castra, viri.',
  'en': 'Abram did not endure this lot, nor so great a disgrace: under his lead three hundred men stand up, a new camp.'},
 {'orig': 'Vae tibi, vae Babylon, nostra quae clade superbis: / Iam rerum versas experiere vices.',
  'en': 'Woe to you, woe, Babylon, who vaunt yourself upon our ruin: now you shall learn how fortunes turn.'},
 {'orig': 'Assyrij cecidere; Loti iam vincula stringunt / Assyrios; Sodomae reddita praeda Duci est.',
  'en': "The Assyrians have fallen; Lot's chains now bind the Assyrians; the booty of Sodom is restored to its captain."},
 {'orig': 'Victor Abramus ouat: cui Rex: Age, diuide praedas, / Redde animas nobis, cetera tolle tibi.',
  'en': 'Abram triumphs as victor; and to him the king: Come, divide the spoils — give the souls back to us, take the rest for yourself.'},
 {'orig': 'Dicite vos Socij, vos Regia castra secuti, / Quae referet vester praemia digna labor?',
  'en': "Say, you Companions, you who have followed the King's camp: what worthy rewards shall your labour bring home?"},
 {'orig': 'Quo lucro stabit victoria? dicite Regi: / Da nobis animas, cetera tolle tibi.',
  'en': 'At what gain shall the victory stand? Say to the King: give us the souls, take the rest for yourself.'},
 {'orig': 'Praemia non leuium ferimus satis ampla laborum, / Si nostra constet vita aliena salus.',
  'en': "We carry home rewards ample enough for no light labours, if another's salvation is bought at the price of our own life."},
])

NEXUS = units([
 {'img': 'assets/imago/nexus-non-sufficit.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 199: ivy winds up an oak '
          'in an open landscape, its tendrils circling trunk and branches.'),
  'orig': 'Renouatio votorum. — Nexus non sufficit vnus.',
  'en': ("The renewal of vows. — One bond is not enough. The third of the "
         "volume's 'non sufficit' lemmata carried here: one world (E1), one "
         "fire (E5) — and one bond. The ivy on the oak as the yearly renewal "
         "of the vows: love multiplies its own chains."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Nulla quies in amore datur: quis comprimat ignem? / Feruida flamma moras, otia nescit amor.',
  'en': 'No rest is granted in love — who could smother its fire? A glowing flame knows no delays; love knows no idleness.'},
 {'orig': 'Siqua potest cessasse, potest periisse fauilla; / Deses ab extincto proximus ardor erit.',
  'en': 'A spark that can pause can also have died; an idle burning is next neighbour to one put out.'},
 {'orig': 'Pectus amans, triplici quamuis adamante reuinxit, / Haec mage, dum renouat vincula, stringit amor.',
  'en': 'Though love has bound the loving breast with triple adamant, it draws those chains the tighter each time it renews them.'},
 {'orig': 'Vultus alit, flammasque nouas, noua spicula vibrat, / Amplexuque nouo vincula multiplicat.',
  'en': 'It feeds its gaze, brandishes new flames and new darts, and with every new embrace multiplies the bonds.'},
 {'orig': 'Et quoties sacros, sua vota, retractat amores, / Et quoties renouat gaudia, vincla facit.',
  'en': 'And as often as it takes up again its sacred loves — its vows — as often as it renews its joys, it forges chains.'},
 {'orig': 'Sic hederae, iuncta quamuis radice ligantur, / Et trunco teneras applicuere comas;',
  'en': 'So the ivies: though they are tied to it by a joined root, and have laid their tender tresses on the trunk,'},
 {'orig': 'Assurgunt, ramosque nouis complexibus vrgent, / Quaque patet quercus, Bacchica serta gerit:',
  'en': 'they climb, press the branches with new embraces, and wherever the oak spreads it wears the garlands of Bacchus:'},
 {'orig': 'Non hederae, nexus non sufficit vnus amori: / Mille hederae amplexus, mille requirit amor.',
  'en': 'For the ivy — for love — one bond is not enough: the ivy asks a thousand embraces, and love a thousand.'},
])
add(NEXUS, [nl_unit('nexus')])

OMNIBUS = units([
 {'img': 'assets/imago/omnibus-omnia.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 452: a mirror stands in a '
          'tiled room between two herm figures, reflecting the light of a '
          'window.'),
  'orig': 'Societatis operarij. — Omnibus omnia.',
  'en': ("The workers of the Society. — All things to all (1 Corinthians 9:22). "
         "The mirror as the Jesuit worker: it takes on every likeness without "
         "flattery and without deceit — the epigram is a small treatise on the "
         "adaptability Ignatius taught in the instruction for Ireland "
         "(Letter XII) and Xavier practised from Comorin to Japan."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Qualiter in speculo facies, motusque relucent, / Aduersasque refert laeuis imago notas;',
  'en': 'As a face and its motions shine back in a mirror, and the smooth image returns your marks reversed,'},
 {'orig': 'Haud aliter formas hominum se vertit in omnes, / Omnibus vt solers omnia fiat amor:',
  'en': 'just so does love turn itself into all the shapes of men, that, all-skilled, it may become all things to all:'},
 {'orig': 'Castus amor, castis quem mentibus indit IESVS, / Ignati sacro quae prius igne calent:',
  'en': "chaste love, which JESUS plants in chaste minds — minds already glowing with Ignatius's sacred fire."},
 {'orig': 'Omnia diuersae capit hic simulacra figurae, / Omnia compositis reddit imaginibus.',
  'en': 'It takes in every likeness of every different figure, and gives them all back in answering images.'},
 {'orig': 'Nec tamen in similes trahit assentatio mores: / Nec studet occultis ille nocere dolis.',
  'en': 'And yet it is no flattery that draws it into like manners, nor does it seek to harm by hidden wiles.'},
 {'orig': 'Fallere nescit amor, numquam sibi dissidet ipse, / Ingenio similis sit licet vsque tuo.',
  'en': 'Love cannot deceive; it is never at odds with itself, though it grow ever so like your own temper.'},
 {'orig': 'Assumet tecum, tecum sua gaudia ponet, / Cum puero ludet, cum sene tristis erit.',
  'en': 'It will take up your ways with you, and with you lay its joys aside; with the boy it will play, with the old man it will be grave.'},
 {'orig': 'Institor extremis merces accersis ab Indis? / Impiger ignoto littore quaeret opes.',
  'en': 'Are you a trader fetching wares from farthest India? Untiring, it will seek out goods on the unknown shore beside you.'},
 {'orig': 'Si victor redeas, laetos canet ille triumphos: / Tecum per terras, per mare, bella geret.',
  'en': 'If you come home a victor, it will sing your glad triumphs; with you it will wage wars by land and by sea.'},
 {'orig': 'Desertas etiam siluas montesque pererrat / Fidus amor, tamquam barbarus ingenio.',
  'en': 'Faithful love wanders even deserted woods and mountains, as though itself barbarous in temper.'},
 {'orig': 'Nempe vt possit amor similes sibi reddere cunctos, / Dissimilis toties redditur ipse sibi.',
  'en': 'For this — that love may render all men like itself — it is rendered, just as many times, unlike itself.'},
])
add(OMNIBUS, [nl_unit('omnibus')])

TERRA = units([
 {'img': 'assets/imago/tum-te-terra-teget.jpg',
  'alt': ('Emblem engraving, Imago primi saeculi p. 721: an eclipse darkens '
          'the sky over the sea — a dark shrouded form against the stars, the '
          'moon below on the water.'),
  'orig': ('Xauerius, orbe peragrato, moritur in littore Chinarum. — '
           'Tum te terra teget, cum totum impleueris orbem.'),
  'en': ("Xavier, having traversed the world, dies on the shore of China. — "
         "Then only shall earth cover you, when you have filled the whole "
         "world. The emblem answers E1: the boy who held two globes ends at "
         "Sancian, and the epigram reads his death as an eclipse — read it "
         "beside the last letter, FX IV."),
  'label': 'The emblem and its lemma'},
 {'orig': 'Cingite fronde caput: Xauerius orbe laboris / Deficit impleto: cingite fronde caput.',
  'en': 'Wreathe his head with leaves: Xavier fails only when the circuit of his labour is filled — wreathe his head with leaves.'},
 {'orig': 'Amplius ille nihil potuit superaddere coeptis: / Tota peragrata est India, iam satis est.',
  'en': 'He could add nothing more to what he had begun: the whole of India is traversed; now it is enough.'},
 {'orig': 'Chinae, Goa, Iapon, Ternata, Moluca, tot vrbes, / Quae toties initae caussa fuere viae;',
  'en': 'China, Goa, Japan, Ternate, the Moluccas — so many cities that were, so many times, the reason for setting out;'},
 {'orig': 'Totque aliae gentes, tot primo subdita Phoebo / Littora, sudoris plus habuere satis.',
  'en': 'and so many other peoples, so many shores that lie under the morning sun, have had more than their fill of his sweat.'},
 {'orig': 'Ergo vel extremam cum nil superesset ad Eon; / Ipsis terrarum finibus immoritur.',
  'en': 'And so, when nothing remained short of the uttermost East, he dies upon the very ends of the earth.'},
 {'orig': 'Immoritur votis ingentibus, orbe repleto: / Cynthia sic etiam plena perire solet.',
  'en': 'He dies upon his vast desires, the world now filled: so even Cynthia — the moon — is wont to perish at her fullest.'},
 {'orig': 'Cynthia terrarum, caeli Franciscus ab vmbra / Palluit: exanimis vultus, amantis erat.',
  'en': "The moon grows pale in the shadow of the earth; Francis paled in the shadow of heaven — and the lifeless face was a lover's face."},
 {'orig': 'Obruitur tenebris & furua Cynthia nube: / Franciscus radiis obruit astra suis.',
  'en': 'Cynthia is buried in darkness and a dusky cloud: Francis buries the stars beneath rays of his own.'},
 {'orig': 'Non iubar hoc magicae carmen tenuauerit artis: / Nil opus ad numeros aera repulsa sonent:',
  'en': 'No spell of magic art shall thin this radiance; no need for the beaten bronze to clash out its rescuing rhythms:'},
 {'orig': 'Perstat, & integros vbi vita reliquerit artus, / Maius ab extincto corpore lumen erit.',
  'en': 'It stands fast; and when life has left the limbs — left them whole — the light from the extinguished body will be the greater.'},
])
add(TERRA, [nl_unit('terra')])

# Dutch mirrors for the six emblems already shipped
add(ALITEM, [nl_unit('alitem')])
add(ORBIS, [nl_unit('orbis')])
add(MONSTRAT, [nl_unit('monstrat')])
add(SAGITTA, [nl_unit('sagitta')])
add(FABER, [nl_unit('faber'),
 {'orig': ('Den hamer en het vier, die moeten samen wercken, / '
           'En met eenpaerigh hulp malckanderen verstercken: / '
           "'t Een maeckt het ijser heet, en 't ander gheeft den slagh, / "
           'Soo krijght het een nieuw vorm dat inden oven lagh. / '
           'VVant schoon den gauwen knecht den blaesbalgh treckt met lusten, / '
           'En dat den meester self de kolen niet laet rusten, / '
           'Maer meer en meer onsteeckt den ouergrooten brandt, / '
           'Komt daer gheen slagh omtrent, het ijser houdt sijn standt.'),
  'en': ("Poirters's first stanza, translated: 'The hammer and the fire must "
         "work together, and with united help strengthen one another: the one "
         "makes the iron hot, the other gives the blow — so what lay in the "
         "furnace receives a new form. For though the quick apprentice pulls "
         "the bellows with a will, and the master himself lets the coals take "
         "no rest but kindles the great blaze more and more: if no blow comes "
         "near it, the iron keeps its old shape.' The stanza continues on the "
         "next page of the print."),
  'label': "Poirters's Dutch verse, first stanza (p. 508)"}])
add(ANIMAS, [nl_unit('animas')])

out = {
 'id': 'imago',
 'autor': 'Imago primi saeculi Societatis Iesu',
 'titel': 'Imago primi saeculi — the centenary emblem book (the title and one emblem from each book)',
 'jahr': 1640,
 'lang': 'la',
 'zitierweise': 'Imago T / E1–E6 [k]',
 'quelle': ("Antwerp: ex officina Plantiniana Balthasaris Moreti, 1640; images "
            "rendered from the Internet Archive scan imagoprimisaecul00boll "
            "(public domain), plates cropped from the page images. Latin "
            "transcribed by eye from the same pages (long s and the ae ligature "
            "normalised, u/v as printed); English: this site's unofficial working "
            "translations (CC0). The Dutch mirror pages come from the vernacular "
            "counterpart issued by the same press in the same year, the "
            "Af-Beeldinghe van d'eerste eeuwe der Societeyt Iesu, with Dutch "
            "verses by Adriaen Poirters SJ (Internet Archive "
            "afbeeldinghevand00boll, public domain); headings and rhymed glosses "
            "transcribed by eye."),
 'hinweis': ("The iconographic path of the apparatus — unlike Calculemus, this "
             "corpus can carry images, and here it does: the engraved title and "
             "nine emblems of the 1640 centenary volume — one from each of the "
             "six books, plus three deepenings — each with its lemma, its "
             "epigram distich by distich, and a working translation, and each "
             "closed by its Dutch mirror: the same plate in the Af-Beeldinghe "
             "of the same year, with Poirters's rhymed vernacular gloss. The "
             "Latin volume holds over 120 emblems in all; this selection is a "
             "spine, not a survey, and each emblem was chosen for what it "
             "touches elsewhere in the corpus. Not part of the concordance "
             "index."),
 'sections': [
  {'id': 'title', 'zk': 'Imago T',
   'titel': 'The engraved title (1640)',
   'blurb': 'The Society enthroned under the IHS, with the six books of her first century in medallions around her.',
   'units': FRONT},
  {'id': 'alitem', 'zk': 'Imago E2',
   'titel': 'Book I · Nouum mutor in alitem — The renewal of the spirit (p. 200)',
   'blurb': ('The silkworm emblem, from Societas nascens: Horace’s metamorphosis '
             'turned to the renovation of vows — enclosure not as prison but as '
             'the workshop of wings.'),
   'units': ALITEM},
  {'id': 'nexus', 'zk': 'Imago E7',
   'titel': 'Book I · Nexus non sufficit vnus — One bond is not enough (p. 199)',
   'blurb': ('The ivy on the oak, the silkworm’s neighbour on the facing page: '
             'the renewal of vows as love multiplying its own chains — and the '
             'third of the volume’s “non sufficit” lemmata carried here.'),
   'units': NEXUS},
  {'id': 'orbis', 'zk': 'Imago E1',
   'titel': 'Book II · Vnus non sufficit orbis — One world is not enough (p. 326)',
   'blurb': ('The emblem of the Indian missions, from Societas crescens: the boy '
             'with two globes, against Alexander who halted at the Ganges. The '
             'most quoted — and most mocked — line of the whole volume.'),
   'units': ORBIS},
  {'id': 'omnibus', 'zk': 'Imago E8',
   'titel': 'Book III · Omnibus omnia — All things to all (p. 452)',
   'blurb': ('The mirror emblem, from Societas agens: 1 Corinthians 9:22 as the '
             'workers’ motto — adaptation without flattery, likeness without '
             'deceit. Ignatius’s rules of dealing (Letter XII), drawn.'),
   'units': OMNIBUS},
  {'id': 'monstrat', 'zk': 'Imago E3',
   'titel': 'Book III · Hac monstrat eundum — The book that shows the way (p. 459)',
   'blurb': ('From Societas agens: the little book of the Exercises as the surest '
             'guide for the choice of a state of life — a wayside Mercury for the '
             'election, surer than Ariadne’s thread or the Pharos.'),
   'units': MONSTRAT},
  {'id': 'sagitta', 'zk': 'Imago E4',
   'titel': 'Book IV · Solem nulla sagitta ferit — No arrow strikes the sun (p. 565)',
   'blurb': ('From Societas patiens: fools shooting arrows at the sun — the '
             'Society’s answer to its attackers, printed while the Monita secreta '
             'and the pamphlets circulated. The counter-voices, seen from inside.'),
   'units': SAGITTA},
  {'id': 'faber', 'zk': 'Imago E5',
   'titel': 'Book V · Solus non sufficit ignis — The forging of Xavier (p. 717)',
   'blurb': ('From Societas honorata: Ignatius as smith, Xavier as the iron, and '
             'Peter Favre — faber, the smith’s own name — as the added hand. '
             'Three works of this corpus in one engraving.'),
   'units': FABER},
  {'id': 'terra', 'zk': 'Imago E9',
   'titel': 'Book V · Tum te terra teget — The death of Xavier as an eclipse (p. 721)',
   'blurb': ('The answer to E1, four hundred pages on: the boy who held two '
             'globes dies at the gate of China, and the epigram reads his death '
             'as the eclipse of a full moon. Beside it belongs the last letter, '
             'FX IV.'),
   'units': TERRA},
  {'id': 'animas', 'zk': 'Imago E6',
   'titel': 'Book VI · Da mihi animas, cetera tolle tibi — The army mission (p. 941)',
   'blurb': ('From the Flemish province’s own book: Abraham refusing the spoils '
             'of Sodom and keeping only the persons — Genesis 14:21 as the emblem '
             'of the camp chaplains.'),
   'units': ANIMAS},
 ],
}

path = os.path.join(REPO, 'data', 'imago.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', sum(len(s['units']) for s in out['sections']), 'units')
