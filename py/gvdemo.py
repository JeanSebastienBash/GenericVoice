#!/usr/bin/env python3
"""
Module: gvdemo.py
Purpose: Generates sample audio files for all supported voices.
Context: Entry point script in py/. Part of Generic Voice v1.0.2 TTS suite.
Impact: Direct user-facing tool.
Related: lib/tts/*/voices/voices.json, py/gv.py
"""


import os
import sys
import json
import subprocess
from pathlib import Path
from glob import glob


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DEMO_DIR = PROJECT_ROOT / "output" / "demo"
GV_PY = PROJECT_ROOT / "py" / "gv.py"

PIPER_VOICES_DIR = PROJECT_ROOT / "lib" / "tts" / "piper" / "voices"
PIPER_VOICES_JSON = PROJECT_ROOT / "lib" / "tts" / "piper" / "voices" / "voices.json"
EDGE_VOICES_JSON = PROJECT_ROOT / "lib" / "tts" / "edge" / "voices" / "voices.json"
ESPEAK_VOICES_JSON = PROJECT_ROOT / "lib" / "tts" / "espeak" / "voices" / "voices.json"

_piper_voices_data = {}


TEXTS = {
    "fr-FR": "Bienvenue sur notre plateforme de petites annonces ! Pour commencer, creez votre compte en quelques clics et completez votre profil afin de gagner la confiance des acheteurs ou des vendeurs. Ensuite, cliquez sur Deposer une annonce et remplissez le formulaire avec un titre clair, une description precise et de belles photos. Choisissez la categorie qui correspond le mieux a votre produit ou service pour qu'il soit facilement trouve. Vous pouvez ensuite fixer votre prix, ajouter vos coordonnees et publier ! Une fois votre annonce en ligne, gerez vos messages directement depuis votre tableau de bord et repondez rapidement aux interesses. Si vous souhaitez plus de visibilite, pensez a activer une option de mise en avant. Enfin, lorsque la vente est conclue, marquez l'annonce comme vendue et laissez un avis a votre interlocuteur. C'est simple, rapide et sur !",
    "en-US": "Welcome to our classified ads platform! To get started, create your account in just a few clicks and complete your profile to gain the trust of buyers or sellers. Then, click on Post an Ad and fill out the form with a clear title, a detailed description and beautiful photos. Choose the category that best matches your product or service so it can be easily found. You can then set your price, add your contact details and publish! Once your ad is online, manage your messages directly from your dashboard and respond quickly to interested parties. If you want more visibility, consider activating a featured ad option. Finally, when the sale is completed, mark the ad as sold and leave a review for your contact. It's simple, fast and safe!",
    "en-GB": "Welcome to our classified ads platform! To get started, create your account in just a few clicks and complete your profile to gain the trust of buyers or sellers. Then, click on Post an Ad and fill out the form with a clear title, a detailed description and beautiful photos. Choose the category that best matches your product or service so it can be easily found. You can then set your price, add your contact details and publish! Once your ad is online, manage your messages directly from your dashboard and respond quickly to interested parties. If you want more visibility, consider activating a featured ad option. Finally, when the sale is completed, mark the ad as sold and leave a review for your contact. It's simple, fast and safe!",
    "de-DE": "Willkommen auf unserer Kleinanzeigen-Plattform! Um zu beginnen, erstellen Sie Ihr Konto in nur wenigen Klicks und vervollstandigen Sie Ihr Profil, um das Vertrauen von Käufern oder Verkaufern zu gewinnen. Klicken Sie dann auf Anzeige aufgeben und fullen Sie das Formular mit einem klaren Titel, einer detaillierten Beschreibung und schonen Fotos aus. Wahlen Sie die Kategorie, die am besten zu Ihrem Produkt oder Ihrer Dienstleistung passt, damit es leicht gefunden werden kann. Dann konnen Sie Ihren Preis festlegen, Ihre Kontaktdaten hinzufugen und veroffentlichen! Sobald Ihre Anzeige online ist, verwalten Sie Ihre Nachrichten direkt von Ihrem Dashboard aus und antworten Sie schnell auf Interessenten. Wenn Sie mehr Sichtbarkeit wunschen, sollten Sie eine Anzeigen-Hervorhebung aktivieren. Schliessen Sie den Verkauf ab, markieren Sie die Anzeige als verkauft und hinterlassen Sie eine Bewertung fur Ihren Kontakt. Es ist einfach, schnell und sicher!",
    "es-ES": "Bienvenido a nuestra plataforma de anuncios clasificados! Para empezar, crea tu cuenta en unos pocos clics y completa tu perfil para ganarte la confianza de compradores o vendedores. Luego, haz clic en Publicar un anuncio y completa el formulario con un titulo claro, una descripcion detallada y bonitas fotos. Elige la categoria que mejor se adapte a tu producto o servicio para que sea facil de encontrar. Luego puedes establecer tu precio, agregar tus datos de contacto y publicar! Una vez que tu anuncio este en linea, gestiona tus mensajes directamente desde tu panel y responde rapidamente a los interesados. Si quieres mas visibilidad, considera activar una opcion de anuncio destacado. Finalmente, cuando la venta se complete, marca el anuncio como vendido y deja una resena a tu contacto. Es simple, rapido y seguro!",
    "it-IT": "Benvenuto sulla nostra piattaforma di annunci! Per iniziare, crea il tuo account in pochi clic e completa il tuo profilo per conquistare la fiducia di acquirenti o venditori. Quindi, clicca su Pubblica un annuncio e compila il modulo con un titolo chiaro, una descrizione dettagliata e belle foto. Scegli la categoria che meglio corrisponde al tuo prodotto o servizio in modo che possa essere facilmente trovato. Puoi quindi impostare il prezzo, aggiungere i tuoi dati di contatto e pubblicare! Una volta che il tuo annuncio è online, gestisci i tuoi messaggi direttamente dalla tua dashboard e rispondi rapidamente agli interessati. Se desideri maggiore visibilità, considera l'attivazione di un'opzione di annuncio in evidenza. Infine, quando la vendita è conclusa, segna l'annuncio come venduto e lascia una recensione al tuo contatto. È semplice, veloce e sicuro!",
    "pt-BR": "Bem-vindo à nossa plataforma de anúncios classificados! Para começar, crie sua conta em poucos cliques e complete seu perfil para conquistar a confiança de compradores ou vendedores. Em seguida, clique em Publicar um anúncio e preencha o formulário com um título claro, uma descrição detalhada e belas fotos. Escolha a categoria que melhor corresponde ao seu produto ou serviço para que possa ser facilmente encontrado. Você pode então definir seu preço, adicionar seus dados de contato e publicar! Assim que seu anúncio estiver online, gerencie suas mensagens diretamente do seu painel e responda rapidamente aos interessados. Se desejar mais visibilidade, considere ativar uma opção de anúncio em destaque. Por fim, quando a venda for concluída, marque o anúncio como vendido e deixe uma avaliação para seu contato. É simples, rápido e seguro!",
    "pt-PT": "Bem-vindo a nossa plataforma de anuncios classificados em Portugal! Para comecar, crie a sua conta em apenas alguns cliques e complete o seu perfil para ganhar a confianca de compradores ou vendedores. Em seguida, clique em Publicar um anuncio e preencha o formulario com um titulo claro, uma descricao detalhada e belas fotos. Escolha a categoria que melhor corresponde ao seu produto ou servico para que possa ser facilmente encontrado. Pode entao definir o seu preco, adicionar os seus dados de contacto e publicar! Assim que o seu anuncio estiver online, gerencie as suas mensagens diretamente do seu painel e responda rapidamente aos interessados. Se desejar mais visibilidade, considere ativar uma opcao de anuncio em destaque. Por fim, quando a venda for concluida, marque o anuncio como vendido e deixe uma avaliacao para o seu contacto. E simples, rapido e seguro!",
    "nl-NL": "Welkom op ons platform voor kleinanunciess! Om te beginnen maakt u in slechts een paar klikken een account aan en voltooit u uw profiel om het vertrouwen te winnen van kopers of verkopers. Klik vervolgens op Advertentie plaatsen en vul het formulier in met een duidelijke titel, een gedetailleerde beschrijving en mooie foto's. Kies de categorie die het beste bij uw product of dienst past zodat deze gemakkelijk gevonden kan worden. U kunt vervolgens uw prijs instellen, uw contactgegevens toevoegen en publiceren! Zodra uw advertentie online is, beheert u uw berichten rechtstreeks van uw dashboard en reageert u snel op geïnteresseerden. Als u meer zichtbaarheid wilt, overweeg dan om een uitgelichte advertentie-optie te activeren. Ten slotte, wanneer de verkoop is afgerond, markeert u de advertentie als verkocht en laat u een beoordeling achter voor uw contact. Het is simpel, snel en veilig!",
    "nl-BE": "Welkom op ons platform voor kleinanunciess! Om te beginnen maakt u in slechts een paar klikken een account aan en voltooit u uw profiel om het vertrouwen te winnen van kopers of verkopers. Klik vervolgens op Advertentie plaatsen en vul het formulier in met een duidelijke titel, een gedetailleerde beschrijving en mooie foto's. Kies de categorie die het beste bij uw product of dienst past zodat deze gemakkelijk gevonden kan worden. U kunt vervolgens uw prijs instellen, uw contactgegevens toevoegen en publiceren! Zodra uw advertentie online is, beheert u uw berichten rechtstreeks van uw dashboard en reageert u snel op geïnteresseerden. Als u meer zichtbaarheid wilt, overweeg dan om een uitgelichte advertentie-optie te activeren. Ten slotte, wanneer de verkoop is afgerond, markeert u de advertentie als verkocht en laat u een beoordeling achter voor uw contact. Het is simpel, snel en veilig!",
    "ru-RU": "Dobro pozhalovat na naschu platformu obyavleniy! Chtoby nachat, sozdajte akkaunt za neskolko klikov i zapolnite svoj profil, chtoby zavoevat doverie pokupatelej ili prodavtsov. Zatem nazhmite Razmestit obyavlenie i zapolnite formu s chetkim zagolovkom, podrobnym opisaniem i krasivymi fotografiyami. Vyberite kategoriyu, kotoraya luchshe vsego sootvetstvuet vashemu produktu ili usluge, chtoby ego mozhno bylo legko najti. Zatem vy mozhete ustanovit tsenu, dobavit svoi kontaktnye dannye i opublikovat! Kak tolko vasho obyavlenie budet opublikovano, upravlyajte soobshcheniyami napryamuyu s paneli upravleniya i bystro otvechajte zainteresovannym litsam. Esli vy khotite bolshej vidimosti, rassmotrite vozmozhnost aktivatsii funktsii prodvizheniya obyavleniya. Nakonets, kogda prodazha budet zavershena, otmette obyavlenie kak prodannoe i ostavte otzyv vashemu kontaktu. Eto prosto, bystro i bezopasno!",
    "pl-PL": "Witaj na naszej platformie ogłoszeń! Aby rozpocząć, utwórz konto w kilka kliknięć i uzupełnij swój profil, aby zdobyć zaufanie kupujących lub sprzedających. Następnie kliknij Umieść ogłoszenie i wypełnij formularz z jasnym tytułem, szczegółowym opisem i ładnymi zdjęciami. Wybierz kategorię, która najlepiej odpowiada Twojemu produktowi lub usłudze, aby można ją było łatwo znaleźć. Następnie możesz ustalić cenę, dodać swoje dane kontaktowe i opublikować! Gdy Twoje ogłoszenie będzie online, zarządzaj wiadomościami bezpośrednio z panelu i szybko odpowiadaj zainteresowanym. Jeśli chcesz większej widoczności, rozważ aktywację opcji wyróżnionego ogłoszenia. Na koniec, gdy sprzedaż zostanie zakończona, oznacz ogłoszenie jako sprzedane i zostaw opinię swojemu kontaktowi. To proste, szybkie i bezpieczne!",
    "ja-JP": "Ware no bunrui koukoku puretto e youkoso! Saisho ni, kureka clikutsu de akuonto o sakusei shi, omotpuraif o kanbi shite kudasai. Sorede, koukoku o happyou suru bosu o click shi, akarui taitoru, shousai na setsumei de foomu o nihonbun de nyuuryoku shitekudasai. Seihin matawa saabisu ni saiteki na kategori o sentaku shite kudasai. Sorede anata wa negaio settei shi, renrakusaki jouhou o tsuika shite publish dekimasu! Anata no koukoku ga onrain ni uppi shiyouto, dasshuboodo kara messenger o kanri shi, kyoushinsha ni henji shitekudasai. Saishuuten ni, baibai ga kanryou shita toki, koukoku o hanbaiki zumi to shinki, anata no torikku ni ribyu o nokoshitekudasai.",
    "ko-KR": "dang-ui bunryu gwanggo peureoteom e oshilsu ropeunnida! Sijak-hante, mankeum clik-mande from account-reul mandeulgo kudasai. Geurigo, gwanggo neomu giyo-reul clikhago, clear title, sangseokjeog-in description de foomu o pileoh-geumyung hap-sida. Munchingeor-eun mulssig-eulo kategori o sentaku shitekudasai. Sorede gwanggo-reul gonggaehago siheom-eul woning-gi wihae jageugaedoelila. Gwanggo-ga online-hante napseub-eul dingsyuboodo-eseo managehago, interested yejeja-ege henji shitekudasai. panmae-ga wanlyeon-doel-myeo, gwanggo-reul pangyu-shi-geom-eseo jeongsokakagi geos-eul bae-eulo namgyeoju sip-eo haeju siplida.",
    "zh-CN": "Huanying lai dao women de fenlei guangao pingtai! Shouxiān, zhǐyào diǎn jī jǐ xià jiù kěyǐ chuàngjiàn nín de zhànghù, bìng wánshàn nín de gèrén zīliào. Ránhòu, diǎn jī fābù guǎnggào, shǐyòng qīngxī de biāotí, xiáng xì de miáoshù tiánxiě biǎogé. Xuǎnzé zuì fúhé nín chǎnpǐn huò fúwù de lèimù. Ránhòu nín kěyǐ shèzhì jiàgé, tiānjiā liánxì fāngshì bìng fābù! Yī dàn nín de guǎnggào shàngxiàn, nín kěyǐ guǎnlǐ wèixìn, bìng kuài sù huí fù. Zuìhòu, dāng jiāoyì wánchéng shí, jiāng guǎnggào biāojì wéi yǐ xiāoshòu, bìng wéi nín de liánxì rén liú xià píngjià.",
    "ar-JO": "Ahlan bik fi mafram al-i'lanat! Li an tabda', min fadlak anklik 'ala Hisab fi bidaya wa akmil mashakhilk. Thumma, anukris 'ala Mawqi' I'lan wa imla' al-nashat ma'a 'unwan wafih, wasf mufassal, wasuwirat jamila. Ikhtar al-fatra allati tueba'id ma'a muntajatika aw khadamatika. Sum ma tumaqqan takht alsi'r, tazid ma'alumattik wa talsh! Ida kan i'lanuka fi al-ishtigal, idabbir risalatak wa astajib li al-muhtamin boutan suri'. Ida limit tahawwal 'ala al-zurar, washhad al-i'lan ka mabii' wa tarak ra'y lilmukhatib.",
    "cs-CZ": "Vitejte na nasi platforme inzeratu! Pro zacatek si vytvorte ucet behem nekolika kliknuti a doplnte svuj profil. Pak kliknete na Vlozit inzerat a vyplnte formulář s jasnym nazvem, podrobnym popisem a krásnymi fotografiemi. Vyberte kategorii, ktera nejlepe odpovida vasemu produktu nebo sluzbe. Pak muzete nastavit cenu, pridat sve kontaktni udaje a publikovat! Jakmile bude vas inzerat online, spravujte zpravy a rychle odpovedzte zajemcum. Nakonec, kdyz je prodej dokoncen, oznacte inzerat jako prodany a zanechte posouzeni.",
    "sv-SE": "Valkommen till varannonsplattform! For att komma igang, skapa ditt konto med bara nagra klick och komplettera din profil. Klicka sedan pa Lagg ut en annons och fyll i formularet med en tydlig titel, en detaljerad beskrivning och vackra foton. Valj den kategori som passerar bast till ditt produkt eller din tjanst. Du kan sedan satta ditt pris, lagga till dina kontaktuppgifter och publicera! Nar din annons ar online, hantera dina meddelanden och svara snabbt pa intresserade parter. Slutligen, nar forsaljningen ar klar, markera annonsen som sald och lamna ett omdome.",
    "tr-TR": "Ilan platformumuza hos geldiniz! Baslamak icin, birkac tiklamayla hesabinizi olusturun ve profilinizi tamamlayin. Ardindan, Bir Ilan Ver tiklayin ve açık bir baslik, ayrintili bir açiklama ve guzel fotograflarla formu doldurun. Urununuz veya hizmetiniz icin en uygun kategoriyi secin. Ardindan fiyatinizi belirleyebilir, iletisim bilgilerinizi ekleyebilir ve yayinlayabilirsiniz! Ilaniniz yayinda oldugunda, mesajlarinizi yonet ve ilgilenenlere hizla yanit verin. Son olarak, satis tamamlandiginda, ilani satildi olarak isaretleyin ve degerlendirme birakm.",
    "hu-HU": "Udv a hirdetesek platformjan! A kezdeshez hozzon letre egy fiot nehany kattintassal es teljesitse profiljat. Ezutan kattintson a Hirdetes feladasara es toltse ki az urlapot egy egyertelmu cimmel, reszletes leirassal es gyonyoru fotokkal. Valassza ki a kategoriat, amely legjobban megfelel a termekenek vagy szolgalatanak. Ezutan beallithatja az ara, hozzaadhatja elerhetoseget es kozreadhatja! Ha a hirdetese online van, kezelje uzeneteit es gyorsan valaszoljon az erdeklodoknek. Vegul, jelolje meg a hirdetest eladottkent es hagyjon ertekelest.",
    "el-GR": "Kalos irthate stin platforma mas gia mikres aggelies! Gia na xekinisete, ftiaξte ton logariasmo sas me liga klik kai sympliroste to profil sas. Se auto to simeio, klikarete sto Post an Ad kai sympliroste thn efarmogh me enan safh titlo, mia leptomerh perigrafh kai wraies fotografies. Dialeksete thn kathgoria pou tairiazei kalutera sto proion h sth metoxys sas. Sth synexeia, mporite na orisete thn timh sas, na prosjesete ta stoixeia epithysews sas kai na dhmosieysete! Otan to aggelia sas einai online, diaxeiriste ta minimata sas kai apanthste grhgorws se osous endiaferontai. Telika, shmeiwste to aggelia ws pwlhmeno kai afste mia kritikh.",
    "fi-FI": "Tervetuloa luokitteluilmoitusalustallemme! Aloittaaksesi luo tilisi vain muutamalla napsautuksella ja taydista profiilisi. Napsauta sitten Lataa ilmoitus ja tayta lomake selkealla otsikolla, tarkalla kuvauksella ja kauniilla kuvilla. Valitse kategoria, joka sopii parhaiten tuotteeseesi tai palveluun. Voit sitten asettaa hintasi, lisata yhteystietosi ja julkaista! Kun ilmoituksesi on verkossa, hallinnoi viestejasi ja vastaa nopeasti kiinnostuneille. Lopuksi, merkkaa ilmoitus myydyksi ja jata arvostelu.",
    "da-DK": "Velkommen til vores rubrikannonceplatform! For at komme i gang skal du oprette din konto med kun et par klik og udfylde din profil. Klik derefter paa Post en Annonce og udfyld formularen med en klar titel, en detaljeret beskrivelse og smukke billeder. Vaelg den kategori, der passer bedst til dit produkt eller din tjeneste. Derefter kan du fastsatte din pris, tilfoje dine kontaktoplysninger og udgive! Naer din annonce er online, kan du styre dine beskeder og svare hurtigt paa interesserede parter. Til sidst, naar salget er gennemfoert, skal du markere annonsen som solgt og efterlade en anmeldelse.",
    "sk-SK": "Vitajte na nasej platforme inzeratov! Pre zaciatok si vytvorte ucet niekolkymi kliknutiami a doplnte svoj profil. Potom kliknite na Vlozit inzerat a vyplnte formulr s jasnym nazvom, podrobnym popisom a krasnymi fotografiami. Vyberte kategoriu, ktera najlepsie zodpoveda vasmu produktu alebo sluzbe. Potom mozete nastavit cenu, pridat svoje kontaktne udaje a publikovat! Hned ako bude vas inzerat online, spravujte spravy a rychlo odpovedzte zaujemcom. Nakoniec, oznacte inzerat ako predany a nechajte posudenie.",
    "bg-BG": "Dobre doshli na nashata platforma za obyavi! Za da zapochneте, suzdajte si akunut s samo nqkolkо klikvaniya i populnete profila си. Sled tova, kliknete varhu Promakni obyava i populnete formulyara s yasen zaglavie, podrobno opisanie i krasivi snimki. Izberete kategoriyata, koqto nay-dobre otgovarya na vasheto proizwedenie ili usluga. Sled tova mozhete da settite tsinata si, dobavite kontaktnite si danni i publikuvate! Vednzha kogato vashata obyava e online, upravlyavayte syobshcheniyata si i otgovaryayte bzrzo na zainteresovanite. Nakraq, markirayte obyavata kato prodana i ostavte otzyv.",
    "ro-RO": "Bine ati venit pe platforma noastra de anunturi! Pentru a incepe, creati un cont cu doar cateva clicuri si completati profilul pentru a castiga increderea cumparatorilor sau vanzatorilor. Apoi, faceti clic pe Depuneti un anunt si completati formularul cu un titlu clar, o descriere detaliata si fotografii frumoase. Alegeti categoria care corespunde cel mai bine produsului sau serviciului dumneavoastra pentru a fi usor de gasit. Apoi puteti stabili pretul, adaugati datele de contact si publicati! Odata ce anuntul dumneavoastra este online, gestionati mesajele si raspundeti rapid celor interesati. In final, marcati anuntul ca vandut si lasati o recenzie contactului dumneavoastra.",
    "fr-CA": "Bienvenue sur Kijiji, la plateforme de petites annonces la plus populaire au Canada! Pour commencer, creez votre compte en quelques clics et completez votre profil afin de gagner la confiance des acheteurs ou des vendeurs. Ensuite, cliquez sur Deposer une annonce et remplissez le formulaire avec un titre clair, une description precise et de belles photos. Choisissez la categorie qui correspond le mieux a votre produit ou service pour qu'il soit facilement trouve. Vous pouvez ensuite fixer votre prix, ajouter vos coordonnes et publier! Une fois votre annonce en ligne, gerez vos messages directement depuis votre tableau de bord et repondez rapidement aux interesses. Si vous souhaitez plus de visibilite, pensez a activer une option de mise en avant. Enfin, lorsque la vente est conclue, marquez l'annonce comme vendue et laissez un avis a votre interlocuteur. C'est simple, rapide et sur!",
    "es-MX": "Bienvenido a nuestra plataforma de anuncios clasificados! Para comenzar, crea tu cuenta en solo unos clics y completa tu perfil para ganar la confianza de compradores o vendedores. Luego, haz clic en Publicar un anuncio y completa el formulario con un titulo claro, una descripcion detallada y buenas fotos. Elige la categoria que mejor se adapte a tu producto o servicio para que sea facil de encontrar. Luego puedes establecer tu precio, agregar tus datos de contacto y publicar! Una vez que tu anuncio este en linea, gestiona tus mensajes directamente desde tu panel y responde rapidamente a los interesados. Si quieres mas visibilidad, considera activar una opcion de anuncio destacado. Finalmente, cuando la venta se complete, marca el anuncio como vendido y deja una resena a tu contacto. Es simple, rapido y seguro!",
    "hi-IN": "Hamare classified ads platform par svagat! Shuruat karne ke liye, kuch click mein apna account banayein aur buyers ya sellers ka vishwas kamaane ke liye apni profile pura karein. Phir, Post an Ad par click karein aur ek saaf title, detailed description aur acche photos ke saath form bhar dein. Woh category chunein jo aapke product ya service se best match karti ho. Phir aap apni price set kar sakte hain, apne contact details add kar sakte hain aur publish kar sakte hain! Jab aapka ad online ho, apne dashboard se directly messages manage karein aur interested parties ko jaldi reply karein. Agar aap zyada visibility chahte hain, to featured ad option activate karna consider karein. Akhir mein, jab sale complete ho, ad ko sold ke roop mein mark karein aur apne contact ko review de. Yeh simple, fast aur safe hai!",
    "no-NO": "Velkommen til vart annonseringsplattform! For a komme i gang, opprett din konto med bare noen fa klikk og fullfor profilen din for a vinne tillit hos kjopere eller selgere. Klikk deretter paa Legg ut en annonse og fyll ut skjemaet med en tydelig tittel, en detaljert beskrivelse og vakre bilder. Velg kategorien som passer best til ditt produkt eller din tjeneste slik at den enkelt kan bli funnet. Deretter kan du fastsatte prisen din, legge til kontaktinformasjonen din og publisere! Nar annonsen din er online, kan du styre meldingene dine direkte fra instrumentbordet og svare raskt paa interesserte parter. Til slutt, nar salget er gjennomfort, merker du annonsen som solgt og legger igjen en anmeldelse til kontakten din. Det er enkelt, raskt og trygt!",
    "uk-UA": "Laskavo prosymo do nashoyi platformy oholoshen! Schob pochaty, stvorit svii akauant za dekilka klikiv ta zapovnit profil, schob otrymaty doviru pokuptsiv abo prodavtsiv. Potim natysnit Opublikuvaty oholoshennya ta zapovnit formu z chitkym zagolovkom, detalmym opysom ta garaznymy fotohrafiyamy. Obereit kategoriyu, yaka naykrashche vidpovidaye vashomu produktu chi posluzi, schob yii mozhna bulo legko znajty. Potim vy mozhete vstanovyty tsinu, dodaty svoyi kontaktni dani ta opublikuvaty! Jak tolko vase ohovoshennyaye online, upravlyayte sms from svogo panelu ta shvydko vidpovidayte zatsikavlenym. Yakshcho vy khotyte bilshoyi visibility, rozghlyanit aktivatsiyu funktsyi popularnoho ohovoshenny. Nakonets, koly prodazha budye zakinchena, poznachte ohovoshenny yak prodane ta zostavte vidgyk dlya svogo kontaktu. Tse prosto, shvydko ta bezpechno!",
    "fr-BE": "Bienvenue sur notre plateforme de petites annonces ! Pour commencer, creez votre compte en quelques clics et completez votre profil afin de gagner la confiance des acheteurs ou des vendeurs. Ensuite, cliquez sur Deposer une annonce et remplissez le formulaire avec un titre clair, une description precise et de belles photos. Choisissez la categorie qui correspond le mieux a votre produit ou service pour qu'il soit facilement trouve. Vous pouvez ensuite fixer votre prix, ajouter vos coordonnes et publier ! Une fois votre annonce en ligne, gereZ vos messages directement depuis votre tableau de bord et repondeZ rapidement aux interesses. Si vous souhaitez plus de visibilite, pensez a activer une option de mise en avant. Enfin, lorsque la vente est conclue, marquez l'annonce comme vendue et laissez un avis a votre interlocuteur. C'est simple, rapide et sur !",
    "fr-CH": "Bienvenue sur notre plateforme de petites annonces ! Pour commencer, creez votre compte en quelques clics et completez votre profil afin de gagner la confiance des acheteurs ou des vendeurs. Ensuite, cliquez sur Deposer une annonce et remplissez le formulaire avec un titre clair, une description precise et de belles photos. Choisissez la categorie qui correspond le mieux a votre produit ou service pour qu'il soit facilement trouve. Vous pouvez ensuite fixer votre prix, ajouter vos coordonnes et publier ! Une fois votre annonce en ligne, gereZ vos messages directement depuis votre tableau de bord et repondeZ rapidement aux interesses. Si vous souhaitez plus de visibilite, pensez a activer une option de mise en avant. Enfin, lorsque la vente est conclue, marquez l'annonce comme vendue et laissez un avis a votre interlocuteur. C'est simple, rapide et sur !",
    "ca-ES": "Benvinguts a la nostra plataforma d'anuncis classificats! Per començar, crea el teu compte en uns pocs clics i completa el teu perfil per guanyar la confiança de compradors o venedors. Després, fes clic a Publicar un anunci i omple el formulari amb un títol clar, una descripció detallada i bones fotos. Tria la categoria que millor s'adapti al teu producte o servei perquè sigui fàcil de trobar. Després pots establir el teu preu, afegir les teves dades de contacte i publicar! Un cop el teu anunci estigui en línia, gestiona els teus missatges directament des del teu panell i respon ràpidament als interessats. Si vols més visibilitat, considera activar una opció d'anunci destacat. Finalment, quan la venda es completi, marca l'anunci com venut i deixa una ressenya al teu contacte. És senzill, ràpid i segur!",
    "cy-GB": "Croeso i'n platfform hysbysebion dosbarthedig! I ddechrau, crëwch eich cyfrif mewn ychydig o gliciau a chwblhewch eich proffil i ennill ymddiriedaeth prynwyr neu werthwyr. Yna, cliciwch ar Postio Hysbyseb a llenwch y ffurflen gyda theitl clir, disgrifiad manwl a lluniau hardd. Dewiswch y categori sy'n cyfateb orau i'ch cynnyrch neu wasanaeth fel y gellir ei ddod o hyd iddo'n hawdd. Yna gallwch osod eich pris, ychwanegu eich manylion cyswllt a chyhoeddi! Unwaith y bydd eich hysbyseb ar-lein, rheolwch eich negeseuon yn uniongyrchol o'ch dangosfwrdd ac ymatebwch yn gyflym i bartïon diddorol. Os ydych am fwy o welededd, ystyriwch weithredu opsiwn hysbyseb nodweddiadol. Yn olaf, pan fydd y gwerthiad yn cael ei gwblhau, marcwch yr hysbyseb fel gwerthiedig a gadael adolygiad i'ch cyswllt. Mae'n syml, cyflym a diogel!",
    "es-AR": "Bienvenido a nuestra plataforma de anuncios clasificados! Para empezar, crea tu cuenta en unos pocos clics y completa tu perfil para ganarte la confianza de compradores o vendedores. Luego, hacé clic en Publicar un anuncio y completá el formulario con un título claro, una descripción detallada y buenas fotos. Elegí la categoría que mejor se adapte a tu producto o servicio para que sea fácil de encontrar. Después podés establecer tu precio, agregar tus datos de contacto y publicar! Una vez que tu anuncio esté en línea, gestioná tus mensajes directamente desde tu panel y respondé rápidamente a los interesados. Si querés más visibilidad, considerá activar una opción de anuncio destacado. Finalmente, cuando la venta se complete, marcá el anuncio como vendido y dejá una reseña a tu contacto. Es simple, rápido y seguro!",
    "es-CO": "Bienvenido a nuestra plataforma de anuncios clasificados! Para empezar, crea tu cuenta en unos pocos clics y completa tu perfil para ganarte la confianza de compradores o vendedores. Luego, haz clic en Publicar un anuncio y completa el formulario con un título claro, una descripción detallada y buenas fotos. Elige la categoría que mejor se adapte a tu producto o servicio para que sea fácil de encontrar. Luego puedes establecer tu precio, agregar tus datos de contacto y publicar! Una vez que tu anuncio esté en línea, gestiona tus mensajes directamente desde tu panel y responde rápidamente a los interesados. Si quieres más visibilidad, considera activar una opción de anuncio destacado. Finalmente, cuando la venta se complete, marca el anuncio como vendido y deja una reseña a tu contacto. Es simple, rápido y seguro!",
    "eu-ES": "Ongi etorri gure sailkatutako iragarkien plataformara! Hasteko, sortu zure kontua klik gutxitan eta osatu zure profila erosle edo saltzaileen konfiantza irabazteko. Ondoren, egin klik Iragarkia argitaratu-n eta bete formularioa titulu argi batekin, deskribapen zehatz batekin eta argazki ederrekin. Aukeratu zure produktu edo zerbitzuari ongien dagokion kategoria erraz aurkitu ahal izateko. Ondoren, zure prezioa ezarri dezakezu, zure kontaktu-datuak gehitu eta argitaratu! Zure iragarkia linean dagoenean, kudeatu zure mezuak zure panelatik zuzenean eta erantzun azkar interesatuei. Ikusgarritasun gehiago nahi baduzu, kontuan hartu iragarki nabarmendu bat aktibatzea. Azkenik, salmenta osatutakoan, markatu iragarkia saldutako gisa eta utzi iruzkin bat zure kontaktuarentzat. Sinplea, azkarra eta segurua da!",
    "fa-IR": "Be platforme agahi-ye daste-bandi-ye ma khosh amadid! Baraye shoru, hesab-e khod ra dar chand click besazid va profil-e khod ra kamel konid ta etemad-e kharidaran ya forushandegan ra kasb konid. Sepas, ruye enteshar-e agahi click konid va form ra ba onvan-e vazeh, tozihat-e daghigh va aks-haye ziba por konid. Daste-bandi-ye monaseb ba mahsol ya khedmat-e khod ra entekhab konid ta be-asani peyda shavad. Sepas mitavanid gheymat-e khod ra moshakhas konid, ettelaat-e tamas-e khod ra ezafe konid va enteshar dahid! Vaghti agahi-ye shoma online shod, payam-haye khod ra mostaghim az dashboard-e khod modiriyat konid va be-sorat-e sari be alaghemandan pasokh dahid. Agar did-e bishtar mikhahid, faal-sazi-ye gozine-ye agahi-ye vizhe ra dar nazar begirid. Dar nahayat, vaghti forush kamel shod, agahi ra be onvan-e forukhte shode neshan dahid va baraye tamas-e khod nazar bezarid. Sade, sari va amn ast!",
    "id-ID": "Selamat datang di platform iklan baris kami! Untuk memulai, buat akun Anda hanya dengan beberapa klik dan lengkapi profil Anda untuk mendapatkan kepercayaan pembeli atau penjual. Kemudian, klik Pasang Iklan dan isi formulir dengan judul yang jelas, deskripsi yang detail dan foto yang bagus. Pilih kategori yang paling sesuai dengan produk atau layanan Anda agar mudah ditemukan. Anda kemudian dapat menetapkan harga, menambahkan detail kontak Anda dan menerbitkan! Setelah iklan Anda online, kelola pesan Anda langsung dari dasbor Anda dan merespons dengan cepat kepada pihak yang tertarik. Jika Anda ingin lebih banyak visibilitas, pertimbangkan untuk mengaktifkan opsi iklan unggulan. Akhirnya, ketika penjualan selesai, tandai iklan sebagai terjual dan tinggalkan ulasan untuk kontak Anda. Sederhana, cepat dan aman!",
    "is-IS": "Velkomin á flokkunarauglýsingasvið okkar! Til að byrja, búðu til reikninginn þinn með aðeins nokkrum smellum og fylltu út prófílinn þinn til að vinna traust kaupenda eða seljenda. Smelltu síðan á Birta auglýsingu og fylltu út eyðublaðið með skýrum titli, nákvæmri lýsingu og fallegum myndum. Veldu þann flokk sem passar best við vöru þína eða þjónustu svo hægt sé að finna hana auðveldlega. Þú getur síðan sett verðið þitt, bætt við tengiliðaupplýsingum þínum og birt! Þegar auglýsingin þín er á netinu, stýrðu skilaboðunum þínum beint frá mælaborðinu þínu og svaraðu fljótt áhugasömum aðilum. Ef þú vilt meiri sýnileika, íhugaðu að virkja valkost fyrir valda auglýsingu. Að lokum, þegar salan er lokið, merktu auglýsinguna sem selda og skildu eftir umsögn fyrir tengiliðinn þinn. Það er einfalt, hratt og öruggt!",
    "ka-GE": "Kargad mogesalmebit chven klasipicirebuli ganacadebis platformaze! Dasawyisad, sheqmenit tkveni angarishi ramdenime klik-it da sheavset tkveni profili, rom moipovot yidvelebis an gamyidvelebis ndoba. Semdeg, dakliket ganacadebis gamoqveynebas da sheavset ckhadi saxelovani, detaliuri aghceroba da lamazi surnebi. Airchiet kategoria, romelic yvelaze kargad sheesabameba tkven produqts an momsaxureobas, rom advilad ipovon. Semdeg shegizliat daadginot fasi, daumatoT sakontaqto monacemebi da gamoaqveynot! Rogorc ki tkveni ganacadeba iqneba onlain, marTvet shetqobanebebi pirdayapird apidan da swrafad upasuxet dainteresbul pirebs. Tu met khedvadobas gsurs, gaithvaliswineT gamorcheuli ganacadebis opsiis gaaqtiureba. Sabolood, rodesac gayidva dasruldeba, monishnet ganacadeba rogorc gayiduli da dautoveT shefaseba tkven kontakti. Es aris martivi, swrafi da uvsaprtkho!",
    "kk-KZ": "Bizding zharnama platformasyna kosh keldiniz! Bastau ushin, birneshe sheru arqyly esepshiytty zhazyp, profildi toltyryp, satyp alushylar nemese satushylardyng senimine ie bolynyz. Sodan keiin, Zharnama ornalastyrudy basyp, anyq taqyryp, tolyq sipattama zhane ademi suretter bar formany toltyrynyz. Onim nemese qyzmetke sai kes kelietin sanatty tandanyz, ony ongai tabu ushin. Sodan keiin baghany belgilep, bailanys derekterin qosyp, jariyalanyz! Zharnamangyz onlain bolghannan keiin, habarlamalardy basqaru panelinen tikelei basqaryp, qyzyghushylyq tanytqandargha tez jauap beriniz. Eger kobileu korinistik qalasangyz, erekshelengen zharnama opsiisin qosudy oylanyz. Aqyrynda, saty aiaqtalghannan keiin, zharnamany satylghan dep belgilep, kontaktyghyzgha pikir qaldyrynyz. Bul qarpaiym, tez zhane qauipsiz!",
    "lv-LV": "Laipni lugti musu sludinajumu platforma! Lidz saksanai, izveidojiet savu kontu tikai ar daziem klikshiem un papildiniet savu profilu, lai iegutu pirceju vai pardeveju uzticebu. Pēc tam noklikskiniet uz Ievietot sludinajumu un aizpildiet formu ar skaidru virsrakstu, detalizetu aprakstu un skaistam fotografijam. Izveleties kategoriju, kas vislabak atbilst jusu produktam vai pakalpojumam, lai to varetu viegli atrast. Tad varat noteikt savu cenu, pievienot kontaktinformaciju un publicet! Kad jusu sludinajums ir tiešsaiste, parvaldiet savus zinojumus tiesi no savo informacijas paneļa un atbildiet atri ieinteresetajam personam. Ja velaties lielaku redzamibu, apsveriet iespeju aktivizet izcelta sludinajuma opciju. Visbeidzot, kad pardosana ir pabeigta, atzimejiet sludinajumu ka pardotu un atstajiet atsauksmi savam kontaktam. Tas ir vienkarsi, atri un drosi!",
    "ml-IN": "ഞങ്ങളുടെ തരംതിരിച്ച പരസ്യ പ്ലാറ്റ്ഫോമിലേക്ക് സ്വാഗതം! ആരംഭിക്കാൻ, ചില ക്ലിക്കുകളിൽ നിങ്ങളുടെ അക്കൗണ്ട് സൃഷ്ടിച്ച് വാങ്ങുന്നവരുടെയോ വിൽക്കുന്നവരുടെയോ വിശ്വാസം നേടാൻ നിങ്ങളുടെ പ്രൊഫൈൽ പൂർത്തിയാക്കുക. തുടർന്ന്, ഒരു പരസ്യം പോസ്റ്റ് ചെയ്യുക ക്ലിക്ക് ചെയ്ത് വ്യക്തമായ ശീർഷകം, വിശദമായ വിവരണം, മനോഹരമായ ഫോട്ടോകൾ എന്നിവയ്ക്ക് ഫോം പൂരിപ്പിക്കുക. നിങ്ങളുടെ ഉൽപ്പന്നത്തിനോ സേവനത്തിനോ ഏറ്റവും അനുയോജ്യമായ വിഭാഗം തിരഞ്ഞെടുക്കുക, അതിനാൽ അത് എളുപ്പത്തിൽ കണ്ടെത്താൻ കഴിയും. തുടർന്ന് നിങ്ങൾക്ക് നിങ്ങളുടെ വില നിശ്ചയിക്കാം, നിങ്ങളുടെ ബന്ധപ്പെടൽ വിവരങ്ങൾ ചേർക്കാം, പ്രസിദ്ധീകരിക്കാം! നിങ്ങളുടെ പരസ്യം ഓൺലൈനിൽ ആയതിന് ശേഷം, നിങ്ങളുടെ ഡാഷ്ബോർഡിൽ നിന്ന് നേരിട്ട് സന്ദേശങ്ങൾ കൈകാര്യം ചെയ്യുകയും താൽപ്പര്യമുള്ളവർക്ക് വേഗത്തിൽ മറുപടി നൽകുകയും ചെയ്യുക. കൂടുതൽ ദൃശ്യപരത വേണമെങ്കിൽ, ഒരു ഫീച്ചേർഡ് പരസ്യ ഓപ്ഷൻ സജീവമാക്കുന്നത് പരിഗണിക്കുക. അവസാനം, വിൽപ്പന പൂർത്തിയാകുമ്പോൾ, പരസ്യം വിറ്റതായി അടയാളപ്പെടുത്തുകയും നിങ്ങളുടെ ബന്ധപ്പെടലിന് ഒരു അവലോകനം നൽകുകയും ചെയ്യുക. ഇത് ലളിതവും വേഗതയേറിയതും സുരക്ഷിതവുമാണ്!",
    "ne-NP": "Hamro classified ads platform ma svagat chha! Suru garna, kahi click ma afno account banauhos ra kinnechah ya bechnechah ko bharosa pauna afno profile pura garnuhos. Tyas pachi, Post an Ad ma click garnuhos ra spashta shirshak, vistrit varnan ra ramro photos sanga form bharidinus. Tapai ko product ya service sanga sab bhanda milne category channuhos, jasle garda sajilai bhetauna sakinchha. Tyas pachi tapai le afno mulya thaharna saknu hunchha, afno samparka vivaran thapna saknu hunchha ra publish garna saknu hunchha! Tapai ko ad online bhayo bhane, afno dashboard bata sidhai messages manage garnuhos ra interested party lai chito reply garnuhos. Yadi tapai lai badhi visibility chahinchha bhane, featured ad option activate garna vichar garnuhos. Antya ma, jab sale pura hunchha, ad lai sold ko rup ma mark garnuhos ra afno contact lai review dinuhos. Yo saral, chhito ra surakshit chha!",
    "sl-SI": "Dobro dosli na nasi platformi za oglase! Zacetek ustvarite svoj racun z le nekaj kliki in dopolnite svoj profil, da si pridobite zaupanje kupcev ali prodajalcev. Nato kliknite na Objavi oglas in izpolnite obrazec z jasnim naslovom, podrobnim opisom in lepimi fotografijami. Izberite kategorijo, ki najbolj ustreza vasemu izdelku ali storitvi, da jo bo mogoce zlahka najti. Nato lahko dolocite svojo ceno, dodate svoje kontaktne podatke in objavite! Ko je vas oglas na spletu, upravljajte svoja sporocila neposredno iz svoje nadzorne plosce in hitro odgovarjajte zainteresiranim strankam. Ce zelite vecjo vidnost, razmislite o aktivaciji moznosti izpostavljenega oglasa. Na koncu, ko je prodaja koncana, oznacite oglas kot prodan in pustite oceno svojemu kontaktu. Preprosto, hitro in varno!",
    "sq-AL": "Mire se erdhët ne platformen tone te njoftimeve! Per te filluar, krijoni llogarine tuaj me vetem disa klikime dhe plotesoni profilin tuaj per te fituar besimin e bleresve ose shitesve. Pastaj, klikoni ne Postoni nje njoftim dhe mbushni formularin me nje titull te qarte, nje pershkrim te detajuar dhe foto te bukura. Zgjidhni kategorine qe i pergjigjet me se miri produktit ose sherbimit tuaj qe te gjendet lehte. Pastaj mund te caktoni cmimin tuaj, te shtoni te dhenat tuaja te kontaktit dhe te publikoni! Pasi njoftimi juaj te jete online, menaxhoni mesazhet tuaj direkt nga paneli juaj dhe i pergjigjuni shpejt paleve te interesuara. Ne doni me shume dukshmeri, merrni parasysh aktivizimin e nje opsioni njoftimi te theksuar. Ne fund, kur shitja te kete perfunduar, shenojeni njoftimin si te shitur dhe lini nje vleresim per kontaktin tuaj. Eshte e thjeshte, e shpejte dhe e sigurt!",
    "sr-RS": "Dobro dosli na nasu platformu za klasifikovane oglase! Da biste poceli, kreirajte svoj nalog sa samo nekoliko klikova i dopunite svoj profil da biste stekli poverenje kupaca ili prodavaca. Zatim, kliknite na Objavi oglas i popunite formular sa jasnim naslovom, detaljnim opisom i lepim fotografijama. Izaberite kategoriju koja najbolje odgovara vasem proizvodu ili usluzi da bi se lako pronasla. Zatim mozete postaviti svoju cenu, dodati svoje kontakt podatke i objaviti! Kada vas oglas bude online, upravljajte svojim porukama direktno sa vase komandne table i brzo odgovarajte zainteresovanim stranama. Ako zelite vecu vidljivost, razmislite o aktiviranju opcije istaknutog oglasa. Na kraju, kada je prodaja zavrsena, oznacite oglas kao prodat i ostavite recenziju svom kontaktu. Jednostavno, brzo i bezbedno!",
    "sw-CD": "Karibu kwenye jukwaa letu la matangazo! Ili kuanza, tengeneza akaunti yako kwa mabonye machache tu na ukamilishe wasifu wako ili kupata uaminifu wa wanunuzi au wauzaji. Kisha, bonyeza Chapisha tangazo na ujaze fomu yenye kichwa wazi, maelezo ya kina na picha nzuri. Chagua kategoria inayolingana zaidi na bidhaa yako au huduma yako ili iweze kupatikana kwa urahisi. Kisha unaweza kuweka bei yako, kuongeza maelezo yako ya mawasiliano na kuchapisha! Tangazo lako likiwa mtandaoni, simamia ujumbe wako moja kwa moja kutoka kwenye dashibodi yako na ujibu haraka kwa wahusika wenye nia. Ikiwa unataka muonekano zaidi, zingatia kuamua chaguo la tangazo lililochaguliwa. Hatimaye, biashara ikikamilika, weka alama tangazo kama limeuzwa na uache tathmini kwa mawasiliano yako. Ni rahisi, haraka na salama!",
    "te-IN": "Ma classified ads platform ku svagatam! Prarambhinchanadaniki, konni click-lalo mi account ni srustinchandi, konnedaraleyda vikretalala vishvasam pondaniki mi profile ni purti cheyandi. Tarvata, Post an Ad ni click chesi, spashtamaina shirshikam, vistrtamaina vivaranam, manchi photos tho form ni purti cheyandi. Mi utpatti leda sevaku saraina vargam ni ennukondi, tadvaa sulabhamaina kanugonu cheyadaniki. Tarvata mi vegalani nirdharinchavaccu, mi samparka vivaralanu jarchi publish cheyavaccu! Mi ad online ayyaka, mi dashboard nundi direct ga messages ni manage cheyandi, interested parties ki veganga reply ivvandi. Ekkuvaina visibility kavali ante, featured ad option ni activate cheyadaniki alochinchandi. Chivariki, sale purti ayyaka, ad ni sold ga mark cheyandi, mi contact ki review ivvandi. Idi simple, fast mariyu safe!",
    "uk-UA": "Laskavo prosymo do nashoyi platformy oholoshen! Schob pochaty, stvorit svii akauant za dekilka klikiv ta zapovnit profil, schob otrymaty doviru pokuptsiv abo prodavtsiv. Potim natysnit Opublikuvaty oholoshennya ta zapovnit formu z chitkym zagolovkom, detalmym opysom ta garaznymy fotohrafiyamy. Obereit kategoriyu, yaka naykrashche vidpovidaye vashomu produktu chi posluzi, schob yii mozhna bulo legko znajty. Potim vy mozhete vstanovyty tsinu, dodaty svoyi kontaktni dani ta opublikuvaty! Jakshcho vashe oholoshennya onlain, upravlyayte povidomlennyamy pryamo z vashoyi paneli ta shvydko vidpovidayte zatsikavlenym. Jakshcho khochete bilshoyi populyarnosti, rozghlyanit aktyvatsiyu funktsiyi vydilenoho oholoshennya. Zreshtoyu, koly prodazh bude zakincheno, poznachte oholoshennya yak prodane ta zalyshyt vidhuk dlya svoho kontaktu. Tse prosto, shvydko ta bezpechno!",
    "ur-PK": "Hamare classified ads platform par khush amdeed! Shuru karne ke liye, kuch clicks mein apna account banayein aur buyers ya sellers ka aitmaad hasil karne ke liye apni profile mukammal karein. Phir, Post an Ad par click karein aur ek wazeh title, tafseeli description aur acchi tasveeron ke saath form pur karein. Woh category chunein jo aapki product ya service se behtar match karti ho taake aasani se mil sake. Phir aap apni price set kar sakte hain, apne contact details shamil kar sakte hain aur publish kar sakte hain! Jab aapka ad online ho, apne dashboard se directly messages manage karein aur interested parties ko jaldi reply karein. Agar aap zyada visibility chahte hain to featured ad option activate karne par ghor karein. Aakhir mein, jab sale mukammal ho, ad ko sold mark karein aur apne contact ko review dein. Yeh aasan, tez aur mehfooz hai!",
    "vi-VN": "Chao mung ban den nen tang quang cao phan loai cua chung toi! De bat dau, hay tao tai khoan chi voi vai click va hoan thanh ho so cua ban de lay long tin cua nguoi mua hoac nguoi ban. Sau do, nhan Dang tin va dien vao bieu mau voi tieu de ro rang, mo ta chi tiet va nhung buc anh dep. Chon danh muc phu hop nhat voi san pham hoac dich vu cua ban de co the de dang tim thay. Sau do ban co the dat gia cua minh, them thong tin lien he va dang! Khi tin cua ban da truc tuyen, hay quan ly tin nhan truc tiep tu bang dieu khien va tra loi nhanh chong cac ben quan tam. Neu ban muon hien thi nhieu hon, hay xem xet kich hoat tuy chon tin noi bat. Cuoi cung, khi giao dich hoan tat, hay danh dau tin da ban va de lai danh gia cho nguoi lien he cua ban. That don gian, nhanh chong va an toan!",
}

