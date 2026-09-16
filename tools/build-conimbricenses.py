# -*- coding: utf-8 -*-
# Build data/conimbricenses.json — the Prooemium of the Coimbra Jesuits'
# commentary on Aristotle's De anima, complete and bilingual.
#
# Latin: transcribed BY EYE from the page images of the 1617 printing,
# Commentarii Collegii Conimbricensis Societatis Iesu, in tres libros De
# anima Aristotelis (Internet Archive commentariicolle00col; PDF leaves
# 12-14 = the printing's columns 2-7). The OCR of the early-modern type
# served only for navigation. Long s and ligatures are normalised, the
# printer's abbreviations silently expanded, u/v kept as printed; the
# marginal captions and source references of the printing are not carried.
# The paragraph numbers are this site's own — the print sets the Prooemium
# as a continuous treatise.
#
# The Prooemium answers the question the whole doctrine-of-the-soul strand
# turns on: what, at the threshold of modernity, the science of the soul
# is — its utility (the Delphic nosce te ipsum), its place in philosophy
# (the soul as horizon aeternitatis et temporis), its literature, its
# position in the physics course (as the Ratio's rules prescribe it), the
# disputed subject of the three books, and their partition — with the
# internal senses signposted to book III, where this apparatus's next
# Coimbra module is to follow.
#
# English: unofficial machine-generated working translation made for this
# site directly from the Latin (CC0). It carries no authority — cite the
# Latin.
#
# Usage: python tools/build-conimbricenses.py
import io, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

U = []
def u(la, en):
    U.append({'n': len(U) + 1, 'k': len(U) + 1, 'en': en, 'orig': la})

u("Quantum scientia de anima, ob certitudinem demonstrandi, & rerum, in quibus "
  "versatur, nobilitatem, inter alias Philosophiae partes emineat: quam sit tum ad "
  "vitam probe instituendam, & moderandam; tum ad omnem veritatis cognitionem "
  "vtilis; ex iis, quae Aristoteles mox docebit, conspicuum fiet. Sed idem, "
  "praesertim quod ad vtilitatem spectat, suaderi amplius, illustrarique ex eo "
  "potest, quia vt celebris illa siue Chilonis, siue Phemonoae, aut Thaletis, vel "
  "quicunque eius auctor fuerit, sententia foribus templi Delphici ab "
  "Amphictyonibus inscripta commonebat, maxime eniti quisque debet, vt se ipsum "
  "norit: nosse autem se nemo potest nisi animi sui naturam, & dignitatem "
  "perspectam habeat. Quin vero, vt M. Tullius lib. 1. Tuscul. quaest. & Plotinus "
  "lib. 3. Enneadis 4. cap. 1. post Platonem in Alcibiade censuerunt, non aliud "
  "Delphica illa inscriptio hortabatur, quam vt animi naturam cognosceremus.",
  "How much the science of the soul stands out among the other parts of "
  "philosophy, for the certainty of its demonstration and the nobility of the "
  "things with which it deals — how useful it is both for founding and governing "
  "life rightly, and for every knowledge of the truth — will become evident from "
  "what Aristotle is about to teach. But the same, especially as regards its "
  "utility, can be further urged and illustrated by this: as that celebrated "
  "saying — whether of Chilon, or of Phemonoe, or of Thales, or whoever its "
  "author was — inscribed by the Amphictyons on the doors of the Delphic temple "
  "admonished, each must strive above all to know himself: and no one can know "
  "himself unless he has looked into the nature and dignity of his own soul. "
  "Indeed, as Cicero in the first book of the Tusculans and Plotinus in Ennead "
  "IV, book 3, chapter 1, judged after Plato in the Alcibiades, that Delphic "
  "inscription urged nothing else than that we should come to know the nature of "
  "the soul.")

u("Videlicet quia quisquis mentis suae vim, & excellentiam spectandam sibi "
  "exhibuerit, intelliget non esse in his fluxis & caducis bonis immorandum; sed "
  "sempiterna, & diuina omni studio, & contentione quaerenda: in quo praecipua "
  "veri, & legitimi Philosophi ornamenta consistunt.",
  "Namely because whoever sets before himself the power and excellence of his "
  "own mind to contemplate will understand that one must not linger among these "
  "fleeting and perishable goods, but seek the everlasting and divine with all "
  "zeal and effort: in which the chief ornaments of the true and legitimate "
  "philosopher consist.")

