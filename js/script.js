// Yukarı Dön Butonu
const scrollToTopBtn = document.getElementById('scrollToTopBtn');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollToTopBtn.classList.add('show');
    } else {
        scrollToTopBtn.classList.remove('show');
    }
});
scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
/* ============================================
   KONFİGÜRASYON
   ============================================ */
const CONFIG = {
    // GitHub kullanıcı adınızı buraya yazın (projeler bu hesaptan çekilecek)
    githubUsername: 'korhnergun',

    // Hero bölümünde döngü ile yazılacak ünvanlar
    typingTitles: [
        'Computer Engineer',
        'Bilgisayar Mühendisi',
        'Tasarımcı'
    ],

    // Yetenekleriniz — istediğinizi ekleyip çıkarabilirsiniz
    skills: [
        { name: 'C#', icon: 'fa-solid fa-hashtag' },
        { name: 'ASP.NET MVC5', icon: 'fa-solid fa-server' },
        { name: 'JavaScript', icon: 'fa-brands fa-js' },
        { name: 'TypeScript', icon: 'fa-solid fa-code' },
        { name: 'Python', icon: 'fa-brands fa-python' },
        { name: 'C / C++', icon: 'fa-solid fa-c' },
        { name: 'React', icon: 'fa-brands fa-react' },
        { name: 'Node.js', icon: 'fa-brands fa-node-js' },
        { name: 'HTML5', icon: 'fa-brands fa-html5' },
        { name: 'CSS3', icon: 'fa-brands fa-css3-alt' },
        { name: 'Git', icon: 'fa-brands fa-git-alt' },
        { name: 'Figma', icon: 'fa-brands fa-figma' },
        { name: 'SQL', icon: 'fa-solid fa-database' }
    ],

    // Tasarımlarınız — daha sonra image alanına URL veya yerel asset yolu yazın
    // image: null bırakılırsa placeholder ikon gösterilir
    designs: [
        {
            title: 'Milflix Kişisel Portre Çizimi',
            category: 'Digital Drawing, Illustration, Procreate',
            description: '',
            image: 'https://i.postimg.cc/dV14CvvV/Basliksiz-1.jpg',
            link: 'https://i.postimg.cc/dV14CvvV/Basliksiz-1.jpg',
        },
        {
            title: 'Yılmaz Şahin Kişisel Portre Çizimi',
            category: 'Digital Drawing, Illustration, Procreate',
            image: 'https://i.postimg.cc/jdVbvgCx/post-1.jpg',
            link: 'https://i.postimg.cc/jdVbvgCx/post-1.jpg',
        },
        {
            title: 'Cenk Öner Twitch Pack',
            category: 'Twitch Overlay, Stream Design',
            image: 'https://i.postimg.cc/C5xF0zyr/cizen-genc-streamer-pack-1920x1080.jpg',
            link: 'https://i.postimg.cc/C5xF0zyr/cizen-genc-streamer-pack-1920x1080.jpg',
        },
        {
            title: 'GTMMaster Twitch Pack',
            category: 'Twitch Overlay, Stream Design',
            image: 'https://i.postimg.cc/9fB5fCY6/gtmmaster-twitch-pack.jpg',
            link: 'https://i.postimg.cc/9fB5fCY6/gtmmaster-twitch-pack.jpg',
        },
        {
            title: 'Kouche Twitch Pack',
            category: 'Twitch Overlay, Stream Design',
            image: 'https://i.postimg.cc/Qd1ZRp9K/cizen-genc-streamer-pack-1920x1080.jpg',
            link: 'https://i.postimg.cc/Qd1ZRp9K/cizen-genc-streamer-pack-1920x1080.jpg',
        },
        {
            title: 'Sunay Can Twitch Pack',
            category: 'Twitch Overlay, Stream Design',
            image: 'https://i.postimg.cc/9MTxfp2P/cizen-genc-streamer-pack-1920x1080.jpg',
            link: 'https://i.postimg.cc/9MTxfp2P/cizen-genc-streamer-pack-1920x1080.jpg',
        }
    ],

    // GitHub dil renkleri
    languageColors: {
        JavaScript: '#f1e05a',
        TypeScript: '#3178c6',
        Python: '#3572a5',
        Java: '#b07219',
        'C++': '#f34b7d',
        C: '#555555',
        'C#': '#178600',
        HTML: '#e34c26',
        CSS: '#563d7c',
        Vue: '#41b883',
        Go: '#00add8',
        Rust: '#dea584',
        Ruby: '#701516',
        PHP: '#4f5d95',
        Swift: '#fa7343',
        Kotlin: '#a97bff',
        Dart: '#00b4ab',
        Shell: '#89e051'
    }
};

/* ============================================
   TEMA YÖNETİMİ
   ============================================ */
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

const savedTheme = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
html.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
});

