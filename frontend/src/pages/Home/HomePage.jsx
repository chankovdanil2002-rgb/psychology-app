import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSpecializations } from '../../api';
import Loader from '../../components/ui/Loader';
import { extractList } from '../../utils/helpers';
import styles from './HomePage.module.css';

const STEPS = [
  { num: '1', title: 'Выберите специализацию', desc: 'Определите, какой тип помощи вам нужен' },
  { num: '2', title: 'Выберите психолога', desc: 'Изучите профили и отзывы специалистов' },
  { num: '3', title: 'Выберите время', desc: 'Найдите удобный слот в расписании' },
  { num: '4', title: 'Запишитесь', desc: 'Подтвердите запись и ждите одобрения' },
];

export default function HomePage() {
  const [specializations, setSpecializations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSpecializations()
      .then((res) => {
        const data = extractList(res);
        setSpecializations(data.slice(0, 6));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className={styles.home}>
      {/* Главный баннер */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>Запишитесь на консультацию к психологу</h1>
          <p>Профессиональная помощь онлайн. Подберите специалиста, удобное время и запишитесь в несколько кликов.</p>
          <div className={styles.heroActions}>
            <Link to="/booking" className={styles.ctaPrimary}>Записаться</Link>
            <Link to="/catalog" className={styles.ctaSecondary}>Каталог психологов</Link>
          </div>
        </div>
      </section>

      {/* Специализации */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Направления</h2>
        {loading ? (
          <Loader />
        ) : (
          <div className={styles.specGrid}>
            {specializations.map((s) => (
              <Link to={`/catalog?specialization=${s.slug}`} key={s.id} className={styles.specCard}>
                <h3>{s.name}</h3>
                {s.description && <p>{s.description}</p>}
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Как это работает */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Как это работает</h2>
        <div className={styles.stepsGrid}>
          {STEPS.map((step) => (
            <div key={step.num} className={styles.stepCard}>
              <div className={styles.stepNum}>{step.num}</div>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