u("Est item doctrina haec magno vsui iis, qui de communi vita & moribus "
  "disceptant, vt constat ex libro 1. Ethic. cap. 13. & ex lib. 6. cap. 1. "
  "Etenim oportet eos à Naturali accipere, quo pacto ratio summam animae arcem "
  "teneat, vt inde appetendi & irascendi vim sibi subiiciat, & insurgentes motus "
  "ad certam normam moderetur. Oportet etiam principium actionum, in quibus "
  "humanae vitae felicitas sita est; itemque partitionem facultatum, qua ad "
  "affectus & virtutes explicandas vtuntur, ab eodem mutuari.",
  "This doctrine is likewise of great use to those who treat of common life and "
  "morals, as is clear from the first book of the Ethics, chapter 13, and from "
  "book 6, chapter 1. For they must receive from the natural philosopher how "
  "reason holds the highest citadel of the soul, so that from there it may "
  "subject to itself the powers of desiring and of being angered, and moderate "
  "the rising motions to a fixed norm. They must also borrow from the same the "
  "principle of the actions in which the happiness of human life is placed, and "
  "likewise the partition of the faculties which they use to explain the "
  "affections and the virtues.")

u("Huc pertinet illa Aristotelis commonitio in extremo capite libri 1. Ethic. "
  "sicuti Medici, qui remedia curandis corporibus adhibent, vt munere suo probe "
  "fungantur, in animorum cognitione multum operae collocant: ita ac multo "
  "potiori ratione Philosopho ciuili, qui sanandis animi morbis studet, comperta "
  "esse debere, quae ad animi scientiam spectant.",
  "To this belongs Aristotle's admonition in the last chapter of the first book "
  "of the Ethics: as physicians who apply remedies to the curing of bodies, in "
  "order to discharge their office rightly, spend much labor on the knowledge of "
  "souls, so — and with much better reason — the civil philosopher, who is "
  "intent on healing the diseases of the soul, ought to have ascertained what "
  "pertains to the science of the soul.")

u("Ad primam vero Philosophiam mirifice confert, quatenus ab intellectu nostro "
  "ad substantias intelligibiles, & à materia absolutas per analogiam quandam, "
  "similitudinemque prouehimur, & humana mens se supra se conuertens, à se ipsa "
  "ad diuinam naturam, à qua profecta est, reuocatur, & quicquid ipsa "
  "perfectionis habet, in Deo omnium perfectionum fonte inuenit, meliori tamen "
  "nota, omnique imperfectione sublata.",
  "To first philosophy it contributes wonderfully, insofar as from our own "
  "intellect we are carried forward, by a certain analogy and likeness, to the "
  "intelligible substances free of matter; and the human mind, turning itself "
  "above itself, is called back from itself to the divine nature from which it "
  "came forth, and whatever of perfection it has itself, it finds in God, the "
  "fountain of all perfections — but under a better mark, and with every "
  "imperfection taken away.")

u("Denique communi ratione, ad omnem Philosophiae partem opportuna est haec de "
  "animo meditatio; quia cum animus rationis consiliique particeps (vt "
  "Trismegistus in Asclepio ait) sit veluti horizon aeternitatis, & temporis, "
  "atque intelligibilis, corporeaeque naturae nexus, ac confinium: vel, vti alii "
  "dixere, totius mundi summa: siquidem natura media extremas repraesentat, "
  "superiorem vt imago, inferiorem vt exemplar: fit vt animi doctrina veluti "
  "quoddam rerum diuinarum & humanarum scientiae compendium existat, nosque ad "
  "omnem aliam veritatis notionem praeparet.",
  "Finally, on a general account this meditation on the soul is opportune for "
  "every part of philosophy; because since the soul, partaker of reason and "
  "counsel, is (as Trismegistus says in the Asclepius) as it were the horizon of "
  "eternity and of time, and the bond and border of the intelligible and the "
  "corporeal nature — or, as others have said, the sum of the whole world, since "
  "as a middle nature it represents the extremes, the higher as an image, the "
  "lower as an exemplar — it comes about that the doctrine of the soul stands as "
  "a kind of compendium of the science of things divine and human, and prepares "
  "us for every other notion of the truth.")

