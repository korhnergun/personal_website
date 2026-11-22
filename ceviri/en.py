# -*- coding: utf-8 -*-
"""
İngilizce sayfayı Türkçe sayfadan üretir: index.html -> en/index.html

Türkçe sayfayı (index.html) değiştirdikten sonra çalıştırın:
    python ceviri/en.py

Betik her çeviri çiftini sayfada arar ve şu durumlarda durur (hiçbir şey yazmadan):
  - bir Türkçe metin sayfada bulunamazsa ya da beklenenden farklı sayıda geçerse
    (Türkçe metni değiştirdiyseniz aşağıdaki listede de güncelleyin),
  - bir sayı/tarih İngilizce karşılığında yoksa,
  - üretilen sayfada çevrilmemiş Türkçe kalırsa.
Şirket, depo, dosya ve kişi adları bilerek çevrilmez.
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'en', 'index.html')

# (Türkçe, İngilizce, kaç kez geçtiği). Bağlam gereken yerlerde etiketlerle birlikte yazıldı.
PAIRS = [
    # --- head
    ('<title>Korhan Ergün TUNÇELLİ: bilgisayar mühendisi, web ve backend geliştirici</title>',
     '<title>Korhan Ergün TUNÇELLİ: computer engineer, web and backend developer</title>', 1),
    ('content="İzmir\'de C#, ASP.NET MVC ve React ile web uygulamaları geliştiren, NKÜ mezunu bilgisayar mühendisinin özgeçmişi, projeleri ve tasarımları."',
     'content="CV, projects and designs of an NKU-graduate computer engineer in İzmir who builds web applications with C#, ASP.NET MVC and React."', 1),
    ('content="Korhan Ergün TUNÇELLİ: bilgisayar mühendisi"', 'content="Korhan Ergün TUNÇELLİ: computer engineer"', 1),
    ('content="Web ve backend geliştirici; stajlar, projeler, yetenekler ve tasarımlar."',
     'content="Web and backend developer; internships, projects, skills and designs."', 1),

    # --- top bar, menu, tab bar, footer links
    ('>İçeriğe geç</a>', '>Skip to content</a>', 1),
    ('aria-label="Korhan Ergün TUNÇELLİ, başa dön"', 'aria-label="Korhan Ergün TUNÇELLİ, back to top"', 1),
    ('aria-label="Ana menü"', 'aria-label="Main menu"', 1),
    ('href="#anasayfa">Ana sayfa</a>', 'href="#anasayfa">Home</a>', 1),
    ('href="#hakkimda">Hakkımda</a>', 'href="#hakkimda">About</a>', 2),
    ('href="#deneyim">Deneyim</a>', 'href="#deneyim">Experience</a>', 2),
    ('href="#yetenek">Yetenekler</a>', 'href="#yetenek">Skills</a>', 2),
    ('href="#projeler">Projeler</a>', 'href="#projeler">Projects</a>', 2),
    ('href="#tasarim">Tasarımlar</a>', 'href="#tasarim">Designs</a>', 2),
    ('href="#iletisim">İletişim</a>', 'href="#iletisim">Contact</a>', 2),
    ('download>CV\'mi indirin</a>', 'download>Download my CV</a>', 1),
    ('aria-label="Koyu temaya geç"', 'aria-label="Switch to dark theme"', 2),
    ('aria-label="Menü"', 'aria-label="Menu"', 1),
    ('aria-label="Dil seçimi"', 'aria-label="Language"', 2),
    ('<span>Hakkımda</span>', '<span>About</span>', 1),
    ('<span>Deneyim</span>', '<span>Experience</span>', 1),
    ('<span>Yetenek</span>', '<span>Skills</span>', 1),
    ('<span>Proje</span>', '<span>Projects</span>', 1),
    ('<span>Tasarım</span>', '<span>Designs</span>', 1),
    ('<span>İletişim</span>', '<span>Contact</span>', 1),
    ('aria-label="Bölümler"', 'aria-label="Sections"', 1),

    # --- hero
    ('</span>Yeni işlere müsait · İzmir</p>', '</span>Available for new roles · İzmir</p>', 1),
    ('<span class="hero__hi">Merhaba, ben</span>', '<span class="hero__hi">Hi, I\'m</span>', 1),
    ('<span class="sr-only">, bilgisayar mühendisi</span>', '<span class="sr-only">, computer engineer</span>', 1),
    ('data-typed=\'["Bilgisayar Mühendisi","Computer Engineer","Tasarımcı"]\'', 'data-typed=\'["Computer Engineer","Designer"]\'', 1),
    ('aria-hidden="true">Bilgisayar Mühendisi</span>', 'aria-hidden="true">Computer Engineer</span>', 1),
    ('C#, ASP.NET MVC ve React ile web uygulamaları geliştiriyorum. Tekirdağ Namık Kemal Üniversitesi\'nden 3.31 ortalamayla mezun oldum.',
     'I build web applications with C#, ASP.NET MVC and React. I graduated from Tekirdağ Namık Kemal University with a 3.31 GPA.', 1),
    ('</span>CV\'mi indirin<svg', '</span>Download my CV<svg', 1),
    ('</span>Projelerimi görün</a>', '</span>See my projects</a>', 1),
    ('alt="Korhan Ergün TUNÇELLİ\'nin portresi"', 'alt="Portrait of Korhan Ergün TUNÇELLİ"', 1),
    ('<b>3.31</b> ortalama</span>', '<b>3.31</b> GPA</span>', 1),
    ('<b>3</b> staj</span>', '<b>3</b> internships</span>', 1),
    ('<b>15</b> teknoloji</span>', '<b>15</b> technologies</span>', 1),
    ('<b>4</b> proje</span>', '<b>4</b> projects</span>', 1),
    ('<dt>Ortalama</dt><dd>3.31</dd><dt>Staj</dt><dd>3 şirket</dd><dt>Teknoloji</dt><dd>15</dd><dt>Proje</dt><dd>4</dd>',
     '<dt>GPA</dt><dd>3.31</dd><dt>Internships</dt><dd>3 companies</dd><dt>Technologies</dt><dd>15</dd><dt>Projects</dt><dd>4</dd>', 1),
    ('aria-label="Yörüngeyi durdur"', 'aria-label="Pause the orbit"', 1),
    ("p ? 'Yörüngeyi oynat' : 'Yörüngeyi durdur'", "p ? 'Play the orbit' : 'Pause the orbit'", 1),

    # --- about
    ('<h2 id="hakkimda-h">Hakkımda</h2>', '<h2 id="hakkimda-h">About me</h2>', 1),
    ('Tekirdağ Namık Kemal Üniversitesi\'nden 3.31 ortalamayla mezun oldum. Bugün <strong>web ve backend</strong> yazılım geliştirme ile veritabanı alanlarında çalışıyor, takım içinde problem çözmeyi seviyorum.',
     'I graduated from Tekirdağ Namık Kemal University with a 3.31 GPA. Today I work in <strong>web and backend</strong> software development and databases, and I enjoy solving problems as part of a team.', 1),
    ('<dt>Konum</dt><dd>İzmir</dd>', '<dt>Location</dt><dd>İzmir</dd>', 1),
    ('<dt>Ortalama</dt><dd>3.31 / 4</dd>', '<dt>GPA</dt><dd>3.31 / 4</dd>', 1),
    ('<dt>Diller</dt><dd>EN B2 · DE A1</dd>', '<dt>Languages</dt><dd>EN B2 · DE A1</dd>', 1),
    ('<dt>Durum</dt><dd><span class="ab-live" aria-hidden="true"></span>Müsait</dd>', '<dt>Status</dt><dd><span class="ab-live" aria-hidden="true"></span>Available</dd>', 1),
    ('<li>Takım çalışması</li><li>Liderlik</li><li>Teknik dokümantasyon</li><li>Problem çözme</li>',
     '<li>Teamwork</li><li>Leadership</li><li>Technical documentation</li><li>Problem solving</li>', 1),
    ('aria-label="Korhan.cs dosyasında şehir, ortalama, diller ve durum satırları sırayla vurgulanıyor"',
     'aria-label="In Korhan.cs the city, GPA, languages and status lines are highlighted in turn"', 1),
    ('</i>Stajlar.cs</span>', '</i>Internships.cs</span>', 1),
    ('data-code-chip>derlendi</span>', 'data-code-chip>compiled</span>', 1),
    ('data-note="İzmir\'de yaşıyorum.">  <span class="k">string</span> Sehir =', 'data-note="I live in İzmir.">  <span class="k">string</span> City =', 1),
    ('<span class="k">double</span> Ortalama =', '<span class="k">double</span> Gpa =', 1),
    ('data-note="İngilizcem iş seviyesinde.">  <span class="k">string</span>[] Diller =', 'data-note="My English is business level.">  <span class="k">string</span>[] Languages =', 1),
    ('<span class="c">// web, backend, veritabanı</span>', '<span class="c">// web, backend, databases</span>', 1),
    ('data-note="Yeni işlere müsaitim.">  <span class="k">bool</span> Musait =', 'data-note="I\'m available for new roles.">  <span class="k">bool</span> Available =', 1),
    ('<span data-code-text>NKÜ bilgisayar mühendisliği mezunu.</span>', '<span data-code-text>Computer engineering graduate of NKU.</span>', 1),

    # --- experience
    ('<h2 id="deneyim-h">Staj deneyimim. <span class="muted">Sağlık, telekom ve otomotiv şirketlerinde üç staj.</span></h2>',
     '<h2 id="deneyim-h">My internship experience. <span class="muted">Three internships at healthcare, telecom and automotive companies.</span></h2>', 1),
    ('data-reading="{n} / {total} sayfa"', 'data-reading="{n} / {total} pages"', 1),
    ('data-files-status>4 sayfa hazır</span>', 'data-files-status>4 pages ready</span>', 1),
    ('>Doktor notları</span>', '>Doctor notes</span>', 1),
    ('>Hemşire notları</span>', '>Nurse notes</span>', 1),
    ('>Hasta verileri</span>', '>Patient data</span>', 1),
    ('>Veri tabloları</span>', '>Data tables</span>', 1),
    ('>TEMMUZ – AĞUSTOS 2024</span>', '>JULY – AUGUST 2024</span>', 1),
    ('>Yazılım geliştirme stajı</p>', '>Software development internship</p>', 1),
    ('React.js ile doktor notları, hemşire notları ve hasta verileri sayfalarındaki tabloları ve not bölümlerini geliştirdim.',
     'I built the tables and note sections on the doctor notes, nurse notes and patient data pages with React.js.', 1),
    ('"alt":"Python ve SQL; MSSQL verisi, fatura süreçleri, şikayet analizi ve tahmin modelleriyle bağlantılı."',
     '"alt":"Python and SQL, connected to MSSQL data, billing processes, complaint analysis and prediction models."', 1),
    ('{"label":"Fatura","icon":"ui:receipt"}', '{"label":"Billing","icon":"ui:receipt"}', 1),
    ('{"label":"Şikayet","icon":"ui:message-square"}', '{"label":"Complaints","icon":"ui:message-square"}', 1),
    ('{"label":"Tahmin","icon":"ui:chart-line"}', '{"label":"Prediction","icon":"ui:chart-line"}', 1),
    ('>ŞUBAT – HAZİRAN 2024</span>', '>FEBRUARY – JUNE 2024</span>', 1),
    ('>Uzun dönem staj</p>', '>Long-term internship</p>', 1),
    ('Fatura süreçleri ve ilgili şikayetler için Python ve SQL çözümleri kurdum; makine öğrenmesiyle veri analizi yaptım.',
     'I built Python and SQL solutions for billing processes and the complaints about them, and analysed data with machine learning.', 1),
    ('Python · MSSQL · Yapay zeka · Agile', 'Python · MSSQL · AI · Agile', 1),
    ('"alt":"Raspberry Pi ağ protokollerine, sistem kurulumlarına, Python ve Django uygulamalarına bağlı."',
     '"alt":"Raspberry Pi, linked to network protocols, system setups, and Python and Django applications."', 1),
    ('{"label":"Ağ","icon":"ui:network"}', '{"label":"Network","icon":"ui:network"}', 1),
    ('>AĞUSTOS – EKİM 2022</span>', '>AUGUST – OCTOBER 2022</span>', 1),
    ('>IT yaz stajı</p>', '>IT summer internship</p>', 1),
    ('Ağ protokolleri, sistem kurulumları ve Raspberry Pi uygulamalarıyla donanım ve yazılımı birlikte çalıştırdım.',
     'I made hardware and software work together through network protocols, system setups and Raspberry Pi applications.', 1),

    # --- skills
    ('<h2 id="yetenek-h">Yeteneklerim. <span class="muted">Dört grupta 15 teknoloji.</span></h2>',
     '<h2 id="yetenek-h">My skills. <span class="muted">15 technologies in four groups.</span></h2>', 1),
    ('"alt":"Yetenekler dört grupta: backend (C#, ASP.NET, SQL), arayüz (React, JavaScript, TypeScript, HTML ve CSS), diğer diller (Python, C ve C++, Node.js, Bootstrap) ve araçlar (Git, GitHub, Figma)."',
     '"alt":"Skills in four groups: backend (C#, ASP.NET, SQL), front end (React, JavaScript, TypeScript, HTML and CSS), other languages (Python, C and C++, Node.js, Bootstrap) and tools (Git, GitHub, Figma)."', 1),
    ('{"label":"Arayüz","icon":"ui:layout-template"', '{"label":"Front end","icon":"ui:layout-template"', 1),
    ('{"label":"HTML ve CSS","icon":"logos:html-5"}', '{"label":"HTML and CSS","icon":"logos:html-5"}', 1),
    ('{"label":"Diller","icon":"ui:code"', '{"label":"Languages","icon":"ui:code"', 1),
    ('{"label":"C ve C++","icon":"logos:c-plusplus"}', '{"label":"C and C++","icon":"logos:c-plusplus"}', 1),
    ('{"label":"Araçlar","icon":"ui:wrench"', '{"label":"Tools","icon":"ui:wrench"', 1),

    # --- projects
    ('<h2 id="projeler-h">Projelerim. <span class="muted">GitHub depoları ve TÜBİTAK destekli bir model.</span></h2>',
     '<h2 id="projeler-h">My projects. <span class="muted">GitHub repositories and a TÜBİTAK-supported model.</span></h2>', 1),
    ('>GitHub profilimi görün</a>', '>See my GitHub profile</a>', 1),
    ('>Maç sonucu tahmin eden model<small>', '>A model that predicts match results<small>', 1),
    ('aria-label="AI Match Predictor GitHub\'da"', 'aria-label="AI Match Predictor on GitHub"', 1),
    ('>Kişisel web sitesi, ASP.NET ile<small>', '>A personal website, built with ASP.NET<small>', 1),
    ('aria-label="PersonalWebSite GitHub\'da"', 'aria-label="PersonalWebSite on GitHub"', 1),
    ('>C# eğitim kampı çalışmaları<small>', '>C# training camp exercises<small>', 1),
    ('aria-label="CSharpEgitimKampi GitHub\'da"', 'aria-label="CSharpEgitimKampi on GitHub"', 1),
    ('>İBB Ecodation frontend çalışması<small>', '>İBB Ecodation front-end work<small>', 1),
    ('aria-label="ibb_ecodation_frontend GitHub\'da"', 'aria-label="ibb_ecodation_frontend on GitHub"', 1),
    ('aria-label="Seçili projenin çalışan görünümü"', 'aria-label="The selected project, shown running"', 1),
    ('data-term-count>4 / 4 adım</span>', 'data-term-count>4 / 4 steps</span>', 1),
    ('>maç verisi okundu</span>', '>match data loaded</span>', 1),
    ('>özellikler hazırlandı</span>', '>features prepared</span>', 1),
    ('<span class="ui-term__n">eğitildi</span>', '<span class="ui-term__n">trained</span>', 1),
    ('>tahminler kaydedildi</span>', '>predictions saved</span>', 1),
    ('<b>Bitti</b>', '<b>Done</b>', 1),
    ('data-term-cmd>python tahmin.py</span>', 'data-term-cmd>python predict.py</span>', 1),
    ('>Repository deseni</span>', '>Repository pattern</span>', 1),
    ('>Entity Framework ve LINQ</span>', '>Entity Framework and LINQ</span>', 1),
    ('>Yönetim paneli</span>', '>Admin panel</span>', 1),
    ('>Giriş formu</span>', '>Login form</span>', 1),
    ('>Bootstrap ile duyarlı arayüz</span>', '>Responsive UI with Bootstrap</span>', 1),
    ('data-reading="{n} / {total} dosya"', 'data-reading="{n} / {total} files"', 2),
    ('data-files-status>6 öğe</span>', 'data-files-status>6 items</span>', 2),
    ('<span class="ui-file__kind">Klasör</span>', '<span class="ui-file__kind">Folder</span>', 4),
    ('<span class="ui-file__kind">Ayar</span>', '<span class="ui-file__kind">Config</span>', 1),
    ('<span class="ui-file__kind">Çözüm</span>', '<span class="ui-file__kind">Solution</span>', 1),

    # --- designs
    ('<h2 id="tasarim-h">Tasarımlarım. <span class="muted">Procreate portreleri ve Twitch yayın paketleri.</span></h2>',
     '<h2 id="tasarim-h">My designs. <span class="muted">Procreate portraits and Twitch stream packages.</span></h2>', 1),
    ('aria-label="Milflix portre çizimi"', 'aria-label="Milflix portrait drawing"', 1),
    ('alt="Milflix için çizilmiş dijital portre"', 'alt="Digital portrait drawn for Milflix"', 1),
    ('aria-label="Yılmaz Şahin portre çizimi"', 'aria-label="Yılmaz Şahin portrait drawing"', 1),
    ('alt="Yılmaz Şahin için çizilmiş dijital portre"', 'alt="Digital portrait drawn for Yılmaz Şahin"', 1),
    ('aria-label="Cenk Öner Twitch paketi"', 'aria-label="Cenk Öner Twitch package"', 1),
    ('alt="Cenk Öner için hazırlanmış Twitch yayın paketi"', 'alt="Twitch stream package made for Cenk Öner"', 1),
    ('aria-label="GTMMaster Twitch paketi"', 'aria-label="GTMMaster Twitch package"', 1),
    ('alt="GTMMaster için hazırlanmış Twitch yayın paketi"', 'alt="Twitch stream package made for GTMMaster"', 1),
    ('aria-label="Kouche Twitch paketi"', 'aria-label="Kouche Twitch package"', 1),
    ('alt="Kouche için hazırlanmış Twitch yayın paketi"', 'alt="Twitch stream package made for Kouche"', 1),
    ('aria-label="Sunay Can Twitch paketi"', 'aria-label="Sunay Can Twitch package"', 1),
    ('alt="Sunay Can için hazırlanmış Twitch yayın paketi"', 'alt="Twitch stream package made for Sunay Can"', 1),

    # --- contact
    ('<h2 id="iletisim-h">İletişim. <span class="muted">Bir e-posta yeter.</span></h2>',
     '<h2 id="iletisim-h">Contact. <span class="muted">One email is enough.</span></h2>', 1),
    ('Yeni projeler, iş birlikleri ya da sadece merhaba demek için yazın; diğer hesaplarım da burada.',
     'Write to me about new projects, collaborations or just to say hello; my other accounts are here too.', 1),
    ('data-sent="Mesajınız gönderildi. E-postanıza dönüş yapacağım." data-sending="Gönderiliyor" data-fix="{n} alanı düzeltin." data-failed="Gönderilemedi: bağlantı kurulamadı. Yazdıklarınız duruyor; tekrar deneyin."',
     'data-sent="Your message has been sent. I will reply to your email."', 1),
    ('value="Kişisel site: yeni iletişim mesajı"', 'value="Personal site: new contact message (English page)"', 1),
    ('>Adınız</label>', '>Your name</label>', 1),
    ('>Adınızı yazın.</p>', '>Write your name.</p>', 1),
    ('>E-postanız</label>', '>Your email</label>', 1),
    ('>@ içeren bir e-posta adresi yazın, ör. ad@alanadi.com.</p>', '>Write an email address with an @, e.g. name@domain.com.</p>', 1),
    ('>Mesajınız</label>', '>Your message</label>', 1),
    ('>Mesajınızı yazın.</p>', '>Write your message.</p>', 1),
    ('>Mesaj gönderin</button>', '>Send message</button>', 1),

    # --- footer
    ('aria-label="Site haritası"', 'aria-label="Site map"', 1),
    ('<p class="footer__lede">Bilgisayar mühendisi, İzmir.</p>', '<p class="footer__lede">Computer engineer, İzmir.</p>', 1),
    ('<h3>Ben</h3>', '<h3>Me</h3>', 1),
    ('<h3>İşler</h3>', '<h3>Work</h3>', 1),
    ('<h3>Bağlantılar</h3>', '<h3>Links</h3>', 1),
    ('Ürün adları ve logolar sahiplerinin ticari markalarıdır.', 'Product names and logos are trademarks of their respective owners.', 1),

    # --- certificates (titles translated; issuers, instructors and programme names kept)
    ('href="#sertifika">Sertifikalar</a>', 'href="#sertifika">Certificates</a>', 2),
    ('<span>Sertifika</span>', '<span>Certificates</span>', 1),
    ('<h2 id="sertifika-h">Sertifikalarım. <span class="muted">Altı belge.</span></h2>', '<h2 id="sertifika-h">My certificates. <span class="muted">Six of them.</span></h2>', 1),
    ('aria-haspopup="dialog">Tümünü görüntüleyin (6)<svg', 'aria-haspopup="dialog">View all (6)<svg', 1),
    ('<b>Prompt Mühendisliği</b>', '<b>Prompt Engineering</b>', 1),
    ('alt="Prompt Mühendisliği başarı belgesi"', 'alt="Prompt Engineering certificate of achievement"', 1),
    ('<b>Python Programlama 201</b>', '<b>Python Programming 201</b>', 1),
    ('alt="Python Programlama 201 başarı belgesi"', 'alt="Python Programming 201 certificate of achievement"', 1),
    ('<b>Python Programlama 101</b>', '<b>Python Programming 101</b>', 1),
    ('alt="Python Programlama 101 başarı belgesi"', 'alt="Python Programming 101 certificate of achievement"', 1),
    ('<b>Mvc5 ile Sıfırdan Admin Panelli Dinamik CV Sitesi</b>', '<b>A Dynamic CV Site with an Admin Panel in MVC5, from Scratch</b>', 1),
    ('alt="Mvc5 ile Sıfırdan Admin Panelli Dinamik CV Sitesi bitirme sertifikası"', 'alt="Certificate of completion: a dynamic CV site with an admin panel in MVC5, from scratch"', 1),
    ('<b>Sourcetree ile Git ve GitHub Kullanımı</b>', '<b>Using Git and GitHub with Sourcetree</b>', 1),
    ('alt="Sourcetree ile Git ve GitHub Kullanımı bitirme sertifikası"', 'alt="Certificate of completion: using Git and GitHub with Sourcetree"', 1),
    ('data-x="Geleceği Yazanlar sınavı · Turkcell Akademi"', 'data-x="Geleceği Yazanlar exam · Turkcell Akademi"', 3),
    ('data-x="Eğitmen: Murat Yücedağ · 7,5 saat"', 'data-x="Instructor: Murat Yücedağ · 7.5 hours"', 1),
    ('data-x="Eğitmen: Emre Altunbilek · 5,5 saat"', 'data-x="Instructor: Emre Altunbilek · 5.5 hours"', 1),
    ('data-x="56/100 puan · B2 Upper Intermediate (okuma ve dinleme)"', 'data-x="Score 56/100 · B2 Upper Intermediate (reading and listening)"', 1),
    ('data-date="21 Kasım 2026"', 'data-date="21 November 2026"', 3),
    ('data-date="3 Temmuz 2025"', 'data-date="3 July 2025"', 1),
    ('data-date="22 Şubat 2025"', 'data-date="22 February 2025"', 1),
    ('data-date="17 Temmuz 2024"', 'data-date="17 July 2024"', 1),
    ('<span class="cert-date">Kasım 2026</span>', '<span class="cert-date">November 2026</span>', 3),
    ('<span class="cert-date">Temmuz 2025</span>', '<span class="cert-date">July 2025</span>', 1),
    ('<span class="cert-date">Şubat 2025</span>', '<span class="cert-date">February 2025</span>', 1),
    ('<span class="cert-date">Temmuz 2024</span>', '<span class="cert-date">July 2024</span>', 1),
    ('aria-label="Kapatın"', 'aria-label="Close"', 1),
    ('target="_blank" rel="noopener">Sertifikayı doğrulayın<svg', 'target="_blank" rel="noopener">Verify the certificate<svg', 1),
    (">PDF'i indirin</a>", '>Download the PDF</a>', 1),
    ('aria-label="Önceki sertifika"', 'aria-label="Previous certificate"', 1),
    ('aria-label="Sonraki sertifika"', 'aria-label="Next certificate"', 1),
    ('aria-label="Sayfanın başına dönün"', 'aria-label="Back to the top"', 1),

    # --- scripts
    ("root.dataset.theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'", "root.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'", 1),
]

# Türkçe harf içeren ama çevrilmemesi gereken adlar (kişi, kurum, şehir, dosya adları)
KEEP = ['Geleceği Yazanlar', 'Turkcell Akademi', 'Murat Yücedağ', 'Emre Altunbilek', 'Korhan Ergün TUNÇELLİ', 'Tekirdağ Namık Kemal', 'İzmir', 'TÜBİTAK', 'İBB', 'Cenk Öner', 'Yılmaz Şahin', 'TR, Türkçe', '"İzmir"', 'Ergün']
# Türkçede çok geçen, aksansız sözcükler: üretilen sayfada görünür metinde kalmamalı
TR_WORDS = r'\b(ve|ile|için|bir|bu|staj|proje|projeler|yazın|görün|deneyim|tasarım|tasarımlar|iletişim|hakkımda|ortalama|diller|durum|musait|sehir|klasör|dosya|sayfa|adım)\b'

def fail(msg):
    print('DURDU:', msg); sys.exit(1)

def main():
    s = open(SRC, encoding='utf-8').read()

    # 1) only the Turkish page needs the Turkish names for the kit's pause buttons
    s, n = re.subn(r'\s*/\* tr-only \*/.*?/\* /tr-only \*/', '', s, flags=re.S)
    if n != 1: fail('tr-only bloğu bulunamadı')

    # 2) the words
    for tr, en, count in PAIRS:
        have = s.count(tr)
        if have != count: fail(f'{have} kez bulundu, {count} bekleniyordu: {tr[:90]}')
        for num in re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'<[^>]+>', ' ', tr)):
            if num not in en and num.replace(',', '.') not in en: fail(f'"{num}" çeviride yok: {en[:90]}')
        s = s.replace(tr, en)

    # 3) the page itself: language, its address, the language switch
    def one(a, b):
        nonlocal s
        if s.count(a) != 1: fail(f'{s.count(a)} kez bulundu: {a[:80]}')
        s = s.replace(a, b)
    one('<html lang="tr"', '<html lang="en"')
    one('<link rel="canonical" href="https://www.korhanerguntuncelli.com/">', '<link rel="canonical" href="https://www.korhanerguntuncelli.com/en/">')
    one('<meta property="og:locale" content="tr_TR">\n<meta property="og:locale:alternate" content="en_US">',
        '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="tr_TR">')
    tr_on = '<a class="lang__opt" href="./" hreflang="tr" lang="tr" aria-label="TR, Türkçe" aria-current="page">TR</a><a class="lang__opt" href="en/" hreflang="en" lang="en" aria-label="EN, English">EN</a>'
    en_on = '<a class="lang__opt" href="../" hreflang="tr" lang="tr" aria-label="TR, Türkçe">TR</a><a class="lang__opt" href="./" hreflang="en" lang="en" aria-label="EN, English" aria-current="page">EN</a>'
    if s.count(tr_on) != 2: fail('dil seçici iki yerde bulunamadı')
    s = s.replace(tr_on, en_on)

    # 4) the page lives one folder down: its files are one level up
    for a in ('href="assets/', 'src="assets/', 'data-img="assets/', 'href="favicon-', 'href="apple-touch-icon', 'href="Korhan%20'):
        s = s.replace(a, a.replace('="', '="../', 1))
    if re.search(r'(?:src|href)="(?!\.\./|https?:|mailto:|#|\./|data:)[^"]+"', s):
        bad = re.findall(r'(?:src|href)="(?!\.\./|https?:|mailto:|#|\./|data:)[^"]+"', s)[:5]
        fail(f'göreli yol kaldı: {bad}')

    # 5) nothing Turkish left in what a reader sees or hears
    left = check(s)
    if left: fail('çevrilmemiş Türkçe kaldı:\n  ' + '\n  '.join(left[:30]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(s)
    write_table()
    print(f'yazıldı: {os.path.relpath(OUT, ROOT)} ve ceviri/ceviri-tablosu.md  ({len(PAIRS)} çeviri çifti)')

def plain(x):
    # the words of one pair, without its tags: a JSON label, an attribute's value, or the text between tags
    j = re.search(r'"(?:label|alt)":"([^"]*)"', x)
    if j: return j.group(1)
    a = re.match(r'^(?:aria-label|alt|content|value|data-[a-z-]+)=([\'"])(.*?)\1', x)
    if a: return a.group(2)
    if not x.startswith('<') and '>' in x:
        lt = x.index('<') if '<' in x else len(x)
        if x.index('>') < lt: x = x[x.index('>') + 1:]
    if x.rfind('<') > x.rfind('>'): x = x[:x.rfind('<')]
    return ' '.join(re.sub(r'<[^>]*>', ' ', x).split()).strip()

def write_table():
    rows, seen = [], set()
    for tr, en, _ in PAIRS:
        a, b = plain(tr), plain(en)
        if a and a != b and (a, b) not in seen:
            seen.add((a, b)); rows.append((a, b))
    out = ['# Türkçe → İngilizce çeviri tablosu', '',
           'Bu dosya `python ceviri/en.py` ile İngilizce sayfayla birlikte yeniden yazılır; elle düzenlemeyin, '
           'bir çeviriyi değiştirmek için `ceviri/en.py` içindeki PAIRS listesini düzenleyin.', '',
           '| Türkçe | İngilizce |', '|---|---|']
    out += [f'| {a.replace("|", "/")} | {b.replace("|", "/")} |' for a, b in rows]
    open(os.path.join(ROOT, 'ceviri', 'ceviri-tablosu.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')

def check(s):
    texts = []
    class P(HTMLParser):
        skip = 0
        def handle_starttag(self, t, a):
            if t == 'style': self.skip += 1
            if t == 'script' and dict(a).get('type') != 'application/json': self.skip += 1
            for k, v in a:
                if v and k in ('alt', 'aria-label', 'title', 'placeholder', 'content', 'data-typed', 'data-sent', 'data-reading', 'data-note', 'value'):
                    texts.append(v)
        def handle_endtag(self, t):
            if t in ('style',) and self.skip: self.skip -= 1
            if t == 'script' and self.skip: self.skip -= 1
        def handle_data(self, d):
            if not self.skip and d.strip(): texts.append(' '.join(d.split()))
    P().feed(s)
    for js in re.findall(r"'([^'\n]{3,})'", ''.join(re.findall(r'<script(?![^>]*application/json)[^>]*>(.*?)</script>', s, re.S))):
        texts.append(js)
    out = []
    for t in texts:
        u = t
        for k in KEEP: u = u.replace(k, '')
        if re.search('[çğıöşüÇĞÖŞÜİ]', u) or re.search(TR_WORDS, u, re.I):
            out.append(t[:120])
    return sorted(set(out))

if __name__ == '__main__':
    main()
