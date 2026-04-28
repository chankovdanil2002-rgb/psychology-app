import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSpecializations } from '../../api';
import { extractList } from '../../utils/helpers';
import styles from './HomePage.module.css';

/* Иконки направлений */
const SPEC_ICONS = ['🧠', '😰', '🌊', '👨‍👩‍👧', '🎓', '💎', '🧭', '🔥', '💞', '🆘', '🕊️', '🌱', '📋', '🎨', '🛡️'];

const STEPS = [
  { num: '01', icon: '🔍', title: 'Выберите направление', desc: 'Определите, какой тип помощи нужен именно вам' },
  { num: '02', icon: '👤', title: 'Найдите психолога', desc: 'Изучите профили, отзывы и специализации' },
  { num: '03', icon: '📅', title: 'Запишитесь онлайн', desc: 'Выберите удобный слот в расписании специалиста' },
  { num: '04', icon: '✅', title: 'Начните работу', desc: 'Получите подтверждение и встретьтесь с психологом' },
];

const STATS = [
  { value: '29', label: 'специалистов', suffix: '' },
  { value: '15', label: 'направлений', suffix: '' },
  { value: '98', label: 'довольных клиентов', suffix: '%' },
  { value: '24', label: 'часа на связи', suffix: '/7' },
];

/* Хук для отслеживания прогресса скролла */
function useScrollProgress() {
  const [scrollY, setScrollY] = useState(0);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const onScroll = () => {
      const sy = window.scrollY;
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      setScrollY(sy);
      setScrollProgress(totalHeight > 0 ? sy / totalHeight : 0);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return { scrollY, scrollProgress };
}

/* Хук для наблюдения за появлением элемента во вьюпорте */
function useReveal(threshold = 0.15) {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); obs.disconnect(); } },
      { threshold }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [threshold]);

  return { ref, visible };
}