u("Ostendit quoque vberem huiusce contemplationis fructum, id quod D. "
  "Augustinus 2. de ordine, cap. 8. asserit; nimirum duas esse praecipuas in "
  "Philosophia quaestiones; vnam de anima, alteram de Deo. Primam efficere, vt "
  "nos ipsos nouerimus; alteram, vt originem nostram; illam nobis dulciorem, "
  "hanc chariorem esse: illam nos dignos beata vita; hanc beatos reddere.",
  "The rich fruit of this contemplation is shown too by what St. Augustine "
  "asserts in the second book On Order, chapter 8: namely that there are two "
  "chief questions in philosophy, one concerning the soul, the other concerning "
  "God. The first brings it about that we know ourselves; the other, that we "
  "know our origin. The former is the sweeter to us, the latter the dearer: the "
  "former makes us worthy of the blessed life, the latter makes us blessed.")

u("Certe animi considerationem magni esse momenti satis ostendunt tam Patrum, "
  "quam externorum etiam Philosophorum ea de re scripta. Nam D. Dionysius cap. "
  "de Diuinis nominibus de anima scripsisse se meminit; D. Iustinus Philosophus "
  "& martyr eiusdem argumenti librum edidit, vt refert D. Hieronymus in libro de "
  "Scriptoribus Ecclesiasticis; D. Augustinus librum vnum composuit de "
  "Immortalitate animae, alterum de Animae quantitate; quatuor de Anima & eius "
  "origine. D. Gregorius Nyssenus satis longam disputationem à se cum sorore "
  "Macrina de Anima & resurrectione habitam literis commendauit. Tertullianus "
  "vnum de Anima librum condidit. Iam vero Ethnici auctores multa de eadem "
  "conscripsere, Trismegistus, Plato, Theophrastus, Plotinus, Chalcidius, "
  "Proclus, Iamblichus, Tullius, auctor operis de Sapientia secundum Aegyptios. "
  "Aristoteles etiam praeter hos tres libros alium reliquit de Animae "
  "quaestionibus, sed iniuria temporis intercidit.",
  "That the consideration of the soul is of great moment is shown well enough "
  "by the writings on this matter of the Fathers as well as of the philosophers "
  "outside. For St. Dionysius records that he wrote of the soul in the chapter "
  "of the Divine Names; St. Justin, philosopher and martyr, published a book of "
  "the same argument, as St. Jerome reports in his book On Ecclesiastical "
  "Writers; St. Augustine composed one book On the Immortality of the Soul, "
  "another On the Quantity of the Soul, and four On the Soul and its Origin. St. "
  "Gregory of Nyssa committed to letters a rather long disputation on the soul "
  "and the resurrection held between himself and his sister Macrina. Tertullian "
  "produced one book On the Soul. And indeed the pagan authors wrote much on "
  "the same — Trismegistus, Plato, Theophrastus, Plotinus, Chalcidius, Proclus, "
  "Iamblichus, Cicero, the author of the work On Wisdom according to the "
  "Egyptians. Aristotle too, besides these three books, left another on "
  "questions of the soul, but it perished by the injury of time.")

u("Porro autem quanto studio hoc opus ab Aristotele elaboratum, perfectumque "
  "sit, testatur ad eius prooemium Themistius hisce verbis: Cum pleraque omnia "
  "Aristotelis scripta, eiusmodi habeantur, vt demirari praestantiam eius facile "
  "suppetat; nulla profecto commentatio est, in qua ille perinde ingenii sui vim "
  "& sublimitatem ostenderit, atque in ea, quae rationem animae continet: siue "
  "enim multitudinem quaestionum, siue copiam rerum pulcherrimarum, siue "
  "doctrinae subtilitatem quaeras; eiusmodi sunt libri de Anima; vt vni homini "
  "omnia, quae ad hoc genus pertinent, in numerato fuisse, constitisseque "
  "videantur.",
  "Moreover, with how much study this work was elaborated and perfected by "
  "Aristotle, Themistius testifies at its proem in these words: Though nearly "
  "all the writings of Aristotle are held to be such that occasion to marvel at "
  "his excellence comes easily, there is surely no treatise in which he has so "
  "shown the power and sublimity of his genius as in the one that contains the "
  "account of the soul: for whether you seek the multitude of questions, or the "
  "abundance of most beautiful matters, or the subtlety of the doctrine, such "
  "are the books On the Soul that everything belonging to this kind seems to "
  "have been at one man's command, and settled by him.")

