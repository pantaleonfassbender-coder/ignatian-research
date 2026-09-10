# -*- coding: utf-8 -*-
# Build data/imago.json — Imago primi saeculi Societatis Iesu (Antwerp:
# Plantin press of Balthasar Moretus, 1640), the Society's centenary volume:
# the iconographic pilot of this apparatus.
#
# Images: rendered from the Internet Archive scan imagoprimisaecul00boll
# (public domain), PDF leaves 8 (engraved title), 213 (printed p. 200) and
# 339 (printed p. 326), cropped to the plates; files in assets/imago/.
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

out = {
 'id': 'imago',
 'autor': 'Imago primi saeculi Societatis Iesu',
 'titel': 'Imago primi saeculi — the centenary emblem book (pilot: two emblems and the title)',
 'jahr': 1640,
 'lang': 'la',
 'zitierweise': 'Imago T / E1 / E2 [k]',
 'quelle': ("Antwerp: ex officina Plantiniana Balthasaris Moreti, 1640; images "
            "rendered from the Internet Archive scan imagoprimisaecul00boll "
            "(public domain), plates cropped from the page images. Latin "
            "transcribed by eye from the same pages (long s and the ae ligature "
            "normalised, u/v as printed); English: this site's unofficial working "
            "translations (CC0)."),
 'hinweis': ("The iconographic pilot of the apparatus — unlike Calculemus, this "
             "corpus can carry images, and here it begins to: the engraved title "
             "and two emblems of the 1640 centenary volume, each with its lemma, "
             "its epigram distich by distich, and a working translation. The "
             "full volume runs to over 950 pages and 126 emblems; whether and "
             "how far this path is extended is stated in the coda, not implied. "
             "Not part of the concordance index."),
 'sections': [
  {'id': 'title', 'zk': 'Imago T',
   'titel': 'The engraved title (1640)',
   'blurb': 'The Society enthroned under the IHS, with the six books of her first century in medallions around her.',
   'units': FRONT},
  {'id': 'orbis', 'zk': 'Imago E1',
   'titel': 'Vnus non sufficit orbis — One world is not enough (p. 326)',
   'blurb': ('The emblem of the Indian missions, from Book II (Societas crescens): '
             'the boy with two globes, against Alexander who halted at the Ganges. '
             'The most quoted — and most mocked — line of the whole volume.'),
   'units': ORBIS},
  {'id': 'alitem', 'zk': 'Imago E2',
   'titel': 'Nouum mutor in alitem — The renewal of the spirit (p. 200)',
   'blurb': ('The silkworm emblem, from Book I (Societas nascens): Horace’s '
             'metamorphosis turned to the renovation of vows — enclosure not as '
             'prison but as the workshop of wings.'),
   'units': ALITEM},
 ],
}

path = os.path.join(REPO, 'data', 'imago.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', sum(len(s['units']) for s in out['sections']), 'units')