export default function HomePage() {
  const [specializations, setSpecializations] = useState([]);
  const { scrollY, scrollProgress } = useScrollProgress();

  const specsReveal  = useReveal(0.1);
  const stepsReveal  = useReveal(0.1);
  const statsReveal  = useReveal(0.2);
  const ctaReveal    = useReveal(0.2);

  useEffect(() => {
    getSpecializations()
      .then((res) => setSpecializations(extractList(res).slice(0, 6)))
      .catch(() => {});
  }, []);

  /* Параллакс для hero-контента — движется медленнее страницы */
  const heroParallax = Math.min(scrollY * 0.4, 200);
  /* Прозрачность hero при скролле */
  const heroOpacity  = Math.max(1 - scrollY / 500, 0);

  return (
    <div className={styles.home}>
      {/* ─── Полоса прогресса скролла ─── */}
      <div
        className={styles.scrollBar}
        style={{ width: `${scrollProgress * 100}%` }}
      />

      {/* ─── HERO ─── */}
      <section className={styles.hero}>
        {/* Декоративные орбы, смещаются при скролле */}
        <div
          className={`${styles.orb} ${styles.orb1}`}
          style={{ transform: `translateY(${scrollY * 0.25}px) scale(${1 + scrollY * 0.0003})` }}
        />
        <div
          className={`${styles.orb} ${styles.orb2}`}
          style={{ transform: `translateY(${scrollY * 0.15}px) translateX(${scrollY * -0.08}px)` }}
        />
        <div
          className={`${styles.orb} ${styles.orb3}`}
          style={{ transform: `translateY(${scrollY * 0.35}px) translateX(${scrollY * 0.06}px)` }}
        />

        {/* Сетка-паттерн поверх градиента */}
        <div className={styles.heroGrid} />

        {/* Контент hero — движется медленнее при скролле */}
        <div
          className={styles.heroContent}
          style={{
            transform: `translateY(${heroParallax}px)`,
            opacity: heroOpacity,
          }}
        >
          <span className={styles.heroBadge}>Психологическая помощь</span>
          <h1 className={styles.heroTitle}>
            Найди своего
            <span className={styles.heroAccent}> психолога </span>
            среди студентов ИППС СФУ
          </h1>
          <p className={styles.heroSubtitle}>
            Молодые специалисты с горящими глазами и современными подходами.
            Запишитесь за несколько минут — без очередей и бюрократии.
          </p>
          <div className={styles.heroActions}>
            <Link to="/booking" className={styles.ctaPrimary}>
              Записаться сейчас
            </Link>
            <Link to="/catalog" className={styles.ctaSecondary}>
              Смотреть психологов
            </Link>
          </div>
        </div>

        {/* Волна внизу hero */}
        <div className={styles.heroWave}>
          <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
            <path d="M0,40 C360,80 1080,0 1440,40 L1440,80 L0,80 Z" fill="var(--color-bg)" />
          </svg>
        </div>
      </section>

      {/* ─── СТАТИСТИКА ─── */}
      <div
        ref={statsReveal.ref}
        className={`${styles.statsRow} ${statsReveal.visible ? styles.revealed : ''}`}
      >
        {STATS.map((s, i) => (
          <div
            key={i}
            className={styles.statItem}
            style={{ transitionDelay: `${i * 80}ms` }}
          >
            <span className={styles.statValue}>
              {s.value}<span className={styles.statSuffix}>{s.suffix}</span>
            </span>
            <span className={styles.statLabel}>{s.label}</span>
          </div>
        ))}
      </div>

      {/* ─── НАПРАВЛЕНИЯ ─── */}
      <section
        ref={specsReveal.ref}
        className={`${styles.section} ${specsReveal.visible ? styles.revealed : ''}`}
      >
        <div className={styles.sectionHeader}>
          <span className={styles.sectionBadge}>Что вас беспокоит?</span>
          <h2 className={styles.sectionTitle}>Направления помощи</h2>
          <p className={styles.sectionSub}>
            Выберите тему — мы подберём подходящего специалиста
          </p>
        </div>

        <div className={styles.specGrid}>
          {specializations.map((s, i) => (
            <Link
              to={`/catalog?specialization=${s.slug}`}
              key={s.id}
              className={styles.specCard}
              style={{ transitionDelay: `${i * 60}ms` }}
            >
              <span className={styles.specIcon}>{SPEC_ICONS[i] ?? '✨'}</span>
              <h3 className={styles.specName}>{s.name}</h3>
              {s.description && (
                <p className={styles.specDesc}>{s.description}</p>
              )}
              <span className={styles.specArrow}>→</span>
            </Link>
          ))}
        </div>

        <div className={styles.sectionCta}>
          <Link to="/catalog" className={styles.linkMore}>
            Все направления →
          </Link>
        </div>
      </section>

      {/* ─── КАК ЭТО РАБОТАЕТ ─── */}
      <section
        ref={stepsReveal.ref}
        className={`${styles.stepsSection} ${stepsReveal.visible ? styles.revealed : ''}`}
      >
        <div className={styles.sectionHeader}>
          <span className={styles.sectionBadge}>Просто и быстро</span>
          <h2 className={styles.sectionTitle}>Как это работает</h2>
        </div>

        <div className={styles.stepsGrid}>
          {STEPS.map((step, i) => (
            <div
              key={step.num}
              className={styles.stepCard}
              style={{ transitionDelay: `${i * 100}ms` }}
            >
              <div className={styles.stepTop}>
                <span className={styles.stepNum}>{step.num}</span>
                <span className={styles.stepIcon}>{step.icon}</span>
              </div>
              <h3 className={styles.stepTitle}>{step.title}</h3>
              <p className={styles.stepDesc}>{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section
        ref={ctaReveal.ref}
        className={`${styles.ctaSection} ${ctaReveal.visible ? styles.revealed : ''}`}
      >
        <div className={styles.ctaOrb1} />
        <div className={styles.ctaOrb2} />
        <div className={styles.ctaInner}>
          <h2 className={styles.ctaTitle}>Готовы сделать первый шаг?</h2>
          <p className={styles.ctaText}>
            Это сложнее всего — но вы уже здесь. Выберите психолога и запишитесь прямо сейчас.
          </p>
          <Link to="/booking" className={styles.ctaBig}>
            Начать сейчас
          </Link>
        </div>
      </section>
    </div>
  );
}