u("Illud vero hoc loco in primis disquirendum occurrit, quod dissidentium "
  "interpretum opinionibus agitatur; videlicet quem haec scientia inter caeteras "
  "Physiologiae partes, doctrinae methodo, atque ordine, locum vendicet. Sed, "
  "longiori disputatione omissa, statuendum est cum Theophrasto apud Themistium "
  "lib. 3. huius operis, cap. 39. suae paraphrasis, & D. Thoma, quem "
  "recentiores fere sequuntur, eam proxime sequi post libros Meteororum; itaque "
  "antecedere totam disciplinam ad res animatas pertinentem. Namque vt D. "
  "Thomas & Theophilus in prooemio huiusce operis animaduertunt, sicuti "
  "Physiologiae totius exordium est Physica Auscultatio; quia vniuersam "
  "Naturalium principiorum explicationem continet: ita congruebat vt initium "
  "commentationum de rebus animatis, esset consideratio animae, quae rerum "
  "animatarum commune principium est.",
  "But here there first occurs a point to be examined, which is agitated by the "
  "opinions of disagreeing interpreters: namely what place this science claims "
  "among the other parts of natural philosophy in the method and order of "
  "teaching. Setting longer disputation aside, it must be settled, with "
  "Theophrastus as reported by Themistius in book 3, chapter 39, of his "
  "paraphrase of this work, and with St. Thomas, whom the more recent writers "
  "generally follow, that it comes next after the books of the Meteorology, and "
  "thus precedes the whole discipline that concerns animate things. For as St. "
  "Thomas and Theophilus observe in the proem of this work, just as the "
  "beginning of all natural philosophy is the Physics, because it contains the "
  "explanation of the universal principles of natural things, so it was fitting "
  "that the beginning of the treatises on animate things should be the "
  "consideration of the soul, which is the common principle of animate things.")

u("Alexander tamen Aphrodisiensis in suo primo de Anima, & Auerroes 4. "
  "Meteororum priorem fecere tractationem de animalium partibus. Primum, quia "
  "contemplatio materiae antecedit contemplationem formae; partes vero, siue "
  "organa, sunt materia, subiectumve animae. Secundo, quia anima definitur per "
  "corpus organicum: quare ne definitio ex ignotis progrediatur, oportuit "
  "declaratum id prius ab Aristotele fuisse. Haec tamen argumenta non "
  "concludunt. Nam esto partes organicae animalium, de quibus Aristoteles in "
  "libro de Partibus animalium disserit, habeant sese ex parte materiae, "
  "quatenus corporeas functiones animae in se recipiunt: dispositionesque "
  "necessariae sunt ad introductionem animae, vt suo loco exponemus. Licet item "
  "partes organicae facilius cognoscantur, quam anima, cuius natura abdita est, "
  "& recondita, non proinde tamen de iis prius agendum fuit, sed de anima "
  "potius; quia vt paulo ante significauimus, monetque Aristoteles 1. capite "
  "libri 1. Physic. & capite 1. & 3. lib. 1. de Partib. animalium, post "
  "Platonem in Phaedro, & Hippocratem in lib. de Natura humana, in omni bene "
  "instituta disciplina, ea tractanda prius sunt, quae patent latius, ac magis "
  "communia habentur, ne eadem saepius repetere cogamur: anima vero latius "
  "patet, quam partes animalium, cum hae animantibus duntaxat, illa omnibus "
  "insit viuentibus. Nec materiae consideratio contemplationem formae praeit, "
  "si aliud doctrinae ratio postulet; anima vero non per corpus organicum "
  "animalis, sed per corpus organicum viuentis in commune definitur. Quod ante "
  "doctrinam de anima declarari ab Aristotele haud necesse fuit; cum ad animae "
  "definitionem percipiendam, distincta & absoluta organici corporis notitia "
  "minime requiratur; sed confusa sufficiat, quae facile potest comparari. "
  "Quin vero non minus ad notitiam organici corporis, scientia animae; quam ad "
  "animae scientiam, organici corporis cognitio exigitur, siquidem anima etiam "
  "in definitione corporis organici adhibetur, cum definiatur id, quod affectum "
  "est organis, ad animae functiones obeundas accommodatis. Quo patet eiusmodi "
  "argumentum, si quid momenti habeat, aequa vi in aduersarios retorqueri "
  "posse.",
  "Alexander of Aphrodisias, however, in his first book On the Soul, and "
  "Averroes on the fourth of the Meteorology, put the treatment of the parts of "
  "animals first. First, because the contemplation of matter precedes the "
  "contemplation of form; and the parts, or organs, are the matter or subject "
  "of the soul. Second, because the soul is defined through the organic body: "
  "therefore, lest the definition proceed from things unknown, it was necessary "
  "that this be declared by Aristotle beforehand. These arguments, however, do "
  "not conclude. For granted that the organic parts of animals, of which "
  "Aristotle treats in the book On the Parts of Animals, stand on the side of "
  "matter insofar as they receive in themselves the bodily functions of the "
  "soul, and are dispositions necessary for the introduction of the soul, as we "
  "shall expound in its place; and granted likewise that the organic parts are "
  "more easily known than the soul, whose nature is hidden and recondite — it "
  "does not follow that they had to be treated first, but rather the soul; "
  "because, as we indicated a little before, and as Aristotle admonishes in the "
  "first chapter of book 1 of the Physics and in chapters 1 and 3 of book 1 On "
  "the Parts of Animals, after Plato in the Phaedrus and Hippocrates in the "
  "book On the Nature of Man, in every well-ordered discipline those things "
  "are to be treated first which extend more widely and are held more common, "
  "lest we be forced to repeat the same things too often: and the soul extends "
  "more widely than the parts of animals, since these are in animals only, "
  "while it is in all living things. Nor does the consideration of matter "
  "precede the contemplation of form if the order of teaching demands "
  "otherwise; and the soul is defined not through the organic body of an "
  "animal, but through the organic body of a living thing in general — which "
  "it was not necessary for Aristotle to declare before the doctrine of the "
  "soul, since for grasping the definition of the soul a distinct and complete "
  "knowledge of the organic body is not at all required; a confused one "
  "suffices, and that is easily obtained. Nay rather, the science of the soul "
  "is no less required for the knowledge of the organic body than the "
  "knowledge of the organic body for the science of the soul, since the soul "
  "too is employed in the definition of the organic body, which is defined as "
  "that which is furnished with organs accommodated to discharging the "
  "functions of the soul. From which it is plain that an argument of this "
  "kind, if it has any weight, can be turned back with equal force upon the "
  "adversaries.")

