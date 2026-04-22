import { useCallback, useEffect, useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getPsychologists, getSpecializations } from '../../api';
import Loader from '../../components/ui/Loader';
import Pagination from '../../components/ui/Pagination';
import StarRating from '../../components/ui/StarRating';
import { extractData, extractList, formatPrice, truncateText } from '../../utils/helpers';
import styles from './CatalogPage.module.css';

export default function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [psychologists, setPsychologists] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalPages, setTotalPages] = useState(1);
  const [filtersOpen, setFiltersOpen] = useState(false);

  const currentPage = parseInt(searchParams.get('page') || '1', 10);
  const search = searchParams.get('search') || '';
  const ordering = searchParams.get('ordering') || '-average_rating';
  const specFilter = searchParams.get('specialization') || '';

  const searchRef = useRef(null);
  const debounceRef = useRef(null);

  // Загружаем специализации один раз
  useEffect(() => {
    getSpecializations()
      .then((res) => {
        const data = extractList(res);
        setSpecializations(data);
      })
      .catch(() => {});
  }, []);

  // Перезагружаем психологов при изменении фильтра
  useEffect(() => {
    setLoading(true);
    const params = { page: currentPage, ordering };
    if (search) params.search = search;
    if (specFilter) params.specialization = specFilter;

    getPsychologists(params)
      .then((res) => {
        const d = extractData(res);
        // Обрабатываем как постраничный, так и прямой ответ
        if (d?.results) {
          setPsychologists(d.results);
          setTotalPages(Math.ceil((d.count || 0) / 12));
        } else {
          setPsychologists(Array.isArray(d) ? d : []);
          setTotalPages(1);
        }
      })
      .catch(() => setPsychologists([]))
      .finally(() => setLoading(false));
  }, [currentPage, search, ordering, specFilter]);

  const updateParam = useCallback(
    (key, value) => {
      const params = new URLSearchParams(searchParams);
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      if (key !== 'page') params.set('page', '1');
      setSearchParams(params);
    },
    [searchParams, setSearchParams]
  );

  const handleSearchInput = (e) => {
    const val = e.target.value;
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => updateParam('search', val), 300);
  };

  return (
    <div className={styles.catalog}>
      <h1 className={styles.title}>Каталог психологов</h1>

      {/* Верхняя панель */}
      <div className={styles.topBar}>
        <input
          ref={searchRef}
          className={styles.searchInput}
          type="text"
          placeholder="Поиск по имени..."
          defaultValue={search}
          onChange={handleSearchInput}
        />
        <select
          className={styles.sortSelect}
          value={ordering}
          onChange={(e) => updateParam('ordering', e.target.value)}
        >
          <option value="-average_rating">По рейтингу</option>
          <option value="price">Цена: по возрастанию</option>
          <option value="-price">Цена: по убыванию</option>
          <option value="-experience_years">По опыту</option>
        </select>
        <button
          className={styles.filterToggle}
          onClick={() => setFiltersOpen(!filtersOpen)}
        >
          Фильтры {filtersOpen ? '▲' : '▼'}
        </button>
      </div>

      <div className={styles.content}>
        {/* Боковая панель */}
        <aside className={`${styles.sidebar} ${filtersOpen ? styles.sidebarOpen : ''}`}>
          <h3>Специализации</h3>
          <div className={styles.filterList}>
            <label className={styles.filterItem}>
              <input
                type="radio"
                name="spec"
                checked={!specFilter}
                onChange={() => updateParam('specialization', '')}
              />
              Все
            </label>
            {specializations.map((s) => (
              <label key={s.id} className={styles.filterItem}>
                <input
                  type="radio"
                  name="spec"
                  checked={specFilter === s.slug}
                  onChange={() => updateParam('specialization', s.slug)}
                />
                {s.name}
              </label>
            ))}
          </div>
        </aside>

        {/* Карточки */}
        <main className={styles.main}>
          {loading ? (
            <Loader />
          ) : psychologists.length === 0 ? (
            <p className={styles.empty}>Психологи не найдены</p>
          ) : (
            <>
              <div className={styles.grid}>
                {psychologists.map((p) => (
                  <Link to={`/psychologists/${p.id}`} key={p.id} className={styles.card}>
                    <div className={styles.cardPhoto}>
                      {p.photo ? (
                        <img src={p.photo} alt={p.full_name} />
                      ) : (
                        <div className={styles.photoPlaceholder}>
                          {(p.full_name || '?')[0]}
                        </div>
                      )}
                    </div>
                    <div className={styles.cardBody}>
                      <h3 className={styles.cardName}>{p.full_name}</h3>
                      {p.specializations && (
                        <p className={styles.cardSpecs}>
                          {(Array.isArray(p.specializations)
                            ? p.specializations
                            : []
                          ).join(', ')}
                        </p>
                      )}
                      <div className={styles.cardRating}>
                        <StarRating value={p.average_rating || 0} size="sm" showValue />
                        <span className={styles.reviewCount}>({p.total_reviews || 0})</span>
                      </div>
                      {p.bio && <p className={styles.cardBio}>{truncateText(p.bio, 100)}</p>}
                      <div className={styles.cardFooter}>
                        {p.experience_years && (
                          <span>Опыт: {p.experience_years} лет</span>
                        )}
                        <span className={styles.cardPrice}>{formatPrice(p.price)}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={(p) => updateParam('page', String(p))}
              />
            </>
          )}
        </main>
      </div>
    </div>
  );
}
