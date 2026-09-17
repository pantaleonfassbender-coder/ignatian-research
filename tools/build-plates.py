# -*- coding: utf-8 -*-
# Build assets/plates/ and data/plates.json — one public-domain plate per
# work or module where a suitable image exists: title pages, frontispieces
# and facsimile pages, mostly from the very digitisations the editions
# cite, fetched page by page over IIIF (no full scans are downloaded or
# carried). Two plates reuse images already in the repository (the Imago
# engraved title, a Trutznachtigall facsimile page). Faithful reproduction
# of a public-domain two-dimensional work adds nothing licensable; every
# plate names its source, digitisation and leaf below.
#
# First tranche: fourteen. Named for later tranches: Suárez (the Vivès
# vol. III title — the Archive collection item serves IIIF only for its
# primary volume; render from the volume PDF instead), Ricci (the 1615
# Augsburg scan dechristianaexpe00ricc carries no usable title page — its
# dedication to Paul V, leaf 9, is the fallback), Pascal (the module's
# text source is a Gutenberg transcription; an early Provinciales printing
# would first have to be sighted), and the locked core works (Testament,
# Diary, Constitutions — plates from the early prints are possible but
# were not hunted). The 1893/1919 apparatus volumes (Institutum, Monumenta
# Ignatiana, O'Leary, Thwaites series pages) add little as images and are
# left without plates, except where the volume itself contributes a
# document (the Thwaites vol. XXXIV title).
#
# Usage: python tools/build-plates.py          (needs the network)
import io, json, os, urllib.request
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'assets', 'plates')
os.makedirs(OUT, exist_ok=True)

def ia(item, leaf, w=1400):
    return f"https://iiif.archive.org/iiif/{item}${leaf}/full/{w},/0/default.jpg"