u("Nunc quodnam horum librorum subiectum sit, expendamus. Venetus hoc loco, & "
  "quidam alii è recentium Philosophorum coetu non animam, sed corpus animatum "
  "esse statuunt. Quod probant; primum, quia haec doctrina pars quaedam est "
  "Physiologiae; ita oportet eius materiam talem esse, vt de ea totius "
  "Physiologiae subiectum tanquam de parte inferiori ac minus late patenti "
  "enuntietur: liquet autem ens mobile de corpore animato, non de anima eo "
  "pacto dici. Deinde quia vel hic, vel nullibi Aristoteles de corpore "
  "animato egit; nullibi egisse absurdum est; nec enim à Philosopho tam "
  "praeclara species entis naturalis silentio inuoluenda fuit. Egit ergo de "
  "illa in hoc opere; ac proinde corpus animatum est illius subiectum. "
  "Tertio, quia id subiectum cuiusque disciplinae est, cui primo, ac per se "
  "conueniunt affectiones, quae in ea tractantur: at nutriri, sentire, "
  "moueri, velle, intelligere caeteraeque eiusmodi affectiones, de quibus in "
  "hisce libris disseritur, non animae, sed corpori animato partim in "
  "commune, partim per sua inferiora primum ac per se competunt, vt capite 4. "
  "primi libri, tex. 54. Aristoteles inquit. Quare non videtur negandum "
  "materiam huic operi subiectum esse corpus animatum.",
  "Now let us weigh what the subject of these books is. Venetus at this "
  "place, and certain others from the company of the more recent "
  "philosophers, hold that it is not the soul but the animate body. They "
  "prove it thus: first, because this doctrine is a certain part of natural "
  "philosophy; therefore its matter must be such that the subject of all "
  "natural philosophy may be predicated of it as of an inferior and less "
  "widely extending part: and it is clear that mobile being is said in that "
  "way of the animate body, not of the soul. Next, because either here or "
  "nowhere did Aristotle treat of the animate body; and that he treated of it "
  "nowhere is absurd, for so noble a species of natural being was not to be "
  "wrapped in silence by the Philosopher. Therefore he treated of it in this "
  "work; and accordingly the animate body is its subject. Third, because the "
  "subject of any discipline is that to which the affections treated in it "
  "belong first and of themselves: but to be nourished, to sense, to be "
  "moved, to will, to understand, and the other affections of this kind, of "
  "which these books treat, belong first and of themselves not to the soul "
  "but to the animate body — partly in general, partly through its inferior "
  "parts — as Aristotle says in chapter 4 of the first book, text 54. "
  "Wherefore it seems not to be denied that the subject of this work is the "
  "animate body.")