DEFAULT_TEXT = "Welcome to Generic Voice. This is a demonstration of text to speech synthesis."

LANG_MAPPING = {
    "fr": "fr-FR",
    "en": "en-US",
    "de": "de-DE",
    "es": "es-ES",
    "it": "it-IT",
    "pt": "pt-PT",
    "nl": "nl-NL",
    "ru": "ru-RU",
    "pl": "pl-PL",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "ar": "ar-JO",
    "cs": "cs-CZ",
    "sv": "sv-SE",
    "tr": "tr-TR",
    "hu": "hu-HU",
    "el": "el-GR",
    "fi": "fi-FI",
    "da": "da-DK",
    "sk": "sk-SK",
    "bg": "bg-BG",
    "ro": "ro-RO",
    "ca": "ca-ES",
    "cy": "cy-GB",
    "es-419": "es-MX",  # Espagnol d'Amérique latine → Mexique
    "eu": "eu-ES",      # Basque
    "fa": "fa-IR",      # Farsi/Persan
    "id": "id-ID",      # Indonésien
    "is": "is-IS",      # Islandais
    "ka": "ka-GE",      # Géorgien
    "kk": "kk-KZ",      # Kazakh
    "lv": "lv-LV",      # Letton
    "ml": "ml-IN",      # Malayalam
    "ne": "ne-NP",      # Népalais
    "sl": "sl-SI",      # Slovène
    "sq": "sq-AL",      # Albanais
    "sr": "sr-RS",      # Serbe
    "sw": "sw-CD",      # Swahili
    "te": "te-IN",      # Telugu
    "uk": "uk-UA",      # Ukrainien
    "ur": "ur-PK",      # Ourdou
    "vi": "vi-VN",      # Vietnamien
    "hi": "hi-IN",      # Hindi
    "no": "no-NO",      # Norvégien
    "en-us": "en-US",
    "en-gb": "en-GB",
    "en-gb-x-rp": "en-GB",
    "pt-br": "pt-BR",
    "pt-pt": "pt-PT",
}