PLATES = [
 { 'id': 'spex',
   'url': ia('bub_gb_eyZ68wmgWoIC', 8),
   'caption': "The editio princeps: Exercitia spiritualia, Rome 1548 — "
              "the Vulgata's title page with the IHS device, the year "
              "Paul III approved the book.",
   'credit': "Exercitia spiritualia (Rome: Antonio Blado, 1548). Internet "
             "Archive bub_gb_eyZ68wmgWoIC, leaf 8. Public domain." },
 { 'id': 'fabri',
   'url': ia('memorialebeatipe0000sign', 9),
   'caption': "Title page of the editio princeps of the Memoriale, Paris "
              "1873 — the printing this edition is made from.",
   'credit': "Memoriale Beati Petri Fabri, ed. Marcel Bouix, S.J. (Paris: "
             "Albanel, 1873). Internet Archive memorialebeatipe0000sign, "
             "leaf 9. Public domain." },
 { 'id': 'ratio',
   'url': ia('bub_gb_6mcuvbXlgXEC', 0),
   'caption': "The Ratio's engraved title in the Roman printing of 1606 — "
              "Ignatius above the rulebook of the schools.",
   'credit': "Ratio atque institutio studiorum Societatis Iesu (Rome: in "
             "Collegio Romano, 1606; the definitive text of 1599). "
             "Internet Archive bub_gb_6mcuvbXlgXEC, leaf 0. Public "
             "domain. The module's text follows the Florence printing of "
             "1893." },
 { 'id': 'conimbricenses',
   'url': ia('commentariicolle00col', 5),
   'caption': "Title page of the 1617 printing of the Coimbra De anima "
              "commentary — the very printing this edition was "
              "transcribed from.",
   'credit': "Commentarii Collegii Conimbricensis, in tres libros De "
             "anima (1617). Internet Archive commentariicolle00col, leaf "
             "5. Public domain." },
 { 'id': 'rodriguez',
   'url': ia('PracticeOfChristianAndReligiousPerfectionV1', 5),
   'caption': "Title page of the Dublin printing of 1861 — the anonymous "
              "English this edition carries.",
   'credit': "Rodríguez, The Practice of Christian and Religious "
             "Perfection, vol. I (Dublin: James Duffy, 1861). Internet "
             "Archive PracticeOfChristianAndReligiousPerfectionV1, leaf "
             "5. Public domain." },
 { 'id': 'caussade',
   'url': ia('abandonmentorabs00caus', 5),
   'caption': "Title page of McMahon's English of 1887 — Ramière's "
              "arrangement, as this edition carries it.",
   'credit': "Abandonment; or, Absolute Surrender to Divine Providence "
             "(New York: Benziger, 1887). Internet Archive "
             "abandonmentorabs00caus, leaf 5. Public domain." },
 { 'id': 'xavier',
   'url': ia('lifelettersofstf01cole', 7),
   'caption': "Title page of Coleridge's Life and Letters, vol. I — the "
              "biography that carries the letters complete.",
   'credit': "H. J. Coleridge, S.J., The Life and Letters of St. Francis "
             "Xavier, vol. I (London: Burns and Oates; first published "
             "1872). Internet Archive lifelettersofstf01cole, leaf 7. "
             "Public domain." },
 { 'id': 'acosta',
   'url': ia('naturalmoralhist01acos', 11),
   'caption': "Title page of the Hakluyt Society printing of Grimston's "
              "1604 English — the text this edition carries.",
   'credit': "Acosta, The Natural and Moral History of the Indies, ed. "
             "Markham (London: Hakluyt Society, 1880). Internet Archive "
             "naturalmoralhist01acos, leaf 11. Public domain." },
 { 'id': 'relations',
   'url': ia('jesuits34jesuuoft', 9),
   'caption': "Title page of Thwaites's vol. XXXIV — Lower Canada and "
              "the Hurons, 1649: the volume of St-Ignace and the "
              "martyrdoms this edition selects from.",
   'credit': "The Jesuit Relations and Allied Documents, vol. XXXIV "
             "(Cleveland: Burrows, 1898). Internet Archive "
             "jesuits34jesuuoft, leaf 9. Public domain." },
 { 'id': 'spee_cautio',
   'url': ia('per_witchcraft-in-europe-and-america_spee-friedrich-von_1631_911', 0),
   'caption': "Title page of the first printing, Rinteln 1631 — the book "
              "published without Spee's name, transcribed here by eye "
              "from this copy.",
   'credit': "Cautio Criminalis, seu de processibus contra sagas liber "
             "(Rinteln: Petrus Lucius, 1631). Internet Archive "
             "per_witchcraft-...-1631_911, leaf 0. Public domain." },
 { 'id': 'monita',
   'url': ia('instructiosecret00browrich', 6),
   'caption': "The hostile edition wears its colours: the frontispiece "
              "“A Jesuit” of Brownlee's New York printing of "
              "1857 — the forgery's polemical afterlife, made visible in "
              "the very edition whose facing texts this module carries.",
   'credit': "Secreta Monita Societatis Jesu / The Secret Instructions "
             "of the Jesuits, ed. W. C. Brownlee (New York, 1857), "
             "frontispiece. Internet Archive instructiosecret00browrich, "
             "leaf 6. Public domain." },
 { 'id': 'dominus',
   'url': ia('sanctissimidomin00cath_5', 1),
   'caption': "Title page of the Lisbon printing of 1773, Latin and "
              "Portuguese — the brief of suppression as it reached the "
              "kingdoms.",
   'credit': "Breve do Santissimo Padre Clemente XIV (Lisbon, 1773). "
             "Internet Archive sanctissimidomin00cath_5, leaf 1. Public "
             "domain." },
 { 'id': 'imago',
   'file': 'assets/imago/frontispiece.jpg',
   'caption': "The engraved title of the Imago primi saeculi, Antwerp "
              "1640 — the Society's self-portrait at its centenary.",
   'credit': "Imago primi saeculi Societatis Iesu (Antwerp: Plantin "
             "press of Balthasar Moretus, 1640). Internet Archive "
             "imagoprimisaecul00boll; the same image opens the module's "
             "reader. Public domain." },
 { 'id': 'spee_trutz',
   'file': 'assets/spee/trutz-oelberg-p170.jpg',
   'caption': "A page of “Bey stiller Nacht” in the Cologne "
              "printing of 1654 — the facsimile the module's reader "
              "carries beside the transcription.",
   'credit': "Trutznachtigall (Cologne, 1654). Internet Archive "
             "trutz-nachtigall-oder-geistlichs-poetisc; the same image "
             "appears in the module's reader. Public domain." },
]

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':
        'ignatiana-plates (ignatian-research.netlify.app)'})
    for attempt in range(4):
        try:
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as e:
            err = e
    raise err

reg = {}
for p in PLATES:
    if p.get('file'):
        im = Image.open(os.path.join(REPO, p['file'])).convert('RGB')
    else:
        im = Image.open(io.BytesIO(fetch(p['url']))).convert('RGB')
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, p['id'] + '.jpg'), quality=82, optimize=True)
    th = im.copy(); th.thumbnail((300, 480), Image.LANCZOS)
    th.save(os.path.join(OUT, p['id'] + '_t.jpg'), quality=80, optimize=True)
    reg[p['id']] = {'caption': p['caption'], 'credit': p['credit']}
    print('plate', p['id'], im.size)

path = os.path.join(REPO, 'data', 'plates.json')
json.dump(reg, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', len(reg), 'plates')