u("Verùm nobilissimi quique Peripatetici, Simplicius, Philoponus, Alexander, "
  "Themistius, D. Thomas, M. Albertus, Aegidius, Theophilus, Iandunus, "
  "Caietanus, Ferrariensis, & plerique alii ad hunc locum communi consensu "
  "aduersariam partem sequuntur, statuuntque horum librorum subiectum esse "
  "animam. Quod ex eo primum suadetur, quia vt ex primo libro Posteriorum, "
  "capite 1. & 9. colliges, id rite subiectum in qualibet scientia "
  "constituitur, cuius definitio in ea inuestigatur, & traditur: in hoc vero "
  "opere non corporis animati, sed animae definitionem quaesiuit, atque "
  "assignauit Aristoteles; vt ipse in prooemio propositum sibi esse dixit, & "
  "in libro de Sensu & sensili persolutum à se fuisse gloriatur. Deinde, quia "
  "si corpus animatum esset huius disciplinae subiectum, cum in categoria "
  "substantiae inferius, atque adeo nobilius sit animal, quam corpus "
  "animatum; sequeretur immerito hanc scientiam propter subiectae materiae "
  "praestantiam, maximeque ob excellentiam animae rationalis caeteris "
  "Physiologiae partibus ab Aristotele anteponi; cum ea potius, quae de "
  "animantibus disserit, eo nomine praeferenda esset. Postremo fauet huic "
  "sententiae ipsa operis inscriptio; nuncupantur enim hi libri de anima.",
  "But all the noblest Peripatetics — Simplicius, Philoponus, Alexander, "
  "Themistius, St. Thomas, Albert the Great, Giles, Theophilus, Jandun, "
  "Cajetan, Ferrariensis, and most others at this place — follow the opposite "
  "side with common consent, and hold that the subject of these books is the "
  "soul. This is urged first from this, that, as you will gather from the "
  "first book of the Posterior Analytics, chapters 1 and 9, that is rightly "
  "constituted the subject in any science whose definition is investigated "
  "and delivered in it: and in this work Aristotle sought and assigned the "
  "definition not of the animate body but of the soul — as he himself in the "
  "proem said was his purpose, and in the book On Sense and the Sensible "
  "boasts to have accomplished. Next, because if the animate body were the "
  "subject of this discipline — since in the category of substance the animal "
  "is lower, and for that reason nobler, than the animate body — it would "
  "follow that this science is undeservedly set by Aristotle before the other "
  "parts of natural philosophy on account of the excellence of its subject "
  "matter, and above all the excellence of the rational soul; for rather the "
  "science that treats of animals would on that title deserve preference. "
  "Lastly, the very inscription of the work favors this opinion; for these "
  "books are entitled On the Soul.")

u("In hac dubitatione dicendum nobis videtur, libros de Anima bifariam "
  "spectari posse. Nimirum vel per se, ac separatim: vel vna cum iis, qui "
  "paruorum Naturalium vocantur, qui illorum quasi accessio quaedam sunt. Tum "
  "si priori modo spectentur, eorum subiectum esse animam; si posteriori, "
  "corpus animatum. Tres enim de Anima libri in scrutanda explicandaque per "
  "se animae natura potissimum insumuntur, nec viuentium affectiones & "
  "proprietates, nisi secundum rationem originis suae, & vt ab anima tanquam "
  "à fonte manant, ac prout ad cognitionem illius obseruiunt, expenduntur. At "
  "in opere paruorum naturalium eaedem, prout iam corpori eiusque organis "
  "accommodantur, in considerationem veniunt. Quo fit, vt eiusmodi opus, & "
  "tres libri de anima integram corporis animati commendationem exhibeant.",
  "In this doubt it seems to us that the books On the Soul can be regarded in "
  "two ways: namely either in themselves and separately, or together with "
  "those called the Parva Naturalia, which are as it were a certain appendage "
  "of them. If they are regarded in the first way, their subject is the "
  "soul; if in the second, the animate body. For the three books On the Soul "
  "are spent above all in searching out and explaining the nature of the soul "
  "in itself; and the affections and properties of living things are weighed "
  "only according to the account of their origin, as they flow from the soul "
  "as from a fountain, and insofar as they serve the knowledge of it. But in "
  "the work of the Parva Naturalia the same are taken into consideration as "
  "they are now accommodated to the body and its organs. Whence it comes "
  "about that such a work, together with the three books On the Soul, "
  "exhibits a complete presentation of the animate body.")