def _load_piper_voices_json():
    """Charge le fichier voices.json de Piper en mémoire."""
    global _piper_voices_data
    if PIPER_VOICES_JSON.exists():
        try:
            with open(PIPER_VOICES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            _piper_voices_data = data.get("voices", {})
        except Exception as e:
            print(f"  ⚠️  Erreur chargement Piper voices.json: {e}")
            _piper_voices_data = {}


def resolve_lang(lang_code: str) -> str:
    """
    Résout un code langue vers une clé TEXTS.
    Retourne 'default' si aucune correspondance trouvée.
    """
    if not lang_code:
        return "default"
    
    normalized = lang_code.replace("_", "-").lower()
    
    if normalized.upper() in [k.upper() for k in TEXTS.keys()]:
        for key in TEXTS.keys():
            if key.upper() == normalized.upper():
                return key
    
    if normalized in LANG_MAPPING:
        return LANG_MAPPING[normalized]
    
    if "-" in normalized:
        base = normalized.split("-")[0]
        if base in LANG_MAPPING:
            return LANG_MAPPING[base]
    
    base = normalized.split("-")[0] if "-" in normalized else normalized
    for key in TEXTS.keys():
        if key.lower().startswith(base):
            return key
    
    return "default"


def get_lang_key_from_voice(voice_id: str, tts_engine: str) -> str:
    """
    Extrait la clé de langue depuis l'ID de voix.
    Pour Piper: utilise voices.json pour obtenir le champ 'language'.
    Pour Edge/eSpeak: utilise la logique existante.
    """
    if tts_engine == "piper":
        if voice_id in _piper_voices_data:
            lang_from_json = _piper_voices_data[voice_id].get("language", "")
            return resolve_lang(lang_from_json)
        
        if "_" in voice_id:
            parts = voice_id.split("_")
            if len(parts) >= 1:
                lang_part = parts[0]
                return resolve_lang(lang_part)
        return "default"
    
    elif tts_engine == "edge":
        if "-" in voice_id:
            parts = voice_id.split("-")
            if len(parts) >= 2:
                lang_key = f"{parts[0]}-{parts[1]}"
                return resolve_lang(lang_key)
        return "default"
    
    elif tts_engine == "espeak":
        return resolve_lang(voice_id)
    
    return "default"


def get_demo_text(voice_id: str, tts_engine: str) -> str:
    """Retourne le texte de démo approprié pour la voix."""
    lang_key = get_lang_key_from_voice(voice_id, tts_engine)
    if lang_key == "default":
        return DEFAULT_TEXT
    return TEXTS.get(lang_key, DEFAULT_TEXT)


def get_piper_voices() -> list:
    """Liste toutes les voix Piper disponibles (fichiers .onnx)."""
    voices = []
    if not PIPER_VOICES_DIR.exists():
        return voices
    
    for onnx_file in sorted(PIPER_VOICES_DIR.glob("*.onnx")):
        if onnx_file.name.endswith(".onnx.json"):
            continue
        voice_id = onnx_file.stem  # Nom sans extension
        voices.append(voice_id)
    
    return voices


def get_edge_voices() -> list:
    """Liste toutes les voix Edge TTS disponibles."""
    voices = []
    if not EDGE_VOICES_JSON.exists():
        return voices
    
    try:
        with open(EDGE_VOICES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        voices_data = data.get("voices", {})
        voices = sorted(voices_data.keys())
    except Exception as e:
        print(f"  ⚠️  Erreur lecture Edge voices: {e}")
    
    return voices


def get_espeak_voices() -> list:
    """Liste toutes les voix eSpeak disponibles."""
    voices = []
    if not ESPEAK_VOICES_JSON.exists():
        return voices
    
    try:
        with open(ESPEAK_VOICES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        voices_data = data.get("voices", {})
        voices = sorted(voices_data.keys())
    except Exception as e:
        print(f"  ⚠️  Erreur lecture eSpeak voices: {e}")
    
    return voices


def run_synthesis(tts_engine: str, voice_id: str, text: str, output_file: Path, error_log_file) -> bool:
    """
    Lance la synthèse via gv.py.
    Retourne True si succès, False si erreur.
    Log l'erreur dans error_log_file et continue (pas d'arrêt immédiat).
    """
    cmd = [
        sys.executable,
        str(GV_PY),
        "--tts", tts_engine,
        "--voice", voice_id,
        "--text", text,
        "--output", str(output_file),
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max par voix
        )
        
        if result.returncode != 0:
            error_msg = f"[{tts_engine}] {voice_id}: code {result.returncode}\n"
            error_msg += f"  command: {' '.join(cmd)}\n"
            if result.stdout:
                error_msg += f"  stdout: {result.stdout[-500:]}\n"
            if result.stderr:
                error_msg += f"  stderr: {result.stderr[:500]}\n"
            error_msg += "-" * 70 + "\n"
            
            error_log_file.write(error_msg)
            error_log_file.flush()
            
            print(f" [✗ ÉCHEC - loggué]")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        error_msg = f"[{tts_engine}] {voice_id}: TIMEOUT (5 min)\n"
        error_msg += f"  command: {' '.join(cmd)}\n"
        error_msg += "-" * 70 + "\n"
        
        error_log_file.write(error_msg)
        error_log_file.flush()
        
        print(f" [⏱️ TIMEOUT - loggué]")
        return False
    
    except Exception as e:
        error_msg = f"[{tts_engine}] {voice_id}: EXCEPTION {e}\n"
        error_msg += f"  command: {' '.join(cmd)}\n"
        error_msg += "-" * 70 + "\n"
        
        error_log_file.write(error_msg)
        error_log_file.flush()
        
        print(f" [✗ EXCEPTION - loggué]")
        return False



def main():
    print("=" * 70)
    print("  Generic Voice - Script de démo interne")
    print("  Génération audio pour toutes les voix")
    print("=" * 70)
    print()
    
    _load_piper_voices_json()
    
    if not GV_PY.exists():
        print(f"❌ ERREUR: {GV_PY} introuvable")
        sys.exit(1)
    
    OUTPUT_DEMO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Répertoire de sortie: {OUTPUT_DEMO_DIR}")
    print()
    
    print("🔍 Collecte des voix disponibles...")
    
    piper_voices = get_piper_voices()
    edge_voices = get_edge_voices()
    espeak_voices = get_espeak_voices()
    
    total_voices = len(piper_voices) + len(edge_voices) + len(espeak_voices)
    
    print(f"   • Piper:  {len(piper_voices):3d} voix")
    print(f"   • Edge:   {len(edge_voices):3d} voix")
    print(f"   • eSpeak: {len(espeak_voices):3d} voix")
    print(f"   ───────────────")
    print(f"   • Total:  {total_voices:3d} voix")
    print()
    
    if total_voices == 0:
        print("❌ Aucune voix trouvée. Abandon.")
        sys.exit(1)
    
    print("⚠️  Ce script va générer des fichiers audio dans output/demo/")
    print("    Temps estimé: 2-4 heures (selon la machine)")
    print()
    response = input("Continuer? [O/n]: ").strip().lower()
    if response and response not in ("o", "oui", "y", "yes"):
        print("Abandon.")
        sys.exit(0)
    
    print()
    print("🚀 Démarrage de la génération...")
    print()
    
    error_log_path = OUTPUT_DEMO_DIR / "demo_errors.log"
    error_log_file = open(error_log_path, "w", encoding="utf-8")
    error_log_file.write("# Log des erreurs de génération demo\n")
    error_log_file.write(f"# Démarré: {__import__('datetime').datetime.now()}\n")
    error_log_file.write("=" * 70 + "\n\n")
    
    processed = 0
    failed = 0
    
    engines = [
        ("piper", piper_voices),
        ("edge", edge_voices),
        ("espeak", espeak_voices),
    ]
    
    for tts_engine, voices in engines:
        if not voices:
            continue
        
        print(f"\n{'='*70}")
        print(f"  Moteur: {tts_engine.upper()} ({len(voices)} voix)")
        print(f"{'='*70}")
        
        for i, voice_id in enumerate(voices, 1):
            processed += 1
            
            text = get_demo_text(voice_id, tts_engine)
            
            safe_voice = voice_id.replace("/", "_").replace("\\", "_")
            output_file = OUTPUT_DEMO_DIR / f"demo_{tts_engine}_{safe_voice}.wav"
            
            voice_file = OUTPUT_DEMO_DIR / f"demo_{tts_engine}_{safe_voice}_voice.wav"
            mix_file = OUTPUT_DEMO_DIR / f"demo_{tts_engine}_{safe_voice}_mix.wav"
            
            print(f"  [{processed:4d}/{total_voices:4d}] {tts_engine:8} {voice_id:40} ... ", end="", flush=True)
            
            if output_file.exists():
                print("[déjà existant ✓]")
                continue
            
            success = run_synthesis(tts_engine, voice_id, text, output_file, error_log_file)
            
            if success:
                if mix_file.exists():
                    if voice_file.exists():
                        voice_file.unlink()
                    mix_file.rename(output_file)
                    print(f"[{output_file.name} ✓]")
                elif voice_file.exists():
                    voice_file.rename(output_file)
                    print(f"[{output_file.name} ✓]")
                else:
                    print("[✗ Fichier introuvable après synthèse]")
                    failed += 1
            else:
                for f in [voice_file, mix_file]:
                    if f.exists():
                        f.unlink()
                failed += 1
    
    error_log_file.close()
    
    generated = list(OUTPUT_DEMO_DIR.glob("demo_*.wav"))
    
    print()
    print("=" * 70)
    if failed == 0:
        print("  ✓ Génération terminée avec succès!")
    else:
        print(f"  ⚠️  Génération terminée avec {failed} échec(s)")
    print("=" * 70)
    print()
    print(f"  Voix traitées: {processed}")
    print(f"  ✓ Réussies:   {processed - failed}")
    if failed > 0:
        print(f"  ✗ Échouées:   {failed}")
        print(f"  📄 Log erreurs: {error_log_path}")
    print(f"  📁 Fichiers: {OUTPUT_DEMO_DIR}")
    print(f"  📊 Total fichiers WAV: {len(generated)}")
    print()
    
    if generated:
        print("  Exemples:")
        for f in sorted(generated)[:5]:
            print(f"    • {f.name}")
        if len(generated) > 5:
            print(f"    ... et {len(generated) - 5} autres")
        print()
    
    if failed > 0:
        print(f"  ⚠️  {failed} voix n'ont pas pu être générées.")
        print("  Consultez le log pour la liste des voix à supprimer.")
        sys.exit(1)
    else:
        error_log_path.unlink(missing_ok=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
