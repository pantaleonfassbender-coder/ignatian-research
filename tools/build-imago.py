# -*- coding: utf-8 -*-
# Build data/imago.json — Imago primi saeculi Societatis Iesu (Antwerp:
# Plantin press of Balthasar Moretus, 1640), the Society's centenary volume:
# the iconographic pilot of this apparatus.
#
# Images: rendered from the Internet Archive scan imagoprimisaecul00boll
# (public domain), cropped to the plates; files in assets/imago/. PDF leaves
# (printed pages): 8 (engraved title), 213 (200), 339 (326), 472 (459),
# 578 (565), 730 (717), 954 (941). The emblem runs sit at the end of each
# book (PDF leaves 185-217, 330-343, 465-493, 574-594, 726-740, 950-965).
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
            "translations (CC0)."),
 'hinweis': ("The iconographic path of the apparatus — unlike Calculemus, this "
             "corpus can carry images, and here it does: the engraved title and "
             "one emblem from each of the six books of the 1640 centenary "
             "volume, each with its lemma, its epigram distich by distich, and "
             "a working translation. The volume holds over 120 emblems in all; "
             "this selection is a spine, not a survey, and each emblem was "
             "chosen for what it touches elsewhere in the corpus. Not part of "
             "the concordance index."),
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
  {'id': 'orbis', 'zk': 'Imago E1',
   'titel': 'Book II · Vnus non sufficit orbis — One world is not enough (p. 326)',
   'blurb': ('The emblem of the Indian missions, from Societas crescens: the boy '
             'with two globes, against Alexander who halted at the Ganges. The '
             'most quoted — and most mocked — line of the whole volume.'),
   'units': ORBIS},
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