u("Aduersariorum vero argumenta, quae probare nitebantur libros de Anima, "
  "etiam per se sumptos, habere pro subiecto corpus animatum, facile "
  "soluuntur.",
  "The arguments of the adversaries, which strove to prove that the books On "
  "the Soul, even taken by themselves, have the animate body for their "
  "subject, are easily dissolved.")

u("Ad primum negari debet, oportere totius disciplinae subiectum de subiectis "
  "partium affirmari: alioqui dicetur ens mobile de sensu & sensibili, itemque "
  "de respiratione & de motu animalium, quas constat esse peculiares materias "
  "quorundam opusculorum Aristotelicae physiologiae. Similiter necessum "
  "foret, orationem Philosophorum, quae totius Logicae subiectum est, "
  "enuntiari de voce simplici, quae est subiectum Categoriarum. Itaque sat "
  "est subiecta partium cuiusque scientiae aliquo modo includi in subiecto "
  "totius; nec sub illo directa serie contineri oportet.",
  "To the first it must be denied that the subject of the whole discipline "
  "has to be affirmed of the subjects of its parts: otherwise mobile being "
  "would be said of sense and the sensible, and likewise of respiration and "
  "of the motion of animals, which are agreed to be the peculiar matters of "
  "certain small works of Aristotelian natural philosophy. In the same way "
  "it would be necessary that discourse, which is the subject of the whole "
  "of logic, be predicated of the simple word, which is the subject of the "
  "Categories. It is enough, then, that the subjects of the parts of any "
  "science be in some way included in the subject of the whole; they need "
  "not be contained under it in a direct series.")

u("Ad secundum, dicendum est, non omisisse Aristotelem corporis animati "
  "explicationem, sed eam, quoad animam, in tribus, qui de ea inscribuntur, "
  "libris; quoad ipsum corpus, quantum sat erat, in paruis naturalibus "
  "tradidisse.",
  "To the second it must be said that Aristotle did not omit the explication "
  "of the animate body, but delivered it — as regards the soul, in the three "
  "books inscribed with its name; as regards the body itself, as much as was "
  "sufficient, in the Parva Naturalia.")

u("Ad tertium, affectiones, de quibus in libris de Anima agitur, primo, ac "
  "per se conuenire animae, vt earum fonti & origini: tametsi vt Aristoteles "
  "loco citato vult, non nisi de toto composito, vt de principe subiecto "
  "enuntientur. Si cui tamen visum fuerit, priorem sententiam, quae licet à "
  "communi abhorreat, improbabilis tamen non est, respondeat argumentis in "
  "contrariam partem adductis; quanquam Aristoteles hisce libris animae "
  "definitionem tanto animo inuestigarit, ac tradiderit: in id tamen non "
  "animae gratia praecipue incubuisse: sed propter corpus animatum, ad quod, "
  "vt ad totius operis scopum, respiciebat. Nec vero animae facultates, quoad "
  "suum principium duntaxat, sed vt totum compositum, id est, corpus "
  "animatum ornant, expendisse. Item doctrinam de anima reliquis naturalis "
  "philosophiae partibus excellere, non vt praecise circa corpus animatum in "
  "commune versatur; sed quatenus disceptat de animo rationali, qui caeteras "
  "physicae considerationis formas, naturae dignitate vincit. Denique "
  "inscribi hos libros de Anima, non vt à principali subiecto, sed vt à "
  "praecipua illius parte, quae proinde subiectum quo dici potest, sicuti & "
  "corpus animatum, subiectum quod, vt Philosophi quidam loquuntur.",
  "To the third: the affections treated in the books On the Soul belong "
  "first and of themselves to the soul, as to their fountain and origin — "
  "although, as Aristotle in the place cited holds, they are predicated only "
  "of the whole composite as of the principal subject. If nevertheless the "
  "former opinion should seem right to anyone — which, though it departs "
  "from the common one, is yet not improbable — let him answer the arguments "
  "brought for the contrary side thus: although Aristotle in these books "
  "investigated and delivered the definition of the soul with such spirit, "
  "yet he applied himself to this not chiefly for the soul's sake, but on "
  "account of the animate body, to which, as to the scope of the whole work, "
  "he was looking; nor did he weigh the faculties of the soul only as "
  "regards their principle, but as they adorn the whole composite, that is, "
  "the animate body. Likewise, that the doctrine of the soul excels the "
  "remaining parts of natural philosophy not precisely as it deals with the "
  "animate body in general, but insofar as it disputes of the rational soul, "
  "which surpasses in dignity of nature the other forms of physical "
  "consideration. Finally, that these books are entitled On the Soul not "
  "from the principal subject but from its chief part — which accordingly "
  "can be called the subject by which, just as the animate body is the "
  "subject which, as certain philosophers speak.")