/* ============================================
   NAVBAR — KAYDIRMA EFEKTİ + AKTİF LİNK
   ============================================ */
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    // Aktif link
    let current = '';
    sections.forEach(section => {
        const top = section.offsetTop - 120;
        if (window.scrollY >= top) {
            current = section.id;
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

/* ============================================
   MOBİL MENÜ
   ============================================ */
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('open');
    navMenu.classList.toggle('open');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('open');
        navMenu.classList.remove('open');
    });
});

/* ============================================
   HERO TYPING ANIMASYONU
   ============================================ */
class TypeWriter {
    constructor(el, words, wait = 2000) {
        this.el = el;
        this.words = words;
        this.wait = wait;
        this.txt = '';
        this.wordIndex = 0;
        this.isDeleting = false;
        this.type();
    }

    type() {
        const current = this.wordIndex % this.words.length;
        const fullTxt = this.words[current];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.el.textContent = this.txt;

        let typeSpeed = this.isDeleting ? 50 : 110;

        if (!this.isDeleting && this.txt === fullTxt) {
            typeSpeed = this.wait;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.wordIndex++;
            typeSpeed = 400;
        }

        setTimeout(() => this.type(), typeSpeed);
    }
}

const typedEl = document.getElementById('typedText');
if (typedEl) {
    new TypeWriter(typedEl, CONFIG.typingTitles);
}

/* ============================================
   YETENEKLER — KART OLUŞTURMA
   ============================================ */
const skillsGrid = document.getElementById('skillsGrid');
if (skillsGrid) {
    skillsGrid.innerHTML = CONFIG.skills.map(skill => `
        <div class="skill-card fade-in">
            <div class="skill-icon"><i class="${skill.icon}"></i></div>
            <div class="skill-name">${skill.name}</div>
        </div>
    `).join('');
}

/* ============================================
   TASARIMLAR — KART OLUŞTURMA
   ============================================ */
const designsGrid = document.getElementById('designsGrid');
if (designsGrid) {
    designsGrid.innerHTML = CONFIG.designs.map(d => `
        <a href="${d.link}" class="design-card fade-in" target="_blank" rel="noopener">
            <div class="design-image">
                ${d.image
                    ? `<img src="${d.image}" alt="${escapeHtml(d.title)}" loading="lazy" />`
                    : `<div class="design-image-placeholder"><i class="fa-solid fa-palette"></i></div>`
                }
            </div>
            <div class="design-info">
                <span class="design-category">${escapeHtml(d.category)}</span>
                <h3 class="design-title">${escapeHtml(d.title)}</h3>
                <p class="design-description">${escapeHtml(d.description)}</p>
                <div class="design-footer">
                    <span>${escapeHtml(d.date)}</span>
                    <span class="design-link">Görüntüle <i class="fa-solid fa-arrow-right"></i></span>
                </div>
            </div>
        </a>
    `).join('');
}

/* ============================================
   GITHUB PROJELER
   ============================================ */
const projectsGrid = document.getElementById('projectsGrid');
const githubProfileLink = document.getElementById('githubProfileLink');

if (githubProfileLink && CONFIG.githubUsername) {
    githubProfileLink.href = `https://github.com/${CONFIG.githubUsername}`;
}

async function loadGitHubProjects() {
    if (!projectsGrid || !CONFIG.githubUsername || CONFIG.githubUsername === 'github') {
        showProjectsMessage('GitHub kullanıcı adınızı js/script.js içinde CONFIG.githubUsername alanına ekleyin.');
        return;
    }

    try {
        const res = await fetch(
            `https://api.github.com/users/${CONFIG.githubUsername}/repos?sort=updated&per_page=100`
        );

        if (!res.ok) throw new Error(`GitHub API hatası: ${res.status}`);

        const repos = await res.json();

        // Fork olmayan, açıklaması olan repoları öncelikli al
        const filtered = repos
            .filter(r => !r.fork)
            .sort((a, b) => b.stargazers_count - a.stargazers_count || new Date(b.updated_at) - new Date(a.updated_at))
            .slice(0, 6);

        if (filtered.length === 0) {
            showProjectsMessage('Henüz görüntülenecek proje bulunmuyor.');
            return;
        }

        projectsGrid.innerHTML = filtered.map(renderProjectCard).join('');
        observeFadeIns();
    } catch (err) {
        console.error(err);
        showProjectsMessage('Projeler yüklenirken bir hata oluştu. GitHub kullanıcı adınızı kontrol edin.');
    }
}

function renderProjectCard(repo) {
    const desc = repo.description || 'Bu proje için henüz bir açıklama eklenmemiş.';
    const lang = repo.language || 'Diğer';
    const langColor = CONFIG.languageColors[lang] || 'var(--accent)';

    return `
        <div class="project-card fade-in">
            <div class="project-header">
                <div class="project-icon"><i class="fa-solid fa-code-branch"></i></div>
                <div class="project-links">
                    <a href="${repo.html_url}" target="_blank" rel="noopener" aria-label="GitHub">
                        <i class="fa-brands fa-github"></i>
                    </a>
                    ${repo.homepage ? `
                        <a href="${repo.homepage}" target="_blank" rel="noopener" aria-label="Demo">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i>
                        </a>` : ''
                    }
                </div>
            </div>
            <h3 class="project-name">${escapeHtml(repo.name)}</h3>
            <p class="project-description">${escapeHtml(desc)}</p>
            <div class="project-meta">
                <span class="project-language">
                    <span class="language-dot" style="background: ${langColor}"></span>
                    ${escapeHtml(lang)}
                </span>
                <span class="project-meta-item">
                    <i class="fa-regular fa-star"></i> ${repo.stargazers_count}
                </span>
                <span class="project-meta-item">
                    <i class="fa-solid fa-code-fork"></i> ${repo.forks_count}
                </span>
            </div>
        </div>
    `;
}

function showProjectsMessage(message) {
    if (!projectsGrid) return;
    projectsGrid.innerHTML = `
        <div class="error-message">
            <i class="fa-solid fa-circle-info" style="font-size: 1.5rem; margin-bottom: 8px; display: block;"></i>
            ${escapeHtml(message)}
        </div>
    `;
}

loadGitHubProjects();

/* ============================================
   FORM — FormSubmit AJAX ile e-posta gönderimi
   Form action="https://formsubmit.co/korhanergunt2@gmail.com" üzerinden çalışır.
   İLK KEZ kullanıldığında FormSubmit aktivasyon e-postası gönderir;
   gelen e-postadaki linke bir kez tıkladıktan sonra tüm gönderimler
   doğrudan korhanergunt2@gmail.com adresine düşer.
   ============================================ */
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    const submitBtn = document.getElementById('contactSubmit');
    const status = document.getElementById('formStatus');
    const btnLabel = submitBtn ? submitBtn.querySelector('.btn-label') : null;
    const originalLabel = btnLabel ? btnLabel.textContent : 'Gönder';

    const setStatus = (type, message) => {
        if (!status) return;
        status.className = `form-status ${type}`;
        status.textContent = message;
    };

    contactForm.addEventListener('submit', async e => {
        e.preventDefault();

        // Honeypot doluysa (bot) sessizce yoksay
        if (contactForm._honey && contactForm._honey.value) return;

        const action = contactForm.getAttribute('action');
        const data = new FormData(contactForm);

        if (submitBtn) {
            submitBtn.disabled = true;
            if (btnLabel) btnLabel.textContent = 'Gönderiliyor...';
        }
        setStatus('loading', 'Mesajınız gönderiliyor...');

        try {
            const res = await fetch(action, {
                method: 'POST',
                body: data,
                headers: { 'Accept': 'application/json' }
            });

            if (res.ok) {
                setStatus('success', 'Mesajınız iletildi — en kısa sürede dönüş yapacağım. Teşekkürler!');
                contactForm.reset();
            } else {
                let msg = 'Mesaj gönderilemedi. Lütfen daha sonra tekrar deneyin.';
                try {
                    const json = await res.json();
                    if (json && json.message) msg = json.message;
                } catch (_) { /* ignore */ }
                setStatus('error', msg);
            }
        } catch (err) {
            console.error(err);
            setStatus('error', 'Bağlantı hatası. İnternet bağlantınızı kontrol edip tekrar deneyin.');
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                if (btnLabel) btnLabel.textContent = originalLabel;
            }
        }
    });
}

/* ============================================
   FADE-IN GÖZLEMCİSİ
   ============================================ */
function observeFadeIns() {
    const targets = document.querySelectorAll('.fade-in:not(.visible)');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

    targets.forEach(t => observer.observe(t));
}

// Timeline elementlerine de fade-in ekle
document.querySelectorAll('.timeline-item, .about-grid > *, .contact-grid > *').forEach(el => {
    el.classList.add('fade-in');
});

observeFadeIns();

/* ============================================
   YIL
   ============================================ */
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* ============================================
   YARDIMCI
   ============================================ */
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/* ============================================
   ARKA PLAN GÖRSELİ — assets/images/ içinde background.* dosyası bulunursa
   otomatik olarak saydam şekilde yüklenir. Birden fazla uzantı denenir.
   ============================================ */
(function tryLoadBackground() {
    const overlay = document.getElementById('bgOverlay');
    if (!overlay) return;

    const candidates = [
        'assets/images/background.png',
        'assets/images/background.jpg',
        'assets/images/background.jpeg',
        'assets/images/background.webp',
        'assets/images/background.png.jpg',
        'assets/images/background.jpg.png'
    ];

    const tryNext = i => {
        if (i >= candidates.length) return;
        const img = new Image();
        img.onload = () => {
            overlay.style.backgroundImage = `url('${candidates[i]}')`;
        };
        img.onerror = () => tryNext(i + 1);
        img.src = candidates[i];
    };

    tryNext(0);
})();