u("Quod ad operis partitionem spectat, ea sic habet: In primo libro disserit "
  "Aristoteles de essentia animae, contra veterum placita; ex propria vero "
  "sententia cap. 1. & 2. lib. 2. Tum reliqua parte eiusdem libri agit de "
  "potentijs animae in commune, de facultatibus ad animam vegetatricem "
  "spectantibus, & de sensibus externis. De internis autem, tribus capitibus "
  "libri tertij. De intellectu à quarto ad nonum. Inde ad finem libri, de "
  "motu & quibusdam affectionibus, quae animantibus in vniuersum competunt.",
  "As to the partition of the work, it stands thus: in the first book "
  "Aristotle discourses on the essence of the soul against the opinions of "
  "the ancients; according to his own judgment, in chapters 1 and 2 of book "
  "2. Then in the remaining part of the same book he treats of the "
  "powers of the soul in general, of the faculties belonging to the "
  "vegetative soul, and of the external senses. Of the internal ones, in "
  "three chapters of the third book; of the intellect, from the fourth to "
  "the ninth; thence to the end of the book, of motion and of certain "
  "affections which belong to living things universally.")

out = {
 'id': 'conimbricenses',
 'autor': 'The Coimbra Jesuits (Manuel de Góis)',
 'titel': 'Commentarii in tres libros De anima — the Prooemium (1598)',
 'jahr': '1598',
 'lang': 'la',
 'zitierweise': 'Con. De an., prooem. [k]',
 'quelle': ("Latin: transcribed by eye from the page images of the 1617 printing, "
            "Commentarii Collegii Conimbricensis Societatis Iesu, in tres libros De "
            "anima Aristotelis (Internet Archive commentariicolle00col; the printing's "
            "columns 2–7) — the OCR of the early-modern type served only for "
            "navigation. First printed at Coimbra in 1598; the modern editions are in "
            "copyright and were not used. Long s and ligatures normalised, the "
            "printer's abbreviations silently expanded, u/v kept as printed; the "
            "marginal captions and source references are not carried, and the "
            "paragraph numbers are this site's own — the print sets the Prooemium as "
            "a continuous treatise. The English is an unofficial machine-generated "
            "working translation made for this site directly from the Latin (CC0), "
            "without authority — cite the Latin. Named next steps: the Prooemium's "
            "Quaestio unica (whether the contemplation of the intellective soul "
            "belongs to natural philosophy) and the questions on the internal senses "
            "in book III."),
 'hinweis': ("What, at the threshold of modernity, is the science of the soul? The "
             "Coimbra course opens with the answer the whole doctrine-of-the-soul "
             "strand turns on: the Delphic nosce te ipsum read as psychology, the "
             "soul as horizon aeternitatis et temporis, Augustine's two questions — "
             "de anima, de Deo — and the disputed subject of Aristotle's three "
             "books, resolved in the college's characteristic both-ways manner. This "
             "is the course the Ratio's rules prescribe for the third year of "
             "philosophy, taught at Coimbra in the generation that carried it to "
             "Goa and Macau. Part of the concordance and the citation-bound "
             "dialogue; not part of the linguistic statistics, which describe the "
             "core corpus only."),
 'sections': [
   {'id': 'prooem', 'zk': 'Con. De an., prooem.',
    'titel': 'Prooemium — De vtilitate, ordine, materia subiecta, & partitione '
             'horum librorum',
    'units': U}],
}

path = os.path.join(REPO, 'data', 'conimbricenses.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', len(U), 'units')
